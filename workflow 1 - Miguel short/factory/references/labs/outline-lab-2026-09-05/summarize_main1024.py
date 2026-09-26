"""Validate and report the explicitly requested 1024 main-pass repeat."""
from pathlib import Path
import json
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[6]
OUT = ROOT / 'output/shorts-outline-lab/2026-09-05'
DEST = OUT / 'main-pass-1024'

def main():
    cv2.setNumThreads(2)
    rows=[]
    for v in ['shieldstral', 'harnessrace', 'game33c']:
        d=OUT / f'results/{v}/matanyone2-main1024-confirm'
        m=json.loads((d/'metrics.json').read_text())
        old=json.loads((OUT/f'results/{v}/matanyone2-speed640/metrics.json').read_text())
        assert m['ok'] and m['local_worker_matches'] and m['spec']['max_side']==1024 and m['spec']['precision']=='bf16'
        assert m['spec']['input_sha256']==old['spec']['input_sha256'] and m['spec']['mask_sha256']==old['spec']['mask_sha256']
        cap=cv2.VideoCapture(str(d/'alpha.mkv')); n=0; minimum=1.; soft=0
        assert cap.get(cv2.CAP_PROP_FPS)==m['fps']
        while True:
            ok,im=cap.read()
            if not ok:break
            assert list(im.shape[1::-1])==m['source_size']
            a=im[:,:,0]; minimum=min(minimum,float((a>127).mean())); soft+=int(np.any((a>0)&(a<255))); n+=1
        cap.release()
        assert n==m['frames'] and minimum>.02 and soft==n
        rows.append(dict(video=v,clip_seconds=n/m['fps'],frames=n,processing_seconds=m['function_seconds'],total_wait_seconds=m['client_wall_seconds'],compute_estimate_usd=m['estimated_compute_usd'],elapsed_estimate_usd=m['conservative_elapsed_estimate_usd'],prior_640_processing_seconds=old['function_seconds'],prior_640_compute_estimate_usd=old['estimated_compute_usd'],same_input_and_manual_mask=True,validated_all_frames=True))
    def costs(file, app=None):
        return sum(float(r['Cost']) for r in json.loads((DEST/file).read_text()) if (r['Object ID']==app if app else r['Description'].startswith('shorts-outline-')))
    app='ap-BsDfEcaQrcUMdNseT4w3hC'
    delta=costs('billing-after.json',app)-costs('billing-before.json',app)
    total=costs('billing-after.json')
    summary=dict(rows=rows,provider_reported_app_delta_usd=delta,provider_reported_outline_total_usd=total,compute_estimate_usd=sum(r['compute_estimate_usd'] for r in rows),elapsed_estimate_usd=sum(r['elapsed_estimate_usd'] for r in rows),qualification='Provider reporting can lag. Estimates are not invoices. Previous 640 runs are a historical comparison, not a paired repeated benchmark.')
    (DEST/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    lines=['# MatAnyone 2: 1024 main-pass confirmation','', 'Fresh sequential calls on the deployed Genial L4 app, using the same clips and manually corrected masks as the earlier 640 tests. BF16, 10 first-frame warmup steps. No production change.','', '| Clip | Duration | Processing | Total wait | Compute estimate | Earlier 640 processing |','|---|---:|---:|---:|---:|---:|']
    for r in rows:
        lines.append(f"| {r['video']} | {r['clip_seconds']:.2f}s | {r['processing_seconds']:.1f}s | {r['total_wait_seconds']:.1f}s | ${r['compute_estimate_usd']:.4f} | {r['prior_640_processing_seconds']:.1f}s |")
    lines+=['',f"Provider-reported app cost increase: **${delta:.4f}**. Function-runtime compute estimate: **${summary['compute_estimate_usd']:.4f}** total; conservative elapsed-time estimate: **${summary['elapsed_estimate_usd']:.4f}**. Provider-reported outline experiment total: **${total:.4f}** at readback. Billing can lag.",'','Processing includes container function work; total wait also includes upload/startup/download. Manual preparation, final Shorts rendering and local review are excluded. All 2,537 frames were decoded, with expected dimensions, soft alpha and presenter presence. These checks do not certify every edge. Earlier 640 timings are historical single-run comparisons.','']
    for r in rows:
        lines.append(f"- [{r['video']} image comparison](../comparisons/{r['video']}-outline-main1024-confirm.png)")
    (DEST/'report.md').write_text('\n'.join(lines)+'\n')
    p=DEST/'experiment.json';e=json.loads(p.read_text());e.update(status='complete',all_frames_validated=2537,provider_reported_delta_usd=delta);p.write_text(json.dumps(e,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
