"""Emphasis ink is judged on what PAINTS: a wrapper DIV around a stroked SVG must
compare the SVG's stroke with the target's ink, not the wrapper's inherited colour
(run-16 MiniMax false failure, 2026-09-06). Real same-colour ink and clearance
still fail."""
import unittest
from playwright.sync_api import sync_playwright
from visual_laws import CHECK_JS

PAGE = '''<style>body{margin:0;color:#0b1e3a}</style><div id="root">
<div id="target" style="position:absolute;left:300px;top:300px;width:200px;height:60px;color:%(text)s;font:32px sans-serif">MiniMax</div>
<div id="emph" data-emphasis="box" data-emphasis-target="target" data-check-at="1"
 style="position:absolute;left:280px;top:280px;width:240px;height:100px">
 <svg width="240" height="100" viewBox="0 0 240 100" style="display:block">
  <rect x="2" y="2" width="236" height="96" fill="none" stroke="%(stroke)s" stroke-width="4"/>
 </svg></div>
</div><script>let time=0;window.__timelines={main:{time:()=>time,duration:()=>3,seek:t=>{time=t}}}</script>'''


class EmphasisInkTest(unittest.TestCase):
    def run_page(self, page, **kw):
        page.set_content(PAGE % kw)
        return page.evaluate(CHECK_JS)

    def test_nested_svg_different_colour_passes(self):
        with sync_playwright() as p:
            b = p.chromium.launch(); page = b.new_page()
            self.assertEqual(self.run_page(page, text='rgb(11, 30, 58)', stroke='rgb(20, 184, 166)'), [])
            b.close()

    def test_nested_svg_same_colour_fails(self):
        with sync_playwright() as p:
            b = p.chromium.launch(); page = b.new_page()
            errors = self.run_page(page, text='rgb(11, 30, 58)', stroke='rgb(11, 30, 58)')
            self.assertTrue(any('same color' in e['detail'] for e in errors), errors)
            b.close()

    def test_wrapper_inherited_colour_is_not_ink(self):
        # The wrapper inherits body colour (navy) but paints nothing itself; only the teal stroke counts.
        with sync_playwright() as p:
            b = p.chromium.launch(); page = b.new_page()
            self.assertEqual(self.run_page(page, text='rgb(11, 30, 58)', stroke='rgb(20, 184, 166)'), [])
            page.locator('#emph svg rect').evaluate('(x)=>x.setAttribute("stroke","none")')
            errors = page.evaluate(CHECK_JS)
            self.assertTrue(any('paints no visible ink' in e['detail'] for e in errors), errors)
            b.close()

    def test_clearance_uses_painted_stroke_width(self):
        with sync_playwright() as p:
            b = p.chromium.launch(); page = b.new_page()
            self.assertEqual(self.run_page(page, text='rgb(11, 30, 58)', stroke='rgb(20, 184, 166)'), [])
            page.locator('#emph').evaluate('(x)=>{x.style.left="296px";x.style.width="208px"}')  # 4px gap minus half a 4px stroke
            errors = page.evaluate(CHECK_JS)
            self.assertTrue(any('4px clearance' in e['detail'] for e in errors), errors)
            b.close()


if __name__ == '__main__':
    unittest.main()


NESTED = '''<style>body{margin:0}</style><div id="root">
<div id="site" style="position:absolute;left:200px;top:200px;width:300px;height:200px;color:%(text)s;font:28px sans-serif">
 <svg width="300" height="200" viewBox="0 0 300 200" style="position:absolute;left:0;top:0">
  <rect x="0" y="0" width="300" height="200" fill="rgb(247, 241, 227)" stroke="none"/>
  <rect id="site-border" data-emphasis="border" data-emphasis-target="site" data-check-at="1"
        x="-8" y="-8" width="316" height="216" fill="rgb(247, 241, 227)" stroke="%(stroke)s" stroke-width="4"/>
 </svg>
 <div style="position:absolute;left:20px;top:20px">Native plants</div>
</div></div><script>let time=0;window.__timelines={main:{time:()=>time,duration:()=>3,seek:t=>{time=t}}}</script>'''


class NestedEmphasisChildTest(unittest.TestCase):
    """An emphasis drawn INSIDE its own target (Plants site border) is never compared with itself,
    and its unchanged paper fill is not its ink; a real same-colour stroke still fails."""

    def test_child_border_different_colour_passes(self):
        with sync_playwright() as p:
            b = p.chromium.launch(); page = b.new_page()
            page.set_content(NESTED % dict(text='rgb(11, 30, 58)', stroke='rgb(120, 60, 200)'))
            self.assertEqual(page.evaluate(CHECK_JS), [])
            b.close()

    def test_child_border_same_colour_as_target_text_fails(self):
        with sync_playwright() as p:
            b = p.chromium.launch(); page = b.new_page()
            page.set_content(NESTED % dict(text='rgb(120, 60, 200)', stroke='rgb(120, 60, 200)'))
            errors = page.evaluate(CHECK_JS)
            self.assertTrue(any('same color' in e['detail'] for e in errors), errors)
            b.close()
