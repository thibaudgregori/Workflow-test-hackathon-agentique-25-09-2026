# codexappshots cutout: author notes

No disagreement with the plan. The plan was built as written. Two format-side changes were made to the emitted page. Neither changes a byte of the sealed module.

## 1. The depth-lane cast is passed as eight names (GRAPHIC CHART 7)

The plan's `cutout_logo_lanes` has seven marks: claude-code, cursor, copilot, gemini, antigravity, warp and claude. `cutout_depthfield.field()` fills tile j of each lane with `cast[(7*j + seed) % len(cast)]`. When the cast has exactly seven marks, `7*j % 7` is always 0, so every lane showed one mark over and over. The first build had Claude Code on all 18 far tiles, Warp on all 18 mid tiles and Gemini on all 20 near tiles. GRAPHIC CHART 7 forbids a lane of one repeated mark.

The generator now passes the same seven marks plus a second Gemini at index 3, for eight names. With eight names the stride visits all eight slots, so every lane shows all seven marks. The two Gemini slots are three tiles apart, and no mark sits next to itself; the generator asserts both. The set of marks is still exactly the plan's.

Shared-tool note for whoever owns `formats/cutout/lib/cutout_depthfield.py` (not edited mid-run): the same thing happens for any cast whose length is a multiple of 7.

## 2. The scene's seven card clips were removed (GLOBAL LAW 8, with LAW 23 kept)

The module gives seven bordered cards `overflow:hidden`: both laptop screens, the Codex window, and the print and screen of both the polaroid and the attached photo. `guard_edge_fade` and prerender's `cutout_checks_24_25` reject any clip without a mask. The split never runs that guard, which is why it only came up here.

I compared the page with and without the clips at 166 instants across chapters 2 and 4. Only two children reach a card corner: the shutter flash inside the chapter-4 screen, and the Codex window's title bar. Without the clip, their square corners showed inside the rounded borders, which LAW 23 forbids. So each one gets the card's inner radius directly: 4 px for the flash (the 14 px screen radius minus its 10 px bezel) and `11px 11px 0 0` for the title bar (the 18 px window radius minus its 7 px border). Then the clips are removed.

After the change, 165 of the 166 instants show no pixel that differs by more than 24 levels. The exception is 23.40 s, in the middle of the window's scale-in, where 739 pixels differ by at most 29 of 255. That is anti-aliasing. This follows the run-22 aieducation cutout (`unclip_shot`).
