#!/usr/bin/env python
"""Local driver for the deployed `shorts-factory-sam2::track` function.

This is the thing a session actually runs.  It hydrates the DEPLOYED function by
name — it does not import `modal_app.py`, does not `modal run`, and cannot
accidentally deploy a local edit — packs the plate and the prompt masks, calls
the GPU, writes the raw alpha next to the session, and reports measured cost.

    ../../../.venv/bin/python track.py \
        --session sessions/airtable \
        --plate   sessions/airtable/plate_wide_25.mp4 \
        --prompts sessions/airtable/prompts \
        --tag v1

    # cents-priced probe: the warm-up lap plus 40 frames, which is all it takes
    # to answer a frame-0 question
    ... track.py --session ... --plate ... --prompts ... --limit 40 --tag probe

PROMPT DIRECTORY CONTRACT.  `--prompts DIR` is scanned for `kf_%05d.png`,
single-channel, plate-sized, >127 = subject.  `kf_00000.png` is the frame-0
prompt and lands on the DISCARDED warm-lap copy of frame 0.  Any other index is
a corrective keyframe applied at that frame.  With no `kf_00000.png` you must
pass `--points`, and you should read the STANDING RULE — FRAME 0 first.

WHAT TO DO WITH THE ANSWER.  A raw alpha is not a matte.  Run `ship.py` for the
post stack and the rim, then `contain.py` against the previous track (a swap has
to be shown to have stayed in its lane) and `stability.py --frame0` (the opening
frame must not be the roughest frame of its own opening).

    --- OR ASK FOR THE MATTE IN THE SAME CALL (2026-09-03) ---

`--ship` gets the finished matte back from the same dispatch.  The GPU
container writes the alpha, the tracked plate and the display plate to the
volume, SPAWNS the CPU-only `ship_remote` lane and exits — so the H100 stops
billing the moment tracking ends — and this driver collects the second
container's result by call id.  It comes back with the three webm layers, the
ship record and both gate verdicts, and writes them into the session exactly
where `ship.py` would have.

Nothing about the matte changes: same `ship.ship_all`, same encoder arguments,
same ffmpeg release line (the ship image carries a static n9.0 build for
exactly this, because Debian's 5.1 does RGB->YUV on the wrong matrix).

THE VARIANT THAT WAS REJECTED, so nobody re-invents it: shipping inside the GPU
container.  Measured 2026-09-03 — 133 s at 8 cores, 148 s at 32, against 57 s
on this laptop, with an idle H100 billing $0.001097/s through all of it
($0.51 for costpertask against $0.13 for its track).  A GPU held open for a
libvpx encode is the most expensive CPU on Modal.

The DISPLAY PLATE still comes from here — it needs the 4K master — so `--ship`
wants `--display WxH` and `--display-plate <mp4>` (cut it with `prep_batch`'s
background stage, or `ship.build_display_plate`).  Without them the layers come
out at the tracked plate's own size, which is the v4 face-detail defect.

    ... track.py --session ... --plate ... --prompts ... \
        --ship --display 1386x990 --display-plate sessions/astramath/plate_display_1386x990.mp4 \
        --edge-box '1386x990+-153+930'
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import costs as COSTS                                            # noqa: E402
APP, FN = "shorts-factory-sam2", "track"
LANES = {"a10": "track", "h100": "track_h100"}   # deployed function per GPU

GPU_USD_S, CPU_USD_S_CORE, MEM_USD_S_GIB = 0.000306, 0.0000131, 0.00000222
GPU_RATES_USD_S = {"A10": 0.000306, "H100": 0.001097, "L40S": 0.000542,
                   "A100": 0.000694, "L4": 0.000222, "T4": 0.000164}


def gpu_rate(gpu_name: str) -> float:
    n = (gpu_name or "").upper()
    for key, rate in GPU_RATES_USD_S.items():
        if key in n:
            return rate
    return GPU_USD_S
CPU_CORES, MEM_GIB = 4.0, 16


def cost(rec, dispatched_at):
    """Billed boot -> scaledown, plus the 2 s scaledown window.  Same arithmetic
    the GPU bench used, so these numbers stay comparable with its report."""
    billed = (rec["t_fn_exit_epoch"] - rec["t_import_epoch"]) + 2.0
    rec["gpu_rate_usd_s"] = gpu_rate(rec.get("gpu", ""))
    gpu = billed * rec["gpu_rate_usd_s"]
    cpu = billed * CPU_CORES * CPU_USD_S_CORE
    mem = billed * MEM_GIB * MEM_USD_S_GIB
    rec["cold_start_seconds"] = round(rec["t_import_epoch"] - dispatched_at, 2)
    rec["billed_container_seconds"] = round(billed, 1)
    rec["measured_cost_usd"] = round(gpu + cpu + mem, 4)
    rec["cost_breakdown_usd"] = dict(gpu=round(gpu, 4), cpu=round(cpu, 4),
                                     mem=round(mem, 4))
    return rec


def json_safe(o, path="rec"):
    """Make the run record writable, and SAY what was not.

    A record that cannot be serialised loses a paid GPU run — the alpha is on
    disk, the ship has already been collected, and the driver dies on the last
    line.  So every bytes value becomes a marker naming its size instead of
    killing the write.  Popping the known blobs by name stays the primary fix;
    this is the net under it.
    """
    if isinstance(o, bytes):
        print(f"WARNING: {path} was {len(o):,} bytes — replaced with a marker "
              "in the run record (pop it by name in track.py)")
        return f"<{len(o)} bytes dropped from the record>"
    if isinstance(o, dict):
        return {k: json_safe(v, f"{path}.{k}") for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [json_safe(v, f"{path}[{i}]") for i, v in enumerate(o)]
    return o


def load_prompts(d: Path) -> dict:
    if not d or not d.exists():
        return {}
    out = {}
    for p in sorted(d.glob("kf_*.png")):
        if p.name.startswith("."):          # macOS AppleDouble siblings
            continue
        # `prompt0.py cut` writes its PROOF SHEET as `kf_overlay_%05d.png` into
        # the same directory, and it matches `kf_*.png`.  Before this guard the
        # first cut prompt any session produced made `track.py` die on
        # `int('overlay')` — a 100 % failure for every new port, found on
        # impossibletask (run 9, 2026-09-01).  Take only the numeric ones; the
        # overlay is evidence, never a prompt.
        part = p.stem.split("_")[1]
        if not part.isdigit():
            continue
        out[int(part)] = p.read_bytes()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", required=True,
                    help="session directory; the alpha and run record land here")
    ap.add_argument("--plate", required=True, help="the plate mp4")
    ap.add_argument("--prompts", default=None, help="dir of kf_%%05d.png masks")
    ap.add_argument("--points", default=None,
                    help="fallback frame-0 clicks, 'x,y,label;x,y,label;...'")
    # ── the exclusion object (2026-09-04) ───────────────────────────────────
    ap.add_argument("--exclude-box", default=None, metavar="x0,y0,x1,y1",
                    help="frame-0 box, PLATE pixels, for the second tracked "
                         "object (obj 2).  The emitted alpha is obj1 AND NOT "
                         "obj2, so this is how you say 'that black thing "
                         "beside my black cap is the chair'")
    ap.add_argument("--exclude-points", default=None,
                    help="frame-0 clicks for obj 2, 'x,y,label;...' (label 1 "
                         "positive on the chair, 0 negative on him)")
    ap.add_argument("--exclude-dilate", type=int, default=2,
                    help="px the obj-2 mask is grown by before subtraction, "
                         "so the surviving boundary sits on the chair's side")
    ap.add_argument("--exclude-name", default=None,
                    help="free text recorded with the exclusion prompt")
    # ── the luma-gated dilation, 2026-09-04.  OFF unless asked for. ─────────
    ap.add_argument("--exclude-luma-dilate", type=int, default=None,
                    help="extra reach in px, DARK PIXELS ONLY: a geodesic "
                         "dilation of the chair mask inside {plate luma < "
                         "--exclude-luma-max}, so it can never eat skin (a "
                         "bright pixel stops it).  OMIT to get the deployed "
                         "standard pass (8 px); 0 turns the gate off and "
                         "leaves the flat margin alone")
    ap.add_argument("--exclude-luma-max", type=int, default=None,
                    help="'dark' means plate luma below this.  Omit for the "
                         "deployed default (60, wingfix's own guard)")
    ap.add_argument("--exclude-luma-rows", default=None, metavar="r0,r1",
                    help="fence the luma-gated growth to these plate rows.  "
                         "OMIT and the container derives it from the frame-0 "
                         "silhouette (crown+180 .. arrival-48), which is what "
                         "protects the black things that are HIS and touch the "
                         "chair: his cap above, his t-shirt below")
    ap.add_argument("--exclude-temporal-fraction", type=float, default=None,
                    help="chunk share that defines stable chair support inside "
                         "the same dark fence (deployed default 0.20); 0 disables "
                         "the temporal anti-flicker pass")
    ap.add_argument("--exclude-temporal-luma-slack", type=int, default=None,
                    help="codec headroom added to the stable support's dark "
                         "threshold (deployed default 10 for q=2 JPEG vs MP4)")
    ap.add_argument("--exclude-json", default=None,
                    help="a `chairprompt.py` record (or a bare list of "
                         "exclusion dicts).  This is how the standard pass "
                         "passes BOTH wings: left becomes obj 2, right obj 3")
    ap.add_argument("--no-chair-object", action="store_true",
                    help="ignore --exclude-json / --exclude-box entirely and "
                         "track ONE object, byte-identical to the pre-2026-09-04 "
                         "path")
    ap.add_argument("--exclude-no-fence", action="store_true",
                    help="deliberately UNFENCED dark growth.  It will eat his "
                         "t-shirt; measured, and it is not a production path")
    ap.add_argument("--frames-tar", default=None,
                    help="a tar of %%05d.jpg, for a BIT-exact rerun")
    ap.add_argument("--tag", default="v1")
    ap.add_argument("--chunk", type=int, default=350)
    ap.add_argument("--overlap", type=int, default=8)
    ap.add_argument("--warm", type=int, default=15,
                    help="warm-up lap length; 0 reproduces a pre-fix track")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--dtype", choices=("fp32", "bf16"), default="fp32")
    ap.add_argument("--gpu", choices=tuple(LANES), default="h100",
                    help="deployed lane: h100 (the default since 2026-09-03 — "
                         "2.73x faster per frame for 1.23x the cost per frame, "
                         "and it is what makes the in-container ship worth "
                         "having) or a10 (every published lab number)")
    # ── --ship: the matte comes back with the alpha ──────────────────────────
    ap.add_argument("--ship", action="store_true",
                    help="ship on Modal's CPU lane straight after the track "
                         "and write the three layers + the ship json into the "
                         "session")
    ap.add_argument("--display", default=None, metavar="WxH",
                    help="the chassis display box the layers are encoded AT")
    ap.add_argument("--display-plate", default=None,
                    help="the mp4 cut from the 4K master at --display, built "
                         "here (the container has no master)")
    ap.add_argument("--display-crf", type=int, default=12)
    ap.add_argument("--plate-json", default=None,
                    help="the session's plate.json; its overwide.plate_box is "
                         "the edge gate's box.  Default <session>/plate.json")
    ap.add_argument("--edge-canvas", default="1080x1920")
    ap.add_argument("--edge-box", default=None, metavar="WxH+L+T",
                    help="the chassis's ACTUAL layer box; take it verbatim "
                         "from plate.json's overwide.plate_box")
    ap.add_argument("--no-edge-gate", action="store_true")
    ap.add_argument("--emit", default="v5",
                    help="anything but `legacy` writes the v5 triple under "
                         "that name; a parity run uses a scratch name (v5b, "
                         "v5c) so it cannot overwrite a shipped v5")
    ap.add_argument("--pad", choices=("mirror", "replicate"), default="mirror")
    ap.add_argument("--temporal", type=int, default=3)
    ap.add_argument("--rim", type=int, default=7)
    ap.add_argument("--crf", type=int, default=10)
    # THE COST LEDGER (2026-09-04).  A hand-run track — a chair pass, an
    # exclusion-object experiment, a repair re-track outside prep_batch — is
    # real Modal money that no report was collecting.  `--run` (or $SHORTS_RUN)
    # says which run's `costs.jsonl` it belongs to; without either, the track
    # runs exactly as before and books nothing.
    ap.add_argument("--run", default=None,
                    help="the run folder this track's cost belongs to "
                         "(default: $SHORTS_RUN; omit to book nothing)")
    a = ap.parse_args()

    import modal

    sess = Path(a.session)
    sess.mkdir(parents=True, exist_ok=True)
    pm = load_prompts(Path(a.prompts)) if a.prompts else {}
    pts = None
    if a.points:
        pts = [[int(v) for v in t.split(",")] for t in a.points.split(";") if t]
    if 0 not in pm and not pts:
        raise SystemExit("no frame-0 prompt: give --prompts with kf_00000.png "
                         "or --points")
    if 0 not in pm:
        print("WARNING: point prompt on frame 0.  SAM2 re-segments a prompted "
              "frame from the prompt it is handed, so the opening frame lands "
              "rougher than its neighbours.  The warm-up lap is what makes this "
              "survivable — do not set --warm 0.  See README, STANDING RULE.")

    excl = None
    if a.exclude_json and not a.no_chair_object:
        blob = json.loads(Path(a.exclude_json).read_text())
        if isinstance(blob, list):
            excl = blob
        else:
            excl = []
            for side in ("left", "right"):
                b = blob.get(side) or {}
                if b.get("found"):
                    excl.append(dict(box=b["box"], points=b["points"],
                                     name=f"{side} headrest wing"))
            if not excl:
                print("--exclude-json: no wing found on either side; tracking "
                      "ONE object (the old path, byte-identical)")
                excl = None
        if excl:
            for e in excl:
                if a.exclude_luma_dilate is not None:
                    e["luma_dilate"] = int(a.exclude_luma_dilate)
                if a.exclude_luma_max is not None:
                    e["luma_max"] = int(a.exclude_luma_max)
                if a.exclude_temporal_fraction is not None:
                    e["temporal_fraction"] = float(a.exclude_temporal_fraction)
                if a.exclude_temporal_luma_slack is not None:
                    e["temporal_luma_slack"] = int(a.exclude_temporal_luma_slack)
                if a.exclude_no_fence:
                    e["luma_rows"] = None
                elif a.exclude_luma_rows:
                    e["luma_rows"] = [int(v) for v in
                                      a.exclude_luma_rows.replace(" ", "").split(",")]
            print(f"EXCLUDE {len(excl)} object(s): "
                  + ", ".join(str(e.get('name')) for e in excl))
    elif (a.exclude_box or a.exclude_points) and not a.no_chair_object:
        excl = dict(dilate=int(a.exclude_dilate), name=a.exclude_name)
        if a.exclude_box:
            box = [int(v) for v in a.exclude_box.replace(" ", "").split(",")]
            if len(box) != 4:
                raise SystemExit("--exclude-box wants x0,y0,x1,y1")
            excl["box"] = box
        if a.exclude_points:
            excl["points"] = [[int(v) for v in t.split(",")]
                              for t in a.exclude_points.split(";") if t]
        # ONLY the flags actually given travel.  An absent key means "give me
        # the deployed standard pass", so the defaults live in ONE place
        # (modal_app.py) and this driver cannot silently pin an old value.
        if a.exclude_luma_dilate is not None:
            excl["luma_dilate"] = int(a.exclude_luma_dilate)
        if a.exclude_luma_max is not None:
            excl["luma_max"] = int(a.exclude_luma_max)
        if a.exclude_temporal_fraction is not None:
            excl["temporal_fraction"] = float(a.exclude_temporal_fraction)
        if a.exclude_temporal_luma_slack is not None:
            excl["temporal_luma_slack"] = int(a.exclude_temporal_luma_slack)
        if a.exclude_no_fence:
            excl["luma_rows"] = None
        elif a.exclude_luma_rows:
            rr = [int(v) for v in
                  a.exclude_luma_rows.replace(" ", "").split(",")]
            if len(rr) != 2:
                raise SystemExit("--exclude-luma-rows wants r0,r1")
            excl["luma_rows"] = rr
        print(f"EXCLUDE obj 2: {excl}")

    kw = dict(prompt_masks={str(k): v for k, v in pm.items()}, points=pts,
              exclude=excl,
              session=sess.name, tag=a.tag, chunk=a.chunk, overlap=a.overlap,
              warm=a.warm, limit=a.limit, fps=a.fps, dtype=a.dtype,
              return_alpha=True)
    if a.frames_tar:
        kw["frames_tar"] = Path(a.frames_tar).read_bytes()
    else:
        kw["video"] = Path(a.plate).read_bytes()

    pj_path = Path(a.plate_json) if a.plate_json else (sess / "plate.json")
    if a.ship:
        # THE BOX AND THE DISPLAY SIZE TRAVEL WITH THE CALL.  The container has
        # no session directory, so what ship.py would have read off disk is
        # handed to it: plate.json's contents (for the over-wide box) and the
        # display plate's own bytes (it needs the 4K master to cut, and the
        # master never leaves this machine).
        kw["ship"] = dict(
            emit=a.emit, pad=a.pad, temporal=a.temporal, rim=a.rim,
            crf=a.crf, fps=a.fps, display=a.display,
            display_crf=a.display_crf, edge_canvas=a.edge_canvas,
            edge_box=a.edge_box, no_edge_gate=bool(a.no_edge_gate),
            plate_json=(json.loads(pj_path.read_text())
                        if pj_path.exists() else None))
        if a.display_plate:
            dp = Path(a.display_plate)
            if not dp.exists():
                raise SystemExit(f"--display-plate {dp} does not exist; the "
                                 "container cannot cut it (no 4K master)")
            kw["display_plate"] = dp.read_bytes()
        elif a.display:
            raise SystemExit("--display without --display-plate: the container "
                             "has no master to re-cut the RGB from")
        else:
            print("WARNING: --ship without --display/--display-plate.  The "
                  "layers come out at the TRACKED plate's size and the chassis "
                  "will upscale them — that is the v4 face-detail defect.")

    fn = modal.Function.from_name(APP, LANES[a.gpu])
    t0 = time.time()
    rec = fn.remote(**kw)
    rec["lane"] = LANES[a.gpu]
    blob = rec.pop("alpha", b"")
    blob2 = rec.pop("alpha_exclude", None)
    # THE NEEDS-HUMAN PATH RETURNS A THIRD ALPHA (2026-09-04).  When the leak
    # heal runs and the second sweep STILL fires, `_track` hands back both
    # tracks — and this driver popped two of the three, so the record write died
    # on `TypeError: Object of type bytes is not JSON serializable` and took the
    # whole run with it AFTER the GPU had been paid for.  trycmm/run 14 was the
    # first take to trip it: leak `furniture`, healed, needs_human.
    blob3 = rec.pop("alpha_preheal", None)
    layers = rec.pop("layers", None) or {}
    cost(rec, t0)

    # ── COLLECT THE SHIP THE GPU CONTAINER SPAWNED ───────────────────────────
    # The track function hands the ship to a CPU-only container and returns its
    # call id immediately, so the GPU stops billing while the VP9 encode runs.
    # This is where the laptop waits for that second container — one dispatch,
    # two results.
    ship = rec.get("ship") or {}
    if ship.get("call_id"):
        t_ship = time.time()
        print(f"ship spawned on the CPU lane ({ship['call_id']}); waiting ...",
              flush=True)
        sr = modal.FunctionCall.from_id(ship["call_id"]).get(timeout=7200)
        layers = sr.pop("layers", None) or {}
        ship.update(sr)
        ship["client_wall_seconds"] = round(time.time() - t_ship, 2)
        rec["ship_seconds"] = ship.get("ship_seconds")
        rec["ship_cost_usd"] = ship.get("measured_cost_usd")
        rec["total_cost_usd"] = round((rec.get("measured_cost_usd") or 0.0)
                                      + (rec["ship_cost_usd"] or 0.0), 4)

    out = sess / f"alpha_{a.tag}.mkv"
    out.write_bytes(blob)
    rec["alpha_local"] = str(out)
    if blob2:
        # the exclusion objects' own alpha: what actually did the subtracting,
        # so it can be watched rather than inferred from what is missing
        out2 = sess / f"alpha_{a.tag}_exclude.mkv"
        out2.write_bytes(blob2)
        rec["exclude_alpha_local"] = str(out2)
    if blob3:
        # the pre-heal track, so the decision is made by eyes on two files
        out3 = sess / f"alpha_{a.tag}_preheal.mkv"
        out3.write_bytes(blob3)
        rec["preheal_alpha_local"] = str(out3)
    rec["plate_local"] = str(Path(a.plate))

    # ── the layers the container encoded, written where ship.py would ────────
    if layers:
        srec = ship.get("record") or {}
        stem = sess / f"matte_{sess.name}_{a.emit}"
        wrote = {}
        for k, name in (srec.get("outputs") or {}).items():
            p = sess / Path(name).name
            p.write_bytes(layers[k])
            wrote[k] = str(p)
        srec["outputs"] = wrote
        srec["alpha_src"] = str(out)
        srec["plate"] = (str(Path(a.display_plate)) if a.display_plate
                         else str(Path(a.plate)))
        if a.display_plate:
            srec["display_plate"] = str(Path(a.display_plate))
        sj = stem.with_name(stem.name + "_ship.json")
        sj.write_text(json.dumps(srec, indent=1))
        ship["ship_json_local"] = str(sj)
        ship["outputs_local"] = wrote
    rec_path = sess / f"run_{a.tag}.json"
    rec_path.write_text(json.dumps(json_safe(rec), indent=1))

    # ── THE COST LEDGER ──────────────────────────────────────────────────────
    # Written the moment the run record is on disk, out of the numbers `cost()`
    # already measured — never re-priced.  The ref is the run record plus the
    # container's own start epoch, so a re-track on the same tag is a SECOND
    # row and a re-read of the same record replaces one.
    _ledger_run = a.run or os.environ.get("SHORTS_RUN")
    if _ledger_run:
        _vid = os.environ.get("SHORTS_VID") or sess.name
        _gpu = " ".join(p for p in str(rec.get("gpu") or "").split()
                        if p.upper() != "NVIDIA")[:12].strip()
        COSTS.safe_record(
            _ledger_run, "modal", "track",
            float(rec.get("measured_cost_usd") or 0.0), video=_vid,
            units=(f"{rec.get('billed_container_seconds')} container-s {_gpu}"
                   f" over {rec.get('frames_tracked')} frames"),
            note=f"SAM2 track, tag {a.tag}, session {sess.name}",
            ref=COSTS.call_ref(_ledger_run, rec_path,
                               rec.get("t_import_epoch")))
        if ship.get("measured_cost_usd"):
            COSTS.safe_record(
                _ledger_run, "modal", "ship",
                float(ship["measured_cost_usd"]), video=_vid,
                units=(f"{ship.get('billed_container_seconds')} container-s "
                       f"CPU x{ship.get('cpu_cores')}"),
                note=f"matte ship on {ship.get('where') or 'modal-cpu'}, "
                     f"tag {a.tag}",
                ref=COSTS.call_ref(_ledger_run, ship.get("ship_json_local"),
                                   ship.get("billed_container_seconds")
                                   or f"usd{ship['measured_cost_usd']}"))

    print(json.dumps({k: v for k, v in rec.items()
                      if k not in ("prompts_applied",)}, indent=1)[:20000])
    print(f"\n{len(blob):,} bytes -> {out}")
    print(f"BILLED {rec['billed_container_seconds']}s "
          f"= ${rec['measured_cost_usd']} "
          f"({rec['ms_per_frame']} ms/frame over "
          f"{rec['frames_tracked']} frames)")
    for s in rec.get("seams", []):
        flag = ("  ** BELOW THE FLOOR **"
                if s in (rec.get("seam_warning") or []) else "")
        print(f"  seam @ {s['seam_at']}: agreement min {s['iou_min']} "
              f"mean {s['iou_mean']}{flag}")
    if ship:
        print(f"\nSHIP ({ship.get('where')}): {ship.get('status')}  "
              f"{ship.get('ship_seconds')}s  "
              f"${ship.get('measured_cost_usd')}  "
              f"(client wall {ship.get('client_wall_seconds')}s, "
              f"{ship.get('workers')} compose threads)")
        if ship.get("log"):
            print(ship["log"].rstrip())
        if ship.get("status") == "refused":
            # EXIT 3, not 1: the TRACK succeeded and its alpha is on disk and
            # worth keeping (the remedy is bolsterfix/wingfix + a re-track, and
            # that needs this alpha).  A distinct code lets prep_batch mark the
            # ship stage refused without throwing away a paid GPU run.
            print(f"GATE {ship.get('gate')} REFUSED:\n{ship.get('verdict')}")
            return 3
        for k, v in (ship.get("outputs_local") or {}).items():
            print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
