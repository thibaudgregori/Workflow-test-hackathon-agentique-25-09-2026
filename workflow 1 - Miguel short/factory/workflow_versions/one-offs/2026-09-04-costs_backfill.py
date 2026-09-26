#!/usr/bin/env python3
"""BACKFILL A RUN'S COST LEDGER FROM ITS ARTEFACTS.

The ledger (`pipeline/costs.py`) starts with run 14: every paid call books
itself as its price is measured.  Runs 1-13 have no ledger, but they DO have
every number — scattered across six artefact families, which is exactly why
run 13's cost table was assembled by hand and came out low.  This script reads
those families and writes the rows the live pipeline would have written.

WHERE EACH DOLLAR HIDES, and this list is the point of the file:

  prep/*.json, prep/*/*.json     per video: the BiRefNet sweep inside
                                 `stages.plate.sweep.lane.measured_cost_usd`,
                                 the SAM2 track in `stages.track.cost_usd`, the
                                 matte ship in `stages.ship.cost_usd`, and the
                                 Scribe duration in the cut stage.  A package
                                 named `_<vid>_failed_cut.json` or
                                 `<vid>.prior_*.json` is an ABANDONED attempt
                                 whose GPU was still paid for.
  gen/_rc_*.json (+ .priorN)     one Modal render per result, with the
                                 container's own start epoch
  review/cands_*.json (+ prior)  the post-render Gemini watcher's own bill
  review/clerk_cands_*.json      the clerk's duplicate second watch (retired by
                                 procedure v3.1 on 2026-09-04)
  gen/_qcpass_*.json (+ prior)   Gate 3, whose cost `qc_v3` PRINTED and nobody
                                 stored — parsed back out of the captured stdout
  pipeline/sam2/sessions/<sess>  every hand-run track: repair re-tracks, chair
                                 passes, exclusion-object experiments.  Sessions
                                 are matched to the run's videos by name, and
                                 filtered to containers that started after the
                                 run did.
  intake/transcripts/*.json      the intake's Scribe pass on the RAW recording
  cuts/*/transcript_tight.json   the cut's Scribe pass

Refs follow the live convention (`<path>@<the call's own identity>`) wherever
the artefact carries an identity, so a backfilled row and a live row for the
same call collide on the key instead of double counting.  The Gemini watcher
rows are the exception: the live watcher keys on the WATCHED FILE's mtime, which
a backfill cannot recover, so it keys on the candidates file's own path (the
archived `.priorN` names make each round distinct).  Do not backfill a run that
already has live rows.

    costs_backfill.py --run shorts_run<N> [--dry-run] [--since <epoch>]
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import costs as C                                                # noqa: E402

SESSIONS = HERE / "sam2" / "sessions"


def _load(p) -> dict:
    try:
        d = json.loads(Path(p).read_text())
        return d if isinstance(d, dict) else {}
    except Exception:                                            # noqa: BLE001
        return {}


def _lane(gpu: str) -> str:
    return " ".join(x for x in str(gpu or "").split()
                    if x.upper() != "NVIDIA")[:12].strip()


def _track_ident(stage: dict, rec: dict):
    """The identity of the container THIS PACKAGE paid for.

    A session holds ONE `run_<tag>.json` per tag, so a second track on the same
    tag overwrites the first — and the first is still money.  Run 13's
    viberesearch is exactly that case: the LAW 46 false positive was cut,
    tracked ($0.1278) and thrown away, then re-prepped on the same tag
    ($0.1350), and only the second record survives on disk.  When the package's
    own billed seconds match the record's, the record IS this package's
    container and its epoch is the identity (so a backfilled row collides with
    the live one).  When they disagree, the package is describing a container
    the record no longer holds, and its own billed seconds are the identity —
    which is what keeps the abandoned attempt in the total."""
    same = (stage.get("billed_container_seconds")
            == rec.get("billed_container_seconds"))
    if same and rec.get("t_import_epoch"):
        return rec["t_import_epoch"]
    return f"billed{stage.get('billed_container_seconds')}"


# ---------------------------------------------------------------------------
def from_prep(run: Path) -> tuple[list[dict], float]:
    rows, seen_epochs = [], []
    paths = sorted(glob.glob(str(run / "prep" / "*.json"))) + \
        sorted(glob.glob(str(run / "prep" / "*" / "*.json")))
    for p in paths:
        pkg = _load(p)
        st = pkg.get("stages")
        vid = pkg.get("id")
        if not st or not vid:
            continue
        abandoned = ("failed" in Path(p).stem or "prior" in Path(p).stem)
        tail = " (abandoned attempt, still billed)" if abandoned else ""

        sweep = ((st.get("plate") or {}).get("sweep") or {})
        lane = sweep.get("lane") or {}
        if lane.get("measured_cost_usd"):
            seen_epochs.append(lane.get("t_import_epoch") or 0)
            rows.append(dict(
                service="modal", stage="sweep",
                usd=float(lane["measured_cost_usd"]), video=vid,
                units=(f"{lane.get('billed_container_seconds')} container-s "
                       f"{lane.get('gpu') or ''}").strip(),
                note="BiRefNet master sweep (the plate solve)" + tail,
                ref=C.call_ref(run, sweep.get("file"),
                               lane.get("container")
                               or lane.get("t_import_epoch"))))

        # AFTER A REPAIR, `stages.track` and `stages.ship` POINT AT THE FINAL
        # ROUND — the same money the round's own record already holds.  So the
        # base attempt is read from `repair.round0`, exactly as
        # `prep_batch._round0_cost` does it, and the rounds are booked below.
        rep = st.get("repair") or {}
        r0 = rep.get("round0") or {}
        tr = (r0.get("track") if r0.get("track") else st.get("track")) or {}
        if tr.get("cost_usd") and tr.get("run_record"):
            rec = _load(tr["run_record"])
            seen_epochs.append(rec.get("t_import_epoch") or 0)
            rows.append(dict(
                service="modal", stage="track", usd=float(tr["cost_usd"]),
                video=vid,
                units=(f"{tr.get('billed_container_seconds')} container-s "
                       f"{_lane(tr.get('gpu'))} over "
                       f"{tr.get('frames_tracked')} frames"),
                note=f"SAM2 track, tag {tr.get('tag') or rec.get('tag')}"
                     + tail,
                ref=C.call_ref(run, tr["run_record"],
                               _track_ident(tr, rec))))

        sh = (r0.get("ship") if r0.get("ship") else st.get("ship")) or {}
        if sh.get("cost_usd"):
            rows.append(dict(
                service="modal", stage="ship", usd=float(sh["cost_usd"]),
                video=vid,
                units=f"{sh.get('billed_container_seconds')} container-s CPU",
                note=f"matte ship ({sh.get('where') or 'modal-cpu'}){tail}",
                ref=C.call_ref(run, sh.get("ship_json"),
                               sh.get("billed_container_seconds")
                               or f"usd{sh['cost_usd']}")))

        # every repair round kept its own record, and its money is real
        for rd in (rep.get("rounds") or []):
            # THE ROUND'S REF IS ITS CONTAINER, not the round number — the live
            # `repair_round` books the re-track by the record's own epoch, so
            # the backfilled row must collide with it and with the session
            # sweep below instead of standing beside them.
            rd_path = Path(pkg.get("session", "")) / f"run_{rd.get('tag')}.json"
            rd_rec = _load(rd_path)
            for which, stage in (("track", "track"), ("ship", "ship")):
                cost = (rd.get("cost_breakdown_usd") or {}).get(which)
                if not cost:
                    continue
                ident = (rd_rec.get("t_import_epoch") if which == "track"
                         else None) or f"repair{rd.get('round')}{which}"
                rows.append(dict(
                    service="modal", stage=stage, usd=float(cost), video=vid,
                    units=(f"{rd_rec.get('billed_container_seconds')} "
                           f"container-s {_lane(rd_rec.get('gpu'))}"
                           if which == "track"
                           else f"repair round {rd.get('round')}"),
                    note=f"{which} re-run, repair round {rd.get('round')} "
                         f"({rd.get('gate')}), tag {rd.get('tag')}",
                    ref=C.call_ref(run, rd_path, ident)))

        cut = st.get("cut") or {}
        secs = cut.get("tight_audio_duration_s")
        tfile = cut.get("transcript_tight")
        if secs is None and tfile:
            secs = _load(tfile).get("audio_duration_secs")
        if tfile and secs:
            rows.append(dict(
                service="elevenlabs", stage="scribe",
                usd=C.scribe_usd(secs), video=vid, units=f"{secs} s audio",
                note=f"Scribe v2 on the cut audio, {C.SCRIBE_RATE_SOURCE}"
                     + tail,
                ref=C.call_ref(run, tfile, secs)))
    return rows, max(seen_epochs or [0])


def from_renders(run: Path) -> list[dict]:
    rows = []
    for p in sorted(glob.glob(str(run / "gen" / "_rc_*.json"))):
        d = _load(p)
        for r in (d.get("results") or []):
            ren = (r or {}).get("render") or {}
            if not ren.get("measured_cost_usd"):
                continue
            job = r.get("job") or {}
            probe = ren.get("probe") or {}
            rows.append(dict(
                service="modal", stage="render",
                usd=float(ren["measured_cost_usd"]), video=job.get("vid"),
                fmt=job.get("fmt") or None,
                units=(f"{ren.get('billed_container_seconds')} container-s x "
                       f"{ren.get('cores')} cores, {probe.get('frames')}f "
                       f"{probe.get('width')}x{probe.get('height')}"),
                note=f"render of {ren.get('name')} "
                     f"(report {Path(p).name})",
                ref=C.call_ref(run, ren.get("output"),
                               ren.get("t_import_epoch"))))
    return rows


def _tokens(calls: list) -> str:
    tin = sum((c or {}).get("input_tokens") or 0 for c in calls)
    tout = sum(((c or {}).get("output_tokens") or 0)
               + ((c or {}).get("thinking_tokens") or 0) for c in calls)
    return f"{tin:,} in / {tout:,} out tokens over {len(calls)} calls"


def from_watchers(run: Path) -> list[dict]:
    rows = []
    for pat, stage, what in (("cands_*.json", "watch", "post-render watcher"),
                             ("clerk_cands_*.json", "clerk_watch",
                              "clerk duplicate re-watch (retired v3.1)"),
                             ("flagcheck_*.json", "verify",
                              "flag verification")):
        for p in sorted(glob.glob(str(run / "review" / pat))):
            if pat == "cands_*.json" and Path(p).name.startswith("clerk_"):
                continue
            d = _load(p)
            if not d.get("cost_usd"):
                continue
            rounds = re.search(r"\.prior(\d+)\.", Path(p).name)
            rows.append(dict(
                service="gemini", stage=stage, usd=float(d["cost_usd"]),
                video=d.get("video_id"), fmt=d.get("fmt") or None,
                units=_tokens(d.get("calls") or []),
                note=f"{what}, {d.get('model')}"
                     + (f", fix round {rounds.group(1)}" if rounds else ""),
                ref=C.rel(run, p)))
    return rows


def from_gate3(run: Path) -> list[dict]:
    rows = []
    for p in sorted(glob.glob(str(run / "gen" / "_qcpass_*.json"))):
        d = _load(p)
        g = (d.get("checks") or {}).get("gate3_gemini_describe") or {}
        cost = g.get("cost_usd")
        blob = {}
        if cost is None and g.get("stdout"):
            s = g["stdout"]
            try:
                blob = json.loads(s[s.index("{"):])
                cost = blob.get("cost_usd")
            except Exception:                                    # noqa: BLE001
                cost = None
        if not cost:
            continue
        u = blob.get("usage") or g.get("usage") or {}
        rows.append(dict(
            service="gemini", stage="gate3", usd=float(cost),
            video=d.get("vid"), fmt=d.get("fmt") or None,
            units=(f"{u.get('in', '?')} in / "
                   f"{(u.get('out') or 0) + (u.get('thoughts') or 0)} out "
                   f"tokens over {u.get('calls', '?')} calls"),
            note=f"Gate 3 describe-mode QC, "
                 f"{blob.get('model') or g.get('model') or 'gemini'} "
                 f"({Path(p).name})",
            ref=C.rel(run, p)))
    return rows


def from_sessions(run: Path, vids: set[str], since: float) -> list[dict]:
    """Every SAM2 container this run's videos ever paid for, including the ones
    no prep package knows about: the chair job, exclusion-object experiments,
    hand re-tracks during a fix round.  Matched by session name, filtered by
    the container's own start epoch so an older run's record is not adopted."""
    rows = []
    for sess in sorted(SESSIONS.iterdir() if SESSIONS.is_dir() else []):
        if not sess.is_dir():
            continue
        base = sess.name
        for v in sorted(vids, key=len, reverse=True):
            if base == v or base.startswith(v + "_"):
                base = v
                break
        else:
            continue
        for p in sorted(sess.glob("run_*.json")):
            rec = _load(p)
            usd = rec.get("measured_cost_usd")
            epoch = rec.get("t_import_epoch") or 0
            if not usd or epoch < since:
                continue
            extra = "" if sess.name == base else f", session {sess.name}"
            rows.append(dict(
                service="modal", stage="track", usd=float(usd), video=base,
                units=(f"{rec.get('billed_container_seconds')} container-s "
                       f"{_lane(rec.get('gpu'))} over "
                       f"{rec.get('frames_tracked')} frames"),
                note=f"SAM2 track, tag {rec.get('tag')}{extra}",
                ref=C.call_ref(run, p, epoch)))
            if rec.get("ship_cost_usd"):
                rows.append(dict(
                    service="modal", stage="ship",
                    usd=float(rec["ship_cost_usd"]), video=base,
                    units=f"{rec.get('ship_seconds')} s ship",
                    note=f"matte ship spawned by the track, "
                         f"tag {rec.get('tag')}{extra}",
                    ref=C.call_ref(run, p, f"ship{rec.get('ship_seconds')}")))
    return rows


def from_intake(run: Path) -> list[dict]:
    rows = []
    # the transcript is named after the RECORDING, so the recording -> id map
    # out of the prep packages is what puts intake's Scribe on a video's line
    by_rec = {}
    for q in sorted(glob.glob(str(run / "prep" / "*.json"))):
        pkg = _load(q)
        if pkg.get("recording") and pkg.get("id"):
            by_rec.setdefault(str(pkg["recording"]), pkg["id"])
    for p in sorted(glob.glob(str(run / "intake" / "transcripts" / "*.json"))):
        secs = _load(p).get("audio_duration_secs")
        if not secs:
            continue
        rows.append(dict(
            service="elevenlabs", stage="scribe", usd=C.scribe_usd(secs),
            video=by_rec.get(Path(p).stem), units=f"{secs} s audio",
            note=f"intake Scribe v2 on the raw recording "
                 f"{Path(p).stem}, {C.SCRIBE_RATE_SOURCE}",
            ref=C.call_ref(run, p, secs)))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--since", type=float, default=None,
                    help="ignore sam2 containers that started before this "
                         "epoch (default: the run's own earliest container "
                         "minus 30 min)")
    a = ap.parse_args()
    run = C.resolve_run(a.run)

    prep_rows, latest = from_prep(run)
    vids = {r["video"] for r in prep_rows if r.get("video")}
    if not vids:                       # a run with no prep packages
        vids = {Path(p).name for p in glob.glob(str(run / "cuts" / "*"))}
    earliest = min([e for e in
                    [_load(x).get("t_import_epoch")
                     for x in glob.glob(str(run / "gen" / "_birefnet_*.json"))]
                    if e] or [0])
    since = a.since if a.since is not None else (
        (earliest - 1800) if earliest else 0)

    groups = {
        "prep (sweep/track/ship/scribe)": prep_rows,
        "renders": from_renders(run),
        "gemini watchers": from_watchers(run),
        "gate 3": from_gate3(run),
        "sam2 sessions (chair job, hand re-tracks)":
            from_sessions(run, vids, since),
        "intake scribe": from_intake(run),
    }
    allrows: list[dict] = []
    for name, rows in groups.items():
        print(f"{name:<44} {len(rows):>3} row(s)  "
              f"${round(sum(r['usd'] for r in rows), 4)}")
        allrows += rows

    keys = {C.make_key(r["service"], r["stage"], r.get("video"),
                       r.get("fmt"), r.get("ref")) for r in allrows}
    print(f"{'-' * 44} {len(allrows):>3} row(s)  "
          f"${round(sum(r['usd'] for r in allrows), 4)}  "
          f"({len(keys)} distinct key(s))")
    if a.dry_run:
        return 0
    n = C.record_many(run, allrows)
    print(f"wrote {n} row(s) -> {run / C.LEDGER_NAME}  "
          f"(ledger total ${C.total(run)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
