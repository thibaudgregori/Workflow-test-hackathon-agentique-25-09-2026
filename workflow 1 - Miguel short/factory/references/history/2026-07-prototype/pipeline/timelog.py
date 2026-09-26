"""Append a machine-stamped timing event: python timelog.py <run> <stage> <start|end|note> [--mode executed|cached|manual] [--note ...] [--ref path]"""
import sys, json, argparse, hashlib
from datetime import datetime, timezone
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('run'); ap.add_argument('stage'); ap.add_argument('event', choices=['start','end','note'])
ap.add_argument('--mode', default=None); ap.add_argument('--note', default=None); ap.add_argument('--ref', default=None); ap.add_argument('--cost-usd', type=float, default=None); ap.add_argument('--job', default=None)
a=ap.parse_args(); run=Path(a.run); run.mkdir(parents=True, exist_ok=True); f=run/'review'/'timing.jsonl'; f.parent.mkdir(parents=True, exist_ok=True)
rec={'ts': datetime.now(timezone.utc).isoformat(timespec='microseconds'), 'stage': a.stage, 'event': a.event}
for k in ('mode','note','ref','job'):
    v=getattr(a,k)
    if v: rec[k]=v
if a.cost_usd is not None: rec['cost_usd']=a.cost_usd
if a.ref and Path(a.ref).is_file(): rec['ref_sha256']=hashlib.sha256(Path(a.ref).read_bytes()).hexdigest()
if a.event=='end':
    prev=[json.loads(l) for l in f.read_text().splitlines()] if f.exists() else []
    starts=[p for p in prev if p['stage']==a.stage and p['event']=='start']
    if starts: rec['elapsed_s']=round((datetime.fromisoformat(rec['ts'])-datetime.fromisoformat(starts[-1]['ts'])).total_seconds(),3)
with f.open('a') as h: h.write(json.dumps(rec)+'\n')
print(json.dumps(rec))
