"""Compose the sealed scene and reviewed fallback matte; build only TikTok.

The approved split generator supplies its caption, audio and scene contracts.
Importing it never builds or rewrites the approved split page.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import claudesessions_split_gen as B

CAP, CC, DF, SC = B.CAP, B.CC, B.DF, B.SC
RUN, F = B.RUN, B.F
VID = 'claudesessions'
S = RUN / f'matting/{VID}'
OUT = RUN / f'projects/{VID}_cutout'

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def guard_plate_box(box, layers):
    for key in ('w','h','left','top'):
        assert box[key] == int(box[key]), (key,box)
    for layer in layers:
        assert (layers[layer]['w'],layers[layer]['h']) == (box['w'],box['h'])
    return {'box':box, 'whole_pixels':True, 'equals_encoded':layers}

def main():
    env = json.loads((HERE/f'_envelope_{VID}.json').read_text())
    ship = json.loads((S/'ship_v5.json').read_text())
    matting = json.loads((S/'matting.json').read_text())
    assert matting['headroom']['pass'] and not matting['headroom']['unsafe_frames']
    seal = json.loads((RUN/f'review/artwork_pass_{VID}.json').read_text())
    for p in (HERE/f'{VID}_scene.py', RUN/f'plans/{VID}_scene_handoff.md'):
        assert seal['evidence'][str(p)] == digest(p), f'Stale scene seal: {p}'
    for key in ('cut','rim','alpha'):
        assert digest(S/f'matte_{VID}_v5_{key}.webm') == ship['hashes'][key]
    assert env['source_sha256'] == ship['hashes']['alpha']
    for sub in ('v','music','sfx','logos'):
        (OUT/f'assets/{sub}').mkdir(parents=True,exist_ok=True)
    v = OUT/'assets/v'
    layers = {}
    for key, name in [('cut','matte.webm'),('rim','matte_rim.webm')]:
        src = S/f'matte_{VID}_v5_{key}.webm'
        shutil.copy2(src,v/name)
        assert digest(v/name) == ship['hashes'][key]
        st = src.stat()
        (v/f'_{name}.src').write_text(f'{src}\n{st.st_size} {st.st_mtime_ns}')
        layers[key] = B.probe_wh(v/name)
    (v/'_matte_source.txt').write_text(str(S))
    box = json.loads((S/'plate.json').read_text())['overwide']['plate_box']
    plate = guard_plate_box({key:box[key] for key in ('w','h','left','top')},layers)
    shutil.copy2(B.CUT/'audio.m4a',v/'voice.m4a')
    voice = {'source':str(B.CUT/'audio.m4a'), **B.probe_audio(v/'voice.m4a')}
    assert voice['sample_rate'] >= 44100
    shutil.copy2(B.MUSIC/'bed_split_v2.mp3', OUT/'assets/music/bed.mp3')
    for name in ('whoosh','pop','click'):
        shutil.copy2(B.SFXLIB/f'{name}.mp3', OUT/f'assets/sfx/{name}.mp3')
    files = {**SC.LOGO_FILES, **SC.LANE_FILES}
    cast = list(SC.CUTOUT_LOGO_LANES)
    plan = json.loads(B.PLAN.read_text())
    assert cast == plan['cutout_logo_lanes'] and not set(cast)&set(SC.LOGO_FILES)
    cast_check = DF.assert_cast_resolves(list(files),files,B.ASSETS/'logos')
    urls = {}
    for key,rel in files.items():
        src = B.ASSETS/'logos'/rel
        shutil.copy2(src,OUT/'assets/logos'/src.name)
        CC.MARK_INK[key] = CC.measure_mark(key,src)
        urls[key] = f'assets/logos/{src.name}'
    cap_y, zy0, zy1 = [env['seats'][k] for k in ('CAP_Y','ZY0','ZY1')]
    k = min(1., (zy1-zy0-16)/(SC.CONTENT_Y1-SC.CONTENT_Y0))
    top = round((zy0+zy1)/2-(SC.CONTENT_Y0+SC.CONTENT_Y1)/2*k,2)
    left = (1080-SC.CORE_W*k)/2
    B.CORE_K, B.CORE_TOP_SPLIT, B.LEFT = k,top,left
    ws, clean = B.clean_tokens(B.words())
    checks = {'word_sync':B.assert_word_sync(ws), 'cues':B.assert_cues(ws),
        'law37':B.assert_law37(ws), 'law41':B.assert_spacing_law(),
        'law39':B.assert_label_law(), 'law42':B.assert_lifetime_law()}
    beats, captions = B.caption_beats(CAP.PillMeasurer(HERE/'_pillwidths_claudesessions_cutout.json'),ws,clean)
    CAP.assert_law12(cap_y,max(b['w'] for b in beats))
    band = B.guard_core_band('cutout',top,k,cap_y)
    rail = B.guard_rail('cutout')
    scene, tweens = SC.build(B.media(), B.outro_lockup('tiktok_ig'))
    scene, repairs = B.repair_dom(scene)
    scene, contracts = B.declare_contracts(scene)
    bf = json.loads((HERE/f'_df/bandframes_{VID}.json').read_text())
    assert bf['source_sha256'] == env['source_sha256']
    y0, seat = DF.seat(bf,cap_bottom=cap_y+CAP.CAP_PILL_HEIGHT/2,
        plate_top=box['top'],plate_scale=box['h']/900,plate_left=box['left'])
    lanes = DF.lanes_at(y0)
    steps = DF.step_beats(ws,B.DUR,n=6,fps=25)
    field,geom,nt = DF.field(lanes,urls,cast,len(steps),rec=lambda *a,**kw:None)
    tweens += DF.schedule(lanes,steps)
    for i,(name,*_) in enumerate(lanes):
        tweens += [f'tl.set("#lw-{name}",{{opacity:0}},0);',
            f'tl.to("#lw-{name}",{{opacity:1,duration:0.52,ease:SOFT}},{SC.BESPOKE[0]["t"]+i*.1:.2f});']
    assert not any(key in ' '.join(w['text'] for w in ws).lower() for key in cast)
    body = [f'<div class="abs ground" style="inset:0;background:{SC.CREAM}"></div>',
        f'<section id="tz-cut" class="clip" data-start="0" data-duration="{B.DUR}" data-track-index="2" style="left:0;top:0;width:1080px;height:1920px">',
        f'<div id="core" class="abs core" data-container style="left:{left}px;top:{top}px;width:{SC.CORE_W}px;height:{SC.CORE_H}px;transform:scale({k})">',
        scene,'</div></section>',
        '<div id="lanes" class="abs" data-overlap-ok data-bleed style="left:0;top:0;width:1080px;height:1920px">'+field+'</div>']
    for name,file,z,filter_css in [('matte-rim','matte_rim.webm',59,'filter:drop-shadow(0 10px 26px rgba(0,0,0,.20));'),('matte','matte.webm',60,'')]:
        body.append(f'<video id="{name}" src="assets/v/{file}" data-start="0" data-duration="{B.DUR}" data-media-start="0" data-track-index="{z}" muted playsinline style="position:absolute;left:{int(box["left"])}px;top:{int(box["top"])}px;width:{int(box["w"])}px;height:{int(box["h"])}px;{filter_css}"></video>')
    body += [B.caption_html(beats,cap_y),B.audio_html(B.sfx_plan())]
    page = B.head(B.TITLE,1080,1920,1,'')+'\n'.join(body)+B.tail(tweens)
    edge_fade = CC.guard_edge_fade(page)
    (OUT/'index.html').write_text(page)
    objs = B.phone_objects()
    report = {'video':VID,'format':'cutout','fps':25,'duration':B.DUR,
        'plate':plate,'seat':cap_y,'core':{'left':left,'top':top,'scale':k},
        'envelope':env['seats'],'voice':voice,'band':band,'rail':rail,
        'depth_field':{'seat':seat,'lanes':geom,'tiles':nt,'step_beats':steps,'step_n':6,'cast':cast,
            'pop_behind':None,'reason':'No depth-lane product is named in this take; the subject mark stays on the stage.'},
        'matte':{'session':str(S),'cut':layers['cut'],'rim':layers['rim'],'hashes':ship['hashes']},
        'shared':{'beat_edges':SC.BEAT_EDGES,'phone_test_objects':objs},
        'captions':captions,'caption_beats':beats,'checks':checks,'cast':cast_check,
        'dom_repairs':repairs,'contracts':contracts,'edge_fade':edge_fade,'handle':CAP.handle('tiktok_ig')}
    for name in ('_build','_geom'):
        (HERE/f'{name}_{VID}_cutout.json').write_text(json.dumps(report,indent=2))
    qc = ['--voice-master',str(B.CUT/'audio.m4a')]
    for obj in objs:
        qc += ['--phone-at',f'{obj["t"]}:'+','.join(map(str,obj['bbox']))+':'+obj['name']]
    qc += ['--alpha',str(S/f'matte_{VID}_v5_alpha.webm'),'--edge-box',
        f'{int(box["w"])}x{int(box["h"])}+{int(box["left"])}+{int(box["top"])}',
        '--plate',str(S/f'plate_display_{int(box["w"])}x{int(box["h"])}.mp4')]
    job = {'project':str(OUT),'vid':VID,'fmt':'cutout','quality':'high','geom':str(HERE/f'_geom_{VID}_cutout.json'),
        'stage':str(RUN/f'staging/tiktok/{VID}_cutout.mp4'),'qc_args':qc}
    (HERE/f'_job_{VID}_cutout.json').write_text(json.dumps(job,indent=2))
    (HERE/f'_spec_{VID}.json').write_text(json.dumps({'run':str(RUN),'out_dir':str(RUN/'output'),'jobs':[job]},indent=2))
    print(json.dumps({'project':str(OUT),'plate':plate,'seat':cap_y,'core':report['core'],'word_sync':checks['word_sync']},indent=2))

if __name__ == '__main__':
    main()
