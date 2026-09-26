"""Review a bounded bidirectional manual-seed test without installing it."""
import argparse
import json
from pathlib import Path
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from cached_repair import composite, panel, digest


def read(path, start, count):
    cap = cv2.VideoCapture(str(path))
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    frames = []
    for _ in range(count):
        ok, bgr = cap.read()
        if not ok:
            raise ValueError(f'Missing frame in {path}')
        frames.append(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    cap.release()
    return frames


def encoder(path, w, h, gray=False):
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-n', '-f', 'rawvideo',
        '-pix_fmt', 'gray' if gray else 'rgb24', '-s', f'{w}x{h}', '-r', '25',
        '-i', 'pipe:0', '-an', '-c:v', 'ffv1' if gray else 'libx264',
        *([] if gray else ['-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart']),
        '-threads', '2', str(path)], stdin=subprocess.PIPE)


def run(base, out):
    review = out / 'review'
    review.mkdir(exist_ok=False)
    source = read(base / 'source-hd.mp4', 602, 25)
    olda = read(base / 'mobilenetv2/alpha.mkv', 602, 25)
    oldf = read(base / 'mobilenetv2/foreground.mp4', 602, 25)
    reverse = read(out / 'reverse-result/alpha.mkv', 0, 3)
    forward = read(out / 'forward-result/alpha.mkv', 0, 23)
    new = reverse[:0:-1] + forward
    alpha = encoder(out / 'alpha602-626.mkv', 1920, 1080, True)
    video = encoder(out / 'comparison-realtime.mp4', 1920, 400)
    detail = encoder(out / 'hand-comparison-realtime.mp4', 1200, 660)
    font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 21)
    for i, (s, oa, of, a) in enumerate(zip(source, olda, oldf, new)):
        frame = 602+i
        alpha.stdin.write(a[:, :, 0].tobytes())
        aa, oo = a[:, :, 0]/255., oa[:, :, 0]/255.
        p = panel(s, of.astype('float32'), oo, s.astype('float32'), aa,
                  (1050, 350, 1770, 1030), frame)
        d = ImageDraw.Draw(p)
        d.rectangle((0, 0, 1200, 37), fill='white')
        for col, title in enumerate(['Source', 'Previous automatic', 'Manual + MatAnyone']):
            d.text((col*400+8, 8), f'{title} | {frame}', fill='black', font=font)
        p.save(review / f'frame-{frame}.jpg', quality=93)
        detail.stdin.write(np.array(p).tobytes())
        full = Image.new('RGB', (1920, 400), 'white')
        d = ImageDraw.Draw(full)
        for col, (title, arr) in enumerate(zip(['Source', 'Previous automatic', 'Manual + MatAnyone'],
                [s, composite(of.astype('float32'), oo, 28, True),
                 composite(s.astype('float32'), aa, 28, True)])):
            d.text((col*640+8, 8), f'{title} | frame {frame}', fill='black', font=font)
            full.paste(Image.fromarray(arr).resize((640, 360)), (col*640, 40))
        full.save(review / f'full-{frame}.jpg', quality=93)
        video.stdin.write(np.array(full).tobytes())
    for proc in (alpha, video, detail):
        proc.stdin.close()
        if proc.wait():
            raise RuntimeError('Encoding failed')
    for start in range(602, 627, 5):
        sheet = Image.new('RGB', (1200, 660*5))
        for n in range(5):
            sheet.paste(Image.open(review/f'frame-{start+n}.jpg'), (0, n*660))
        sheet.save(review/f'sheet-{start}-{start+4}.jpg', quality=90)
    timings = [json.loads((out/d/'result.json').read_text()) for d in ('forward-result', 'reverse-result')]
    (out/'combined-result.json').write_text(json.dumps({
        'source_frames': [602, 626], 'seed_frame': 604,
        'mapping': '602,603 from reverse indices2,1;604..626 from forward indices0..22',
        'model_seconds': sum(t['total_seconds'] for t in timings),
        'cloud_cost_usd': 0, 'installed': False,
        'alpha_sha256': digest(out/'alpha602-626.mkv'),
        'source_sha256': digest(base/'source-hd.mp4'),
        'seed_sha256': digest(out/'reviewed-seed604.png'),
        'note': 'Local MPS FP32 test. Independent visual review required.'}, indent=2)+'\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('base', type=Path)
    p.add_argument('out', type=Path)
    a = p.parse_args()
    run(a.base, a.out)
