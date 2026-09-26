"""Reserve the final batch against the existing $10 experiment budget."""
import hashlib,json,time
from pathlib import Path
import modal
from run_test import OUT,reserve,update

def main():
    dest=OUT/'autoseed';rid='automatic-seed-three-video-preview-v1';inputs=[]
    for inv in json.loads((OUT/'inventory.json').read_text()):
        video=Path(inv['plate']).read_bytes();mask=Path(inv['initial_mask']).read_bytes()
        inputs.append({'id':inv['id'],'video':video,'mask':mask,'video_sha256':hashlib.sha256(video).hexdigest(),'mask_sha256':hashlib.sha256(mask).hexdigest()})
    reserve(rid,{'app':'shorts-outline-autoseed','videos':3,'variants':['direct','guided'],'frames_per_preview':200,'manual_masks_supplied':False})
    start=time.monotonic();call=None
    try:
        call=modal.Function.from_name('shorts-outline-autoseed','run').spawn(inputs)
        update(rid,state='running',call_id=call.object_id);(dest/'call.json').write_text(json.dumps({'call_id':call.object_id},indent=2));print('CALL',call.object_id,flush=True)
        result=call.get(timeout=1100)
        for relative,blob in result.pop('artifacts').items():
            parts=Path(relative).parts;assert len(parts)==3 and '..' not in parts
            p=dest/'results'/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(blob)
        result['client_wall_seconds']=time.monotonic()-start;result['conservative_elapsed_estimate_usd']=result['client_wall_seconds']*.00028372
        result['local_worker_matches']=result['worker_sha256']==hashlib.sha256((Path(__file__).parent/'autoseed_worker.py').read_bytes()).hexdigest()
        (dest/'metrics.json').write_text(json.dumps(result,indent=2));update(rid,state='complete',metrics=str(dest/'metrics.json'),estimated_usd=result['conservative_elapsed_estimate_usd']);print(json.dumps({k:v for k,v in result.items() if k not in ('results','model_lock','inputs')},indent=2),flush=True)
    except BaseException as e:
        if call:call.cancel(terminate_containers=True)
        update(rid,state='failed',error=str(e),elapsed=time.monotonic()-start);raise

if __name__=='__main__':main()
