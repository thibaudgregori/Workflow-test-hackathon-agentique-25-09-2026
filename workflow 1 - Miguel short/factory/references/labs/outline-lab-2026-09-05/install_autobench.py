"""Download pinned public benchmark dependencies and verify their source digests."""
from pathlib import Path
import requests,json,hashlib,concurrent.futures
ROOT=Path(__file__).resolve().parents[6];OUT=ROOT/'output/shorts-outline-lab/2026-09-05/auto-model-benchmark';CACHE=OUT/'models';CACHE.mkdir(exist_ok=True)
entries=[]
def get(url,dest,expected=None,kind=None):
 dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():
  r=requests.get(url,timeout=180);r.raise_for_status();dest.write_bytes(r.content)
 data=dest.read_bytes();sha=hashlib.sha256(data).hexdigest()
 if expected:
  check=sha if kind=='sha256' else hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert check==expected,(dest,'digest mismatch')
 e=dict(path=str(dest.relative_to(CACHE)),url=url,sha256=sha,bytes=len(data),verified_source_digest=bool(expected));print('VERIFIED',e['path'],e['bytes'],flush=True);return e
repo='ZhengPeng7/BiRefNet-portrait';rev='b6561965a70070d9143fd9e558f6ca3c481510db';url=f'https://huggingface.co/api/models/{repo}/tree/{rev}?recursive=true&expand=false';tree=[]
while url:
 r=requests.get(url,timeout=45);r.raise_for_status();tree+=r.json();url=r.links.get('next',{}).get('url')
(OUT/'birefnet-tree.json').write_text(json.dumps(tree,indent=2))
jobs=[]
for x in tree:
 if x['type']=='file' and x['path'] in ['model.safetensors','config.json','birefnet.py','BiRefNet_config.py','README.md']:
  jobs.append((f'https://huggingface.co/{repo}/resolve/{rev}/{x["path"]}',CACHE/'birefnet'/x['path'],x.get('lfs',{}).get('oid',x['oid']),'sha256' if x.get('lfs') else 'git'))
revmod='28165a451e4610c9d77cfdf925a94610bb2810fb'
for x in json.loads((OUT/'modnet-tree.json').read_text())['tree']:
 if x['type']=='blob' and (x['path'].startswith('src/') or x['path'] in ['LICENSE','demo/video_matting/custom/run.py']):
  jobs.append((f'https://raw.githubusercontent.com/ZHKKKe/MODNet/{revmod}/{x["path"]}',CACHE/'modnet'/x['path'],x['sha'],'git'))
jobs += [
('https://drive.usercontent.google.com/download?id=1Nf1ZxeJZJL8Qx9KadcYYyEmmlKhTADxX&export=download&confirm=t',CACHE/'modnet/model.ckpt',None,None),
('https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/1/selfie_multiclass_256x256.tflite',CACHE/'mediapipe/selfie.tflite',None,None),
('https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task',CACHE/'mediapipe/face.task',None,None)]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for fut in [pool.submit(get,*j) for j in jobs]:entries.append(fut.result())
assert (CACHE/'modnet/model.ckpt').stat().st_size>20_000_000
(OUT/'model-lock.json').write_text(json.dumps(dict(birefnet_revision=rev,modnet_revision=revmod,mediapipe_version='0.10.21',files=entries),indent=2)+'\n')
print('LOCK COMPLETE',flush=True)
