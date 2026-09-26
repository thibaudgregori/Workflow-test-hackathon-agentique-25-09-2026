"""Create Instagram/TikTok covers using Miguel's approved original option 17."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import re
from PIL import Image, ImageDraw, ImageFont

W=next(p for p in Path(__file__).resolve().parents if (p/'execution/render_shorts_cover_options.py').is_file())
T=W/'assets/templates/thumbnails/shorts-covers'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_headline_plan(path):
    """Validate the agent's transcript-backed editorial decision before rendering."""
    plan=json.loads(path.read_text())
    transcript=Path(plan['transcript_path']).expanduser()
    if not transcript.is_absolute(): transcript=W/transcript
    if digest(transcript)!=plan['transcript_sha256']:
        raise ValueError('Transcript changed: read it again and refresh the headline plan.')
    raw=transcript.read_text()
    if transcript.suffix=='.json':
        data=json.loads(raw)
        if not isinstance(data,dict) or not isinstance(data.get('text'),str):
            raise ValueError('Transcript JSON must contain the complete text field; normalize other formats to a complete text file first.')
        text=data['text']
    else: text=raw
    if not text.strip() or plan.get('full_transcript_read') is not True or plan.get('transcript_character_count')!=len(text):
        raise ValueError('Read the complete transcript before preparing the headline plan.')
    normalize=lambda value:' '.join(value.casefold().split())
    evidence=plan.get('supporting_quotes',[])
    if not evidence or any(not q.strip() or normalize(q) not in normalize(text) for q in evidence):
        raise ValueError('Headline evidence must quote the actual transcript.')
    keyword=plan.get('keyword','').strip()
    lines=[x.strip().upper() for x in plan['lines']]
    if not 2<=len(lines)<=4 or any(not x or '\n' in x for x in lines):
        raise ValueError('Use two to four non-empty headline lines.')
    contains=lambda value:bool(re.search(r'(?<!\w)'+re.escape(normalize(keyword))+r'(?!\w)',normalize(value)))
    if not keyword or not contains(text) or not contains(lines[-1]):
        raise ValueError('The key word or phrase must appear in the transcript and the highlighted final line.')
    if not plan.get('keyword_reason','').strip() or not plan.get('headline_reason','').strip():
        raise ValueError('Record why the keyword and headline represent this video.')
    # THE COVER MUST SAY WHAT THE VIDEO SAYS (Miguel, 2026-09-07): "STOP COUNTING / TOKENS / PER TASK"
    # shipped for a video whose point is the opposite. The author must read the three lines as ONE
    # sentence, write that sentence down, state the video's claim in one sentence, and confirm they match.
    sentence=plan.get('headline_sentence','').strip(); claim=plan.get('video_claim','').strip()
    if not sentence or not claim or plan.get('headline_matches_claim') is not True:
        raise ValueError('Coherence check missing: add headline_sentence (the three lines read as one sentence), video_claim (one sentence from the transcript) and headline_matches_claim: true after reading them side by side.')
    joined=normalize(' '.join(lines)).replace('  ',' ')
    if any(w not in normalize(sentence) for w in joined.split() if len(w)>3 and w.isalpha()):
        raise ValueError('headline_sentence must contain the words on the cover; write the lines as the viewer reads them, not a paraphrase.')
    return plan,transcript,lines


