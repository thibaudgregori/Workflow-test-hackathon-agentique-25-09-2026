"""Queue nominated failures for one cached repair; never stop other recordings."""
import fcntl
import hashlib
import json
from pathlib import Path
from auto_repair import run_manifest, digest, atomic, validate_entries

import os, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runs import newest_run  # noqa: E402
# THE RUN IS A PARAMETER (2026-09-20): this tool used to live inside the 2026-09-05 TikTok remake folder and
# treat its own folder as the run. SHORTS_RUN or the newest run on disk is the run now.
R = Path(os.environ["SHORTS_RUN"]).expanduser().resolve() if os.environ.get("SHORTS_RUN") else newest_run()


def route_cached_repair(vid, alpha, config):
    """Create/reuse an edit-plan request, without running or approving a repair."""
    if Path(vid).name != vid or vid in ('', '.', '..'):
        raise ValueError('Invalid recording ID')
    entries = [e for e in json.loads((R / config['nominations']).read_text()) if e['id'] == vid]
    if not entries:
        return {'state': 'not_nominated', 'visual_review_still_required': True}
    validate_entries(entries)
    first = entries[0]
    # Recheck both original artifacts, including the actual caller's alpha.
    if (digest(alpha) != first['before_alpha_sha256'] or
            digest(first['before_alpha']) != first['before_alpha_sha256'] or
            digest(first['source']) != first['source_sha256']):
        return {'id': vid, 'state': 'needs_fresh_review',
                'reason': 'Nomination belongs to different source or original alpha',
                'installed': False, 'continue_other_recordings': True}
    identity = {
        'source': str(Path(first['source']).resolve()),
        'source_sha256': first['source_sha256'],
        'before_alpha': str(Path(first['before_alpha']).resolve()),
        'before_alpha_sha256': first['before_alpha_sha256'],
        'nominations': sorted([{'frame': e['frame'], 'roi_xyxy': e['roi_xyxy']}
                               for e in entries], key=lambda e: e['frame']),
    }
    identity_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    folder = R / config['cached_donor_repair']['queue'] / vid
    folder.mkdir(parents=True, exist_ok=True)
    # One persistent recording slot prevents fresh paths from silently retrying.
    with (folder / 'queue.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        record = folder / 'queue.json'
        if record.exists():
            cached = json.loads(record.read_text())
            if cached.get('identity') != identity or cached.get('identity_sha256') != identity_hash:
                return {'id': vid, 'state': 'needs_fresh_review',
                        'reason': 'Existing repair request differs; inspect it before any new attempt',
                        'queue_record': str(record), 'installed': False,
                        'continue_other_recordings': True}
            # Engine/reviewer result files are intentionally not consumed here.
            return cached
        plan_directory = folder / 'plan'
        plan_directory.mkdir(exist_ok=True)
        result = {
            'id': vid, 'state': 'needs_agent_edit_plan', 'identity': identity,
            'identity_sha256': identity_hash, 'queue_record': str(record),
            'plan_directory': str(plan_directory), 'attempts_started': 0,
            'max_candidate_attempts': 1, 'existing_artifacts_only': True,
            'cloud_dispatch_allowed': False, 'new_cloud_cost_usd': 0,
            'independent_hash_bound_review_required': True,
            'auto_install': False, 'installed': False,
            'continue_other_recordings': True,
            'trigger': 'Existing reviewer frame/ROI nominations; not whole-video detection',
            'rejected_methods_must_not_retry': True,
            'required_plan_bindings': ['source', 'baseline_alpha', 'baseline_foreground',
                                       'donor_alpha', 'donor_foreground'],
            'plan_requirements': 'Bind each cached artifact by path and SHA256; specify explicit frames and polygons',
        }
        atomic(record, result)
        return result


def after_matting(vid, alpha, policy=None):
    policy = policy or json.loads((R / 'production-policy.json').read_text())
    config = policy.get('automated_outline_repair', {})
    if not config.get('enabled'):
        return {'state': 'disabled'}
    try:
        if config.get('cached_donor_repair', {}).get('enabled'):
            result = route_cached_repair(vid, alpha, config)
        else:
            manifest = R / config['nominations']
            entries = [e for e in json.loads(manifest.read_text()) if e['id'] == vid]
            if not entries:
                return {'state': 'not_nominated', 'visual_review_still_required': True}
            if any(e['before_alpha_sha256'] != digest(alpha) for e in entries):
                result = {'id': vid, 'state': 'needs_fresh_review',
                          'reason': 'Nomination belongs to a different original alpha', 'installed': False}
            elif config.get('candidate_method_status') != 'validated':
                result = {'id': vid, 'state': 'needs_manual_review',
                          'reason': 'Automatic methods failed validation; no repeated attempt',
                          'evidence': config['validation_report'], 'installed': False, 'new_cloud_cost_usd': 0}
            else:
                result = run_manifest(manifest, R / config['output'], [vid], expected_alpha=alpha)[0]
    except Exception as ex:
        result = {'id': vid, 'state': 'needs_manual_review', 'reason': str(ex),
                  'installed': False, 'continue_other_recordings': True}
    try:
        queue = R / 'review/automatic-repair-queue'
        queue.mkdir(parents=True, exist_ok=True)
        if Path(vid).name != vid or vid in ('', '.', '..'):
            raise ValueError('Invalid recording ID')
        atomic(queue / (vid + '.json'), result)
    except Exception as ex:
        result = {**result, 'queue_write_error': str(ex), 'continue_other_recordings': True}
    return result
