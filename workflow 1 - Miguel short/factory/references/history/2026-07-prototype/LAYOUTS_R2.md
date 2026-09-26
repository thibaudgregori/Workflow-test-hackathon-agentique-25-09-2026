# Round 2 — 10 distinct layouts per format

Feedback driving this round: variants must look EXTREMELY different (layout-level, not seeds);
real UI in faceless too; verify the full relevant UI region is visible; fix FREE type (use the
system's Poppins, not a foreign slab font); fix connectors spacing (nothing touches); split
lower-thirds move from purple to the brand terracotta/orange; clean & professional only.

## Shared design system (LOCKED, all layouts)
- Palette: cream `#F0F3EE`/`#F6F1EA`, dark `#101012`/`#17171B`, ink `#111`, terracotta
  `#C66748`/`#DD7259`, lime `#BEED4B` (small accents only), yellow `#F5A623` (FREE), white cards.
- Type: Poppins (500-800) UI/titles; Instrument Serif Italic for accent numbers/words; JetBrains
  Mono micro-labels; Lora for the Claude wordmark. **FREE = Poppins 800 uppercase, yellow
  `#F5A623`, soft 4px `#C97300` offset shadow + tight tracking — no Archivo slab.**
- Captions: faceless = one-word black pill (unchanged, y≈820). Split = phrase pill now
  **terracotta `#C4573A` bg, white Nunito 800 text** at the seam (y=460; full-face y≈735, CTA 643).
- Audio: same VO/music/SFX stack as round 1.
- Real UI assets: `pipeline/remotion/public/ui/*` + `assets/ui_captures/round2/*` (agent manifest).
  **UI images are never height-cropped: render full image aspect (fixed width, auto height).**
- Beats identical to STYLE_SPEC.md. CTA + hook copy identical across layouts (they are the brand),
  but their ARRANGEMENT varies per layout.

## Faceless layouts (F1-F10) — all feature scenes show REAL UI
| id | name | scene anatomy |
|----|------|---------------|
| F1 | Reference Pro | R1 look, but mock cards replaced by real-UI screenshot cards w/ browser chrome; lime badge; title+sub below. |
| F2 | Headline Top | Huge title + serif italic number top-left block; full-width real-UI card lower half; caption pill between. |
| F3 | Phone Frame | Real UI inside a centered dark phone mockup (rounded 54px bezel); title below phone; tiny badge chip above. |
| F4 | Split Canvas | Top 45% dark w/ white title + number, bottom 55% cream w/ UI card straddling the boundary. |
| F5 | Big Number Ghost | Giant outlined serif number (~360px, 8% ink) behind centered UI card; title beneath. |
| F6 | Sidebar Rail | Left vertical rail (72px, dark) with 01-05 progress dots; right column: title, sub, UI card. |
| F7 | Dark Mode | Dark `#101012` canvas; cream UI cards; terracotta titles; lime → terracotta badges; white captions pill w/ dark text inverted? keep black pill w/ white text (works on dark). |
| F8 | Spotlight Zoom | Full-bleed blurred UI screenshot as background + sharp zoomed crop card of the SAME UI centered (magnifier feel); title chip top. |
| F9 | Checklist Build | Persistent checklist panel: features tick on as narrated (✓ + name), active row expands showing a small UI thumbnail; title top. |
| F10 | Editorial Serif | Cream; oversized Instrument Serif Italic feature word (e.g. *Memory*) + small caps Poppins label; UI card bottom-right at slight tilt; terracotta rule lines. |

Hook/CTA arrangement varies per layout family (top-aligned for F2/F6, centered otherwise), same copy.

## Split layouts (S1-S10) — face zone bottom (except S2), orange captions
| id | name | top-zone anatomy |
|----|------|------------------|
| S1 | Reference Pro | R1 split look with fixed spacing + orange captions + uncropped UI. |
| S2 | Inverted | Face TOP (0-564), content BOTTOM (564-1024): number+title then UI card. |
| S3 | Full-bleed UI | Real UI screenshot/video fills the whole top zone edge-to-edge; gradient scrim; title bottom-left of zone. |
| S4 | Serif Poster | Dark top; giant Instrument Serif Italic number fills left half; feature title stacked right; small UI chip card bottom. |
| S5 | Phone-in-Zone | Cream top; phone mockup (with UI) leaning right at 6°; title top-left. |
| S6 | Progress Steps | Top strip: 5-step progress bar (01-05, active terracotta); center: UI card; no big number. |
| S7 | Dark Terminal | Dark top; mono `claude.ai` title bar full width; UI in a terminal-like window; terracotta cursor accent. |
| S8 | Checklist | Cream top; accumulating feature checklist left; active feature's UI thumbnail right. |
| S9 | Video Zone | Official UI demo VIDEO fills top zone (ken-burns if image fallback); mono label overlay. |
| S10 | Typographic | Feature word huge (Poppins 800, two-tone: word ink + number terracotta outline); thin UI strip card below. |

## Content per scene (all layouts pull from the same real-UI pool)
memory → memory_toggle (full row incl. Learn more) / round2 memory assets;
websearch → websearch_toggle (full block); projects → projects_modal or chat history;
thinking → dark thinking card (custom, matches reference precedent) or round2 asset;
connectors → `ui/connectors_panel.png` (960x490) which has the greeting + composer + the 4 logo
tiles BAKED IN with guaranteed spacing (**no separate logo-row elements anywhere — supersedes the
earlier gap rule; this is how "nothing touches" is enforced**); models → model pills / round2 asset.

## Verification additions (QC round 2)
- Rubric judges brand-family + professionalism + internal layout quality (NOT sameness with the
  reference — layouts are intentionally different).
- New score_ui: the relevant UI region is fully visible (whole toggle row + description, whole
  modal, whole composer) — no cropped text inside UI screenshots.
- Explicit check: connectors icons/labels have clear space (no touching elements).
