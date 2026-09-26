"""Add the existing video rim to the still cutout, preserving its soft alpha."""
import importlib.util
import json
import shutil
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[6]
OUT = ROOT / 'output/shorts-outline-lab/2026-09-05/photo-cutout-demo'
SPEC = importlib.util.spec_from_file_location('video_post', Path(__file__).resolve().parents[1] / 'sam2/post.py')
post = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(post)

def main():
    style = json.loads((ROOT / 'assets/templates/documents/still-cutout-demo.json').read_text())
    rgba = np.asarray(Image.open(OUT / 'game33c-transparent.png').convert('RGBA'))
    rgb = rgba[:, :, :3].astype(np.float32)
    a = rgba[:, :, 3].astype(np.float32) / 255
    h, w = a.shape
    hi = cv2.resize(a, (w * post.UP, h * post.UP), interpolation=cv2.INTER_LINEAR) > .5
    rim = post.rim_alpha(hi, a.shape)
    cream = np.array(post.CREAM_BGR[::-1], dtype=np.float32)
    combined_alpha = a + rim * (1 - a)
    premul = rgb * a[:, :, None] + cream * (rim * (1 - a))[:, :, None]
    straight = np.divide(premul, combined_alpha[:, :, None], out=np.zeros_like(premul), where=combined_alpha[:, :, None] > 0)
    outlined = np.dstack((np.rint(straight).clip(0,255).astype(np.uint8), np.rint(combined_alpha * 255).clip(0,255).astype(np.uint8)))
    Image.fromarray(outlined).save(OUT / 'game33c-transparent-outlined.png')
    sheet = Image.new('RGB', (1460, 1240), tuple(style['light']))
    draw = ImageDraw.Draw(sheet)
    font = '/System/Library/Fonts/Supplemental/Arial.ttf'
    title = ImageFont.truetype(font, 34)
    label = ImageFont.truetype(font, 24)
    small = ImageFont.truetype(font, 19)
    draw.text((30, 20), 'Your usual video outline', font=title, fill='#182331')
    draw.text((30, 68), 'Cream #FFFDF9 / same 7 px outline / original cutout preserved', font=small, fill='#485361')
    for i, name in enumerate(['light', 'dark']):
        comp = np.rint(premul + np.array(style[name]) * (1 - combined_alpha[:, :, None])).clip(0,255).astype(np.uint8)
        im = Image.fromarray(comp)
        im.save(OUT / f'game33c-{name}-outlined.png')
        x = 30 + i * 720
        draw.text((x, 116), f'On {name}', font=label, fill='#182331')
        sheet.paste(im.resize((680,378), Image.Resampling.LANCZOS), (x,155))
        sheet.paste(im.crop((635,0,1175,570)).resize((580,612), Image.Resampling.LANCZOS), (x+50,575))
    draw.text((30,1200), 'Game 33c still / same video rim routine applied to the existing matte / no new model call', font=small, fill='#485361')
    sheet.save(OUT / 'game33c-outlined-comparison.png')
    assets = ROOT / 'assets/images/personal-cutouts/game33c-demo'
    shutil.copy2(OUT / 'game33c-transparent-outlined.png', assets / 'game33c-transparent-outlined.png')
    meta = dict(color_rgb=post.CREAM_BGR[::-1], radius_pixels=post.RIM_PX, source='pipeline/sam2/post.py:rim_alpha', original_matte_preserved=True, new_model_calls=0)
    (OUT / 'outline-provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(OUT / 'game33c-outlined-comparison.png')

if __name__ == '__main__':
    main()
