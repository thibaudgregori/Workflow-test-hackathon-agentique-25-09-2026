#!/usr/bin/env python
"""EDGE CLIP — the silhouette must never touch a side edge above the bust.

WHY THIS FILE EXISTS
====================
Round 4, Miguel: "some clipping on my left side".  Round 5 the same class was
found on `impossibletask`; on 2026-09-02 a full-take sweep found it again on
`kimiram`, in two windows of 0.80 s and 0.20 s.  Every one of those windows had
already been signed off by a clerk doing 2.5 s spot checks.  Three of the four
known windows are under 0.8 s, so **a sampled review cannot clear this defect**:
the instrument has to look at every frame, and it has to be cheap enough that
looking at every frame is the normal path (~40 s per take).

WHAT THE DEFECT LOOKS LIKE, AND WHAT IT IS NOT
----------------------------------------------
The cutout bust is welded to the bottom of the canvas and its shoulders spill
past BOTH side edges on EVERY frame, by design — that is the format's full-bleed
base.  A limb leaving frame is not a defect either: `review/edgeclip_evidence_*`
shows the control frames with the cream keyline tracing his SHOULDER
continuously into the frame edge, which is exactly how a body should exit.

The defect is that the trim is **CUT BY THE PLATE**.  The rim layer is that same
trim dilated 7 px, so where the alpha is flush against the plate's own border the
rim is flush too, and the shape has NO OUTLINE on the side it was cut.  That
outline-less block then enters the visible frame, and a shape with a missing edge
reads as an amputation.  In the evidence sheet the defect frames show the hand
and forearm ending in a hard vertical slice with no keyline along it, against
controls where the keyline runs into the edge.

    a COMPLETE shape running off the canvas  ->  a body leaving frame
    a shape the PLATE cut                    ->  an amputation

**So the gate is the PLATE'S OWN BORDERS, not the visible frame edge.**  The
frame edges are measured too and reported, because how close a limb comes to the
visible edge is worth knowing, but they do not gate.

THE REMEDY IS AN OVER-WIDE PLATE
--------------------------------
Not a repaint, and not a re-crop that shuffles the trade around: on `kimiram`
LAW 44 could not be satisfied by ANY 1.2:1 window (defect frames by visible-left
master column: 117 at 650, 120 at 700, 76 at 740, 20 at 790, 26 at 903, 24 at
1000 — a measured optimum of 20, never a zero).  The remedy is to stop the plate
from being the thing that cuts him:

    keep `k`, the head scale and the face centre EXACTLY as the foundation
    requires, and extend the master crop sideways so the plate is WIDER than the
    visible frame and sits at a more negative left offset.

Then nothing on canvas moves — same visible master window, same head parity,
same face centre, same frozen post parameters, because a plate px is still the
same physical size — and the FRAME does the cutting while the plate never does.
`kimiram` went from a 1188x990 box at (-54, 930) to 1485x990 at (-351, 930).
The plate is then no longer 1.2:1 and no longer centred on the canvas; the
chassis reads its origin from `plate.json` instead of assuming symmetry.  See
`formats/cutout/CHASSIS.md`.

WHY THE OBVIOUS TEST DOES NOT WORK
----------------------------------
"leftmost x above the bottom 15 % of the silhouette" flags 100 % of frames in
every take measured, and separates nothing: at the left edge column the shoulder
occupies the bottom ~155 rows of a ~924-row silhouette (16.8 %), i.e. MORE than
the 15 % exclusion.  Any fixed percentage is a guess about a body.

THE INSTRUMENT — STRUCTURAL, NOT PROPORTIONAL
=============================================
The bust base is excluded by TOPOLOGY, not by a percentage.  At each visible
edge column the silhouette's contiguous opaque runs are extracted per frame:

    BUST RUN     the run that contains the bottom row.  This is the base, and it
                 is allowed to cross the edge — that is what full-bleed means.
    OTHER RUNS   anything else.

A frame is a DEFECT at that edge when either:

  1. ISOLATED LIMB — an opaque run at the edge column that is separated from the
     bust run by transparent background.  Only a hand, finger or elbow can
     produce this.  Unambiguous, no threshold.

  2. CONTACT RISE — the bust run's top climbs more than RISE_PX_PLATE above THAT
     TAKE'S OWN shoulder baseline (the median contact row at that column).  This
     catches the arm that merges with the shoulder instead of detaching from it.

The baseline is per take and per edge because a shoulder height is a property of
the day's chair, not of the format.  It is also tight — across a clean take at a
plate border the contact row moves single digits at p90 (kimiram RIGHT 7,
perplexityprojects LEFT 6, RIGHT 11) and tops out at 16 / 19 / 44 canvas px over
a whole take.  Against 255 on kimiram's cut LEFT and 408 on impossibletask's.
RISE_PX_PLATE = 60 sits above every clean observation and four times below every
defective one.

CALIBRATION, on the three staged cutouts of run 9:

    kimiram (shipped)          2 windows, plate LEFT, 16.92-17.40 / 32.28-32.40
    impossibletask (retired)   3 windows, plate LEFT x2 + RIGHT x1
    perplexityprojects         CLEAN, plate limb margin +42 px both sides

THE MARGIN, REPORTED ALONGSIDE
------------------------------
For each frame and edge, the rows STRICTLY ABOVE that edge column's bust-run top
are limb territory.  The margin is the frame-x of the leftmost opaque pixel in
that territory (and the mirror for the right edge), minimised over the take.  A
negative margin means the limb crossed the visible edge and was cut by it; the
floor is exactly the plate's own left offset, because once the alpha is flush
against its own border it cannot say how much more of him is out there — that
question is answered in master space by a plate-window sweep, not here.

GEOMETRY
--------
The alpha is measured in ITS OWN pixels and mapped to canvas x with the plate
box the chassis records in `_geom_*.json`:

    frame_x = alpha_x * (box_w / alpha_w) + box.left

so an alpha at 1080x900, at 1188x990, or at any future display size all measure
the same silhouette against the same canvas.  Nothing is resampled.

DECODING VP9 ALPHA
------------------
`-c:v libvpx-vp9` MUST precede `-i`.  ffmpeg's default VP9 decoder returns
`yuv420p` and silently drops the alpha plane — the sweep that found this defect
first read zero frames because of it.

USAGE
-----
    $V pipeline/edge_clip_check.py \
        --alpha  pipeline/sam2/sessions/kimiram/matte_kimiram_v5_alpha.webm \
        --geom   <run>/gen/_geom_kimiram.json \
        --label  kimiram \
        --out    <run>/review/edgeclip_kimiram.json \
        --plot   <run>/review/edgeclip_kimiram.png

    # no geom file (e.g. inside ship.py, before a generator has ever run):
    ... --box 1188x990+-54+930 --canvas 1080x1920

Exit code 1 when any defect window is found.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------- the law
RISE_PX = 30.0          # canvas px the bust run may climb above its own baseline
# ...AT THE VISIBLE FRAME EDGE.  At the PLATE'S OWN BORDER — which is where the
# gate lives — the threshold is doubled, and the reason is geometry rather than
# leniency: the plate border sits further out on the shoulder slope, where the
# slope is shallower, so the SAME body sway moves the contact row much further.
# Measured on the three staged cutouts, max contact rise at a plate border over
# a whole take:  kimiram RIGHT 16, perplexityprojects LEFT 19, perplexityprojects
# RIGHT 44  — all clean columns, all shoulder.  Against kimiram LEFT 255 and
# impossibletask LEFT 340, both of which are a cut hand.  60 sits above every
# clean observation and four times below every defective one.  The isolated-limb
# test carries most of the weight in any case; this is the backstop for an arm
# that merges with the shoulder instead of detaching from it.
RISE_PX_PLATE = 60.0
ALPHA_THR = 127         # >  this is opaque
CANVAS_W, CANVAS_H = 1080, 1920


# ------------------------------------------------------------------ probing
def probe_stream(path: Path) -> dict:
    """Width, height, pix_fmt, fps — and whether there is an ALPHA PLANE.

    `pix_fmt` ALONE CANNOT ANSWER THAT for the files this factory ships.  A VP9
    matte written `yuva420p` probes back as plain `yuv420p`, because ffprobe
    uses the default VP9 decoder, which drops the alpha plane before it ever
    reports a format — the same trap that made the first sweep read zero frames.
    The container knows: matroska/webm carries `alpha_mode=1` as a stream tag.
    So the alpha plane is detected from the TAG first, and from `pix_fmt` only
    as a fallback for formats that report it honestly.
    """
    o = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,pix_fmt,r_frame_rate,codec_name:stream_tags=alpha_mode",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    st = json.loads(o)["streams"][0]
    tags = {k.lower(): v for k, v in (st.get("tags") or {}).items()}
    pf = st.get("pix_fmt") or ""
    st["has_alpha"] = (str(tags.get("alpha_mode", "0")) == "1"
                       or pf.startswith("yuva") or pf.startswith("rgba")
                       or pf.startswith("bgra") or pf.startswith("ya"))
    return st


def fps_of(st: dict) -> float:
    n, d = (st.get("r_frame_rate") or "25/1").split("/")
    return float(n) / float(d or 1)


def decode_alpha(path: Path, w: int, h: int, has_alpha: bool):
    """Stream the ALPHA plane as (h, w) uint8, one frame at a time.

    A `yuva*` stream carries a real alpha plane and is pulled through
    `alphaextract` with the VP9 decoder named EXPLICITLY.  A plain gray/`yuv*`
    stream (the raw SAM2 `alpha_*.mkv`) already IS the mask, so it is read as
    luma.  Both paths end in the same array, which is what lets this check run
    on a shipped matte and on a raw track with no special-casing upstream.
    """
    if has_alpha:
        cmd = ["ffmpeg", "-nostdin", "-v", "error", "-c:v", "libvpx-vp9",
               "-i", str(path), "-vf", "alphaextract", "-pix_fmt", "gray",
               "-f", "rawvideo", "-"]
    else:
        cmd = ["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
               "-pix_fmt", "gray", "-f", "rawvideo", "-"]
    n = w * h
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 4)
    try:
        while True:
            b = p.stdout.read(n)
            if len(b) < n:
                return
            yield np.frombuffer(b, np.uint8).reshape(h, w)
    finally:
        p.stdout.close()
        p.wait()


def _margin(b, lim, tag, cols, aw, sx, left, cw):
    """Frame-x of the extreme opaque pixel in the rows ABOVE `lim`."""
    if lim <= 0:
        return float("nan")
    sub = b[:lim]
    if not sub.any():
        return float("nan")
    if tag == "left":
        return int(np.where(sub, cols[None, :], aw).min()) * sx + left
    return (cw - 1.0) - (int(np.where(sub, cols[None, :], -1).max()) * sx + left)


def _extreme_rows(b, tag, cols, aw):
    """Per-row leftmost (or rightmost) opaque column, as int16; aw = empty."""
    if tag == "left":
        return np.where(b, cols[None, :], aw).min(axis=1).astype(np.int16)
    return np.where(b, cols[None, :], -1).max(axis=1).astype(np.int16)


# --------------------------------------------------------------------- runs
def runs_of(col: np.ndarray) -> list[tuple[int, int]]:
    """Contiguous True runs in a boolean column, as [start, end] row pairs."""
    idx = np.flatnonzero(np.diff(np.concatenate(([0], col.view(np.int8), [0]))))
    return [(int(a), int(b - 1)) for a, b in zip(idx[::2], idx[1::2])]


def split_runs(col: np.ndarray) -> tuple[tuple[int, int] | None, list]:
    """(bust run, other runs).  The bust run is the one touching the bottom."""
    rs = runs_of(col)
    if not rs:
        return None, []
    last = rs[-1]
    if last[1] == len(col) - 1:
        return last, rs[:-1]
    return None, rs


# -------------------------------------------------------------------- sweep
def _edge_block(per, tag, c, aw, ah, sx, sy, cw, n, fps, rise_px, ref, left):
    """Verdict + margins at ONE column.  `ref` is the canvas x that column sits
    at, and margins are measured relative to it: for a PLATE edge that is the
    plate's own border, for a FRAME edge it is 0 / cw-1."""
    d = per[(tag, c)]
    bt = np.array(d["bust_top"], float)
    seen = bt >= 0
    base = float(np.median(bt[seen])) if seen.any() else float("nan")
    rise_rows = rise_px / sy
    rise = np.where(seen, base - bt, 0.0)
    iso = np.array(d["n_other"]) > 0
    contact = seen & (rise > rise_rows)
    detached = (~seen) & iso
    bad = iso | contact | detached
    marg = np.array(d["margin"], float)
    fin = np.isfinite(marg)
    lb = int(max(0, round(base - rise_rows))) if seen.any() else 0
    lmar = np.full(n, np.nan)
    for i, rows in enumerate(d["rows"]):
        if lb <= 0:
            continue
        sub = rows[:lb]
        if tag.endswith("left"):
            x = int(sub.min())
            if x < aw:
                lmar[i] = (x * sx + left) - ref
        else:
            x = int(sub.max())
            if x >= 0:
                lmar[i] = ref - (x * sx + left)
    lfin = np.isfinite(lmar)
    windows = []
    idx = np.flatnonzero(bad)
    if idx.size:
        for g in np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1):
            f0, f1 = int(g[0]), int(g[-1])
            windows.append(dict(
                edge=tag, frames=[f0, f1],
                t=[round(f0 / fps, 2), round(f1 / fps, 2)],
                duration_s=round((f1 - f0 + 1) / fps, 2), n_frames=int(g.size),
                peak_rise_canvas_px=round(float((rise[g] * sy).max()), 1),
                isolated_limb_frames=int(iso[g].sum()),
                worst_margin_canvas_px=(round(float(np.nanmin(lmar[g])), 1)
                                        if np.isfinite(lmar[g]).any() else None)))
    stats = dict(
        column_alpha=c, in_alpha=0 <= c < aw,
        reference_canvas_x=round(ref, 1),
        shoulder_baseline_alpha_row=round(base, 1) if seen.any() else None,
        rise_threshold_canvas_px=rise_px,
        rise_canvas_px=(dict(p50=round(float(np.percentile(rise[seen] * sy, 50)), 1),
                             p90=round(float(np.percentile(rise[seen] * sy, 90)), 1),
                             max=round(float((rise[seen] * sy).max()), 1))
                        if seen.any() else None),
        frames_no_bust_run=int((~seen).sum()),
        defect_frames=int(bad.sum()),
        isolated_limb_frames=int(iso.sum()),
        contact_rise_frames=int((contact & ~iso).sum()),
        min_margin_canvas_px=(round(float(marg[fin].min()), 1) if fin.any() else None),
        limb_band_top_alpha_row=lb,
        min_limb_margin_canvas_px=(round(float(lmar[lfin].min()), 1)
                                   if lfin.any() else None),
        p01_limb_margin_canvas_px=(round(float(np.percentile(lmar[lfin], 1)), 1)
                                   if lfin.any() else None),
        median_limb_margin_canvas_px=(round(float(np.median(lmar[lfin])), 1)
                                      if lfin.any() else None))
    trace = dict(bust_top=[int(v) for v in d["bust_top"]],
                 n_other=[int(v) for v in d["n_other"]],
                 limb_margin=[None if not np.isfinite(v) else round(float(v), 1)
                              for v in lmar])
    return stats, windows, trace


