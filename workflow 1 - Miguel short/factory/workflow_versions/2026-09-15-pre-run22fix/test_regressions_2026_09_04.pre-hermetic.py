#!/usr/bin/env python
"""Regression checks for the three run-14 prep failures.

Run: ~/Documents/Workspace/.venv/bin/python pipeline/prep/test_regressions_2026_09_04.py

Each of these was a real failure that cost a paid run or blocked a lane.  They
are asserted against the RUN-14 CASE ITSELF, with the numbers in the assertion,
so a future edit that reintroduces the bug fails here instead of in a batch.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

F = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "pipeline" / "sam2"))
sys.path.insert(0, str(F / "pipeline" / "matting"))

FAILED: list[str] = []


def check(name: str, fn) -> None:
    try:
        fn()
        print(f"  PASS  {name}")
    except Exception as exc:                                  # noqa: BLE001
        FAILED.append(f"{name}: {type(exc).__name__}: {exc}")
        print(f"  FAIL  {name}: {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------
# 1. game33c — an INNER discard marker is a stumble, not a false start
# ---------------------------------------------------------------------------
def t_inner_marker():
    from prep import cutlib
    tp = (F / "shorts_run14/intake/transcripts/2026-09-03 15-28-15.json")
    if not tp.exists():
        raise RuntimeError(f"fixture missing: {tp}")
    d = json.loads(tp.read_text())
    ws = d["words"] if isinstance(d, dict) and "words" in d else d
    ws = [w for w in ws if w.get("type", "word") == "word"]
    mk = cutlib.discard_markers(ws)
    assert mk == [2, 62, 85, 124], f"marker set moved: {mk}"
    rec = cutlib.detect_take(
        ws, sign_off_key=("catch", "you", "in", "the", "next"),
        opening_families=[
            ("you", "can", "now", "create", "your", "own", "3d", "game",
             "for", "only", "33", "cents"),
            ("you", "can", "now", "create", "a", "3d", "game", "for",
             "only", "33", "cents")])
    assert rec["take_word_index"] == 86, f"take moved to w{rec['take_word_index']}"
    # the marker rule must WITNESS the opening off w85, not disagree off w124
    mr = rec["cross_check_marker_rule"]
    assert mr.get("verdict") == "equality", mr
    assert rec["markers_before_keeper"] == [2, 62, 85], rec["markers_before_keeper"]
    inner = rec["inner_markers"]
    assert [m["index"] for m in inner] == [124], inner
    assert inner[0]["text"] == "thrir--", inner[0]
    assert "33" in inner[0]["context"], inner[0]["context"]


# ---------------------------------------------------------------------------
# 2. trycrm — a bytes field must never lose a paid track
# ---------------------------------------------------------------------------
def t_json_safe():
    import track
    rec = {"a": 1, "alpha_preheal": b"\x00" * 10,
           "nest": {"b": b"xy", "c": [b"z", 3]}}
    out = track.json_safe(rec)
    json.dumps(out)                                   # must not raise
    assert out["alpha_preheal"].endswith("bytes dropped from the record>")
    assert out["nest"]["c"][0].startswith("<")
    assert out["a"] == 1 and out["nest"]["c"][1] == 3
    # and the driver must POP the three known blobs by name
    src = (F / "pipeline/sam2/track.py").read_text()
    for key in ('rec.pop("alpha"', 'rec.pop("alpha_exclude"',
                'rec.pop("alpha_preheal"'):
        assert key in src, f"track.py no longer pops {key}"


def t_ship_recovery():
    """prep_batch's ship stage must rebuild a missing run record from disk."""
    src = (F / "pipeline/prep/prep_batch.py").read_text()
    assert "def recover_run_record" in src, "the recovery helper is gone"
    calls = [ln for ln in src.splitlines()
             if "recover_run_record(" in ln and not ln.strip().startswith("def ")]
    assert calls, "recover_run_record is defined but never called"
    assert any("session, tag" in c for c in calls), calls


# ---------------------------------------------------------------------------
# 3. grokbuild — a gate refusal on a side with no chair object must self-heal
#    with a derived exclusion prompt BEFORE wingfix
# ---------------------------------------------------------------------------
def t_chair_from_refusal():
    """The derivation must ACCEPT trycrm's real wing and REJECT grokbuild's.

    Both were verified by eye on the plates on 2026-09-04:
      * trycrm  RIGHT — the protrusion gate names x781-857, and that IS the
        chair's right wing held inside the mask.  A prompt must come out.
      * grokbuild RIGHT — the outline gate names cut column 494 with the
        silhouette edge at 769, i.e. a 275 px "wedge", and the dark inside the
        mask there is HIS OWN BEARD, LIPS, JAW AND NECK with the chair
        correctly excluded outside the edge.  A prompt must NOT come out: this
        is the guard that stops the self-heal carving a face, and two wingfix
        rounds had already carved his neck before it was caught.
    """
    import chairprompt
    assert hasattr(chairprompt, "from_refusal"), "from_refusal is gone"

    def sess(v):
        S = F / "pipeline/sam2/sessions" / v
        if not (S / "plate_wide_25.mp4").exists():
            raise RuntimeError(f"{v} session missing; cannot assert the case")
        b = S / "prompts" / "_original" / "birefnet_00000.png"
        return S, (b if b.exists() else S / "prompts" / "birefnet_00000.png")

    S, body = sess("trycrm")
    ok = chairprompt.from_refusal(S / "plate_wide_25.mp4", body, side="right",
                                 rows=(180, 470), wing_cols=(781, 857),
                                 gate="protrusion")
    assert ok.get("found"), f"trycrm's real right wing was rejected: {ok.get('why')}"
    x0, y0, x1, y1 = ok["box"]
    assert 760 <= x0 <= 790 and 850 <= x1 <= 880, f"box drifted: {ok['box']}"
    assert y1 - y0 >= 80, f"box too short: {ok['box']}"
    assert ok["width"] == 77, ok["width"]
    pos = [q for q in ok["points"] if q[2] == 1]
    neg = [q for q in ok["points"] if q[2] == 0]
    assert len(pos) >= 3 and len(neg) >= 2, (len(pos), len(neg))
    assert ok["luma"]["mean"] < 40, ok["luma"]
    assert ok["source"].startswith("derived from the protrusion gate"), ok["source"]

    S, body = sess("grokbuild")
    no = chairprompt.from_refusal(S / "plate_wide_25.mp4", body, side="right",
                                  rows=(289, 489), cut_column=494,
                                  gate="outline")
    assert not no.get("found"), \
        f"grokbuild's FALSE-POSITIVE window produced a prompt: {no.get('box')}"
    assert no.get("verdict") == "not a wing", no
    assert no.get("width") == 275, no.get("width")
    assert "NOT another cut" in no["why"], no["why"]


def t_repair_tries_chair_first():
    src = (F / "pipeline/prep/prep_batch.py").read_text()
    assert "chair_from_gate" in src, "the chair-first repair branch is gone"
    i, j = src.index("def repair_round"), src.index("def auto_repair")
    body = src[i:j]
    assert "chair_from_gate" in body, "repair_round no longer tries the chair route"
    assert body.index("chair_from_gate") < body.index("wing_args("), \
        "wingfix is being tried BEFORE the chair object"


def t_outline_longest_flat_counterexample():
    """AUDIT A4's reproduced 70-row near-vertical edge."""
    import numpy as np
    import outline
    v = np.array([100] + [101] * 35 + [102] * 35)
    got = outline._longest_flat(v, 1)
    assert got == (70, 1), f"valid 70-row suffix undercounted as {got}"


def t_outline_missing_measurements_fail_closed():
    """AUDIT A5: empty/truncated evidence is UNMEASURABLE, never clean."""
    import numpy as np
    import outline
    alpha = np.zeros((4, 900, 400), np.uint8)
    same = np.zeros_like(alpha)
    empty_alpha = outline.scan(alpha, same)
    assert empty_alpha["verdict"] == "unmeasurable", empty_alpha
    assert empty_alpha["sides"]["left"]["measured"] == 0, empty_alpha
    assert empty_alpha["sides"]["right"]["measured"] == 0, empty_alpha
    assert any("no measurable LAW 48 band" in e
               for e in empty_alpha["measurement_errors"]), empty_alpha

    missing_plate = outline.scan(alpha, same[:0])
    assert missing_plate["verdict"] == "unmeasurable", missing_plate
    assert missing_plate["frames"] == 0, missing_plate
    assert missing_plate["alpha_frames"] == 4, missing_plate
    assert missing_plate["plate_frames"] == 0, missing_plate
    assert any("frame-count mismatch" in e
               for e in missing_plate["measurement_errors"]), missing_plate

    # The shipper must refuse the report before render, even if a caller supplied
    # an outline override.  Missing evidence cannot be waived into existence.
    import ship
    old_protrusion = ship.protrusion_gate
    old_outline = ship.outline_gate
    try:
        ship.protrusion_gate = lambda *a, **k: {"verdict": "clean",
                                                "windows": [], "wings": []}
        ship.outline_gate = lambda *a, **k: missing_plate
        try:
            ship.ship_all(alpha=Path("missing-alpha"), plate=Path("missing-plate"),
                          out_stem=Path("never-rendered"),
                          plate_src=Path("missing-plate"),
                          allow_outline="must not bypass missing evidence")
        except ship.ShipRefused as exc:
            assert exc.gate == "outline_measurement", exc.gate
            assert "UNMEASURABLE, never clean" in exc.message, exc.message
        else:
            raise AssertionError("ship_all accepted an unmeasurable outline")
    finally:
        ship.protrusion_gate = old_protrusion
        ship.outline_gate = old_outline


