#!/usr/bin/env python3
"""ONE BUILD, ONE COMPOSITION - hermesdocs / DIAGRAM BUILD / CUTOUT.

    TikTok   cutout   projects/hermesdocs_cutout   @migueltorrez.ai

THE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/hermesdocs_scene.py` + the
handoff are sealed (`review/artwork_pass_hermesdocs.json`, production v4); this
file asserts both digests against the seal, imports the module and seats it in
the stage zone measured off THIS recording's shipped alpha
(`gen/hermesdocs_cutout_envelope.py`).

CAPTIONS, LAW ASSERTS (cues, word-sync, LAW 37, labels, lifetimes, the four
connectors, the three border-flip emphases, the draw-on dash law), SFX AND THE
PAGE SHELL ARE THE SPLIT'S OWN CODE (`hermesdocs_split_gen`, imported, never
run as a build): the two masters carry one caption stream and one soundtrack.
Only the SEAT differs (the pill seated 26.5 px above his measured crown with
the pill that RENDERS, 114.59).

PLACEMENT: k = 1.00 and core top 192, the split's placement.  The stage zone
(192 .. 806.4) holds content 252..736 with 70.4 px to the zone bottom, so the
approved split geometry carries over unchanged and the plan's bespoke bboxes
ARE the cutout page's bboxes (the handoff's centring formula would give top
197.2, a 5 px move that buys nothing and breaks the plan-bbox identity).

THE MATTE: MatAnyone 2 from the reviewed selection (Astra, one round, two
chair-exclusion edits), ship marker ok, headroom min 45.1 px over all 707
frames.  Layers staged as is, digests checked against `ship_v5.json`.  The
plate is OVER-WIDE (1386x990); its origin (-153, 930) is READ from plate.json's
`overwide.plate_box`, never computed (NOT centred).

THE DEPTH FIELD is the chassis's (`cutout_depthfield`).  Per-video choices: the
CAST (the plan's `cutout_logo_lanes`: ollama, openclaw, notebooklm, claude,
chatgpt, mistral, huggingface) and the pop-behind (none: the only products he
names are Hermes and Firecrawl, both stage marks; AnyDoc has no mark).
DF.field picks cast[(7j + 5i) % len]: SEVEN marks would put one mark in every
slot of a lane, so FIELD_ORDER walks the roster in an EIGHT-slot cycle (claude
twice, never adjacent) and every lane carries all seven.
THE LANES ARRIVE WHEN THE HOOK HAS LANDED: wrappers held at 0 and faded in at
HOOK_CLEAR = "privacy." (2.22 s), the end of the hook sentence, when the safe
is drawn, the Nous girl tile has dropped and the dial turns to lock.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hermesdocs_split_gen as B                 # noqa: E402

CAP, CC, DF, SC = B.CAP, B.CC, B.DF, B.SC
RUN, F, CUT = B.RUN, B.F, B.CUT
VID = "hermesdocs"
W, H = B.W, B.H
DUR = B.DUR
FPS = B.FPS
S = RUN / f"matting/{VID}"
OUT = RUN / f"projects/{VID}_cutout"
LOGOS = B.LOGOS
EASE = '"power3.out"'

CORE_K = 1.00
CORE_TOP = 192.0
# the hook sentence "Hermes Agent just dropped another banger for privacy." has
# landed on "privacy." (the safe drawn 0.10-0.50, the Nous girl tile dropped
# 0.44, the dial starts its lock turn 2.22).
HOOK_CLEAR = round(SC.CUE["lock"], 2)                          # 2.22 s
# One step per spoken beat at the foundation's pulse (12 over 40 s = 3.3 s):
# (23.88 outro - 2.22) / 3.3 = 6.6 -> 7.
STEP_N = 7

DEPTH_FILES = {k: SC.CUTOUT_LANE_FILES[k] for k in SC.CUTOUT_LOGO_LANES}
DEPTH_BANNED = {"nous-girl-line", "hermes", "firecrawl"}
# an 8-slot cycle (coprime with the field's stride 7); the one repeat (claude,
# slots 3 and 7) is never next to itself, wrap-around included.
FIELD_ORDER = ["ollama", "openclaw", "notebooklm", "claude", "chatgpt",
               "mistral", "huggingface", "claude"]


def digest(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def guard_plate_box(box: dict, layers: dict) -> dict:
    """THE BOX IS THE PLATE'S ENCODED SIZE AT WHOLE-PIXEL OFFSETS (v5.1)."""
    for k in ("w", "h", "left", "top"):
        if abs(box[k] - round(box[k])) > 1e-9:
            raise SystemExit(f"plate box {k}={box[k]} is not a whole pixel")
    for name, enc in layers.items():
        if (box["w"], box["h"]) != (enc["w"], enc["h"]):
            raise SystemExit(f"plate box {box['w']}x{box['h']} != encoded {name} "
                             f"{enc['w']}x{enc['h']}")
    return {"box": dict(box), "whole_pixels": True, "equals_encoded": layers,
            "origin": "read from plate.json overwide.plate_box (not computed; "
                      "the box is deliberately not centred)"}


