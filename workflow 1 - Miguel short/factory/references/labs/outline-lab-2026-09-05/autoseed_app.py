"""One bounded automatic-start comparison, independent of production apps."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,time
import modal

HERE=Path(__file__).resolve().parent
app=modal.App('shorts-outline-autoseed')
if modal.is_local():
    cache=HERE.parents[5]/'output/shorts-outline-lab/2026-09-05/autoseed'
    image=(modal.Image.from_id('im-073CzHXhHPjGI81w47D7Eo')
        .add_local_dir(cache/'models/segformer','/opt/models/segformer',copy=True)
        .add_local_file(cache/'model-lock.json','/opt/autoseed-model-lock.json',copy=True)
        .add_local_file(HERE/'autoseed_worker.py','/opt/autoseed_worker.py',copy=True)
        .run_commands('python -c "from transformers import AutoImageProcessor, AutoModelForSemanticSegmentation; m=AutoModelForSemanticSegmentation.from_pretrained(\'/opt/models/segformer\',local_files_only=True); print(m.config.num_labels)"'))
else:image=modal.Image.debian_slim()

@app.function(image=image,gpu='L4',cpu=(2,2),memory=(16384,16384),timeout=900,startup_timeout=180,min_containers=0,max_containers=1,buffer_containers=0,scaledown_window=2,retries=0,single_use_containers=True)
def run(inputs:list):
    start=time.monotonic();assert len(inputs)==3
    assert {x['id'] for x in inputs}=={'shieldstral','harnessrace','game33c'}
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);metadata=[]
        for entry in inputs:
            folder=root/entry['id'];folder.mkdir()
            for name,key in [('video.mp4','video'),('original.png','mask')]:
                assert hashlib.sha256(entry[key]).hexdigest()==entry[key+'_sha256']
                (folder/name).write_bytes(entry[key])
            metadata.append({k:v for k,v in entry.items() if k not in ('video','mask')})
        (root/'inputs.json').write_text(json.dumps(metadata))
        p=subprocess.run(['python','/opt/autoseed_worker.py',str(root)],timeout=850)
        if p.returncode:raise RuntimeError('Automatic seed batch failed')
        result=json.loads((root/'metrics.json').read_text());result['inputs']=metadata
        result['function_seconds']=time.monotonic()-start
        result['estimated_compute_usd']=result['function_seconds']*.00028372
        result['model_lock']=json.loads(Path('/opt/autoseed-model-lock.json').read_text())
        result['artifacts']={str(f.relative_to(root)):f.read_bytes() for f in root.glob('*/*/*') if f.name in ['mask.png','alpha.mkv','metrics.json']}
        return result
