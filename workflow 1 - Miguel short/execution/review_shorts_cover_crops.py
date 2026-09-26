"""Export exact crop guides and labelled contact sheets from clean cover masters."""
from pathlib import Path
import csv
import json
from PIL import Image, ImageDraw, ImageFont

W=Path(__file__).resolve().parents[1]
OUT=W/'output/shorts-cover-options/2026-09-06/top-filled-v6'
BLUE='#167BB5'
ORANGE='#D57617'
CREAM='#EFE7DC'
FONT='/Users/migle/Library/Fonts/JetBrainsMono-Bold.ttf'
CROPS={'3x4':(0,240,1080,1680),'4x3':(0,555,1080,1365)}


def label(draw, xy, text, size=20, fill='#141416'):
    draw.text(xy,text,font=ImageFont.truetype(FONT,size),fill=fill)


def grid(items,dest,guides=False):
    columns=5;step=580 if guides else 465
    canvas=Image.new('RGB',(1520,110+step*((len(items)+4)//5)),CREAM)
    d=ImageDraw.Draw(canvas)
    label(d,(20,18),'TOP TITLES / CROP GUIDES' if guides else 'TOP TITLES / EXACT 3:4 PREVIEW',25)
    label(d,(20,56),'BLUE = vertical 3:4 | ORANGE = landscape 4:3' if guides else 'Blue edge = visible 3:4 crop. Guides are not on final covers.',19)
    for i,r in enumerate(items):
        x=20+(i%5)*300;y=100+(i//5)*step
        source=OUT/'guides'/f'{r["id"]}-crop-guide.jpg' if guides else OUT/'tiktok'/f'{r["id"]}-3x4-preview.jpg'
        height=498 if guides else 373
        with Image.open(source) as im:canvas.paste(im.resize((280,height),Image.Resampling.LANCZOS),(x,y))
        if not guides:d.rectangle((x,y,x+279,y+height-1),outline=BLUE,width=2)
        label(d,(x,y+height+10),f'{r["id"].upper()} / {r["title_weight"]}',19)
        label(d,(x,y+height+35),'/'.join(str(s['size']).removesuffix('.0') for s in r['line_styles'])+' px',18)
    canvas.save(dest,quality=96,subsampling=0)


def main():
    records=json.loads((OUT/'verification.json').read_text())['renders']
    guides=OUT/'guides';guides.mkdir(exist_ok=True)
    for r in records:
        with Image.open(r['master']) as src:
            im=src.convert('RGB');d=ImageDraw.Draw(im)
            for name,color in [('3x4',BLUE),('4x3',ORANGE)]:
                x0,y0,x1,y1=CROPS[name]
                d.rectangle((x0+4,y0+3,x1-5,y1-4),outline=color,width=8)
                src.crop(CROPS[name]).convert('RGB').save(guides/f'{r["id"]}-{name}-actual.jpg',quality=96,subsampling=0)
            im.save(guides/f'{r["id"]}-crop-guide.jpg',quality=96,subsampling=0)
    grid(records,OUT/'all-20-top-only.jpg')
    grid(records[:10],OUT/'01-10-crop-outlines.jpg',True)
    grid(records[10:],OUT/'11-20-crop-outlines.jpg',True)
    chosen='top06'
    comparison=Image.new('RGB',(1380,940),CREAM);d=ImageDraw.Draw(comparison)
    label(d,(20,18),'THE SAME COVER / EXACT CENTRED CROPS',28)
    panels=[('Full 9:16 + outlines',guides/f'{chosen}-crop-guide.jpg',(420,747),BLUE),
            ('Vertical 3:4',guides/f'{chosen}-3x4-actual.jpg',(420,560),BLUE),
            ('Landscape 4:3',guides/f'{chosen}-4x3-actual.jpg',(420,315),ORANGE)]
    for i,(title,path,size,color) in enumerate(panels):
        x=20+i*460;label(d,(x,70),title,22,color)
        with Image.open(path) as im:comparison.paste(im.resize(size,Image.Resampling.LANCZOS),(x,115))
        d.rectangle((x,115,x+size[0]-1,114+size[1]),outline=color,width=3)
    label(d,(20,898),'Crop simulations, not a live platform preview. Final cover files contain no outlines.',18)
    comparison.save(OUT/'crop-explained.jpg',quality=97,subsampling=0)
    with (OUT/'font-settings.csv').open('w') as f:
        writer=csv.writer(f);writer.writerow(['id','title','line_sizes_px','weight','title_photo_gap_px'])
        for r in records:
            boxes=r['protected_boxes'];gap=boxes['.subject']['y']-(boxes['.title']['y']+boxes['.title']['height'])
            writer.writerow([r['id'],' '.join(r['lines']),'/'.join(str(x['size']) for x in r['line_styles']),r['title_weight'],round(gap,2)])
    (OUT/'crop-geometry.json').write_text(json.dumps({'master':[1080,1920],'centred_crops':CROPS,'outlines_on_review_only':True},indent=2))
    print('Created 20 crop guides, exact crops, labelled grids and explanatory comparison.')


if __name__=='__main__':
    main()
