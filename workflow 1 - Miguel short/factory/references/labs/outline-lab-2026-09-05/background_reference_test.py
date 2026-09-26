"""Single-use Background Matting V2 comparison; original shared $10 budget.

Official TorchScript weights: PeterL1n/BackgroundMattingV2 release v1.0.0.
Full HD source and real matching background; no manual person/hand selection.
"""
from pathlib import Path
import hashlib,json,math,subprocess,tempfile,time
import modal

HERE=Path(__file__).resolve().parent
W=HERE.parents[5] if modal.is_local() else Path('/opt')
OUT=W/'output/shorts-outline-lab/2026-09-05/background-reference-test'
app=modal.App('shorts-outline-background-reference-test')
if modal.is_local():
    image=(modal.Image.from_id('im-073CzHXhHPjGI81w47D7Eo')
           .add_local_dir(OUT/'models','/opt/background-models',copy=True))
else:image=modal.Image.debian_slim()
RATE=.000222+2*.0000131+16*.00000222

@app.function(image=image,gpu='L4',cpu=(2,2),memory=(16384,16384),timeout=240,startup_timeout=120,
              min_containers=0,max_containers=1,buffer_containers=0,scaledown_window=2,retries=0,single_use_containers=True)
def run(video:bytes,background:bytes,spec:dict):
    import cv2,numpy as np,torch,torchvision
    torch.set_num_threads(2);cv2.setNumThreads(1)
    started=time.monotonic()
    if hashlib.sha256(video).hexdigest()!=spec['video_sha256'] or hashlib.sha256(background).hexdigest()!=spec['background_sha256']:raise ValueError('Input hash mismatch')
    if set(spec['models'])-{'mobilenetv2','resnet50'}:raise ValueError('Unsupported model')
    lock=json.loads(Path('/opt/background-models/lock.json').read_text())
    artifacts={};records=[]
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);(root/'source.mp4').write_bytes(video)
        bg=cv2.imdecode(np.frombuffer(background,np.uint8),cv2.IMREAD_COLOR)
        bg=torch.from_numpy(cv2.cvtColor(bg,cv2.COLOR_BGR2RGB)).permute(2,0,1).unsqueeze(0).cuda().half()/255
        h,w=bg.shape[-2:]
        if (w,h)!=(1920,1080) or spec['frames']>1000:raise ValueError('Bounded HD test only')
        def writer(path,gray=False):
            command=['ffmpeg','-v','error','-threads','1','-f','rawvideo','-pix_fmt','gray' if gray else 'rgb24','-s',f'{w}x{h}','-r','25','-i','pipe:0','-an']
            command+=['-c:v','ffv1','-threads','1'] if gray else ['-c:v','libx264','-preset','ultrafast','-crf','17','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart']
            return subprocess.Popen(command+[str(path)],stdin=subprocess.PIPE)
        for name in spec['models']:
            tick=time.monotonic();p=Path('/opt/background-models')/(name+'.pth')
            if hashlib.sha256(p.read_bytes()).hexdigest()!=lock[name]['sha256']:raise ValueError('Model changed')
            model=torch.jit.load(str(p),map_location='cuda').eval()
            model.backbone_scale=.25;model.refine_mode='sampling';model.refine_sample_pixels=80000
            folder=root/name;folder.mkdir();alpha=writer(folder/'alpha.mkv',True);fgr=writer(folder/'foreground.mp4')
            cap=cv2.VideoCapture(str(root/'source.mp4'));count=0;inference=0.;samples=[]
            try:
                with torch.inference_mode():
                    while True:
                        ok,b=cap.read()
                        if not ok:break
                        if count>=spec['frames']:raise ValueError('Unexpected extra source frame')
                        if time.monotonic()-started>210:raise TimeoutError('Bounded test runtime exceeded')
                        src=torch.from_numpy(cv2.cvtColor(b,cv2.COLOR_BGR2RGB)).permute(2,0,1).unsqueeze(0).cuda().half()/255
                        torch.cuda.synchronize();it=time.monotonic();pha,fg=model(src,bg)[:2];torch.cuda.synchronize();inference+=time.monotonic()-it
                        a=pha[0,0].float().clamp(0,1).mul(255).round().byte().cpu().numpy()
                        rgb=fg[0].float().clamp(0,1).mul(255).round().byte().permute(1,2,0).cpu().numpy()
                        alpha.stdin.write(a.tobytes());fgr.stdin.write(rgb.tobytes())
                        if count in spec['sample_frames']:
                            composite=np.clip(rgb.astype(float)*(a[:,:,None]/255)+28*(1-a[:,:,None]/255),0,255).astype(np.uint8)
                            ok,png=cv2.imencode('.png',cv2.cvtColor(composite,cv2.COLOR_RGB2BGR));samples.append(count)
                            artifacts[f'{name}/sample-{count}.png']=png.tobytes()
                        count+=1
                if count!=spec['frames']:raise ValueError(f'Incomplete output: {count}')
            finally:
                cap.release();alpha.stdin.close();fgr.stdin.close()
                if alpha.wait()!=0 or fgr.wait()!=0:raise RuntimeError('Encoder failed')
            records.append({'model':name,'frames':count,'inference_seconds':inference,'total_seconds':time.monotonic()-tick,'sample_frames':samples,'model_sha256':lock[name]['sha256']})
            for kind in ['alpha.mkv','foreground.mp4']:artifacts[f'{name}/{kind}']=(folder/kind).read_bytes()
            del model;torch.cuda.empty_cache()
    seconds=time.monotonic()-started
    return {'records':records,'function_seconds':seconds,'estimated_compute_usd':seconds*RATE,'cost_note':'Runtime estimate, not invoice; startup/build/idle excluded',
            'artifacts':artifacts,'hashes':{k:hashlib.sha256(v).hexdigest() for k,v in artifacts.items()},'spec':spec}