def t_game33c_temporal_chair_support():
    """2026-09-05 flicker: obj3 loses a chair region, then reacquires it."""
    import importlib.util
    import cv2
    import numpy as np

    app_path = F / "pipeline/sam2/modal_app.py"
    spec = importlib.util.spec_from_file_location("sam2_modal_regression", app_path)
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)

    session = F / "pipeline/sam2/sessions/game33c"
    # The fixed chair-support window: right object, inside the proven luma fence.
    # Cropping keeps this regression under 25 MB instead of stacking 350 full
    # 1620x900 masks in the laptop test process.
    ys, xs = slice(184, 428), slice(980, 1200)
    cap = cv2.VideoCapture(str(session / "alpha_v2_exclude.mkv"))
    raw = []
    for _ in range(350):
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        raw.append(gray[ys, xs] > 127)
    cap.release()
    assert len(raw) == 350, len(raw)
    support, rec = app.temporal_exclusion_support(
        raw, rows=(0, 244), fraction=0.20)
    assert rec["vote_threshold"] == 70, rec
    assert rec["support_px"] > 10_000, rec
    # The tracker sees q=2 JPEG luma.  A chair pixel at 61 there can be 59 in
    # the MP4 that ships, so the measured +10 codec headroom must include it.
    base = np.zeros_like(support)
    jpeg_luma = np.full_like(support, 61, dtype=np.uint8)
    # `reach=0` turns OFF the 2026-09-05 skin fence so this stays a test of the
    # codec headroom alone; the fence has its own test below.
    no_slack, n0 = app.apply_temporal_support(
        base, support, jpeg_luma, luma_max=60, slack=0, reach=0)
    with_slack, n1 = app.apply_temporal_support(
        base, support, jpeg_luma, luma_max=60, slack=10, reach=0)
    assert n0 == 0 and not no_slack.any(), (n0, int(no_slack.sum()))
    assert n1 == int(support.sum()) and np.array_equal(with_slack, support), n1

    alpha = cv2.VideoCapture(str(session / "alpha_v2.mkv"))
    plate = cv2.VideoCapture(str(session / "plate_wide_25.mp4"))
    before, after = {}, {}
    for f in (100, 110, 120, 125, 130):
        alpha.set(cv2.CAP_PROP_POS_FRAMES, f)
        plate.set(cv2.CAP_PROP_POS_FRAMES, f)
        oka, af = alpha.read()
        okp, pf = plate.read()
        assert oka and okp, f
        am = cv2.cvtColor(af, cv2.COLOR_BGR2GRAY)[ys, xs] > 127
        lum = cv2.cvtColor(pf, cv2.COLOR_BGR2GRAY)[ys, xs]
        residue = am & (lum < 60) & support
        before[f] = int(residue.sum())
        after[f] = int((residue & ~support).sum())
    alpha.release()
    plate.release()
    assert int(np.median([before[f] for f in (100, 110, 120, 125)])) >= 250, before
    assert before[130] <= 5, before       # the old mask abruptly catches up at 5.2 s
    assert max(after.values()) == 0, after

    # The next failure in the same fix loop: ship.post.fill_holes resurrected
    # the tracked-out chair after the alpha was clean.  On the saved f100 it
    # adds more than 100 dark pixels; guarded_polish must keep all of them zero.
    import post
    import ship
    stable = cv2.VideoCapture(str(session / "alpha_v3_stable.mkv"))
    guard_cap = cv2.VideoCapture(str(session / "alpha_v3_guard.mkv"))
    plate_cap = cv2.VideoCapture(str(session / "plate_wide_25.mp4"))
    for cap2 in (stable, guard_cap, plate_cap):
        cap2.set(cv2.CAP_PROP_POS_FRAMES, 100)
    oks, sf = stable.read()
    okg, gf = guard_cap.read()
    okp, pf = plate_cap.read()
    for cap2 in (stable, guard_cap, plate_cap):
        cap2.release()
    assert oks and okg and okp
    sg = cv2.cvtColor(sf, cv2.COLOR_BGR2GRAY)
    guard = cv2.cvtColor(gf, cv2.COLOR_BGR2GRAY) > 127
    lum = cv2.cvtColor(pf, cv2.COLOR_BGR2GRAY)
    filled = post.spatial(sg) > 0.5
    resurrected = int((filled & guard & (lum < 60)).sum())
    assert resurrected >= 100, resurrected
    protected = filled.copy()
    protected[guard] = False
    polished, _ = ship.guarded_polish(protected, guard)
    assert int(((polished > 0.5) & guard).sum()) == 0

    src = app_path.read_text()
    assert src.count("temporal_exclusion_support(") >= 2, \
        "the tested helper is no longer called by the deployed track"
    assert "got_effective[loc(g)].tobytes()" in src, \
        "the exclusion diagnostic no longer writes the effective mask"
    prep_src = (F / "pipeline/prep/prep_batch.py").read_text()
    assert 'cmd += ["--exclusion-guard", str(guard)]' in prep_src, \
        "local prep ship no longer passes the effective exclusion guard"
    assert "exclusion_on_volume=(str(dest2) if dest2 else None)" in src, \
        "remote ship no longer receives the effective exclusion guard"
    ship_src = (F / "pipeline/sam2/ship.py").read_text()
    assert "guarded_polish(am > 0.5, guard)" in ship_src, \
        "ship no longer reapplies the guard after the temporal median"


# ---------------------------------------------------------------------------
# game33c round 2 — NO REPAIR MAY REMOVE SKIN (2026-09-05)
# ---------------------------------------------------------------------------
def t_game33c_no_repair_removes_skin():
    """The chair support ate his beard, jaw and hairline; two rules stop it.

    The delivered v3 cut-out had the chair gone on all 691 frames AND enclosed
    cream holes inside his face up to 940 px (prior render: 46 px), sustained
    8.48-8.88 s.  Cause: a carried chair support gated on DARKNESS alone.  This
    asserts the fence, the hole refill, the ship gate, and the measured result
    on the session's own saved masks.
    """
    import importlib.util
    import cv2
    import numpy as np

    app_path = F / "pipeline/sam2/modal_app.py"
    spec = importlib.util.spec_from_file_location("sam2_modal_skin", app_path)
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)
    import ship

    # --- 1. the fence itself.  A support pixel is a BRIDGE, not a claim. -----
    base = np.zeros((80, 80), bool)
    base[10:20, 10:20] = True              # this frame's own chair evidence
    support = np.zeros((80, 80), bool)
    support[22:26, 12:16] = True           # 2 px away  -> a bridge
    support[60:64, 60:64] = True           # ~45 px away -> a free-standing claim
    dark = np.zeros((80, 80), np.uint8)    # everything is dark
    got, n = app.apply_temporal_support(base, support, dark, luma_max=60,
                                        slack=10, reach=20)
    assert n == 16, n
    assert got[22:26, 12:16].all(), "the bridge over the gap was refused"
    assert not got[60:64, 60:64].any(), "a free-standing support claim survived"
    # no evidence at all on this frame -> the support claims nothing
    empty, n2 = app.apply_temporal_support(np.zeros((80, 80), bool), support,
                                           dark, luma_max=60, slack=10, reach=20)
    assert n2 == 0 and not empty.any(), n2
    assert app.EXCL_TEMPORAL_REACH == 20, app.EXCL_TEMPORAL_REACH

    # --- 2. an exclusion may not leave a hole INSIDE him ---------------------
    body = np.zeros((60, 60), bool)
    body[10:50, 10:50] = True
    guard = np.zeros((60, 60), bool)
    guard[20:25, 20:25] = True             # fully enclosed by the body
    guard[10:14, 10:14] = True             # a corner bite, legitimately outside
    safe, given = ship.skin_safe_guard(body, guard)
    assert given == 25, given
    assert not safe[20:25, 20:25].any(), "the enclosed bite survived"
    assert safe[10:14, 10:14].all(), "an outside bite was wrongly given back"
    assert not ship.interior_holes(body & ~safe).any()

    # a hole nowhere near the guard is a tracker artefact, not a repair
    holes = np.zeros((60, 60), bool)
    holes[30:33, 30:33] = True
    assert ship.holes_from(holes, np.zeros((60, 60), bool)) == 0
    assert ship.holes_from(holes, guard) == 0
    touching = np.zeros((60, 60), bool)
    touching[29, 29] = True
    assert ship.holes_from(holes, touching) == 9

    # --- 3. the measured result on the saved game33c masks -------------------
    session = F / "pipeline/sam2/sessions/game33c"
    for name in ("alpha_v3_stable.mkv", "alpha_v3_guard.mkv", "alpha_v4.mkv",
                 "alpha_v4_guard.mkv"):
        if not (session / name).exists():
            raise RuntimeError(f"fixture missing: {session / name}")
    caps = {n: cv2.VideoCapture(str(session / f"alpha_{n}.mkv"))
            for n in ("v3_stable", "v3_guard", "v4", "v4_guard")}
    worst_old = worst_new = 0
    try:
        for f in (212, 214, 216, 218, 220, 222):
            g = {}
            for n, c in caps.items():
                c.set(cv2.CAP_PROP_POS_FRAMES, f)
                ok, fr = c.read()
                assert ok, (n, f)
                g[n] = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY) > 127
            old = g["v3_stable"] & ~g["v3_guard"]
            new = g["v4"]
            worst_old = max(worst_old,
                            ship.holes_from(ship.interior_holes(old),
                                            g["v3_guard"]))
            worst_new = max(worst_new,
                            ship.holes_from(ship.interior_holes(new),
                                            g["v4_guard"]))
    finally:
        for c in caps.values():
            c.release()
    assert worst_old > 300, f"the v3 defect no longer reproduces: {worst_old}"
    assert worst_new == 0, f"the repaired matte still holes his face: {worst_new}"

    # --- 4. the ship gate refuses the old numbers and passes the new ---------
    bad = ship.presenter_loss_verdict([], [0] * 691, [940] * 691, [940] * 691)
    assert bad["verdict"] == "refused" and bad["refusals"], bad
    assert "940" in bad["refusals"][0], bad
    good = ship.presenter_loss_verdict([12], [0] * 691, [56] * 691, [0] * 691)
    assert good["verdict"] == "clean", good     # 56 px, but none of it the guard's
    skin = ship.presenter_loss_verdict([], [61] * 691, [0] * 691, [0] * 691)
    assert skin["verdict"] == "refused", skin
    assert "luma >= 110" in skin["refusals"][0], skin

    # --- 5. the delivered evidence, as measured -----------------------------
    series = json.loads(
        (F / "shorts_run14/review/facehole_game33c_series.json").read_text())
    d = series["delivered"]["measured"]
    assert d["v3"]["max"] >= 900 and d["v3"]["over300"] == 11, d["v3"]
    assert d["new"]["over300"] == 0 and d["new"]["max"] <= 60, d["new"]
    assert d["prior"]["max"] <= 50, d["prior"]
    assert series["whole"]["new"]["notch"]["max"] <= 50, series["whole"]["new"]
    assert series["whole"]["v3"]["notch"]["max"] > 1000, series["whole"]["v3"]

    # --- 6. the rule is still WIRED, not just present ------------------------
    src = app_path.read_text()
    assert 'reach=e["temporal_reach"]' in src, \
        "the deployed track no longer passes the support reach"
    assert "enclosed_holes(got[fi] > 127) & union" in src, \
        "the deployed track no longer hands back holes inside the presenter"
    ship_src = (F / "pipeline/sam2/ship.py").read_text()
    assert "skin_safe_guard(body, guard)" in ship_src, \
        "ship no longer corrects a guard that would hole the presenter"
    assert 'raise ShipRefused(presenter_loss_message(pl), rec, "presenter_loss")' \
        in ship_src, "ship no longer REFUSES on presenter loss"
    refit = (F / "pipeline/sam2/support_refit.py").read_text()
    assert "from modal_app import" in refit, \
        "support_refit no longer imports the deployed rule"


def _grokbuild_law48() -> dict:
    """The untouched v1 refusal, before the two harmful historical carves."""
    hist = json.loads((F / "shorts_run14/prep/grokbuild.json").read_text())
    law = dict(hist["stages"]["repair"]["rounds"][0]["outline"])
    import outline
    law["cfg"] = dict(outline.OUTLINE)
    return law


def _grokbuild_pkg() -> dict:
    return {
        "id": "grokbuild",
        "session": str(F / "pipeline/sam2/sessions/grokbuild"),
        "cut_dir": str(F / "shorts_run14/cuts/grokbuild"),
        "run": str(F / "shorts_run14"),
        "stages": {
            "track": {"status": "ok", "tag": "v1"},
            "ship": {"status": "REFUSED", "gate": "outline",
                     "gate_refusal": "grokbuild v1 LAW 48 replay"},
        },
    }


