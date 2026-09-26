"""Production evidence, prepared context and approval contracts. No paid calls.

`--evidence` takes ONE reader round or several, comma separated: the cold
reader is a stochastic instrument and a shared scene seals on SEAL_ROUNDS of
them (run 16, kimiwork, 2026-09-06).
"""
from pathlib import Path
import argparse, hashlib, json, os, shutil, sys

F=Path(__file__).resolve().parent.parent
ROOT=F.parents[3]
sys.path.insert(0,str(F/'pipeline/matting'))
from selection import atomic_json, digest


def project_hash(project):
    p=Path(project).resolve()
    rows=[]
    for f in sorted(p.rglob('*')):
        if f.is_file() and not any(x.startswith('.') or x in ('node_modules','output') for x in f.relative_to(p).parts):
            rows.append((str(f.relative_to(p)),digest(f)))
    if not rows:raise ValueError('Empty project')
    return hashlib.sha256(json.dumps(rows).encode()).hexdigest()


def check_phone(run, vid, fmt, project):
    if fmt=='cutout' and (Path(run)/'production-policy.json').exists():
        matte=Path(run)/'matting'/vid
        result=json.loads((matte/'matting.json').read_text())
        guard=result.get('headroom',{})
        if guard.get('pass') is not True or guard.get('identity',{}).get('guard_sha256')!=digest(F/'pipeline/matting/headroom.py') or guard.get('identity',{}).get('alpha_sha256')!=digest(matte/'alpha_v1.mkv'):
            raise ValueError('Cutout needs a current full-frame headroom PASS; recrop and re-review, never carve the head')
    rec=json.loads((Path(run)/'review'/f'phone_pass_{vid}_{fmt}.json').read_text())
    if rec.get('verdict')!='PASS' or rec.get('project_sha256')!=project_hash(project):
        raise ValueError('Missing or stale independent phone approval')
    for p,h in rec.get('evidence',{}).items():
        if not Path(p).exists() or digest(p)!=h:raise ValueError('Phone approval evidence changed')
    if not rec.get('evidence'):raise ValueError('No independent reader evidence')
    return rec


def prepare_context(run, vid):
    run=Path(run); transcript=run/'cuts'/vid/'transcript_tight.json'
    if not transcript.exists():raise ValueError('Complete tight transcript missing')
    intake=json.loads((run/'prep/_intake.json').read_text())
    row=next(x for x in intake if x['id']==vid)
    data={'video':row,'transcript':json.loads(transcript.read_text()),'stages':{},
          'rules':{'standard':str(F/'STANDARD.md'),'learnings':str(F/'LEARNINGS.md'),
                   'workflow':str(ROOT/'.claude/workflows/daily-shorts.js')},
          'source_files':{},'policy':'Fresh bespoke creation per recording; shared only across its formats.'}
    for p in (run/'prep/stages').glob(vid+'.*.json'):data['stages'][p.stem]=json.loads(p.read_text())
    for p in sorted((run/'intake').rglob('*')):
        if p.is_file() and p.suffix in ('.json','.md','.txt'):
            data['source_files'][str(p)]=p.read_text()
    target=run/'plans'/f'{vid}_context.json';atomic_json(target,data)
    atomic_json(run/'production-policy.json',{'version':2,'require_phone_approval':True,'final_delivery_requires_clerk':True})
    return {'context':str(target),'source_files':len(data['source_files'])}


def plan_report(run,vid):
    p=Path(run)/'plans'/f'{vid}_plan.json';d=json.loads(p.read_text())
    # The plan remains complete; this readable view is generated, never re-authored.
    target=p.with_suffix('.md')
    target.write_text('# '+vid+' — creative plan\n\n'+d.get('lane_reason','')+'\n\n```json\n'+json.dumps(d,indent=2,ensure_ascii=False)+'\n```\n')
    return {'plan_json':str(p),'plan_md':str(target)}


SEAL_ROUNDS=3            # independent dispatches a SHARED module needs before it can be sealed
MISREAD_MAX=1            # a SECOND reader naming a different object is the drawing, not the noise
MISREAD_FRACTION=0.25    # ... and so is one in four


