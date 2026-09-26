"""Build Fable's OWN candidate selection for one recording: initial mask + explicit include/exclude polygons
-> candidate mask, overlays (contour / dark / cream), hashes, machine timestamps. Does NOT approve anything."""
import sys, json, hashlib, argparse
from datetime import datetime, timezone
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent))
from selection import identity, digest
ap=argparse.ArgumentParser(); ap.add_argument('--run',required=True); ap.add_argument('--vid',required=True); ap.add_argument('--edits',required=True,help='JSON list of {operation, points, reason}'); ap.add_argument('--notes',default='')
a=ap.parse_args(); R=Path(a.run); sess=R/'matting'/a.vid; V=R/'matting/_selection_views'; V.mkdir(exist_ok=True)
pkg=json.load(open(R/'prep'/f'{a.vid}.json')); st=pkg['stages']
plate=Path(st['plate']['plate']); source=Path(st['cut']['master']); crop=sess/'plate.json'; base=Path(st['prompt0']['prompt_png'])
ident=identity(plate, source, crop)
cap=cv2.VideoCapture(str(plate)); ok,fr=cap.read(); cap.release(); H,W=fr.shape[:2]
m=cv2.imread(str(base),cv2.IMREAD_GRAYSCALE); m=cv2.resize(m,(W,H),interpolation=cv2.INTER_NEAREST) if m.shape!=(H,W) else m
img=Image.fromarray(m).convert('L'); edits=json.loads(Path(a.edits).read_text()); d=ImageDraw.Draw(img)
for e in edits:
    assert e['operation'] in ('include','exclude') and len(e['points'])>=3
    for x,y in e['points']: assert 0<=x<W and 0<=y<H, ('point outside frame',x,y)
    d.polygon([tuple(p) for p in e['points']], fill=255 if e['operation']=='include' else 0)
cand=sess/'selection_candidate.mask.png'; img.save(cand); mk=(np.asarray(img)>127).astype(np.uint8)
base_mk=(m>127).astype(np.uint8); removed=int(((base_mk==1)&(mk==0)).sum()); added=int(((base_mk==0)&(mk==1)).sum())
rgb=cv2.cvtColor(fr,cv2.COLOR_BGR2RGB)
# overlay with contour
ov=Image.fromarray(rgb).convert('RGBA'); ta=np.zeros((H,W,4),np.uint8); ta[mk==1]=(40,200,90,60); ov=Image.alpha_composite(ov,Image.fromarray(ta)); dd=ImageDraw.Draw(ov)
for c in cv2.findContours(mk,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]:
    pts=[tuple(p[0]) for p in c]
    if len(pts)>2: dd.line(pts+[pts[0]],fill=(255,40,40,255),width=3)
for e in edits:
    dd.polygon([tuple(p) for p in e['points']], outline=(255,220,0,255))
ov.convert('RGB').save(V/f'{a.vid}_candidate_overlay.png')
for name,col in (('dark',(28,28,28)),('cream',(243,238,228))):
    comp=np.empty_like(rgb); comp[:]=col; comp[mk==1]=rgb[mk==1]; Image.fromarray(comp).save(V/f'{a.vid}_candidate_{name}.png')
rec={'version':1,'status':'candidate_needs_parent_review','vid':a.vid,'identity':ident,'base_mask':str(base),'base_mask_sha256':digest(base),
     'candidate_mask':str(cand),'candidate_mask_sha256':digest(cand),'edits':edits,'pixels_removed':removed,'pixels_added':added,
     'mask_area_px':int(mk.sum()),'mask_fraction':round(float(mk.mean()),4),'reviewer':'Fable 5.1 (this session), own first-frame review','notes':a.notes,
     'overlays':{k:str(V/f'{a.vid}_candidate_{k}.png') for k in ('overlay','dark','cream')},'source_sha256':ident['source_sha256'],'crop_sha256':ident['crop_sha256'],
     'created_utc':datetime.now(timezone.utc).isoformat(timespec='microseconds')}
(sess/'selection_candidate.json').write_text(json.dumps(rec,indent=1)); print(json.dumps({k:rec[k] for k in ('vid','pixels_removed','pixels_added','mask_area_px','candidate_mask_sha256','created_utc')}))
