"""Title-first local delivery. No API calls, rendering or publishing.

The author supplies delivery/<id>.json with a stable short_id, approved title,
projects {youtube,tiktok,instagram: directory}, and source_files
{package-relative name: file or directory}. Paths are relative to the run.
Source files must include the generator, shared code and raw recording needed
for editing. Project symlinks are materialized, never archived as broken links.
"""
import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from fsutil import digest  # shared (2026-09-20)

PLATFORMS = {'youtube': ('youtube', 'split'), 'tiktok': ('tiktok', 'cutout'),
             'instagram': ('reels', 'whiteboard')}
LABELS = {'youtube': 'YouTube', 'tiktok': 'TikTok', 'instagram': 'Instagram'}
STATES = ('Ready to Publish', 'Partially Published', 'Published Shorts')  # the same three names locally and on Drive (2026-09-20)
SKIP = {'.git', '__pycache__', 'node_modules', '.DS_Store'}


def json_write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def safe_relative(value):
    p = Path(value)
    if p.is_absolute() or not p.parts or any(x in ('..', '.') for x in p.parts) or '\\' in value:
        raise ValueError('Unsafe package path: ' + value)
    return p


def title_name(title):
    if not isinstance(title, str) or not title.strip() or re.search(r'[/\\\x00-\x1f]', title):
        raise ValueError('An explicit, filesystem-safe short title is required')
    if title.strip() in ('.', '..') or title.strip().startswith('.'):
        raise ValueError('Invalid short title')
    return title.strip()


def enumerate_source(source, destination, ancestors=()):
    """Resolve symlink trees, failing on missing assets, cycles and secrets."""
    source = Path(source)
    real = source.resolve(strict=True)
    if real in ancestors:
        raise ValueError('Cyclic source link: ' + str(source))
    if source.name in SKIP:
        return []
    if source.name == 'secrets' or source.name.startswith('.env') or real.name.startswith('.env') or 'secrets' in real.parts:
        raise ValueError('Secret path cannot enter a video package')
    if real.is_file():
        return [(real, destination)]
    if not real.is_dir():
        raise ValueError('Not a regular source file: ' + str(source))
    rows = []
    for child in sorted(real.iterdir()):
        rows.extend(enumerate_source(child, destination / child.name, ancestors + (real,)))
    return rows


def prepare(run, vid, verdict):
    run = Path(run).resolve()
    rec = json.loads(Path(verdict).read_text())
    # A verdict is a word, not a sentence (2026-09-06): clerks write 'PASS (9/9 objects ...)'.
    def _pass(v): return isinstance(v, str) and re.match(r'^PASS\b', v.strip()) is not None
    if not _pass(rec.get('verdict')) or not _pass(rec.get('phone_verdict')) or rec.get('confirmed', 0) != 0:
        raise ValueError('Independent final review has not approved this Short')
    reviewed = {str(Path(p).resolve()): h for p, h in rec.get('reviewed_files', {}).items()}
    if len(reviewed) != 3:
        raise ValueError('Final review must record all three exact MP4 hashes')
    # Check media first, before reading packaging instructions or creating files.
    exports = {}
    for platform, (folder, fmt) in PLATFORMS.items():
        p = run / 'staging' / folder / f'{vid}_{fmt}.mp4'
        if reviewed.get(str(p)) != digest(p):
            raise ValueError('Reviewed MP4 differs from staged file: ' + str(p))
        exports[platform] = p
    spec = json.loads((run / 'delivery' / f'{vid}.json').read_text())
    title = title_name(spec.get('title'))
    sid = spec.get('short_id', '')
    if not re.fullmatch(r'[A-Za-z0-9_-]{8,100}', sid):
        raise ValueError('Use a persistent short_id, not a title or run number')
    if set(spec.get('projects', {})) != set(PLATFORMS):
        raise ValueError('All three editable platform projects are required')
    if not spec.get('source_files') or spec.get('dependencies_reviewed') is not True:
        raise ValueError('Explicit raw/source/generator dependencies must be reviewed before delivery')
    rows = [(p, Path('Exports') / (LABELS[k] + '.mp4')) for k, p in exports.items()]
    for platform, value in spec['projects'].items():
        project = (run / Path(value).expanduser()).resolve()
        if not (project / 'index.html').is_file():
            raise ValueError('Editable index.html missing: ' + str(project))
        rows.extend(enumerate_source(project, Path('Project') / LABELS[platform]))
    for name, value in spec['source_files'].items():
        rows.extend(enumerate_source(run / Path(value).expanduser(), Path('Source Assets') / safe_relative(name)))
    transcript = run / 'cuts' / vid / 'transcript_tight.json'
    if not transcript.is_file():
        raise ValueError('Tight transcript is required')
    rows.extend([(transcript, Path('Publishing/transcript_tight.json')),
                 (Path(verdict), Path('Publishing/final_review.json'))])
    names = [str(dest).casefold() for _, dest in rows]
    if len(names) != len(set(names)):
        raise ValueError('Package path collision')
    return spec, title, rows