def evidence_rounds(evidence):
    """One evidence path, or several: a list, or a comma-separated string.

    THE COLD READER IS A STOCHASTIC INSTRUMENT AND ONE SAMPLE IS NOT A
    MEASUREMENT (run 16, kimiwork, 2026-09-06).  Measured on BYTE-IDENTICAL
    crops - same sha256, four independent dispatches - the presentation screen
    came back sure / unsure / unsure / sure and the receipt came back
    'document with download arrow' unsure on the very crop the artwork seal
    had just read 'receipt', sure.  Gating a binary on ONE draw of that
    instrument does both halves of the damage: it blocks good drawings at
    random in every later lane, and it seals a bad one on a lucky draw -
    kimiwork's app window sealed 1/1 `sure` and then read 'Refrigerator'
    twice, from two independent readers, on one identical crop."""
    xs=evidence if isinstance(evidence,(list,tuple)) else str(evidence).split(',')
    paths=[Path(str(x).strip()) for x in xs if str(x).strip()]
    if not paths:raise ValueError('No independent reader evidence')
    return paths


ANSWER_WORDS=5           # the law's cap on a cold reader's answer


def _clean_answer(read):
    """Did this read honour the five-word contract the prompt states?

    The cap is the READER's half of the contract and the author cannot make it
    comply.  A longer answer is still a read of the noun - `none - task manager
    UI panel` names the panel - but it is not a clean identification, so it can
    never be the `sure` read that carries an object (see `consensus`)."""
    name=str(read.get('name','')).strip()
    return bool(name) and len(name.split())<=ANSWER_WORDS


def consensus(row,reads):
    """Rule on ONE object over every independent read of it.

    The confidence flag is a sample; the NOUN is the measurement.  Whether a
    read names the intended object stays the author's judgement and always did
    ('browser window with app icon' IS an app window) - it is declared per read
    in the scoring row as `match`: 'intended' | 'synonym' | 'different'.  What
    the code owns is the arithmetic over those judgements:

      * a SECOND reader naming a different object fails the object however many
        rounds are run.  Two independent readers said 'Refrigerator' about
        kimiwork's app window on one identical crop: that is the drawing.
      * ONE different name in four or more reads is instrument noise, recorded
        and not fatal - kimiwork's receipt, 1 of 5.
      * at least half the reads must NAME it - `intended` or `synonym`.  This
        replaces "at least half the reads must be `sure`" (run 17, pcoverheat,
        2026-09-08).  The old line gated the binary on the flag this docstring
        has always called a sample, and it cost a lane: the download arrow at
        `shorts_run17/review/phone_pcoverheat_cutout/01.png` - an arrow onto a
        bar - was named `download arrow` / `download arrow icon` /
        `download icon (arrow over line)` by SIX of six independent readers,
        zero different, and was refused as "needs revision" on `sure` 2 of 6.
        The SAME drawing had sealed at the artwork seat hours earlier on `sure`
        3 of 6 (`review/artwork_scores_pcoverheat.json`): nothing about the ink
        changed between the two seats, only which way the coin landed four
        times.  And the rule's own cited case does not need it - kimiwork's app
        window was `Refrigerator` TWICE, so `diff` 2 > MISREAD_MAX already
        fails it above, with or without the confidence count.
      * ...but at least ONE reader must have been `sure` of a name it actually
        reached, in five words or fewer.  Unanimity among readers who were all
        guessing is not a measurement, so kimiwork's five-of-five hedged
        presentation screen still fails.  A `sure` on a DIFFERENT noun buys
        nothing: a confidently wrong reader is not evidence of legibility.

    A scoring row with no per-read judgement is a single-sample score and keeps
    the old rule exactly: every read must be `sure`."""
    n=len(reads);sure=sum(1 for r in reads if r.get('confidence')=='sure')
    judged=row.get('reads') or []
    if not judged:
        if any(r.get('confidence')!='sure' for r in reads):
            raise ValueError('Only clear independent identifications pass; uncertain objects need revision')
        return {'i':row.get('i'),'reads':n,'sure':sure,'different':0,'single_sample':n==1}
    if len(judged)!=n:
        raise ValueError(f'Object {row.get("i")}: {len(judged)} judged reads for {n} dispatched; every read is scored or none is')
    if any(j.get('match') not in ('intended','synonym','different') for j in judged):
        raise ValueError(f'Object {row.get("i")}: every judged read declares match intended|synonym|different')
    diff=sum(1 for j in judged if j.get('match')=='different')
    if diff>MISREAD_MAX or diff>MISREAD_FRACTION*n:
        raise ValueError(f'Object {row.get("i")}: {diff} of {n} independent readers named a DIFFERENT object; '
                         'that is the drawing, not the instrument - redraw it, do not re-read it')
    agreed=n-diff
    if agreed*2<n:
        raise ValueError(f'Object {row.get("i")}: only {agreed} of {n} independent readers NAMED it; '
                         'fewer than half the readers reaching the intended object is the drawing, not the instrument')
    sure_agreed=sum(1 for j in judged if j.get('match') in ('intended','synonym')
                    and j.get('confidence')=='sure' and _clean_answer(j))
    if sure_agreed<1:
        raise ValueError(f'Object {row.get("i")}: not one of {n} independent readers were sure of a name that reached it; '
                         'a drawing no reader can name confidently even once needs revision')
    return {'i':row.get('i'),'reads':n,'sure':sure,'agreed':agreed,'sure_agreed':sure_agreed,
            'different':diff,'single_sample':False}


