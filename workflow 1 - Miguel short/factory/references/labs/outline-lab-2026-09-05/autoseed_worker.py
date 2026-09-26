"""Automatic first-frame selection experiment; never reads reviewed masks."""
import json,subprocess,sys,time,hashlib
from pathlib import Path
import cv2
import numpy as np
import torch
from PIL import Image
from transformers import AutoImageProcessor,AutoModelForSemanticSegmentation

def main(root):
    root=Path(root);torch.set_num_threads(2);cv2.setNumThreads(2);start=time.monotonic()
    processor=AutoImageProcessor.from_pretrained('/opt/models/segformer',local_files_only=True)
    model=AutoModelForSemanticSegmentation.from_pretrained('/opt/models/segformer',local_files_only=True).cuda().eval()
    entries=json.loads((root/'inputs.json').read_text());results=[]
    for entry in entries:
        folder=root/entry['id'];cap=cv2.VideoCapture(str(folder/'video.mp4'));ok,bgr=cap.read();cap.release();assert ok
        rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB);h,w=rgb.shape[:2];t=time.monotonic()
        with torch.inference_mode():
            batch=processor(images=rgb,return_tensors='pt').to('cuda');logits=model(**batch).logits
            logits=torch.nn.functional.interpolate(logits,size=(h,w),mode='bilinear',align_corners=False)
            probs=logits.softmax(1)[0];labels=probs.argmax(0).cpu().numpy()
            person=(1-probs[0]-probs[16]).cpu().numpy()
        seconds=time.monotonic()-t
        original=np.array(Image.open(folder/'original.png').convert('L'))>127
        seeds={'direct':((labels!=0)&(labels!=16)),
               'guided':((original&(person>.15))|(person>.85))}
        for name,mask in seeds.items():
            dest=folder/name;dest.mkdir();Image.fromarray(mask.astype('uint8')*255).save(dest/'mask.png')
            (dest/'video.mp4').symlink_to(folder/'video.mp4')
            assert mask.mean()>.02,'Empty automatically generated person mask'
            spec={'mode':'matanyone2','max_side':640,'limit':200,'precision':'bf16','warmup':10}
            (dest/'spec.json').write_text(json.dumps(spec))
            print('AUTO',entry['id'],name,'seed seconds',round(seconds,3),flush=True)
            proc=subprocess.run(['python','/opt/worker.py',str(dest/'spec.json'),str(dest)],timeout=150)
            if proc.returncode:raise RuntimeError(f'Matting failed for {entry["id"]}/{name}')
            metrics=json.loads((dest/'metrics.json').read_text());metrics.update(video=entry['id'],variant=name,seed_seconds=seconds,seed_sha256=hashlib.sha256((dest/'mask.png').read_bytes()).hexdigest(),original_seed_sha256=hashlib.sha256((folder/'original.png').read_bytes()).hexdigest())
            (dest/'metrics.json').write_text(json.dumps(metrics,indent=2));results.append(metrics)
    (root/'metrics.json').write_text(json.dumps({'results':results,'worker_seconds':time.monotonic()-start,'worker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))

if __name__=='__main__':main(sys.argv[1])
