"""Deploy one of three isolated, on-demand outline experiment applications."""
from pathlib import Path
import os,time,json,hashlib,subprocess,tempfile
import modal

HERE=Path(__file__).resolve().parent
MODEL_CACHE=(HERE.parents[5]/'output/shorts-outline-lab/2026-09-05/models') if modal.is_local() else Path('/opt/models')
MODE=os.environ.get('OUTLINE_MODEL','matanyone2')
assert MODE in ('matanyone2','sam2matting','vitmatte')
app=modal.App('shorts-outline-'+MODE)
if modal.is_local():
    image=(modal.Image.debian_slim(python_version='3.11')
     .apt_install('git','ffmpeg','libgl1','libglib2.0-0')
     .pip_install('torch==2.8.0','torchvision==0.23.0','numpy<3','opencv-python-headless','pillow','tqdm','hydra-core','iopath','einops','scipy','imageio','huggingface_hub==0.36.2','safetensors','kornia','timm','transformers==4.57.1','requests','psutil')
     .run_commands('git clone https://github.com/pq-yang/MatAnyone2.git /opt/MatAnyone2 && cd /opt/MatAnyone2 && git checkout 0079197acd6d16a741f71558809c06c586c579e0',
     'git clone https://github.com/FudanCVL/SAM2Matting.git /opt/SAM2Matting && cd /opt/SAM2Matting && git checkout 73dd721d77b56749248aefe5e8824d7f61b9d13c')
     .env({'PYTHONPATH':'/opt/MatAnyone2:/opt/SAM2Matting','OMP_NUM_THREADS':'2','HF_HUB_OFFLINE':'1'})
     .add_local_file(HERE/'model-lock.json','/opt/model-lock.json',copy=True)
     .add_local_dir(MODEL_CACHE/MODE,'/opt/models/'+MODE,copy=True,
                    ignore=(lambda path:'Base+' in str(path)) if MODE=='sam2matting' and os.environ.get('OUTLINE_INCLUDE_BASE')!='1' else [])
     .run_commands('python -c "from matanyone2 import MatAnyone2; from sam2.build_sam import build_sam2matting_video_predictor; from transformers import VitMatteForImageMatting; print(1)"')
     .add_local_file(HERE/'worker.py','/opt/worker.py',copy=True))
else:
    image=modal.Image.debian_slim()


@app.function(image=image,gpu='L4',cpu=(2,2),memory=(16384,16384),timeout=900,startup_timeout=180,min_containers=0,max_containers=1,buffer_containers=0,scaledown_window=2,retries=0,single_use_containers=True,env={'OUTLINE_MODEL':MODE})
def run(video:bytes,mask:bytes,spec:dict,baseline:bytes=b''):
    start=time.monotonic()
    assert spec['mode']==MODE
    assert 0<spec.get('limit',1200)<=1200
    assert 256<=spec.get('max_side',1024)<=1620
    assert hashlib.sha256(video).hexdigest()==spec['input_sha256']
    assert hashlib.sha256(mask).hexdigest()==spec['mask_sha256']
    if baseline: assert hashlib.sha256(baseline).hexdigest()==spec['baseline_sha256']
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp);(p/'video.mp4').write_bytes(video);(p/'mask.png').write_bytes(mask)
        if baseline:(p/'baseline.mkv').write_bytes(baseline)
        (p/'spec.json').write_text(json.dumps(spec))
        proc=subprocess.run(['python','/opt/worker.py',str(p/'spec.json'),str(p)],timeout=850)
        if proc.returncode:raise RuntimeError(f'Model worker failed: {proc.returncode}')
        result=json.loads((p/'metrics.json').read_text())
        result['function_seconds']=time.monotonic()-start
        result['estimated_compute_usd']=result['function_seconds']*(.000222+2*.0000131+16*.00000222)
        result['cost_note']='Estimate from function runtime; excludes pre-entry startup. Not an invoice.'
        result['model_lock']=json.loads(Path('/opt/model-lock.json').read_text())[MODE]
        result['worker_sha256']=hashlib.sha256(Path('/opt/worker.py').read_bytes()).hexdigest()
        result['alpha']=(p/'alpha.mkv').read_bytes()
        result['alpha_sha256']=hashlib.sha256(result['alpha']).hexdigest()
        return result