def select_photo(args,bank,bank_dir):
    requested=args.photo.expanduser().resolve() if args.photo else None
    pose=args.pose
    if requested:
        for name,entry in bank['photos'].items():
            known=[Path(entry['source']).resolve(),Path(entry.get('original_source',entry['source'])).resolve(),*(bank_dir/f for f in entry['files'])]
            if requested in known:
                pose=name
                if requested in [Path(entry['source']).resolve(),Path(entry.get('original_source',entry['source'])).resolve()] and digest(requested)!=entry['source_sha256']:
                    raise ValueError('The original photo changed; its stored cutout must be reviewed again.')
                break
        else:
            with Image.open(requested) as im:
                if 'A' not in im.getbands() or im.getchannel('A').getextrema()[0]==255:
                    raise ValueError('New raw photo: first prepare a reviewed outlined RGBA cutout using pipeline/matting/PHOTO_WORKFLOW.md; do not use a generic background remover.')
            return requested,'custom-photo',digest(requested),{'bank_version':None,'input':str(requested),'custom_cutout_requires_visual_review':True}
    pose=pose or 'neutral-smile'
    if pose not in bank.get('active_poses',bank['photos']):
        raise ValueError(f'Pose {pose} was removed from the approved thumbnail selection.')
    if pose not in bank['photos']:
        raise ValueError(f'Unknown pose {pose}. Available: '+', '.join(bank['photos']))
    entry=bank['photos'][pose];name=pose+'-rim.png';photo=bank_dir/name
    expected=entry['sha256'][name]
    if digest(photo)!=expected:
        raise ValueError('Corrected photo does not match its bank manifest. Reconcile before rendering.')
    return photo,pose,expected,{'bank_version':bank['version'],'source':entry['source'],'bank_pose':pose,'input':str(requested or photo)}


HIGHLIGHT_RATIO=0.86   # non-highlight lines are at most this fraction of the highlight size
HIGHLIGHT_MIN=160      # px; below this the whole headline shrinks and floats up, leaving a hole above the face
HIGHLIGHT_MAX_CHARS=8
GAP_MIN,GAP_MAX=70,155  # px between the headline block bottom and the top of the cap; poses outside this band leave a hole or a collision
TITLE_BOX_PAD=19        # measured: rendered .title box height = sum(line sizes) * leading + 19 px


def pose_gaps(bank,bank_dir,option,block_h):
    """Predict, per active pose, the gap between the headline block and the head.

    Mirrors render_shorts_cover_options: the cutout is scaled to photo_height (or 984 wide),
    its alpha bottom is pinned to body_bottom_y, and the title top is centred between 300 and
    the photo top, clamped to 285..360. A raised-hand pose has a taller alpha box, so it scales
    down and its head sits ~170 px lower than arms-crossed. Miguel, 2026-09-07: use the bigger
    poses (arms-crossed, neutral-smile) under the shorter headline blocks so the gap is filled.
    """
    gaps={}
    for pose in bank.get('active_poses',bank['photos']):
        max_w=bank['photos'][pose].get('cover_max_width',984)
        with Image.open(bank_dir/f'{pose}-rim.png') as im:
            safe_h=min(option.get('photo_height',860),max_w*im.height/im.width)
            a=im.getchannel('A').getbbox();H=im.height
        photo_y=option['body_bottom_y']-safe_h*a[3]/H;head=photo_y+safe_h*a[1]/H
        title_y=max(285,min(360,(300+photo_y-block_h-48)/2))
        gaps[pose]=round(head-title_y-block_h)
    return gaps


def choose_pose(requested,gaps,seed):
    fitting=[p for p,g in gaps.items() if GAP_MIN<=g<=GAP_MAX]
    if not fitting:
        raise ValueError('No pose fits this headline block: '+json.dumps(gaps)+'. Rewrap the headline.')
    if requested in (None,'auto'):
        return fitting[int(hashlib.sha256(seed.encode()).hexdigest(),16)%len(fitting)],fitting
    if requested in gaps and not GAP_MIN<=gaps[requested]<=GAP_MAX:
        raise ValueError(f'Pose {requested} leaves a {gaps[requested]} px gap under this headline (allowed {GAP_MIN}-{GAP_MAX}). Poses that fit: '+', '.join(fitting)+'. Pass --pose auto to let the block height pick.')
    return requested,fitting  # in Avenir Next Heavy at the 902 px width, 8 characters is the longest highlight that stays >= HIGHLIGHT_MIN


