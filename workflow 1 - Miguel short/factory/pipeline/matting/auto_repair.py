"""One free, bounded temporal repair attempt per source; never auto-promote.

Input: hash-bound review nominations (frame + hand rectangle), not hand drawings.
OpenCV DIS: https://docs.opencv.org/4.10.0/de/d4f/classcv_1_1DISOpticalFlow.html
Only unmodified neighboring source frames and original alpha are algorithm inputs.
"""
from pathlib import Path
import argparse, concurrent.futures, fcntl, hashlib, json, time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import os, sys
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from fsutil import digest  # shared (2026-09-20)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runs import newest_run  # noqa: E402
# THE RUN IS A PARAMETER (2026-09-20): this tool used to live inside the 2026-09-05 TikTok remake folder and
# treat its own folder as the run. SHORTS_RUN or the newest run on disk is the run now.
R = Path(os.environ["SHORTS_RUN"]).expanduser().resolve() if os.environ.get("SHORTS_RUN") else newest_run()
W = R.parents[4]
DEFAULT_OUT = W / 'output/shorts-tiktok-remake/2026-09-05/auto-repair-flow-corrected'
VERSION = 'temporal-consensus-v3-corrected'
cv2.setNumThreads(1)

def atomic(path, data):
    tmp = path.with_suffix('.writing')
    tmp.write_text(json.dumps(data, indent=2)); tmp.replace(path)

def read_frames(path, numbers):
    cap = cv2.VideoCapture(str(path)); result = {}
    try:
        for n in sorted(numbers):
            cap.set(cv2.CAP_PROP_POS_FRAMES, n); ok, b = cap.read()
            if not ok: raise ValueError(f'Missing frame {n}: {path}')
            result[n] = b
    finally: cap.release()
    return result

