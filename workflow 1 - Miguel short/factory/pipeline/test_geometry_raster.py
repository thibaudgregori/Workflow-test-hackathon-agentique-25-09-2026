import unittest
from playwright.sync_api import sync_playwright
from geometry_audit import LAYOUT_JS, check_layout, _lthin

class RasterClassificationTest(unittest.TestCase):
    def test_short_declared_connector(self):
        self.assertTrue(_lthin(dict(w=6,h=26,connectTo="target")))
        self.assertFalse(_lthin(dict(w=60,h=260,connectTo="target")))
        self.assertFalse(_lthin(dict(w=6,h=26)))

    def test_drawn_panel_logo_and_real_raster(self):
        with sync_playwright() as p:
            browser=p.chromium.launch();page=browser.new_page()
            page.set_content('''<style>body{margin:0}.panel{position:absolute;left:50px;top:50px;width:400px;height:300px;border:4px solid black}.box{position:absolute;left:42px;top:42px;width:424px;height:324px;border:4px solid rgb(196,87,58)}</style>
            <div id="root"><section data-start="0" data-duration="3">
            <div id="panel" class="panel"><img id="logo" style="width:30px;height:30px;margin:120px 180px"></div>
            <div id="box" class="box" data-emphasis="box"></div></section></div>
            <script>window.__timelines={main:{pause(){},seek(){}}}</script>''')
            rows=page.evaluate(LAYOUT_JS,1)["objs"]
            self.assertFalse(next(x for x in rows if x['id']=='panel')['img'])
            self.assertFalse(any(x[0]=='enclose' and x[1]=='error' for x in check_layout(rows)))
            page.locator('#logo').evaluate('x=>{x.style.width="100%";x.style.height="100%";x.style.margin="0"}')
            rows=page.evaluate(LAYOUT_JS,1)["objs"]
            self.assertTrue(next(x for x in rows if x['id']=='panel')['img'])
            self.assertTrue(any(x[0]=='enclose' and x[1]=='error' for x in check_layout(rows)))
            browser.close()

if __name__=='__main__':unittest.main()
