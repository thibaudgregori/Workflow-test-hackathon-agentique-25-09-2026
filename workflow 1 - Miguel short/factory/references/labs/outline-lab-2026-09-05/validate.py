"""Decode every selected matte; flag motion outliers for visual review.

Area changes are review pointers, never an automatic outline-quality verdict.
"""
import argparse,json
from pathlib import Path
import cv2
import numpy as np

ROOT=Path(__file__).resolve().parents[6]
OUT=ROOT/'output/shorts-outline-lab/2026-09-05'

def main():
    cv2.setNumThreads(2)
    parser=argparse.ArgumentParser();parser.add_argument('--video');parser.add_argument('--model');args=parser.parse_args()
    selected=json.loads((OUT/'selection.json').read_text());records=[]
    for inv in json.loads((OUT/'inventory.json').read_text()):
        video=inv['id']; cap=cv2.VideoCapture(inv['plate'])
        if args.video and video!=args.video:cap.release();continue
        expected=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));width=int(cap.get(3));height=int(cap.get(4));cap.release()
        paths={'current':Path(inv['comparison_baseline_alpha'])}
        paths.update({mode:OUT/'results'/video/tag/'alpha.mkv' for mode,tag in selected[video].items()})
        for mode,path in paths.items():
            if args.model and mode!=args.model:continue
            cap=cv2.VideoCapture(str(path));i=0;prev=None;changes=[];areas=[];soft=[]
            while True:
                ok,bgr=cap.read()
                if not ok:break
                assert bgr.shape[:2]==(height,width)
                a=cv2.resize(bgr[:,:,0],(width//4,height//4),interpolation=cv2.INTER_AREA).astype(np.float32)/255
                areas.append(float((a>.5).mean()));soft.append(float(((a>.02)&(a<.98)).mean()))
                if prev is not None:changes.append((i,float(np.abs(a-prev).mean())))
                prev=a;i+=1
            cap.release();assert i==expected and min(areas)>.02,(video,mode,i,expected)
            top=[]
            for idx,score in sorted(changes,key=lambda x:x[1],reverse=True):
                if all(abs(idx-j)>25 for j,_ in top):top.append((idx,score))
                if len(top)==4:break
            records.append({'video':video,'mode':mode,'tag':selected[video].get(mode,'shipped'),'frames':i,'dimensions':[width,height],'foreground_fraction_min':min(areas),'soft_fraction_mean':float(np.mean(soft)),'largest_change_review_frames':[{'frame':j,'seconds':round(j/25,2),'mean_alpha_change':s} for j,s in top],'quality_verdict':'Requires visual review; motion is not necessarily flicker'})
            print(video,mode,i,[round(j/25,2) for j,_ in top],flush=True)
    if (args.video or args.model) and (OUT/'validation.json').exists():
        keys={(r['video'],r['mode']) for r in records}
        records=[r for r in json.loads((OUT/'validation.json').read_text()) if (r['video'],r['mode']) not in keys]+records
    (OUT/'validation.json').write_text(json.dumps(records,indent=2))

if __name__=='__main__':main()
