"""Aligned evidence grids and motion previews for automatic-seed comparisons."""
from pathlib import Path
import json,subprocess,argparse
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
from compare import OUT,FONT,frame,composite
DEST=OUT/'auto-model-benchmark'
CROPS={'shieldstral':(420,0,950,590),'harnessrace':(350,0,870,590),'game33c':(645,0,1175,590)}
MODELS=['birefnet','modnet','mediapipe'];LABELS=['BiRefNet portrait','MODNet','MediaPipe']
def main(tag,images_only=False):
 dest=DEST/'comparisons';dest.mkdir(exist_ok=True);font=ImageFont.truetype(FONT,22);small=ImageFont.truetype(FONT,17)
 for inv in json.loads((OUT/'inventory.json').read_text()):
  v=inv['id'];n=int(inv['plate_metadata']['expect_frames']);indices=[0,100,n//2,n-1];paths=[inv['comparison_baseline_alpha'],OUT/f'results/{v}/matanyone2-speed640/alpha.mkv']+[DEST/m/tag/v/'faceguard/alpha.mkv' for m in MODELS];names=['CURRENT: shipped SAM2','Reviewed-start reference']+LABELS
  for kind in ['outline','full']:
   cw,ch=(350,390) if kind=='outline' else (430,269);sheet=Image.new('RGB',(5*cw,75+4*(ch+27)),(242,240,235));d=ImageDraw.Draw(sheet);d.text((12,10),v.upper()+' | automatic first-frame models | full clips at25fps',font=font,fill='black')
   for j,name in enumerate(names):d.text((j*cw+8,45),name,font=small,fill='black')
   for i,idx in enumerate(indices):
    rgb=frame(inv['plate'],idx)
    for j,path in enumerate(paths):
     alpha=frame(str(path),idx);alpha=cv2.resize(alpha,(rgb.shape[1],rgb.shape[0]),interpolation=cv2.INTER_LINEAR) if alpha.shape[:2]!=rgb.shape[:2] else alpha;im=Image.fromarray(composite(rgb,alpha,rim=False));im=im.crop(CROPS[v]) if kind=='outline' else im;sheet.paste(im.resize((cw,ch),Image.Resampling.LANCZOS),(j*cw,75+i*(ch+27)));d.text((j*cw+8,75+i*(ch+27)+ch+3),f'{idx/25:.2f}s',font=small,fill='black')
   sheet.save(dest/f'{v}-{kind}.png')
  rgb=frame(inv['plate'],0);sheet=Image.new('RGB',(1200,70+2*450),(242,240,235));d=ImageDraw.Draw(sheet)
  for j,(m,name) in enumerate(zip(MODELS,LABELS)):
   d.text((j*400+10,12),name,font=font,fill='black')
   for i,var in enumerate(['raw','faceguard']):
    mask=np.array(Image.open(DEST/m/tag/v/var/'mask.png').convert('L'));im=Image.fromarray(composite(rgb,np.repeat(mask[:,:,None],3,axis=2),rim=False)).crop(CROPS[v]).resize((400,420));sheet.paste(im,(j*400,70+i*450));d.text((j*400+10,48+i*450),'Automatic' if i==0 else '+ face protection',font=small,fill='black')
  sheet.save(dest/f'{v}-seeds-and-guard.png')
  if images_only:print('GRIDS',v,flush=True);continue
  # Same full source clip, three aligned automatic outputs. No repeated random seeks.
  cap=cv2.VideoCapture(inv['plate']);acs=[cv2.VideoCapture(str(DEST/m/tag/v/'faceguard/alpha.mkv')) for m in MODELS];base=Image.new('RGB',(1200,490),(242,240,235));d=ImageDraw.Draw(base)
  for j,name in enumerate(LABELS):d.text((j*400+10,10),name,font=font,fill='black')
  enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1200x490','-r','25','-i','-','-an','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(dest/f'{v}-automatic-comparison.mp4')],stdin=subprocess.PIPE)
  for idx in range(n):
   ok,bgr=cap.read();assert ok;rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB);panel=base.copy()
   for j,ac in enumerate(acs):
    ok,a=ac.read();assert ok;im=Image.fromarray(composite(rgb,a,rim=False)).crop(CROPS[v]).resize((400,446));panel.paste(im,(j*400,44))
   enc.stdin.write(panel.tobytes())
  enc.stdin.close();assert enc.wait()==0;cap.release()
  for ac in acs:ac.release()
  print('COMPARED',v,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--tag',default='r1');p.add_argument('--images-only',action='store_true');a=p.parse_args();main(a.tag,a.images_only)
