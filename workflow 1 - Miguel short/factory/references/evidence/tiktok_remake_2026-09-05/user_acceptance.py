"""Scoped user acceptance of existing hand findings, separate from reviewer verdicts.

No render, deployment, budget, technical QC, or final-export approval is performed.
"""
from pathlib import Path
import hashlib
import json
import time

RUN = Path(__file__).resolve().parent
ACCEPTED_IDS = ('astramath', 'costpertask', 'game33c', 'impossibletask', 'perplexityprojects', 'trycrm')
FRAMES = {'astramath':[154,155,156], 'costpertask':[520,521,522],
          'game33c':[139,140,141], 'impossibletask':[73],
          'perplexityprojects':[405], 'trycrm':[5]}
AUTHORITY = ('User explicitly overrides the existing zoom-only hand flags as false positives '
             'and requests completion of missing TikTok renders. Relayed by root on 2026-09-06.')

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _identity(vid, run):
    d = run/'matting'/vid
    ready = json.loads((d/'ready.json').read_text())
    current = json.loads((d/'matting.json').read_text())
    paths = {'source_master':Path(ready['master']), 'source_plate':Path(ready['plate']),
             'raw_alpha':d/'alpha_v1.mkv'}
    for kind in ('cut','rim','alpha'):
        p = Path(current['outputs'][kind])
        assert digest(p) == current['ship']['hashes'][kind], f'{vid}: stale shipped {kind}'
        paths['shipped_'+kind] = p
    assert digest(paths['source_master']) == ready['source_sha256']
    assert digest(paths['source_plate']) == ready['plate_sha256']
    assert current['headroom']['pass'] is True
    assert current['headroom']['identity']['alpha_sha256'] == digest(paths['raw_alpha'])
    return {key:{'path':str(p),'sha256':digest(p)} for key,p in paths.items()}

def create(vid, run=RUN):
    run = Path(run)
    assert vid in ACCEPTED_IDS
    target = run/'review'/vid/'user-acceptance.json'
    if target.exists():
        return validate_matte_acceptance(vid, run)
    identity = _identity(vid, run)
    evidence = []
    for name in ('independent-matte-review.json','agent-review.json'):
        p = target.parent/name
        if p.exists():
            report = json.loads(p.read_text())
            assert report['alpha_sha256'] == identity['raw_alpha']['sha256'], f'{vid}: stale review'
            assert not report.get('face_missing_observed') and not report.get('chair_retained_observed')
            evidence.append({'path':str(p),'sha256':digest(p),'snapshot':report})
    assert evidence, 'Existing review required'
    record = {'version':1,'id':vid,'decision':'USER_ACCEPTED_HAND_FINDINGS',
        'authority':AUTHORITY,'recorded_by':'prepare_crops','created_epoch':time.time(),
        'accepted_scope':'Only existing localized hand/fingertip matte findings in preserved reviews.',
        'accepted_source_frames':FRAMES[vid], 'identity':identity,'preserved_reviews':evidence,
        'independent_verdicts_unchanged':True,'technical_checks_waived':False,
        'final_export_review_waived':False,'new_findings_accepted':False}
    with target.open('x') as f: json.dump(record,f,indent=2); f.write('\n')
    return validate_matte_acceptance(vid,run)

def validate_matte_acceptance(vid, run=RUN):
    """Authorize only the existing matte hand hold; caller retains all other gates."""
    run = Path(run)
    assert vid in ACCEPTED_IDS
    p = run/'review'/vid/'user-acceptance.json'
    record = json.loads(p.read_text())
    assert record['version'] == 1 and record['id'] == vid
    assert record['decision'] == 'USER_ACCEPTED_HAND_FINDINGS'
    assert record['authority'] == AUTHORITY
    assert record['accepted_source_frames'] == FRAMES[vid]
    assert record['technical_checks_waived'] is False
    assert record['final_export_review_waived'] is False
    assert record['new_findings_accepted'] is False
    assert record['identity'] == _identity(vid,run), 'Acceptance does not match current source/matte/layers'
    for evidence in record['preserved_reviews']:
        assert digest(evidence['path']) == evidence['sha256'], 'Review changed since user acceptance; reconcile scope explicitly'
        assert json.loads(Path(evidence['path']).read_text()) == evidence['snapshot']
    return record

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('ids',nargs='+',choices=ACCEPTED_IDS)
    parser.add_argument('--record-authorized-user-acceptance',action='store_true')
    args = parser.parse_args()
    for vid in args.ids:
        record = create(vid) if args.record_authorized_user_acceptance else validate_matte_acceptance(vid)
        print(json.dumps({'id':vid,'decision':record['decision'],'alpha_sha256':record['identity']['raw_alpha']['sha256']}))
