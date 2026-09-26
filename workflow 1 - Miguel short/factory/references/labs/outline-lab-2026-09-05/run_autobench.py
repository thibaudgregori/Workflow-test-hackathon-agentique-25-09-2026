"""Run the authorized model comparison under the shared10-dollar ledger."""
from pathlib import Path
import json,hashlib,time,argparse
from concurrent.futures import ThreadPoolExecutor
import modal
from run_test import OUT,reserve,update
DEST=OUT/'auto-model-benchmark'
def run_one(mode,tag,inputs):
 rid=f'autobench-{mode}-{tag}';dest=DEST/mode/tag;dest.mkdir(parents=True,exist_ok=True)
 reserve(rid,{'app':'shorts-outline-autobench','mode':mode,'videos':3,'variants':['raw','faceguard'],'max_frames':1200,'manual_masks_supplied':False});call=None;t=time.monotonic()
 try:
  call=modal.Function.from_name('shorts-outline-autobench','run').spawn(inputs,mode);update(rid,state='running',call_id=call.object_id);(dest/'call.json').write_text(json.dumps({'call_id':call.object_id,'mode':mode,'at':time.time()},indent=2));print('CALL',mode,call.object_id,flush=True)
  d=call.get(timeout=1100)
  for rel,blob in d.pop('artifacts').items():
   pp=Path(rel);assert not pp.is_absolute() and '..' not in pp.parts and len(pp.parts) in [2,3];p=dest/pp;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(blob)
  d['client_wall_seconds']=time.monotonic()-t;d['conservative_elapsed_estimate_usd']=d['client_wall_seconds']*.00028372;d['local_worker_matches']=d['worker_sha256']==hashlib.sha256((Path(__file__).parent/'autobench_worker.py').read_bytes()).hexdigest();assert d['local_worker_matches'];(dest/'metrics.json').write_text(json.dumps(d,indent=2));update(rid,state='complete',metrics=str(dest/'metrics.json'),estimated_usd=d['conservative_elapsed_estimate_usd']);print('DONE',mode,round(d['client_wall_seconds'],2),round(d['conservative_elapsed_estimate_usd'],4),flush=True);return mode
 except BaseException as e:
  if call:call.cancel(terminate_containers=True)
  update(rid,state='failed',error=str(e),elapsed=time.monotonic()-t);print('FAILED',mode,str(e),flush=True);raise
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--tag',default='r1');p.add_argument('--models',nargs='+',default=['birefnet','modnet','mediapipe']);a=p.parse_args();inputs=[]
 for inv in json.loads((OUT/'inventory.json').read_text()):
  blob=Path(inv['plate']).read_bytes();inputs.append({'id':inv['id'],'video':blob,'video_sha256':hashlib.sha256(blob).hexdigest()})
 with ThreadPoolExecutor(max_workers=3) as pool:
  futures=[pool.submit(run_one,m,a.tag,inputs) for m in a.models]
  errors=[]
  for f in futures:
   try:f.result()
   except Exception as e:errors.append(str(e))
  if errors:raise RuntimeError(errors)
