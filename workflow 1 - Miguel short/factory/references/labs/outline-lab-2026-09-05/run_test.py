"""Budgeted, resumable driver. Call only deployed apps; reserve before dispatch."""
import argparse,fcntl,json,time,hashlib,sys
from pathlib import Path
import modal

ROOT=Path(__file__).resolve().parents[6]
OUT=ROOT/'output/shorts-outline-lab/2026-09-05'
LEDGER=OUT/'budget.json'

def reserve(request_id,spec):
    with (OUT/'budget.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        data=json.loads(LEDGER.read_text()) if LEDGER.exists() else {'limit_usd':10,'build_and_overhead_reserve_usd':2,'calls':[]}
        old=next((r for r in data['calls'] if r['id']==request_id),None)
        if old:raise RuntimeError('This request was already dispatched; use saved output or inspect its call ID. No blind retry.')
        if round(data.get('build_and_overhead_reserve_usd',2)*100)+sum(round(x.get('accounted_usd',x['reserved_usd'])*100) for x in data['calls'])+40>round(data['limit_usd']*100):raise RuntimeError('Budget exhausted')
        data['calls'].append({'id':request_id,'reserved_usd':.40,'spec':spec,'state':'reserved','at':time.time()})
        LEDGER.write_text(json.dumps(data,indent=2))

def update(request_id,**fields):
    with (OUT/'budget.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX); data=json.loads(LEDGER.read_text())
        next(x for x in data['calls'] if x['id']==request_id).update(fields)
        LEDGER.write_text(json.dumps(data,indent=2))

def main():
    p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('mode',choices=['matanyone2','sam2matting','vitmatte']);p.add_argument('--tag',default='r1');p.add_argument('--limit',type=int,default=1200);p.add_argument('--max-side',type=int,default=1024);p.add_argument('--variant',default='tiny');p.add_argument('--band',type=int,default=24);p.add_argument('--precision',default='bf16');p.add_argument('--seed',default='reviewed');a=p.parse_args()
    inv=next(x for x in json.loads((OUT/'inventory.json').read_text()) if x['id']==a.video)
    spec={'mode':a.mode,'limit':a.limit,'max_side':a.max_side,'variant':a.variant,'band':a.band,'precision':a.precision}
    dest=OUT/'results'/a.video/f'{a.mode}-{a.tag}';dest.mkdir(parents=True,exist_ok=True)
    if (dest/'metrics.json').exists(): print('CACHED',dest);return
    seed=OUT/'seeds'/f'{a.video}.png' if a.seed=='reviewed' else Path(inv['initial_mask'])
    payload=Path(inv['plate']).read_bytes();mask=seed.read_bytes();baseline=Path(inv['baseline_alpha']).read_bytes() if a.mode=='vitmatte' else b''
    spec['input_sha256']=hashlib.sha256(payload).hexdigest();spec['mask_sha256']=hashlib.sha256(mask).hexdigest()
    spec['baseline_sha256']=hashlib.sha256(baseline).hexdigest() if baseline else None
    rid=f'{a.video}-{a.mode}-{a.tag}';reserve(rid,spec)
    start=time.monotonic();call=None
    try:
        call=modal.Function.from_name('shorts-outline-'+a.mode,'run').spawn(video=payload,mask=mask,spec=spec,baseline=baseline)
        update(rid,state='running',call_id=call.object_id);print('CALL',call.object_id,flush=True)
        (dest/'call.json').write_text(json.dumps({'call_id':call.object_id,'spec':spec},indent=2))
        result=call.get(timeout=1100)
        alpha=result.pop('alpha');assert hashlib.sha256(alpha).hexdigest()==result['alpha_sha256']
        result['local_worker_matches']=result.get('worker_sha256')==hashlib.sha256((Path(__file__).parent/'worker.py').read_bytes()).hexdigest()
        (dest/'alpha.mkv').write_bytes(alpha);result['client_wall_seconds']=time.monotonic()-start
        result['conservative_elapsed_estimate_usd']=result['client_wall_seconds']*.00028372
        (dest/'metrics.json').write_text(json.dumps(result,indent=2));update(rid,state='complete',metrics=str(dest/'metrics.json'),estimated_usd=result['conservative_elapsed_estimate_usd'])
        print(json.dumps(result,indent=2),flush=True)
    except BaseException as e:
        if call:call.cancel(terminate_containers=True)
        update(rid,state='failed',error=str(e),elapsed=time.monotonic()-start)
        raise

if __name__=='__main__':main()
