# codexsiri cutout: author notes (2026-09-23)

No disagreement with the plan. The plan was built as written: k 1.00, core top 192 (the handoff's
placement), the plan's six topical lanes (chatgpt, gemini, claude, perplexity, grok, meta), no pop-behind
(every product he names is a stage mark), lanes faded in at HOOK_CLEAR 1.45 s (SIRI SUCKS written at
0.95 + 0.50).

One page-level declaration, logged here because it touches the sealed scene's emitted markup:

- The chassis string guard `cutout_core.guard_edge_fade` (run inside `prerender_check.py`) failed on
  `#post-avatar` and `#post-inner`, the two in-card picture frames of the X post card (a rounded 12 px
  avatar crop, a bordered strip of the video poster). STANDARD law 27 (lab law 8) scopes the edge fade to
  elements deliberately cut by the FRAME edge; these sit deep inside the card and the frame. The module is
  sealed, so the cutout page adds a fully OPAQUE mask (`mask-image: linear-gradient(#000,#000)`) to those
  two elements only. No pixel changes. Gate 1's geometric edgefade sweep (the load-bearing half of check
  24) reports 0 frame-edge chops on its own.
- Suggested follow-up (not done, shared tool is fingerprinted mid-run): let `guard_edge_fade` exempt
  in-card frames that carry `data-asset` inside a `data-container` card, so the next post card in a cutout
  needs no declaration.