def plate_origin(box_w: float, box_h: float) -> tuple[float, float]:
    ob = json.loads((S / "plate.json").read_text())["overwide"]["plate_box"]
    if [float(ob["w"]), float(ob["h"])] != [float(box_w), float(box_h)]:
        raise SystemExit(f"plate.json box {ob['w']}x{ob['h']} != staged "
                         f"{box_w}x{box_h}")
    return float(ob["left"]), float(ob["top"])


def guard_seal() -> dict:
    seal = json.loads((RUN / f"review/artwork_pass_{VID}.json").read_text())
    if seal.get("verdict") != "PASS":
        raise SystemExit("the scene seal is not PASS")
    ev = seal.get("evidence") or {}
    out = {}
    for p in (HERE / f"{VID}_scene.py", RUN / f"plans/{VID}_scene_handoff.md"):
        want = ev.get(str(p))
        if want is None:
            raise SystemExit(f"the seal names no digest for {p}")
        if want != digest(p):
            raise SystemExit(f"stale scene seal: {p} changed since it was sealed")
        out[p.name] = want
    return out


def place(zy0: float, zy1: float) -> tuple[float, float, float, dict]:
    k, top = CORE_K, CORE_TOP
    left = round((W - SC.CORE_W * k) / 2, 2)
    y0, y1 = top + SC.CONTENT_Y0 * k, top + SC.CONTENT_Y1 * k
    if y0 < zy0 or y1 > zy1:
        raise SystemExit(f"content {y0}..{y1} leaves the stage zone {zy0}..{zy1}")
    return k, left, top, {"k": k, "left": left, "top": top,
                          "why": "the split's placement (k 1.00, top 192); legal "
                                 "inside this body's stage zone, and the plan's "
                                 "bespoke bboxes map 1:1",
                          "stage_zone": [zy0, zy1],
                          "content_band_canvas": [y0, y1],
                          "clear_to_zone_bottom": round(zy1 - y1, 2)}


def guard_silhouette(env: dict, top: float, k: float, left: float) -> dict:
    """NEVER OCCLUDE HIM: the lowest inked core row must sit above the highest
    silhouette row of the whole take (union over all frames)."""
    ink_bottom = top + SC.CONTENT_Y1 * k
    crown = env["union_top_canvas"]
    if ink_bottom >= crown:
        raise SystemExit(f"scene ink reaches y={ink_bottom}, crown at {crown}")
    return {"scene_ink_bottom_canvas": ink_bottom, "silhouette_crown_canvas": crown,
            "clear_px": round(crown - ink_bottom, 1)}