def t_not_a_wing_vetoes_outline_wingfix():
    """AUDIT A1: replay grokbuild and prove the carve call count is zero."""
    from prep import prep_batch
    law = _grokbuild_law48()
    pkg = _grokbuild_pkg()
    carved, shipped = [], []
    old_report = prep_batch.outline_report
    old_fix = prep_batch._run_fix
    old_ship = prep_batch.ship_matte
    try:
        prep_batch.outline_report = lambda *a, **k: law

        def forbidden_carve(*a, **k):
            carved.append((a, k))
            raise AssertionError("wingfix was called after verified anatomy")

        def fake_ship(p, run, *, tag, emit="v5", allow_outline=None):
            shipped.append({"tag": tag, "emit": emit,
                            "allow_outline": allow_outline})
            p["stages"]["ship"] = {"status": "ok",
                                    "protrusion_verdict": "clean"}

        prep_batch._run_fix = forbidden_carve
        prep_batch.ship_matte = fake_ship
        rd = prep_batch.repair_round(
            pkg, {}, F / "shorts_run14", r=1, base_tag="v1",
            gate="outline", gpu="h100", emit="v5", remote_ship=True,
            limit=None, stride=6, sweep_local=False)
    finally:
        prep_batch.outline_report = old_report
        prep_batch._run_fix = old_fix
        prep_batch.ship_matte = old_ship

    assert carved == [], f"a carve was attempted: {carved}"
    assert len(shipped) == 1, shipped
    assert shipped[0]["tag"] == "v1", "the unchanged alpha must ship"
    assert "straight p95 61.0" in shipped[0]["allow_outline"], shipped[0]
    assert "at-line 29.3%" in shipped[0]["allow_outline"], shipped[0]
    assert "dark p95 59.4%" in shipped[0]["allow_outline"], shipped[0]
    assert rd["outcome"] == "verified anatomy", rd
    assert rd["ship_status"] == "ok" and rd["tag"] == "v1", rd
    assert rd["cost_usd"] == 0.0 and "track_cmd" not in rd, rd

    # Add a second failing instrument: the same anatomy verdict may no longer
    # auto-waive, and the recording must be stamped needs_miguel.
    bad = json.loads(json.dumps(law))
    bad["sides"]["right"]["straight_frac_at_line"] = 0.50
    bad["refusals"][0]["straight_frac_at_line"] = 0.50
    bad["refusals"][0]["why"].append(
        "a straight run of >= 40 rows on 50.0% of frames (ceiling 45%)")
    pkg2 = _grokbuild_pkg()
    rd2 = prep_batch.finish_not_a_wing_round(
        pkg2, F / "shorts_run14",
        rd={"refused_verdict": "two-instrument outline replay"},
        gate="outline", law=bad, chair=rd["chair_from_gate"],
        prev_tag="v1", emit="v5")
    assert rd2["ship_status"] == "needs_miguel", rd2
    assert pkg2["stages"]["ship"]["status"] == "needs_miguel", pkg2
    assert "allow_outline" not in rd2 and "track_cmd" not in rd2, rd2


def t_not_a_wing_vetoes_protrusion_wingfix():
    """AUDIT A1: the protrusion branch also stops; it cannot auto-waive."""
    from prep import prep_batch
    pkg = _grokbuild_pkg()
    pkg["stages"]["ship"]["gate"] = "protrusion"
    scan = {
        "verdict": "wing", "windows": [],
        "wings": [{"side": "right", "rows": [289, 489],
                   "x0": 494, "x1": 768, "width": 275,
                   "shoulder_ref": 489}],
    }
    carved, shipped = [], []
    old_scan = prep_batch.gate_scan
    old_fix = prep_batch._run_fix
    old_ship = prep_batch.ship_matte
    try:
        prep_batch.gate_scan = lambda *a, **k: scan
        prep_batch._run_fix = lambda *a, **k: carved.append((a, k))
        prep_batch.ship_matte = lambda *a, **k: shipped.append((a, k))
        rd = prep_batch.repair_round(
            pkg, {}, F / "shorts_run14", r=1, base_tag="v1",
            gate="protrusion", gpu="h100", emit="v5", remote_ship=True,
            limit=None, stride=6, sweep_local=False)
    finally:
        prep_batch.gate_scan = old_scan
        prep_batch._run_fix = old_fix
        prep_batch.ship_matte = old_ship

    assert carved == [], f"the protrusion branch attempted a carve: {carved}"
    assert shipped == [], "a protrusion refusal must never use --allow-outline"
    assert rd["outcome"] == "verified anatomy", rd
    assert rd["ship_status"] == "needs_miguel", rd
    assert pkg["stages"]["ship"]["status"] == "needs_miguel", pkg["stages"]["ship"]
    assert rd["cost_usd"] == 0.0 and "track_cmd" not in rd, rd



# ---------------------------------------------------------------------------
# run 16, plantsite (2026-09-06) — the cold reader had no dispatcher, so an
# UNREAD shared scene became a PASS and three lanes deadlocked on it.
#   * the artwork author had no agent-spawn verb: cold_reads_run 0,
#     blocking_before_render true, verdict PASS, nothing checked it
#   * four independent readers then named the shared peak object "flower",
#     never "a website about plants"
#   * split, whiteboard and cutout each returned no staged path, and none of
#     them was allowed to redraw the shared module
# Numbers below are this recording's own.
# ---------------------------------------------------------------------------
def _plantsite_reads():
    """The four real reads on the shared peak object, from run 16's evidence."""
    import json as _j
    rows = []
    for f, tag in (("coldread_plantsite_split_round1.json", "split r1"),
                   ("coldread_plantsite_split_round2.json", "split r2"),
                   ("coldread_plantsite_cutout_round1.json", "cutout r1")):
        fp = F / "shorts_run16/review" / f
        if fp.exists():
            for r in _j.loads(fp.read_text()).get("names", []):
                if r.get("i") == 1:
                    rows.append((tag, r.get("name"), r.get("confidence")))
    return rows


def t_run16_peak_object_read_flower():
    """The evidence on disk must still say the shared peak object read 'flower'."""
    rows = _plantsite_reads()
    assert rows, "run 16 plantsite cold-read evidence is missing"
    assert all(n == "flower" and c == "sure" for _, n, c in rows), rows
    # the sanctioned candidate, cold-read on the same crops
    cand = json.loads((F / "shorts_run16/review/coldread_plantsite_split_cand.json").read_text())
    names = {r["i"]: r["name"] for r in cand["names"]}
    assert names[0] == "flower" and names[1] == "laptop with flower", names


def t_run16_dispatch_failure_is_not_a_read(tmp=None):
    """A reader that never saw the image is refused, never scored.

    Run 16's split author dispatched the first round with paths RELATIVE to
    /tmp and two readers answered 'file not found'.  Those rows must not be
    scoreable."""
    import tempfile
    import production
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        ev = d / "reader.json"
        ev.write_text(json.dumps({
            "names": [{"i": 0, "path": "/x/00.png", "name": "", "confidence": "cannot tell"},
                      {"i": 1, "path": "/x/01.png", "name": "flower", "confidence": "sure"}],
            "dispatch_failures": [{"i": 0, "error": "the reader never saw the image: file not found"}]}))
        sc = d / "scores.json"
        sc.write_text(json.dumps({"objects": [{"i": 0, "verdict": "PASS", "reason": "x"},
                                              {"i": 1, "verdict": "PASS", "reason": "x"}]}))
        try:
            production.read_rows(ev, sc)
        except ValueError as e:
            assert "never saw the image" in str(e), e
        else:
            raise AssertionError("a dispatch failure was accepted as a read")


def t_run16_cold_read_parses_a_non_read():
    """cold_read._one turns 'file not found' and junk into dispatch errors."""
    import cold_read
    from unittest import mock

    class R:
        def __init__(self, out, rc=0):
            self.stdout, self.stderr, self.returncode = out, "", rc

    png = F / "shorts_run16/review/cold/26bb260e/01.png"
    assert png.exists(), png
    with mock.patch.object(cold_read.subprocess, "run", return_value=R("Error: file not found")):
        row = cold_read._one(1, png, None, 10)
    assert row["confidence"] == "cannot tell" and "never saw the image" in row["dispatch_error"], row
    with mock.patch.object(cold_read.subprocess, "run", return_value=R("sure, it is a flower")):
        row = cold_read._one(1, png, None, 10)
    assert "unparseable" in row["dispatch_error"], row
    with mock.patch.object(cold_read.subprocess, "run",
                           return_value=R('{"name":"flower","confidence":"pretty sure"}')):
        row = cold_read._one(1, png, None, 10)
    assert row["name"] == "flower" and row["confidence"] == "cannot tell", row
    with mock.patch.object(cold_read.subprocess, "run",
                           return_value=R('{"name":"a browser window with a big flower","confidence":"sure"}')):
        row = cold_read._one(1, png, None, 10)
    assert row.get("over_five_words") is True, row
    # and the real read, unchanged: index and crop hash travel with the row
    with mock.patch.object(cold_read.subprocess, "run",
                           return_value=R('{"name":"flower","confidence":"sure"}')):
        row = cold_read._one(1, png, None, 10)
    assert row == {"i": 1, "path": str(png), "name": "flower", "confidence": "sure",
                   "crop_sha256": row["crop_sha256"]}, row


def t_run16_unread_shared_scene_is_not_a_pass():
    """artwork-check refuses a scene with no cold-read record; artwork-pass
    refuses the plantsite peak object; a clean read seals and then goes stale."""
    import tempfile
    import production
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        run = d / "run"; (run / "review").mkdir(parents=True)
        module = d / "plantsite_scene.py"; module.write_text("# shared scene\n")
        handoff = d / "plantsite_scene_handoff.md"; handoff.write_text("# handoff\n")

        # 1. what actually happened: PASS with zero reads and no record
        try:
            production.check_artwork(run, "plantsite", module, handoff)
        except ValueError as e:
            assert "cold read" in str(e), e
        else:
            raise AssertionError("an unread shared scene passed artwork-check")

        # 2. the real reads: object 1 FAILS, so the scene cannot be sealed
        ev = d / "reader.json"
        ev.write_text(json.dumps({"names": [
            {"i": 0, "path": "/c/00.png", "name": "checklist clipboard", "confidence": "sure"},
            {"i": 1, "path": "/c/01.png", "name": "flower", "confidence": "sure"},
            {"i": 2, "path": "/c/02.png", "name": "calendar", "confidence": "sure"}]}))
        sc = d / "scores.json"
        sc.write_text(json.dumps({"objects": [
            {"i": 0, "verdict": "PASS", "reason": "the checklist"},
            {"i": 1, "verdict": "FAIL", "reason": "intended a website about plants; read flower"},
            {"i": 2, "verdict": "PASS", "reason": "the calendar"}]}))
        try:
            production.save_artwork(run, "plantsite", module, handoff, ev, sc)
        except ValueError as e:
            assert "failed object" in str(e).lower(), e
        else:
            raise AssertionError("a failed shared object was sealed")

        # 3. the seated replacement reads: the scene seals, and check passes.
        #    RUN 16 (kimiwork, 2026-09-06): on THREE independent rounds, not one.
        #    kimiwork's app window sealed on a single `sure` read and then read
        #    'Refrigerator' twice out of the next four reads of the same pixels.
        rounds = []
        for k in range(production.SEAL_ROUNDS):
            f = d / f"reader2_{k}.json"
            f.write_text(json.dumps({"names": [
                {"i": 0, "path": "/c2/00.png", "name": "checklist clipboard", "confidence": "sure"},
                {"i": 1, "path": "/c2/01.png", "name": "laptop with flower", "confidence": "sure"},
                {"i": 2, "path": "/c2/02.png", "name": "calendar", "confidence": "sure"}]}))
            rounds.append(str(f))
        sc2 = d / "scores2.json"
        sc2.write_text(json.dumps({"objects": [{"i": i, "verdict": "PASS", "reason": "read"}
                                               for i in (0, 1, 2)]}))
        try:
            production.save_artwork(run, "plantsite", module, handoff, rounds[0], sc2)
        except ValueError as e:
            assert "independent cold-read rounds" in str(e), e
        else:
            raise AssertionError("one draw of a stochastic reader sealed a shared scene")
        rec = production.save_artwork(run, "plantsite", module, handoff, ",".join(rounds), sc2)
        assert rec["objects"] == 3 and rec["verdict"] == "PASS" and rec["seal_rounds"] == 3, rec
        assert production.check_artwork(run, "plantsite", module, handoff)["objects"] == 3

        # 4. a repair round that edits the module invalidates the seal
        module.write_text("# shared scene, peak object reseated\n")
        try:
            production.check_artwork(run, "plantsite", module, handoff)
        except ValueError as e:
            assert "evidence changed" in str(e), e
        else:
            raise AssertionError("a stale shared-artwork seal passed")



