"""Matched real-source/model-output media, no generated pixels or paid calls."""
from pathlib import Path
import cv2,hashlib,json,subprocess,time
import numpy as np
from PIL import Image,ImageDraw,ImageFont

W=Path(__file__).resolve().parents[6]
O=W/'output/shorts-outline-lab/2026-09-05/background-reference-test'
result=json.loads((O/'result.json').read_text());nominations=json.loads((O/'source-nominations.json').read_text())
models=['mobilenetv2','resnet50'];wanted={v['frame']:v for v in nominations['nominations']}
for name,sha in result['hashes'].items():
    if hashlib.sha256((O/name).read_bytes()).hexdigest()!=sha:raise ValueError('Output changed')
for name,expected in [('source-hd.mp4',result['spec']['video_sha256']),('background.png',result['spec']['background_sha256'])]:
    if hashlib.sha256((O/name).read_bytes()).hexdigest()!=expected:raise ValueError('Input changed')
style=json.loads((W/'assets/templates/documents/hand-outline-evidence.json').read_text());font=ImageFont.truetype(style['font'],24)
caps=[cv2.VideoCapture(str(O/'source-hd.mp4'))]+[cv2.VideoCapture(str(O/m/k)) for m in models for k in ['foreground.mp4','alpha.mkv']]
video=O/'comparison-cream.mp4'
encoder=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1920x400','-r','25','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-threads','4','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
start=time.monotonic();count=0;media=[];coverage=[]
def comp(fg,a,bg,rim=False):
    a=a.astype(float)/255.;back=np.full_like(fg,bg,dtype=float)
    if rim:
        r=cv2.GaussianBlur(cv2.dilate(a.astype(np.float32),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))),(3,3),.6)[:,:,None]
        back=np.array([255,253,249])*r+back*(1-r)
    return np.clip(fg*a[:,:,None]+back*(1-a[:,:,None]),0,255).astype(np.uint8)
try:
    while True:
        pairs=[c.read() for c in caps]
        if not pairs[0][0]:
            if any(ok for ok,_ in pairs[1:]):raise ValueError('Extra output frames')
            break
        if not all(ok for ok,_ in pairs):raise ValueError('Missing output frame')
        src=cv2.cvtColor(pairs[0][1],cv2.COLOR_BGR2RGB)
        fgs=[cv2.cvtColor(pairs[1+i*2][1],cv2.COLOR_BGR2RGB) for i in range(2)];alphas=[pairs[2+i*2][1][:,:,0] for i in range(2)]
        if count in [25,100,150,300,400,475,525,575,600,825,900]:coverage.append({'frame':count,'foreground_fraction':[float(np.mean(a>127)) for a in alphas]})
        full=Image.new('RGB',(1920,400),'white');draw=ImageDraw.Draw(full)
        for j,(im,title) in enumerate(zip([src]+[comp(f,a,28,True) for f,a in zip(fgs,alphas)],['Source','Fast: MobileNetV2','Larger: ResNet50'])):
            full.paste(Image.fromarray(im).resize((640,360)),(j*640,40));draw.text((j*640+10,6),title,fill='black',font=font)
        encoder.stdin.write(np.asarray(full).tobytes())
        if count in wanted:
            n=wanted[count];rois=n['hand_rois_xyxy'];detail=Image.new('RGB',(1200,50+len(rois)*620),'white');d=ImageDraw.Draw(detail)
            for j,title in enumerate(['Source','Fast: MobileNetV2','Larger: ResNet50']):d.text((j*400+8,8),title,fill='black',font=font)
            for row,roi in enumerate(rois):
                for bgrow,(bg,rim) in enumerate([(240,False),(28,True)]):
                    for col,im in enumerate([src]+[comp(f,a,bg,rim) for f,a in zip(fgs,alphas)]):
                        crop=Image.fromarray(im).crop(tuple(roi));crop.thumbnail((390,300));detail.paste(crop,(col*400+(400-crop.width)//2,50+row*620+bgrow*310+(300-crop.height)//2))
            path=O/f'hands-{count}.jpg';detail.save(path,quality=96)
            fullpath=O/f'full-{count}.jpg';full.save(fullpath,quality=96)
            media.append({'frame':count,'seconds':count/25,'detail':str(path),'full':str(fullpath),'detail_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rois':rois})
        count+=1
finally:
    for c in caps:c.release()
    encoder.stdin.close()
    if encoder.wait()!=0:raise RuntimeError('Comparison encoder failed')
if count!=result['spec']['frames']:raise ValueError('Frame count mismatch')
(O/'comparison-media.json').write_text(json.dumps({'frames':count,'seconds':time.monotonic()-start,'video':str(video),'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'comparisons':media,'coverage_samples':coverage,'note':'Actual model alpha and foreground. Local approximate7px cream preview; no production finishing or content render.'},indent=2))
print('Comparisons ready',count,flush=True)
