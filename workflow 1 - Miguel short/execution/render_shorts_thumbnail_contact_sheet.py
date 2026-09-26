"""Render one transcript-backed cover per photo-bank pose and a labelled collage."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

W=next(p for p in Path(__file__).resolve().parents if (p/'execution/render_shorts_thumbnail.py').is_file())


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--headline-plan',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();out=args.output.resolve();plan=args.headline_plan.resolve()
    if out.exists() and any(out.iterdir()):parser.error('Use a new output directory.')
    bank=json.loads((W/'assets/images/miguel-photo-bank/manifest.json').read_text())
    poses=list(bank.get('active_poses',bank['photos']));started=time.monotonic()
    out.mkdir(parents=True,exist_ok=True)
    def render(pose):
        start=time.monotonic()
        result=subprocess.run([str(W/'.venv/bin/python'),str(W/'execution/render_shorts_thumbnail.py'),
            '--headline-plan',str(plan),'--pose',pose,'--output',str(out/pose)],capture_output=True,text=True)
        if result.returncode:raise RuntimeError(f'{pose}: {result.stderr}')
        return {'pose':pose,'seconds':round(time.monotonic()-start,2),'bundle':str(out/pose)}
    with ThreadPoolExecutor(max_workers=3) as pool: records=list(pool.map(render,poses))
    width=480;image_h=640;cell_h=750;gap=24;header=110;cols=3;rows=(len(poses)+cols-1)//cols
    sheet=Image.new('RGB',(gap+cols*(width+gap),header+rows*(cell_h+gap)),'#EFE7DC')
    draw=ImageDraw.Draw(sheet)
    font_path=str(W/'assets/fonts/jetbrains-mono/JetBrainsMono-Bold.ttf')
    titlefont=ImageFont.truetype(font_path,32);font=ImageFont.truetype(font_path,19)
    draw.text((24,20),f'OPTION 17 / ALL {len(poses)} PHOTOS / INSTAGRAM 3:4',font=titlefont,fill='#141416')
    plan_data=json.loads(plan.read_text())
    draw.text((24,66),'Transcript keyword: '+plan_data['keyword']+' | Highlight: '+plan_data['lines'][-1],font=font,fill='#514940')
    for i,record in enumerate(records):
        folder=Path(record['bundle']);m=json.loads((folder/'manifest.json').read_text())
        x=gap+(i%cols)*(width+gap);y=header+(i//cols)*(cell_h+gap)
        with Image.open(folder/'Review/instagram-grid-3x4.jpg') as im:
            sheet.paste(im.resize((width,image_h),Image.Resampling.LANCZOS),(x,y))
        for j,line in enumerate([f'{i+1:02d}  '+record['pose'],'Avenir Next Heavy / 900','Sizes: '+' / '.join(map(str,m['font']['line_sizes']))+' px']):
            assert draw.textlength(line,font=font)<=width
            draw.text((x,y+image_h+14+j*27),line,font=font,fill='#C4573A' if j==0 else '#141416')
    collage=out/'all-photos-collage.jpg';sheet.save(collage,quality=97,subsampling=0)
    manifest={'photos':records,'count':len(records),'headline_plan':str(plan),'collage':str(collage),
              'elapsed_seconds':round(time.monotonic()-started,2),'paid_calls':0,'visual_review':'pending','published':False}
    (out/'batch-manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(manifest))


if __name__=='__main__':main()
