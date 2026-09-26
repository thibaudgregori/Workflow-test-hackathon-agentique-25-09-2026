# warpgrok — cutout author notes

Built as planned. Three choices this lane made, none of which changes the plan's picture:

1. **OpenCode depth tile uses the product mark, not the wordmark.** The plan names `opencode`;
   the handoff's proof resolved it to `coding-tools/opencode-color.png`, which is the word
   "opencode" set in type. A depth tile paints its mark at 0.50 of a 78/116/148 px tile, so a
   wordmark arrives as illegible type rather than a mark. This build uses
   `coding-tools/opencode-mark.png` (OpenCode's own icon), which passes
   `assert_cast_resolves`. If Miguel reads it as a blank box on the phone, the fallback is to
   swap `opencode` for another terminal agent from the same category.
2. **Phone boxes are the handoff's `SC.BESPOKE` core boxes mapped through this page's own
   placement** (k 1.0, left 0, core top 171.2), as handoff section 9.1 says the core boxes are
   authoritative over the plan's pre-drawing bboxes.
3. **Lanes arrive at HOOK_CLEAR 2.26 s** (Gemini key drop at 1.76 s + 0.50 s settle), one lane
   per 0.10 s. No pop-behind: the take names only Warp and Grok, both stage marks.