def deliver(run, vid, verdict, root=None):
    spec, title, rows = prepare(run, vid, verdict)
    root = Path(root) if root else Path.home() / 'Movies/Shorts Factory'
    existing = []
    for state in STATES:
        for p in (root / state).glob('*/Publishing/package.json'):
            if json.loads(p.read_text()).get('short_id') == spec['short_id']:
                existing.append(p.parents[1])
    if len(existing) > 1:
        raise ValueError('Duplicate local short identity; reconcile before delivery')
    destination = existing[0] if existing else root / STATES[0] / title
    if destination.exists() and not existing:
        raise ValueError('Title already belongs to another package; do not merge')
    hashes = {str(dest): digest(src) for src, dest in rows}
    if existing:
        old = json.loads((destination / 'Publishing/package.json').read_text())
        if old['files'] != hashes or any(not (destination / rel).is_file() or digest(destination / rel) != h for rel, h in hashes.items()):
            raise ValueError('Existing package differs; preserve it and explicitly plan a revision')
        # A title change reuses the same identity, never creates a second package.
        renamed = destination.with_name(title)
        if renamed != destination:
            if renamed.exists():
                raise ValueError('Renamed title collides with another package')
            destination.rename(renamed)
            destination = renamed
            old['title'] = title
            json_write(destination / 'Publishing/package.json', old)
        return result(destination)
    root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.package-', dir=root))
    try:
        for src, rel in rows:
            out = staging / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, out)
            if digest(out) != hashes[str(rel)]:
                raise ValueError('Source changed during copying: ' + str(src))
        # Require all local HTML references to resolve inside the archived project.
        for html in (staging / 'Project').rglob('*.html'):
            for ref in re.findall(r'(?:src|href)\s*=\s*[\"\']([^\"\']+)', html.read_text()):
                if ref.startswith(('https:', 'http:', '//', '#', 'data:', 'mailto:')):
                    continue
                target = (html.parent / ref.split('?')[0].split('#')[0]).resolve()
                if not target.is_relative_to(staging.resolve()) or not target.exists():
                    raise ValueError('Non-portable or missing project reference: ' + ref)
        json_write(staging / 'Publishing/status.json', {
            'short_id': spec['short_id'], 'platforms': {p: {
                'status': 'ready', 'url': None, 'uploaded_at': None, 'visibility': None
            } for p in PLATFORMS}})
        json_write(staging / 'Publishing/package.json', {
            'schema_version': 1, 'short_id': spec['short_id'], 'title': title,
            'internal_source': {'run': str(Path(run).resolve()), 'recording_id': vid},
            'files': hashes, 'dependency_review': spec.get('dependency_review', ''),
            'verification': 'Copied files hash-verified; no rebuild or upload performed'})
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging.rename(destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)  # Only this invocation's disposable staging tree.
    return result(destination)


def result(destination):
    return {'package_dir': str(destination), 'approved_files': [
        str(destination / 'Exports' / (LABELS[p] + '.mp4')) for p in PLATFORMS]}
