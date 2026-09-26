"""Build-time geometry audit: enforce STANDARD.md geometry laws on the live DOM, pre-render.

Loads a HyperFrames project in headless Chromium, seeks the real GSAP timeline
(window.__timelines["main"]) through the whole composition, measures actual bounding
boxes, and checks the machine-checkable laws:

  clipped      element extends past its zone edge (overflow:hidden will cut it)
  collision    two visible atoms intersect (rings/annotations exempt)
  unequal      same-class tile/node grids differ in size or break grid alignment
  margin       static content hugging the frame edge (<20px)
  seam         top-zone content within 24px of the caption seam (862.5)
  floating     connector bar whose end touches no box edge (underlines exempt)
  offcenter    centered text whose box is not actually centered
  glyph        ERROR: a plate's single glyph (img/svg) off the plate centre, OR a
               glyph in a COMPOSED card that near-misses an axis (within 15% of
               centre but outside 2px tolerance = intended-centred-plus-bug;
               deliberate side placements sit far off-axis and are never judged)
  edgefade     ERROR: GLOBAL LAW 8 — a painted box STRADDLES a frame edge with no
               alpha mask on it or any ancestor, i.e. it is hard-chopped by the
               frame instead of fading out. Measured on the emitted DOM, so it
               holds whichever generator built the page (`data-bleed` opts out)
  ghost        an atom in an active clip never reaches 1px size across the whole
               timeline (broken geometry — e.g. a connector span authored with
               x0 > x1 renders at negative width and simply does not exist)

A violation only counts when it persists across >=2 consecutive samples with the
element static (transition frames are never flagged). Violations get annotated
screenshots. Exit code 1 on errors, 0 when clean (warnings never fail the build).

Usage:
  geometry_audit.py <project_dir> [--step 0.5] [--out <dir>] [--no-shots]

Opt-outs (set by generators where a law legitimately does not apply):
  data-overlap-ok   element may overlap others (e.g. badge on a card corner)
  data-bleed        element may touch/exceed frame or zone edges
  data-glyph-ok     this plate's glyph is deliberately off-centre (asymmetric composition)
"""
import argparse
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

STEP_DEFAULT = 0.5
SEAM_Y = 862.5
FRAME_W = 1080
EDGE_MARGIN = 20
SEAM_MARGIN = 24
STATIC_EPS = 4.0        # rect moved less than this between samples = static
MIN_OVERLAP_PX = 3.0    # w and h of intersection must both exceed this
MIN_OVERLAP_FRAC = 0.02 # ...and area must exceed 2% of the smaller atom
SIZE_TOL = 1.5          # equal-group size tolerance
GRID_TOL = 1.5          # grid row/col alignment tolerance
CENTER_TOL = 4.0
CONNECTOR_END_TOL = 14.0
# Glyph centring (Miguel, 2026-08-12). Calibrated over six known-good projects at 0.5s
# steps - grokprice_icon 0.00, meatwrapper_icon 0.00, deepresearch_icon 0.01, hermes_icon
# 0.01 (46 plates), erdos_counter 0.05, agentreviews_icon 0.10 - against the defect class,
# an absolutely positioned glyph inset from the plate's PADDING box while its size assumed
# the border box: grokpublish_icon v3 measured 3.75px (exactly the plate's border width)
# and hermesjourney_icon measures 3.05px. 2.0 sits 20x above the clean-project noise floor
# and still catches the class. NOT 4.0: the defect it exists for is 3.75px, so a 4px gate
# would be blind to it. Warning only - it never fails a build.
GLYPH_CENTER_TOL = 2.0
GLYPH_MIN_PLATE = 40.0   # below this a "plate" is a chip/dot, not a card
# Composed-card near-miss centring (Miguel, 2026-08-13 — Law 15). A glyph whose
# centre lands within this fraction of the card's span from the card centre is
# read as INTENDED centred; outside the band it is a deliberate side placement
# (avatar beside copy lines: ~25-40% off-axis) and is never judged. Both the
# solo and near-miss checks are ERRORS now: real defects measured 3.05-3.75px
# against a 0.00-0.10px clean-project floor, and warning-only let one ship.
GLYPH_NEAR_MISS_FRAC = 0.15
GLYPH_MIN_SIZE = 16.0    # smaller svg/img children are decoration, not glyphs

