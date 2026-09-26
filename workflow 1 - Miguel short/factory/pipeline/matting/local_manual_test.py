"""Small local manual-seed quality test; no cloud dispatch or production install."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import cv2
import numpy as np
from PIL import Image

W=Path(__file__).resolve().parents[6]
LAB=W/'output/shorts-outline-lab/2026-09-05'
sys.path[:0]=[str(LAB/'vendor/local-matting-deps'),str(LAB/'vendor/MatAnyone2')]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(video,mask,out,device,max_side,warmup,max_frames=100):
    import torch
    from matanyone2 import MatAnyone2,InferenceCore
    from omegaconf import OmegaConf
    from safetensors.torch import load_file
    if out.exists():raise ValueError('Output exists; no blind retry')
    out.mkdir(parents=True)
    torch.set_num_threads(4);cv2.setNumThreads(2)
    start=time.monotonic()
    cap=cv2.VideoCapture(str(video));ow,oh=int(cap.get(3)),int(cap.get(4));fps=cap.get(5);count=int(cap.get(7))
    if not 0 < max_frames <= 5400:raise ValueError('Frame limit must be 1..5400')
    if not 0<count<=max_frames or not 0<fps<=60 or count/fps>180:
        raise ValueError(f'Local input exceeds {max_frames} frames or 180 seconds')
    scale=min(1,max_side/max(ow,oh));w,h=round(ow*scale/2)*2,round(oh*scale/2)*2
    seed=np.asarray(Image.open(mask).convert('L'))
    if seed.shape!=(oh,ow):raise ValueError('Seed and clip geometry differ')
    model_dir=LAB/'models/matanyone2'
    cfg=OmegaConf.create(json.loads((model_dir/'config.json').read_text())['cfg']);cfg.model.pretrained_resnet=False
    model=MatAnyone2(cfg,single_object=True)
    model.load_state_dict(load_file(str(model_dir/'model.safetensors')),strict=True)
    model=model.to(device).eval();processor=InferenceCore(model,device=device)
    load_seconds=time.monotonic()-start
    def tensor(b):return torch.from_numpy(cv2.cvtColor(cv2.resize(b,(w,h)),cv2.COLOR_BGR2RGB)).permute(2,0,1).float().to(device)/255
    def sync():
        if device=='mps':torch.mps.synchronize()
    enc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','gray','-s',f'{ow}x{oh}','-r',str(fps),'-i','pipe:0','-an','-c:v','ffv1','-threads','2',str(out/'alpha.mkv')],stdin=subprocess.PIPE)
    try:
        with torch.inference_mode():
            ok,b=cap.read();assert ok;first=tensor(b)
            seed=cv2.resize(seed,(w,h),interpolation=cv2.INTER_NEAREST)
            processor.step(first,torch.from_numpy((seed>127).astype(np.float32)*255).to(device),objects=[1])
            for i in range(warmup):processor.step(first,first_frame_pred=True)
            sync();warmup_seconds=time.monotonic()-start-load_seconds
            for i in range(count):
                if i:ok,b=cap.read();assert ok
                prob=processor.step(tensor(b),first_frame_pred=(i==0))
                a=processor.output_prob_to_mask(prob).float().cpu().numpy()
                if not np.isfinite(a).all():raise ValueError('Non-finite alpha')
                a=cv2.resize(np.clip(a,0,1),(ow,oh),interpolation=cv2.INTER_LINEAR)
                enc.stdin.write(np.rint(a*255).astype(np.uint8).tobytes())
                if i in (0,45,150):
                    rgba=np.dstack([cv2.cvtColor(b,cv2.COLOR_BGR2RGB),np.rint(a*255).astype(np.uint8)])
                    Image.fromarray(rgba).save(out/f'preview-{i:06d}.png')
                if i%5==0:print('FRAME',i,'SECONDS',round(time.monotonic()-start,2),flush=True)
            sync()
    finally:
        cap.release();enc.stdin.close()
        if enc.wait()!=0:raise RuntimeError('Alpha encoding failed')
    result={'frames':count,'fps':fps,'device':device,'precision':'fp32','max_side':max_side,'warmup':warmup,
        'load_seconds':load_seconds,'warmup_seconds':warmup_seconds,'total_seconds':time.monotonic()-start,
        'video_sha256':sha(video),'mask_sha256':sha(mask),'weights_sha256':sha(model_dir/'model.safetensors'),
        'alpha_sha256':sha(out/'alpha.mkv'),'vendor_revision':subprocess.check_output(['git','-C',str(LAB/'vendor/MatAnyone2'),'rev-parse','HEAD'],text=True).strip(),
        'max_frames':max_frames,'new_cloud_cost_usd':0,'installed':False,'note':'Manual-seed quality trial on local hardware. Not a Modal speed/BF16 parity measurement.'}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('video',type=Path);p.add_argument('mask',type=Path);p.add_argument('out',type=Path)
    p.add_argument('--device',choices=['cpu','mps'],default='mps');p.add_argument('--max-side',type=int,default=1024);p.add_argument('--warmup',type=int,default=10)
    p.add_argument('--max-frames',type=int,default=100,help='Explicitly allow a complete longer local video, up to5400frames/180s')
    a=p.parse_args();run(a.video,a.mask,a.out,a.device,a.max_side,a.warmup,a.max_frames)
