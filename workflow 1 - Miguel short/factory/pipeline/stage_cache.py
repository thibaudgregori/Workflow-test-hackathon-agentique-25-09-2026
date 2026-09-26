"""Reuse a completed agent stage only while its inputs and artifacts match."""
from pathlib import Path
import argparse, hashlib, json, re, sys
F=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(F/'pipeline/matting'))
from selection import digest, atomic_json


def fingerprint(run,label):
    run=Path(run);files=[F/'PRODUCTION.md',F/'STANDARD.md',F.parents[3]/'.claude/workflows/daily-shorts.js',run/'prep/_intake.json']
    files += [F/'pipeline'/p for p in ('production.py','visual_laws.py','geometry_audit.py','stage_cache.py','matting/client.py','matting/selection.py','matting/headroom.py','prep/platelib.py')]
    if label.startswith('deliver_'):
        files += [F/'pipeline/deliver'/p for p in ('short_package.py','push_run_to_drive.py','README.md')]
        files += list((run/'delivery').glob('*.json'))
        files += list((run/'review').glob('final_*.json'))
    files += [p for p in (run/'intake').rglob('*') if p.is_file() and p.suffix in ('.json','.md','.txt')]
    intake=json.loads((run/'prep/_intake.json').read_text()) if (run/'prep/_intake.json').exists() else []
    for row in intake:
        vid=row['id']
        if vid not in label:continue
        files += [run/'cuts'/vid/'master.mp4',run/'cuts'/vid/'transcript_tight.json']
        if not label.startswith('plan_'):files += [run/'plans'/f'{vid}_plan.json']
        if label.startswith(('split_','cutout_','whiteboard_')):
            files += [run/'plans'/f'{vid}_scene_handoff.md',run/'gen'/f'{vid}_scene.py']
            fmt=label.split('_')[0]
            project=run/'projects'/f'{vid}_{fmt}'
            files += [p for p in project.rglob('*') if p.is_file() and 'node_modules' not in p.parts]
            files += list((run/'gen').glob(vid+'*.py'))
            if fmt=='cutout':files += [run/'matting'/vid/'selection.json',run/'matting'/vid/'matting.json']
        if label.startswith('audit_'):
            files += list((run/'staging').glob('*/'+vid+'_*.mp4'))
            files += list((run/'review').glob('phone_pass_'+vid+'_*.json'))
    values=[(str(p),digest(p) if p.is_file() else None) for p in files]
    return hashlib.sha256(json.dumps(values).encode()).hexdigest()


def artifacts(value):
    if isinstance(value,dict):
        for v in value.values():yield from artifacts(v)
    elif isinstance(value,list):
        for v in value:yield from artifacts(v)
    elif isinstance(value,str) and value.startswith('/') and len(value)<1000 and '\n' not in value:
        p=Path(value)
        if p.is_file():yield p


def check(run,label,reseal=False):
    run=Path(run);result=run/'review'/f'agent_done_{label}.json';manifest=result.with_suffix('.cache.json')
    try:
        d=json.loads(manifest.read_text())
        if d['result_sha256']!=digest(result):return {'found':False}
        if d['fingerprint']!=fingerprint(run,label):
            # THE ARTIFACTS ARE THE PROOF (run 20, 2026-09-14): a drifted fingerprint with
            # every artifact still hash-equal is the same finished work under an edited
            # rule file; re-seal it instead of redoing it (a planner rebuilt a sealed
            # scene under two staged renders because platelib.py had been patched).
            if reseal and all(Path(p).is_file() and digest(p)==h for p,h in d['artifacts'].items()):
                save(run,label);return {'found':True,'json':result.read_text(),'resealed':True}
            return {'found':False}
        if any(not Path(p).is_file() or digest(p)!=h for p,h in d['artifacts'].items()):return {'found':False}
        return {'found':True,'json':result.read_text()}
    except (OSError,ValueError,KeyError):return {'found':False}


def save(run,label):
    result=Path(run)/'review'/f'agent_done_{label}.json';d=json.loads(result.read_text())
    atomic_json(result.with_suffix('.cache.json'),{'fingerprint':fingerprint(run,label),
        'result_sha256':digest(result),'artifacts':{str(p):digest(p) for p in artifacts(d)}})
    return {'saved':True}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['check','save']);p.add_argument('--run',type=Path,required=True);p.add_argument('--label',required=True);p.add_argument('--reseal-if-artifacts-match',action='store_true');a=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_]+',a.label):raise ValueError('Invalid stage label')
    print(json.dumps(check(a.run,a.label,reseal=a.reseal_if_artifacts_match) if a.action=='check' else save(a.run,a.label)))
