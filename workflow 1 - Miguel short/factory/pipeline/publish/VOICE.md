# Miguel's voice for shorts captions, descriptions and tags

Source: the complete transcripts of 74 shorts (29 Ready to Publish, 45 published on YouTube in August 2026) plus the 45 YouTube descriptions and tag lists that shipped with them. Read in full on 2026-09-07. The 10 Partially Published packages keep their transcripts inside the editable-history archives and were not read; the 20 unedited Sept 4 recordings have no transcript yet.

## How Miguel talks

1. **The first sentence is the claim, and it is a strong one.** "LLMs are dead." "Brains don't matter anymore." "Claude is holding you hostage." "You can now buy a full-time employee for $12,000." "People who tell you to use open source models are lying to you." A number or a price is the favourite hook: 33 cents, 82%, 1.5 terabytes, 40 times, $2,000.
2. **Then he earns it in plain words.** The pivot is "Now, ..." or "Let me explain to you." followed by one concrete case, usually a person: "like this guy right here on X", "this user on X did exactly that", "according to this latest tweet by Tibo". Never abstract for more than one sentence.
3. **Every explanation lands on what it lets you do.** "You can now delegate real work." "Go ahead, open the application, and create your first automation." "Start asking yourself: what is my advantage when speed is no longer the moat?" He speaks to one person, second person, imperative.
4. **He names products exactly and compares them as equivalents.** "Kimi Work is the equivalent of ChatGPT Work and Claude Cowork." "The best of both worlds." Lists of tools are common and always concrete: ChatGPT Work, Codex, Claude Cowork, Claude Code, Hermes Agent, Grok Build, OpenCode.
5. **Numbers are the argument.** Prices, percentages, RAM, token costs, days apart. When a number is missing he gives the order of magnitude: "five grand to 10 grand", "a couple of thousands of dollars".
6. **He is enthusiastic but keeps a skeptic's line.** "Of course, this comes from the lab that created the model, so we have to take it with a grain of salt." "We don't really know where this is going, but we certainly have to keep up." "We'll see if this feature survives."
7. **One idea per short, one takeaway per idea.** The closing thought is a judgment, not a summary: "The barrier to entry got lower, but expectations got higher." "It's still a human plus machine combo." "At $12,000, this is still not a toy, it's a business investment."
8. **Fixed sign-off, spoken:** "Now, follow for more AI news and tutorials each and every single day, and catch you in the next one." Variants swap "news" for "videos" or "tools". In writing it is optional and follows the useful content, see below.
9. **Vocabulary**: simple, everyday, no jargon without a one-clause definition ("a harness is something that gives a model the capacity to interact with the real world"). Recurring words: "fantastic", "huge", "game changer" (rare), "shocked", "unbelievable", "the equivalent of", "the best of both worlds", "each and every single day", "for you", "your business". Spoken tics to drop in writing: "literally", "actually", "now" as a filler, "you see".
10. **Never**: em dashes, corporate phrasing ("leverage synergies"), exclamation marks in stacks, emoji walls, clickbait that the video does not pay off, hedged verbs ("might potentially"). He does not write in the first person plural about "we at Genial"; captions are "I" or "you".

## Description policy, 8 September 2026

This is the factory's generation prompt for `Publishing/captions.json`, consumed by
`publish_short.py`. It replaces the uniform two-sentence/follow/#AINews template.
The voice observations above remain useful; historical samples are not the new
description structure. Titles retain the existing upload-to-youtube Title Formula
Guide and factory checklist. Improve descriptions without silently rewriting an
approved title, cover, recording, or already scheduled/published post.

Read the COMPLETE final tight transcript for this exact Short, its source/context
material, existing captions and approved title before classifying or writing.
Use `Source Assets/Cut/transcript_tight.json` or a verified packaged transcript.
If it lives only in editable history, recover that exact source first; never
substitute another run's same-named recording or YouTube auto-captions. Read all
referenced material needed for promised resources. Missing source means hold the
affected description, not guess. No additional model call is required: the
current metadata author makes and reviews the editorial decision.

