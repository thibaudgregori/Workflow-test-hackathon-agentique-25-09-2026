"""Capture settled full composition frames, without playback or reader tests."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

RUN = Path(__file__).resolve().parents[1]
TIMES = [1.8, 8.2, 12.7, 15.3, 18.3, 24.4, 29.9, 35.5, 41.5]
OUT = RUN/'review/primeagent_page_frames'
OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch()
    for fmt in ('split','whiteboard','cutout'):
        page = browser.new_page(viewport={'width':1080,'height':1920})
        print(f'Opening {fmt}',flush=True)
        page.goto((RUN/f'projects/primeagent_{fmt}/index.html').as_uri(),wait_until='domcontentloaded')
        page.wait_for_function('!!window.__timelines?.main')
        page.evaluate('Promise.race([document.fonts.ready,new Promise(r=>setTimeout(r,6000))])')
        page.evaluate('() => {const t=window.__timelines.main;t.pause();t.progress(1,true);t.progress(0,true)}')
        imgs=[]
        for t in TIMES:
            page.evaluate('t => {window.__timelines.main.seek(t,false);}',t)
            page.evaluate('''t => { for (const c of document.getElementById('root').children) {
                if(c.dataset.start===undefined)continue;
                const s=Number(c.dataset.start),d=Number(c.dataset.duration);
                c.style.visibility=(t>=s-.01&&t<s+d-.01)?'visible':'hidden';
            }}''',t)
            page.evaluate('''async t => {await Promise.all([...document.querySelectorAll('video')].map(v=>new Promise(resolve=>{
                v.pause();const start=Number(v.dataset.start||0);const mt=Number(v.dataset.mediaStart||0);
                const target=Math.max(0,t-start+mt);
                if(v.readyState>=2 && Math.abs(v.currentTime-target)<.01){resolve();return;}
                v.addEventListener('seeked',resolve,{once:true});v.currentTime=target;setTimeout(resolve,8000);
            })))}''',t)
            print(f'Capturing {fmt} {t}',flush=True)
            path=OUT/f'{fmt}_{t:.2f}.png'
            page.screenshot(path=str(path))
            im=Image.open(path).convert('RGB').resize((360,640))
            tile=Image.new('RGB',(360,670),'white');tile.paste(im,(0,30))
            ImageDraw.Draw(tile).text((10,8),f'{fmt} {t:.2f}s',fill='black')
            imgs.append(tile)
        sheet=Image.new('RGB',(360*3,670*3),'white')
        for i,im in enumerate(imgs):sheet.paste(im,((i%3)*360,(i//3)*670))
        sheet.save(OUT/f'{fmt}_sheet.jpg',quality=95)
        page.close()
    browser.close()
print(json.dumps({'directory':str(OUT),'times':TIMES}))