def stage() -> dict:
    ship = json.loads((S / "ship_v5.json").read_text())
    if ship.get("status") != "ok":
        raise SystemExit("ship_v5.json is not ok")
    matting = json.loads((S / "matting.json").read_text())
    hr = matting["headroom"]
    if not hr["pass"] or hr["unsafe_frames"]:
        raise SystemExit("headroom guard did not pass on this matte")
    sel = json.loads((S / "selection.json").read_text())
    if sel.get("status") != "reviewed":
        raise SystemExit("the frame-0 selection is not reviewed")
    if matting["track"]["spec"]["mask_sha256"] != sel["mask_sha256"]:
        raise SystemExit("the shipped matte was not tracked from the reviewed mask")
    astra = json.loads((RUN / f"review/astra_astra_matte_{VID}.result.json").read_text())
    if astra.get("status") != "ok" or astra.get("ship") != "ok":
        raise SystemExit("Astra's matte review is not ok")
    for key in ("cut", "rim", "alpha"):
        if digest(S / f"matte_{VID}_v5_{key}.webm") != ship["hashes"][key]:
            raise SystemExit(f"matte {key} layer does not match ship_v5.json")
    for sub in ("v", "music", "sfx", "logos"):
        (OUT / f"assets/{sub}").mkdir(parents=True, exist_ok=True)
    v = OUT / "assets/v"
    layers = {}
    for key, name in (("cut", "matte.webm"), ("rim", "matte_rim.webm")):
        src = S / f"matte_{VID}_v5_{key}.webm"
        shutil.copy2(src, v / name)
        if digest(v / name) != ship["hashes"][key]:
            raise SystemExit(f"staged {name} differs from the shipped layer")
        st = src.stat()
        (v / f"_{name}.src").write_text(f"{src}\n{st.st_size} {st.st_mtime_ns}")
        layers[key] = B.probe_wh(v / name)
    (v / "_matte_source.txt").write_text(str(S))
    shutil.copy2(CUT / "audio.m4a", v / "voice.m4a")
    voice = {"source": str(CUT / "audio.m4a"), **B.probe_audio(v / "voice.m4a")}
    if voice["sample_rate"] < 44100:
        raise SystemExit(f"staged voice is {voice['sample_rate']} Hz")
    bed = B.LIB_MUSIC / "bed_split_v2.mp3"
    shutil.copy2(bed, OUT / "assets/music/bed.mp3")
    for s in ("whoosh", "pop", "click"):
        shutil.copy2(B.LIB_SFX / f"{s}.mp3", OUT / f"assets/sfx/{s}.mp3")
    plan = json.loads(B.PLAN.read_text())
    if list(DEPTH_FILES) != list(plan["cutout_logo_lanes"]):
        raise SystemExit("the depth roster is not the plan's cutout_logo_lanes")
    if set(DEPTH_FILES) & (DEPTH_BANNED | set(SC.LOGO_FILES)):
        raise SystemExit("a stage/subject mark is in the depth roster")
    allf = {**SC.LOGO_FILES, **DEPTH_FILES}
    cast_check = DF.assert_cast_resolves(list(allf), dict(allf), LOGOS,
                                        label="hermesdocs stage marks + depth roster")
    urls = {}
    for key, rel in allf.items():
        src = LOGOS / rel
        shutil.copy2(src, OUT / "assets/logos" / src.name)
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        urls[key] = f"assets/logos/{src.name}"
    for key in SC.LOGO_FILES:
        if urls[key] != B.LOGO_URL[key]:
            raise SystemExit(f"the stage mark URL for {key} differs from the split's")
    return {"ship": ship, "matting_headroom": hr, "layers": layers,
            "voice": voice, "bed": str(bed), "urls": urls,
            "selection_mask_sha256": sel["mask_sha256"],
            "astra_review": {"status": astra.get("status"),
                             "selection_changed": astra.get("selection_changed"),
                             "edits": astra.get("edits"),
                             "rounds": astra.get("rounds")},
            "cast_check": {k: v2.get("path") if isinstance(v2, dict) else v2
                           for k, v2 in cast_check.items()}}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    seal = guard_seal()
    env = json.loads((HERE / f"_envelope_{VID}.json").read_text())
    st = stage()
    if env["source_sha256"] != st["ship"]["hashes"]["alpha"]:
        raise SystemExit("the envelope was measured on a different alpha")
    if env["crown_gate"]["frames_on_plate_top"]:
        raise SystemExit("the silhouette touches the plate's top row: a cut, not a crown")

    box_w, box_h = float(st["layers"]["cut"]["w"]), float(st["layers"]["cut"]["h"])
    box_left, box_top = plate_origin(box_w, box_h)
    box = {"w": box_w, "h": box_h, "left": box_left, "top": box_top}
    plate = guard_plate_box(box, st["layers"])
    plate["face_centre_canvas"] = env.get("face_centre_canvas")

    cap_y, zy0, zy1 = (env["seats"][k] for k in ("CAP_Y", "ZY0", "ZY1"))
    k, left, top, place_rec = place(zy0, zy1)
    # the split's canvas() / guard_rail() / phone_objects() read these
    B.CORE_K, B.CORE_TOP_SPLIT, B.LEFT = k, top, left
    sil = guard_silhouette(env, top, k, left)

    ws, clean_rep = B.clean_tokens(B.words())
    checks = {"cues": B.assert_cues(ws), "word_sync": B.assert_word_sync(ws),
              "law37": B.assert_law37(ws), "law39": B.assert_label_law(),
              "law42": B.assert_lifetime_law(), "law38": B.assert_emphasis_law(),
              "law2": B.assert_cast_law(), "silhouette": sil}
    SFX = B.sfx_plan()
    checks["law22"] = B.assert_sfx(SFX)

    m = CAP.PillMeasurer(HERE / f"_pillwidths_{VID}_cutout.json")
    beats, cap_rep = B.caption_beats(m, ws, clean_rep)
    CAP.assert_law12(cap_y, max(b["w"] for b in beats))
    band = B.guard_core_band(top, k, cap_y)
    rail = B.guard_rail()
    objs = B.phone_objects()

    scene, tweens = SC.build(B.media(), B.outro_lockup("tiktok_ig"))
    checks["draw_on"] = B.assert_draw_on(tweens, scene)
    checks["law40"] = B.assert_connectors(scene)
    scene, checks["law40_law38_declared"] = B.declare_contracts(scene)
    for shape in ("<circle", "<ellipse"):
        if shape in scene:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the scene")

    # THE DEPTH FIELD (chassis constants; cast is the plan's)
    bf = json.loads((HERE / f"_df/bandframes_{VID}.json").read_text())
    if bf.get("source_sha256") != env["source_sha256"]:
        raise SystemExit("band frames measured on a different alpha")
    y0, seat = DF.seat(bf, cap_bottom=cap_y + CAP.CAP_PILL_HEIGHT / 2,
                       plate_top=box["top"], plate_scale=round(box["h"] / 900.0, 4),
                       plate_left=box["left"])
    lanes = DF.lanes_at(y0)
    steps = DF.step_beats(ws, DUR, n=STEP_N, fps=FPS)
    cast = list(DEPTH_FILES)
    if set(FIELD_ORDER) != set(cast) or len(FIELD_ORDER) % 7 == 0:
        raise SystemExit("FIELD_ORDER is not the plan's roster in a coprime length")
    field, lane_geom, n_tiles = DF.field(lanes, st["urls"], FIELD_ORDER, len(steps),
                                         rec=lambda *a, **kw: None)
    lane_mix = {}
    for chunk in field.split('class="abs lanewrap"')[1:]:
        name = re.search(r'id="lw-([^"]+)"', chunk).group(1)
        keys = re.findall(r'assets/logos/([^"]+)', chunk)
        lane_mix[name] = sorted(set(keys))
        if len(set(keys)) < len(cast):
            raise SystemExit(f"lane {name} carries {sorted(set(keys))}, not the "
                             "whole roster")
        if any(a == b for a, b in zip(keys, keys[1:])):
            raise SystemExit(f"lane {name} puts a mark beside itself")
    tweens = list(tweens) + DF.schedule(lanes, steps, ease=EASE)
    tweens += [f'tl.set("#lw-{n}",{{opacity:0}},0);' for n, *_ in lanes]
    tweens += [f'tl.to("#lw-{n}",{{opacity:1,duration:0.52,ease:{EASE}}},'
               f'{HOOK_CLEAR + i * 0.10:.2f});' for i, (n, *_) in enumerate(lanes)]
    if any(re.search(r"ease:SOFT\b", t) for t in tweens):
        raise SystemExit("an undeclared SOFT ease reached the page")
    # a depth mark may never be SPOKEN as itself
    spoken = " ".join(w["text"] for w in ws).lower()
    named = [c for c in cast if re.search(rf"\b{re.escape(c)}\b", spoken)]
    if named:
        raise SystemExit(f"a depth mark is spoken in the take: {named}")

    body = [
        f'<div class="abs ground" style="left:0;top:0;width:{int(W)}px;'
        f'height:{int(H)}px;background:{SC.CREAM}"></div>',
        f'<section id="tz-cut" class="clip" data-start="0" data-duration="{DUR}" '
        f'data-track-index="2" style="left:0;top:0;width:{int(W)}px;height:{int(H)}px">',
        f'<div class="abs core" id="core" data-container style="left:{left}px;'
        f'top:{top}px;width:{SC.CORE_W:.0f}px;height:{SC.CORE_H:.0f}px;'
        f'transform:scale({k})">',
        scene, "</div></section>",
        f'<div class="abs" id="lanes" data-overlap-ok data-bleed style="left:0;top:0;'
        f'width:{int(W)}px;height:{int(H)}px">' + field + "</div>",
    ]
    for name, file, z, filt in (
            ("matte-rim", "matte_rim.webm", 59,
             "filter:drop-shadow(0 10px 26px rgba(0,0,0,.20));"),
            ("matte", "matte.webm", 60, "")):
        body.append(
            f'<video id="{name}" src="assets/v/{file}" data-start="0" '
            f'data-duration="{DUR}" data-media-start="0" data-track-index="{z}" '
            f'muted playsinline style="position:absolute;left:{int(box["left"])}px;'
            f'top:{int(box["top"])}px;width:{int(box["w"])}px;'
            f'height:{int(box["h"])}px;{filt}"></video>')
    body += [B.caption_html(beats, cap_y), B.audio_html(SFX)]
    page = B.head(B.TITLE, "") + "\n".join(body) + B.tail(tweens)
    edge_fade = CC.guard_edge_fade(page)
    (OUT / "index.html").write_text(page, encoding="utf-8")

    report = {
        "video": VID, "format": "cutout", "platform": "tiktok", "fps": FPS,
        "duration": DUR, "seal": seal, "plate": plate, "seat": cap_y,
        "envelope": env["seats"], "crown_gate": env["crown_gate"],
        "core": place_rec, "band": band, "rail": rail,
        "voice": st["voice"], "matte": {"session": str(S), "layers": st["layers"],
                                        "hashes": st["ship"]["hashes"],
                                        "backend": "matanyone2",
                                        "selection_mask_sha256": st["selection_mask_sha256"],
                                        "astra_review": st["astra_review"],
                                        "headroom": st["matting_headroom"]},
        "depth_field": {"seat": seat, "lanes": lane_geom, "tiles": n_tiles,
                        "step_beats": steps, "step_n": STEP_N, "cast": cast,
                        "files": DEPTH_FILES, "field_order": FIELD_ORDER,
                        "lane_mix": lane_mix,
                        "hook_clear_s": HOOK_CLEAR,
                        "intro_dur": DF.INTRO_DUR, "pop_behind": None,
                        "pop_behind_why_none": "the products he names are Hermes "
                        "(the Nous girl, a stage mark) and Firecrawl (a stage "
                        "mark); AnyDoc has no mark of its own. The depth field "
                        "never carries the story's own marks."},
        "shared": {"beat_edges": SC.BEAT_EDGES, "phone_test_objects": objs},
        "captions": {"n": len(beats), "texts": [b["text"] for b in beats],
                     "widest_px": round(max(b["w"] for b in beats), 1)},
        "caption_beats": beats, "transcript": cap_rep, "checks": checks,
        "cast_check": st["cast_check"], "edge_fade": edge_fade,
        "handle": CAP.handle("tiktok_ig"), "render": {"w": 1080, "h": 1920, "zoom": 1}}
    for name in ("_build", "_geom"):
        (HERE / f"{name}_{VID}_cutout.json").write_text(
            json.dumps(report, indent=1, default=str))

    qc = ["--voice-master", str(CUT / "audio.m4a")]
    for o in objs:
        qc += ["--phone-at", f'{o["t"]}:' + ",".join(map(str, o["bbox"]))
               + f':{o["name"]}']
    qc += ["--alpha", str(S / f"matte_{VID}_v5_alpha.webm"),
           "--edge-box", f'{int(box["w"])}x{int(box["h"])}+{int(box["left"])}'
           f'+{int(box["top"])}',
           "--plate", str(S / f'plate_display_{int(box["w"])}x{int(box["h"])}.mp4')]
    job = {"project": str(OUT), "vid": VID, "fmt": "cutout", "quality": "high",
           "stage": str(RUN / f"staging/tiktok/{VID}_cutout.mp4"), "qc_args": qc}
    print(json.dumps({"project": str(OUT), "plate": plate["box"], "seat": cap_y,
                      "core": place_rec, "band": band, "silhouette": sil,
                      "hook_clear": HOOK_CLEAR, "steps": steps, "lanes_y0": y0,
                      "seat_rec": seat, "lane_mix": lane_mix,
                      "captions": report["captions"]["texts"],
                      "job": job}, indent=1, default=str))


if __name__ == "__main__":
    main()