## Choose the description from the video's purpose

`content_type` and `description_length` are separate from the vertical video
format. A detailed description does not turn a Short into a long-form upload.
Classify by meaning, not keywords, duration, the title, or the habitual spoken
sign-off "AI news and tutorials". Record the decision and a transcript quote in
`description_strategy` before drafting all three platforms.

| Content type | Viewer promise | Description length and contents |
|---|---|---|
| `news` | A launch, update, availability change, benchmark or timely development; what changed and why it matters | `concise`: the news, why it matters, and the useful qualifications directly in the description. Keep necessary qualifications. No invented setup guide. |
| `tutorial` | A repeatable action, workflow, setting or copyable prompt the viewer can use | `detailed`: outcome first, then the actual steps/settings or complete promised prompt, useful caveats and verified resources. Usually 3 to 6 short lines. A single-action tip may use `concise` if that preserves everything useful. |
| `explainer` | A comparison, opinion, case study or explanation without a repeatable procedure | `concise`: claim plus supporting example/takeaway. Do not force news or a tutorial onto it. |

For mixed videos, choose the dominant promise: "a tool launched and can edit
slides" is news even if it shows a demo; "here is how to configure five settings"
is a tutorial even if the feature is new. Preserve the secondary context in one
sentence. If uncertain, use a concise factual description and state the ambiguity
in the internal rationale. Do not manufacture steps to justify a longer choice.

Length is an editorial target, not an SEO claim or a minimum to pad to:
- YouTube: roughly 30 to 70 body words for concise; 80 to 220 for detailed.
- Instagram: concise news or a scannable tutorial with the useful steps intact.
- TikTok: compact news; tutorials may be longer than the former 300-character
  rule when actual steps or a promised prompt justify it.
- No compulsory biography, broad social directory, repeated title, generic
  summary heading, or filler to reach a target. Never invent chapters for Shorts.
  Complete promised instructions/resources outrank target length. YouTube's
  5,000-character hard limit still applies; never silently truncate.

## Apply the description and funnel advice to Shorts

Source: `output/transcripts/roast-growth-strategy-feedback-2026-09-07/transcript.txt`
and Miguel's 7 September description session. Nick's direct advice was compact
benefit-led links above the fold, recognizable chapter headings where appropriate,
and a coherent funnel. The adaptive lengths here are Miguel's Shorts request,
not a claim that Nick prescribed word counts or a Shorts template.

Start a Short with its specific value in natural search language: the actual
tool and problem/result. Deliver the useful answer in the description itself.
An optional compact save/follow/question line may follow the useful content.
Preserve the speaker's certainty, attribution and limitations. A lab's claim is
not an independently measured result. An old recording does not establish a
current price, ranking or release date; prefer "the launch covered here" over
an invented "today". Do not import facts from another video.

### Current direction: deliver the value here

Miguel, 8 September 2026: keep the useful material in the description for now.
This replaces the earlier default funnel/profile/related-video routing proposal.
Do not make a viewer leave the post to receive the answer promised by this Short.

- Put practical steps, settings, commands and complete copyable prompts directly
  in each platform's description when supported by the source. Include useful
  prerequisites, limitations and tradeoffs. More value means actionable detail,
  not an inflated word count or invented instructions.
- News still stays concise when the useful information fits in a few sentences.
  Tutorials may be longer; preserve all meaningful steps. Do not discard the
  prompt or checklist merely to meet the suggested length range.
- Do not default to "link in bio", "watch the full tutorial", "download the
  checklist", "comment a keyword" or "DM me for the prompt". Do not invent a
  resource page, attachment, tutorial, giveaway, automated reply or community.
- Omit promotional website URLs when they cannot function as clickable links in
  the exact publishing surface. Ordinary pasted URLs in YouTube Shorts do not
  become clickable. Special link features on other platforms are not assumed
  available; a valid website alone is not proof the publishing route supports it.
