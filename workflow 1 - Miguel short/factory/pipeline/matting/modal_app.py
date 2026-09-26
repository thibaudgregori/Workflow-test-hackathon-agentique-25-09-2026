"""Production person matting and soft-alpha finishing, both on demand."""
from pathlib import Path
import hashlib, importlib.util, json, os, subprocess, sys, tempfile, time
import modal

HERE = Path(__file__).resolve().parent
PIPE = HERE.parent
APP_NAME = 'shorts-factory-matting'
app = modal.App(APP_NAME)
MODEL_REVISION = '40c894a6f68d1f55c86ab0de838d89dc61587930'
RATE_GPU = .000222 + 2*.0000131 + 16*.00000222
RATE_CPU = 32*.0000131 + 16*.00000222

if modal.is_local():
    # Reuse the tested, pinned image layers and weights, not a second download.
    # the pinned image lives beside this file since 2026-09-20 (was loaded out of the outline lab)
    spec = importlib.util.spec_from_file_location('matting_image', HERE/'image.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    gpu_image = mod.image.add_local_file(HERE/'worker.py', '/opt/production_worker.py', copy=True)
    cpu_image = (modal.Image.debian_slim(python_version='3.11')
        .apt_install('ffmpeg','curl','xz-utils','libgl1','libglib2.0-0')
        .pip_install('numpy<3','opencv-python-headless','pillow')
        .run_commands('curl -fsSL https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n9.0-latest-linux64-gpl-9.0.tar.xz -o /tmp/ffmpeg.tar.xz',
            'mkdir -p /opt/ffmpeg && tar -xJf /tmp/ffmpeg.tar.xz -C /opt/ffmpeg --strip-components=1 && rm /tmp/ffmpeg.tar.xz')
        .env({'SHIP_FFMPEG':'/opt/ffmpeg/bin/ffmpeg','SHIP_FFPROBE':'/opt/ffmpeg/bin/ffprobe','OMP_NUM_THREADS':'1'})
        .add_local_file(PIPE/'sam2/ship.py','/opt/finish/ship.py',copy=True)
        .add_local_file(PIPE/'sam2/post.py','/opt/finish/post.py',copy=True))
else:
    gpu_image = cpu_image = modal.Image.debian_slim()


@app.function(image=gpu_image, gpu='L4', cpu=(2,2), memory=(16384,16384),
    timeout=900, startup_timeout=180, min_containers=0, max_containers=3,
    scaledown_window=2, retries=0, single_use_containers=True)
def run(video: bytes, mask: bytes, spec: dict):
    started = time.monotonic()
    if spec.get('mode') != 'matanyone2': raise ValueError('Only MatAnyone 2 is enabled')
    if hashlib.sha256(video).hexdigest() != spec['input_sha256'] or hashlib.sha256(mask).hexdigest() != spec['mask_sha256']:
        raise ValueError('Input hashes do not match reviewed selection')
    if spec.get('precision') not in ('bf16','fp32') or spec.get('max_side') not in (640,1024):
        raise ValueError('Unsupported production precision/resolution')
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp); (p/'video.mp4').write_bytes(video); (p/'mask.png').write_bytes(mask)
        (p/'spec.json').write_text(json.dumps(spec))
        subprocess.run(['python','/opt/production_worker.py',str(p/'spec.json'),str(p)],check=True,timeout=850)
        result=json.loads((p/'metrics.json').read_text())
        if result['frames'] != spec['frames']: raise ValueError('Incomplete video')
        alpha=(p/'alpha.mkv').read_bytes()
    seconds=time.monotonic()-started
    return {**result, 'alpha':alpha, 'alpha_sha256':hashlib.sha256(alpha).hexdigest(),
        'function_seconds':seconds, 'estimated_compute_usd':seconds*RATE_GPU,
        'model_revision':MODEL_REVISION, 'worker_sha256':hashlib.sha256(Path('/opt/production_worker.py').read_bytes()).hexdigest(),
        'cost_note':'Function runtime estimate; startup and scale-down additional, not an invoice.'}


@app.function(image=cpu_image, cpu=(32,32), memory=(16384,16384), timeout=900,
    min_containers=0, max_containers=3, scaledown_window=2, retries=0, single_use_containers=True)
def finish(alpha: bytes, display: bytes, spec: dict):
    started=time.monotonic(); sys.path.insert(0,'/opt/finish')
    from ship import render
    import cv2
    if hashlib.sha256(alpha).hexdigest()!=spec['alpha_sha256'] or hashlib.sha256(display).hexdigest()!=spec['display_sha256']:
        raise ValueError('Finishing input hash mismatch')
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp); (p/'alpha.mkv').write_bytes(alpha); (p/'display.mp4').write_bytes(display)
        rec=render(p/'alpha.mkv',p/'display.mp4',p/'matte',fps=spec['fps'],temporal=1,
                   workers=12,alpha_mode='soft')
        if rec['frames'] != spec['frames']: raise ValueError('Finished frame count mismatch')
        layers={k:Path(v).read_bytes() for k,v in rec['outputs'].items()}
        # Decode alpha with libvpx: the default ffmpeg VP9 decoder drops alpha.
        cmd=['/opt/ffmpeg/bin/ffmpeg','-v','error','-c:v','libvpx-vp9','-i',rec['outputs']['alpha'],
             '-vf','alphaextract','-pix_fmt','gray','-f','rawvideo','pipe:1']
        raw=subprocess.Popen(cmd,stdout=subprocess.PIPE)
        import numpy as np
        count=0; size=rec['width']*rec['height']; minimum=1.; fractional=0
        while True:
            b=raw.stdout.read(size)
            if not b: break
            if len(b)!=size: raise ValueError('Truncated finished alpha frame')
            a=np.frombuffer(b,np.uint8); minimum=min(minimum,float(np.mean(a>127)))
            fractional+=int(np.count_nonzero((a>0)&(a<255))); count+=1
        if raw.wait()!=0 or count!=spec['frames'] or minimum<.02 or not fractional:
            raise ValueError('Finished alpha validation failed')
    seconds=time.monotonic()-started
    return {'status':'ok','frames':count,'width':rec['width'],'height':rec['height'],
        'fps':spec['fps'],'alpha_mode':'soft','rim_px':7,'temporal':1,
        'layers':layers,'hashes':{k:hashlib.sha256(v).hexdigest() for k,v in layers.items()},
        'seconds':seconds,'estimated_compute_usd':seconds*RATE_CPU,
        'fractional_alpha_pixels':fractional,'minimum_person_fraction':minimum,
        'review_status':'needs_final_visual_review',
        'ship_source_sha256':hashlib.sha256(Path('/opt/finish/ship.py').read_bytes()).hexdigest()}
