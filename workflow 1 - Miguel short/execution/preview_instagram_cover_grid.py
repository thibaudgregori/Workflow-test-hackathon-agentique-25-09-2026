"""Show clean centred 3:4 cover crops in a three-column profile-grid preview."""
from pathlib import Path
import json
from PIL import Image

W=Path(__file__).resolve().parents[1]
SOURCE=W/'output/shorts-cover-options/2026-09-06/top-filled-v6'
OUT=W/'output/shorts-cover-options/2026-09-06/instagram-grid-v7'


def make_grid(records,dest):
    width,height,gap=360,480,3
    rows=(len(records)+2)//3
    canvas=Image.new('RGB',(width*3+gap*2,rows*height+gap*(rows-1)),'white')
    for i,record in enumerate(records):
        with Image.open(record['master']) as master:
            crop=master.crop((0,240,1080,1680)).convert('RGB')
            canvas.paste(crop.resize((width,height),Image.Resampling.LANCZOS),((i%3)*(width+gap),(i//3)*(height+gap)))
    canvas.save(dest,quality=97,subsampling=0)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    records=json.loads((SOURCE/'verification.json').read_text())['renders']
    make_grid(records,OUT/'instagram-grid-all-20.jpg')
    for start in (0,9,18):
        make_grid(records[start:start+9],OUT/f'instagram-grid-{start+1:02d}-{min(start+9,len(records)):02d}.jpg')
    (OUT/'README.md').write_text('Clean three-column Instagram profile-grid preview. Tiles are exact centred 3:4 crops from the existing 1080 x 1920 masters: x=0..1080, y=240..1680. No guide lines, font annotations, account statistics, or fabricated app UI. Options run left to right, top to bottom. This is a layout mockup; final app placement depends on the selected cover crop. No covers were published or changed on Instagram.\n')
    (OUT/'order.json').write_text(json.dumps([{'position':i+1,'id':r['id'],'title':' '.join(r['lines'])} for i,r in enumerate(records)],indent=2))
    print('Saved clean 3-column, 3:4 Instagram grid previews.')


if __name__=='__main__':
    main()
