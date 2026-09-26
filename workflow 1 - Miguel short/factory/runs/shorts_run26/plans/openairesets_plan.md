# openairesets — creative plan

The whole claim is one everyday object, an hourglass of usage that runs out and gets flipped for a price, carried through four beats (reset for sale, the $200 plan running dry, four hourglasses at once, a wall that keeps rising), with the OpenAI mark as the seller, so drawn objects and a real mark argue it better than intake's kinetic type would.

```json
{
  "id": "openairesets",
  "duration_s": 20.64,
  "lane": "icon choreography",
  "lane_reason": "The whole claim is one everyday object, an hourglass of usage that runs out and gets flipped for a price, carried through four beats (reset for sale, the $200 plan running dry, four hourglasses at once, a wall that keeps rising), with the OpenAI mark as the seller, so drawn objects and a real mark argue it better than intake's kinetic type would.",
  "beats": [
    {
      "i": 0,
      "t_start": 0.1,
      "t_end": 2.96,
      "words": "OpenAI just started selling resets for their clients",
      "says": "OpenAI now sells usage resets to its customers.",
      "picture": "An hourglass stands alone in the middle, its top bulb almost empty and a thin terracotta stream still falling: the usage is running out. On 'selling' it slides right and the OpenAI tile pops in on the left with a terracotta arrow into the hourglass. On 'resets' the hourglass FLIPS over and the top bulb is full again. RESETS is written large above it, then a price tag with a '$' swings on from its top corner on a string: a reset, for sale.",
      "whiteboard": "The marker draws the hourglass first, alone on the axis (caps, posts, glass, a little sand on top, a pile below). Then the OpenAI mark on the left and an arrow into the hourglass; on 'resets' the hourglass is redrawn upside-down-full (a curved flip arrow beside it, then the top bulb inked full); RESETS written above; the tag with '$' drawn hanging off the top cap.",
      "objects": [
        "hourglass",
        "openai tile",
        "arrow openai to hourglass",
        "price tag",
        "RESETS"
      ],
      "emphasis": []
    },
    {
      "i": 1,
      "t_start": 3.3,
      "t_end": 8.8,
      "words": "because now even a $200 per month subscription is no longer enough for power users,",
      "says": "Even the $200 monthly plan runs out for heavy users.",
      "picture": "The tile, arrow, tag and RESETS leave and the full hourglass slides back to the centre. '$200' then '/ MONTH' is written under it: this hourglass is the $200 plan. On 'subscription' half the sand falls; on 'no longer enough' the rest pours through until the top bulb is EMPTY, and a terracotta box snaps around the hourglass: not enough.",
      "whiteboard": "Same chapter, the hourglass carried: '$200 / MONTH' written under it, the top sand erased in two steps while the bottom pile is inked higher, then a terracotta marker box around the hourglass.",
      "objects": [
        "hourglass",
        "$200 / MONTH"
      ],
      "emphasis": [
        {
          "target": "hourglass",
          "kind": "box",
          "why": "LAW 38 rule 2: the hourglass is a DRAWN object, so the emphasis is BOXING, a terracotta rectangle with a small radius around it (on the board, box_emphasis). It carries no raster text. Never a ring."
        }
      ]
    },
    {
      "i": 2,
      "t_start": 9.1,
      "t_end": 12.52,
      "words": "which sometimes have up to four different accounts all at once",
      "says": "Power users run up to four accounts at the same time.",
      "picture": "The box and the price label leave. On 'up to' the empty hourglass shrinks and moves to the left end of a row; on 'four', 'different', 'accounts' three more FULL hourglasses pop in beside it, one per word. 4 ACCOUNTS is written under the row. On 'all at once' the three full ones all start pouring TOGETHER, the same drop on the same frame.",
      "whiteboard": "New chapter: the empty hourglass redrawn small at the left, three more drawn to its right one per word, 4 ACCOUNTS written under the row, then the sand in all three drops together.",
      "objects": [
        "four hourglasses row",
        "4 ACCOUNTS"
      ],
      "emphasis": []
    },
    {
      "i": 3,
      "t_start": 12.78,
      "t_end": 15.7,
      "words": "to make sure that they can keep building the things that they need.",
      "says": "They do it so they never have to stop building.",
      "picture": "Under the row a brick wall rises course by course: the bottom course on 'keep', the middle on 'building', the top on 'things', and every time a course lands the sand in the three running hourglasses drops again. KEEP BUILDING is written under the wall.",
      "whiteboard": "Same chapter: the wall is drawn course by course under the row, the top sand in the hourglasses erased a step with each course, KEEP BUILDING written under it.",
      "objects": [
        "brick wall",
        "four hourglasses row",
        "KEEP BUILDING"
      ],
      "emphasis": []
    },
    {
      "i": 4,
      "t_start": 16.08,
      "t_end": 20.64,
      "words": "Now follow for more AI news, videos, and tutorials each and every single day and catch you in the next one.",
      "says": "The daily sign-off.",
      "picture": "The opaque cream sheet rises over the finished board and the chassis outro lockup lands on a small ink hourglass: terracotta rule, mono handle, daily AI micro-line.",
      "whiteboard": "The rising sheet, then the same lockup on the board's own small hourglass.",
      "objects": [
        "outro lockup",
        "small hourglass glyph"
      ],
      "emphasis": []
    }
  ],
  "bespoke_objects": [
    {
      "name": "hourglass price tag",
      "t": 2.9,
      "bbox": [
        0.4537,
        0.1781,
        0.75,
        0.3135
      ],
      "space": "norm",
      "why_bespoke": "A reset of a usage limit has no logo; an hourglass that has run out and gets flipped, wearing a '$' price tag, IS 'selling resets' in one picture. It is the hook object (LAW 20) and it carries a state from frame one (running out). Its UI-glyph reading (wait) is the same name as the object, so it cannot misread the way the database drum did.",
      "how_drawn": "Ink-line hourglass: two flat mount-filled caps, two side posts, a curved card-filled glass with terracotta sand in the bulbs; a pointed card-filled price tag with a punched hole and a JetBrains Mono '$' hangs from the top cap on a thin string. One object, one bbox (the tag is part of it)."
    },
    {
      "name": "four hourglasses row",
      "t": 12.7,
      "bbox": [
        0.2148,
        0.1573,
        0.7852,
        0.2412
      ],
      "space": "norm",
      "why_bespoke": "'Four different accounts all at once' is four allowances running in parallel; four copies of the same hourglass, three pouring together and one already empty, show both the count and the simultaneity that a counter or four logos cannot.",
      "how_drawn": "The same hourglass drawn at 0.62 scale four times in an evenly spaced row (a >=3 identical-shape series, one object), the left one empty, the other three with sand falling."
    },
    {
      "name": "rising brick wall",
      "t": 15.4,
      "bbox": [
        0.3056,
        0.2948,
        0.6944,
        0.3604
      ],
      "space": "norm",
      "why_bespoke": "'Keep building the things they need' is the payoff: a wall that keeps gaining courses while the hourglasses drain is the work the usage buys, drawn as a thing and not as a label.",
      "how_drawn": "Three courses of card-filled ink-outline bricks with small radii in running bond (5, 4 + two halves, 5), popping in course by course from the bottom."
    }
  ],
  "labels": [
    {
      "for": "hourglass",
      "text": "RESETS",
      "place": "above",
      "at": 2.18,
      "note": "LAW 39 + LAW 9: the KEY TERM, written first and alone at 48 px (25.6 design units), centred on the hourglass's own axis at its displaced seat, entirely above it; 'resets' ends 2.14 (LAW 24, no peek-ahead). Declared data-label-for=\"hourglass\" on the DOM and label_plan= on the board."
    },
    {
      "for": "hourglass",
      "text": "$200 / MONTH",
      "place": "below",
      "at": 4.5,
      "note": "LAW 39: under the centred hourglass. '$200' lands on '$200' (4.50), '/ MONTH' on 'per' (5.36), both inside LABEL_WINDOW. Word-sync: the typed number is the spoken number. Declared data-label-for=\"hourglass\"."
    },
    {
      "for": "four hourglasses row",
      "text": "4 ACCOUNTS",
      "place": "below",
      "at": 11.62,
      "note": "LAW 39 / LAW 50: under the row, centred on the row's own axis x 540 (the row's extent 232..848); 'accounts' ends 11.60. Same placement as every other object label in the video (below). Declared data-label-for=\"hg-row\"."
    },
    {
      "for": "brick wall",
      "text": "KEEP BUILDING",
      "place": "below",
      "at": 14.6,
      "note": "LAW 39 / LAW 50: under the wall, centred on its axis; 'building' ends 14.54. Declared data-label-for=\"wall\"."
    }
  ],
  "lifetimes": [
    {
      "mark": "hourglass",
      "t_from": 0.1,
      "t_to": 10.68,
      "anchor": "hourglass",
      "note": "LAW 42: the spine of chapter 0 (reset -> the $200 plan running dry); at 10.68 it hands over, in place, to hg-1, the left hourglass of the row."
    },
    {
      "mark": "openai-tile",
      "t_from": 1.06,
      "t_to": 3.58,
      "anchor": null,
      "note": "beat 0 only."
    },
    {
      "mark": "conn-sell",
      "t_from": 1.4,
      "t_to": 3.58,
      "anchor": null,
      "note": "beat 0 only."
    },
    {
      "mark": "price-tag",
      "t_from": 2.4,
      "t_to": 3.58,
      "anchor": null,
      "note": "beat 0 only; part of the hourglass block while it is on."
    },
    {
      "mark": "key-term",
      "t_from": 2.18,
      "t_to": 3.58,
      "anchor": null,
      "note": "beat 0 only: the next beat's hourglass is the $200 plan, not the reset."
    },
    {
      "mark": "key-200",
      "t_from": 4.5,
      "t_to": 9.38,
      "anchor": null,
      "note": "beat 1 only."
    },
    {
      "mark": "emph-hourglass",
      "t_from": 7.04,
      "t_to": 9.18,
      "anchor": null,
      "note": "the emphasis lives only inside the beat that argues it."
    },
    {
      "mark": "hg-row (hg-1..hg-4)",
      "t_from": 10.6,
      "t_to": 16.56,
      "anchor": null,
      "note": "chapter 1, held until the outro sheet covers it (finite t_to)."
    },
    {
      "mark": "key-accounts",
      "t_from": 11.62,
      "t_to": 16.56,
      "anchor": null,
      "note": "chapter 1, to the sheet."
    },
    {
      "mark": "wall",
      "t_from": 13.82,
      "t_to": 16.56,
      "anchor": null,
      "note": "chapter 1, to the sheet."
    },
    {
      "mark": "key-building",
      "t_from": 14.6,
      "t_to": 16.56,
      "anchor": null,
      "note": "chapter 1, to the sheet."
    }
  ],
  "connectors": [
    {
      "to": "hourglass",
      "from": [
        "openai-tile"
      ],
      "note": "ONE arrow (the letter of LAW 40 binds two or more), built with anchor_points anyway: OpenAI tile right-edge centre -> the hourglass's VIRTUAL rectangle left-edge centre, level, never onto the curved glass outline. data-connect-to=\"hourglass\" + data-overlap-ok."
    }
  ],
  "blocks": [
    [
      "hourglass",
      "price-tag"
    ],
    [
      "hourglass",
      "key-term"
    ],
    [
      "hourglass",
      "key-200"
    ],
    [
      "hourglass",
      "emph-hourglass"
    ],
    [
      "openai-tile",
      "mark-openai"
    ],
    [
      "hg-row",
      "key-accounts"
    ],
    [
      "wall",
      "key-building"
    ]
  ],
  "blocks_note": "LAW 41: the tag hangs off the hourglass on a string and is one object with it; each key is welded to what it names; the emphasis box is welded to its hourglass. The row of four identical hourglasses and the wall's bricks are inferred series. Non-block gutters aimed >= 24 core px (tile -> hourglass 108, row key -> wall 39).",
  "pointing_cues": [],
  "pointing_cues_note": "LAW 37: pointing_cues.py --vid openairesets returned 'No pointing cue in this take' (gen/_cues_openairesets.json, cues []). Nothing answered, nothing waived; no source post is raised (GLOBAL LAW 3).",
  "boards": {
    "mode": "chapters",
    "why": "LAW 43: CHAPTERS ARE THE DEFAULT, and the script has two idea groups: what OpenAI sells and why one plan is not enough (one hourglass), then how power users cope (four hourglasses feeding a wall). The hourglass is carried across the seam as the left hourglass of the row, so the handover lands on an idea (LAW 45).",
    "chapters": [
      {
        "i": 0,
        "t_start": 0.1,
        "t_end": 8.8,
        "erase_at": 9.1,
        "holds": [
          "hourglass",
          "openai-tile",
          "conn-sell",
          "price-tag",
          "key-term",
          "key-200",
          "emph-hourglass"
        ],
        "why_together": "The product (a reset for sale) and the problem it answers (the $200 plan running dry): one hourglass."
      },
      {
        "i": 1,
        "t_start": 9.1,
        "t_end": 15.7,
        "erase_at": null,
        "holds": [
          "hg-row",
          "key-accounts",
          "wall",
          "key-building"
        ],
        "why_together": "How power users cope today: four allowances pouring at once so the wall keeps rising."
      }
    ],
    "key_term": "RESETS"
  },
  "cast": [],
  "cast_note": "THE ROSTER IS TOPICAL: the script makes no comparison between tools, so there is no roster. The one mark the short names, OpenAI (registry key 'openai', assets/logos/ai-models/openai.png), is the story's own subject and sits on the stage, not in a cast.",
  "cutout_logo_lanes": [
    "chatgpt",
    "codex",
    "claude",
    "claude-code",
    "cursor"
  ],
  "cutout_logo_lanes_note": "Topical: the plans that hit usage limits. ChatGPT and Codex are the OpenAI products whose limits get reset; Claude (the other $200 plan) and Claude Code / Cursor are the neighbouring building tools power users juggle across accounts. None is the stage mark (openai), none repeated. Files: ai-models/chatgpt-color.png, coding-tools/codex-color.png, ai-models/claude-color.png, coding-tools/claudecode-color.png (MARK IDENTITY: the outline-free mascot, never the sticker), coding-tools/cursor.png.",
  "open_questions": [
    "Wing review: prompt0 landed (prep/stages/openairesets.prompt0.json, ok, 12.2 s) with wing_review TRUE for openairesets - the Astra matte step and the cutout author own it. Markers at plan time: cut ok (63.7 s, cut master 20.64 s, corroboration 'model-authored keep ranges'), plate ok (92.6 s, overwide_applied true), selection ok, cues ok, track RUNNING (backend matanyone2, no cost yet), ship NOT landed.",
    "The hourglass silhouette is also the classic 'wait' cursor glyph; unlike the database drum its glyph reading and its object name are the same word, so it was kept. If Miguel dislikes it, the fallback is a coin-slot 'insert coin to continue' machine."
  ],
  "open_doubts": []
}
```