SNAPSHOT_JS = r"""
(t) => {
  const tl = window.__timelines && window.__timelines["main"];
  if (!tl) return { error: "no timeline" };
  tl.pause();
  tl.seek(t, false);
  const root = document.getElementById("root");
  const clips = Array.from(root.children).filter(el => el.dataset && el.dataset.start !== undefined);
  const active = [];
  for (const c of clips) {
    const s = parseFloat(c.dataset.start), d = parseFloat(c.dataset.duration);
    const on = t >= s - 0.01 && t < s + d - 0.01;
    c.style.visibility = on ? "visible" : "hidden";
    if (on && c.tagName !== "VIDEO") active.push(c);
  }
  const effOpacity = (el, stopAt) => {
    let o = 1, n = el;
    while (n && n !== stopAt.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.display === "none") return 0;
      o *= parseFloat(cs.opacity);
      n = n.parentElement;
    }
    return o;
  };
  const out = [];
  const ghosts = [];
  for (const sec of active) {
    const srect = sec.getBoundingClientRect();
    const atoms = Array.from(sec.children);
    for (const a of atoms) {
      const cs = getComputedStyle(a);
      const op = effOpacity(a, sec);
      if (op < 0.15 || cs.visibility === "hidden") continue;
      const r = a.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) {
        // Sub-1px atoms used to be skipped silently, which made a connector
        // authored with x0 > x1 (negative width) invisible to every check —
        // four of eight structural links can be missing while the audit says
        // "0 errors". Record the skip as a ghost sighting unless some element
        // child actually renders (a zero-size positioning wrapper is fine).
        let childVisible = false;
        for (const k of a.querySelectorAll("*")) {
          const kr = k.getBoundingClientRect();
          if (kr.width >= 1 && kr.height >= 1) { childVisible = true; break; }
        }
        if (!childVisible)
          ghosts.push({ id: a.id || null, sec: sec.id, cls: (a.getAttribute("class") || "") });
        continue;
      }
      const ruleEl = a.querySelector(":scope > .rule, :scope > .ruleY") ||
                     ((a.classList.contains("rule") || a.classList.contains("ruleY")) ? a : null);
      const hasRule = !!ruleEl;
      let ruleRect = null;
      if (ruleEl) {
        const rr = ruleEl.getBoundingClientRect();
        ruleRect = { x: rr.left, y: rr.top, w: rr.width, h: rr.height };
      }
      const bg = (cs.backgroundColor !== "rgba(0, 0, 0, 0)" &&
                  cs.backgroundColor !== "transparent") ||
                 parseFloat(cs.borderTopWidth) > 0;
      let contentRect = null;
      // Range rects ignore overflow clipping: an odometer wrapping a tall roll
      // strip would measure 5x its visible height. Keep the layout box there.
      const clips = ["hidden", "clip"].includes(cs.overflowY) ||
                    ["hidden", "clip"].includes(cs.overflowX);
      if (!bg && !clips) {
        try {
          const rg = document.createRange();
          rg.selectNodeContents(a);
          const rr = rg.getBoundingClientRect();
          if (rr.width > 0 && rr.height > 0)
            contentRect = { x: rr.left, y: rr.top, w: rr.width, h: rr.height };
        } catch (e) {}
      }
      let upscaled = null;
      for (const img of a.querySelectorAll("img")) {
        const ir = img.getBoundingClientRect();
        if (img.naturalWidth > 0 && ir.width >= 240 &&
            ir.width > img.naturalWidth * 1.15) {
          upscaled = { natural: img.naturalWidth, rendered: Math.round(ir.width) };
          break;
        }
      }
      // A plate whose ONLY content is one glyph must centre it. Measure the glyph's own
      // border box against the plate's: the two are concentric by construction in a
      // correct build, so any drift is a real authoring error (an inset measured from the
      // padding box instead of the border box, an odd pad, a stale offset).
      // The "only content" test is strict on purpose - it counts EVERY visible child
      // element, not just glyphs. A card that also carries a title bar, copy lines or a
      // badge is a COMPOSITION: its glyph is centred in the space its chrome leaves, and
      // reading that as a centring claim produced the two calibration false positives
      // (agentreviews s3-t*, a logo under a terminal title bar; hermesjourney c-card, an
      // avatar beside copy lines).
      let glyph = null;
      let glyphs = [];
      if (a.dataset.glyphOk === undefined) {
        const kids = Array.from(a.children).filter(k => {
          const kcs = getComputedStyle(k);
          if (kcs.display === "none" || kcs.visibility === "hidden" ||
              parseFloat(kcs.opacity) < 0.15) return false;
          const kr = k.getBoundingClientRect();
          return kr.width > 1 && kr.height > 1;
        });
        if (kids.length === 1 && ["svg", "img"].includes(kids[0].tagName.toLowerCase())) {
          const kr = kids[0].getBoundingClientRect();
          glyph = { x: kr.left, y: kr.top, w: kr.width, h: kr.height,
                    tag: kids[0].tagName.toLowerCase() };
        }
        // Composed cards too (2026-08-13): every visible svg/img child is
        // reported, so Python can run the near-miss centring check on cards
        // that also carry labels/chrome — the smallteams person glyphs escaped
        // because the strict only-content test above skipped them entirely.
        for (const k of kids) {
          const tag = k.tagName.toLowerCase();
          if (!["svg", "img"].includes(tag)) continue;
          const kr = k.getBoundingClientRect();
          glyphs.push({ x: kr.left, y: kr.top, w: kr.width, h: kr.height, tag: tag });
        }
      }
      out.push({
        ruleRect: ruleRect,
        cr: contentRect,
        upscaled: upscaled,
        glyph: glyph,
        glyphs: glyphs,
        plateLike: a.classList.contains("ltile") || a.classList.contains("node") ||
                   a.classList.contains("shot") ||
                   (bg && parseFloat(cs.borderTopLeftRadius) > 0),
        id: a.id || null,
        cls: (a.getAttribute("class") || ""),
        sec: sec.id,
        sec_cls: (sec.getAttribute("class") || ""),
        secTop: srect.top, secBot: srect.bottom, secL: srect.left, secR: srect.right,
        x: r.left, y: r.top, w: r.width, h: r.height,
        op: op,
        text: (a.innerText || "").trim().slice(0, 40),
        align: cs.textAlign,
        isRing: a.classList.contains("ring"),
        isRule: hasRule,
        isBox: a.classList.contains("ltile") || a.classList.contains("node") ||
               a.classList.contains("shot") || a.classList.contains("chip"),
        hasBg: bg,
        rotated: (() => {
          const m = cs.transform;
          if (!m || m === "none") return false;
          const p = m.match(/matrix\(([^)]+)\)/);
          if (!p) return false;
          return Math.abs(parseFloat(p[1].split(",")[1])) > 0.01;
        })(),
        overlapOk: a.dataset.overlapOk !== undefined,
        bleedOk: a.dataset.bleed !== undefined,
      });
    }
  }
  return { atoms: out, ghosts: ghosts };
}
"""


EDGEFADE_JS = r"""
(t) => {
  const tl = window.__timelines && window.__timelines["main"];
  if (!tl) return [];
  tl.pause();
  tl.seek(t, false);
  const root = document.getElementById("root");
  for (const c of Array.from(root.children)) {
    if (!c.dataset || c.dataset.start === undefined) continue;
    const s = parseFloat(c.dataset.start), d = parseFloat(c.dataset.duration);
    c.style.visibility = (t >= s - 0.01 && t < s + d - 0.01) ? "visible" : "hidden";
  }
  const rr = root.getBoundingClientRect();
  const W = rr.width, H = rr.height, EPS = 0.75;
  const SKIP = new Set(["video", "audio", "source", "script", "style", "track"]);
  // an alpha fade anywhere up the chain satisfies the law: the pixels this
  // element paints at the frame edge are ramped by SOME ancestor's mask.
  const exempt = (el) => {
    let n = el;
    while (n && n !== root.parentElement) {
      if (n.dataset && n.dataset.bleed !== undefined) return true;
      const cs = getComputedStyle(n);
      const m = cs.maskImage || cs.webkitMaskImage;
      if (m && m !== "none") return true;
      n = n.parentElement;
    }
    return false;
  };
  // AN <svg> IS JUDGED BY ITS INK, NOT BY ITS CANVAS.  Every svg in this
  // factory is authored `width:100% height:100%` inside its own box, so its
  // layout rect says nothing about where it paints; run 9's takeover has one
  // whose box spans -86..2246 and whose drawing sits comfortably inside the
  // frame.  getBBox() is the union of what it actually draws, in user units;
  // getScreenCTM maps that to the page.
  const inkRect = (el) => {
    const r = el.getBoundingClientRect();
    if (el.tagName.toLowerCase() !== "svg") return r;
    try {
      const bb = el.getBBox(), m = el.getScreenCTM();
      if (!m || bb.width <= 0 || bb.height <= 0) return r;
      const p = el.createSVGPoint();
      let xs = [], ys = [];
      for (const [dx, dy] of [[0, 0], [bb.width, 0], [0, bb.height],
                              [bb.width, bb.height]]) {
        p.x = bb.x + dx; p.y = bb.y + dy;
        const q = p.matrixTransform(m);
        xs.push(q.x); ys.push(q.y);
      }
      return { left: Math.min(...xs), top: Math.min(...ys),
               width: Math.max(...xs) - Math.min(...xs),
               height: Math.max(...ys) - Math.min(...ys) };
    } catch (e) { return r; }
  };
  // WHAT REACHES THE EDGE, NOT WHAT THE LAYOUT BOX CLAIMS.  A meter fill is
  // authored 825px wide and slid inside a 300px track: its own box runs to
  // -499, but the track (overflow:hidden, entirely inside the frame) already
  // cut it and the frame edge never touches it.  So every ancestor clip EXCEPT
  // #root is applied first — #root is excluded on purpose, because #root IS
  // the frame edge and clipping by it would erase the very violation.
  const visibleRect = (el) => {
    let r = inkRect(el);
    let box = { l: r.left, t: r.top, r: r.left + r.width, b: r.top + r.height };
    let n = el.parentElement;
    while (n && n !== root) {
      const cs = getComputedStyle(n);
      if (["hidden", "clip", "scroll", "auto"].includes(cs.overflowX) ||
          ["hidden", "clip", "scroll", "auto"].includes(cs.overflowY)) {
        const p = n.getBoundingClientRect();
        box.l = Math.max(box.l, p.left); box.t = Math.max(box.t, p.top);
        box.r = Math.min(box.r, p.right); box.b = Math.min(box.b, p.bottom);
      }
      n = n.parentElement;
    }
    return { left: box.l, top: box.t,
             width: box.r - box.l, height: box.b - box.t };
  };
  const out = [], flagged = [];
  for (const el of root.querySelectorAll("*")) {
    const tag = el.tagName.toLowerCase();
    if (SKIP.has(tag)) continue;
    if (el.ownerSVGElement) continue;      // svg internals: the <svg> speaks for them
    const r = visibleRect(el);
    if (r.width < 2 || r.height < 2) continue;
    const x0 = r.left - rr.left, x1 = x0 + r.width;
    const y0 = r.top - rr.top, y1 = y0 + r.height;
    // STRADDLING an edge is the violation.  Fully off-canvas is invisible and
    // fully inside is not cut; only a box with pixels on both sides of the
    // frame line is being CHOPPED by it.
    const crossX = (x0 < -EPS && x1 > EPS) || (x1 > W + EPS && x0 < W - EPS);
    const crossY = (y0 < -EPS && y1 > EPS) || (y1 > H + EPS && y0 < H - EPS);
    if (!crossX && !crossY) continue;
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") continue;
    // a bare positioning wrapper paints nothing, so nothing of it is chopped
    const painted = (cs.backgroundColor !== "rgba(0, 0, 0, 0)" &&
                     cs.backgroundColor !== "transparent") ||
                    parseFloat(cs.borderTopWidth) > 0 ||
                    ["img", "svg"].includes(tag) ||
                    (el.childElementCount === 0 &&
                     (el.textContent || "").trim().length > 0);
    if (!painted) continue;
    let o = 1, n = el;
    while (n && n !== root.parentElement) {
      o *= parseFloat(getComputedStyle(n).opacity);
      n = n.parentElement;
    }
    if (o < 0.15) continue;
    if (exempt(el)) continue;
    if (flagged.some(f => f.contains(el))) continue;   // report the OUTERMOST
    flagged.push(el);
    const name = el.id || el.getAttribute("class") || tag;
    out.push({
      key: el.id || `${name}@${Math.round(x0)},${Math.round(y0)}`,
      detail: `${name} is cut by the frame edge with no alpha fade ` +
              `(box ${Math.round(x0)}..${Math.round(x1)} x ` +
              `${Math.round(y0)}..${Math.round(y1)})`,
    });
  }
  return out;
}
"""