# ---------------------------------------------------------------------------
# RUN 17 (eudisclosure, 2026-09-08) — "the gate agent never returned"
#
# The MATTE GATE returned NOTHING on all three spawn attempts and never wrote
# its started sentinel, while prep/stages/eudisclosure.ship.json had said
# "status": "ok" on disk since 00:45:23 with all three matte layers written.
# The workflow could not tell that apart from a refused encode and spent the
# recording's ONE repair round on it.  The gate's judgement is now
# deterministic python that ALWAYS answers.
# ---------------------------------------------------------------------------
def t_run17_gate_marker_reads_the_ok_ship_marker():
    from prep import gate_marker
    run = F / "shorts_run17"
    if not (run / "prep/stages/eudisclosure.ship.json").exists():
        raise RuntimeError("fixture missing: run 17 eudisclosure ship marker")
    # the BASE marker - the file the gate agent could not report - on its own
    over, main = gate_marker.marker_paths(run, "eudisclosure", "ship")
    base, state = gate_marker._load(main)
    assert state == "ok" and base["status"] == "ok", (state, base)
    assert base["keys"]["frames"] == 692, base["keys"]
    assert base["keys"]["ship_source_sha256"] == (
        "cf367be51d742c272d9f79db8a13e00297684001ebf666283095059206e149e7"), base["keys"]
    # and the gate over the whole stage, override applied or not
    st = gate_marker.gate(run, "eudisclosure", "ship")
    assert st["status"] == "ok" and gate_marker.passed(st), st
    assert st["final"] is False, st
    assert st["waited_s"] == 0.0, st          # an ok marker costs no wait at all
    assert st["override_used"] is over.is_file(), (st["override_used"], str(over))
    assert abs(st["track_cost_usd"] - 0.018519859643289158) < 1e-12, st
    assert sorted(st["outputs"]) == ["alpha", "cut", "rim"], st["outputs"]
    for layer in ("cut", "rim", "alpha"):
        assert Path(st["outputs"][layer]).is_file(), st["outputs"]
    assert "log_tail" not in st, "a passing gate does not carry the batch log"


def t_run17_gate_marker_never_returns_nothing():
    """Missing, truncated, refused and overridden markers all get an answer."""
    import tempfile
    from prep import gate_marker
    with tempfile.TemporaryDirectory() as td:
        run = Path(td)
        d = run / "prep" / "stages"
        d.mkdir(parents=True)

        # 1. no marker yet: "missing", never final, never an exception
        st = gate_marker.gate(run, "eudisclosure", "ship")
        assert st["status"] == "missing" and st["final"] is False, st

        # 2. mark_stage writes with write_text, which is NOT atomic, so a reader
        #    can catch a half-written file.  That is not a verdict.
        m = d / "eudisclosure.ship.json"
        m.write_text('{"id": "eudisclosure", "stage": "ship", "sta')
        st = gate_marker.gate(run, "eudisclosure", "ship")
        assert st["status"] == "unreadable" and st["final"] is False, st

        # 3. a REFUSED marker is reported verbatim, and it is still pollable
        m.write_text(json.dumps({"id": "eudisclosure", "stage": "ship",
                                 "status": "REFUSED",
                                 "keys": {"error": "edge clip at frame 12"}}))
        st = gate_marker.gate(run, "eudisclosure", "ship")
        assert st["status"] == "REFUSED" and st["final"] is False, st
        assert st["error"] == "edge clip at frame 12", st
        assert "log_tail" in st, st

        # 4. THE OVERRIDE WINS, without anyone remembering to look for it
        (d / "eudisclosure.ship.override.json").write_text(json.dumps(
            {"id": "eudisclosure", "stage": "ship", "status": "ok",
             "keys": {"repair_reason": "the matte was always good"}}))
        st = gate_marker.gate(run, "eudisclosure", "ship")
        assert st["status"] == "ok" and st["override_used"] is True, st
        assert gate_marker.passed(st), st

        # 5. SKIPPED_NEEDS_KEY is the only kind of word that ends the polling
        (d / "eudisclosure.ship.override.json").unlink()
        m.write_text(json.dumps({"id": "eudisclosure", "stage": "ship",
                                 "status": "SKIPPED_NEEDS_KEY", "keys": {}}))
        assert gate_marker.gate(run, "eudisclosure", "ship")["final"] is True


def t_run17_gate_marker_waits_in_python_not_in_an_agent():
    """--wait-s blocks in ONE command and returns the instant the marker lands."""
    import tempfile
    from prep import gate_marker
    with tempfile.TemporaryDirectory() as td:
        run = Path(td)
        d = run / "prep" / "stages"
        d.mkdir(parents=True)
        m = d / "eudisclosure.ship.json"
        m.write_text(json.dumps({"id": "eudisclosure", "stage": "ship",
                                 "status": "running", "keys": {}}))
        now = [0.0]
        polls = []

        def sleep(sec):
            polls.append(sec)
            now[0] += sec
            if len(polls) == 3:               # prep stamps the marker mid-wait
                m.write_text(json.dumps({"id": "eudisclosure", "stage": "ship",
                                         "status": "ok", "keys": {"frames": 692}}))

        st = gate_marker.gate(run, "eudisclosure", "ship", wait_s=570, poll_s=5,
                              _clock=lambda: now[0], _sleep=sleep)
        assert st["status"] == "ok" and st["waited_s"] == 15.0, (st, polls)
        assert len(polls) == 3, polls          # it did NOT wait out the deadline

        # a marker that never lands still returns, at the deadline, non-final
        m.write_text(json.dumps({"id": "eudisclosure", "stage": "ship",
                                 "status": "running", "keys": {}}))
        now[0] = 0.0
        st = gate_marker.gate(run, "eudisclosure", "ship", wait_s=10_000, poll_s=5,
                              _clock=lambda: now[0],
                              _sleep=lambda sec: now.__setitem__(0, now[0] + sec))
        assert st["status"] == "running" and st["final"] is False, st
        assert st["waited_s"] <= gate_marker.MAX_WAIT_S + 5, st


# ---------------------------------------------------------------------------
# RUN 17, cursorworkspace, 2026-09-08.  THE SECOND RECORDING OF THE SAME RUN.
# Its gate:ship agent also returned nothing, over prep/stages/cursorworkspace.
# ship.json which had said "status": "ok" since 00:35:38 with all three matte
# layers sha256-equal to ship_v5.json.  Two things came out of it.  (1) The
# fallback written that morning is ITSELF an agent, so one empty reader puts the
# workflow straight back in the trap: it is now retried (test_workflow.mjs).
# (2) Both repair agents proved the encode by hand-hashing the three webms
# against ship_v5.json, because gate_marker only checked is_file() - so an "ok"
# over a truncated or stale layer read "ok" and `outputs` quietly came back
# short.  That hand-check is now the rule: verify_outputs re-hashes, and a
# passing marker whose files disagree with its own manifest becomes
# `outputs_incomplete`, pollable, never final, never a lane.
# ---------------------------------------------------------------------------
def t_run17_ship_ok_is_only_as_good_as_its_layers():
    from prep import gate_marker
    run = F / "shorts_run17"
    m = run / "prep/stages/cursorworkspace.ship.json"
    if not m.exists():
        raise RuntimeError("fixture missing: run 17 cursorworkspace ship marker")
    base, state = gate_marker._load(m)
    assert state == "ok" and base["status"] == "ok", (state, base)
    assert base["keys"]["frames"] == 538, base["keys"]
    assert (base["keys"]["width"], base["keys"]["height"]) == (1386, 990), base["keys"]
    assert base["keys"]["ship_source_sha256"] == (
        "cf367be51d742c272d9f79db8a13e00297684001ebf666283095059206e149e7"), base["keys"]

    st = gate_marker.gate(run, "cursorworkspace", "ship")
    assert st["status"] == "ok" and gate_marker.passed(st), st
    assert st["final"] is False and st["waited_s"] == 0.0, st
    assert abs(st["track_cost_usd"] - 0.0165812557340256) < 1e-15, st
    assert sorted(st["outputs"]) == ["alpha", "cut", "rim"], st["outputs"]
    # the hand-check both repair agents did, now done by the gate itself
    assert st["outputs_verified"] == "ok", st
    man, mstate = gate_marker._load(
        run / "matting/cursorworkspace/ship_v5.json")
    assert mstate == "ok" and man["frames"] == 538, man
    assert man["hashes"]["cut"] == (
        "3a5568d8df7cfdf27df2f70985b7e1381914c7bdfca1a21af762c3f6236904dc"), man
    ver = gate_marker.verify_outputs(run, "cursorworkspace", "ship")
    assert ver["verified"] == "ok" and ver["bad"] == [], ver