def read_rows(evidence,scoring):
    """The independent-reader contract, shared by the lane gate and the artwork gate.

    Run 16 (plantsite, 2026-09-06): the artwork author returned verdict PASS
    with cold_reads_run 0 and blocking_before_render true, and nothing checked
    it.  Reader evidence is now validated in ONE place and a dispatch failure -
    a reader that never saw the image - is refused instead of scored.

    Run 16 (kimiwork, 2026-09-06): evidence may now be SEVERAL independent
    rounds, and the verdict is their consensus rather than one draw of a noisy
    instrument.  See `evidence_rounds` and `consensus`."""
    scores=json.loads(Path(scoring).read_text())
    rows=scores.get('objects',scores.get('rows',[]))
    names=[]
    for path in evidence_rounds(evidence):
        answers=json.loads(path.read_text())
        if answers.get('dispatch_failures'):raise ValueError('A reader that never saw the image is not a read; re-dispatch those crops')
        got=answers.get('names',[])
        if not rows or len(rows)!=len(got) or {x.get('i') for x in rows}!={x.get('i') for x in got} or len({x.get('i') for x in got})!=len(got):raise ValueError('Every bespoke object requires a reader answer and a score')
        names+=got
    if any(x.get('verdict')!='PASS' for x in rows):raise ValueError('A failed object cannot be rendered')
    if any(not str(x.get('name','')).strip() for x in names):
        raise ValueError('Only clear independent identifications pass; an answer that names nothing is not a read')
    # A reader that overran the five-word cap used to refuse the WHOLE round
    # (run 17, pcoverheat, 2026-09-08): three long answers about object 3 -
    # `none - UI table, not object` and friends, the reader declining the
    # prompt's "everyday OBJECT" premise about a UI panel - would have thrown
    # away the six clean reads of objects 0, 1 and 2 in the same file.  The
    # violation is now recorded on the read and priced by `consensus`, where it
    # costs that read its `sure` credit and nothing else.
    for x in names:
        if not _clean_answer(x):x['over_five_words']=True
    for row in rows:consensus(row,[n for n in names if n.get('i')==row.get('i')])
    return rows,names