if __name__=='__main__':
    from run_test import reserve,update
    rid='background-reference-20260905-first-comparison'
    record=OUT/'call.json'
    recovery=None
    if record.exists():
        recovery=json.loads(record.read_text())
        if recovery.get('state')!='failed_startup_cancelled' or not recovery.get('cancelled'):raise RuntimeError('Existing attempt; inspect saved result/call ID instead of dispatching twice')
    video=(OUT/'source-hd.mp4').read_bytes();background=(OUT/'background.png').read_bytes()
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames','-of','json',str(OUT/'source-hd.mp4')]))
    frames=int(probe['streams'][0]['nb_read_frames'])
    spec={'video_sha256':hashlib.sha256(video).hexdigest(),'background_sha256':hashlib.sha256(background).hexdigest(),'frames':frames,
          'models':['mobilenetv2','resnet50'],'sample_frames':[25,300,350,400,450,500,550,600,650,700,750,800,850,900]}
    if recovery is None:reserve(rid,{'stage':'background_reference_test',**spec})
    else:
        # One diagnosed import fix under the SAME retained 40-cent reservation.
        # The cancelled call remains in history; never claim its cost was zero.
        update(rid,state='reserved',startup_failure=recovery,accounted_usd=.4)
    start=time.monotonic();handle=None
    def save(data):
        tmp=record.with_suffix('.writing');tmp.write_text(json.dumps(data,indent=2));tmp.replace(record)
    save({'state':'building','request_id':rid,'spec':spec})
    try:
        with modal.enable_output():
            with app.run():
                handle=run.spawn(video,background,spec)
                save({'state':'running','request_id':rid,'call_id':handle.object_id,'spec':spec});update(rid,state='running',call_id=handle.object_id)
                result=handle.get(timeout=270)
                for name,blob in result.pop('artifacts').items():
                    if hashlib.sha256(blob).hexdigest()!=result['hashes'][name]:raise ValueError('Output hash mismatch')
                    path=OUT/name;path.parent.mkdir(exist_ok=True);path.write_bytes(blob)
                wall=time.monotonic()-start;accounted=.4 if recovery else max(.02,math.ceil((wall+20)*RATE*100)/100+.01)
                result.update(client_wall_seconds=wall,accounted_usd=accounted,provider_charge_usd=None,worker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
                (OUT/'result.json').write_text(json.dumps(result,indent=2));save({'state':'complete','call_id':handle.object_id,'request_id':rid,'result':str(OUT/'result.json')})
                update(rid,state='complete',estimated_usd=result['estimated_compute_usd'],accounted_usd=accounted,metrics=str(OUT/'result.json'))
                print(json.dumps({k:result[k] for k in ['records','function_seconds','estimated_compute_usd','client_wall_seconds','accounted_usd']},indent=2))
    except BaseException as ex:
        if handle:
            try:handle.cancel(terminate_containers=True)
            except Exception:pass
        save({'state':'failed','request_id':rid,'call_id':handle.object_id if handle else None,'error':str(ex)})
        update(rid,state='failed',error=str(ex),accounted_usd=.4)
        raise
