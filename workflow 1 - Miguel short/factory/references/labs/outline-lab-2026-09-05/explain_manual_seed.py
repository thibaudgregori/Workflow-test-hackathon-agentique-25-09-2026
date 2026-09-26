"""Render evidence diagrams from exact saved coordinates and masks, not generated imagery."""
from pathlib import Path
import json,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[6];OUT=ROOT/'output/shorts-outline-lab/2026-09-05';SRC=OUT/'manual-start-timing';DEST=OUT/'manual-start-walkthrough';DEST.mkdir(exist_ok=True)
steps=json.loads((ROOT/'assets/templates/documents/outline-walkthrough.json').read_text())
p=json.loads((SRC/'shieldstral-provenance.json').read_text());rgb=Image.open(OUT/'shieldstral-00-source.png').convert('RGB');old=np.array(Image.open(p['base_mask']).convert('L'))>127;new=np.array(Image.open(SRC/'shieldstral-mask.png').convert('L'))>127;arr=np.array(rgb);points=[tuple(q) for q in p['points']]
font='/System/Library/Fonts/Supplemental/Arial.ttf';large=ImageFont.truetype(font,42);small=ImageFont.truetype(font,29);tiny=ImageFont.truetype(font,22);label=ImageFont.truetype(font,20)
W,H=1080,1160;crop=(360,140,960,520)
def tint(mask,color,amount=.48):
 a=arr.astype(float).copy();a[mask]=a[mask]*(1-amount)+np.array(color)*amount;return Image.fromarray(a.astype('uint8'))
def panel(im,step,zoom=False):
 out=Image.new('RGB',(W,H),(245,243,238));d=ImageDraw.Draw(out);d.text((35,28),step['title'],font=large,fill=(20,25,30));d.multiline_text((35,96),step['detail'],font=small,fill=(45,50,55),spacing=12)
 if zoom:im=im.crop(crop)
 scale=min(1010/im.width,880/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);out.paste(im,((W-im.width)//2,230+(850-im.height)//2));d.text((35,1110),'Shieldstral | reconstruction from the saved correction',font=tiny,fill=(65,70,75));return out
def drawpoints(n=999,lines=False):
 im=rgb.copy();d=ImageDraw.Draw(im);pts=points[:n]
 if lines and len(pts)>1:d.line(pts,fill=(255,218,35),width=3)
 if lines and n>=len(points):d.line([points[-1],points[0]],fill=(255,218,35),width=3)
 for i,(x,y) in enumerate(pts):
  if 360<x<960 and 140<=y<520:
   d.ellipse((x-3,y-3,x+3,y+3),fill=(255,218,35),outline='black')
   if i in [0,4,8,12,26,30,33,37]:
    dx=-84 if x<700 else 12;d.text((x+dx,y-12),str(i+1),font=label,fill=(255,230,50),stroke_width=2,stroke_fill='black')
 return im
images=[rgb,tint(old,(30,235,120)),drawpoints(),None,Image.fromarray(new.astype('uint8')*255).convert('RGB'),None,Image.fromarray(np.where(new[:,:,None],arr,np.full_like(arr,(36,41,50))))]
im=drawpoints(lines=True);d=ImageDraw.Draw(im)
for box in p['keep_boxes']:d.rectangle(box,outline=(35,205,255),width=5)
d.line((0,180,1440,180),fill=(35,205,255),width=2);images[3]=im
change=arr.copy().astype(float)
for mask,col in [(old&~new,(255,45,65)),(new&~old,(0,220,250))]:change[mask]=change[mask]*.3+np.array(col)*.7
images[5]=Image.fromarray(change.astype('uint8'))
manifest=[]
for i,(im,step) in enumerate(zip(images,steps)):
 f=DEST/f'{i+1:02d}-step.png';panel(im,step,zoom=i in [2,5]).save(f);manifest.append({'file':str(f.relative_to(OUT)),'caption':step['caption']})
# Animate the saved point list: explicitly a reconstruction, not a screen recording.
mp4=DEST/'08-point-construction.mp4'
proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','5','-i','-','-an','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],stdin=subprocess.PIPE)
for n in list(range(1,len(points)+1))+[len(points)]*12:
 step={'title':'How the point list becomes a line','detail':f'Reconstruction: {n} of {len(points)} saved points.\nThe script joins them in this order.'};frame=panel(drawpoints(n,True),step,zoom=True);proc.stdin.write(frame.tobytes())
proc.stdin.close();assert proc.wait()==0
manifest.append({'file':str(mp4.relative_to(OUT)),'caption':'Animation of the exact saved coordinate list, shown progressively. This is a reconstruction to explain the script, NOT footage of me drawing with a mouse. The line outside the zoomed area continues around the shoulders/body; the final mask also reuses the original cap, body and hands as explained in step 4. Same operation was used for Harness Race and Game33c.'})
(DEST/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(DEST/'README.md').write_text('# Manual correction walkthrough\n\nReconstruction from the exact saved Shieldstral coordinates and masks. No new model calls. Seven numbered images plus an animation; all source images remain unchanged.\n\n'+ '\n'.join(f"- [{Path(x['file']).name}]({Path(x['file']).name}): {x['caption']}" for x in manifest)+'\n');print(DEST)
