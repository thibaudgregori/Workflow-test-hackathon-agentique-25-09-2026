"""Build the compact decision report from actual saved experiment results."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from compare import frame,composite,STYLE,FONT

ROOT=Path(__file__).resolve().parents[6]
OUT=ROOT/'output/shorts-outline-lab/2026-09-05'

def main():
    selections=json.loads((OUT/'selection.json').read_text())
    inventory=json.loads((OUT/'inventory.json').read_text())
    labels={'vitmatte':'SAM2 + ViTMatte','sam2matting':'SAM2Matting Tiny','matanyone2':'MatAnyone 2'}
    rows=[]
    for video,modes in selections.items():
        for mode,tag in modes.items():
            d=json.loads((OUT/'results'/video/tag/'metrics.json').read_text())
            rows.append({'video':video,'model':labels[mode],'tag':tag,'seconds':d['function_seconds'],'wall_seconds':d['client_wall_seconds'],'compute_estimate_usd':d['estimated_compute_usd'],'elapsed_estimate_usd':d['conservative_elapsed_estimate_usd']})
    (OUT/'selected-results.json').write_text(json.dumps(rows,indent=2))
    costs=[r['elapsed_estimate_usd'] for r in rows if r['model']=='MatAnyone 2']
    canvas=Image.new('RGB',(1080,1600),(242,240,235));draw=ImageDraw.Draw(canvas)
    big=ImageFont.truetype(FONT,36);small=ImageFont.truetype(FONT,23);medium=ImageFont.truetype(FONT,27)
    draw.text((30,18),'Outline tests | my pick: MatAnyone 2',font=big,fill=(25,30,40))
    draw.text((30,66),f'About ${min(costs):.2f}-${max(costs):.2f} per matte at the quality setting',font=medium,fill=(25,30,40))
    draw.text((30,108),'Current SAM2',font=medium,fill=(25,30,40));draw.text((560,108),'MatAnyone 2 / corrected start',font=medium,fill=(25,30,40))
    crops={'shieldstral':(420,0,950,590),'harnessrace':(350,0,870,590),'game33c':(645,0,1175,590)}
    moments={'shieldstral':0,'harnessrace':8,'game33c':4.5}
    notes={'shieldstral':'Shieldstral | right ear restored','harnessrace':'Harness race | cleaner chair separation','game33c':'Game 33c | chair removed, beard preserved'}
    for i,inv in enumerate(inventory):
        v=inv['id'];idx=round(moments[v]*25);rgb=frame(inv['plate'],idx);y=151+i*450
        for j,path in enumerate([inv['comparison_baseline_alpha'],OUT/'results'/v/selections[v]['matanyone2']/'alpha.mkv']):
            im=Image.fromarray(composite(rgb,frame(path,idx))).crop(crops[v]).resize((380,423),Image.Resampling.LANCZOS)
            canvas.paste(im,(85+j*530,y))
        draw.text((30,y+424),notes[v],font=small,fill=(25,30,40))
    draw.text((30,1515),'Real frames. Same scale and background. Your choice comes next.',font=small,fill=(25,30,40))
    draw.text((30,1550),'Estimates exclude seed preparation and final video rendering.',font=small,fill=(25,30,40))
    canvas.save(OUT/'comparisons/summary.png')
    table='\n'.join(f"| {r['video']} | {r['model']} | {r['seconds']:.1f}s | {r['wall_seconds']:.1f}s | ${r['compute_estimate_usd']:.4f} | ${r['elapsed_estimate_usd']:.4f} |" for r in rows)
    speed=[]
    for inv in inventory:
        v=inv['id'];d=json.loads((OUT/'results'/v/'matanyone2-speed640/metrics.json').read_text())
        speed.append(f"| {v} | {d['function_seconds']:.1f}s | {d['client_wall_seconds']:.1f}s | ${d['estimated_compute_usd']:.4f} | ${d['conservative_elapsed_estimate_usd']:.4f} | [Compare](comparisons/{v}-outline-speed.png) |")
    speed_table='\n'.join(speed)
    billing=json.loads((OUT/'billing-summary.json').read_text()) if (OUT/'billing-summary.json').exists() else {}
    from jinja2 import Environment,FileSystemLoader
    env=Environment(loader=FileSystemLoader(str(ROOT/'assets/templates')),autoescape=False)
    report=env.get_template('documents/outline-test-report.md.j2').render(billing=billing,table=table,speed_table=speed_table)
    (OUT/'report.md').write_text(report)
    print('Report and summary image written')

if __name__=='__main__':main()
