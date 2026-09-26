"""Prepare complete, aligned gesture evidence from cached model outputs only."""
import argparse
import json
from pathlib import Path
import time

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from cached_repair import KEYS, digest, composite, save, validate


def run(plan_path, out, start, end):
    started = time.monotonic()
    plan = json.loads(plan_path.read_text())
    width,height,frames,fps = validate(plan)
    if not 0 <= start <= end < frames:
        raise ValueError('Invalid full gesture range')
    out.mkdir(parents=True, exist_ok=False)
    caps=[cv2.VideoCapture(plan['inputs'][k]['path']) for k in KEYS]
    for cap in caps:cap.set(cv2.CAP_PROP_POS_FRAMES,start)
    font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',22)
    # Full width preserves both hands and the source's face/chair context.
    # Panel row 1 shows the exact production rim function; row 2 is light/no rim.
    rows=[];sheets=[]
    try:
        for frame in range(start,end+1):
            reads=[c.read() for c in caps]
            if not all(ok for ok,_ in reads):raise ValueError(f'Missing aligned frame {frame}')
            src=cv2.cvtColor(reads[0][1],cv2.COLOR_BGR2RGB)
            a0=reads[1][1][:,:,0].astype(np.float32)/255
            f0=cv2.cvtColor(reads[2][1],cv2.COLOR_BGR2RGB).astype(np.float32)
            a1=reads[3][1][:,:,0].astype(np.float32)/255
            f1=cv2.cvtColor(reads[4][1],cv2.COLOR_BGR2RGB).astype(np.float32)
            im=Image.new('RGB',(1920,760),'white');d=ImageDraw.Draw(im)
            for i,title in enumerate(['Source','MobileNetV2','ResNet50']):
                d.text((i*640+8,8),f'{title} | frame {frame} ({frame/fps:.2f}s)',fill='black',font=font)
            for row,(bg,rim) in enumerate([(28,True),(240,False)]):
                for col,rgb in enumerate([src,composite(f0,a0,bg,rim),composite(f1,a1,bg,rim)]):
                    im.paste(Image.fromarray(rgb).resize((640,360)),(col*640,40+row*360))
            path=out/f'frame-{frame:04d}.jpg';im.save(path,quality=96)
            rows.append({'frame':frame,'path':str(path.resolve()),'sha256':digest(path)})
            sheets.append(im.resize((1440,570)))
            if len(sheets)==5 or frame==end:
                sheet=Image.new('RGB',(1440,len(sheets)*570),'white')
                for i,p in enumerate(sheets):sheet.paste(p,(0,i*570))
                sheet.save(out/f'sheet-{frame-len(sheets)+1:04d}-{frame:04d}.jpg',quality=95)
                sheets=[]
            if frame%25==0:print('Prepared',frame,flush=True)
    finally:
        for cap in caps:cap.release()
    result={'inputs':plan['inputs'],'frame_range':[start,end],'frames':rows,
            'fps':fps,'seconds':time.monotonic()-started,'new_cloud_cost_usd':0,
            'scope':'Cached predictions only; full-frame source, dark with production rim and light/no rim. No candidate repair or model run.'}
    save(out/'evidence.json',result)
    print(json.dumps({'frames':len(rows),'seconds':result['seconds'],'new_cloud_cost_usd':0}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('plan',type=Path);p.add_argument('out',type=Path)
    p.add_argument('--start',type=int,required=True);p.add_argument('--end',type=int,required=True)
    a=p.parse_args();run(a.plan,a.out,a.start,a.end)