def sweep(alpha: Path, box: dict, canvas=(CANVAS_W, CANVAS_H),
          rise_px: float = RISE_PX, rise_px_plate: float = RISE_PX_PLATE) -> dict:
    """Every frame, four columns: the PLATE's own borders and the FRAME's.

    THE GATE IS THE PLATE'S BORDERS.  The defect LAW 44 names is not "a limb is
    near the frame edge" — a body leaving frame is what the format does on every
    approved cutout, and the shoulders do it on every frame.  It is that the trim
    is CUT BY THE PLATE, so the 7 px rim is cut with it and the shape carries no
    outline on the side it was cut.  That shape then enters the visible frame as
    an outline-less block, which is what reads as an amputation.  A COMPLETE
    shape running off the canvas reads as leaving frame.

    So the gate asks: is the silhouette flush against the plate's own left or
    right border, ABOVE THE BUST?  The bust base is exempt, structurally: it is
    the run that touches the bottom row, and it is welded to the frame by design.

    The FRAME edges are measured too and reported, because how close a limb comes
    to the visible edge is worth knowing — but they do not gate.  The remedy for
    a plate-edge failure is an OVER-WIDE PLATE (see CHASSIS.md): keep k, the head
    scale and the face centre exactly, and extend the master crop sideways so the
    plate is wider than the frame and sits at a more negative left offset.  Then
    the frame does the cutting and the plate never does.
    """
    st = probe_stream(alpha)
    aw, ah = int(st["width"]), int(st["height"])
    fps = fps_of(st)
    bw, bh = float(box["w"]), float(box["h"])
    left, top = float(box["left"]), float(box["top"])
    cw, _ch = canvas
    sx, sy = bw / aw, bh / ah

    # PLATE borders (the gate) and FRAME edges (reported), in ALPHA columns
    fl = int(round((0.0 - left) / sx))
    fr = int(round((cw - 1.0 - left) / sx))
    spec = [("plate_left", 0, left),
            ("plate_right", aw - 1, left + (aw - 1) * sx),
            ("frame_left", min(max(fl, 0), aw - 1), 0.0),
            ("frame_right", min(max(fr, 0), aw - 1), cw - 1.0)]

    cols = np.arange(aw)
    per = {(tag, c): dict(bust_top=[], n_other=[], margin=[], rows=[])
           for tag, c, _ in spec}
    n = 0
    for a in decode_alpha(alpha, aw, ah, st["has_alpha"]):
        b = a > ALPHA_THR
        rows_l = _extreme_rows(b, "left", cols, aw)
        rows_r = _extreme_rows(b, "right", cols, aw)
        for tag, c, ref in spec:
            d = per[(tag, c)]
            bust, other = split_runs(b[:, c])
            d["bust_top"].append(bust[0] if bust else -1)
            d["n_other"].append(len(other))
            lim = bust[0] if bust else ah
            d["margin"].append(_margin(b, lim, "left" if tag.endswith("left")
                                       else "right", cols, aw, sx,
                                       left if tag.startswith("plate") else left,
                                       cw))
            d["rows"].append(rows_l if tag.endswith("left") else rows_r)
        n += 1
    if not n:
        raise SystemExit(f"decoded 0 frames from {alpha} — if this is a VP9 "
                         f"alpha, the decoder dropped the alpha plane")

    # A PLATE BORDER GATES ONLY IF IT IS ON SCREEN.  Miguel, 2026-09-03 (run 12):
    # "if my hand just goes slightly out of the border, it's okay."  With an
    # OVER-WIDE plate the plate's own border sits OUTSIDE the phone's visible
    # frame, so a hand cut there, and the 7 px rim cut with it, is never seen:
    # the frame does the cutting, which is exactly the remedy this law
    # prescribes.  So a plate side is gated only when its border lies inside
    # the visible canvas or within RIM_PX of it; otherwise its windows are
    # reported as information, like the frame edges.  astramath and
    # chatgptwork (run 12) were refused for one- and two-frame touches at a
    # plate border 153 / 136 px outside the frame; those now ship.
    RIM_PX_VISIBLE = 7.0
    plate_right_edge = left + bw
    visible_gate = {
        "plate_left": left > -RIM_PX_VISIBLE,
        "plate_right": plate_right_edge < cw + RIM_PX_VISIBLE,
    }
    outside_px = {"plate_left": round(-left, 1),
                  "plate_right": round(plate_right_edge - cw, 1)}

    blocks, traces, gate_windows, info_windows = {}, {}, [], []
    for tag, c, ref in spec:
        thr = rise_px_plate if tag.startswith("plate") else rise_px
        stats, wins, tr = _edge_block(per, tag, c, aw, ah, sx, sy, cw, n, fps,
                                      thr, ref, left)
        blocks[tag] = stats
        traces[tag] = tr
        if tag.startswith("plate") and not visible_gate[tag]:
            for w in wins:
                w["gated"] = False
                w["why_not_gated"] = (f"{tag} border is {outside_px[tag]} px "
                                      f"outside the visible frame (rim {RIM_PX_VISIBLE:g} px)")
            stats["gated"] = False
            stats["border_outside_frame_px"] = outside_px[tag]
            info_windows.extend(wins)
        else:
            if tag.startswith("plate"):
                stats["gated"] = True
            (gate_windows if tag.startswith("plate") else info_windows).extend(wins)
    gate_windows.sort(key=lambda w: w["frames"][0])
    info_windows.sort(key=lambda w: w["frames"][0])

    return dict(
        alpha=str(alpha), frames=n, fps=fps,
        alpha_size=[aw, ah], pix_fmt=st["pix_fmt"],
        box=dict(w=bw, h=bh, left=left, top=top),
        canvas=[cw, _ch], scale=[round(sx, 6), round(sy, 6)],
        overwide=bool(left < -1 and left + bw > cw + 1),
        law=dict(rise_px_frame=rise_px, rise_px_plate=rise_px_plate,
                 alpha_threshold=ALPHA_THR,
                 gate="the PLATE's own left and right borders, ONLY where "
                      "that border is on screen or within the rim of it "
                      "(Miguel, 2026-09-03)",
                 plate_border_gated=visible_gate,
                 plate_border_outside_frame_px=outside_px,
                 statement="the silhouette never touches a side edge above the "
                           "bust; full-take sweep, never sampled"),
        edges=blocks,
        windows=gate_windows,
        frame_edge_windows=info_windows,
        verdict="CLIPPED" if gate_windows else "CLEAN",
        _traces=traces)



