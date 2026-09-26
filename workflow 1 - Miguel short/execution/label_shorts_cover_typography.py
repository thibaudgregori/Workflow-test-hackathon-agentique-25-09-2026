"""Create labelled review sheets without adding technical labels to cover exports."""
import csv
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W=Path(__file__).resolve().parents[1]
ROOT=W/'output/shorts-cover-options/2026-09-06'
OUT=ROOT/'type-comparison-v4'
FONT='/Users/migle/Library/Fonts/JetBrainsMono-Bold.ttf'
NAMES={400:'Regular',500:'Medium',600:'SemiBold',700:'Bold',800:'ExtraBold'}


def sheet(options, source, dest, columns, heading):
    rows=(len(options)+columns-1)//columns
    canvas=Image.new('RGB',(20+columns*320,105+rows*475),'#EFE7DC')
    draw=ImageDraw.Draw(canvas)
    title=ImageFont.truetype(FONT,24)
    label=ImageFont.truetype(FONT,19)
    draw.text((20,20),heading,font=title,fill='#141416')
    draw.text((20,57),'JetBrains Mono | sizes on the 1080 x 1920 master',font=label,fill='#514940')
    for i,opt in enumerate(options):
        x=20+(i%columns)*320;y=100+(i//columns)*475
        with Image.open(source/'tiktok'/f'{opt["id"]}-3x4-preview.jpg') as im:
            canvas.paste(im.resize((300,400),Image.Resampling.LANCZOS),(x,y))
        size=min(opt['size'],opt.get('title_max_size',128))
        weight=opt.get('title_weight',700)
        draw.text((x,y+411),f'{opt["id"].upper()}  |  {size} px',font=label,fill='#C4573A')
        draw.text((x,y+438),f'{NAMES[weight]} ({weight})',font=label,fill='#141416')
    canvas.save(dest,quality=97,subsampling=0)


def main():
    templates=W/'assets/templates/thumbnails/shorts-covers'
    previous=json.loads((templates/'real-topics.json').read_text())
    current=json.loads((templates/'type-comparison.json').read_text())
    sheet(previous,ROOT/'real-topics-v3',OUT/'previous-six-labelled.jpg',3,'PREVIOUS SIX | FONT SIZE + WEIGHT')
    sheet(current,OUT,OUT/'ten-options-labelled.jpg',5,'10 OPTIONS | 180 px TOP ROW / 208 px BOTTOM ROW')
    rows=[]
    for group,options in [('previous',previous),('new',current)]:
        for o in options:
            rows.append({'set':group,'id':o['id'],'headline':' / '.join(o['lines']),
                         'size_px':min(o['size'],o.get('title_max_size',128)),
                         'weight':o.get('title_weight',700),'weight_name':NAMES[o.get('title_weight',700)]})
    with (OUT/'font-settings.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    lines=['# Cover font settings','','All sizes are pixels on the 1080 x 1920 master. All use JetBrains Mono. The new comparison holds the photograph, wording, colours, logo positions, and layout fixed. Labels are outside the covers.','','| Set | Option | Title | Size | Weight |','|---|---|---|---:|---|']
    for r in rows:
        lines.append(f'| {r["set"]} | {r["id"]} | {r["headline"]} | {r["size_px"]} px | {r["weight_name"]} ({r["weight"]}) |')
    (OUT/'font-settings.md').write_text('\n'.join(lines)+'\n')
    print('Created labelled sheets for the previous six and new ten; saved CSV and Markdown settings.')


if __name__=='__main__':
    main()
