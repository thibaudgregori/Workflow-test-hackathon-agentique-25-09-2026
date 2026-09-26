"""Reviewed selection -> deployed matting -> deployed soft-alpha export."""
from pathlib import Path
import argparse, hashlib, json, math, sys, time
import modal
from selection import atomic_json, digest, validate

HERE=Path(__file__).resolve().parent


def execute(plate, source, crop, selection, display, output, *, name, resolution=1024,
            precision='bf16', experiment_budget=False):
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    chosen=validate(selection,plate,source,crop)
    ident=chosen['identity']
    spec={'mode':'matanyone2','frames':ident['frames'],'max_side':resolution,'precision':precision,
          'warmup':10,'input_sha256':ident['plate_sha256'],'mask_sha256':chosen['mask_sha256']}
    key=hashlib.sha256(json.dumps({'spec':spec,'source':ident,'worker':digest(HERE/'worker.py'),
        'app':digest(HERE/'modal_app.py'),'ship':digest(HERE.parent/'sam2/ship.py'),
        'display':digest(display)},sort_keys=True).encode()).hexdigest()
    cache=output/'matting-cache'/key; cache.mkdir(parents=True,exist_ok=True)
    def call(stage,kwargs):
        rid='production-'+name+'-'+key[:12]+'-'+stage
        record=cache/(stage+'-call.json')
        if record.exists(): raise RuntimeError('Prior dispatch exists without completion; inspect its call ID before retrying')
        if experiment_budget:
            from budget import reserve,update  # pipeline/matting/budget.py (was the outline lab's run_test, 2026-09-20)
            reserve(rid,{'stage':stage,**spec})
        started=time.monotonic()
        handle=None
        rate=.00028372 if stage=='run' else .00045472
        def accounted(elapsed):
            return max(.02,math.ceil((elapsed+20)*rate*100)/100+.01)
        try:
            # Keep an uncertain dispatch durable even when spawn fails before returning an ID.
            atomic_json(record,{'call_id':None,'key':key,'stage':stage,'status':'dispatching'})
            handle=modal.Function.from_name('shorts-factory-matting',stage).spawn(**kwargs)
            atomic_json(record,{'call_id':handle.object_id,'key':key,'stage':stage,'status':'running'})
            if experiment_budget:update(rid,state='running',call_id=handle.object_id)
            # POLL, DO NOT WAIT 18 MINUTES (2026-09-21): a run takes 67-92 s and a finish 60-160 s
            # (client wall up to 203 s for 1081 frames, measured across runs 17-22). A result that has
            # not arrived after 600 s is lost; fail the stage with the reason so the repair round acts.
            deadline=started+600; result=None
            while result is None:
                try: result=handle.get(timeout=30)
                except TimeoutError:
                    if time.monotonic()>deadline: raise TimeoutError(f'{stage}: no result after 600 s (call {handle.object_id}); the call was cancelled')
                    print(f'[{stage}] waiting {int(time.monotonic()-started)}s ...', flush=True)
            elapsed=time.monotonic()-started; result['client_wall_seconds']=elapsed
            atomic_json(record,{'call_id':handle.object_id,'key':key,'stage':stage,'status':'complete',
                'client_wall_seconds':elapsed,'estimated_compute_usd':result.get('estimated_compute_usd'),
                'provider_charge_usd':None,'cost_basis':'runtime estimate; invoice not fetched'})
            if experiment_budget:update(rid,state='complete',estimated_usd=result.get('estimated_compute_usd'),
                accounted_usd=accounted(elapsed))
            return result
        except BaseException as e:
            cancel_error=None
            if handle is not None:
                try:handle.cancel(terminate_containers=True)
                except BaseException as cancel_exc:cancel_error=str(cancel_exc)
            elapsed=time.monotonic()-started
            failure={'call_id':handle.object_id if handle is not None else None,'key':key,'stage':stage,
                'status':'failed','error':str(e),'cancel_error':cancel_error,'client_wall_seconds':elapsed,
                'provider_charge_usd':None,
                'cost_basis':'unresolved paid attempt; do not count as free or blindly retry'}
            try:atomic_json(record,failure)
            finally:
                if experiment_budget:update(rid,state='failed',error=str(e),cancel_error=cancel_error,
                    accounted_usd=max(.4,accounted(elapsed)))
            raise
    alpha=cache/'alpha.mkv'; metrics=cache/'run.json'
    if metrics.exists():
        r=json.loads(metrics.read_text())
        if not alpha.exists() or digest(alpha)!=r['alpha_sha256']: raise ValueError('Cached alpha damaged')
    else:
        r=call('run',{'video':Path(plate).read_bytes(),'mask':Path(chosen['mask']).read_bytes(),'spec':spec})
        data=r.pop('alpha')
        if hashlib.sha256(data).hexdigest()!=r['alpha_sha256']: raise ValueError('Alpha download hash mismatch')
        if r.get('worker_sha256')!=digest(HERE/'worker.py'): raise ValueError('Deployed worker differs from local production source')
        alpha.write_bytes(data);atomic_json(metrics,r)
    from headroom import check as check_headroom
    headroom=check_headroom(alpha,display,expected_frames=ident['frames'],report=cache/'headroom.json')
    fm=cache/'finish.json'
    if fm.exists():
        f=json.loads(fm.read_text())
        for kind,h in f['hashes'].items():
            if digest(cache/(kind+'.webm'))!=h: raise ValueError('Cached layer damaged')
    else:
        f=call('finish',{'alpha':alpha.read_bytes(),'display':Path(display).read_bytes(),
             'spec':{'frames':ident['frames'],'fps':ident['fps'],'alpha_sha256':digest(alpha),'display_sha256':digest(display)}})
        if f.get('ship_source_sha256')!=digest(HERE.parent/'sam2/ship.py'): raise ValueError('Deployed finishing source differs')
        for kind,b in f.pop('layers').items():
            if hashlib.sha256(b).hexdigest()!=f['hashes'][kind]:raise ValueError('Layer download hash mismatch')
            (cache/(kind+'.webm')).write_bytes(b)
        atomic_json(fm,f)
    # Runtime filenames retain the existing chassis contract; cache remains immutable.
    import shutil
    shutil.copy2(alpha,output/'alpha_v1.mkv')
    outputs={}
    for kind in f['hashes']:
        dest=output/f'matte_{name}_v5_{kind}.webm';shutil.copy2(cache/(kind+'.webm'),dest);outputs[kind]=str(dest)
    rec={'status':'ok','backend':'matanyone2','key':key,'selection':str(selection),'headroom':headroom,
         'track':{k:v for k,v in r.items()},'ship':{**f,'outputs':outputs},'outputs':outputs}
    atomic_json(output/'matting.json',rec)
    atomic_json(output/'ship_v5.json',f | {'outputs':outputs})
    return rec


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ['plate','source','crop','selection','display','output']:p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--name',required=True);p.add_argument('--resolution',type=int,default=1024,choices=[640,1024])
    p.add_argument('--experiment-budget',action='store_true');a=p.parse_args()
    print(json.dumps(execute(a.plate,a.source,a.crop,a.selection,a.display,a.output,name=a.name,
        resolution=a.resolution,experiment_budget=a.experiment_budget),indent=2))


if __name__=='__main__':main()
