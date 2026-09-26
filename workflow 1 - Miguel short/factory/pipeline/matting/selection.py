"""A reviewed selection belongs to one exact source and prepared plate."""
from pathlib import Path
import argparse, hashlib, json, os
import cv2
import numpy as np
from PIL import Image, ImageDraw
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from fsutil import digest, atomic_json  # shared (2026-09-20)


def identity(plate, source, crop):
    cap = cv2.VideoCapture(str(plate)); ok, frame = cap.read()
    if not ok: raise ValueError('Cannot decode first frame')
    result = dict(plate_sha256=digest(plate), source_sha256=digest(source),
                  crop_sha256=digest(crop), first_frame_sha256=hashlib.sha256(frame.tobytes()).hexdigest(),
                  width=frame.shape[1], height=frame.shape[0],
                  fps=cap.get(cv2.CAP_PROP_FPS), frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    cap.release(); return result


def validate(path, plate, source, crop):
    p = Path(path); d = json.loads(p.read_text())
    if d.get('status') != 'reviewed' or d.get('identity') != identity(plate, source, crop):
        raise ValueError('Selection is unreviewed or belongs to a different recording/crop')
    mask = Path(d['mask']); a = np.asarray(Image.open(mask).convert('L'))
    if digest(mask) != d['mask_sha256'] or a.shape != (d['identity']['height'], d['identity']['width']):
        raise ValueError('Reviewed mask changed or has the wrong dimensions')
    if not .02 < np.mean(a > 127) < .98: raise ValueError('Implausible person mask')
    return d


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['prepare', 'approve', 'validate'])
    for name in ['plate', 'source', 'crop', 'selection']: p.add_argument('--'+name, type=Path, required=True)
    p.add_argument('--mask', type=Path); p.add_argument('--edits', type=Path)
    p.add_argument('--reviewer'); p.add_argument('--notes', default='')
    a = p.parse_args()
    if a.action == 'validate': print(json.dumps(validate(a.selection, a.plate, a.source, a.crop))); return
    ident = identity(a.plate, a.source, a.crop)
    if a.action == 'prepare':
        cap = cv2.VideoCapture(str(a.plate)); _, frame = cap.read(); cap.release()
        a.selection.parent.mkdir(parents=True, exist_ok=True)
        image = a.selection.with_suffix('.frame.png'); cv2.imwrite(str(image), frame)
        print(json.dumps({'identity':ident, 'frame':str(image), 'selection':str(a.selection), 'status':'needs_visual_review'})); return
    if not a.mask or not a.reviewer or not a.notes: p.error('approve requires --mask, --reviewer and visual --notes')
    img = Image.open(a.mask).convert('L')
    if img.size != (ident['width'], ident['height']): raise ValueError('Mask and plate dimensions differ')
    edits = json.loads(a.edits.read_text()) if a.edits else []
    # Coordinates are recorded explicitly; nothing is transferred to another recording.
    draw = ImageDraw.Draw(img)
    for edit in edits:
        if edit['operation'] not in ('include', 'exclude') or len(edit['points']) < 3:
            raise ValueError('Edits require include/exclude polygons')
        if any(not (0 <= x < img.width and 0 <= y < img.height) for x,y in edit['points']):
            raise ValueError('Selection point outside frame')
        draw.polygon([tuple(x) for x in edit['points']], fill=255 if edit['operation']=='include' else 0)
    target = a.selection.with_suffix('.mask.png'); img.save(target)
    atomic_json(a.selection, {'version':1, 'status':'reviewed', 'identity':ident,
        'mask':str(target.resolve()), 'mask_sha256':digest(target), 'base_mask_sha256':digest(a.mask),
        'edits':edits, 'reviewer':a.reviewer, 'notes':a.notes,
        'crop':json.loads(a.crop.read_text()), 'reuse_scope':'this exact source, plate and crop only'})
    print(json.dumps(validate(a.selection,a.plate,a.source,a.crop)))


if __name__ == '__main__': main()