def t_run17_a_broken_layer_is_not_a_pass():
    """An ok marker over a truncated/missing/stale layer must not ship a lane."""
    import shutil
    import tempfile
    from prep import gate_marker
    src = F / "shorts_run17/matting/cursorworkspace"
    with tempfile.TemporaryDirectory() as td:
        run = Path(td)
        d = run / "prep" / "stages"
        d.mkdir(parents=True)
        s = run / "matting" / "cursorworkspace"
        s.mkdir(parents=True)
        # this recording's real marker and real manifest, with stand-in layers
        shutil.copy(F / "shorts_run17/prep/stages/cursorworkspace.ship.json",
                    d / "cursorworkspace.ship.json")
        shutil.copy(src / "ship_v5.json", s / "ship_v5.json")
        man = json.loads((s / "ship_v5.json").read_text())
        assert sorted(man["hashes"]) == ["alpha", "cut", "rim"], man

        # 1. an ok marker with NO layers at all is not a pass
        st = gate_marker.gate(run, "cursorworkspace", "ship")
        assert st["status"] == "outputs_incomplete", st
        assert st["marker_status"] == "ok" and st["final"] is False, st
        assert not gate_marker.passed(st) and st["outputs"] == {}, st
        assert len(st["outputs_bad"]) == 3, st

        # 2. layers that exist but are NOT the encode's own bytes: still not a pass
        for layer in ("cut", "rim", "alpha"):
            (s / f"matte_cursorworkspace_v5_{layer}.webm").write_bytes(b"not the matte")
        st = gate_marker.gate(run, "cursorworkspace", "ship")
        assert st["status"] == "outputs_incomplete", st
        assert all("sha256 differs" in b for b in st["outputs_bad"]), st
        assert "ship_v5.json" in st["error"], st

        # 3. an EMPTY layer is named as empty, not as a hash difference
        (s / "matte_cursorworkspace_v5_rim.webm").write_bytes(b"")
        st = gate_marker.gate(run, "cursorworkspace", "ship")
        assert "rim: empty file" in st["outputs_bad"], st

        # 4. NO MANIFEST, NO DOWNGRADE.  Nothing to check against is not a defect,
        #    and the gate must never invent a failure out of a missing file.
        (s / "ship_v5.json").unlink()
        st = gate_marker.gate(run, "cursorworkspace", "ship")
        assert st["status"] == "ok" and gate_marker.passed(st), st
        assert st["outputs_verified"] == "no_manifest", st

        # 5. and a REAL layer set passes: the true bytes of this recording
        shutil.copy(src / "ship_v5.json", s / "ship_v5.json")
        for layer in ("cut", "rim", "alpha"):
            shutil.copy(src / f"matte_cursorworkspace_v5_{layer}.webm",
                        s / f"matte_cursorworkspace_v5_{layer}.webm")
        st = gate_marker.gate(run, "cursorworkspace", "ship")
        assert st["status"] == "ok" and st["outputs_verified"] == "ok", st
        assert sorted(st["outputs"]) == ["alpha", "cut", "rim"], st


# ---------------------------------------------------------------------------
# RUN 17, pcoverheat, 2026-09-08 — the confidence FLAG was gating the binary
# that the NOUN measures, and it held the cutout lane with nothing staged.
# ---------------------------------------------------------------------------
PCOVERHEAT_ROUNDS = [str(F / f"shorts_run17/review/phone_reader_pcoverheat_cutout_r{k}.json")
                     for k in (6, 7, 8, 9, 10, 11)]
PCOVERHEAT_SCORES = F / "shorts_run17/review/phone_scores_pcoverheat_cutout.json"


def _pcoverheat():
    """The six lane rounds and the author's scoring, exactly as they are on disk."""
    scores = json.loads(PCOVERHEAT_SCORES.read_text())
    names = []
    for path in PCOVERHEAT_ROUNDS:
        f = Path(path)
        if not f.exists():
            raise RuntimeError(f"fixture missing: {f}")
        names += json.loads(f.read_text())["names"]
    return scores["objects"], names


def t_run17_six_of_six_readers_named_the_download_arrow():
    """The evidence on disk: object 1 is unanimous and object 3 is not a hedge.

    `phone_pcoverheat_cutout/01.png` is an arrow onto a bar.  Every one of six
    independent readers named it a download arrow; two said `sure`.  Object 3
    is a table headed PROCESSES with HOT / RAM / CPU columns: three readers
    answered by DECLINING the prompt's "everyday OBJECT" premise - `none - UI
    table, not object` - and named the panel anyway, in six words."""
    objects, names = _pcoverheat()
    reads1 = [n for n in names if n["i"] == 1]
    assert len(reads1) == 6, reads1
    assert all("download" in n["name"].lower() for n in reads1), reads1
    assert sum(1 for n in reads1 if n["confidence"] == "sure") == 2, reads1
    reads3 = [n for n in names if n["i"] == 3]
    assert sum(1 for n in reads3 if n["name"].lower().startswith("none")) == 3, reads3
    assert sum(1 for n in reads3 if len(n["name"].split()) > 5) == 3, reads3


def t_run17_the_noun_is_the_measurement_not_the_flag():
    """consensus rules on all four pcoverheat objects, on the numbers on disk.

    Before the fix objects 1 and 3 both raised "only 2 of 6 independent readers
    were sure" and the cutout lane returned staged "" - a gate reading `cutout:
    no staged path` for a drawing six of six readers had named correctly."""
    import production
    objects, names = _pcoverheat()
    got = {row["i"]: production.consensus(row, [n for n in names if n["i"] == row["i"]])
           for row in objects}
    # SUBSET, NOT EXACT EQUALITY (2026-09-15): consensus later gained `hedged`
    # and `clerk_must_adjudicate`, and whole-dict equality failed on the new
    # fields while the numbers this test is about were all correct.
    def has(got, want):
        assert {k: got[k] for k in want} == want, got
    has(got[0], {"i": 0, "reads": 6, "sure": 5, "agreed": 5, "sure_agreed": 5,
                 "different": 1, "single_sample": False})
    # the download arrow: 2 of 6 sure, 6 of 6 named it, zero different
    has(got[1], {"i": 1, "reads": 6, "sure": 2, "agreed": 6, "sure_agreed": 2,
                 "different": 0, "single_sample": False})
    assert got[2]["agreed"] == 6 and got[2]["sure_agreed"] == 6, got[2]
    # the process list: one `computer` inside the misread window, and its one
    # `sure` read that reached it (`table`) is the whole floor it clears
    has(got[3], {"i": 3, "reads": 6, "sure": 2, "agreed": 5, "sure_agreed": 1,
                 "different": 1, "single_sample": False})


def t_run17_the_confidence_floor_did_not_vanish():
    """One `sure` read that REACHED the object, or it still fails.

    The floor moved from half to one; it was not removed.  Three refusals that
    must survive any future edit, all built off pcoverheat's own object 1:
      * every reader hedging -> fail (kimiwork's presentation screen rule);
      * the only `sure` read naming a DIFFERENT thing -> fail, because a
        confidently wrong reader is not evidence that the drawing reads;
      * the only `sure` read overrunning the five-word cap -> fail, because a
        six-word answer is not a clean identification.
    And a second reader naming a different object still fails ahead of all of
    them, whatever the flags say."""
    import production
    objects, names = _pcoverheat()
    row = json.loads(json.dumps(objects[1]))
    reads = [n for n in names if n["i"] == 1]

    hedged = json.loads(json.dumps(row))
    for r in hedged["reads"]:
        r["confidence"] = "unsure"
    # THE FLOOR BECAME A ROUTE, NOT A REFUSAL (2026-09-15). Six readers who all
    # REACHED the object and all hedged no longer fail it: STANDARD ("THE PHONE
    # TEST") passes it and routes it to the clerk, who settles the hedge on the
    # DELIVERED render where the object moves and carries its label. What must
    # never happen is a SILENT pass, so assert the routing flags are set - and
    # the clerk brief in daily-shorts.js must hand the clerk that list.
    out = production.consensus(hedged, [{"i": 1, "confidence": "unsure"}] * 6)
    assert out["sure_agreed"] == 0 and out["agreed"] == 6, out
    assert out["hedged"] is True and out["clerk_must_adjudicate"] is True, out
    wf = (Path(__file__).resolve().parents[4] / ".claude/workflows/daily-shorts.js")
    if wf.is_file():
        brief = wf.read_text()
        assert "clerk_must_adjudicate" in brief, "consensus routes hedges to the clerk and nothing tells the clerk"
        assert "HEDGED OBJECTS" in brief, "the clerk brief does not ask for a hedged-objects report"

    wrong = json.loads(json.dumps(row))
    for r in wrong["reads"]:
        r["confidence"] = "unsure"
    wrong["reads"][0].update(confidence="sure", name="toaster oven", match="different")
    # A CONFIDENTLY WRONG READER IS STILL NOT EVIDENCE (2026-09-15). The refusal
    # became a route, but the property this test exists for is unchanged and is
    # the one worth asserting: a `sure` read that named a DIFFERENT thing does
    # not count toward `sure_agreed`, so it cannot carry the object. It leaves
    # the object with zero sure reads that reached it, which routes it to the
    # clerk instead of passing it clean.
    out = production.consensus(wrong, reads)
    assert out["sure_agreed"] == 0, out
    assert out["different"] >= 1, out
    assert out["clerk_must_adjudicate"] is True, out

    longwinded = json.loads(json.dumps(row))
    for r in longwinded["reads"]:
        r["confidence"] = "unsure"
    longwinded["reads"][0].update(confidence="sure",
                                  name="download icon, an arrow over a line")
    # Same shape for the word cap: a six-word answer is not a clean
    # identification, so it does not become the object's one sure read.
    out = production.consensus(longwinded, reads)
    assert out["sure_agreed"] == 0, out
    assert out["clerk_must_adjudicate"] is True, out

    misread = json.loads(json.dumps(row))
    misread["reads"][0]["match"] = "different"
    misread["reads"][1]["match"] = "different"
    try:
        production.consensus(misread, reads)
    except ValueError as e:
        assert "named a DIFFERENT object" in str(e), e
    else:
        raise AssertionError("two different names passed")


def t_run17_a_long_answer_cannot_refuse_the_whole_round():
    """Object 3's three six-word answers used to throw away every other read.

    `read_rows` raised "a reader answer is one to five words" for the file, so
    the six clean reads of objects 0, 1 and 2 in the same round died with it.
    The violation is now stamped on the read and priced in `consensus`."""
    import tempfile
    import production
    from selection import atomic_json
    objects, _ = _pcoverheat()
    with tempfile.TemporaryDirectory() as d:
        # the verdict column is the AUTHOR's, and on disk it still carries the
        # HOLD it wrote under the old rule; this check is about the five-word
        # answers, so it rules on the same six rounds with the rows passed
        sc = Path(d) / "scores.json"
        atomic_json(sc, {"objects": [{**row, "verdict": "PASS"} for row in objects]})
        rows, names = production.read_rows(",".join(PCOVERHEAT_ROUNDS), sc)
    assert len(rows) == 4 and len(names) == 24, (len(rows), len(names))
    flagged = [n for n in names if n.get("over_five_words")]
    assert len(flagged) == 3 and {n["i"] for n in flagged} == {3}, flagged
    # an answer that names NOTHING is still not a read
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        ev = d / "reader.json"
        atomic_json(ev, {"names": [{"i": 0, "path": "/c/00.png", "name": "  ",
                                    "confidence": "sure"}]})
        sc = d / "scores.json"
        atomic_json(sc, {"objects": [{"i": 0, "verdict": "PASS"}]})
        try:
            production.read_rows(str(ev), sc)
        except ValueError as e:
            assert "names nothing is not a read" in str(e), e
        else:
            raise AssertionError("an empty answer was scored as a read")