def fit_lines(lines,option):
    if lines==option['lines']:
        return option['line_sizes']
    font_path=option['font_path'];tracking=option['tracking'];sizes=[]
    for i,line in enumerate(lines):
        size=240;limit=902 if i==len(lines)-1 else 940
        while size>64 and ImageFont.truetype(font_path,size).getlength(line)+tracking*len(line)>limit:
            size-=1
        if size<96:
            raise ValueError('Headline line is too long to read on a phone; shorten or rewrap it.')
        sizes.append(size)
    # THE HIGHLIGHT IS THE BIGGEST WORD (Miguel, 2026-09-07): the terracotta
    # final line carries the keyword and must be the largest type on the cover.
    # Every other line is capped to HIGHLIGHT_RATIO of it; the highlight itself
    # keeps the largest size its width allows.
    highlight=sizes[-1]
    # A LONG HIGHLIGHT SINKS THE COVER (Miguel, 2026-09-07): a wide keyword line
    # (IMPOSSIBLE, OPEN WEIGHTS, CODEX VOICE) fits only at 115-150 px, every other
    # line is capped below it, and the short block floats to the top of the frame.
    # Keep the terracotta line to HIGHLIGHT_MAX_CHARS characters (one short word,
    # a number, or two tiny words) so it renders at HIGHLIGHT_MIN px or more.
    if highlight<HIGHLIGHT_MIN:
        raise ValueError(f'The highlighted keyword line {lines[-1]!r} ({len(lines[-1])} characters) only fits at {highlight} px; it must reach {HIGHLIGHT_MIN} px. Use a keyword line of at most {HIGHLIGHT_MAX_CHARS} characters and move the longer words to the set-up lines.')
    sizes=[min(s,int(highlight*HIGHLIGHT_RATIO)) for s in sizes[:-1]]+[highlight]
    if sum(sizes)*option['title_leading']>505:
        sizes=[int(s*505/(sum(sizes)*option['title_leading'])) for s in sizes]
    if min(sizes)<96:
        raise ValueError('Too much headline text. Use fewer words or three shorter lines.')
    if max(sizes[:-1],default=0)>=sizes[-1]:
        raise ValueError('The highlighted keyword line must be the biggest type on the cover; shorten the other lines or the highlight.')
    return sizes


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--headline-plan',type=Path,help='Required transcript-backed editorial plan; see the skill')
    source=parser.add_mutually_exclusive_group()
    source.add_argument('--pose',help='Corrected photo-bank pose, or "auto" to let the headline block height pick a pose that fills the gap')
    source.add_argument('--photo',type=Path,help='Existing original photo or reviewed outlined RGBA cutout')
    parser.add_argument('--output',type=Path,help='New output directory')
    parser.add_argument('--list-poses',action='store_true')
    args=parser.parse_args()
    config=json.loads((T/'factory-default.json').read_text())
    bank_path=W/config['photo_bank'];bank=json.loads(bank_path.read_text())
    if args.list_poses:
        print('\n'.join(bank.get('active_poses',bank['photos'])));return
    if not args.output or not args.headline_plan:
        parser.error('Provide --output and --headline-plan after reading the full video transcript.')
    plan,context,lines=read_headline_plan(args.headline_plan.expanduser().resolve())
    out=args.output.expanduser().resolve()
    if out.exists() and any(out.iterdir()):parser.error('Output directory is not empty; use a new revision directory.')
    option=dict(config['default_option']);option['font_path']=str(W/option['font_path'])
    option['line_sizes']=fit_lines(lines,option)
    block_h=sum(option['line_sizes'])*option['title_leading']+TITLE_BOX_PAD
    gaps=pose_gaps(bank,bank_path.parent,option,block_h)
    if not args.photo:
        args.pose,fitting=choose_pose(args.pose,gaps,plan.get('short_id') or ' '.join(lines))
    else: fitting=None
    photo,pose,sha,provenance=select_photo(args,bank,bank_path.parent)
    provenance['pose_fit']={'block_height_px':round(block_h),'predicted_gap_px':gaps.get(pose),'gap_band':[GAP_MIN,GAP_MAX],'poses_that_fit':fitting,'all_gaps':gaps}
    option['subject_max_w']=bank['photos'].get(pose,{}).get('cover_max_width',984)
    option.update(lines=lines,size=max(option['line_sizes']),pose=pose)
    resources=json.loads((T/'factory-resources.json').read_text())
    for logo in resources['logos']:logo['path']=str(W/logo['path'])
    resources['sources']=[{'pose':pose,'path':str(photo),'sha256':sha}]
    out.mkdir(parents=True,exist_ok=True);project=out/'Project';project.mkdir()
    prep_path=project/'preparation.json';prep_path.write_text(json.dumps(resources,indent=2))
    options_path=project/'options.json';options_path.write_text(json.dumps([option],indent=2))
    provenance['source_context']={'path':str(context),'sha256':digest(context)}
    shutil.copy2(context,project/('source-context'+context.suffix))
    (project/'headline-plan.json').write_text(json.dumps(plan,indent=2))
    subprocess.run([str(W/'.venv/bin/python'),str(W/'execution/render_shorts_cover_options.py'),
                    '--preparation',str(prep_path),'--options',str(options_path),'--template',config['template'],
                    '--output',str(project/'render')],check=True)
    verification=json.loads((project/'render/verification.json').read_text());record=verification['renders'][0]
    exports=out/'Exports';exports.mkdir();previews=out/'Review';previews.mkdir()
    image_dir=project/'render/tiktok'
    files={}
    for platform in config['platforms']:
        for ext in ('jpg','png'):
            dest=exports/f'{platform}-cover.{ext}';shutil.copy2(image_dir/f'cover.{ext}',dest)
            files[dest.name]={'path':str(dest),'sha256':digest(dest),'dimensions':[1080,1920]}
    shutil.copy2(image_dir/'cover-3x4-preview.jpg',previews/'instagram-grid-3x4.jpg')
    shutil.copy2(image_dir/'cover-3x4-preview.jpg',previews/'centred-3x4-preview.jpg')
    card=Image.new('RGB',(720,1220),'#EFE7DC')
    with Image.open(previews/'instagram-grid-3x4.jpg') as im:
        card.paste(im.resize((720,960),Image.Resampling.LANCZOS),(0,0))
    d=ImageDraw.Draw(card);font=ImageFont.truetype(resources['fonts']['mono'],27)
    info=['DEFAULT 17 / AVENIR NEXT HEAVY (900)',
          'Line sizes: '+' / '.join(str(int(x['size'])) for x in record['line_styles'])+' px',
          'Centered / leading 99% / tracking -2px',
          '3:4 preview / body anchored to bottom',
          'Clean 1080 x 1920 covers in Exports/']
    for i,line in enumerate(info):d.text((20,985+43*i),line,font=font,fill='#141416')
    card.save(previews/'font-settings.jpg',quality=96,subsampling=0)
    manifest={'standard':config['standard'],'platforms':config['platforms'],'headline':lines,
              'keyword':plan['keyword'],'highlighted_text':lines[-1],'editorial_plan':plan,
              'photo':provenance,'photo_sha256':sha,'files':files,'font':{'family':option['font_family'],
              'weight':900,'line_sizes':option['line_sizes'],'line_height':.99,'letter_spacing_px':-2},
              'grid_crop':[0,240,1080,1680],'body_bottom_y':1682,'automated_checks':'passed',
              'visual_review':'pending','published':False,'paid_model_calls':0,'paid_cloud_calls':0}
    assert files['instagram-cover.jpg']['sha256']==files['tiktok-cover.jpg']['sha256']
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps({'output':str(out),'standard':config['standard'],'platforms':config['platforms'],
                      'visual_review':'pending','master_size':[1080,1920]}))


if __name__=='__main__':
    main()