def save_phone(run,vid,fmt,project,evidence,scoring):
    # `--evidence` may be SEVERAL independent rounds, comma separated (run 16,
    # kimiwork, 2026-09-06).  `read_rows` was taught that and this hash record
    # was not, so a multi-round lane approval died on
    # `FileNotFoundError: 'a.json,b.json,c.json'` - every round is hashed.
    evidence_paths=[*evidence_rounds(evidence),Path(scoring)]
    if (Path(run)/'production-policy.json').exists():
        geometry=Path(project)/'geometry_audit/report.json'
        report=json.loads(geometry.read_text())
        if report.get('strict') is not True or report.get('errors')!=0 or report.get('project')!=Path(project).name:
            raise ValueError('Production requires a clean strict geometry report')
        evidence_paths.append(geometry)
    read_rows(evidence,scoring)
    rec={'verdict':'PASS','project_sha256':project_hash(project),
         'evidence':{str(Path(p).resolve()):digest(p) for p in evidence_paths}}
    atomic_json(Path(run)/'review'/f'phone_pass_{vid}_{fmt}.json',rec);return rec


def scene_lock(run,vid,holder,release=False):
    """THE REPAIR-ROUND OWNER OF A SHARED SCENE MODULE, as an actual file.

    STANDARD.md has said since 2026-09-06 that on a repair round the lane which
    takes `<run>/gen/.<vid>_scene.lock` atomically owns the shared module, and
    that *"not mine to change" is not a terminal reason on a repair round*.
    The lock had no implementation anywhere in this pipeline - it existed only
    as prose - so run 16's kimiwork split and cutout authors each found the one
    shared object their readers refused, each correctly read CLAIMS.md ("does
    NOT touch the shared scene"), and each returned exactly that terminal
    sentence.  Two lanes, one deadlock, and a gate that could only report "no
    staged path".  A rule that names an instrument has to ship the instrument."""
    d=Path(run)/'gen';d.mkdir(parents=True,exist_ok=True);lock=d/f'.{vid}_scene.lock'
    if release:
        if lock.exists() and json.loads(lock.read_text()).get('holder')!=holder:raise ValueError('That lock is held by another lane')
        lock.unlink(missing_ok=True);return {'lock':str(lock),'held_by':None}
    try:
        fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError:
        rec=json.loads(lock.read_text())
        if rec.get('holder')==holder:return {**rec,'lock':str(lock),'reentrant':True}
        raise ValueError(f'The shared scene is being repaired by {rec.get("holder")}; poll this lock and rebuild from the republished module, never fork your own copy')
    rec={'holder':holder,'vid':vid,'at':__import__('datetime').datetime.now().isoformat(timespec='seconds')}
    with os.fdopen(fd,'w') as fh:json.dump(rec,fh)
    return {**rec,'lock':str(lock),'owns':'gen/%s_scene.py + plans/%s_scene_handoff.md for this round'%(vid,vid)}


def save_artwork(run,vid,module,handoff,evidence,scoring):
    """Bind a SHARED scene module to the cold reads of its own bespoke objects.

    An unproven shared drawing is the one defect three format lanes cannot
    repair: the module belongs to the artwork stage, so a lane that finds its
    peak object unreadable has nothing it is allowed to change.  Run 16's
    plantsite lost split, whiteboard and cutout to exactly that.

    SEAL_ROUNDS (kimiwork, 2026-09-06): and it must be sealed on MORE THAN ONE
    sample.  kimiwork's app window was sealed on a single `sure` read, and the
    two lanes that then built on it drew 'Refrigerator' twice out of the next
    four reads of the same pixels.  A one-sample seal does not survive being
    re-sampled by the lanes, and by then the only agent allowed to redraw it
    has gone home.  Three independent dispatches at the seal cost minutes; a
    seal that fails downstream costs the recording."""
    # the objects first: "a reader refused object 1" is the more useful refusal
    # than "you owe me two more rounds of the same".
    rows,names=read_rows(evidence,scoring)
    rounds=evidence_rounds(evidence)
    if len({str(x.resolve()) for x in rounds})<SEAL_ROUNDS:
        raise ValueError(f'A shared scene seals on {SEAL_ROUNDS} independent cold-read rounds, not one: the reader is a '
                         'stochastic instrument and a single sample seals a marginal object on a lucky draw '
                         '(pipeline/cold_read.py dispatch ... --tag round1|round2|round3)')
    paths=[module,handoff,*rounds,scoring]
    for p in paths:
        if not Path(p).exists():raise ValueError(f'Artwork approval needs {p}')
    rec={'verdict':'PASS','vid':vid,'objects':len(rows),'seal_rounds':len(rounds),
         'module':str(Path(module).resolve()),'handoff':str(Path(handoff).resolve()),
         'evidence':{str(Path(p).resolve()):digest(p) for p in paths}}
    atomic_json(Path(run)/'review'/f'artwork_pass_{vid}.json',rec);return rec


