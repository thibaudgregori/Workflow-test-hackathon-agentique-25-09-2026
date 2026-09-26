"""HEAD HEIGHT ON THE DELIVERED SHORT — the cutout's own unambiguous instrument.

The composited frame is a bad place to look for the top of his cap: the depth
field puts DARK tiles above his head, and the luminance dark-run scan
(`pipeline/measure_head.py`) walks straight into them.  On the shipped
`perplexityprojects` cutout it resolved a cap top on only 8 of 18 sampled frames
and the other 10 fell back to `1.42 x face_h`, a different estimator.

So the crown is taken from the thing that DEFINES it — the matte's own alpha,
which is the die-cut edge the viewer sees — and the chin from MediaPipe on the
delivered frame.  The alpha layer is painted 1:1, so `canvas_y = plate_top + alpha_row`
with no scale factor in between. Pass the actual layer top after a recrop;
930 remains the default for older callers. The layer's LEFT
offset is per-video and must be passed in: an OVER-WIDE plate (kimiram -351,
impossibletask -252) is deliberately not centred, and assuming the chassis'
default -54 puts the face column band on the wrong part of the alpha.

    head_canvas_px = chin_y_canvas - crown_y_canvas
    head_405x720   = head_canvas_px * 720 / 1920

Reported at 405x720 so it is directly comparable with round 6's clerk sheet, and
in canvas px so it can be read against FRAMING.md's 496 +- 38.4 px law.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

F = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(F / "pipeline"))  # measure_head.py lives here since 2026-09-20
import measure_head as MH  # noqa: E402
import cv2  # noqa: E402

PLATE_TOP = 930.0
K405 = 720.0 / 1920.0


def crown_rows(alpha: Path, w: int, h: int, idxs: set[int], cx_frac: dict,
               plate_left: float) -> dict:
    """Topmost opaque row inside a column band centred on the face, per frame."""
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", str(alpha),
         "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
    fs = w * h * 4
    out, i = {}, 0
    while True:
        buf = proc.stdout.read(fs)
        if len(buf) < fs:
            break
        if i in idxs:
            a = np.frombuffer(buf, np.uint8).reshape(h, w, 4)[..., 3] > 127
            cxc = cx_frac[i] * 1080.0 - plate_left       # canvas x -> alpha col
            x0, x1 = int(max(0, cxc - 90)), int(min(w, cxc + 90))
            rows = np.where(a[:, x0:x1].any(1))[0]
            out[i] = int(rows.min()) if rows.size else None
        i += 1
    proc.stdout.close(); proc.wait()
    return out


def measure(video: Path, alpha: Path, times: list[float], plate_left: float,
            fps: float = 25.0, *, plate_top: float = PLATE_TOP) -> dict:
    pr = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "json", str(alpha)],
        capture_output=True, text=True, check=True).stdout)["streams"][0]
    aw, ah = pr["width"], pr["height"]
    chins, cxs = {}, {}
    for t in times:
        m = MH.measure(str(video), t)
        if not m:
            continue
        i = int(round(t * fps))
        chins[i] = m["chin_y_frac"] * 1920.0
        cxs[i] = m["face_cx_frac"]
    crowns = crown_rows(alpha, aw, ah, set(chins), cxs, plate_left)
    rows = []
    for i, chin in sorted(chins.items()):
        c = crowns.get(i)
        if c is None:
            continue
        crown_canvas = plate_top + c
        rows.append({"frame": i, "t": round(i / fps, 2),
                     "crown_canvas_y": round(crown_canvas, 1),
                     "chin_canvas_y": round(chin, 1),
                     "head_canvas_px": round(chin - crown_canvas, 1)})
    hh = np.array([r["head_canvas_px"] for r in rows])
    return {"video": str(video), "alpha": str(alpha), "plate_top": plate_top, "n": len(rows),
            "head_canvas_px": {"median": round(float(np.median(hh)), 1),
                               "p10": round(float(np.percentile(hh, 10)), 1),
                               "p90": round(float(np.percentile(hh, 90)), 1)},
            "head_405x720_px": round(float(np.median(hh)) * K405, 1),
            "head_frac_of_1920": round(float(np.median(hh)) / 1920, 4),
            "law_496_delta_pct": round((float(np.median(hh)) - 496.0) / 496.0 * 100, 1),
            "samples": rows}


if __name__ == "__main__":
    out = {}
    for spec in sys.argv[1:]:
        label, vid, alpha, left, t0, t1, n = spec.split("|")
        ts = [round(float(t), 2) for t in np.linspace(float(t0), float(t1), int(n))]
        out[label] = measure(Path(vid), Path(alpha), ts, float(left))
        out[label]["plate_left"] = float(left)
        r = out[label]
        print(f"{label:36s} n={r['n']:3d}  canvas {r['head_canvas_px']['median']:6.1f} "
              f" @405x720 {r['head_405x720_px']:6.1f}  vs law 496: "
              f"{r['law_496_delta_pct']:+.1f}%")
    Path(sys.argv[0]).with_name("_headscale_matte.json").write_text(json.dumps(out, indent=1))
