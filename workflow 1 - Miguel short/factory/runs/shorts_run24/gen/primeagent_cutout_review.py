"""Capture settled cutout frames, including the head of the take.

The head of the take is the point of this rerun: the depth lanes must be behind
him from frame 0, so the first four captures sit inside the first two seconds.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

RUN = Path(__file__).resolve().parents[1]
TIMES = [0.04, 0.5, 1.2, 1.8, 3.5, 6.0, 8.2, 12.7, 15.3, 18.3, 24.4, 29.9,
         35.5, 41.5]
OUT = RUN / 'review/primeagent_cutout_frames'
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1080, 'height': 1920})
    page.goto((RUN / 'projects/primeagent_cutout/index.html').as_uri(),
              wait_until='domcontentloaded')
    page.wait_for_function('!!window.__timelines?.main')
    page.evaluate('Promise.race([document.fonts.ready,'
                  'new Promise(r=>setTimeout(r,6000))])')
    page.evaluate('() => {const t=window.__timelines.main;t.pause();'
                  't.progress(1,true);t.progress(0,true)}')
    imgs = []
    for t in TIMES:
        page.evaluate('t => {window.__timelines.main.seek(t,false);}', t)
        page.evaluate('''t => { for (const c of document.getElementById('root').children) {
            if(c.dataset.start===undefined)continue;
            const s=Number(c.dataset.start),d=Number(c.dataset.duration);
            c.style.visibility=(t>=s-.01&&t<s+d-.01)?'visible':'hidden';
        }}''', t)
        page.evaluate('''async t => {await Promise.all([...document.querySelectorAll('video')].map(v=>new Promise(resolve=>{
            v.pause();const start=Number(v.dataset.start||0);const mt=Number(v.dataset.mediaStart||0);
            const target=Math.max(0,t-start+mt);
            if(v.readyState>=2 && Math.abs(v.currentTime-target)<.01){resolve();return;}
            v.addEventListener('seeked',resolve,{once:true});v.currentTime=target;setTimeout(resolve,8000);
        })))}''', t)
        print(f'Capturing cutout {t}', flush=True)
        path = OUT / f'cutout_{t:05.2f}.png'
        page.screenshot(path=str(path))
        im = Image.open(path).convert('RGB').resize((300, 533))
        tile = Image.new('RGB', (300, 563), 'white')
        tile.paste(im, (0, 30))
        ImageDraw.Draw(tile).text((8, 8), f'cutout {t:.2f}s', fill='black')
        imgs.append(tile)
    sheet = Image.new('RGB', (300 * 5, 563 * 3), 'white')
    for i, im in enumerate(imgs):
        sheet.paste(im, ((i % 5) * 300, (i // 5) * 563))
    sheet.save(OUT / 'cutout_sheet.jpg', quality=95)
    page.close()
    browser.close()
print(json.dumps({'directory': str(OUT), 'times': TIMES}))
