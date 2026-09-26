"""Block a cropped person before exporting the expensive finished layers."""
from pathlib import Path
import cv2
import numpy as np
from selection import atomic_json, digest

FLOOR_PX = 24.0


def check(alpha, display, *, expected_frames, report):
    key={'alpha_sha256':digest(alpha),'display_sha256':digest(display),
         'guard_sha256':digest(__file__),'expected_frames':expected_frames,'floor_px':FLOOR_PX}
    report=Path(report)
    if report.exists():
        import json
        saved=json.loads(report.read_text())
        if saved.get('identity')==key and saved.get('pass') is True:return saved
    display_cap=cv2.VideoCapture(str(display));display_height=display_cap.get(cv2.CAP_PROP_FRAME_HEIGHT);display_cap.release()
    cap=cv2.VideoCapture(str(alpha));height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    if height<=0 or display_height<=0:raise ValueError('Cannot measure headroom inputs')
    scale=display_height/height;fps=cap.get(cv2.CAP_PROP_FPS)
    bad=[];count=0;minimum=float('inf');worst=None
    while True:
        ok,frame=cap.read()
        if not ok:break
        # Ignore isolated mask specks, not a narrow cap or fingertip.
        foreground=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)>=128
        rows=np.flatnonzero(foreground.sum(axis=1)>=2)
        clearance=float(rows[0])*scale if rows.size else -1.0
        if clearance<minimum:minimum=clearance;worst=count
        if clearance<FLOOR_PX:bad.append(count)
        count+=1
    cap.release()
    result={'identity':key,'pass':count==expected_frames and not bad,'frames_checked':count,
            'min_top_clearance_px':minimum if count else None,'floor_px':FLOOR_PX,
            'worst_frame':worst,'worst_seconds':worst/fps if fps and worst is not None else None,
            'unsafe_frames':len(bad),'first_unsafe_frames':bad[:30],
            'scope':'Every matte frame, top edge of prepared person layer; no caption or semantic face claim'}
    atomic_json(report,result)
    if not result['pass']:
        raise ValueError(f'HEADROOM HOLD: {len(bad)} unsafe frames; minimum {minimum:.1f}px, need {FLOOR_PX}px. '
                         'Move/enlarge the crop and re-review the selection. Never erase the head or hands to pass. '
                         'If the original camera frame is already clipped, flag the source recording.')
    return result
