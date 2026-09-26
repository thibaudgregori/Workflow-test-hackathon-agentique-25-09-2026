"""Local source/alpha previews with a cream rim; no model or cloud calls."""
import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('video', type=Path)
    ap.add_argument('alpha', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--rim', type=int, default=7, help='Radius in source pixels')
    a = ap.parse_args()
    if a.output.exists():
        raise ValueError('Output exists; preserve earlier previews')
    source, mask = cv2.VideoCapture(str(a.video)), cv2.VideoCapture(str(a.alpha))
    width, height = int(source.get(3)), int(source.get(4))
    fps, count = source.get(5), int(source.get(7))
    if not 0 < count <= 5400 or not 0 < fps <= 60 or count / fps > 180:
        raise ValueError('Expected a complete short video of at most180seconds')
    if (int(mask.get(3)), int(mask.get(4))) != (width, height):
        raise ValueError('Source and alpha geometry differ')
    if abs(mask.get(5) - fps) > .001:
        raise ValueError('Source and alpha frame rates differ')
    a.output.mkdir(parents=True)
    cv2.setNumThreads(2)
    tile_h = min(960, height)
    tile_w = round(width * tile_h / height / 2) * 2
    header = 48
    font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 20)
    labels = Image.new('RGB', (tile_w * 3, header), '#e6e0d7')
    draw = ImageDraw.Draw(labels)
    for i, label in enumerate(('ORIGINAL', 'DARK', 'CREAM')):
        draw.text((i * tile_w + 18, 14), label, fill='#152537', font=font)
    labels = np.asarray(labels)
    encoders = []
    def encoder(name, w, h):
        cmd = ['ffmpeg', '-v', 'error', '-n', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
               '-s', f'{w}x{h}', '-r', str(fps), '-i', 'pipe:0', '-i', str(a.video),
               '-map', '0:v:0', '-map', '1:a:0?', '-c:v', 'libx264', '-preset', 'veryfast',
               '-crf', '18', '-pix_fmt', 'yuv420p', '-threads', '2', '-c:a', 'copy',
               '-movflags', '+faststart', '-shortest', str(a.output / name)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        encoders.append(proc)
        return proc
    dark = encoder('cutout-dark.mp4', width, height)
    cream = encoder('cutout-cream.mp4', width, height)
    comparison = encoder('comparison.mp4', tile_w * 3, tile_h + header)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * a.rim + 1,) * 2)
    backgrounds = [np.array(c, np.float32) for c in ((21, 37, 55), (247, 243, 236))]
    rim_color = np.array((255, 253, 249), np.float32)
    start = time.monotonic()
    written = 0
    evidence_frames = {round(t * fps) for t in (0, 5, 15, 30, 45, 60, 75, 90, count / fps - 1)}
    try:
        for i in range(count):
            ok, bgr = source.read()
            mok, alpha_bgr = mask.read()
            if not ok or not mok:
                raise ValueError(f'Missing source/alpha frame{i}')
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            alpha_u8 = alpha_bgr[:, :, 0]
            alpha = alpha_u8.astype(np.float32)[:, :, None] / 255
            rim = cv2.dilate(alpha_u8, kernel).astype(np.float32)[:, :, None] / 255
            panels = [cv2.resize(rgb, (tile_w, tile_h), interpolation=cv2.INTER_AREA)]
            for proc, bg in zip((dark, cream), backgrounds):
                under = rim_color * rim + bg * (1 - rim)
                composed = np.rint(rgb * alpha + under * (1 - alpha)).clip(0, 255).astype(np.uint8)
                proc.stdin.write(composed.tobytes())
                panels.append(cv2.resize(composed, (tile_w, tile_h), interpolation=cv2.INTER_AREA))
            frame = np.vstack((labels, np.hstack(panels)))
            comparison.stdin.write(frame.tobytes())
            if i in evidence_frames:
                Image.fromarray(frame).save(a.output / f'frame-{i:06d}.jpg', quality=94)
            written += 1
            if i % 300 == 0:
                print(f'PREVIEW {i}/{count} {time.monotonic()-start:.1f}s', flush=True)
        if mask.read()[0]:
            raise ValueError('Alpha contains extra frames')
    finally:
        source.release()
        mask.release()
        for proc in encoders:
            proc.stdin.close()
        codes = [proc.wait() for proc in encoders]
    if any(codes) or written != count:
        raise RuntimeError('Incomplete preview export')
    result = {'frames': written, 'fps': fps, 'source_size': [width, height],
              'seconds': time.monotonic() - start, 'rim_source_pixels': a.rim,
              'source': str(a.video.resolve()), 'alpha': str(a.alpha.resolve()),
              'cloud_cost_usd': 0, 'files': {}}
    for path in (a.video, a.alpha, *sorted(a.output.glob('*.mp4'))):
        result['files'][str(path.resolve())] = hashlib.sha256(path.read_bytes()).hexdigest()
    (a.output / 'verification.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