# ---------------------------------------------------------------------------
# geo (run 19, 2026-09-13) — the keeper opening sat MID-BREATH and the head
# refused the whole cut.  "this is why | AI SEO, also known as GEO, is
# brutally hard": the content rule's keeper is "AI" (w26 @37.38), 0.141 s
# after "why", so no >= SILENCE_RUN_MIN silence exists before it.  The take
# starts at the head of that utterance, w23 "this" @36.779, which has a
# measured 0.48 s silence run (36.169-36.649) in front of it.
# ---------------------------------------------------------------------------
def t_geo_lead_in_walk_back():
    from prep import cutlib
    tp = F / "shorts_run19/intake/transcripts/2026-09-04 13-58-49.json"
    if not tp.exists():
        raise RuntimeError(f"fixture missing: {tp}")
    ws = cutlib.load_words(tp)
    assert len(ws) == 192, len(ws)
    rec = cutlib.detect_take(
        ws, opening_key=("ai", "seo", "also", "known", "as"),
        sign_off_key=("catch", "you", "in", "the", "next"),
        expected={"take_index": 26, "raw_words": 192},
        allow_uncorroborated=True)
    first = rec["take_word_index"]
    assert first == 26, first
    assert rec["openings_found"] == [0, 6, 26], rec["openings_found"]
    # the boundary the old head rule choked on
    gap = round(float(ws[first]["start"]) - float(ws[first - 1]["end"]), 3)
    assert gap == 0.141 and gap < cutlib.SILENCE_RUN_MIN, gap

    lead = cutlib.utterance_lead_in(ws, first, openings=rec["openings_found"],
                                    markers=cutlib.discard_markers(ws))
    assert lead is not None, "the walk-back refused geo's lead-in"
    assert lead["lead_in_index"] == 23, lead
    assert lead["lead_in_words"] == ["this", "is", "why"], lead
    assert lead["lead_in_start_s"] == 36.779, lead
    assert lead["lead_in_prev_end_s"] == 36.159, lead
    assert lead["boundary_gap_s"] == 0.62, lead
    # the walk-back may never reach the abandoned attempt at w6
    assert lead["floor_index"] == 7, lead
    assert lead["lead_in_index"] > 19, lead

    # a discard marker inside the lead-in is an abandonment: refuse, do not walk
    stumbled = [dict(w) for w in ws]
    stumbled[24]["text"] = "wh--"
    assert cutlib.discard_markers(stumbled) == [24], cutlib.discard_markers(stumbled)
    assert cutlib.utterance_lead_in(
        stumbled, first, openings=rec["openings_found"],
        markers=cutlib.discard_markers(stumbled))["lead_in_index"] == 25, \
        "the walk-back crossed a discard marker"
    # a keeper that already starts its own utterance needs no walk-back
    assert cutlib.utterance_lead_in(ws, 20, openings=[0, 6],
                                    markers=[]) is None

    # --- the AUDIO half: the refusal at the keeper, the head at the lead-in --
    raw = Path("/Users/migle/Movies/2026-09-04 13-58-49.mp4")
    if not raw.exists():
        raise RuntimeError(f"fixture missing: {raw}")
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        try:
            cutlib.measured_head(raw, prev_end=float(ws[first - 1]["end"]),
                                 scribe_start=float(ws[first]["start"]),
                                 scratch=Path(d),
                                 scribe_end=float(ws[first]["end"]))
        except RuntimeError as exc:
            assert "no silence run" in str(exc), exc
        else:
            raise AssertionError("the keeper boundary measured a silence run "
                                 "it does not have")
        head = cutlib.measured_head(
            raw, prev_end=lead["lead_in_prev_end_s"],
            scribe_start=lead["lead_in_start_s"], scratch=Path(d),
            scribe_end=float(ws[lead["lead_in_index"]]["end"]))
    assert head["onset_rule"] == "silence-run end", head
    assert head["measured_onset_s"] == 36.649, head
    assert head["silence_run_duration_s"] == 0.48, head
    assert head["head_s"] == 36.549, head
    assert head["head_inside_silence_run"] is True, head
    # cross-check 2b must be satisfied against the LEAD-IN start, not the keeper
    assert abs(head["measured_onset_s"] - lead["lead_in_start_s"]) <= 0.20, head


def t_geo_skip_marker_cannot_unpass_a_stage():
    """geo (run 19): the repair rerun stamped `skipped` over other markers.

    The package json has merged since run 14; the MARKER the gates poll did
    not.  A `--skip track,ship` repair must leave a passing marker exactly as
    it was, and must still stamp every verdict it really measured.
    """
    import tempfile

    import prep_batch
    with tempfile.TemporaryDirectory() as d:
        run = Path(d)
        pkg = {"id": "geo", "run": str(run), "stages": {}}
        stages = run / "prep" / "stages"

        prep_batch.mark_stage(pkg, "ship", {"status": "ok", "wall_s": 89.9,
                                            "matte_cut": "/x/cut.webm"})
        prep_batch.mark_stage(pkg, "plate", {"status": "error", "wall_s": 0.0,
                                             "error": "RuntimeError: no cut master"})
        # the repair rerun: both stages skipped
        prep_batch.mark_stage(pkg, "ship", {"status": "skipped", "wall_s": None})
        prep_batch.mark_stage(pkg, "plate", {"status": "skipped", "wall_s": 0.0})
        ship = json.loads((stages / "geo.ship.json").read_text())
        assert ship["status"] == "ok", ship
        assert ship["keys"]["matte_cut"] == "/x/cut.webm", ship
        # a failure carries no paid work to protect; the skip is recorded
        assert json.loads((stages / "geo.plate.json").read_text())["status"] \
            == "skipped"
        # and a real verdict always lands, over anything
        prep_batch.mark_stage(pkg, "ship", {"status": "REFUSED", "wall_s": 12.0})
        assert json.loads((stages / "geo.ship.json").read_text())["status"] \
            == "REFUSED"
        prep_batch.mark_stage(pkg, "cut", {"status": "ok", "wall_s": 37.8,
                                           "cut_master_duration_s": 53.456})
        prep_batch.mark_stage(pkg, "cut", {"status": "reused", "wall_s": 0.0})
        cut = json.loads((stages / "geo.cut.json").read_text())
        assert cut["status"] == "ok" and cut["keys"]["cut_master_duration_s"] == 53.456, cut


def t_geo_vpn_preflight_guards_uploads_not_the_batch():
    """geo (run 19): ProtonVPN refused a cut-only repair that uploads nothing.

    The guard is about Modal uploads.  With plate/track/ship skipped (or the
    BiRefNet sweep local) there is no upload to protect, so the batch launches;
    the moment one Modal stage is planned the refusal is exactly as before.
    """
    import prep_batch

    def fake_scutil(*_a, **_k):
        class R:                                          # noqa: D401
            stdout = ('* (Connected)      4E0D41C5 VPN (ch.protonvpn.mac) '
                      '"ProtonVPN"   [VPN:ch.protonvpn.mac]\n'
                      '* (Connected)      6CB0B932 VPN (io.tailscale.ipn.macsys) '
                      '"Tailscale"   [VPN:io.tailscale.ipn.macsys]\n')
        return R()

    real = prep_batch.subprocess.run
    prep_batch.subprocess.run = fake_scutil
    try:
        assert prep_batch.MODAL_STAGES == ("plate", "track", "ship"), \
            prep_batch.MODAL_STAGES
        # geo's repair: the local chain only — must launch
        prep_batch.vpn_preflight(skip={"plate", "prompt0", "track", "ship"})
        # a selection-review front with a local sweep — must launch
        prep_batch.vpn_preflight(skip={"track", "ship"}, sweep_local=True)
        # and the guard still fires for every batch that really uploads
        for bad_skip in ({}, {"ship"}, {"plate", "prompt0"}, {"track"}):
            try:
                prep_batch.vpn_preflight(skip=set(bad_skip))
            except SystemExit as exc:
                assert "ProtonVPN is CONNECTED" in str(exc), exc
            else:
                raise AssertionError(f"the VPN guard did not fire for skip={bad_skip}")
        # --allow-vpn is unchanged
        prep_batch.vpn_preflight(allow=True, skip=set())
    finally:
        prep_batch.subprocess.run = real


def t_grokwatch_false_start_boundary():
    from prep import cutlib
    tp = F / "shorts_run20/intake/transcripts/2026-09-04 13-15-13.json"
    if not tp.exists():
        tp = F / "shorts_run17/intake/transcripts/2026-09-04 13-15-13.json"
    if not tp.exists():
        raise RuntimeError(f"fixture missing: {tp}")
    ws = cutlib.load_words(tp)
    rec = cutlib.detect_take(
        ws, opening_families=[("grok", "can", "now", "watch", "videos"), ("grok", "can", "now", "watch")],
        sign_off_key=("catch", "you", "in", "the", "next"), allow_uncorroborated=True)
    first = rec["take_word_index"]
    assert ws[first]["text"].lower().startswith("grok"), ws[first]
    prev_end, take_start = float(ws[first - 1]["end"]), float(ws[first]["start"])
    gap = round(take_start - prev_end, 3)
    assert gap <= cutlib.FALSE_START_GAP_MAX, gap
    head = cutlib.false_start_boundary_head(prev_end, take_start)
    assert head is not None and prev_end < head["head_s"] < take_start, head
    assert head["false_start_gap_s"] == gap, head
    # a wide gap is NOT a false-start boundary: the silence rules own it
    assert cutlib.false_start_boundary_head(prev_end - 1.0, take_start) is None
    print(f"  PASS  grokwatch: keeper w{first} {gap}s after {ws[first - 1]['text']!r}; head {head['head_s']}")


# ---------------------------------------------------------------------------
# grokwatch (run 20, 2026-09-14): the keeper opening starts 0.03 s after an
# abandoned fragment ("...the entire v-... | Grok can now watch").  No silence
# run before the keeper, and the utterance walk-back only reaches the fragment,
# whose own boundary the audio did not measure as silence either.  LAW 46 puts
# the take at the fragment's boundary instead of refusing the cut.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# grok1080 (run 20, 2026-09-14): the matte fallback shipped against a plate
# that did not exist.  fallback_sam2.py carried run 19's literal
# `plate_display_1584x990.mp4`; grok1080's plate is 1260x900 * 1.10 = 1386x990,
# so the copy loop silently copied nothing, ship_all got a missing file, ffmpeg
# read `video_size -1x-1` and the decode ended out of step at output frame 0 -
# AFTER the paid H100 track had already landed 580 frames on disk.  The display
# plate's name is now DERIVED from plate.json in one place, and a session that
# has no display plate is refused BY NAME before ffmpeg is ever called.
# ---------------------------------------------------------------------------
def t_grok1080_display_plate_is_derived_not_a_literal():
    import platelib
    F = Path(__file__).resolve().parents[2]

    # a) grok1080's own numbers: plate_size 1260x900, paint scale 1.10
    with tempfile.TemporaryDirectory() as td:
        sess = Path(td)
        (sess / "plate.json").write_text(json.dumps({"plate_size": [1260, 900], "paint_scale": 1.1}))
        assert platelib.display_plate_size(sess / "plate.json") == (1386, 990)
        # missing on disk -> the DERIVED name comes back so the caller can refuse by name
        derived = platelib.display_plate(sess)
        assert derived.name == "plate_display_1386x990.mp4", derived
        assert not derived.exists()
        (sess / "plate_display_1386x990.mp4").write_bytes(b"")
        assert platelib.display_plate(sess).name == "plate_display_1386x990.mp4"
        # run 19's geo plate (1440x900) must resolve somewhere else entirely
        (sess / "plate.json").write_text(json.dumps({"plate_size": [1440, 900]}))
        assert platelib.display_plate_size(sess / "plate.json") == (1584, 990)

    # b) no hardcoded plate name may survive in the fallback
    src = (F / "pipeline/matting/fallback_sam2.py").read_text()
    assert "1584x990" not in src, "run 19's display-plate literal is back in fallback_sam2.py"
    assert not re.search(r"plate_display_\d+x\d+", src), "fallback_sam2.py hardcodes a display plate again"
    assert "platelib.display_plate(" in src, "fallback_sam2.py no longer derives the display plate"
    # and the refusal must happen before ship_all is reached
    CALL = "srec, scan, edge = ship_all("
    assert src.index("the display plate is missing in") < src.index(CALL), \
        "the missing-plate refusal must come before the ship_all call"

    # c) the live run-20 session agrees with the derivation
    live = F / "shorts_run20/matting/grok1080/plate.json"
    if live.exists():
        assert platelib.display_plate_size(live) == (1386, 990)
        assert platelib.display_plate(live.parent).name == "plate_display_1386x990.mp4"
    print("  PASS  grok1080: display plate derived 1260x900 x1.10 -> 1386x990, no literal in fallback_sam2")