def plot(rep: dict, png: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    tr = rep["_traces"]
    n = rep["frames"]
    fps = rep["fps"]
    t = np.arange(n) / fps
    sy = rep["scale"][1]
    fig, ax = plt.subplots(3, 1, figsize=(15, 10.5), sharex=True)
    fig.suptitle(f"EDGE CLIP — {Path(rep['alpha']).name}   "
                 f"{n} frames / {n / fps:.2f}s   verdict {rep['verdict']}",
                 fontsize=13)

    # 1. the LIMB-BAND margin — the number a plate window is designed against
    lo = 0.0
    for tag, col in (("plate_left", "#c4573a"), ("plate_right", "#2f6f7f"),
                     ("frame_left", "#e0a08a"), ("frame_right", "#8fb6c0")):
        m = np.array([np.nan if v is None else v
                      for v in tr[tag]["limb_margin"]], float)
        if np.isfinite(m).any():
            lo = min(lo, float(np.nanmin(m)))
        ax[0].plot(t, m, lw=0.9 if tag.startswith("plate") else 0.6,
                   color=col, label=f"{tag} limb margin")
    ax[0].axhline(0, color="k", lw=1.2)
    ax[0].axhline(24, color="#888", lw=0.9, ls="--", label="24 px design floor")
    ax[0].set_ylabel("limb margin (canvas px)")
    ax[0].set_title("solid = the PLATE's own borders (the gate); "
                    "pale = the visible frame (reported)", fontsize=9)
    ax[0].legend(loc="upper right", fontsize=8)
    ax[0].set_ylim(min(-70.0, lo - 10.0), 420)
    ax[0].grid(alpha=0.25)

    # 2. contact height above the baseline
    for tag, col in (("plate_left", "#c4573a"), ("plate_right", "#2f6f7f")):
        bt = np.array(tr[tag]["bust_top"], float)
        base = rep["edges"][tag]["shoulder_baseline_alpha_row"]
        r = np.where(bt >= 0, (base - bt) * sy, np.nan) if base is not None \
            else np.full(n, np.nan)
        ax[1].plot(t, r, lw=0.8, color=col, label=f"{tag} contact rise")
    ax[1].axhline(rep["law"]["rise_px_plate"], color="k", lw=1.1, ls="--",
                  label=f"{rep['law']['rise_px_plate']:.0f} px limb threshold "
                        f"(plate border)")
    ax[1].set_ylabel("bust-run top above its baseline, at the PLATE border "
                     "(canvas px)")
    ax[1].legend(loc="upper right", fontsize=8)
    ax[1].grid(alpha=0.25)

    # 3. isolated runs at the edge columns
    for tag, col in (("plate_left", "#c4573a"), ("plate_right", "#2f6f7f")):
        ax[2].plot(t, tr[tag]["n_other"], lw=0.9, color=col,
                   label=f"{tag} detached runs")
    ax[2].set_ylabel("runs detached from the bust")
    ax[2].set_xlabel("seconds")
    ax[2].legend(loc="upper right", fontsize=8)
    ax[2].grid(alpha=0.25)

    for w in rep["windows"]:
        for a in ax:
            a.axvspan(w["t"][0], w["t"][1] + 1 / fps, color="#c4573a",
                      alpha=0.16, lw=0)
    png.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(png, dpi=110)
    plt.close(fig)


# --------------------------------------------------------------- geom / box
def box_from_geom_dict(g: dict, fmt: str = "cutout") -> dict:
    """The plate box, from a `_geom` record in any of its shapes.

    A per-video geom is keyed by FORMAT (`{"cutout": {...}, "split": {...}}`);
    a format-lab geom is the cutout block itself.  Both are accepted, and the
    older `plate.w/h/left/top` spelling is accepted alongside `plate.box`, so a
    geom file from any port can be swept without re-running its generator.
    """
    blk = g.get(fmt) if isinstance(g.get(fmt), dict) else None
    if blk is None:
        blk = g if isinstance(g.get("plate"), dict) else None
    if blk is None:
        blk = next((v for v in g.values()
                    if isinstance(v, dict) and isinstance(v.get("plate"), dict)),
                   None)
    pl = (blk or {}).get("plate") or {}
    bx = pl.get("box")
    # The geometry reports written by the cutout generator spell the box as a
    # MAPPING (`plate.box = {w,h,left,top}`); the older ports spell it as a
    # two-number list beside `plate.left/top`.  Both are the same box.
    if isinstance(bx, dict) and bx.get("w") and bx.get("h"):
        return dict(w=float(bx["w"]), h=float(bx["h"]),
                    left=float(bx.get("left", pl.get("left", 0))),
                    top=float(bx.get("top", pl.get("top", 0))))
    if bx and not isinstance(bx, dict) and len(bx) == 2:
        return dict(w=float(bx[0]), h=float(bx[1]),
                    left=float(pl["left"]), top=float(pl["top"]))
    if pl.get("w") and pl.get("h"):
        return dict(w=float(pl["w"]), h=float(pl["h"]),
                    left=float(pl["left"]), top=float(pl["top"]))
    raise SystemExit(f"no plate box in this geom record for format '{fmt}'")


def box_from_geom(geom_path: Path, fmt: str = "cutout") -> dict:
    return box_from_geom_dict(json.loads(Path(geom_path).read_text()), fmt)


def parse_box(s: str) -> dict:
    """'1188x990+-54+930'"""
    wh, rest = s.split("x", 1)
    h, l, t = rest.replace("+-", "+~").split("+")
    f = lambda v: float(v.replace("~", "-"))
    return dict(w=float(wh), h=f(h), left=f(l), top=f(t))


def centred_box(alpha_w: int, alpha_h: int, canvas_w: int = CANVAS_W,
                canvas_h: int = CANVAS_H) -> dict:
    """The chassis rule, for callers with no geom file (ship.py).

    `chassis_gen.py`: the layer box IS the plate's own encoded size, centred on
    the canvas and base-planted — `PLATE_LEFT = (W - box_w) / 2`,
    `PLATE_TOP = H - box_h`.
    """
    return dict(w=float(alpha_w), h=float(alpha_h),
                left=(canvas_w - alpha_w) / 2.0, top=float(canvas_h - alpha_h))


# --------------------------------------------------------------------- main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alpha", required=True,
                    help="the shipped matte alpha (_alpha.webm), the cut layer, "
                         "or a raw SAM2 alpha_*.mkv")
    ap.add_argument("--geom", default=None, help="_geom_*.json for the plate box")
    ap.add_argument("--format", default="cutout", help="geom block to read")
    ap.add_argument("--box", default=None, metavar="WxH+L+T",
                    help="plate box, when there is no geom file")
    ap.add_argument("--canvas", default=f"{CANVAS_W}x{CANVAS_H}")
    ap.add_argument("--rise", type=float, default=RISE_PX,
                    help="contact-rise threshold at the VISIBLE FRAME edge "
                         "(reported only)")
    ap.add_argument("--rise-plate", type=float, default=RISE_PX_PLATE,
                    help="contact-rise threshold at the PLATE border (the gate)")
    ap.add_argument("--label", default=None)
    ap.add_argument("--out", default=None, help="JSON report")
    ap.add_argument("--plot", default=None, help="PNG plot")
    ap.add_argument("--full-traces", action="store_true",
                    help="keep the per-frame traces in the JSON")
    a = ap.parse_args()

    alpha = Path(a.alpha)
    cw, ch = (int(v) for v in a.canvas.lower().split("x"))
    if a.geom:
        box = box_from_geom(Path(a.geom), a.format)
    elif a.box:
        box = parse_box(a.box)
    else:
        st = probe_stream(alpha)
        box = centred_box(int(st["width"]), int(st["height"]), cw, ch)
        print(f"no --geom/--box: assuming the chassis rule, box "
              f"{box['w']:.0f}x{box['h']:.0f} at ({box['left']}, {box['top']})")

    rep = sweep(alpha, box, (cw, ch), a.rise, a.rise_plate)
    rep["label"] = a.label or alpha.stem
    if a.plot:
        plot(rep, Path(a.plot))
        rep["plot"] = a.plot
    if a.out:
        p = Path(a.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        r = dict(rep) if a.full_traces else {k: v for k, v in rep.items()
                                             if k != "_traces"}
        p.write_text(json.dumps(r, indent=1))

    slim = {k: v for k, v in rep.items() if k != "_traces"}
    print(json.dumps(slim, indent=1))
    for tag in ("plate_left", "plate_right", "frame_left", "frame_right"):
        e = rep["edges"][tag]
        kind = "GATE " if tag.startswith("plate") else "info "
        print(f"{kind}{tag:12s} baseline row {e['shoulder_baseline_alpha_row']}  "
              f"limb margin min {e['min_limb_margin_canvas_px']} px  "
              f"defect frames {e['defect_frames']}")
    if rep["frame_edge_windows"]:
        print(f"\n(reported, NOT a gate) the silhouette crosses the VISIBLE "
              f"frame edge above the bust in "
              f"{len(rep['frame_edge_windows'])} window(s): "
              + ", ".join(f"{w['edge'].split('_')[1]} {w['t'][0]}-{w['t'][1]}s"
                          for w in rep["frame_edge_windows"])
              + ".  With a complete trim that is a body LEAVING FRAME, which is "
                "what the shoulders do on every frame.")
    if rep["windows"]:
        print(f"\nEDGE CLIP: {len(rep['windows'])} window(s) AT THE PLATE BORDER")
        for w in rep["windows"]:
            print(f"  {w['edge']:12s} f{w['frames'][0]}-{w['frames'][1]}  "
                  f"{w['t'][0]:.2f}s-{w['t'][1]:.2f}s  {w['duration_s']}s  "
                  f"peak rise {w['peak_rise_canvas_px']} px  "
                  f"isolated {w['isolated_limb_frames']}")
        raise SystemExit(1)
    print("\nEDGE CLIP: CLEAN — the trim is never cut by the plate above the "
          "bust, so the rim is continuous everywhere the frame cuts him")


if __name__ == "__main__":
    main()
