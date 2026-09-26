"""Budgeted production matting for explicitly reviewed recordings; no auto-retry."""
from pathlib import Path
import argparse,json,time,sys,concurrent.futures
import os
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runs import newest_run
RUN=Path(os.environ['SHORTS_RUN']).expanduser().resolve() if os.environ.get('SHORTS_RUN') else newest_run()  # 2026-09-20: the run is a parameter
from client import execute
from selection import atomic_json
from repair_stage import after_matting

def one(vid):
 d=RUN/'matting'/vid;r=json.loads((d/'ready.json').read_text());start=time.time()
 try:
  res=execute(Path(r['plate']),Path(r['master']),Path(r['crop']),d/'selection.json',Path(r['display']),d,name=vid,resolution=1024,experiment_budget=True)
  rec={'id':vid,'status':'matting_complete_needs_visual_review','started_at':start,'finished_at':time.time(),'matting_client_seconds':time.time()-start,'prep_seconds':r['prep_seconds'],'frames':r['frames'],'duration':r['duration'],'gpu_client_seconds':res['track']['client_wall_seconds'],'gpu_function_seconds':res['track']['function_seconds'],'finish_client_seconds':res['ship']['client_wall_seconds'],'finish_function_seconds':res['ship']['seconds'],'compute_runtime_estimate_usd':res['track']['estimated_compute_usd']+res['ship']['estimated_compute_usd'],'provider_charge_usd':None,'headroom_min_px':res['headroom']['min_top_clearance_px']}
  rec['automatic_repair']=after_matting(vid,d/'alpha_v1.mkv')
 except BaseException as e:
  rec={'id':vid,'status':'HOLD','error':str(e),'started_at':start,'finished_at':time.time(),'matting_client_seconds':time.time()-start}
 atomic_json(d/'run-timing.json',rec);print(json.dumps(rec),flush=True);return rec
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('ids',nargs='+');p.add_argument('--jobs',type=int,default=3);a=p.parse_args()
 if not 1<=a.jobs<=3:raise ValueError('Maximum3 production GPU slots')
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:results=list(ex.map(one,a.ids))
 sys.exit(1 if any(x['status']=='HOLD' for x in results) else 0)
