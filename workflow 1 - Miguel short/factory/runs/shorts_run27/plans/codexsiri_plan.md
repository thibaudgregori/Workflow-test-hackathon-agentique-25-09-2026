# codexsiri — creative plan

Intake's diagram-build guess stands: the script is one connection built in steps (a phone running Siri, a free GitHub repo, Codex made by OpenAI, the line that joins them, and the phone's screen changing hands), bracketed by a hook, a source post and a 'free, linked below' close; there are no numbers to count and no steps to tick.

```json
{
  "id": "codexsiri",
  "duration_s": 36.16,
  "lane": "diagram build",
  "lane_reason": "Intake's diagram-build guess stands: the script is one connection built in steps (a phone running Siri, a free GitHub repo, Codex made by OpenAI, the line that joins them, and the phone's screen changing hands), bracketed by a hook, a source post and a 'free, linked below' close; there are no numbers to count and no steps to tick.",
  "stage_markers_at_plan_time": {
    "cut": "ok, 78.0 s wall, cut master 36.16 s, tight audio 36.128 s, corroboration 'model-authored keep ranges', analysis_wav_written false",
    "plate": "ok, 180.3 s wall, crop 2848x1780+561+274, scale_k 0.505618, head 451.1 px on canvas, overwide_applied true, face_dx_pct 0.036, visible_window_drift 0.9 master px",
    "prompt0": "ok, 19.2 s wall, wing_review TRUE for codexsiri (the instrument proposed no cut and abstained, removed_px 0); the Astra matte step owns the look at matting/codexsiri/prompts/kf_overlay_00000.png",
    "selection": "ok, selection inputs ready for the outline review (no reviewed selection yet)",
    "track": "skipped (backend matanyone2), no Modal cost booked on the marker",
    "ship": "marker not landed at plan time",
    "cues": "ok, cue_count 1 ('this guy', 4.12 s)"
  },
  "false_start_check": "The tight transcript opens 'Siri sucks, so here's how you can make it 100 times better thanks to AI' once, at 0.10 s, and the phrase does not repeat anywhere in the 36.16 s (the raw take's seven restarts were dropped by keep_words 289-410), so the cut is right (LAW 46).",
  "source_post": {
    "notion_source_url": "https://x.com/jxnlco/status/2085827690909822991",
    "resolved_post": "https://x.com/sharifshameem/status/2085801979863826926",
    "resolution": "The Notion row's Source URL is @jxnlco's repost; X syndication returns the ORIGINAL post for that id: Sharif Shameem (@sharifshameem), 2026-08-07, 'Siri sucks. So I made a way for Codex to act as my iPhone's voice assistant. Now Codex can read my screen, control apps, and take actions on my behalf - all in vanilla iOS 27.' with a 3 min vertical video of an iPhone in his hand.",
    "saved": "runs/shorts_run27/assets/source_codexsiri/: syndication.json, avatar_sharifshameem.jpg (400x400), video_poster.jpg (675x1200, the video's poster frame), post_video_720.mp4"
  },
  "beats": [
    {
      "i": 0,
      "t_start": 0.1,
      "t_end": 3.96,
      "words": "Siri sucks, so here's how you can make it 100 times better thanks to AI.",
      "says": "Siri is bad, and AI can make it far better.",
      "picture": "On 'Siri' an ink-line iPhone pops ALONE on the axis with the real Siri mark on its screen. On 'sucks' it slides left and a speech bubble holding one big question mark pops beside it (Siri not understanding you). SIRI SUCKS is written large above the pair. Nothing else: the phone is the subject the whole video changes.",
      "objects": [
        "phone",
        "siri-screen",
        "bubble-q",
        "key-siri"
      ],
      "emphasis": [],
      "whiteboard_version": "Same picture as marker ink: the phone outline drawn centred with the Siri mark stamped on its screen, redrawn one step left as the question bubble is drawn at its right; SIRI SUCKS written first, alone, large, above."
    },
    {
      "i": 1,
      "t_start": 4.12,
      "t_end": 5.4,
      "words": "This guy did exactly that.",
      "says": "One person actually did it.",
      "picture": "The hook board leaves and the SOURCE POST takes the stage (3.70-7.30): an X post card in the chart (cream card, ink-alpha border, radius 18), header with his avatar, SHARIF SHAMEEM @SHARIFSHAMEEM and the X mark, a hairline, the post's own five lines, and under them a strip of the video it carried (a phone in his hand). On 'This' the marker fill wipes under the two lines 'Siri sucks. So I made a way for Codex / to act as my iPhone's voice assistant.' No metrics chrome.",
      "objects": [
        "post-card",
        "hl-post-1",
        "hl-post-2",
        "post-inner"
      ],
      "emphasis": [
        {
          "target": "post-card line 1-2",
          "kind": "highlight",
          "why": "Text living in a raster-like source card (the post's own words): LAW 38 rule 1, the marker fill, one fill per line, wiped left to right."
        }
      ],
      "whiteboard_version": "The board pastes the same X post card (note_asset raster) and swipes the marker highlight under the same two lines."
    },
    {
      "i": 2,
      "t_start": 5.54,
      "t_end": 9.96,
      "words": "He was so frustrated with the Siri experience that was just so bad out of the box,",
      "says": "Stock Siri, the way it ships, frustrated him.",
      "picture": "The card leaves on 'experience'; the same phone (Siri on its screen) pops back centred. On 'so bad' an open cardboard box draws around its lower half, flaps up, so the phone is literally sitting in its box. OUT OF THE BOX is written under the box on 'out of the box'.",
      "objects": [
        "phone",
        "siri-screen",
        "box",
        "key-box"
      ],
      "emphasis": [],
      "whiteboard_version": "The card is erased as the phone is redrawn centred (LAW 45: the phone lands inside the erase); the open box is drawn around its bottom with flaps up; OUT OF THE BOX written under it."
    },
    {
      "i": 3,
      "t_start": 10.02,
      "t_end": 19.4,
      "words": "that he took matter into his own hands and created this free GitHub repo that manages to connect his Siri to Codex, the coding assistant made by OpenAI.",
      "says": "He built a free GitHub repo that links Siri to Codex, OpenAI's coding assistant.",
      "picture": "On 'took' the box leaves and the phone lifts out and slides to the left seat. On 'GitHub' the GitHub tile pops in the centre, GITHUB REPO written under it on 'repo'. On 'connect' an ink line draws from the phone's right edge into the GitHub tile's left edge. On 'Codex' the Codex tile pops at the right with its line from GitHub, CODEX written under it. On 'OpenAI' a small OpenAI badge pops on the Codex tile's top-right corner (the maker under the product).",
      "objects": [
        "phone",
        "siri-screen",
        "github-tile",
        "key-github",
        "line-phone-github",
        "codex-tile",
        "key-codex",
        "line-github-codex",
        "openai-badge"
      ],
      "emphasis": [],
      "whiteboard_version": "The box is erased as the phone is redrawn at the left; the GitHub tile, the two lines, the Codex tile and the OpenAI badge are drawn on the same words, keys under each tile on one baseline."
    },
    {
      "i": 4,
      "t_start": 19.6,
      "t_end": 22.9,
      "words": "Now, this drastically improves his experience with Siri.",
      "says": "His phone's assistant is now Codex, and it is far better.",
      "picture": "THE PEAK. On 'this drastically' a terracotta charge runs back along the lines, Codex to GitHub, then GitHub to the phone; on 'improves' the phone's screen changes hands: the Siri mark fades and the Codex mark pops in its place. On 'experience' the phone's own outline flips terracotta and back at 'Siri'.",
      "objects": [
        "phone",
        "codex-screen",
        "charge-a",
        "charge-b",
        "github-tile",
        "codex-tile"
      ],
      "emphasis": [
        {
          "target": "phone",
          "kind": "box",
          "why": "The phone is a DRAWN object: LAW 38 rule 2, its own outline stroke flips to terracotta (the DOM lane's panel border flip) at 21.62 and back at 22.76. Never a ring."
        }
      ],
      "whiteboard_version": "The marker retraces both lines in terracotta from Codex back to the phone, scribbles out the Siri mark on the phone's screen and stamps the Codex mark there, then retraces the phone outline in terracotta."
    },
    {
      "i": 5,
      "t_start": 23.34,
      "t_end": 25.98,
      "words": "Now he can communicate and actually get stuff done.",
      "says": "Now he can talk to it and it does real work.",
      "picture": "On 'Now' GitHub, Codex, the lines and their keys leave; the Codex phone slides to the left seat. On 'communicate' the speech bubble returns beside it, this time holding three lines of speech instead of the hook's question mark (the call-back). On 'get' a clipboard pops at the right and its three rows tick terracotta on 'get', 'stuff', 'done'; GET STUFF DONE written under it.",
      "objects": [
        "phone",
        "codex-screen",
        "bubble-talk",
        "clipboard",
        "key-done"
      ],
      "emphasis": [],
      "whiteboard_version": "Erase GitHub/Codex/lines (the phone stays, LAW 45); the bubble with three speech lines is drawn beside the phone; the clipboard is drawn at the right and its three boxes are ticked in terracotta on the three words; GET STUFF DONE under it."
    },
    {
      "i": 6,
      "t_start": 26.1,
      "t_end": 31.4,
      "words": "This repo is 100% free, and it's also linked in the description down below if you ever need it.",
      "says": "The repo is free and linked in the description.",
      "picture": "On 'This' the phone, bubble and clipboard leave and the GitHub tile pops centred, GITHUB REPO under it on 'repo'. On '100%' the tile slides left and a paper price tag, tied to the tile's edge by a short string, pops at the right with FREE written on it. On 'description' IN THE DESCRIPTION is written centred under the pair, and on 'down' a terracotta arrow draws straight down from it toward the description.",
      "objects": [
        "github-tile-2",
        "key-github-2",
        "tag",
        "tag-string",
        "key-desc",
        "arrow-down"
      ],
      "emphasis": [],
      "whiteboard_version": "Erase to the GitHub tile drawn centred (it lands inside the erase); the price tag with its string and FREE on it; IN THE DESCRIPTION written under; a terracotta arrow drawn down."
    },
    {
      "i": 7,
      "t_start": 31.86,
      "t_end": 36.16,
      "words": "Now follow for more AI news, videos, and tutorials each and every single day, and catch you in the next one.",
      "says": "The channel's standing call to action.",
      "picture": "The opaque cream sheet rises and wipes the board. On it, small and centred, the ink phone glyph (blank screen, no brand mark), then the terracotta rule and the handle lockup.",
      "objects": [
        "o-sheet",
        "o-glyph",
        "o-rule",
        "o-slot"
      ],
      "emphasis": [],
      "whiteboard_version": "Identical: the rising sheet, the small phone outline, the rule, the lockup."
    }
  ],
  "bespoke_objects": [
    {
      "name": "phone with Siri",
      "t": 1.6,
      "bbox": [
        0.338,
        0.1823,
        0.662,
        0.3385
      ],
      "space": "norm",
      "why_bespoke": "The hook's subject (LAW 20): the thing every viewer owns and the thing the whole video changes; the question bubble beside it is Siri not understanding, which a mark alone cannot say.",
      "how_drawn": "A tall rounded-rectangle phone body in thick ink with a dynamic-island pill, a side button and a card-fill screen carrying the real Siri mark, plus a speech bubble with one heavy question mark at its right."
    },
    {
      "name": "phone in box",
      "t": 9.9,
      "bbox": [
        0.3519,
        0.1583,
        0.6481,
        0.3448
      ],
      "space": "norm",
      "why_bespoke": "'Bad out of the box' made literal: the stock phone still standing in its open shipping box is the factory default in one picture.",
      "how_drawn": "The same ink phone standing inside an open cardboard box drawn as a wide front panel with a tape strip and two flaps folded up and out, the box's front covering the phone's lower third."
    },
    {
      "name": "clipboard with checkmarks",
      "t": 26.02,
      "bbox": [
        0.6157,
        0.2052,
        0.7639,
        0.3146
      ],
      "space": "norm",
      "why_bespoke": "'Actually get stuff done' as an object: a to-do clipboard whose rows tick on the spoken words argues finished work, which a logo cannot.",
      "how_drawn": "A tall board with rounded corners, a clip at the top centre, three rows of square check boxes each followed by a short line, the boxes ticked in terracotta."
    },
    {
      "name": "free price tag",
      "t": 28.5,
      "bbox": [
        0.4222,
        0.1969,
        0.6815,
        0.2594
      ],
      "space": "norm",
      "why_bespoke": "'100% free' as the object a price is written on: a tag reading FREE hung off the repo says the repo costs nothing.",
      "how_drawn": "A paper price tag (rectangle with a pointed left end and a punched hole) in card fill and ink outline, FREE written large inside, tied by a short string to the GitHub tile's right edge."
    }
  ],
  "labels": [
    {
      "for": "phone",
      "text": "SIRI SUCKS",
      "place": "above",
      "at": 0.42,
      "note": "LAW 9 key term: written FIRST, alone, 48 px (25.6 design units), centred on x 540 inside the phone+bubble group; drawn 0.95 after 'sucks' ends. LAW 39: above its host, centre inside the phone's extent +/-15%."
    },
    {
      "for": "box",
      "text": "OUT OF THE BOX",
      "place": "below",
      "at": 9.08,
      "note": "LAW 39: below, centred on the box's axis (540)."
    },
    {
      "for": "github-tile",
      "text": "GITHUB REPO",
      "place": "below",
      "at": 13.6,
      "note": "LAW 39 / LAW 50: every tile key sits BELOW its tile on ONE baseline (core y 436)."
    },
    {
      "for": "codex-tile",
      "text": "CODEX",
      "place": "below",
      "at": 16.58,
      "note": "LAW 39 / LAW 50: below, same baseline as GITHUB REPO."
    },
    {
      "for": "clipboard",
      "text": "GET STUFF DONE",
      "place": "below",
      "at": 24.86,
      "note": "LAW 39: below, centred on the clipboard; same baseline as the chapter-3 keys."
    },
    {
      "for": "github-tile-2",
      "text": "GITHUB REPO",
      "place": "below",
      "at": 26.34,
      "note": "LAW 39: below its tile, moves with it (LAW 28)."
    },
    {
      "for": "arrow-down",
      "text": "IN THE DESCRIPTION",
      "place": "above",
      "at": 29.48,
      "note": "LAW 39: the arrow hangs under its words; the words name what the arrow points to."
    }
  ],
  "lifetimes": [
    {
      "mark": "phone",
      "t_from": 0.1,
      "t_to": 3.62,
      "anchor": null,
      "note": "hook window; the card owns 3.70-7.30"
    },
    {
      "mark": "bubble-q",
      "t_from": 0.42,
      "t_to": 3.62,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "key-siri",
      "t_from": 0.95,
      "t_to": 3.62,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "post-card",
      "t_from": 3.7,
      "t_to": 7.3,
      "anchor": null,
      "note": "GLOBAL LAW 3: 3.6 s"
    },
    {
      "mark": "phone (second window)",
      "t_from": 7.4,
      "t_to": 26.1,
      "anchor": null,
      "note": "the spine of chapters 2-5, crossing three seams (LAW 45 handover); finite"
    },
    {
      "mark": "box",
      "t_from": 8.62,
      "t_to": 10.3,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "key-box",
      "t_from": 9.08,
      "t_to": 10.3,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "github-tile",
      "t_from": 13.24,
      "t_to": 23.3,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "codex-tile",
      "t_from": 16.58,
      "t_to": 23.3,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "openai-badge",
      "t_from": 18.94,
      "t_to": 23.3,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "lines + charge",
      "t_from": 15.0,
      "t_to": 23.3,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "bubble-talk",
      "t_from": 23.74,
      "t_to": 26.1,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "clipboard",
      "t_from": 24.86,
      "t_to": 26.1,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "github-tile-2",
      "t_from": 26.1,
      "t_to": 31.86,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "tag",
      "t_from": 27.02,
      "t_to": 31.86,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "key-desc + arrow-down",
      "t_from": 29.48,
      "t_to": 31.86,
      "anchor": null,
      "note": ""
    },
    {
      "mark": "o-glyph / o-rule / o-slot",
      "t_from": 32.34,
      "t_to": null,
      "anchor": "outro",
      "note": "the outro lockup, anchors"
    }
  ],
  "connectors": [
    {
      "to": "github-tile",
      "from": [
        "phone"
      ],
      "note": "ONE line into GitHub's LEFT edge at anchor_points(github_box, 1, 'left'); it starts ON the phone's outer right edge at the same y. Touches both, no gap."
    },
    {
      "to": "codex-tile",
      "from": [
        "github-tile"
      ],
      "note": "ONE line into Codex's LEFT edge at anchor_points(codex_box, 1, 'left') from GitHub's right edge, level."
    },
    {
      "to": "phone",
      "from": [
        "codex-tile via github-tile"
      ],
      "note": "The 19.92 charge re-traces the two lines in terracotta, in two segments (Codex->GitHub, GitHub->phone), never across the GitHub mark."
    },
    {
      "to": "tag",
      "from": [
        "github-tile-2"
      ],
      "note": "The tag's string: from the tile's right edge to the tag's punched hole, both ends on ink."
    }
  ],
  "blocks": [
    [
      "phone",
      "siri-screen",
      "codex-screen"
    ],
    [
      "phone",
      "bubble-q"
    ],
    [
      "phone",
      "box"
    ],
    [
      "codex-tile",
      "openai-badge",
      "key-codex"
    ],
    [
      "github-tile",
      "key-github"
    ],
    [
      "clipboard",
      "key-done"
    ],
    [
      "github-tile-2",
      "key-github-2",
      "tag-string",
      "tag"
    ],
    [
      "key-desc",
      "arrow-down"
    ],
    [
      "post-card",
      "post-header",
      "post-text",
      "hl-post-1",
      "hl-post-2",
      "post-inner"
    ]
  ],
  "blocks_note": "LAW 41: anything authored as ONE object that geometry cannot infer - a welded label, a container's contents. A paragraph and a >=3 identical-shape series are inferred for you. The phone and its box overlap on purpose (it stands inside it); the badge sits on the Codex tile's corner on purpose.",
  "pointing_cues": [
    {
      "cue_i": 0,
      "at": 4.12,
      "phrase": "this guy",
      "asset": "The X post by Sharif Shameem (@sharifshameem), https://x.com/sharifshameem/status/2085801979863826926, 2026-08-07, reached through this recording's Notion row (3b631704-6eeb-81a3-85a8-d7d13c796da9, Source URL x.com/jxnlco/status/2085827690909822991, a repost that X syndication resolves to this original). Saved under runs/shorts_run27/assets/source_codexsiri/. Built as an X post card in the graphic chart: card #FFFDF9, 3 px ink-alpha border, radius 18; header row with his avatar (rounded square), 'SHARIF SHAMEEM @SHARIFSHAMEEM' in JetBrains Mono uppercase and the X mark in INK; a hairline; the post's own words in five lines; a strip of the video it carried. Up 3.70-7.30 (3.6 s). NO metrics chrome (GLOBAL LAW 3).",
      "platform": "X",
      "inner": "the 3-minute vertical video the post carried (his iPhone in his hand, Codex driving apps), shown as a still strip of its poster frame under the text; the claim is in the post's words, so there is no zoom into it.",
      "highlight": "the two lines 'Siri sucks. So I made a way for Codex' / 'to act as my iPhone's voice assistant.' - one marker fill per line, wiped at 4.12 and 4.22, because that sentence is exactly the claim Miguel makes."
    }
  ],
  "boards": {
    "mode": "chapters",
    "why": "LAW 43 default: the script moves through six different ideas (Siri is bad, the post, stock out of the box, the repo linking Siri to Codex, what he can do now, free and linked), so the board clears between them; the phone is carried across the seams as the spine.",
    "chapters": [
      {
        "i": 0,
        "t_start": 0.1,
        "t_end": 3.7,
        "erase_at": 3.62,
        "holds": [
          "phone",
          "bubble-q",
          "key-siri"
        ],
        "why_together": "the hook: Siri on a phone, not understanding"
      },
      {
        "i": 1,
        "t_start": 3.7,
        "t_end": 7.36,
        "erase_at": 7.3,
        "holds": [
          "post-card"
        ],
        "why_together": "the source post, alone"
      },
      {
        "i": 2,
        "t_start": 7.36,
        "t_end": 10.3,
        "erase_at": 10.3,
        "holds": [
          "phone",
          "box",
          "key-box"
        ],
        "why_together": "stock Siri, still in its box"
      },
      {
        "i": 3,
        "t_start": 10.3,
        "t_end": 23.3,
        "erase_at": 23.3,
        "holds": [
          "phone",
          "github-tile",
          "codex-tile",
          "openai-badge",
          "lines",
          "charge",
          "key-github",
          "key-codex"
        ],
        "why_together": "the one diagram: phone - repo - Codex, and the screen changing hands"
      },
      {
        "i": 4,
        "t_start": 23.3,
        "t_end": 26.1,
        "erase_at": 26.1,
        "holds": [
          "phone",
          "bubble-talk",
          "clipboard",
          "key-done"
        ],
        "why_together": "what the Codex phone lets him do"
      },
      {
        "i": 5,
        "t_start": 26.1,
        "t_end": 31.86,
        "erase_at": 31.86,
        "holds": [
          "github-tile-2",
          "key-github-2",
          "tag",
          "key-desc",
          "arrow-down"
        ],
        "why_together": "the repo is free and linked below"
      }
    ],
    "key_term": "SIRI SUCKS"
  },
  "cast": [
    "siri",
    "codex",
    "github",
    "openai",
    "x-logo"
  ],
  "cast_note": "THE ROSTER IS TOPICAL: the comparison the SCRIPT makes. Never a consumer-app wall, never a placeholder, never the story's own subject mark (that belongs on the stage). MARK IDENTITY: 'Claude Code' is the plain no-outline mascot (registry key 'claude-code'), NEVER 'claude-code-sticker'; Claude Cowork is the ORANGE mark. Files: siri = ai-models/siri-color.png, codex = coding-tools/codex-color.png (the product mark, LAW 35), github = coding-tools/github-mark.png, openai = ai-models/openai.png (the maker badge only), x-logo = platforms/x-logo.svg (the post card's frame).",
  "cutout_logo_lanes": [
    "chatgpt",
    "gemini",
    "claude",
    "perplexity",
    "grok",
    "meta"
  ],
  "cutout_logo_lanes_note": "THE LOGO LANES BEHIND HIM ARE TOPICAL (Miguel, 2026-09-04 run-13 review: 'it would be cool if the logos behind me in cutout are relevant to the video'). The marks travelling the background lanes are the products and companies THIS SHORT names, or their obvious neighbours in the same category. A generic house set is a rejection. Here: the other AI assistants that compete to be the voice in your phone (ChatGPT, Gemini, Claude, Perplexity, Grok, Meta AI); never Siri or Codex, which are on the stage.",
  "open_questions": [
    "wing review: prompt0 landed with wing_review true for codexsiri (instrument abstained, no cut); the Astra matte step owns the look at matting/codexsiri/prompts/kf_overlay_00000.png.",
    "The post never says 'GitHub'; Miguel does, so the GitHub tile follows his words (GLOBAL LAW 3: on-screen claims track what he says)."
  ],
  "open_doubts": [],
  "open_doubts_note": "AN OPEN DOUBT STOPS AND ASKS (Miguel, 2026-09-04). open_questions are things an author can build around. open_doubts are doubts that CHANGE WHAT THE VIEWER SEES - which card, which platform, which picture, which claim. If you write one with changes_what_viewer_sees true, THIS RECORDING DOES NOT GET BUILT: the workflow pauses it and asks Miguel one line. So do not park a real doubt in open_questions to keep the line moving, and do not invent a doubt you could decide yourself."
}
```