# =============================================================================
# ROUND-4 LAYOUT LAWS (Miguel, 2026-09-02) — measured on the EMITTED DOM
# =============================================================================
# Round 4 rejected four things the old atom model could not even see, because it
# only ever looked at a clip's DIRECT children — and every run-9 generator wraps
# its scene in one positioned <div> or one <svg>, so `check_sample` was judging
# ONE atom per clip.  This lane walks the whole subtree of every active clip and
# judges the elements that carry an `id`: in this factory an id is the author
# saying "this is a thing", and id-less SVG internals (tick rows, dot grids,
# glyph sub-paths) are strokes of a drawing, not objects in an argument.
#
#   cramp       LAW 5 — two objects with a positive gutter under CRAMP_ERR_PX
#   crossing    LAW 5 — a connector's line passes through printed type
#   enclose     LAW 38 — the WRONG emphasis for the target: a ring/ellipse
#               around anything, or a box drawn on IMAGE TEXT (a box around a
#               DRAWN object is legal; a misplaced highlight is a warning)
#   sidelabel   LAW 3 — a name placed beside its object instead of above/below
#   anchorline  LAW 4 — connectors into one target landing at different heights
#
# CALIBRATION (2026-09-02, measured over the three approved round-4 references
# and the two rejected impossibletask pages, 0.5 s steps):
#   impossibletask_split   b3-codexlbl | b3-panel     2.0 px   <- Miguel's cramp
#   perplexityprojects_cutout (APPROVED)  floor      19.3 px
#   kimiram_split             (APPROVED)  floor      25.0 px
# Miguel's stated aim is 24 px.  At 24 px the approved cutout reports a pair, so
# the REFUSAL line is 16 px — the largest round value strictly under the approved
# floor, and the same frame-space number the whiteboard harness uses (8.5 board
# units).  24 px stays the number the PLAN aims for and the clerk reads.
CRAMP_ERR_PX = 16.0
CRAMP_AIM_PX = 24.0
LABEL_WELD_PX = 60.0      # how far a name may sit from the thing it names
LABEL_AXIS_FRAC = 0.15    # Miguel: the name's centre inside the object +/-15 %
ANCHOR_Y_TOL_PX = 4.0     # connectors into one target: same height, +/-4 px
ENCLOSE_MARGIN_PX = 26.0  # an outline this close around a thing is emphasis
# AMENDED LAW 38 (Miguel, 2026-09-02): a RECTANGULAR box is legal emphasis for a
# drawn object.  Only an OVAL is not — so the radius test that used to catch any
# rounded outline at 35 % of the short side now fires at 50 %, the point where a
# rectangle's corners have eaten the whole edge and it reads as a pill.
RING_RADIUS_FRAC = 0.5

