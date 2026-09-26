"""Record wall time for a reviewed first-frame outline; no cloud calls."""
from pathlib import Path
import argparse,json,time,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parents[6]/'output/shorts-outline-lab/2026-09-05'
DEST=OUT/'manual-start-timing'
p=argparse.ArgumentParser();p.add_argument('action',choices=['start','save','finish']);p.add_argument('video');p.add_argument('--points',type=json.loads);p.add_argument('--shoulder-end',type=int,default=600);p.add_argument('--keep-boxes',type=json.loads,default=[]);args=p.parse_args()
log=DEST/'timing.json';data=json.loads(log.read_text());now=time.time()
if args.action=='start':data['events'].append(dict(video=args.video,event='inspection_started',unix=now))
if args.action=='save':
    v=args.video;inv=next(x for x in json.loads((OUT/'inventory.json').read_text()) if x['id']==v)
    rgb=Image.open(OUT/f'{v}-00-source.png').convert('RGB');base=np.array(Image.open(inv['initial_mask']).convert('L'))>127
    polygon=Image.new('L',rgb.size);ImageDraw.Draw(polygon).polygon(args.points,fill=255);shape=np.array(polygon)>0
    mask=base.copy();mask[180:args.shoulder_end] &= shape[180:args.shoulder_end];mask[180:450]=shape[180:450]
    for x0,y0,x1,y1 in args.keep_boxes:mask[y0:y1,x0:x1] |= base[y0:y1,x0:x1]
    seed=Image.fromarray(mask.astype('uint8')*255);seed.save(DEST/f'{v}-mask.png')
    a=np.asarray(rgb);bg=np.full_like(a,(36,41,50));cut=Image.fromarray(np.where(mask[:,:,None],a,bg))
    panel=Image.new('RGB',(rgb.width*2,rgb.height+50),'white');panel.paste(rgb,(0,50));panel.paste(cut,(rgb.width,50));d=ImageDraw.Draw(panel);d.text((20,15),'SOURCE',fill='black');d.text((rgb.width+20,15),'NEW MANUALLY CORRECTED START',fill='black');panel.save(DEST/f'{v}-comparison.png')
    (DEST/f'{v}-provenance.json').write_text(json.dumps(dict(points=args.points,keep_boxes=args.keep_boxes,shoulder_end=args.shoulder_end,base_mask=inv['initial_mask'],procedure='Retain original cap above y180 and lower body below shoulder_end; replace head y180:450 with selected boundary; intersect shoulders y450:shoulder_end',seed_sha256=hashlib.sha256((DEST/f'{v}-mask.png').read_bytes()).hexdigest()),indent=2))
    data['events'].append(dict(video=v,event='mask_saved',unix=time.time(),save_seconds=time.time()-now))
if args.action=='finish':data['events'].append(dict(video=args.video,event='review_completed',unix=now))
log.write_text(json.dumps(data,indent=2)+'\n');print(data['events'][-1])
