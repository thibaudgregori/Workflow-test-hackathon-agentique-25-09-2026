# eudisclosure: split author notes (2026-09-23)

No disagreement with the plan. The split builds the sealed scene as handed off (k 1.00, left 0, core top 192, `media = {}`, lockup `yt`). Two things are logged because they touch what the module emits or what the handoff says.

## 1. The key term's box is trimmed to its ink on this page (the ink does not move)

- **Finding.** `geometry_audit.py --strict` refused the page with one error: `cramp flag-finial | key-disclose gutter 11.0px (floor 16)`, 2.0 to 3.5 s.
- **Cause.** The module sizes `#key-disclose` as its 58 px line box (core y 96 to 154). The DISCLOSE ink, measured in the render browser on this page, spans core y 106 to 141 (canvas 298 to 333, x 420 to 657). The empty 13 px under the baseline puts the declared box 11 px above the finial (core 165). The visible gap between the ink and the finial is 24 px.
- **What the page does.** It adds one page CSS rule, `#key-disclose { height:46px !important; }`. Top, width, line-height, font and centring stay as they are. A pixel diff of the top zone at 2.50 s, before and after, shows a maximum difference of 0: no ink moves. The declared box now ends 1 px under the ink, and the audit measures the true 23 px gutter.
- **Module on disk.** Untouched. The seal hash is unchanged.
- **For the cutout.** The cutout will hit the same line-box finding at its own k: 11·k px against the 16 px floor. It can use the same page rule, or the design agent can resize the box in a resealed module.

## 2. One authored cue sits under a different word than the handoff says

The handoff places `pole` (0.44 s) "inside 'in' (0.50)". But 0.44 s is 0.06 s before "in" starts. It falls inside the 1.0 s window of "live" (0.32 to 0.44), and the build verifies it against that word. Nothing on screen changes.

## Word-sync, as seen on the page

| key | appears at | the word it lands on | caption on screen |
|---|---|---|---|
| DISCLOSE | 1.48 | "disclose" | "now you have to disclose" |
| AI (bubble) | 5.66 | "content." (after "AI generated") | "or AI generated content." |
| AI (page) | 6.26 | "And", 0.26 s after "content." | "And in the case of AI" |
| AI GENERATED | 11.46 | "AI", with "generated" at 11.80 | "is AI generated" |
| AI MODIFIED (right Polaroid) | 12.80 | "AI", with "modified." at 13.24 | "or AI modified." |
| AI MODIFIED (photo / screenshot) | 22.64 / 23.10 | "disclose" / "that.", whose referent is "AI to even do slight modifications" (17.70 to 19.94) | "to disclose that." |

No key shows a number. None disagrees with its words.