def check_artwork(run,vid,module,handoff):
    p=Path(run)/'review'/f'artwork_pass_{vid}.json'
    if not p.exists():raise ValueError('No shared-artwork approval: every bespoke object in the scene module needs an independent cold read before any lane consumes it (pipeline/cold_read.py)')
    rec=json.loads(p.read_text())
    if rec.get('verdict')!='PASS':raise ValueError('Shared-artwork approval is not a PASS')
    if module and rec.get('module')!=str(Path(module).resolve()):raise ValueError('Shared-artwork approval names another scene module')
    if handoff and rec.get('handoff')!=str(Path(handoff).resolve()):raise ValueError('Shared-artwork approval names another handoff')
    for f,h in rec.get('evidence',{}).items():
        if not Path(f).exists() or digest(f)!=h:
            # A REFUSAL THAT NAMES THE OWNER, not a dead end.  The lane holding
            # the scene lock is repairing this module on purpose and has to
            # re-seal it; a lane that holds no lock is looking at somebody
            # else's half-finished repair and must wait for the republish.
            lock=Path(run)/'gen'/f'.{vid}_scene.lock'
            who=json.loads(lock.read_text()).get('holder') if lock.exists() else None
            raise ValueError(f'Shared-artwork evidence changed: {f}. '
                             +(f'{who} holds the scene lock and is repairing it: rebuild from the republished module once it re-seals.'
                               if who else
                               'If a reader refused one of its objects, this is a repair round and the module HAS an owner: take '
                               f'`production.py scene-lock --run {run} --vid {vid} --holder <your lane>`, redraw that object, '
                               f're-read it cold over {SEAL_ROUNDS} rounds and re-run artwork-pass. "Not mine to change" is not a '
                               'terminal reason on a repair round.'))
    return rec


def deliver_approved(run,vid,day,verdict):
    # day/run remain internal provenance, not the user-facing delivery hierarchy.
    from deliver.short_package import deliver
    return deliver(run, vid, verdict)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['context','plan-report','phone-pass','phone-check','artwork-pass','artwork-check','scene-lock','deliver'])
    p.add_argument('--run',type=Path,required=True);p.add_argument('--vid',required=True)
    for x in ['fmt','project','evidence','scoring','day','verdict','module','handoff','holder']:p.add_argument('--'+x)
    p.add_argument('--release',action='store_true',help='scene-lock: hand the shared module back')
    a=p.parse_args()
    if a.action=='context':r=prepare_context(a.run,a.vid)
    elif a.action=='plan-report':r=plan_report(a.run,a.vid)
    elif a.action=='phone-pass':r=save_phone(a.run,a.vid,a.fmt,a.project,a.evidence,a.scoring)
    elif a.action=='phone-check':r=check_phone(a.run,a.vid,a.fmt,a.project)
    elif a.action=='artwork-pass':r=save_artwork(a.run,a.vid,a.module,a.handoff,a.evidence,a.scoring)
    elif a.action=='artwork-check':r=check_artwork(a.run,a.vid,a.module,a.handoff)
    elif a.action=='scene-lock':r=scene_lock(a.run,a.vid,a.holder,release=a.release)
    else:r=deliver_approved(a.run,a.vid,a.day,a.verdict)
    print(json.dumps(r,indent=2))


if __name__=='__main__':main()
