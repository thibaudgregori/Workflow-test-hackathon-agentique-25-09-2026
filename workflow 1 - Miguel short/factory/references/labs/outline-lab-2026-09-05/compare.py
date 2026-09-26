"""Make aligned comparison images and clips from real frames, never generated pixels."""
from pathlib import Path
import argparse,json,subprocess
import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[6]
OUT=ROOT/'output/shorts-outline-lab/2026-09-05'
STYLE=json.loads((ROOT/'assets/templates/documents/outline-comparison.json').read_text())
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def frame(path,index):
    cap=cv2.VideoCapture(str(path));cap.set(cv2.CAP_PROP_POS_FRAMES,index);ok,a=cap.read();cap.release()
    if not ok:raise ValueError(f'Cannot decode {path} frame {index}')
    return cv2.cvtColor(a,cv2.COLOR_BGR2RGB)

def composite(rgb,alpha,rim=False):
    a=alpha[:,:,0].astype('float32')/255
    bg=np.zeros_like(rgb,dtype='float32');bg[:]=STYLE['matte_background']
    if rim:
        d=cv2.dilate((a>.5).astype('uint8'),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))).astype('float32')
        bg=bg*(1-d[:,:,None])+np.array(STYLE['rim_color'])*d[:,:,None]
    return np.rint(rgb*a[:,:,None]+bg*(1-a[:,:,None])).clip(0,255).astype('uint8')

def main():
    p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--tag',default='r1');p.add_argument('--clip',action='store_true');p.add_argument('--selection');p.add_argument('--seconds',help='Comma-separated exact timestamps for additional review');p.add_argument('--speed',action='store_true');p.add_argument('--mobile',action='store_true');p.add_argument('--seed-check',action='store_true');a=p.parse_args()
    inv=next(x for x in json.loads((OUT/'inventory.json').read_text()) if x['id']==a.video)
    variants=[('Source',None),('Current shipped SAM2',Path(inv.get('comparison_baseline_alpha',inv['baseline_alpha'])))]
    selected=json.loads(Path(a.selection).read_text()).get(a.video,{}) if a.selection else {}
    for mode,label in [('vitmatte','SAM2 + ViTMatte'),('sam2matting','SAM2Matting'),('matanyone2','MatAnyone 2')]:
        candidate=OUT/'results'/a.video/selected.get(mode,f'{mode}-{a.tag}')/'alpha.mkv'
        if candidate.exists():variants.append((label,candidate))
    if a.speed:
        variants=[variants[0],variants[1],('MatAnyone 2 / 1024',OUT/'results'/a.video/selected['matanyone2']/'alpha.mkv'),('MatAnyone 2 / 640',OUT/'results'/a.video/'matanyone2-speed640'/'alpha.mkv')]
    if a.mobile:variants=[variants[1],('MatAnyone 2 / 1024',OUT/'results'/a.video/selected['matanyone2']/'alpha.mkv')]
    if a.seed_check:variants=[variants[0],('MatAnyone / original start',OUT/'results'/a.video/'matanyone2-original-seed'/'alpha.mkv'),('MatAnyone / corrected start',OUT/'results'/a.video/selected['matanyone2']/'alpha.mkv')]
    dest=OUT/'comparisons';dest.mkdir(exist_ok=True)
    font=ImageFont.truetype(FONT,22);small=ImageFont.truetype(FONT,17)
    samples={'shieldstral':[0,8.6,18,28],'harnessrace':[0,8,18,36],'game33c':[0,4.5,8.7,20]}[a.video]
    if a.seconds:samples=[float(x) for x in a.seconds.split(',')]
    crop={'shieldstral':(420,0,950,590),'harnessrace':(350,0,870,590),'game33c':(645,0,1175,590)}[a.video]
    for kind in ['outline','full']:
        cw,ch=(370,412) if kind=='outline' else (480,300)
        sheet=Image.new('RGB',(len(variants)*cw,70+len(samples)*(ch+30)),(242,240,235));draw=ImageDraw.Draw(sheet)
        draw.text((14,8),a.video.upper()+' | same frames, same scale',font=font,fill=(25,30,40))
        for col,(name,_) in enumerate(variants):draw.text((col*cw+12,40),name,font=small,fill=(25,30,40))
        for row,sec in enumerate(samples):
            idx=round(sec*25);rgb=frame(inv['plate'],idx)
            for col,(name,path) in enumerate(variants):
                im=rgb if path is None else composite(rgb,frame(path,idx),rim=(kind=='full'))
                im=Image.fromarray(im)
                if kind=='outline':im=im.crop(crop)
                im=im.resize((cw,ch),Image.Resampling.LANCZOS);y=70+row*(ch+30);sheet.paste(im,(col*cw,y));draw.text((col*cw+12,y+ch+4),f'{sec:.2f}s',font=small,fill=(25,30,40))
        sheet.save(dest/f'{a.video}-{kind}-{a.tag}.png')
    if a.clip:
        paths=[inv['plate']]+[str(path) for _,path in (variants if a.mobile else variants[1:])];caps=[cv2.VideoCapture(x) for x in paths]
        n=int(caps[0].get(cv2.CAP_PROP_FRAME_COUNT));cw,ch=(480,534) if a.mobile else (480,300)
        enc=subprocess.Popen(['ffmpeg','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{cw*len(variants)}x{ch+36}','-r','25','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(dest/f'{a.video}-comparison-{a.tag}.mp4')],stdin=subprocess.PIPE)
        for idx in range(n):
            got=[c.read() for c in caps]
            if not all(ok for ok,_ in got):raise ValueError(f'Missing comparison frame {idx}')
            rgb=cv2.cvtColor(got[0][1],cv2.COLOR_BGR2RGB);row=Image.new('RGB',(cw*len(variants),ch+36),(242,240,235));d=ImageDraw.Draw(row)
            for j,(name,_) in enumerate(variants):
                im=composite(rgb,got[j+1][1],rim=False) if a.mobile else (rgb if j==0 else composite(rgb,got[j][1],rim=True))
                im=Image.fromarray(im)
                if a.mobile:im=im.crop(crop)
                row.paste(im.resize((cw,ch)),(j*cw,36));d.text((j*cw+8,8),name+f' | {idx/25:.2f}s',font=small,fill='black')
            enc.stdin.write(np.array(row).tobytes())
        enc.stdin.close();assert enc.wait()==0
        for c in caps:c.release()
    print('Saved comparisons for',a.video)

if __name__=='__main__':main()