def test_corrections_groq_to_grok():
    """2026-09-05: Scribe writes Groq for Grok; the vocabulary corrections map rewrites it."""
    import cutlib
    payload = {"words": [{"type": "word", "text": "Groq"}, {"type": "word", "text": "Build,"},
                         {"type": "word", "text": "SuperGroq"}, {"type": "word", "text": "hello"}]}
    n = cutlib.apply_corrections(payload)
    assert n == 3, n
    assert [w["text"] for w in payload["words"]] == ["Grok", "Build,", "SuperGrok", "hello"]
    print("  PASS  corrections: Groq -> Grok, punctuation kept")


# ---------------------------------------------------------------------------
# fluxvideo (run 20, 2026-09-14): the matte fallback resumed a paid track that
# belonged to a SUPERSEDED contour.  fallback_sam2.py keyed its
# "a previous call was interrupted after the paid track" resume on the alpha's
# FILE NAME alone, so the 21:40 fallback wrote the astra-reviewed mask
# (e0fafdaa, both chair polygons excluded) as its prompt and then shipped
# alpha_fb1.mkv, tracked at 17:12 from the pre-review birefnet contour
# (46bbf6ba, the mask selection.json still records as base_mask_sha256, chair
# included).  The chair headrest lobe rode through to the viewer test -
# chair_band p50 728 -> 2102 px, WORSE than the MatAnyone matte the fallback
# was meant to repair - under a note claiming "reviewed frame-0 contour as the
# only prompt".  The resume is now bound to the prompt: same contour resumes
# free, a corrected contour tracks under its own tag and its own volume path.
# ---------------------------------------------------------------------------
def t_fluxvideo_paid_track_resume_is_bound_to_the_prompt():
    import fallback_sam2 as fb
    F = Path(__file__).resolve().parents[2]
    REVIEWED = "e0fafdaa3fe798cfc5918dc542b5849a9327579e2c50640447bdc0ac1311d97b"
    PRE_REVIEW = "46bbf6ba0c01dabd104ef747c5627bea55e223e6fcaec270ef792cdea66d537f"

    # a) fluxvideo's own two contours, from the live session
    M = F / "shorts_run20/matting/fluxvideo"
    if (M / "selection.json").exists():
        sel = json.loads((M / "selection.json").read_text())
        assert sel["status"] == "reviewed", sel["status"]
        assert sel["mask_sha256"] == REVIEWED, sel["mask_sha256"]
        assert sel["base_mask_sha256"] == PRE_REVIEW, sel["base_mask_sha256"]
        assert sel["mask_sha256"] != sel["base_mask_sha256"], "the review changed nothing?"
        # the chair lobe the viewer held on is an EXCLUDE in the reviewed contour
        labels = " ".join(e.get("label", "") for e in sel["edits"] if e["operation"] == "exclude")
        assert "backrest lobe" in labels, labels
        assert len(sel["edits"]) == 2, sel["edits"]

    # b) the rule itself, on fluxvideo's real hashes
    with tempfile.TemporaryDirectory() as td:
        S = Path(td)
        # nothing on disk -> the asked-for tag, fresh track
        assert fb.resume_tag(S, "fb1", REVIEWED)[0] == "fb1"
        # THE RUN-20 STATE: a paid alpha whose provenance was never recorded.
        # It must NOT be inherited by the reviewed contour.
        (S / "alpha_fb1.mkv").write_bytes(b"paid")
        eff, why = fb.resume_tag(S, "fb1", REVIEWED)
        assert eff == "fb1_pe0fafdaa", eff
        assert eff != "fb1", "the superseded alpha was resumed again"
        assert "NOT reused" in why and "unrecorded prompt" in why, why
        # the receipt naming the pre-review contour: same refusal, and it says so
        (S / "alpha_fb1.prompt.json").write_text(json.dumps({"prompt_mask_sha256": PRE_REVIEW}))
        eff, why = fb.resume_tag(S, "fb1", REVIEWED)
        assert eff == "fb1_pe0fafdaa", eff
        assert PRE_REVIEW in why, why
        # a genuine interrupted resume is still FREE: same contour, same tag
        (S / "alpha_fb1.prompt.json").write_text(json.dumps({"prompt_mask_sha256": REVIEWED}))
        eff, why = fb.resume_tag(S, "fb1", REVIEWED)
        assert eff == "fb1", eff
        assert "nothing re-dispatched" in why, why
        # and the derived tag is deterministic, so it resumes itself next time
        (S / "alpha_fb1_pe0fafdaa.mkv").write_bytes(b"paid")
        (S / "alpha_fb1_pe0fafdaa.prompt.json").write_text(json.dumps({"prompt_mask_sha256": REVIEWED}))
        assert fb.resume_tag(S, "fb1_pe0fafdaa", REVIEWED)[0] == "fb1_pe0fafdaa"

    # c) the bare file-existence resume may not come back into the source
    src = (F / "pipeline/matting/fallback_sam2.py").read_text()
    assert 'alpha = S / f"alpha_{a.tag}.mkv"' not in src, "the tag-only resume is back in fallback_sam2.py"
    assert "resume_tag(S, a.tag, prompt_sha)" in src, "fallback_sam2.py no longer asks resume_tag"
    assert src.index("resume_tag(S, a.tag, prompt_sha)") < src.index("srec, scan, edge = ship_all("), \
        "the resume decision must be made before the alpha is shipped"
    # every paid track leaves its receipt
    assert 'f"alpha_{eff_tag}.prompt.json"' in src, "the track no longer records the contour it used"

    # d) the live run-20 session: the two alphas are on disk with their receipts,
    #    and the reviewed contour resumes fb2 - never fb1
    S = F / "shorts_run20/matting_fallback/fluxvideo"
    if (S / "alpha_fb1.mkv").exists() and (S / "alpha_fb2.mkv").exists():
        assert fb.tracked_prompt(S, "fb1") == PRE_REVIEW, fb.tracked_prompt(S, "fb1")
        assert fb.tracked_prompt(S, "fb2") == REVIEWED, fb.tracked_prompt(S, "fb2")
        assert fb.resume_tag(S, "fb2", REVIEWED)[0] == "fb2"
        assert fb.resume_tag(S, "fb1", REVIEWED)[0] == "fb1_pe0fafdaa"
    print("  PASS  fluxvideo: e0fafdaa never inherits 46bbf6ba's paid alpha; same contour still resumes free")



# ---------------------------------------------------------------------------
# grokemail (run 21, 2026-09-15) — the production matte lane had no furniture
# check and no background-haze check, so a chair tab standing on the shoulder
# for the whole 43 s and a 2.2 s pale slab beside the head both shipped "ok".
#
# The numbers below are grokemail's own, measured on the matte the viewer test
# rejected, and codexdetail's, measured on the matte that PASSED the same gate
# the same day.  chair_band, soft-alpha, components, holes and IoU all read
# WORSE on the matte that passed; only these two measures separate them.
# ---------------------------------------------------------------------------
def t_run21_grokemail_frozen_edge_is_furniture():
    import numpy as np
    import matte_review as mr

    # grokemail, measured: the shipped matte held its top edge across columns
    # 596-631 to sd 0.76 px over 216 sampled frames while the flanking shoulder
    # columns wandered by 16.35.  That is the chair tab on the frame-left
    # shoulder, and `sam2/ship.py`'s protrusion gate refused the same tab at
    # x595:617 the moment the SAM2 fallback ran it.
    rng = np.random.default_rng(21)
    n, H, W = 216, 990, 800
    A = np.zeros((n, H, W), np.uint8)
    for i in range(n):
        top = np.full(W, 600.0 + rng.normal(0, 16.35))
        top[596:632] = 534 + rng.normal(0, 0.76)              # the frozen tab
        for x in range(W):
            A[i, int(round(top[x])):, x] = 255
    got = mr.frozen_edge(A)
    assert got["hold"] is True, got
    runs = got["runs"]
    assert len(runs) == 1, runs
    r = runs[0]
    assert 590 <= r["x0"] <= 600 and 625 <= r["x1"] <= 640, r
    assert r["edge_sd"] <= 1.5 and r["flank_sd"] >= 3.0, r
    assert r["ratio"] >= 4.0, r

    # codexdetail, the run-21 matte that PASSED: the whole silhouette moves.
    B = np.zeros((185, H, W), np.uint8)
    for i in range(185):
        top = np.full(W, 600.0 + rng.normal(0, 12.0))
        for x in range(W):
            B[i, int(round(top[x])):, x] = 255
    clean = mr.frozen_edge(B)
    assert clean["hold"] is False, clean
    assert clean["runs"] == [], clean