LAYOUT_JS = r"""
(t) => {
  const tl = window.__timelines && window.__timelines["main"];
  if (!tl) return { error: "no timeline" };
  tl.pause(); tl.seek(t, false);
  const root = document.getElementById("root");
  // run-9 split pages are authored 2160 wide and rendered into a 1080 frame;
  // every measurement below is normalised to FRAME DESIGN PX so one constant
  // governs every format.
  const scale = 1080 / parseFloat(root.dataset.width || "1080");
  const clips = Array.from(root.children).filter(
      el => el.dataset && el.dataset.start !== undefined);
  const active = [];
  for (const c of clips) {
    const s = parseFloat(c.dataset.start), d = parseFloat(c.dataset.duration);
    const on = t >= s - 0.01 && t < s + d - 0.01;
    c.style.visibility = on ? "visible" : "hidden";
    // THE WHITEBOARD IS NOT JUDGED HERE.  Its zone is ONE <svg> canvas whose
    // paths are drawn progressively with stroke-dashoffset, so every path's
    // bounding box is its FINAL shape from frame 0 and a DOM gutter reads ink
    // that is not on screen yet.  The whiteboard's spacing, enclosure, label
    // and lifetime laws are proved on its AUTHORED board, in board units, by
    // formats/whiteboard/lib/whiteboard_build.py.
    if (on && c.tagName !== "VIDEO" && !c.querySelector("#cam > svg")) active.push(c);
  }
  const SKIP = new Set(["script","style","source","track","defs","clippath",
                        "video","audio","lineargradient","stop","filter","mask"]);
  const eff = (el, stop) => { let o = 1, n = el;
    while (n && n !== stop.parentElement) { const cs = getComputedStyle(n);
      if (cs.display === "none" || cs.visibility === "hidden") return 0;
      o *= parseFloat(cs.opacity); n = n.parentElement; } return o; };
  const out = [];
  for (const sec of active) {
    for (const el of sec.querySelectorAll("[id]")) {
      const tag = el.tagName.toLowerCase();
      if (SKIP.has(tag)) continue;
      const cs = getComputedStyle(el);
      if (eff(el, sec) < 0.15) continue;
      // progressively drawn ink (stroke-dashoffset): the box is the FINAL
      // shape at every instant, so it cannot be measured for spacing.
      if (cs.strokeDasharray && cs.strokeDasharray !== "none") continue;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) continue;
      const bg = cs.backgroundColor !== "rgba(0, 0, 0, 0)" &&
                 cs.backgroundColor !== "transparent";
      const bw = Math.max(parseFloat(cs.borderTopWidth) || 0,
                          parseFloat(cs.borderLeftWidth) || 0);
      const leafText = el.childElementCount === 0 &&
                       (el.textContent || "").trim().length > 0;
      const svgInk = !!el.ownerSVGElement &&
        ["rect","circle","ellipse","path","line","polyline","text","image"].includes(tag);
      const media = ["img","svg","image"].includes(tag);
      if (!(bg || bw > 0 || leafText || svgInk || media)) continue;
      const d = el.dataset || {};
      // AMENDED LAW 38 needs to know what a thing IS, not only how it is drawn:
      // words that live inside a RASTER (a post card, a screenshot, a document,
      // a UI capture) are highlighted; a DRAWN object is boxed.  `img` is "this
      // element is or wraps a raster"; `assetish` is the factory's own naming
      // for a pasted capture (`.shot`, `#postcard`, `x-card`) — never a drawn
      // card, which is why `data-asset` exists as the explicit declaration.
      const nm = (el.id || "") + " " + (el.getAttribute("class") || "");
      // A drawn panel can contain a small logo without becoming a raster.
      // Unnamed image-only wrappers count only when the image fills the panel.
      const onlyChild = el.children.length === 1 ? el.firstElementChild : null;
      const childRect = onlyChild?.getBoundingClientRect();
      const imageWrapper = onlyChild && ["img","image"].includes(onlyChild.tagName.toLowerCase()) &&
          childRect.width >= r.width * .9 && childRect.height >= r.height * .9;
      const isImg = ["img","image"].includes(tag) || !!imageWrapper;
      const assetish = d.asset !== undefined ||
        /(^|[-_ ])(postcard|post|tweet|screenshot|shot|capture|thread|raster|asset)([-_ 0-9]|$)/i.test(nm);
      const m = cs.transform, mm = m && m !== "none" ? m.match(/matrix\(([^)]+)\)/) : null;
      const rot = mm ? Math.abs(parseFloat(mm[1].split(",")[1])) > 0.01 : false;
      const radius = Math.max(parseFloat(cs.borderTopLeftRadius) || 0,
                              parseFloat(cs.rx) || 0);
      out.push({
        id: el.id, cls: el.getAttribute("class") || "", tag: tag, sec: sec.id,
        x: r.left * scale, y: r.top * scale,
        w: r.width * scale, h: r.height * scale,
        text: (el.textContent || "").trim().slice(0, 30),
        leaf: leafText, bg: bg, bw: bw * scale, radius: radius * scale,
        rot: rot, media: media, img: isImg, assetish: assetish,
        edge: (bw > 0 ? cs.borderTopColor : cs.stroke) || "",
        stroked: !!el.ownerSVGElement && cs.stroke !== "none" &&
                 (cs.fill === "none" || cs.fill === "rgba(0, 0, 0, 0)"),
        overlapOk: d.overlapOk !== undefined, bleedOk: d.bleed !== undefined,
        block: d.block || null, labelFor: d.labelFor || null,
        connectTo: d.connectTo || null, container: d.container !== undefined,
        emphasis: d.emphasis || null, spacingOk: d.spacingOk !== undefined,
      });
    }
  }
  return { objs: out };
}
"""


def _lgap(a, b):
    dx = max(b["x"] - (a["x"] + a["w"]), a["x"] - (b["x"] + b["w"]), 0.0)
    dy = max(b["y"] - (a["y"] + a["h"]), a["y"] - (b["y"] + b["h"]), 0.0)
    return (dx * dx + dy * dy) ** 0.5


def _lolap(a, b):
    ox = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
    oy = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
    return max(ox, 0.0) * max(oy, 0.0)


def _lcontains(a, b, m=1.0):
    return (a["x"] - m <= b["x"] and a["y"] - m <= b["y"] and
            a["x"] + a["w"] + m >= b["x"] + b["w"] and
            a["y"] + a["h"] + m >= b["y"] + b["h"])


def _lcx(o):
    return o["x"] + o["w"] / 2


def _enc_margin(a, b):
    """How much air `a` leaves around a thing it contains."""
    return min(b["x"] - a["x"], b["y"] - a["y"],
               (a["x"] + a["w"]) - (b["x"] + b["w"]),
               (a["y"] + a["h"]) - (b["y"] + b["h"]))


def _loutline(o):
    """Drawn as an EDGE and not a fill: a bordered transparent box, or SVG ink
    that is stroked with no fill."""
    return (o["bw"] > 0 and not o["bg"]) or o["stroked"]


def _lring(o):
    """A RING — a circle, an ellipse, or an outline whose corners are so round
    it reads as an oval (radius at half the short side is a pill, not a box).
    Banned as emphasis on every target: this is the circled clock."""
    if o["tag"] in ("circle", "ellipse"):
        return True
    if "ring" in o["cls"] or (o.get("emphasis") or "") == "ring":
        return True
    return _loutline(o) and o["radius"] >= RING_RADIUS_FRAC * min(o["w"], o["h"])


def _laccent(o):
    """Drawn in the accent — the terracotta family (TERRA #C4573A, TERRA_L
    #DD7259, TERRA_2 #E68569).  A NEUTRAL hairline is chrome (a card border, a
    frame around a screenshot); the accent is what says "look here"."""
    m = re.match(r"rgba?\(([^)]+)\)", (o.get("edge") or "").strip())
    if not m:
        return False
    v = [float(x) for x in m.group(1).replace("/", ",").split(",")[:4]]
    if len(v) > 3 and v[3] < 0.2:
        return False
    r, g, b = v[0], v[1], v[2]
    return r > 120 and r > g * 1.35 and r > b * 1.35


def _lboxemph(o):
    """An emphasis BOX — a rectangular ACCENT outline, or a declared border
    flip.  LEGAL on a drawn object or on scene type; wrong on image text.
    A neutral outline is not emphasis at all and is never judged here."""
    if (o.get("emphasis") or "") == "box":
        return True
    return _loutline(o) and _laccent(o) and not _lring(o)


def _lhighlight(o):
    """The marker fill: a translucent swipe declared `data-emphasis="highlight"`
    or carrying the factory's `hl` class."""
    return ((o.get("emphasis") or "") == "highlight" or
            "hl" in o["cls"].split() or o["id"].startswith("hl"))


def _lasset(o):
    """A RASTER: the element is or wraps an image, or it is named like one of
    this factory's pasted captures (`.shot`, `#postcard`, `x-card`)."""
    return bool(o.get("img") or o.get("assetish"))


def _in_asset(o, live):
    """This thing lives INSIDE a raster — so its words are image text."""
    return any(a is not o and _lasset(a) and _lcontains(a, o, 2.0)
               for a in live)


def _lthin(o):
    """A CONNECTOR. It is supposed to touch what it joins, so it is never a
    party to the gutter law — but it is the only thing the crossing law judges."""
    lo, hi = min(o["w"], o["h"]), max(o["w"], o["h"])
    return lo <= 14.0 and (bool(o.get("connectTo")) or hi / max(lo, 1.0) >= 6.0)


def _lwelded(a, b):
    """GLOBAL LAW 9 / ROUND-4 LAW 3: a name and the thing it names are ONE
    BLOCK — printed above or below it, centred on its axis."""
    for lab, obj in ((a, b), (b, a)):
        if not lab["leaf"] or obj["leaf"]:
            continue
        if lab.get("labelFor") and lab["labelFor"] == obj["id"]:
            return True
        if abs(_lcx(lab) - _lcx(obj)) <= obj["w"] * (0.5 + LABEL_AXIS_FRAC) + 4:
            if (lab["y"] + lab["h"] <= obj["y"] + 2 or
                    lab["y"] >= obj["y"] + obj["h"] - 2):
                return True
    return False


