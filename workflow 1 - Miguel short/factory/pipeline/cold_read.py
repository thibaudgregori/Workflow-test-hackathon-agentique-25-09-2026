"""The COLD READER dispatcher.  No paid API: one independent `claude -p`
process per crop, on session capacity.

WHY THIS FILE EXISTS (run 16, plantsite, 2026-09-06)
----------------------------------------------------
Every author brief says "use the native Agent tool for a FRESH independent cold
reader".  Two of run 16's subagents - the plantsite ARTWORK author and the
plantsite WHITEBOARD author - had no agent-spawn verb in their toolset at all.
The artwork author shipped its shared scene module with `cold_reads_run: 0,
blocking_before_render: true` and still returned verdict PASS; the whiteboard
author cut its three crops, wrote a dispatch brief for somebody else and
returned with nothing staged.  The split and cutout authors, in the same run and
with the same missing verb, improvised: they launched one `claude -p` per crop
from /tmp and got real reads back.

That improvisation is the mechanism.  It belongs in the pipeline, not in one
author's head, so "I have no agent-spawn verb" can never again stall a lane or
launder an unproven drawing into a PASS.

TWO RULES THIS FILE ENCODES, BOTH PAID FOR IN RUN 16
----------------------------------------------------
1. ABSOLUTE PATHS.  The split author's first dispatch handed the readers paths
   relative to /tmp and two of them answered "file not found".  A harness
   failure is NOT a read: those rows are refused here, never scored.
2. BLIND COPIES.  The reader is handed a copy under a random token, named by
   the object's index alone.  No video id, no format, no plan, no topic, no
   sealed key, and no path that carries the recording's name.

Evidence shape is exactly what `production.py phone-pass` consumes:
    {"names": [{"i": 0, "path": "...", "name": "...", "confidence": "sure"}]}
plus per-row provenance this module adds (crop_sha256, reader, dispatched_at).

    python pipeline/cold_read.py dispatch --crop A.png --crop B.png \
        --out review/phone_reader_<vid>_<fmt>.json --tag round1 \
        --cold-root <run>/review/cold
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse, datetime, json, os, re, secrets, shutil, subprocess, sys

F = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(F / 'pipeline/matting'))
from selection import atomic_json, digest  # noqa: E402

CONFIDENCES = ('sure', 'unsure', 'cannot tell')

# The prompt is the law's wording and nothing else.  It never names the video,
# the topic, the format or the intended object.
PROMPT = ('Look at the image at {path} . Name the single everyday object drawn '
          'in it. At most FIVE words. Reply with ONE line of JSON and nothing '
          'else: {{"name":"<=5 words","confidence":"sure|unsure|cannot tell"}}')

# THE QUESTION MUST FIT THE OBJECT (Miguel, 2026-09-08).  Asking "name the
# everyday object" about a depiction of software gets the honest and useless
# answer "no object; text label image" - the reader is right and the drawing is
# not on trial.  A `ui` crop is asked what software it looks like instead;
# `furniture` (connectors, bars, arrows, brackets) has a role, not a name, and
# is never dispatched at all.
PROMPT_UI = ('Look at the image at {path} . It shows a piece of software on a screen. '
             'In at most FIVE words, what kind of software or panel is it? Reply with ONE '
             'line of JSON and nothing else: '
             '{{"name":"<=5 words","confidence":"sure|unsure|cannot tell"}}')
PROMPTS = {'metaphor': PROMPT, 'ui': PROMPT_UI}

# Anything that means the reader never saw the picture.  These are dispatch
# failures, not reads, and they are refused rather than scored (rule 1).
NOT_A_READ = re.compile(r'file not found|no such file|does not exist|cannot read|permission|enoent',
                        re.I)


def _blind_dir(cold_root: Path, tag: str | None) -> Path:
    token = secrets.token_hex(4)
    name = f'{tag}-{token}' if tag else token
    d = cold_root / name
    d.mkdir(parents=True, exist_ok=False)
    return d


def _one(idx: int, path: Path, model: str | None, timeout: int) -> dict:
    """One independent reader process.  cwd is neutral; the path is absolute."""
    # The prompt goes in on STDIN, never as a trailing argv word: `--allowedTools`
    # is variadic, so `claude -p --allowedTools Read "<prompt>"` swallows the
    # prompt into the tool list and the CLI exits 1 with "Input must be provided
    # either through stdin or as a prompt argument" (measured, run 16).
    cmd = ['claude', '-p', '--allowedTools', 'Read']
    if model:
        cmd += ['--model', model]
    row = {'i': idx, 'path': str(path), 'name': '', 'confidence': 'cannot tell',
           'crop_sha256': digest(path)}
    try:
        r = subprocess.run(cmd, cwd='/tmp', input=PROMPT.format(path=str(path)),
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        row['dispatch_error'] = f'the reader did not answer within {timeout}s'
        return row
    out = (r.stdout or '').strip()
    if r.returncode != 0:
        row['dispatch_error'] = f'claude -p exited {r.returncode}: {(r.stderr or out)[:200]}'
        return row
    if NOT_A_READ.search(out):
        row['dispatch_error'] = f'the reader never saw the image: {out[:200]}'
        return row
    m = re.search(r'\{.*\}', out, re.S)
    if not m:
        row['dispatch_error'] = f'unparseable reader reply: {out[:200]}'
        return row
    try:
        ans = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        row['dispatch_error'] = f'unparseable reader reply ({e}): {out[:200]}'
        return row
    name = str(ans.get('name', '')).strip()
    conf = str(ans.get('confidence', '')).strip().lower()
    if conf not in CONFIDENCES:
        conf = 'cannot tell'
    # A read is a read even when it is wrong; only the >5-word cap is the
    # author's own contract with the law, and it is reported, never trimmed.
    row['name'] = name
    row['confidence'] = conf
    if name and len(name.split()) > 5:
        row['over_five_words'] = True
    return row


def _ledger_path(cold_root):
    return Path(cold_root) / '_read_crops.json'


def refuse_unchanged(crops, cold_root):
    """A crop that already has a verdict this run is never re-read.

    Run 18 (2026-09-08): `saascut` dispatched three rounds on byte-identical
    crops and collected three identical verdicts; `hermesdoctor` ran four full
    five-object rounds on one unchanged set.  Six rounds, zero design changes.
    Identical crop + independent reader is not a second measurement, it is a
    copy, so the dispatcher refuses it rather than the brief asking politely.
    Seal what reads, redraw what misses, and send only the NEW bytes.
    """
    led = _ledger_path(cold_root)
    seen = json.loads(led.read_text()) if led.exists() else {}
    repeats = [c for c in crops if seen.get(digest(c))]
    if repeats:
        raise SystemExit('These crops already have a verdict this run and will not be re-read: '
                         + ', '.join(str(c) for c in repeats)
                         + '\nRedraw the object and dispatch the new crop, or seal it on the reads it already has.')
    return seen, led


def dispatch(crops, out, tag=None, cold_root=None, model=None, timeout=240, workers=4):
    crops = [Path(c).resolve() for c in crops]
    for c in crops:
        if not c.exists():
            raise ValueError(f'crop does not exist: {c}')
    out = Path(out).resolve()
    cold_root = Path(cold_root).resolve() if cold_root else out.parent / 'cold'
    blind = _blind_dir(cold_root, tag)
    blind_paths = []
    for i, c in enumerate(crops):
        b = blind / f'{i:02d}{c.suffix.lower() or ".png"}'
        shutil.copyfile(c, b)
        blind_paths.append(b)

    with ThreadPoolExecutor(max_workers=max(1, min(workers, len(blind_paths)))) as ex:
        rows = list(ex.map(lambda a: _one(a[0], a[1], model, timeout),
                           list(enumerate(blind_paths))))
    rows.sort(key=lambda r: r['i'])

    failed = [r for r in rows if r.get('dispatch_error')]
    rec = {
        'tag': tag or '',
        'cold_dir': str(blind),
        'reader': ('one independent `claude -p` process per crop, launched from /tmp, handed ONLY '
                   'the absolute path of a blind copy under a random token - no plan, no topic, no '
                   'manifest, no sealed key, and no path naming the video'),
        'prompt': PROMPT.format(path='<absolute path of one blind crop>'),
        'dispatched_at': datetime.datetime.now().isoformat(timespec='seconds'),
        'cli': subprocess.run(['claude', '--version'], capture_output=True, text=True).stdout.strip(),
        'source_crops': {str(c): digest(c) for c in crops},
        'names': [{k: v for k, v in r.items() if k != 'dispatch_error'} for r in rows],
    }
    if failed:
        # A harness failure is not a read (rule 1).  It is recorded, it is
        # visible, and it exits non-zero so nobody scores it by accident.
        rec['dispatch_failures'] = [{'i': r['i'], 'error': r['dispatch_error']} for r in failed]
    atomic_json(out, rec)
    return rec


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('action', choices=['dispatch'])
    p.add_argument('--crop', action='append', required=True,
                   help='one crop per flag, in object-index order')
    p.add_argument('--out', required=True, help='evidence json to write')
    p.add_argument('--tag', default=None, help='round1 / round2 / cand - names the blind folder')
    p.add_argument('--cold-root', default=None, help='where blind folders live (default <out>/../cold)')
    p.add_argument('--model', default=None, help='leave unset to inherit the configured reader model')
    p.add_argument('--timeout', type=int, default=240)
    p.add_argument('--workers', type=int, default=4)
    p.add_argument('--rounds', type=int, default=1,
                   help='independent rounds to dispatch CONCURRENTLY (2026-09-14). The seal '
                        'contract wants SEAL_ROUNDS independent samples of one crop set; they '
                        'are independent by design, so running them one after another only '
                        'multiplied the wall clock (run 19: 15-17 min per artwork seal). With '
                        '--rounds N the evidence files are <out stem>_r1..N.json and the blind '
                        'folders <tag>_r1..N; pass them to production.py comma-separated.')
    a = p.parse_args()
    if a.rounds <= 1:
        rec = dispatch(a.crop, a.out, tag=a.tag, cold_root=a.cold_root, model=a.model,
                       timeout=a.timeout, workers=a.workers)
        print(json.dumps(rec, indent=2))
        sys.exit(1 if rec.get('dispatch_failures') else 0)
    out = Path(a.out)
    stem, suffix = out.with_suffix(''), out.suffix or '.json'
    tag = a.tag or 'round'
    jobs = [(f'{stem}_r{i}{suffix}', f'{tag}_r{i}') for i in range(1, a.rounds + 1)]
    with ThreadPoolExecutor(max_workers=a.rounds) as ex:
        recs = list(ex.map(lambda j: dispatch(a.crop, j[0], tag=j[1], cold_root=a.cold_root,
                                              model=a.model, timeout=a.timeout, workers=a.workers), jobs))
    failures = sum(len(r.get('dispatch_failures') or []) for r in recs)
    summary = {'rounds': [j[0] for j in jobs], 'evidence_arg': ','.join(j[0] for j in jobs),
               'dispatch_failures': failures,
               'names_by_round': [[(n['i'], n.get('name'), n.get('confidence')) for n in r['names']] for r in recs]}
    print(json.dumps(summary, indent=2))
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
