"""On-demand three-model benchmark, isolated from all production apps."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,time
import modal
HERE=Path(__file__).resolve().parent
app=modal.App('shorts-outline-autobench')
if modal.is_local():
 cache=HERE.parents[5]/'output/shorts-outline-lab/2026-09-05/auto-model-benchmark'
 image=(modal.Image.from_id('im-073CzHXhHPjGI81w47D7Eo')
  .apt_install('libegl1','libgles2')
  .pip_install('mediapipe==0.10.21','numpy==1.26.4','opencv-python-headless==4.11.0.86')
  .add_local_dir(cache/'models','/opt/autobench-models',copy=True)
  .add_local_file(cache/'model-lock.json','/opt/autobench-lock.json',copy=True)
  .add_local_file(HERE/'autobench_worker.py','/opt/autobench_worker.py',copy=True)
  .run_commands("python -c \"import sys;sys.path.insert(0,'/opt');from autobench_worker import load_model,face_detector; a=load_model('modnet');print('MODNet strict load OK');del a; a=load_model('birefnet');print('BiRefNet load OK');del a;a=load_model('mediapipe');a.close();f=face_detector();f.close();print('MediaPipe OK')\""))
else:image=modal.Image.debian_slim()
@app.function(image=image,gpu='L4',cpu=(2,2),memory=(16384,16384),timeout=900,startup_timeout=180,min_containers=0,max_containers=3,buffer_containers=0,scaledown_window=2,retries=0,single_use_containers=True)
def run(inputs:list,mode:str):
 assert mode in ('birefnet','modnet','mediapipe');assert len(inputs)==3;assert {e['id'] for e in inputs}=={'shieldstral','harnessrace','game33c'};start=time.monotonic()
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);metadata=[]
  for e in inputs:
   assert hashlib.sha256(e['video']).hexdigest()==e['video_sha256'];p=root/e['id'];p.mkdir();(p/'video.mp4').write_bytes(e['video']);metadata.append({'id':e['id'],'video_sha256':e['video_sha256']})
  (root/'inputs.json').write_text(json.dumps(metadata));r=subprocess.run(['python','/opt/autobench_worker.py',str(root),mode],timeout=850)
  if r.returncode:raise RuntimeError('Benchmark worker failed')
  data=json.loads((root/'metrics.json').read_text());data.update(function_seconds=time.monotonic()-start,inputs=metadata,model_lock=json.loads(Path('/opt/autobench-lock.json').read_text()));data['estimated_compute_usd']=data['function_seconds']*.00028372
  data['artifacts']={str(f.relative_to(root)):f.read_bytes() for f in root.rglob('*') if f.is_file() and not f.is_symlink() and f.name in ['alpha.mkv','mask.png','probability.png','face.json','seed-metrics.json','metrics.json'] and f.parent!=root};return data
