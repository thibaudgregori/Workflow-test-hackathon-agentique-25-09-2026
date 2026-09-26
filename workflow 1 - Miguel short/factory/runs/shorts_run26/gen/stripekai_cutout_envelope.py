"""Measure the shipped stripekai alpha in display coordinates for the cutout.

Every frame of `matte_stripekai_v5_alpha.webm` (1386x990, the plate box's
ENCODED size) is swept: the crown (highest occupied row on any frame) seats the
caption pill with the pill that RENDERS (CAP.CAP_PILL_HEIGHT), never the frozen
108.2, and `cutout_depthfield.measure_band_frames` writes the per-frame band
extents the depth-field seat is solved on.  The plate box origin is READ from
plate.json (over-wide, extended 148.5 canvas px on the left and 49.5 on the
right, left -202: NOT centred), never computed.

It also records where his face sits (head-band column centre, every 10th
frame) so the build report can show the face is on the frame axis.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

F = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(F / 'formats/cutout/lib'))
sys.path.insert(0, str(F / 'pipeline'))
import cutout_depthfield as DF  # noqa: E402
import captions as CAP  # noqa: E402

VID = 'stripekai'
S = RUN / f'matting/{VID}'
ALPHA = S / f'matte_{VID}_v5_alpha.webm'
EXPECT_FRAMES = 895
CLEAR = 26.5
FACE_BAND = 160


def main():
    box = json.loads((S / 'plate.json').read_text())['overwide']['plate_box']
    probe = json.loads(subprocess.check_output(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
         'stream=width,height', '-of', 'json', str(ALPHA)]))['streams'][0]
    w, h = probe['width'], probe['height']
    assert (w, h) == (box['w'], box['h']), ((w, h), box)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-c:v', 'libvpx-vp9', '-i', str(ALPHA),
                          '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], stdout=subprocess.PIPE)
    tops = []
    face_cx = []
    x0 = np.full(h, w, np.int32)
    x1 = np.full(h, -1, np.int32)
    i = 0
    while True:
        buf = p.stdout.read(w * h * 4)
        if not buf:
            break
        assert len(buf) == w * h * 4
        occ = np.frombuffer(buf, np.uint8).reshape(h, w, 4)[:, :, 3] > 24
        rows = np.flatnonzero(occ.any(1))
        assert len(rows)
        tops.append(int(rows[0]))
        x0[rows] = np.minimum(x0[rows], occ.argmax(1)[rows])
        x1[rows] = np.maximum(x1[rows], (w - 1 - occ[:, ::-1].argmax(1))[rows])
        if i % 10 == 0:
            band = occ[rows[0]:rows[0] + FACE_BAND]
            ys, xs = np.nonzero(band)
            face_cx.append(float(xs.mean()) + box['left'])
        i += 1
    assert p.wait() == 0
    assert len(tops) == EXPECT_FRAMES, len(tops)
    assert min(tops) >= 24, min(tops)
    crown = box['top'] + min(tops)
    cap_y = round(crown - CLEAR - CAP.CAP_PILL_HEIGHT / 2, 1)
    zy1 = round(cap_y - CAP.CAP_PILL_HEIGHT / 2 - CLEAR, 1)
    sha = hashlib.sha256(ALPHA.read_bytes()).hexdigest()
    mass = np.array(face_cx)
    face = {'frames_sampled': len(face_cx), 'band_rows': FACE_BAND,
            'mass_cx_median': round(float(np.median(mass)), 1),
            'mass_cx_p5_p95': [round(float(np.percentile(mass, 5)), 1),
                               round(float(np.percentile(mass, 95)), 1)],
            'offset_from_540': round(float(np.median(mass)) - 540.0, 1)}
    out = {'source': str(ALPHA), 'source_sha256': sha, 'frames_sampled': len(tops),
           'plate_box': box, 'union_top_canvas': crown,
           'row_x0': x0.tolist(), 'row_x1': x1.tolist(),
           'face_centre_canvas': face,
           'crown_gate': {'frames': len(tops), 'frames_on_plate_top': tops.count(0),
                          'minimum': min(tops),
                          'worst_frame': int(np.argmin(tops))},
           'seats': {'CAP_Y': cap_y, 'ZY0': 192.0, 'ZY1': zy1,
                     'CAP_H_true_rendered': CAP.CAP_PILL_HEIGHT,
                     'true_clear_to_crown': round(crown - cap_y - CAP.CAP_PILL_HEIGHT / 2, 2)}}
    (RUN / f'gen/_envelope_{VID}.json').write_text(json.dumps(out, indent=2))
    bf = DF.measure_band_frames(ALPHA)
    bf['source_sha256'] = sha
    dst = RUN / f'gen/_df/bandframes_{VID}.json'
    dst.parent.mkdir(exist_ok=True)
    dst.write_text(json.dumps(bf))
    print(json.dumps({'frames': len(tops), 'minimum_top': min(tops),
                      'crown_canvas': crown, 'seats': out['seats'], 'face': face}))


if __name__ == '__main__':
    main()
