"""Automatic outline benchmark; only video bytes enter, never reviewed masks."""
from pathlib import Path
import sys,json,time,hashlib,subprocess,shutil,gc
import numpy as np
import cv2
import torch
from PIL import Image
CACHE=Path('/opt/autobench-models')
def load_model(mode):
 if mode=='birefnet':
  from transformers import AutoModelForImageSegmentation
  m=AutoModelForImageSegmentation.from_pretrained(str(CACHE/'birefnet'),trust_remote_code=True,local_files_only=True).eval();return m
 if mode=='modnet':
  sys.path.insert(0,str(CACHE/'modnet'));from src.models.modnet import MODNet
  m=MODNet(backbone_pretrained=False);weights=torch.load(CACHE/'modnet/model.ckpt',map_location='cpu',weights_only=True);m.load_state_dict({k.removeprefix('module.'):v for k,v in weights.items()},strict=True);return m.eval()
 if mode=='mediapipe':
  import mediapipe as mp
  return mp.tasks.vision.ImageSegmenter.create_from_options(mp.tasks.vision.ImageSegmenterOptions(base_options=mp.tasks.BaseOptions(model_asset_path=str(CACHE/'mediapipe/selfie.tflite')),running_mode=mp.tasks.vision.RunningMode.IMAGE,output_category_mask=True,output_confidence_masks=True))
 raise ValueError(mode)
def predict(model,mode,rgb):
 h,w=rgb.shape[:2]
 if mode=='mediapipe':
  import mediapipe as mp
  r=model.segment(mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb));return 1-r.confidence_masks[0].numpy_view().copy()
 if mode=='birefnet':
  im=Image.fromarray(rgb).resize((1024,1024),Image.Resampling.BILINEAR);a=np.array(im);t=torch.from_numpy(a).permute(2,0,1).float().cuda()/255.;t=(t-t.new_tensor([.485,.456,.406])[:,None,None])/t.new_tensor([.229,.224,.225])[:,None,None]
  with torch.inference_mode():prob=model(t[None])[-1].sigmoid()[0,0]
 else:
  rh,rw=(512,int(w/h*512)) if w>=h else (int(h/w*512),512);rh-=rh%32;rw-=rw%32;a=cv2.resize(rgb,(rw,rh),interpolation=cv2.INTER_AREA);t=torch.from_numpy(a).permute(2,0,1).float().cuda()/127.5-1
  with torch.inference_mode():prob=model(t[None],True)[2][0,0]
 return cv2.resize(prob.float().cpu().numpy(),(w,h),interpolation=cv2.INTER_LINEAR)
def face_detector():
 import mediapipe as mp
 return mp.tasks.vision.FaceLandmarker.create_from_options(mp.tasks.vision.FaceLandmarkerOptions(base_options=mp.tasks.BaseOptions(model_asset_path=str(CACHE/'mediapipe/face.task')),running_mode=mp.tasks.vision.RunningMode.IMAGE,num_faces=1,min_face_detection_confidence=.5,min_face_presence_confidence=.5))
def face_core(detector,rgb):
 import mediapipe as mp
 r=detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb));mask=np.zeros(rgb.shape[:2],np.uint8)
 if not r.face_landmarks:return mask.astype(bool),[]
 h,w=mask.shape;pts=np.array([[round(p.x*w),round(p.y*h)] for p in r.face_landmarks[0]],np.int32);hull=cv2.convexHull(pts);cv2.fillConvexPoly(mask,hull,255);mask=cv2.erode(mask,np.ones((7,7),np.uint8));return mask>0,pts.tolist()
def qa_video(video,alpha,detector):
 cap=cv2.VideoCapture(str(video));ac=cv2.VideoCapture(str(alpha));samples=[];index=0;areas=[]
 while True:
  ok,bgr=cap.read();oka,a=ac.read()
  if not ok:assert not oka;break
  assert oka;areas.append(float(np.mean(a[:,:,0]>127)))
  if index%25==0:
   core,pts=face_core(detector,cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB));samples.append({'frame':index,'face_detected':bool(pts),'face_core_retained':float(np.mean(a[:,:,0][core]>127)) if core.any() else None})
  index+=1
 cap.release();ac.release();return {'frames':index,'face_samples':samples,'foreground_area_fraction_min':min(areas),'foreground_area_fraction_max':max(areas),'area_delta_p95':float(np.percentile(np.abs(np.diff(areas)),95))}