def t_run21_grokemail_background_haze_holds_for_a_window():
    import numpy as np
    import matte_review as mr

    def matte(haze_samples):
        n, H, W = len(haze_samples), 300, 400
        A = np.zeros((n, H, W), np.uint8)
        A[:, 120:280, 150:330] = 255                   # the person, opaque core
        A[:, 118:120, 150:330] = 90                    # its own soft edge, attached
        for i, px in enumerate(haze_samples):
            if px <= 0:
                continue
            w = max(1, px // 60)
            A[i, 40:100, 40:40 + w] = 18               # detached background slab
        return A

    # grokemail's own profile at 5 fps: the slab holds through 2.2 s, then goes
    got = mr.background_haze(matte([20, 6368, 6167, 5684, 5629, 6669, 3324, 4022,
                                    1988, 3650, 2708, 2075] + [0] * 40), 5)
    assert got["hold"] is True, got
    assert got["longest_run_s"] >= 1.0, got
    assert got["max"] >= 1500, got

    # codexdetail, the matte that passed: one isolated sampled frame of it,
    # which is a motion-blurred hand and must never hold a lane.
    clean = mr.background_haze(matte([0] * 24 + [5045] + [0] * 30), 5)
    assert clean["hold"] is False, clean
    assert clean["longest_run_s"] < 1.0, clean
    assert clean["frames_over_floor"] == 1, clean


def t_run21_the_production_matte_review_reports_both():
    """The gate must reach the stage-17 viewer, not just exist as a function."""
    import matte_review as mr
    src = Path(mr.__file__).read_text()
    assert '"background_haze": haze' in src, "haze never lands in metrics.json"
    assert '"frozen_edge": frozen' in src, "frozen edge never lands in metrics.json"
    assert '"auto_hold"' in src and "AUTO-HOLD:" in src, "no verdict is printed"

    live = F / "shorts_run21/review/matte_grokemail/metrics.json"
    if live.exists():
        m = json.loads(live.read_text())
        if "background_haze" in m:            # regenerated since the fix
            for k in ("background_haze", "frozen_edge", "auto_hold"):
                assert k in m, k
            assert "longest_run_s" in m["background_haze"], m["background_haze"]
            assert "runs" in m["frozen_edge"], m["frozen_edge"]


def t_run21_skip_plate_reuses_the_plate_the_selection_is_bound_to():
    """A matting repair re-run must not rebuild the plate under the contour."""
    src = (F / "pipeline/prep/prep_batch.py").read_text()
    i = src.index('with Stage(package, vid, "plate")')
    branch = src[i:i + 2600]
    assert '"plate" in skip' in branch, branch[:200]
    assert '"status": "reused"' in branch, "a skipped plate still stamps a bare skipped"
    assert '"plate": str(f)' in branch, "a skipped plate hands matting no plate path"
    # the adapter's own precondition, unchanged
    ad = (F / "pipeline/matting/prep_adapter.py").read_text()
    assert "('ok','reused')" in ad.replace(" ", ""), ad[:200]

    # grokemail's live plate is the one the reviewed selection is bound to
    sess = F / "shorts_run21/matting/grokemail"
    if (sess / "selection.json").exists() and (sess / "plate.json").exists():
        import hashlib
        sel = json.loads((sess / "selection.json").read_text())
        pj = json.loads((sess / "plate.json").read_text())
        f = Path(pj["file"])
        assert pj["plate_size"] == [1800, 900], pj["plate_size"]
        if f.exists():
            h = hashlib.sha256(f.read_bytes()).hexdigest()
            assert h == sel["identity"]["plate_sha256"], (
                "the plate under grokemail's reviewed selection has been rebuilt")



# ---------------------------------------------------------------------------
# run 22, aieducation - the reviewer that looked in one place for a shipped matte
#
# prep_batch ships the triple into whatever --sessions pointed at.  Run 22's
# matte batch used the factory-wide default sessions root, so the matte landed
# in pipeline/sam2/sessions/aieducation and matte_review.py - which only knew
# <run>/matting/<id> - declared "No matte exists", after having already created
# an empty review/matte_aieducation/.  Both halves are fixed: resolve the
# session from what prep recorded, and never leave an empty evidence dir behind.
# ---------------------------------------------------------------------------
def t_run22_aieducation_session_is_resolved_from_prep() -> None:
    import matte_review as mr

    vid = "aieducation"
    real = (F / "pipeline/sam2/sessions" / vid).resolve()
    assert (real / f"matte_{vid}_v5_cut.webm").exists(), "run-22 shipped triple is gone"

    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "shorts_run22"
        (run / "prep").mkdir(parents=True)
        (run / "matting" / vid).mkdir(parents=True)          # the empty convention dir
        (run / "prep" / f"{vid}.json").write_text(json.dumps({
            "id": vid,
            "session": str(real),
            "stages": {"ship": {"outputs": {
                "cut": str(real / f"matte_{vid}_v5_cut.webm"),
                "rim": str(real / f"matte_{vid}_v5_rim.webm"),
                "alpha": str(real / f"matte_{vid}_v5_alpha.webm"),
            }}},
        }))
        sess, how, tried = mr.resolve_session(run, vid)
        assert sess == real, f"resolved {sess}, wanted {real}"
        assert how == "prep package ship outputs", how

        # the package alone is enough; _batch.json sessions_root is the backup
        (run / "prep" / f"{vid}.json").unlink()
        (run / "prep" / "_batch.json").write_text(json.dumps(
            {"sessions_root": str(real.parent)}))
        sess, how, _ = mr.resolve_session(run, vid)
        assert sess == real and how == "batch sessions_root", (sess, how)

        # nothing anywhere -> the convention, and every candidate is named
        (run / "prep" / "_batch.json").unlink()
        sess, how, tried = mr.resolve_session(run, vid)
        assert sess == run / "matting" / vid and how == "run-local convention"
        assert tried and "run-local convention" in tried[-1]


def t_run22_a_missing_matte_leaves_no_empty_evidence_dir() -> None:
    import subprocess as sp

    vid = "aieducation"
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / "shorts_run22"
        (run / "prep").mkdir(parents=True)
        r = sp.run([sys.executable, str(F / "pipeline/matting/matte_review.py"),
                    "--run", str(run), "--vid", vid],
                   capture_output=True, text=True)
        assert r.returncode != 0, "a missing matte must not exit 0"
        blob = r.stdout + r.stderr
        assert "missing" in blob and "candidates tried" in blob, blob[-400:]
        assert not (run / "review" / f"matte_{vid}").exists(), \
            "an empty review/matte_<id>/ reads as blank sheets to the next agent"

if __name__ == "__main__":
    print("REGRESSIONS 2026-09-04 (run 14 prep failures)")
    check("game33c: inner discard marker is kept and witnesses the opening",
          t_inner_marker)
    check("trycrm: json_safe + the three blob pops", t_json_safe)
    check("trycrm: prep_batch ship-stage record recovery", t_ship_recovery)
    check("grokbuild: chairprompt.from_refusal on the real refusal window",
          t_chair_from_refusal)
    check("grokbuild: repair_round tries the chair object before wingfix",
          t_repair_tries_chair_first)
    check("AUDIT A4: straight-run counter finds the 70-row suffix",
          t_outline_longest_flat_counterexample)
    check("AUDIT A5: empty and truncated measurements fail closed",
          t_outline_missing_measurements_fail_closed)
    check("game33c: temporal chair support removes the saved obj3 flicker",
          t_game33c_temporal_chair_support)
    check("AUDIT A1: not-a-wing vetoes outline wingfix; zero carve",
          t_not_a_wing_vetoes_outline_wingfix)
    check("AUDIT A1: not-a-wing vetoes protrusion wingfix; needs_miguel",
          t_not_a_wing_vetoes_protrusion_wingfix)
    check("game33c: NO REPAIR MAY REMOVE SKIN — reach fence, hole refill, gate",
          t_game33c_no_repair_removes_skin)
    print("RUN 16 (plantsite, 2026-09-06) — the unread shared scene")
    check("plantsite: the shared peak object read 'flower' on all four readers",
          t_run16_peak_object_read_flower)
    check("plantsite: a reader that never saw the image is not a read",
          t_run16_dispatch_failure_is_not_a_read)
    check("plantsite: cold_read refuses non-reads and normalises confidence",
          t_run16_cold_read_parses_a_non_read)
    check("plantsite: an unread shared scene is not a PASS, and a seal goes stale",
          t_run16_unread_shared_scene_is_not_a_pass)
    print("RUN 17 (eudisclosure, 2026-09-08) — the gate agent that never returned")
    check("eudisclosure: the ok ship marker reads ok, with its three matte layers",
          t_run17_gate_marker_reads_the_ok_ship_marker)
    check("eudisclosure: missing, truncated, REFUSED and override all answer",
          t_run17_gate_marker_never_returns_nothing)
    check("eudisclosure: the gate waits in python, in ONE bounded command",
          t_run17_gate_marker_waits_in_python_not_in_an_agent)
    print("RUN 17 (cursorworkspace, 2026-09-08) — the second gate, and the layers under an ok")
    check("cursorworkspace: the ok ship marker verifies against its own ship_v5.json",
          t_run17_ship_ok_is_only_as_good_as_its_layers)
    check("cursorworkspace: a truncated/missing/stale layer is not a pass, and no manifest is not a defect",
          t_run17_a_broken_layer_is_not_a_pass)
    print("RUN 17 (pcoverheat, 2026-09-08) \u2014 the confidence flag that held the cutout lane")
    check("pcoverheat: six of six readers named the download arrow, two were sure",
          t_run17_six_of_six_readers_named_the_download_arrow)
    check("pcoverheat: the NOUN is the measurement; all four objects rule",
          t_run17_the_noun_is_the_measurement_not_the_flag)
    check("pcoverheat: the confidence floor moved to one sure read, it did not vanish",
          t_run17_the_confidence_floor_did_not_vanish)
    check("pcoverheat: a six-word answer no longer refuses the whole round",
          t_run17_a_long_answer_cannot_refuse_the_whole_round)
    print("RUN 19 (geo, 2026-09-13) — the keeper opening that sat mid-breath")
    check("geo: the lead-in walk-back starts the take at its utterance head",
          t_geo_lead_in_walk_back)
    check("geo: the VPN preflight guards Modal uploads, not every batch",
          t_geo_vpn_preflight_guards_uploads_not_the_batch)
    check("geo: a skipped stage cannot un-pass the marker a gate polls",
          t_geo_skip_marker_cannot_unpass_a_stage)
    check("grokwatch: the keeper runs out of an abandoned fragment - false-start boundary, not a refusal",
          t_grokwatch_false_start_boundary)
    print("RUN 20 (grok1080, 2026-09-14) \u2014 the matte fallback's hardcoded display plate")
    check("grok1080: the fallback derives the display plate from plate.json, never a literal",
          t_grok1080_display_plate_is_derived_not_a_literal)
    print("RUN 20 (fluxvideo, 2026-09-14) \u2014 the matte fallback that resumed a superseded contour's paid track")
    check("fluxvideo: the paid-track resume is bound to the reviewed prompt, not the tag",
          t_fluxvideo_paid_track_resume_is_bound_to_the_prompt)
    print("RUN 21 (grokemail, 2026-09-15) \u2014 the production matte lane with no furniture check")
    check("grokemail: a frozen top-edge run on a moving shoulder is furniture (x596-631, sd 0.76 vs 16.35)",
          t_run21_grokemail_frozen_edge_is_furniture)
    check("grokemail: detached fractional alpha that holds for a window is a HOLD; one frame of it is not",
          t_run21_grokemail_background_haze_holds_for_a_window)
    check("grokemail: both measures reach the stage-17 viewer as an auto-hold verdict",
          t_run21_the_production_matte_review_reports_both)
    check("grokemail: --skip plate reuses the plate the reviewed selection is bound to",
          t_run21_skip_plate_reuses_the_plate_the_selection_is_bound_to)
    print("RUN 22 (aieducation, 2026-09-15) \u2014 the reviewer that knew one session path")
    check("aieducation: the matte session is resolved from what prep recorded, not one convention",
          t_run22_aieducation_session_is_resolved_from_prep)
    check("aieducation: a missing matte names every candidate and leaves no empty evidence dir",
          t_run22_a_missing_matte_leaves_no_empty_evidence_dir)
    print()
    if FAILED:
        print(f"{len(FAILED)} FAILED")
        for f in FAILED:
            print("  -", f)
        raise SystemExit(1)
    print("all clear")


