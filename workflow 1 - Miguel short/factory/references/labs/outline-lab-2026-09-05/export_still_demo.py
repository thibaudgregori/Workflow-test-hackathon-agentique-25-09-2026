"""Export an existing manually guided video matte as an honest still example."""
from pathlib import Path
import hashlib
import json
import shutil
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from compare import frame

ROOT = Path(__file__).resolve().parents[6]
OUT = ROOT / 'output/shorts-outline-lab/2026-09-05'

def main():
    dest = OUT / 'photo-cutout-demo'
    dest.mkdir(exist_ok=True)
    style = json.loads((ROOT / 'assets/templates/documents/still-cutout-demo.json').read_text())
    inv = next(x for x in json.loads((OUT / 'inventory.json').read_text()) if x['id'] == 'game33c')
    matte = OUT / 'results/game33c/matanyone2-r3/alpha.mkv'
    metrics = json.loads(matte.with_name('metrics.json').read_text())
    sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    assert sha(inv['plate']) == metrics['spec']['input_sha256']
    assert sha(matte) == metrics['alpha_sha256']
    rgb = frame(inv['plate'], 690)
    alpha = frame(matte, 690)[:, :, 0]
    assert rgb.shape[:2] == alpha.shape
    rgba = np.dstack((rgb, alpha))
    Image.fromarray(rgb).save(dest / 'game33c-original.png')
    Image.fromarray(rgba).save(dest / 'game33c-transparent.png')
    Image.fromarray(alpha).save(dest / 'game33c-alpha.png')
    a = alpha.astype(np.float32)[:, :, None] / 255
    composites = [rgb]
    for label in ['light', 'dark']:
        comp = np.rint(rgb * a + np.array(style[label]) * (1 - a)).clip(0, 255).astype(np.uint8)
        composites.append(comp)
        Image.fromarray(comp).save(dest / f'game33c-{label}.png')
    fontpath = '/System/Library/Fonts/Supplemental/Arial.ttf'
    big = ImageFont.truetype(fontpath, 39)
    medium = ImageFont.truetype(fontpath, 23)
    small = ImageFont.truetype(fontpath, 18)
    canvas = Image.new('RGB', (1680, 1160), tuple(style['light']))
    draw = ImageDraw.Draw(canvas)
    draw.text((30, 18), style['title'], font=big, fill='#182331')
    draw.text((30, 70), style['subtitle'], font=medium, fill='#485361')
    for i, comp in enumerate(composites):
        x = 30 + i * 550
        draw.text((x, 121), style['labels'][i], font=medium, fill='#182331')
        im = Image.fromarray(comp)
        canvas.paste(im.resize((520, 289), Image.Resampling.LANCZOS), (x, 157))
        canvas.paste(im.crop((635, 0, 1175, 570)).resize((520, 549), Image.Resampling.LANCZOS), (x, 516))
    draw.text((30, 475), style['detail_title'], font=medium, fill='#182331')
    draw.text((30, 1101), style['footer'], font=small, fill='#485361')
    canvas.save(dest / 'game33c-before-after.png')
    check = np.asarray(Image.open(dest / 'game33c-transparent.png'))
    assert np.array_equal(check[:, :, :3], rgb)
    assert np.array_equal(check[:, :, 3], alpha)
    assert alpha.min() == 0 and alpha.max() == 255 and np.any((alpha > 0) & (alpha < 255))
    provenance = dict(source=inv['plate'], frame=690, seconds=27.6,
        method='Existing MatAnyone2 1024 result initialized with a manually corrected first-frame mask; still export, not a fresh photo-model inference',
        alpha_source=str(matte), input_sha256=metrics['spec']['input_sha256'], alpha_sha256=metrics['alpha_sha256'],
        width=rgb.shape[1], height=rgb.shape[0], new_model_calls=0, new_model_cost_usd=0,
        original_rgb_preserved=True, alpha_preserved=True)
    (dest / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    assets = ROOT / 'assets/images/personal-cutouts/game33c-demo'
    assets.mkdir(parents=True, exist_ok=True)
    for name in ['game33c-transparent.png', 'provenance.json']:
        shutil.copy2(dest / name, assets / name)
    print(dest / 'game33c-before-after.png')

if __name__ == '__main__':
    main()
