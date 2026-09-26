"""Render source-preserving portrait cover designs with the factory background.

No model/API calls. The standalone Jinja template and editable options are in assets.
"""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import time
import argparse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

W = Path(__file__).resolve().parents[1]
F = W / 'projects/personal/content/shorts-factory'
OUT = W / 'output/shorts-cover-options/2026-09-06'
TEMPLATES = W / 'assets/templates/thumbnails/shorts-covers'
sys.path.insert(0, str(F / 'formats/cutout/lib'))
import cutout_core as C
import cutout_depthfield as D


def main():
    global OUT
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=OUT/'crop-safe-v2')
    parser.add_argument('--options',type=Path,default=TEMPLATES/'options.json')
    parser.add_argument('--template',default='portrait.html.j2')
    parser.add_argument('--preparation',type=Path,default=OUT/'preparation.json')
    args=parser.parse_args()
    started = time.monotonic()
    prep = json.loads(args.preparation.read_text())
    OUT=args.output.resolve()
    OUT.mkdir(parents=True,exist_ok=True)
    options = json.loads(args.options.read_text())
    photos = {s['pose']: s for s in prep['sources']}
    media = {}
    for logo in prep['logos']:
        p = Path(logo['path'])
        C.MARK_INK[logo['key']] = C.measure_mark(logo['key'], p)
        media[logo['key']] = p.as_uri()
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=select_autoescape())
    template = env.get_template(args.template)
    sources = OUT / 'sources'
    sources.mkdir(parents=True, exist_ok=True)
    evidence = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width':1080, 'height':1920}, device_scale_factor=1)
        for i, option in enumerate(options):
            opt = dict(option)
            folder = OUT / opt['platform']
            folder.mkdir(exist_ok=True)
            photo = Path(photos[opt['pose']]['path'])
            digest = hashlib.sha256(photo.read_bytes()).hexdigest()
            assert digest == photos[opt['pose']]['sha256'], 'Source cutout changed'
            cast = list(media)
            cast_index=opt.get('cast_index',i)%8
            cast = cast[cast_index:] + cast[:cast_index]
            depth, geometry, tiles = D.field(D.lanes_at(opt.get('depth_y',1050)), media, cast, 1, rec=lambda *a, **kw:None)
            with Image.open(photo) as photo_image:
                # subject_max_w > 984 lets a wide pose (plush held out to the side) bleed a few px past the
                # safe margins instead of shrinking the face; default 984 keeps the original contract.
                max_w=opt.get('subject_max_w',984)
                safe_h=min(opt.get('photo_height',640),max_w*photo_image.height/photo_image.width)
                safe_w=safe_h*photo_image.width/photo_image.height
                alpha_box=photo_image.getchannel('A').getbbox()
                source_height=photo_image.height
            if 'body_bottom_y' in opt:
                opt['photo_y']=opt['body_bottom_y']-safe_h*alpha_box[3]/source_height
            assert safe_w<=max_w
            bleed=max(0,(safe_w-984)/2)
            opt.update(variant=opt['id'], photo_uri=photo.as_uri(),handle=C.CAP.handle('tiktok_ig'),
                       safe_subject_w=safe_w,safe_subject_h=safe_h,safe_subject_x=(1080-safe_w)/2,
                       font_uri=Path(prep['fonts']['mono']).as_uri(),
                       heavy_font_uri=(Path(prep['fonts']['mono']).parent/'JetBrainsMono-ExtraBold.ttf').as_uri(),depth_html=depth)
            opt['extra_font_uris']={weight:(Path(prep['fonts']['mono']).parent/f'JetBrainsMono-{name}.ttf').as_uri()
                                    for weight,name in [(400,'Regular'),(500,'Medium'),(600,'SemiBold')]}
            if 'font_path' in opt:
                opt['display_font_uri']=Path(opt['font_path']).as_uri()
            source = sources / (opt['id'] + '.html')
            source.write_text(template.render(**opt))
            page.goto(source.as_uri())
            page.evaluate('document.fonts.ready')
            page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
            title_style=page.locator('.title').evaluate('(e)=>{const s=getComputedStyle(e);return {size:parseFloat(s.fontSize),weight:Number(s.fontWeight),family:s.fontFamily}}')
            assert page.evaluate('(s)=>document.fonts.check(`${s.weight} 40px ${s.family}`)',title_style)
            assert title_style['weight']==opt.get('title_weight',700)
            bounds = page.locator('.title').bounding_box()
            if 'body_bottom_y' in opt:
                title_y=max(285,min(360,(300+opt['photo_y']-bounds['height']-48)/2))
                page.locator('.title').evaluate('(e,y)=>e.style.top=`${y}px`',title_y)
                bounds=page.locator('.title').bounding_box()
                page.locator('.lanewrap').evaluate_all('(els,delta)=>els.forEach(e=>e.style.transform=`translateY(${delta}px)`)',opt['photo_y']-865)
            elif 'follow_title_gap' in opt:
                photo_y=bounds['y']+bounds['height']+opt['follow_title_gap']
                page.locator('.subject').evaluate('(e,y)=>e.style.top=`${y}px`',photo_y)
                page.locator('.lanewrap').evaluate_all('(els,delta)=>els.forEach(e=>e.style.transform=`translateY(${delta}px)`)',photo_y-opt['photo_y'])
            assert bounds['x'] >= 0 and bounds['x'] + bounds['width'] <= 1080
            title_width = page.locator('.title').evaluate('(e)=>({scroll:e.scrollWidth,client:e.clientWidth})')
            assert title_width['scroll'] <= title_width['client'], (opt['id'], title_width)
            line_styles=page.locator('.title > span').evaluate_all('(els)=>els.map(e=>({text:e.textContent,size:parseFloat(getComputedStyle(e).fontSize),weight:Number(getComputedStyle(e).fontWeight),scroll:e.scrollWidth,client:e.clientWidth}))')
            assert all(line['scroll']<=line['client'] for line in line_styles),(opt['id'],line_styles)
            protected={}
            for selector in ('.brand','.title','.art','.subject','.footer'):
                if not page.locator(selector).count():
                    continue
                box=page.locator(selector).bounding_box()
                slack=bleed+1 if selector=='.subject' else 0
                assert box['x']>=40-slack and box['x']+box['width']<=1040+slack,(opt['id'],selector,box)
                bottom_limit=opt.get('body_bottom_y',1635)+1 if selector=='.subject' else 1635
                assert box['y']>=285 and box['y']+box['height']<=bottom_limit,(opt['id'],selector,box)
                protected[selector]=box
            title_box=protected['.title'];photo_box=protected['.subject']
            assert (title_box['y']+title_box['height']<=photo_box['y']-20 or
                    photo_box['y']+photo_box['height']<=title_box['y']-20), 'Headline overlaps photo'
            png = folder / (opt['id'] + '.png')
            source.write_text(page.content())
            page.screenshot(path=str(png))
            with Image.open(png) as im:
                im.convert('RGB').save(folder / (opt['id'] + '.jpg'), quality=96, subsampling=0)
                preview = im.convert('RGB').resize((270,480), Image.Resampling.LANCZOS)
                preview.save(folder / (opt['id'] + '-small.jpg'), quality=95)
                im.crop((0,240,1080,1680)).convert('RGB').save(folder / (opt['id']+'-3x4-preview.jpg'),quality=96,subsampling=0)
                # Pixel equality proves the removed outer bands contain only cream.
                rgb=im.convert('RGB')
                blank_bottom=int(opt.get('body_bottom_y',1633))+2
                for crop in ((0,0,1080,285),(0,blank_bottom,1080,1920)):
                    extrema=rgb.crop(crop).getextrema()
                    assert extrema==((246,246),(241,241),(234,234)),(opt['id'],crop,extrema)
                if 'body_bottom_y' in opt:
                    # The last visible row must contain the opaque subject, not a cream band.
                    bottom_row=rgb.crop((400,1679,680,1680))
                    assert sum(1 for pixel in bottom_row.getdata() if max(pixel)-min(pixel)>25 or max(pixel)<160)>140, 'Empty body edge in 3:4 crop'
                if opt['platform'] == 'instagram':
                    im.crop((0,285,1080,1635)).convert('RGB').save(folder / (opt['id']+'-4x5.jpg'),quality=96,subsampling=0)
            evidence.append({**option,'source_photo_sha256':digest,'master':str(png),'dimensions':[1080,1920],
                             'title_box':bounds,'title_style':title_style,'line_styles':line_styles,'font_loaded':True,'images_loaded':True,
                             'protected_boxes':protected,'outer_bands_plain_cream':True,
                             'blank_band_bottom_start':blank_bottom,
                             'render_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),
                             'depth_tiles':tiles if opt['platform']=='tiktok' else 0})
        browser.close()
    font = ImageFont.truetype(prep['fonts']['mono'], 22)
    for platform in ['tiktok','instagram']:
        batch = [o for o in options if o['platform']==platform]
        if not batch:
            continue
        columns=4 if len(batch)>5 else len(batch)
        rows=(len(batch)+columns-1)//columns
        sheet = Image.new('RGB',(35+columns*295,90+rows*565),'#EFE7DC')
        draw = ImageDraw.Draw(sheet)
        draw.text((30,22),platform.upper()+f' / {len(batch)} COVER OPTIONS',font=font,fill='#141416')
        for i, o in enumerate(batch):
            x=30+(i%columns)*295;y=78+(i//columns)*565
            with Image.open(OUT / platform / (o['id']+'.png')) as im:
                im = im.convert('RGB').resize((270,480),Image.Resampling.LANCZOS)
                sheet.paste(im,(x,y))
            draw.text((x,y+500),o['id'].upper(),font=font,fill='#C4573A')
        sheet.save(OUT / (platform+'-collage.jpg'),quality=97,subsampling=0)
        grid=Image.new('RGB',(35+columns*295,90+rows*430),'#EFE7DC');gd=ImageDraw.Draw(grid)
        gd.text((30,22),platform.upper()+' / 3:4 BROWSING PREVIEW',font=font,fill='#141416')
        for i,o in enumerate(batch):
            x=30+(i%columns)*295;y=78+(i//columns)*430
            with Image.open(OUT/platform/(o['id']+'-3x4-preview.jpg')) as im:
                grid.paste(im.resize((270,360),Image.Resampling.LANCZOS),(x,y))
            gd.text((x,y+375),o['id'].upper(),font=font,fill='#C4573A')
        grid.save(OUT/(platform+'-3x4-collage.jpg'),quality=97,subsampling=0)
    shutil.copy2(args.options,sources / 'options.json')
    shutil.copy2(TEMPLATES / args.template,sources / args.template)
    (OUT / 'verification.json').write_text(json.dumps({'renders':evidence,'local_seconds':round(time.monotonic()-started,2),
        'paid_model_calls':0,'paid_cloud_calls':0,'visual_review':'pending'},indent=2))
    print(json.dumps({'master_count':len(evidence),'output':str(OUT),'seconds':round(time.monotonic()-started,2)}))


if __name__ == '__main__':
    main()
