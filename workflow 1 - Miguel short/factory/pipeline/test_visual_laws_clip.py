"""A completed-state check must gate clips at that instant, then restore state."""
import unittest
from playwright.sync_api import sync_playwright
from visual_laws import CHECK_JS


class ClipVisibilityTest(unittest.TestCase):
    def test_completed_clip_and_restore(self):
        with sync_playwright() as p:
            browser=p.chromium.launch()
            page=browser.new_page(viewport={'width':1080,'height':1920})
            page.set_content('''<style>body{margin:0}</style><div id="root">
            <section data-start="0" data-duration="3" style="visibility:hidden">
            <svg width="400" height="300">
            <rect id="target" x="200" y="100" width="80" height="80" fill="black"/>
            <line id="mark" x1="20" y1="140" x2="200" y2="140" stroke="orange"
             data-connect-to="target" data-anchor-side="left" data-check-at="1"/>
            </svg></section><section data-start="3" data-duration="5" style="visibility:visible"></section>
            </div><script>let time=6;window.__timelines={main:{time:()=>time,duration:()=>8,seek:t=>{time=t}}}</script>''')
            self.assertEqual(page.evaluate(CHECK_JS),[])
            self.assertEqual(page.evaluate('window.__timelines.main.time()'),6)
            self.assertEqual(page.locator('section').evaluate_all('(xs)=>xs.map(x=>x.style.visibility)'),['hidden','visible'])
            page.locator('#mark').evaluate('(x)=>x.dataset.checkAt="4"')
            errors=page.evaluate(CHECK_JS)
            self.assertTrue(any('hides the mark' in x['detail'] for x in errors))
            browser.close()

    def test_css_bar_and_arrow_tip_keep_distance_gate(self):
        with sync_playwright() as p:
            browser=p.chromium.launch();page=browser.new_page()
            page.set_content('''<style>body{margin:0}</style><div id="root">
            <div id="target" style="position:absolute;left:200px;top:100px;width:80px;height:80px;background:black"></div>
            <div id="mark" data-connect-to="target" data-check-at="1" data-anchor-side="left"
             style="position:absolute;left:20px;top:137px;width:180px;height:6px;background:orange"></div>
            </div><script>let time=0;window.__timelines={main:{time:()=>time,duration:()=>3,seek:t=>{time=t}}}</script>''')
            self.assertEqual(page.evaluate(CHECK_JS),[])
            page.locator('#mark').evaluate('(x)=>x.style.width="170px"')
            self.assertTrue(any('10.00px' in x['detail'] for x in page.evaluate(CHECK_JS)))
            page.locator('#mark').evaluate('''x=>{x.innerHTML='<div class="ahead" style="position:absolute;left:160px;top:-7px;width:20px;height:20px;background:orange;clip-path:polygon(0% 0%,100% 50%,0% 100%)"></div>'}''')
            self.assertEqual(page.evaluate(CHECK_JS),[])
            page.locator('.ahead').evaluate('(x)=>x.style.left="150px"')
            self.assertTrue(any('10.00px' in x['detail'] for x in page.evaluate(CHECK_JS)))
            page.locator('#mark').evaluate('(x)=>x.style.transform="rotate(20deg)"')
            self.assertTrue(any('supported painted CSS' in x['detail'] for x in page.evaluate(CHECK_JS)))
            browser.close()

    def test_separate_svg_arrowhead_endpoint(self):
        with sync_playwright() as p:
            browser=p.chromium.launch();page=browser.new_page()
            page.set_content('''<svg width="400" height="300">
            <rect id="target" x="200" y="100" width="80" height="80"/>
            <g id="arrow" data-connect-to="target" data-anchor-side="left" data-check-at="1">
            <path class="sline" d="M20 140 L180 140" fill="none" stroke="orange"/>
            <path class="shead" d="M200 140 L180 150 L180 130 Z" fill="orange"/>
            </g></svg><script>let time=0;window.__timelines={main:{time:()=>time,duration:()=>3,seek:t=>{time=t}}}</script>''')
            self.assertEqual(page.evaluate(CHECK_JS),[])
            page.locator('.shead').evaluate('(x)=>x.setAttribute("class","ahead")')
            self.assertEqual(page.evaluate(CHECK_JS),[])
            page.locator('.ahead').evaluate('(x)=>{x.setAttribute("d","M180 130 L200 140 L180 150");x.setAttribute("fill","none");x.setAttribute("stroke","orange")}')
            self.assertEqual(page.evaluate(CHECK_JS),[])
            page.locator('.ahead').evaluate('(x)=>x.setAttribute("d","M170 130 L190 140 L170 150")')
            self.assertTrue(any('10.00px' in x['detail'] for x in page.evaluate(CHECK_JS)))
            page.locator('.ahead').evaluate('(x)=>x.setAttribute("d","M190 140 L170 150 L170 130 Z")')
            self.assertTrue(any('10.00px' in x['detail'] for x in page.evaluate(CHECK_JS)))
            browser.close()

    def test_highlight_compares_painted_background(self):
        with sync_playwright() as p:
            browser=p.chromium.launch();page=browser.new_page()
            page.set_content('''<div id="target" style="color:rgb(0,0,0)">TEXT</div>
            <div id="mark" data-emphasis="highlight" data-emphasis-target="target" data-check-at="1"
            style="width:100px;height:20px;border:0;background:orange;color:rgb(0,0,0)"></div>
            <script>window.__timelines={main:{duration:()=>3,seek:t=>{}}}</script>''')
            self.assertEqual(page.evaluate(CHECK_JS),[])
            page.locator('#mark').evaluate('(x)=>x.style.backgroundColor="rgb(0,0,0)"')
            self.assertTrue(any('same color' in x['detail'] for x in page.evaluate(CHECK_JS)))
            browser.close()


if __name__=='__main__':unittest.main()
