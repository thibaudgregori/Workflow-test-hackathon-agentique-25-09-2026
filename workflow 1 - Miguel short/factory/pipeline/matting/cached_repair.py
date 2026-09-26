"""One local, reviewable edit attempt using aligned, previously computed mattes.

No model dispatch, installation, or inference retries. A plan is an agent's
explicit per-frame choice, not an automatic detector or a silhouette guess.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from fsutil import digest  # shared (2026-09-20)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'sam2'))
from post import rim_alpha, SIGMA_HI, FEATHER

VERSION = 'cached-donor-v1'
KEYS = ('source', 'baseline_alpha', 'baseline_foreground', 'donor_alpha', 'donor_foreground')


def save(path, value):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.writing')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.replace(path)


def validate(plan):
    if not plan.get('editor') or not plan.get('alignment_note'):
        raise ValueError('Agent identity and source alignment evidence required')
    specs = []
    for key in KEYS:
        item = plan['inputs'][key]
        if digest(item['path']) != item['sha256']:
            raise ValueError(f'Stale input: {key}')
        cap = cv2.VideoCapture(item['path'])
        specs.append(tuple(cap.get(p) for p in (cv2.CAP_PROP_FRAME_WIDTH,
                     cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FRAME_COUNT, cv2.CAP_PROP_FPS)))
        cap.release()
    if not specs[0][2] or any(s != specs[0] for s in specs[1:]):
        raise ValueError('Source, alpha and foreground must have identical geometry, frames and FPS')
    w, h, frames, fps = specs[0]
    if not plan['cases'] or not plan['patches']:
        raise ValueError('At least one review case and one explicit patch required')
    ids = [c['id'] for c in plan['cases']]
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate case IDs')
    covered = set()
    for c in plan['cases']:
        if not c['id'].replace('-', '').replace('_', '').isalnum():
            raise ValueError('Invalid case ID')
        start, end = c['window']
        x0, y0, x1, y1 = c['view_roi']
        if not (0 <= start <= end < frames and end-start <= 100):
            raise ValueError('Review window must contain at most 101 valid frames')
        if not (0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h):
            raise ValueError('Invalid view ROI')
        covered.update(range(start, end + 1))
    touched = set()
    for p in plan['patches']:
        if p['frame'] not in covered or p['frame'] in touched:
            raise ValueError('Patch frame missing from review windows or duplicated')
        touched.add(p['frame'])
        xy = np.asarray(p['polygon'], dtype=float)
        if (len(xy) < 3 or xy.shape[1:] != (2,) or not np.isfinite(xy).all()
                or (xy < 0).any() or (xy[:, 0] >= w).any() or (xy[:, 1] >= h).any()):
            raise ValueError('Invalid source-bound polygon')
        if not any(
                c['window'][0] <= p['frame'] <= c['window'][1]
                and c['view_roi'][0] <= xy[:, 0].min()
                and c['view_roi'][1] <= xy[:, 1].min()
                and xy[:, 0].max() < c['view_roi'][2]
                and xy[:, 1].max() < c['view_roi'][3]
                for c in plan['cases']):
            raise ValueError('Full patch polygon must be visible in a review case on its frame')
        if not (1 <= p['feather_px'] <= 24) or not p.get('reason'):
            raise ValueError('Explicit reason and bounded inward feather required')
    return int(w), int(h), int(frames), fps


def blend(f0, a0, f1, a1, polygon, feather):
    """Feather inward only; never change alpha or visible RGB outside support."""
    support = np.zeros(a0.shape, np.uint8)
    cv2.fillPoly(support, [np.asarray(polygon, np.int32)], 1)
    weight = np.clip(cv2.distanceTransform(support, cv2.DIST_L2, 5) / feather, 0, 1)
    a = a0.copy()
    f = f0.copy()
    inside = weight > 0
    t = weight[inside]
    mixed_a = (1-t)*a0[inside] + t*a1[inside]
    pm = ((1-t[:, None])*f0[inside]*a0[inside, None]
          + t[:, None]*f1[inside]*a1[inside, None])
    a[inside] = mixed_a
    f[inside] = pm / np.maximum(mixed_a[:, None], 1e-8)
    assert np.array_equal(a[~inside], a0[~inside])
    assert np.array_equal(f[~inside], f0[~inside])
    return f, a, inside


def composite(f, a, background, rim):
    back = np.full_like(f, background, dtype=np.float32)
    if rim:
        h, w = a.shape
        hi = cv2.resize((a > .5).astype(np.uint8), (w*2, h*2),
                        interpolation=cv2.INTER_NEAREST) > 0
        d = rim_alpha(hi, a.shape, rim_px=7, sigma_hi=SIGMA_HI, feather=FEATHER)
        back = np.array([255, 253, 249], np.float32)*d[..., None] + back*(1-d[..., None])
    return np.clip(f*a[..., None] + back*(1-a[..., None]), 0, 255).astype(np.uint8)


def panel(source, f0, a0, f, a, roi, frame):
    x0, y0, x1, y1 = roi
    # Finite production rim kernel gets 48 source pixels of context. Crop only
    # after deriving the rim; the visible ROI has no artificial crop-edge rim.
    lx, ly, rx, ry = max(0,x0-48), max(0,y0-48), min(a.shape[1],x1+48), min(a.shape[0],y1+48)
    sl = np.s_[ly:ry, lx:rx]
    inner = np.s_[y0-ly:y1-ly, x0-lx:x1-lx]
    canvas = Image.new('RGB', (1200, 660), 'white')
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 21)
    for col, title in enumerate(['Source', 'Before', 'Candidate']):
        draw.text((col*400+12, 8), f'{title} | frame {frame}', fill='black', font=font)
    for row, (bg, rim) in enumerate([(28, True), (240, False)]):
        views = [source[y0:y1,x0:x1], composite(f0[sl],a0[sl],bg,rim)[inner],
                 composite(f[sl],a[sl],bg,rim)[inner]]
        for col, view in enumerate(views):
            im = Image.fromarray(view)
            im.thumbnail((390,300))
            canvas.paste(im, (col*400+(400-im.width)//2, 40+row*310+(300-im.height)//2))
    return canvas


def build(plan_path, out):
    started = time.monotonic()
    plan_path, out = Path(plan_path), Path(out)
    plan = json.loads(plan_path.read_text())
    spec = validate(plan)
    key = hashlib.sha256((digest(plan_path)+VERSION+digest(__file__)+digest(Path(__file__).resolve().parents[1]/'sam2/post.py')).encode()).hexdigest()
    # One source attempt within this stable plan directory, even if a caller
    # changes output paths. The production queue owns the stable directory.
    registry = plan_path.resolve().parent / '.cached-repair-attempts'
    registry.mkdir(exist_ok=True)
    guard = registry / (plan['inputs']['source']['sha256'] + '.json')
    attempt = {'attempt_key': key, 'output': str(out.resolve()),
               'source_sha256': plan['inputs']['source']['sha256'],
               'scope': 'one source attempt per plan directory'}
    try:
        with guard.open('x') as handle:
            json.dump(attempt, handle, indent=2)
            handle.write('\n')
    except FileExistsError:
        if json.loads(guard.read_text()) != attempt:
            raise ValueError('Source already attempted in this plan directory; no new output or plan retry')
    result_path = out/'result.json'
    if result_path.exists():
        old = json.loads(result_path.read_text())
        if old['attempt_key'] != key or any(digest(p) != h for p,h in old['artifacts'].items()):
            raise ValueError('Existing candidate changed; review required, no automatic retry')
        return {**old, 'cache_reused': True}
    # mkdir is the same-source attempt lock. Failed attempts stay visible and
    # are not silently re-run; operators must review them first.
    out.mkdir(parents=True, exist_ok=False)
    save(out/'attempt.json', {'key':key, 'state':'started', 'plan':str(plan_path.resolve())})
    save(out/'plan.json', plan)
    patches = {p['frame']:p for p in plan['patches']}
    stats, cases = [], []
    try:
        for case in plan['cases']:
            caps = [cv2.VideoCapture(plan['inputs'][k]['path']) for k in KEYS]
            begin,end = case['window']
            for cap in caps:
                cap.set(cv2.CAP_PROP_POS_FRAMES, begin)
            writer = cv2.VideoWriter(str(out/(case['id']+'.mp4')),
                     cv2.VideoWriter_fourcc(*'mp4v'), spec[3], (1200,660))
            if not writer.isOpened():
                raise RuntimeError('Preview encoder unavailable')
            sheets=[]
            try:
                for frame in range(begin,end+1):
                    reads=[c.read() for c in caps]
                    if not all(ok for ok,_ in reads):
                        raise ValueError(f'Missing aligned frame {frame}')
                    src=cv2.cvtColor(reads[0][1],cv2.COLOR_BGR2RGB)
                    a0=reads[1][1][:,:,0].astype(np.float32)/255
                    f0=cv2.cvtColor(reads[2][1],cv2.COLOR_BGR2RGB).astype(np.float32)
                    a1=reads[3][1][:,:,0].astype(np.float32)/255
                    f1=cv2.cvtColor(reads[4][1],cv2.COLOR_BGR2RGB).astype(np.float32)
                    f,a=f0,a0
                    if frame in patches:
                        p=patches[frame]
                        f,a,support=blend(f0,a0,f1,a1,p['polygon'],p['feather_px'])
                        np.savez_compressed(out/f'patch-{frame}.npz', alpha=a, foreground=f)
                        stats.append({'frame':frame, 'alpha_changed_pixels':int(np.count_nonzero(a!=a0)),
                                      'outside_alpha_changed_pixels':0,'outside_rgb_changed_pixels':0})
                    im=panel(src,f0,a0,f,a,case['view_roi'],frame)
                    path=out/f'{case["id"]}-{frame}.jpg'
                    im.save(path,quality=96)
                    writer.write(cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR))
                    sheets.append(im.resize((600,330)))
            finally:
                writer.release()
                for cap in caps: cap.release()
            sheet=Image.new('RGB',(1200,330*((len(sheets)+1)//2)),'white')
            for i,im in enumerate(sheets):sheet.paste(im,((i%2)*600,(i//2)*330))
            sheet.save(out/(case['id']+'-all-frames.jpg'),quality=94)
            cases.append({**case,'patched_frames':[f for f in range(begin,end+1) if f in patches]})
        artifacts={str(p.resolve()):digest(p) for p in out.iterdir() if p.name!='attempt.json'}
        result={'version':VERSION,'attempt_key':key,'state':'needs_independent_review',
                'editor':plan['editor'],'plan_sha256':digest(plan_path),'inputs':plan['inputs'],
                'cases':cases,'patches':stats,'artifacts':artifacts,'seconds':time.monotonic()-started,
                'new_cloud_cost_usd':0,'installed':False,'production_approved':False,
                'scope':'Window previews and lossless frame patches only. Normal seven-pixel rim function at source-pixel scale; no full display-layout render.',
                'review_requirements':['source comparison','every frame including patch entry/exit',
                    'face/chair/hand preservation','light composite','normal cream rim','natural source blur']}
        save(result_path,result)
        save(out/'attempt.json', {'key':key,'state':'needs_independent_review'})
        return result
    except BaseException as ex:
        save(out/'attempt.json', {'key':key,'state':'failed_no_auto_retry','error':str(ex)})
        raise


def review(result_path, review_path):
    result_path, review_path=Path(result_path),Path(review_path)
    result=json.loads(result_path.read_text());r=json.loads(review_path.read_text())
    if (r.get('reviewer')==result['editor'] or not r.get('reviewer')
            or r.get('result_sha256')!=digest(result_path)):
        raise ValueError('Independent reviewer and exact candidate hash required')
    if any(digest(p)!=h for p,h in result['artifacts'].items()):
        raise ValueError('Candidate evidence changed after review')
    if any(digest(i['path'])!=i['sha256'] for i in result['inputs'].values()):
        raise ValueError('Source or model outputs changed after review')
    if not result['cases'] or not r['cases']:
        raise ValueError('At least one reviewed test window required')
    if set(r['cases'])!={c['id'] for c in result['cases']}:
        raise ValueError('Every test window requires its own verdict')
    for c in result['cases']:
        v=r['cases'][c['id']]
        if (v['verdict'] not in ('PASS','HOLD') or not v.get('reason')
                or v.get('frames_reviewed')!=list(range(c['window'][0],c['window'][1]+1))):
            raise ValueError('Explicit verdict and every motion frame required')
    approval={'state':'approved_test_windows' if all(v['verdict']=='PASS' for v in r['cases'].values()) else 'HOLD',
              'result_sha256':digest(result_path),'review_sha256':digest(review_path),
              'cases':r['cases'],'installed':False,'production_approved':False,
              'next':'Full-source finish and existing headroom/final review required before any delivery'}
    save(result_path.parent/'review-gate.json',approval)
    return approval


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['build','review']);p.add_argument('input');p.add_argument('output')
    args=p.parse_args()
    r=build(args.input,args.output) if args.action=='build' else review(args.input,args.output)
    print(json.dumps({k:v for k,v in r.items() if k not in ('artifacts','inputs')},indent=2))
