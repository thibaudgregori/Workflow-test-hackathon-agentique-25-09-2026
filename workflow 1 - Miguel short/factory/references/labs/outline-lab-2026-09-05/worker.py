"""Isolated model adapters for the outline comparison. No production writes."""
from pathlib import Path
import json, os, sys, time, subprocess
import cv2
import numpy as np


def run(spec, root):
    import torch
    from PIL import Image
    torch.set_num_threads(2)
    cv2.setNumThreads(2)
    root = Path(root)
    mode = spec['mode']
    cap = cv2.VideoCapture(str(root / 'video.mp4'))
    ow, oh = int(cap.get(3)), int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    expected = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    scale = min(1., spec.get('max_side', 1024) / max(ow, oh))
    w, h = round(ow * scale / 2) * 2, round(oh * scale / 2) * 2
    limit = min(expected, spec.get('limit', expected))
    seed = np.array(Image.open(root / 'mask.png').convert('L'))
    seed = cv2.resize(seed, (w,h), interpolation=cv2.INTER_NEAREST)
    enc = subprocess.Popen(['ffmpeg','-v','error','-threads','2','-f','rawvideo','-pix_fmt','gray','-s',f'{ow}x{oh}','-r',str(fps),'-i','pipe:0','-an','-c:v','ffv1','-threads','2','-y',str(root/'alpha.mkv')],stdin=subprocess.PIPE)
    frames = 0
    t0 = time.monotonic()
    def write(alpha):
        nonlocal frames
        if not np.isfinite(alpha).all(): raise ValueError(f'Non-finite alpha at {frames}')
        alpha=np.clip(alpha,0,1)
        if np.mean(alpha>.5)<.02: raise ValueError(f'Empty or lost presenter at frame {frames}')
        if alpha.shape != (oh,ow): alpha=cv2.resize(alpha,(ow,oh),interpolation=cv2.INTER_LINEAR)
        enc.stdin.write(np.rint(alpha*255).astype('uint8').tobytes())
        frames+=1
        if frames%100==0: print(f'PROGRESS {frames}/{limit} {time.monotonic()-t0:.1f}s',flush=True)
    load_start=time.monotonic()
    if mode == 'matanyone2':
        from matanyone2 import MatAnyone2, InferenceCore
        from omegaconf import OmegaConf
        from safetensors.torch import load_file
        cfg=OmegaConf.create(json.loads(Path('/opt/models/matanyone2/config.json').read_text())['cfg'])
        cfg.model.pretrained_resnet=False  # Full checkpoint includes these weights.
        model=MatAnyone2(cfg,single_object=True)
        model.load_state_dict(load_file('/opt/models/matanyone2/model.safetensors'),strict=True)
        model=model.cuda().eval()
        processor=InferenceCore(model,device='cuda')
    elif mode == 'sam2matting':
        import sam2.build_sam as sam_builder
        from sam2.build_sam import build_sam2matting_video_predictor
        def strict_checkpoint(model,path):
            weights=torch.load(path,map_location='cpu',weights_only=True)['model']
            model.load_state_dict(weights,strict=True)
        sam_builder._load_checkpoint=strict_checkpoint
        variant=spec.get('variant','tiny')
        suffix='Tiny' if variant=='tiny' else 'Base+'
        cfg='tiny' if variant=='tiny' else 'base+'
        model=build_sam2matting_video_predictor(f'configs/sam2matting-sam2.1{cfg}.yaml',f'/opt/models/sam2matting/SAM2Matting-SAM2.1{suffix}.pt',device='cuda')
    elif mode == 'vitmatte':
        from transformers import VitMatteImageProcessor, VitMatteForImageMatting
        processor=VitMatteImageProcessor.from_pretrained('/opt/models/vitmatte')
        model=VitMatteForImageMatting.from_pretrained('/opt/models/vitmatte').cuda().eval()
    else: raise ValueError(mode)
    torch.cuda.synchronize()
    load_seconds=time.monotonic()-load_start
    infer_start=time.monotonic()
    dtype=torch.bfloat16 if spec.get('precision','bf16')=='bf16' else torch.float32
    with torch.inference_mode(), torch.autocast('cuda',dtype=dtype,enabled=dtype!=torch.float32):
        if mode=='matanyone2':
            ok, frame=cap.read()
            if not ok: raise ValueError('Empty input')
            def tensor(frame):
                rgb=cv2.cvtColor(cv2.resize(frame,(w,h)),cv2.COLOR_BGR2RGB)
                return torch.from_numpy(rgb).permute(2,0,1).float().cuda()/255.
            first=tensor(frame)
            # Upstream matting mode divides masks by 255 internally.
            processor.step(first,torch.from_numpy((seed>127).astype('float32')*255).cuda(),objects=[1])
            for _ in range(spec.get('warmup',10)): processor.step(first,first_frame_pred=True)
            for i in range(limit):
                if i:
                    ok,frame=cap.read()
                    if not ok: raise ValueError(f'Missing frame {i}')
                prob=processor.step(tensor(frame),first_frame_pred=(i==0))
                write(processor.output_prob_to_mask(prob).float().cpu().numpy())
        elif mode=='sam2matting':
            # The upstream eager loader keeps every 1024-square RGB frame in RAM.
            # Decode to disk and retain only two normalized tensors, with the same
            # PIL resizing/normalization; model tracking and alpha heads unchanged.
            from functools import lru_cache
            import sam2.sam2matting_video_predictor as vp
            fd=root/'frames';fd.mkdir()
            for i in range(limit):
                ok,frame=cap.read()
                if not ok: raise ValueError(f'Missing frame {i}')
                cv2.imwrite(str(fd/f'{i:06d}.png'),cv2.resize(frame,(w,h)),[cv2.IMWRITE_PNG_COMPRESSION,1])
            class LazyFrames:
                def __len__(self): return limit
                @lru_cache(maxsize=2)
                def __getitem__(self,i):
                    a=np.array(Image.open(fd/f'{i:06d}.png').convert('RGB').resize((1024,1024)))
                    x=torch.from_numpy(a).permute(2,0,1).float().cuda()/255
                    return (x-torch.tensor([.485,.456,.406],device='cuda')[:,None,None])/torch.tensor([.229,.224,.225],device='cuda')[:,None,None]
            vp.load_video_frames=lambda **kwargs:(LazyFrames(),h,w)
            state=model.init_state(video_path=str(fd),offload_state_to_cpu=True)
            m=torch.from_numpy((seed>127).astype('float32')*20-10).cuda()[None,None]
            m=torch.nn.functional.interpolate(m,(256,256),mode='bilinear',align_corners=False)
            model.add_new_mask(inference_state=state,frame_idx=0,obj_id=1,mask=m)
            for idx,_,_,alpha,_ in model.propagate_in_video(state):
                if idx!=frames: raise ValueError('Out-of-order model frames')
                write(alpha.squeeze().float().cpu().numpy())
        else:
            acap=cv2.VideoCapture(str(root/'baseline.mkv'))
            band=int(spec.get('band',24))
            kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(band*2+1,band*2+1))
            for i in range(limit):
                ok,frame=cap.read();aok,a=acap.read()
                if not ok or not aok: raise ValueError(f'Missing input or alpha {i}')
                rgb=cv2.cvtColor(cv2.resize(frame,(w,h)),cv2.COLOR_BGR2RGB)
                b=(cv2.resize(a[:,:,0],(w,h))>127).astype('uint8')
                fg=cv2.erode(b,kernel);bg=cv2.dilate(b,kernel)
                trimap=np.where(fg,255,np.where(bg,128,0)).astype('uint8')
                inputs=processor(images=rgb,trimaps=trimap,return_tensors='pt').to('cuda')
                alpha=model(**inputs).alphas[0,0,:h,:w].float().cpu().numpy()
                write(alpha)
            acap.release()
    torch.cuda.synchronize()
    infer_seconds=time.monotonic()-infer_start
    cap.release();enc.stdin.close()
    if enc.wait()!=0: raise RuntimeError('Alpha encoder failed')
    if frames!=limit: raise RuntimeError(f'Frame count {frames} != {limit}')
    check=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=nb_read_frames,width,height','-of','json',str(root/'alpha.mkv')]))['streams'][0]
    assert int(check['nb_read_frames'])==limit and check['width']==ow and check['height']==oh
    result={'ok':True,'spec':spec,'frames':frames,'fps':fps,'source_size':[ow,oh],'inference_size':[w,h],'load_seconds':load_seconds,'process_seconds':infer_seconds,'total_worker_seconds':time.monotonic()-t0,'peak_gpu_gib':torch.cuda.max_memory_allocated()/2**30,'torch':torch.__version__,'gpu':torch.cuda.get_device_name()}
    (root/'metrics.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result),flush=True)

if __name__=='__main__': run(json.loads(Path(sys.argv[1]).read_text()),sys.argv[2])
