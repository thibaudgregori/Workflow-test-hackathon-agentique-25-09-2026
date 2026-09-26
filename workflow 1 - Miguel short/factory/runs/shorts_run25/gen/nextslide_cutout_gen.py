#!/usr/bin/env python3
"""CUTOUT -> TIKTOK for nextslide.  Composes the SEALED scene and the SHIPPED matte.

    TikTok   cutout   projects/nextslide_cutout   @migueltorrez.ai

The lane scene is consumed, never re-authored: `gen/nextslide_scene.py` plus
`plans/nextslide_scene_handoff.md`, sealed by `review/artwork_pass_nextslide.json`
(both hashes asserted below).  The split generator is imported for its caption,
cue, word-sync, label, lifetime, spacing, connector and emphasis contracts;
importing it never builds or rewrites the split page.

Per-body geometry comes from `gen/nextslide_cutout_envelope.py` (the envelope
sweep of the shipped `_alpha.webm`, every frame).  The plate box is READ from
plate.json's over-wide block (1584x990 at -351, 930), never centred.

THE LANES ARRIVE WHEN THE HOOK HAS LANDED: the wrappers fade in at
HOOK_CLEAR = SC.CUE["keyterm"] (1.80 s, AI PRESENTATIONS written on the end of
"AI sucks at creating presentations"), one lane 0.10 s after the other.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import nextslide_split_gen as B  # noqa: E402

CAP, CC, DF, SC = B.CAP, B.CC, B.DF, B.SC
RUN, F = B.RUN, B.F
VID = "nextslide"
S = RUN / f"matting/{VID}"
OUT = RUN / f"projects/{VID}_cutout"
W, H, DUR, FPS = B.W, B.H, B.DUR, B.FPS

HOOK_CLEAR = SC.CUE["keyterm"]          # 1.80: the hook has landed
# ONE STEP PER SPOKEN BEAT at the foundation's pulse (grokpublish: 12 steps over
# 40.8 s, lead 1.6 / tail 1.2 -> 3.17 s per step).  (33.2 - 2.8) / 3.17 = 9.6 -> 10.
STEP_N = round((DUR - 2.8) / ((40.8 - 2.8) / 12))
LANE_FILES = dict(SC.CUTOUT_LANE_FILES)
CAST = list(SC.CUTOUT_LOGO_LANES)
STAGE_MARKS = {"nextslide", "openai", "chatgpt", "claude", "gemini", "grok"}


def digest(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def guard_plate_box(box: dict, layers: dict) -> dict:
    for key in ("w", "h", "left", "top"):
        if box[key] != int(box[key]):
            raise SystemExit(f"plate box {key}={box[key]} is not a whole pixel")
    for name, wh in layers.items():
        if (wh["w"], wh["h"]) != (box["w"], box["h"]):
            raise SystemExit(f"layer {name} is {wh}, the box is {box}")
    return {"box": box, "whole_pixels": True, "equals_encoded": layers}


def stage_assets() -> dict:
    for sub in ("v", "music", "sfx", "logos"):
        (OUT / f"assets/{sub}").mkdir(parents=True, exist_ok=True)
    v = OUT / "assets/v"
    ship = json.loads((S / "ship_v5.json").read_text())
    layers = {}
    for key, name in (("cut", "matte.webm"), ("rim", "matte_rim.webm")):
        src = S / f"matte_{VID}_v5_{key}.webm"
        if digest(src) != ship["hashes"][key]:
            raise SystemExit(f"{src.name} does not match ship_v5.json")
        shutil.copy2(src, v / name)
        if digest(v / name) != ship["hashes"][key]:
            raise SystemExit(f"staged {name} does not match the shipped layer")
        st = src.stat()
        (v / f"_{name}.src").write_text(f"{src}\n{st.st_size} {st.st_mtime_ns}")
        layers[key] = B.probe_wh(v / name)
    st = (S / f"matte_{VID}_v5_cut.webm").stat()
    (v / "_matte_source.txt").write_text(
        f"{S / f'matte_{VID}_v5_cut.webm'}\n{st.st_size} {st.st_mtime_ns}")
    shutil.copy2(B.CUT / "audio.m4a", v / "voice.m4a")
    voice = {"source": str(B.CUT / "audio.m4a"), **B.probe_audio(v / "voice.m4a")}
    if voice["sample_rate"] < 44100:
        raise SystemExit(f"staged voice is {voice['sample_rate']} Hz")
    shutil.copy2(B.LIB_MUSIC / "bed_split_v2.mp3", OUT / "assets/music/bed.mp3")
    for name in ("whoosh", "pop", "click"):
        shutil.copy2(B.LIB_SFX / f"{name}.mp3", OUT / f"assets/sfx/{name}.mp3")
    urls = {}
    for key, rel in {**B.STAGE_FILES, **LANE_FILES}.items():
        src = B.LOGOS / rel
        if not src.exists():
            raise SystemExit(f"registry key {key!r} does not resolve: {src}")
        shutil.copy2(src, OUT / "assets/logos" / src.name)
        if key != "nextslide":
            CC.MARK_INK[key] = CC.measure_mark(key, src)
        urls[key] = f"assets/logos/{src.name}"
    return {"ship": ship, "layers": layers, "voice": voice, "urls": urls}


def main() -> None:
    # ---- the seal, the matte, the headroom
    seal = json.loads((RUN / f"review/artwork_pass_{VID}.json").read_text())
    if seal.get("verdict") != "PASS":
        raise SystemExit("the scene is not sealed")
    for p in (HERE / f"{VID}_scene.py", RUN / f"plans/{VID}_scene_handoff.md"):
        if seal["evidence"][str(p)] != digest(p):
            raise SystemExit(f"stale scene seal: {p}")
    matting = json.loads((S / "matting.json").read_text())
    hr = matting["headroom"]
    if not hr["pass"] or hr["unsafe_frames"]:
        raise SystemExit("the matte's headroom guard does not pass")
    env = json.loads((HERE / f"_envelope_{VID}.json").read_text())
    st = stage_assets()
    if env["source_sha256"] != st["ship"]["hashes"]["alpha"]:
        raise SystemExit("the envelope was measured on another alpha")
    box = json.loads((S / "plate.json").read_text())["overwide"]["plate_box"]
    plate = guard_plate_box({k: box[k] for k in ("w", "h", "left", "top")},
                            st["layers"])
    edge_box = f'{int(box["w"])}x{int(box["h"])}+{int(box["left"])}+{int(box["top"])}'

    # ---- the cast
    plan = json.loads(B.PLAN.read_text())
    if CAST != plan["cutout_logo_lanes"]:
        raise SystemExit(f"lane cast {CAST} is not the plan's {plan['cutout_logo_lanes']}")
    if set(CAST) & STAGE_MARKS:
        raise SystemExit("a stage mark is in the depth cast")
    cast_rep = DF.assert_cast_resolves(CAST, LANE_FILES, B.LOGOS, label="nextslide lanes")

    # ---- the seat: stage zone from the envelope, core centred in it
    cap_y, zy0, zy1 = (env["seats"][k] for k in ("CAP_Y", "ZY0", "ZY1"))
    band_h = SC.CONTENT_Y1 - SC.CONTENT_Y0
    k = min(1.0, (zy1 - zy0 - 16) / band_h)
    top = round((zy0 + zy1) / 2 - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
    left = (W - SC.CORE_W * k) / 2
    B.CORE_K, B.CORE_TOP_SPLIT, B.LEFT = k, top, left

    # ---- the contracts, re-run against this seat
    ws, clean_rep = B.clean_tokens(B.words())
    rep = {"cues": B.assert_cues(ws), "word_sync": B.assert_word_sync(ws),
           "law37": B.assert_law37(ws), "law39": B.assert_label_law(),
           "law42": B.assert_lifetime_law(), "law41": B.assert_spacing_law(),
           "law38": B.assert_emphasis_law(), "law2": B.assert_cast_law()}
    sfx = B.sfx_plan()
    rep["law22"] = B.assert_sfx(sfx)
    media = B.media()
    scene_html, tweens = SC.build(media, B.outro_lockup("tiktok_ig"))
    rep["law40"] = B.assert_anchor_law(scene_html)
    scene_html, rep["declared"] = B.declare_contracts(scene_html, rep["law40"])
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or emphasis is missing its check instant")

    m = CAP.PillMeasurer(HERE / f"_pillwidths_{VID}_cutout.json")
    beats, cap_rep = B.caption_beats(m, ws, clean_rep)
    CAP.assert_law12(cap_y, max(b["w"] for b in beats))
    rep["band"] = B.guard_core_band(top, k, cap_y)
    rep["rail"] = B.guard_rail()

    # ---- THE DEPTH FIELD (chassis constants; the cast is the only choice)
    bf = json.loads((HERE / f"_df/bandframes_{VID}.json").read_text())
    if bf["source_sha256"] != env["source_sha256"]:
        raise SystemExit("band frames were measured on another alpha")
    y0, seat = DF.seat(bf, cap_bottom=cap_y + CAP.CAP_PILL_HEIGHT / 2,
                       plate_top=box["top"], plate_scale=box["h"] / 900.0,
                       plate_left=box["left"])
    lanes = DF.lanes_at(y0)
    steps = DF.step_beats(ws, DUR, n=STEP_N, fps=FPS)
    field, geom, n_tiles = DF.field(lanes, st["urls"], CAST, len(steps),
                                    rec=lambda *a, **kw: None)
    tweens += DF.schedule(lanes, steps)
    # the hook is the subject, not the wall: lanes come in once it has landed
    tweens += [f'tl.set("#lw-{n}",{{opacity:0}},0);' for n, *_ in lanes]
    tweens += [f'tl.to("#lw-{n}",{{opacity:1,duration:0.52,ease:SOFT}},'
               f'{HOOK_CLEAR + i * 0.10:.2f});' for i, (n, *_) in enumerate(lanes)]

    body = [
        f'<div class="abs ground" style="left:0;top:0;width:{int(W)}px;'
        f'height:{int(H)}px;background:{SC.CREAM}"></div>',
        f'<section id="tz-cut" class="clip" data-start="0" data-duration="{DUR}" '
        f'data-track-index="2" style="left:0;top:0;width:{int(W)}px;height:{int(H)}px">',
        f'<div class="abs core" id="core" data-container style="left:{left}px;'
        f'top:{top:.2f}px;width:{SC.CORE_W:.0f}px;height:{SC.CORE_H:.0f}px;'
        f'transform:scale({k})">',
        scene_html, "</div></section>",
        f'<div id="lanes" class="abs" data-overlap-ok data-bleed style="left:0;top:0;'
        f'width:{int(W)}px;height:{int(H)}px">' + field + "</div>",
    ]
    for name, file, z, filt in (
            ("matte-rim", "matte_rim.webm", 59,
             "filter:drop-shadow(0 10px 26px rgba(0,0,0,.20));"),
            ("matte", "matte.webm", 60, "")):
        body.append(
            f'<video id="{name}" src="assets/v/{file}" data-start="0" '
            f'data-duration="{DUR}" data-media-start="0" data-track-index="{z}" muted '
            f'playsinline style="position:absolute;left:{int(box["left"])}px;'
            f'top:{int(box["top"])}px;width:{int(box["w"])}px;'
            f'height:{int(box["h"])}px;{filt}"></video>')
    body += [B.caption_html(beats, cap_y), B.audio_html(sfx)]
    page = B.head(B.TITLE, "") + "\n".join(body) + B.tail(tweens)
    edge_fade = CC.guard_edge_fade(page)
    (OUT / "index.html").write_text(page, encoding="utf-8")

    objs = B.phone_objects()
    report = {
        "video": VID, "format": "cutout", "fps": FPS, "duration": DUR,
        "plate": plate, "edge_box": edge_box, "seat": cap_y,
        "core": {"left": left, "top": top, "scale": k},
        "envelope": env["seats"], "crown_gate": env["crown_gate"],
        "voice": st["voice"],
        "depth_field": {"seat": seat, "lanes": geom, "tiles": n_tiles,
                        "step_beats": steps, "step_n": STEP_N, "cast": CAST,
                        "hook_clear_s": HOOK_CLEAR, "intro_dur": DF.INTRO_DUR,
                        "pop_behind": None,
                        "reason": "The only tools this take names (OpenAI, "
                                  "NextSlide, ChatGPT, Claude, Gemini, Grok) are "
                                  "stage marks, which stay out of the depth field."},
        "matte": {"session": str(S), "layers": st["layers"],
                  "hashes": st["ship"]["hashes"], "headroom": hr},
        "phone_objects": objs, "captions": {"n": len(beats),
                                            "texts": [b["text"] for b in beats],
                                            "widest_px": round(max(b["w"] for b in beats), 1)},
        "transcript": cap_rep, "checks": rep, "cast": cast_rep,
        "edge_fade": edge_fade, "handle": CAP.handle("tiktok_ig")}
    for name in ("_build", "_geom"):
        (HERE / f"{name}_{VID}_cutout.json").write_text(
            json.dumps(report, indent=1, default=str))
    print(json.dumps({"project": str(OUT), "plate": plate, "seat": cap_y,
                      "core": report["core"], "band": rep["band"],
                      "lanes_y0": y0, "steps": steps, "hook_clear": HOOK_CLEAR,
                      "captions": len(beats), "phone": objs,
                      "edge_box": edge_box}, indent=1, default=str))


if __name__ == "__main__":
    main()