def main(root,mode):
 root=Path(root);start=time.monotonic();torch.set_num_threads(2);cv2.setNumThreads(2);t=time.monotonic();model=load_model(mode)
 if mode!='mediapipe':model=model.cuda();torch.cuda.synchronize()
 load_seconds=time.monotonic()-t;detector=face_detector();entries=json.loads((root/'inputs.json').read_text());results=[]
 # Generate every starting mask before freeing the segmentation model.
 for e in entries:
  folder=root/e['id'];cap=cv2.VideoCapture(str(folder/'video.mp4'));ok,bgr=cap.read();cap.release();assert ok;rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB);t=time.monotonic();prob=predict(model,mode,rgb);seed_seconds=time.monotonic()-t;assert np.isfinite(prob).all();raw=prob>.5;t=time.monotonic();core,points=face_core(detector,rgb);guard_seconds=time.monotonic()-t
  (folder/'face.json').write_text(json.dumps({'landmarks':points,'added_pixels':int(np.sum(core&~raw)),'face_core_pixels':int(core.sum()),'guard_seconds':guard_seconds}))
  for variant,mask in [('raw',raw),('faceguard',raw|core)]:
   dest=folder/variant;dest.mkdir();Image.fromarray(mask.astype('uint8')*255).save(dest/'mask.png');(dest/'video.mp4').symlink_to(folder/'video.mp4');(dest/'seed-metrics.json').write_text(json.dumps({'seed_seconds':seed_seconds,'guard_seconds':guard_seconds,'added_face_pixels':int(np.sum(mask&~raw)),'face_detected':bool(points),'foreground_fraction':float(mask.mean())}));assert mask.mean()>.02
  Image.fromarray(np.rint(prob*255).clip(0,255).astype('uint8')).save(folder/'probability.png');print('SEED',mode,e['id'],round(seed_seconds,3),'face restored',int(np.sum(core&~raw)),flush=True)
 if mode=='mediapipe':model.close()
 del model;gc.collect();torch.cuda.empty_cache()
 for e in entries:
  folder=root/e['id'];raw_metrics=None
  for variant in ['raw','faceguard']:
   dest=folder/variant;seed=json.loads((dest/'seed-metrics.json').read_text());spec={'mode':'matanyone2','max_side':640,'limit':1200,'precision':'bf16','warmup':10};(dest/'spec.json').write_text(json.dumps(spec));same=variant=='faceguard' and (dest/'mask.png').read_bytes()==(folder/'raw/mask.png').read_bytes()
   if same:
    shutil.copyfile(folder/'raw/alpha.mkv',dest/'alpha.mkv');m=dict(raw_metrics);m['reused_identical_raw']=True;m['incremental_matting_seconds']=0
   else:
    t=time.monotonic();proc=subprocess.run(['python','/opt/worker.py',str(dest/'spec.json'),str(dest)],timeout=200)
    if proc.returncode:raise RuntimeError(f'Matting failed:{mode}/{e["id"]}/{variant}')
    m=json.loads((dest/'metrics.json').read_text());m['incremental_matting_seconds']=time.monotonic()-t;m['reused_identical_raw']=False;m['qa']=qa_video(folder/'video.mp4',dest/'alpha.mkv',detector)
   m.update(video=e['id'],model=mode,variant=variant,**seed);m['mask_sha256']=hashlib.sha256((dest/'mask.png').read_bytes()).hexdigest();(dest/'metrics.json').write_text(json.dumps(m,indent=2));results.append(m)
   if variant=='raw':raw_metrics=m
   print('COMPLETE',mode,e['id'],variant,m['frames'],'reused',same,flush=True)
 detector.close();(root/'metrics.json').write_text(json.dumps({'model':mode,'model_load_seconds':load_seconds,'worker_seconds':time.monotonic()-start,'results':results,'worker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main(sys.argv[1],sys.argv[2])
