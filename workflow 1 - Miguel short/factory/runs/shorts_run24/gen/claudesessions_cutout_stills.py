"""Full-frame local page proofs at settled beats, with the actual video layers."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

RUN = Path(__file__).resolve().parents[1]
OUT = RUN/'review/claudesessions_cutout_stills'
OUT.mkdir(exist_ok=True)
times = [1.9, 2.4, 4.6, 9.4, 16.8, 19.4]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True,
        executable_path='/Applications/Brave Browser.app/Contents/MacOS/Brave Browser')
    page = browser.new_page(viewport={'width':1080,'height':1920})
    page.goto((RUN/'projects/claudesessions_cutout/index.html').as_uri())
    page.wait_for_function('!!window.__timelines?.main')
    page.evaluate('document.fonts.ready')
    page.evaluate('() => {const t=window.__timelines.main;t.pause();t.progress(1,true);t.progress(0,true);} ')
    for t in times:
        page.evaluate('''async t => {
            window.__timelines.main.seek(t,false);
            for(const el of document.querySelector('#root').children) {
                if(el.dataset.start !== undefined) {
                    const a=Number(el.dataset.start), b=a+Number(el.dataset.duration);
                    el.style.visibility=t>=a && t<b ? 'visible':'hidden';
                }
            }
            await Promise.all(Array.from(document.querySelectorAll('video')).map(v=>new Promise(resolve=>{
                v.pause(); v.addEventListener('seeked',resolve,{once:true}); v.currentTime=t;
                setTimeout(resolve,3000);
            })));
        }''',t)
        page.screenshot(path=str(OUT/f'{t:.2f}.png'))
    browser.close()
(OUT/'manifest.json').write_text(json.dumps({'times':times,'project':str(RUN/'projects/claudesessions_cutout')},indent=2))
print(OUT)