def _lparagraph(a, b):
    """Two printed lines sharing a column are one piece of type."""
    if not (a["leaf"] and b["leaf"]):
        return False
    ox = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
    return ox > 0.0 and _lgap(a, b) <= 1.2 * max(a["h"], b["h"])


def check_layout(objs):
    """The five ROUND-4 layout laws for one sample. DOM-composed formats only —
    the whiteboard is one <svg> canvas and is judged on its AUTHORED board by
    `formats/whiteboard/lib/whiteboard_build.py`."""
    finds = []
    live = [o for o in objs if not o["rot"] and not o["overlapOk"]
            and not o["bleedOk"] and not o["spacingOk"]]

    # a run of >=3 identical shapes in one section is a SERIES (a dot row, a
    # segmented meter, a ladder): it is one object drawn in parts.
    series = {}
    for o in live:
        series.setdefault((o["sec"], o["cls"], round(o["w"]), round(o["h"])),
                          []).append(o["id"])
    in_series = {i for k, v in series.items() if len(v) >= 3 and k[1] for i in v}

    # ---- LAW 5a: the gutter ------------------------------------------------
    body = [o for o in live if not _lthin(o)]
    for i in range(len(body)):
        for j in range(i + 1, len(body)):
            a, b = body[i], body[j]
            if a["sec"] != b["sec"]:
                continue
            if a["block"] and a["block"] == b["block"]:
                continue
            if a["id"] in in_series and b["id"] in in_series:
                continue
            if _lcontains(a, b) or _lcontains(b, a):
                continue                       # composition, not a gutter
            if _lolap(a, b) > 0:
                continue                       # `collision` owns real overlap
            g = _lgap(a, b)
            if g <= 0.0:
                continue    # edge contact: an assembled drawing or a landing
            if _lwelded(a, b) or _lparagraph(a, b):
                continue
            if g < CRAMP_ERR_PX:
                finds.append(("cramp", "error",
                              tuple(sorted((a["id"], b["id"]))),
                              f"{a['id']} | {b['id']} gutter {g:.1f}px "
                              f"(floor {CRAMP_ERR_PX:.0f}, aim {CRAMP_AIM_PX:.0f})"))

    # ---- LAW 5b: a connector never crosses printed type --------------------
    texts = [o for o in live if o["leaf"]]
    for c in (o for o in live if _lthin(o)):
        for tx in texts:
            if tx["sec"] != c["sec"]:
                continue
            if _lcontains(tx, c, 2.0):
                continue                       # a rule INSIDE its own label
            # THE CORE BAND: an underline or a strike grazes the type's edge;
            # a crossing goes through the letters.
            core = {"x": tx["x"] + 0.04 * tx["w"], "w": tx["w"] * 0.92,
                    "y": tx["y"] + 0.22 * tx["h"], "h": tx["h"] * 0.50}
            if _lolap(c, core) > 0:
                finds.append(("crossing", "error",
                              tuple(sorted((c["id"], tx["id"]))),
                              f"connector {c['id']} passes through the printed "
                              f"key {tx['id']} ({tx['text'][:18]!r})"))

    # ---- LAW 38 (amended): the RIGHT emphasis for the target ---------------
    # (a) a RING / ELLIPSE / CIRCLE as emphasis        -> error, every target
    # (b) a BOX whose target is IMAGE TEXT (a raster)  -> error, use highlight
    # (c) a HIGHLIGHT on a drawn object or scene type  -> warning, prefer a box
    # A rectangular box around a DRAWN object is LEGAL (Miguel, 2026-09-02) and
    # is no longer a finding — it still owes `cramp` its 16 px gutter.
    for o in live:
        if o["container"]:
            continue
        held = [b for b in live if b is not o and b["sec"] == o["sec"]
                and _lcontains(o, b, 0.0)]
        near = [(b, _enc_margin(o, b)) for b in held]
        near = [(b, m) for b, m in near if m <= ENCLOSE_MARGIN_PX]
        if _lring(o):
            for b, m in near:
                finds.append(("enclose", "error",
                              tuple(sorted((o["id"], b["id"]))),
                              f"{o['id']} is a RING/ELLIPSE drawn AROUND "
                              f"{b['id']} (margin {m:.0f}px). A ring is never "
                              f"emphasis: highlight text on an image, box a "
                              f"drawn object"))
                break
            continue
        if not _lboxemph(o):
            continue
        # (b) the box's target is a raster, or type living inside one
        for b, m in near:
            if not (_lasset(b) or _in_asset(b, live)):
                continue
            finds.append(("enclose", "error",
                          tuple(sorted((o["id"], b["id"]))),
                          f"{o['id']} BOXES {b['id']}, which is image text "
                          f"(margin {m:.0f}px). Words that are pixels get the "
                          f"marker highlight; boxing is for drawn objects"))
            break
        else:
            if _in_asset(o, live):
                host = next(a for a in live if _lasset(a) and a is not o
                            and _lcontains(a, o, 2.0))
                finds.append(("enclose", "error",
                              tuple(sorted((o["id"], host["id"]))),
                              f"{o['id']} is a BOX drawn inside the raster "
                              f"{host['id']} — that is image text. Use the "
                              f"marker highlight"))

    # (c) the wrong tool the other way round: a marker swipe over a drawn
    # object or over scene type.  WARNING, never an error — Miguel approved
    # boards that swipe a track bar and a written key, and a law written from
    # one instance has already over-banned a tool he likes once.
    for o in live:
        if not _lhighlight(o):
            continue
        tgt = [b for b in live if b is not o and b["sec"] == o["sec"]
               and not b["container"] and _lolap(o, b) > 0]
        if not tgt:
            continue
        if any(_lasset(b) or _in_asset(b, live) for b in tgt):
            continue
        finds.append(("enclose", "warning",
                      tuple(sorted((o["id"], tgt[0]["id"]))),
                      f"{o['id']} highlights {tgt[0]['id']}, which is not "
                      f"image text. The marker is for words inside a raster; "
                      f"a drawn object or scene type takes the box"))

    # ---- LAW 3: a name goes above or below, never beside -------------------
    for lab in texts:
        host = None
        if lab["labelFor"]:
            host = next((o for o in live if o["id"] == lab["labelFor"]), None)
        else:
            cands = [(o, _lgap(lab, o)) for o in live
                     if o is not lab and o["sec"] == lab["sec"] and not o["leaf"]
                     and not _lthin(o) and not _lcontains(o, lab, 1.0)]
            cands = [(o, d) for o, d in cands if d <= LABEL_WELD_PX]
            if cands:
                host = min(cands, key=lambda p: p[1])[0]
        if host is None:
            continue
        band = host["w"] * (0.5 + LABEL_AXIS_FRAC)
        above = lab["y"] + lab["h"] <= host["y"] + 2
        below = lab["y"] >= host["y"] + host["h"] - 2
        # only a name that is genuinely OFF-AXIS is "beside": a name that sits
        # on its object's axis and merely overlaps it vertically is inside a
        # composition, and `collision` owns that.
        if abs(_lcx(lab) - _lcx(host)) > band and not (above or below):
            sev = "error" if lab["labelFor"] else "warning"
            finds.append(("sidelabel", sev,
                          tuple(sorted((lab["id"], host["id"]))),
                          f"{lab['id']} ({lab['text'][:18]!r}) sits BESIDE "
                          f"{host['id']}: centre off by "
                          f"{_lcx(lab) - _lcx(host):+.0f}px on a +/-{band:.0f}px "
                          f"band. A name goes above or below"))

    # ---- LAW 4: connectors into one target land on aligned anchors ---------
    by_target = {}
    for c in (o for o in live if o["connectTo"]):
        by_target.setdefault(c["connectTo"], []).append(c)
    for tgt, cs in by_target.items():
        if len(cs) < 2:
            continue
        t = next((o for o in live if o["id"] == tgt), None)
        if t is None:
            continue
        ends = []
        for c in cs:
            horiz = c["w"] >= c["h"]
            cy, cx = c["y"] + c["h"] / 2, c["x"] + c["w"] / 2
            pts = ([(c["x"], cy), (c["x"] + c["w"], cy)] if horiz
                   else [(cx, c["y"]), (cx, c["y"] + c["h"])])
            ends.append(min(pts, key=lambda p: _lgap(
                {"x": p[0], "y": p[1], "w": 0.1, "h": 0.1}, t)))
        ys = [p[1] for p in ends]
        xs = [p[0] for p in ends]
        tcx = t["x"] + t["w"] / 2
        level = max(ys) - min(ys) <= ANCHOR_Y_TOL_PX
        mirrored = level and len(xs) % 2 == 0 and all(
            abs((sorted(xs)[k] + sorted(xs)[-1 - k]) / 2 - tcx) <= ANCHOR_Y_TOL_PX
            for k in range(len(xs) // 2))
        if not (level or mirrored):
            finds.append(("anchorline", "error",
                          tuple(sorted(c["id"] for c in cs)),
                          f"{len(cs)} connectors into {tgt} land at y="
                          f"{sorted(round(y) for y in ys)} — spread "
                          f"{max(ys) - min(ys):.0f}px over a "
                          f"{ANCHOR_Y_TOL_PX:.0f}px tolerance. Terminate them on "
                          f"the target's virtual bounding rectangle"))
    return finds



def key_of(a):
    return a["id"] or f"{a['sec']}/{a['cls']}/{round(a['x'])},{round(a['y'])}"


def rect_close(a, b, eps=STATIC_EPS):
    return (abs(a["x"] - b["x"]) < eps and abs(a["y"] - b["y"]) < eps and
            abs(a["w"] - b["w"]) < eps and abs(a["h"] - b["h"]) < eps)


def intersect(a, b):
    ox = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
    oy = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
    if ox <= MIN_OVERLAP_PX or oy <= MIN_OVERLAP_PX:
        return 0.0
    smaller = min(a["w"] * a["h"], b["w"] * b["h"])
    return (ox * oy) / max(smaller, 1.0)


def intersect_abs(a, b):
    """Fraction of a's area covered by b (no minimum-depth gating)."""
    ox = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
    oy = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
    if ox <= 0 or oy <= 0:
        return 0.0
    return (ox * oy) / max(a["w"] * a["h"], 1.0)


def check_sample(atoms, static_keys):
    """Return raw findings for one sample; only static atoms produce findings."""
    finds = []
    stat = [a for a in atoms if key_of(a) in static_keys]

    for a in stat:
        if a["bleedOk"] or a["isRing"] or "tz" not in a["sec_cls"]:
            continue
        # rotated elements: axis-aligned boxes wildly overstate diagonal strokes
        # (an X-strike line "spans" a huge rect). whiteboard panning canvases are
        # intentionally taller than the zone.
        if a["rotated"] or a["h"] >= (a["secBot"] - a["secTop"]) * 1.4:
            continue
        over_r = (a["x"] + a["w"]) - a["secR"]
        over_l = a["secL"] - a["x"]
        over_b = (a["y"] + a["h"]) - a["secBot"]
        over_t = a["secTop"] - a["y"]
        is_shot = "shot" in a["cls"]
        worst_h = max(over_r, over_l)
        worst_v = max(over_b, over_t)
        worst = worst_v if is_shot else max(worst_h, worst_v)
        if worst > 2.0:
            finds.append(("clipped", "error", (key_of(a),),
                          f"{a['id'] or a['cls']} exceeds zone edge by {worst:.0f}px"))
        if a["w"] < FRAME_W * 0.95:
            if a["x"] < EDGE_MARGIN or (FRAME_W - (a["x"] + a["w"])) < EDGE_MARGIN:
                finds.append(("margin", "warning", (key_of(a),),
                              f"{a['id'] or a['cls']} within {EDGE_MARGIN}px of frame edge"))
        if "tz" in a["sec"] or a["secBot"] <= SEAM_Y + 5:
            bottom = a["y"] + a["h"]
            # v1.1 SEAM IS SACRED (Miguel's pilot verdict): touching the caption
            # band is an error; mere proximity stays a warning
            if SEAM_Y - 12 < bottom <= SEAM_Y + 2:
                finds.append(("seam", "error", (key_of(a),),
                              f"{a['id'] or a['cls']} touches the caption seam"))
            elif SEAM_Y - SEAM_MARGIN < bottom <= SEAM_Y + 2:
                finds.append(("seam", "warning", (key_of(a),),
                              f"{a['id'] or a['cls']} within {SEAM_MARGIN}px of caption seam"))

    def thin_bar(a):
        lo, hi = min(a["w"], a["h"]), max(a["w"], a["h"])
        return lo <= 14 and hi / max(lo, 1) >= 8

    solids = [a for a in stat if not a["isRing"] and not a["isRule"]
              and not a["overlapOk"] and not thin_bar(a)]
    for i in range(len(solids)):
        for j in range(i + 1, len(solids)):
            a, b = solids[i], solids[j]
            if a["sec"] != b["sec"]:
                continue
            # unpainted atoms are judged by their glyph/content extent (Range
            # rect), not their layout box: fixed-width counters, letter-spaced
            # labels, and transparent group bands overstate their pixels
            if a["rotated"] or b["rotated"]:
                continue   # diagonal annotation strokes; boxes overstate them
            ra = a.get("cr") or a
            rb = b.get("cr") or b
            frac = intersect(ra, rb)
            # 0.20 for text pairs: tight leading makes adjacent display lines'
            # boxes kiss by 10-19% with zero glyph contact
            thresh = 0.20 if (a["text"] and b["text"]) else MIN_OVERLAP_FRAC
            if frac > thresh:
                # containment / concentric = composition (icon in node, check in
                # box, text in frame), not a collision; the law targets partial
                # edge crossings between peers
                if frac >= 0.96:
                    continue
                ca = (ra["x"] + ra["w"] / 2, ra["y"] + ra["h"] / 2)
                cb = (rb["x"] + rb["w"] / 2, rb["y"] + rb["h"] / 2)
                concentric = (abs(ca[0] - cb[0]) <= 20 and abs(ca[1] - cb[1]) <= 20)
                if concentric and frac >= 0.70:
                    continue
                # corner badge riding a drawn card (check chip on a tile corner)
                # = composition; only when the host visibly IS a card (painted
                # background/border), so a label crossing a bare line still flags
                big, small = (a, b) if ra["w"] * ra["h"] >= rb["w"] * rb["h"] else (b, a)
                bigr, smallr = (ra, rb) if big is a else (rb, ra)
                ratio = (smallr["w"] * smallr["h"]) / max(bigr["w"] * bigr["h"], 1.0)
                if ratio <= 0.18 and big.get("hasBg") and frac >= 0.5:
                    continue
                ids = tuple(sorted((key_of(a), key_of(b))))
                finds.append(("collision", "error", ids,
                              f"{ids[0]} ∩ {ids[1]} = {frac * 100:.0f}% of smaller"))

    groups = {}
    for a in stat:
        if a["cls"].startswith("abs ltile") or a["cls"].startswith("abs node"):
            groups.setdefault((a["sec"], a["cls"]), []).append(a)
    for (sec, cls), g in groups.items():
        if len(g) < 3:
            continue
        # cluster by size (14px linkage): a hero tile 2x the grid size is
        # intentional hierarchy; near-misses inside one cluster are the violation
        sizes = sorted(g, key=lambda a: a["w"] * a["h"])
        clusters, cur = [[sizes[0]]], sizes[0]
        for a in sizes[1:]:
            if abs(a["w"] - cur["w"]) <= 8 and abs(a["h"] - cur["h"]) <= 8:
                clusters[-1].append(a)
            else:
                clusters.append([a])
            cur = a
        for cl in clusters:
            if len(cl) < 3:
                continue
            ws = [a["w"] for a in cl]; hs = [a["h"] for a in cl]
            if max(ws) - min(ws) > SIZE_TOL or max(hs) - min(hs) > SIZE_TOL:
                finds.append(("unequal", "error",
                              tuple(sorted(key_of(a) for a in cl)),
                              f"{len(cl)}x '{cls}' in {sec}: w {min(ws):.0f}-{max(ws):.0f}, "
                              f"h {min(hs):.0f}-{max(hs):.0f}"))
        for axis in ("x", "y"):
            vals = sorted(a[axis] for a in g)
            clusters = [[vals[0]]]
            for v in vals[1:]:
                if v - clusters[-1][-1] <= GRID_TOL:
                    clusters[-1].append(v)
                else:
                    clusters.append([v])
            for c in clusters:
                if max(c) - min(c) > GRID_TOL:
                    finds.append(("unequal", "warning",
                                  tuple(sorted(key_of(a) for a in g)),
                                  f"grid {axis}-alignment drift {max(c) - min(c):.1f}px in {sec}"))
                    break

    boxes = [a for a in atoms if a["isBox"]]
    texts = [a for a in stat if a["text"] and not a["isRule"]]
    for a in stat:
        if not a["isRule"] or a["bleedOk"]:
            continue
        # judge the drawn extent of the inner rule, not the wrapper: a connector
        # still scaled to zero is not on screen and has no ends to check
        d = a.get("ruleRect") or a
        if d["w"] < 2 or d["h"] < 2:
            continue
        # a bar sitting inside a shot/photo is a meter fill or an occluded
        # decoration, not a floating connector
        inside = any(intersect_abs(d, s) >= 0.9 for s in atoms
                     if ("shot" in s["cls"] or s["isBox"]) and s is not a)
        if inside:
            continue
        horizontal = d["w"] >= d["h"]
        underline = False
        for tx in texts:
            gap = d["y"] - (tx["y"] + tx["h"])
            hspan = min(d["x"] + d["w"], tx["x"] + tx["w"]) - max(d["x"], tx["x"])
            if -6 <= gap <= 60 and hspan >= 0.4 * d["w"]:
                underline = True
                break
        if underline or not boxes:
            continue
        cy, cx = d["y"] + d["h"] / 2, d["x"] + d["w"] / 2
        ends = ([(d["x"], cy), (d["x"] + d["w"], cy)] if horizontal
                else [(cx, d["y"]), (cx, d["y"] + d["h"])])
        for (ex, ey) in ends:
            near = any(
                (abs(ex - b["x"]) <= CONNECTOR_END_TOL or
                 abs(ex - (b["x"] + b["w"])) <= CONNECTOR_END_TOL or
                 abs(ey - b["y"]) <= CONNECTOR_END_TOL or
                 abs(ey - (b["y"] + b["h"])) <= CONNECTOR_END_TOL)
                and (b["x"] - CONNECTOR_END_TOL <= ex <= b["x"] + b["w"] + CONNECTOR_END_TOL)
                and (b["y"] - CONNECTOR_END_TOL <= ey <= b["y"] + b["h"] + CONNECTOR_END_TOL)
                for b in boxes)
            if not near:
                finds.append(("floating", "warning", (key_of(a),),
                              f"connector {a['id'] or a['cls']} end at "
                              f"({ex:.0f},{ey:.0f}) touches no box edge"))
                break

    for a in stat:
        # upscaled raster = fine print smaller than a phone can resolve; the
        # hermes ladder.png escape (362px source at 465px) passed every other
        # gate while its 11px sub-lines were unreadable
        if a.get("upscaled"):
            u = a["upscaled"]
            finds.append(("upscaled", "warning", (key_of(a),),
                          f"{a['id'] or a['cls']} renders a {u['natural']}px raster "
                          f"at {u['rendered']}px (legibility risk: crop, don't blow up)"))

    for a in stat:
        # glyph centring: a card with one glyph in it claims to centre that glyph.
        # ERROR since 2026-08-13 (Law 15): real defects measure 3.05-3.75px while
        # the clean-project noise floor is 0.00-0.10px, and warning-only let the
        # hermesjourney 3.05px ship.
        g = a.get("glyph")
        if not g or not a.get("plateLike") or a["bleedOk"]:
            continue
        if min(a["w"], a["h"]) < GLYPH_MIN_PLATE:
            continue
        dx = (g["x"] + g["w"] / 2) - (a["x"] + a["w"] / 2)
        dy = (g["y"] + g["h"] / 2) - (a["y"] + a["h"] / 2)
        if max(abs(dx), abs(dy)) > GLYPH_CENTER_TOL:
            finds.append(("glyph", "error", (key_of(a),),
                          f"{a['id'] or a['cls']} {g['tag']} off plate centre by "
                          f"dx={dx:+.1f} dy={dy:+.1f}px "
                          f"(tol {GLYPH_CENTER_TOL:.1f})"))

    for a in stat:
        # NEAR-MISS centring in COMPOSED cards (2026-08-13, Law 15): a glyph in
        # a card that also carries labels/chrome can't claim full-centre — but a
        # glyph sitting ALMOST on an axis is intended-centred-plus-bug (the
        # smallteams person figures), while deliberate side placements sit FAR
        # off-axis. Flag per axis: close to centre but outside tolerance.
        # Solo-glyph plates are handled by the strict check above.
        gl = a.get("glyphs") or []
        if len(gl) < 1 or not a.get("plateLike") or a["bleedOk"]:
            continue
        if a.get("glyph"):          # solo case already judged strictly
            continue
        if min(a["w"], a["h"]) < GLYPH_MIN_PLATE:
            continue
        for g in gl:
            if max(g["w"], g["h"]) < GLYPH_MIN_SIZE:
                continue            # decorative speck, not a composition claim
            dx = (g["x"] + g["w"] / 2) - (a["x"] + a["w"] / 2)
            dy = (g["y"] + g["h"] / 2) - (a["y"] + a["h"] / 2)
            for axis, off, span in (("dx", dx, a["w"]), ("dy", dy, a["h"])):
                if GLYPH_CENTER_TOL < abs(off) <= GLYPH_NEAR_MISS_FRAC * span:
                    finds.append(("glyph", "error", (key_of(a),),
                                  f"{a['id'] or a['cls']} {g['tag']} near-miss centring: "
                                  f"{axis}={off:+.1f}px on a {span:.0f}px card "
                                  f"(tol {GLYPH_CENTER_TOL:.1f}, band "
                                  f"{GLYPH_NEAR_MISS_FRAC:.0%})"))
                    break

    for a in stat:
        # only wide blocks whose centering is a layout claim; narrow labels
        # inherit text-align:center from ancestors without claiming centering
        if (a["align"] == "center" and a["text"]
                and FRAME_W * 0.6 <= a["w"] < FRAME_W * 0.95):
            cx = a["x"] + a["w"] / 2
            if abs(cx - FRAME_W / 2) > CENTER_TOL:
                finds.append(("offcenter", "warning", (key_of(a),),
                              f"{a['id'] or a['cls']} centered-text box center off by "
                              f"{abs(cx - FRAME_W / 2):.0f}px"))
    return finds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--step", type=float, default=STEP_DEFAULT)
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-shots", action="store_true")
    ap.add_argument("--strict", action="store_true", help="Production visual checks; no overlap/glyph exemptions")
    args = ap.parse_args()

    proj = Path(args.project_dir).resolve()
    strict = args.strict or any((p / "production-policy.json").exists() for p in proj.parents)
    html = proj / "index.html"
    if not html.exists():
        sys.exit(f"no index.html in {proj}")
    out_dir = Path(args.out) if args.out else proj / "geometry_audit"
    out_dir.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(html.as_uri())
        for _ in range(60):
            if page.evaluate('!!(window.__timelines && window.__timelines["main"])'):
                break
            page.wait_for_timeout(250)
        else:
            sys.exit("timeline never registered")
        # bounded font wait: fonts.ready can hang forever when the CDN fetch
        # stalls (broken-IPv6 machine); fallback-font geometry is acceptable
        page.evaluate("Promise.race([document.fonts.ready,"
                      " new Promise(r => setTimeout(r, 6000))])")
        page.wait_for_timeout(400)
        if strict:
            from visual_laws import enforce_no_exemptions
            enforce_no_exemptions(page)
        # Prime: force every tween to record real start/end state. Without this,
        # fromTo immediateRender leaves later tweens' from-values (often opacity:1)
        # painted on elements whose entrance the playhead never crossed — phantom
        # visibles that the renderer (which always sweeps forward) never shows.
        page.evaluate('() => { const tl = window.__timelines["main"];'
                      ' tl.pause(); tl.progress(1, true); tl.progress(0, true); }')
        duration = float(page.locator("#root").get_attribute("data-duration"))

        prev_rects, prev_static_finds = {}, {}
        confirmed = {}   # (type, ids) -> {times, severity, detail}
        ghost_hits = {}          # key -> [times seen at sub-1px]
        ever_visible = set()     # exact atom keys that rendered >=1px at least once
        ever_visible_loose = set()  # sec/cls pairs, for id-less atoms whose position key drifts
        t = 0.05
        while t < duration:
            snap = page.evaluate(SNAPSHOT_JS, t)
            if "error" in snap:
                sys.exit(snap["error"])
            atoms = snap["atoms"]
            cur = {key_of(a): a for a in atoms}
            ever_visible.update(cur.keys())
            ever_visible_loose.update(f"{a['sec']}/{a['cls']}" for a in atoms)
            for g in snap.get("ghosts", []):
                gkey = g["id"] or f"{g['sec']}/{g['cls']}"
                ghost_hits.setdefault(gkey, []).append(round(t, 2))
            static_keys = {k for k, a in cur.items()
                           if k in prev_rects and rect_close(a, prev_rects[k])}
            finds = check_sample(atoms, static_keys)
            # GLOBAL LAW 8, measured on the EMITTED DOM rather than trusted to
            # the generator.  The chassis has a `guard_edge_fade`, but a guard
            # only fires if the code path that built the page CALLS it: run 9's
            # two hand-rolled depth lanes never did, and 6 of 22 tiles per video
            # shipped hard-chopped at x=0 and x=1080 with all three gates green.
            # This check does not care who built the page.
            finds += [("edgefade", "error", (e["key"],), e["detail"])
                      for e in page.evaluate(EDGEFADE_JS, t)]
            # ROUND-4 LAYOUT LAWS. Own element model (see LAYOUT_JS): the whole
            # subtree, id-bearing elements only, normalised to frame design px.
            lay = page.evaluate(LAYOUT_JS, t)
            if "error" not in lay:
                finds += check_layout(lay["objs"])
            cur_keys = set()
            for (typ, sev, ids, detail) in finds:
                fk = (typ, ids)
                cur_keys.add(fk)
                if fk in prev_static_finds:      # persisted 2+ consecutive samples
                    rec = confirmed.setdefault(fk, {"severity": sev, "detail": detail,
                                                    "times": []})
                    rec["times"].append(round(t, 2))
            prev_static_finds = {(typ, ids): True for (typ, sev, ids, detail) in finds}
            prev_rects = cur
            t += args.step

        if strict:
            from visual_laws import CHECK_JS
            violations = page.evaluate(CHECK_JS)
        else:
            violations = []
        for (typ, ids), rec in sorted(confirmed.items(),
                                      key=lambda kv: kv[1]["times"][0]):
            sev = rec["severity"]
            if len(rec["times"]) < 2 and sev == "error":
                sev = "warning"   # blip at a transition edge, not a held state
            violations.append({
                "type": typ, "severity": sev, "elements": list(ids),
                "detail": rec["detail"],
                "from": rec["times"][0], "to": rec["times"][-1],
            })

        # Ghost check is cross-sweep, not per-sample: an atom that was sighted
        # at sub-1px and NEVER rendered a visible pixel anywhere in the whole
        # timeline does not exist on screen. Always an error — there is no
        # legitimate reason to animate a permanently invisible element.
        for gkey, times in sorted(ghost_hits.items()):
            if gkey in ever_visible or gkey in ever_visible_loose:
                continue
            violations.append({
                "type": "ghost", "severity": "error", "elements": [gkey],
                "detail": "never reaches 1px size across the whole timeline "
                          "(broken geometry, e.g. a span authored right-to-left)",
                "from": times[0], "to": times[-1],
            })

        if violations and not args.no_shots:
            for i, v in enumerate(violations[:10]):
                page.evaluate(SNAPSHOT_JS, v["from"] + args.step)
                sel_ids = [e for e in v["elements"] if "/" not in e]
                page.evaluate("""(ids) => ids.forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.style.outline = "5px solid #FF2D2D";
                })""", sel_ids)
                shot = out_dir / f"violation_{i:02d}_{v['type']}.png"
                page.screenshot(path=str(shot),
                                clip={"x": 0, "y": 0, "width": 1080, "height": 920})
                page.evaluate("""(ids) => ids.forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.style.outline = "";
                })""", sel_ids)
                v["screenshot"] = shot.name
        browser.close()

    errors = [v for v in violations if v["severity"] == "error"]
    warnings = [v for v in violations if v["severity"] == "warning"]
    report = {"project": proj.name, "duration": duration, "step": args.step, "strict": strict,
              "errors": len(errors), "warnings": len(warnings),
              "violations": violations}
    (out_dir / "report.json").write_text(json.dumps(report, indent=2))

    print(f"{proj.name}: {len(errors)} errors, {len(warnings)} warnings "
          f"({duration:.1f}s @ {args.step}s step)")
    for v in violations:
        mark = "ERROR " if v["severity"] == "error" else "warn  "
        print(f"  {mark} {v['from']:>6.1f}-{v['to']:<6.1f} {v['type']:<9} {v['detail']}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