- A URL that is an essential part of a copyable command or prompt remains literal
  instructional content. Preserve it when source-supported; do not mistake it
  for a promotional link or silently break the instructions. If an actual
  promised external resource cannot be delivered in the description or through
  a verified usable link, disclose the missing input before publication.
- At most one optional save/follow/specific-question CTA after the useful text.
  It may be omitted. Keep the correct native platform handle for a follow CTA.
  Do not replace useful detail with engagement requests.

The existing Genial booking, newsletter and LinkedIn destinations remain the
long-form policy; they are not a required block for Shorts. No new resource hub,
profile change, messaging automation or related-video attachment is part of this
change. A later explicit direction can add a verified distribution route.

Platform references checked 8 September 2026:
[YouTube ordinary URLs versus mentions and special links](https://support.google.com/youtube/answer/13748639),
[TikTok Destination Links require a separate eligible setup](https://ads.tiktok.com/help/article/about-destination-links?lang=en),
and [Meta documents business-plan Reel links](https://about.fb.com/news/2024/07/launching-meta-verified-subscription-plans-for-businesses-on-instagram-and-facebook-in-india/).
These exceptions do not justify inserting an ordinary URL and claiming it works.

## Resources, tags and platform writing

Include any promised prompt, command or resource, using the actual source.
Keep command syntax and meaningful settings intact; clean speech filler only.
Give the complete useful content inline whenever possible, including promised
prompts and small tutorials. Add an external resource link only if its exact
source and usability on the publishing surface are verified. For an applicable
tool link, follow upload-to-youtube's affiliate lookup; never invent a referral
URL. If a promise cannot be fulfilled, record the missing input and hold for
correction. Do not
drop it just because the video was classified as news. Optional sources/tools
sections appear only when useful, never as empty template headings.

Write each platform from the same transcript and strategy, with its own wording.
Handles: YouTube `@migueltorrezai`; TikTok/Instagram `@migueltorrez.ai`.
YouTube gets at most 3 relevant hashtags; TikTok/Instagram get a small set of
specific topical hashtags only where useful. `#AINews` and the `AI News` tag are
appropriate for news, not obligatory on evergreen tutorials. YouTube tags use
title case, actual product/topic first, then a few relevant categories. Preserve
the existing title casing validation. No cloned description/tag set across a batch.

## Author readback and publishing handoff

After drafting, read all three final texts against the complete transcript:
the title and body promise the same result, every claim is supported, steps and
promised resources are delivered inline where possible, no unsupported links or
redirect promises, no misleading freshness,
no generic fluff, correct handles and topical tags. Show the full descriptions
and the classification/rationale in the batch review. Updating these instructions
does not authorize changing existing posts or publishing a batch.

Add this internal object alongside `youtube`, `tiktok`, and `instagram` in
`captions.json`. Paths are relative to the package (an exact absolute source path
is also accepted); SHA256 is of the full source file, not the quote. Evidence is
one or more verbatim transcript excerpts. Never put this bookkeeping in captions.

```json
"description_strategy": {
  "version": "2026-09-08",
  "content_type": "tutorial",
  "description_length": "detailed",
  "reason": "Five settings are explained; readers benefit from a reusable checklist.",
  "transcript_path": "Source Assets/Cut/transcript_tight.json",
  "transcript_sha256": "<actual SHA256>",
  "evidence": ["<actual excerpt from the full transcript>"],
  "resource_review": "<promises found and fulfilled, or no resource/prompt promises>"
}
```

Run `pipeline/publish/description_policy.py --package "<package>"` before the
batch proposal. `publish_short.py` runs the same read-only preflight for pending
platforms before any upload. Old captions lacking a strategy need author review
and regeneration under this policy; do not fabricate a strategy around old copy.
The validator checks source binding, evidence presence and structural limits;
it cannot certify semantic accuracy or that the author read the whole transcript.
That remains the author's required readback. No extra audit agent or API spend.
