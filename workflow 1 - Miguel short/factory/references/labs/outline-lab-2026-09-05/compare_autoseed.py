"""Compare automatic starting outlines without modifying any production video."""
from pathlib import Path
import json,subprocess
import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from compare import OUT,FONT,frame,composite

def main():
    root=OUT/'autoseed';dest=root/'comparisons';dest.mkdir(exist_ok=True)
    font=ImageFont.truetype(FONT,21);small=ImageFont.truetype(FONT,17)
    crops={'shieldstral':(420,0,950,590),'harnessrace':(350,0,870,590),'game33c':(645,0,1175,590)}
    for inv in json.loads((OUT/'inventory.json').read_text()):
        v=inv['id'];paths=[None,OUT/'results'/v/'matanyone2-speed640/alpha.mkv',root/'results'/v/'direct/alpha.mkv',root/'results'/v/'guided/alpha.mkv']
        names=['Source','Manual start + MatAnyone','Automatic start + MatAnyone','Automatic + existing outline']
        for kind in ['outline','full']:
            cw,ch=(400,446) if kind=='outline' else (480,300)
            sheet=Image.new('RGB',(4*cw,80+3*(ch+30)),(242,240,235));draw=ImageDraw.Draw(sheet)
            draw.text((15,10),v.upper()+' | automatic starting-outline test | 8-second preview',font=font,fill='black')
            for j,name in enumerate(names):draw.text((j*cw+8,47),name,font=small,fill='black')
            for i,sec in enumerate([0,4,7.8]):
                idx=round(sec*25);rgb=frame(inv['plate'],idx)
                for j,path in enumerate(paths):
                    im=Image.fromarray(rgb if path is None else composite(rgb,frame(path,idx),rim=False))
                    if kind=='outline':im=im.crop(crops[v])
                    y=80+i*(ch+30);sheet.paste(im.resize((cw,ch),Image.Resampling.LANCZOS),(j*cw,y));draw.text((j*cw+8,y+ch+4),f'{sec:.2f}s',font=small,fill='black')
            sheet.save(dest/f'{v}-{kind}.png')
        # Show the actual selection step before the video matting model touches it.
        rgb=frame(inv['plate'],0);sheet=Image.new('RGB',(1600,505),(242,240,235));draw=ImageDraw.Draw(sheet)
        seeds=[Path(inv['initial_mask']),OUT/'seeds'/f'{v}.png',root/'results'/v/'direct/mask.png',root/'results'/v/'guided/mask.png']
        for j,(name,path) in enumerate(zip(['Original automatic','Manually corrected','New automatic selection','New automatic + original'],seeds)):
            mask=np.array(Image.open(path).convert('L'));alpha=np.repeat(mask[:,:,None],3,axis=2)
            im=Image.fromarray(composite(rgb,alpha)).crop(crops[v]).resize((400,446),Image.Resampling.LANCZOS)
            sheet.paste(im,(j*400,50));draw.text((j*400+8,15),name,font=small,fill='black')
        sheet.save(dest/f'{v}-starting-outlines.png')
        print('Saved',v,flush=True)

if __name__=='__main__':main()