def propose(rgb, alpha, frame, roi):
    """Flow is target -> neighbor, so remapping samples neighbor at target+flow."""
    x0,y0,x1,y1 = roi; h,w = alpha[frame].shape
    # Context supports motion estimation; changes remain strictly inside the ROI.
    l,t,r,b = max(0,x0-48),max(0,y0-48),min(w,x1+48),min(h,y1+48)
    target = cv2.cvtColor(rgb[frame][t:b,l:r], cv2.COLOR_BGR2GRAY)
    yy,xx = np.mgrid[0:target.shape[0],0:target.shape[1]].astype(np.float32)
    values, validity = [], []
    for k in [-2,-1,1,2]:
        if frame+k not in rgb: continue
        neighbor = cv2.cvtColor(rgb[frame+k][t:b,l:r], cv2.COLOR_BGR2GRAY)
        dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
        flow = dis.calc(target,neighbor,None)
        back = dis.calc(neighbor,target,None)
        mx,my = xx+flow[:,:,0],yy+flow[:,:,1]
        def warp(a): return cv2.remap(a,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
        cycle = np.linalg.norm(flow+warp(back),axis=2)
        photo = np.abs(target.astype(float)-warp(neighbor).astype(float))
        valid = (cycle<1.5)&(photo<24)&(mx>=1)&(my>=1)&(mx<target.shape[1]-2)&(my<target.shape[0]-2)
        values.append(warp(alpha[frame+k][t:b,l:r]).astype(float)); validity.append(valid)
    if len(values)<3: return alpha[frame].copy(), {'changed_pixels':0,'reason':'insufficient neighbors'}
    values,validity=np.stack(values),np.stack(validity)
    # Require agreement from at least 3 independently aligned neighboring masks.
    masked=np.where(validity,values,np.nan)
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',RuntimeWarning)
        estimate=np.nanmedian(masked,axis=0)
        spread=np.nanmax(masked,axis=0)-np.nanmin(masked,axis=0)
    old=alpha[frame][t:b,l:r]; allowed=np.zeros_like(old,dtype=bool)
    allowed[y0-t:y1-t,x0-l:x1-l]=True
    # Do not invent detached foreground or erase opaque foreground cores.
    distance=cv2.distanceTransform((old<40).astype(np.uint8),cv2.DIST_L2,3)
    safe=(validity.sum(axis=0)>=3)&(spread<65)&allowed&(distance<32)
    delta=estimate-old.astype(float)
    safe &= ((delta>20)&(estimate>60)) | ((delta < -20)&(old<180))
    candidate=old.copy(); candidate[safe]=np.rint(np.clip(estimate[safe],0,255)).astype(np.uint8)
    full=alpha[frame].copy(); full[t:b,l:r]=candidate
    changed=full!=alpha[frame]
    outside=changed.copy(); outside[y0:y1,x0:x1]=False
    if outside.any(): raise ValueError('Repair escaped nominated ROI')
    return full, {'changed_pixels':int(changed.sum()),'added_opacity':float(np.maximum(full.astype(float)-alpha[frame],0).sum()/255),
                  'removed_opacity':float(np.maximum(alpha[frame].astype(float)-full,0).sum()/255),'outside_changed_pixels':0}

def background_proposal(rgb,alpha,frame,roi,samples):
    """Candidate only: reconstruct static background from actual clear observations."""
    from scipy.ndimage import distance_transform_edt
    import warnings
    x0,y0,x1,y1=roi
    current=rgb[frame][y0:y1,x0:x1].astype(float); old=alpha[frame][y0:y1,x0:x1]
    if not np.any(old>=220):
        return alpha[frame].copy(),{'changed_pixels':0,'added_opacity':0.,'removed_opacity':0.,'outside_changed_pixels':0,'reason':'no opaque reference'}
    colors=np.stack([rgb[n][y0:y1,x0:x1] for n in samples]).astype(float)
    clear=np.stack([alpha[n][y0:y1,x0:x1]<5 for n in samples])
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',RuntimeWarning)
        bg=np.nanmedian(np.where(clear[:,:,:,None],colors,np.nan),axis=0)
        noise=np.nanmedian(np.where(clear,np.linalg.norm(colors-bg,axis=3),np.nan),axis=0)
    # Nearest opaque source pixel supplies color, not a synthesized hand shape.
    distance,indices=distance_transform_edt(old<220,return_indices=True)
    fg=current[indices[0],indices[1]]
    direction=fg-bg; norm=np.sum(direction**2,axis=2)
    a=np.clip(np.sum((current-bg)*direction,axis=2)/np.maximum(norm,1),0,1)
    residual=np.linalg.norm(current-(bg+a[:,:,None]*direction),axis=2)
    support=(clear.sum(axis=0)>=5)&(noise<12)&(norm>1600)&(residual<20)&(distance<65)&(old<220)&(a>.12)&(a<.98)
    # Only restore supported opacity; leave existing subject pixels untouched.
    candidate=old.copy(); values=np.nan_to_num(np.rint(a*255)).astype(np.uint8)
    support &= values.astype(float)>old.astype(float)+20
    candidate[support]=values[support]
    full=alpha[frame].copy();full[y0:y1,x0:x1]=candidate
    outside=full!=alpha[frame];outside[y0:y1,x0:x1]=False
    if outside.any():raise ValueError('Repair escaped nominated ROI')
    return full,{'changed_pixels':int(np.count_nonzero(full!=alpha[frame])),
                 'added_opacity':float(np.maximum(full.astype(float)-alpha[frame],0).sum()/255),'removed_opacity':0.,
                 'outside_changed_pixels':0,'background_sample_count':len(samples),'background_supported_pixels':int(support.sum())}

def sheet(source,before,after,roi,path,title):
    x0,y0,x1,y1=roi; rgb=cv2.cvtColor(source,cv2.COLOR_BGR2RGB)
    h,w=before.shape; pad=20; roi=(max(0,x0-pad),max(0,y0-pad),min(w,x1+pad),min(h,y1+pad))
    style=json.loads((W/'assets/templates/documents/hand-outline-evidence.json').read_text())
    font=ImageFont.truetype(style['font'],22)
    canvas=Image.new('RGB',(1200,950),(244,244,240)); draw=ImageDraw.Draw(canvas)
    draw.text((16,10),title,fill='black',font=font)
    for j,label in enumerate(['Source footage','Original outline','Automatic candidate']): draw.text((16+j*400,50),label,fill='black',font=font)
    for row,bg in enumerate([28,240,'cream']):
        panels=[rgb]
        for mask in [before,after]:
            a=mask[:,:,None]/255.
            background=np.full_like(rgb,28 if bg=='cream' else bg,dtype=float)
            if bg=='cream':
                rim=cv2.GaussianBlur(cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))),(3,3),0.6)[:,:,None]/255.
                background=np.array([255,253,249])*rim+background*(1-rim)
            panels.append(np.clip(rgb*a+background*(1-a),0,255).astype(np.uint8))
        for col,view in enumerate(panels):
            im=Image.fromarray(view).crop(roi); im.thumbnail((390,265))
            canvas.paste(im,(col*400+(400-im.width)//2,90+row*280+(265-im.height)//2))
    draw.text((16,930),'Dark / light / approximate cream preview. Candidate only; no original overwritten.',fill='black',font=ImageFont.truetype(style['font'],16))
    canvas.save(path,quality=94)

def validate_entries(entries):
    if not entries:raise ValueError('Empty nominations')
    first=entries[0];seen=set()
    for e in entries:
        for key in ['id','source','before_alpha','source_sha256','before_alpha_sha256']:
            if e[key]!=first[key]:raise ValueError('Mixed recording identities')
        if e['frame'] in seen:raise ValueError('Duplicate nominated frame')
        seen.add(e['frame'])

def one(entries,out):
    validate_entries(entries)
    folder=Path(out).resolve()/entries[0]['id'];folder.mkdir(parents=True,exist_ok=True)
    with (folder/'attempt.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        return _one(entries,Path(out).resolve())

def _one(entries,out):
    start=time.monotonic(); e=entries[0]; name=e['id']; out=Path(out)/name; out.mkdir(parents=True,exist_ok=True)
    identity={'version':VERSION,'source_sha256':digest(e['source']),'before_alpha_sha256':digest(e['before_alpha']),
              'nominations':[{'frame':v['frame'],'roi':v['roi_xyxy']} for v in entries],'code_sha256':digest(__file__)}
    if identity['source_sha256']!=e['source_sha256'] or identity['before_alpha_sha256']!=e['before_alpha_sha256']:raise ValueError('Stale nomination')
    record=out/'attempt.json'
    if record.exists():
        cached=json.loads(record.read_text())
        if cached['identity']!=identity:raise ValueError('Existing attempt differs; do not retry silently')
        if cached['state']=='running': raise RuntimeError('Interrupted attempt; inspect existing artifacts')
        for r in cached.get('results',[]):
            for key in ['candidate','comparison']:
                if digest(r[key])!=r[key+'_sha256']:raise ValueError('Cached artifact changed')
        return cached
    atomic(record,{'id':name,'identity':identity,'state':'running','attempt':1})
    try:
        cap=cv2.VideoCapture(e['source']);total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));w=int(cap.get(3));h=int(cap.get(4));cap.release()
        for v in entries:
            x0,y0,x1,y1=v['roi_xyxy']
            if not (0<=v['frame']<total and 0<=x0<x1<=w and 0<=y0<y1<=h):raise ValueError('Invalid frame or ROI')
        frames=sorted({n for v in entries for n in range(max(0,v['frame']-3),min(total,v['frame']+4))})
        if len(frames)>20:raise ValueError('Repair window exceeds limit')
        all_frames=frames
        rgb=read_frames(e['source'],all_frames); alpha={n:b[:,:,0] for n,b in read_frames(e['before_alpha'],all_frames).items()}
        results=[]
        for v in entries:
            n=v['frame']; roi=v['roi_xyxy']; assert alpha[n].shape==rgb[n].shape[:2]
            candidate,metrics=propose(rgb,alpha,n,roi)
            target=out/f'candidate-{n}.png'; cv2.imwrite(str(target),candidate)
            image=out/f'comparison-{n}.jpg'; sheet(rgb[n],alpha[n],candidate,roi,image,f'{name} | frame {n} | automatic attempt 1')
            results.append({'frame':n,'roi':roi,**metrics,'candidate':str(target),'candidate_sha256':digest(target),'comparison':str(image),'comparison_sha256':digest(image)})
        record_data={'id':name,'identity':identity,'state':'needs_independent_review' if any(r['changed_pixels'] for r in results) else 'needs_manual_review',
                     'attempt':1,'max_attempts':1,'seconds':time.monotonic()-start,'new_cloud_cost_usd':0,'installed':False,
                     'trigger':'existing reviewer frame/hand-ROI nominations; not an automatic whole-video detector','results':results}
        atomic(record,record_data); return record_data
    except Exception as ex:
        atomic(record,{'id':name,'identity':identity,'state':'needs_manual_review','error':str(ex),'attempt':1,'installed':False}); raise

def run_manifest(manifest,out=DEFAULT_OUT,ids=None,expected_alpha=None):
    out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
    entries=json.loads(Path(manifest).read_text()); groups={}
    for e in entries:
        if ids and e['id'] not in ids: continue
        if expected_alpha and digest(expected_alpha)!=e['before_alpha_sha256']: raise ValueError('Review belongs to a different outline')
        groups.setdefault(e['id'],[]).append(e)
    if not groups: return []
    start=time.monotonic()
    def safe(es):
        try:return one(es,out)
        except Exception as ex:return {'id':es[0]['id'],'state':'needs_manual_review','error':str(ex),'installed':False}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(safe,groups.values()))
    atomic(Path(out)/'summary.json',{'version':VERSION,'wall_seconds':time.monotonic()-start,'new_cloud_cost_usd':0,'results':results})
    return results

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path,required=True);p.add_argument('--out',type=Path,default=DEFAULT_OUT);p.add_argument('--ids',nargs='*');a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    for result in run_manifest(a.manifest,a.out,a.ids): print(json.dumps(result),flush=True)
