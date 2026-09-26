"""Emit timeline.json — beats, faceless word captions, split phrase captions, variants."""
import json
import re
from pathlib import Path

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
words = [w for w in json.loads((FACTORY / "analysis/transcript_tight.json").read_text())["words"]
         if w["type"] == "word"]

PROPER = {"claude", "google", "workspace", "microsoft", "365", "slack", "notion", "opus", "ai",
          "sonnet", "haiku", "4.3", "4.6"}

# ---- beats (locked in STYLE_SPEC.md) ----
BEATS = [
    {"id": "hook", "start": 0.00, "end": 5.20},
    {"id": "memory", "start": 5.28, "end": 11.50},
    {"id": "websearch", "start": 11.62, "end": 18.35},
    {"id": "projects", "start": 18.46, "end": 25.50},
    {"id": "thinking", "start": 25.62, "end": 32.05},
    {"id": "connectors", "start": 32.14, "end": 39.50},
    {"id": "freeplan", "start": 39.56, "end": 47.90},
    {"id": "cta", "start": 48.02, "end": 50.91},
]

# ---- faceless word captions: 1 word at a time, feature scenes only (5.28 - 47.90) ----
fc = []
for i, w in enumerate(words):
    t0 = w["start"]
    if t0 < 5.28 or t0 >= 47.90:
        continue
    t1 = words[i + 1]["start"] if i + 1 < len(words) else w["end"] + 0.2
    t1 = min(t1, w["end"] + 0.6)  # don't hold forever across pauses
    text = re.sub(r"[^\w.'&$%-]", "", w["text"])
    low = text.lower().strip(".")
    display = text if low in PROPER or text[:1].isupper() and low in PROPER else text.lower()
    display = display.strip('.,!?";:').strip()
    if not display:
        continue
    # fix the mis-recognized "4.3" -> narrator means Sonnet 4.6 but caption mirrors audio word
    fc.append({"t0": round(t0, 2), "t1": round(t1, 2), "text": display})

# ---- split phrase captions: 2-4 word chunks, punctuation kept, full video ----
phrases, cur = [], []
for w in words:
    cur.append(w)
    text = " ".join(x["text"] for x in cur)
    endp = re.search(r"[.,!?]$", w["text"])
    nxt_gap = False
    idx = words.index(w)
    if idx + 1 < len(words):
        nxt_gap = words[idx + 1]["start"] - w["end"] > 0.32
    if len(cur) >= 4 or endp or nxt_gap:
        phrases.append({"t0": round(cur[0]["start"], 2), "t1": round(w["end"] + 0.12, 2), "text": text})
        cur = []
if cur:
    phrases.append({"t0": round(cur[0]["start"], 2),
                    "t1": round(cur[-1]["end"] + 0.12, 2), "text": " ".join(x["text"] for x in cur)})
# make captions contiguous (hold until next starts)
for i in range(len(phrases) - 1):
    phrases[i]["t1"] = round(min(phrases[i + 1]["t0"], phrases[i]["t1"] + 0.5), 2)

# ---- variant content seeds (style locked; copy varies) ----
MEMORY_MSGS = [
    "Remember I use TypeScript & dark mode", "Remember I write in French & love bullet points",
    "Remember my startup is called Flowly", "Remember I prefer short, direct answers",
    "Remember I code in Python & use VS Code", "Remember my deadline is every Friday",
    "Remember I run a YouTube channel", "Remember I'm learning UX design",
    "Remember my team ships on Mondays", "Remember I want examples with every answer",
]
SEARCH_RESULTS = [
    "Claude Fable 5 launched today with stronger reasoning and…",
    "Anthropic ships new free tier features for Claude users…",
    "Claude adds real-time web search with cited sources…",
    "New Claude update brings memory to the free plan…",
    "Claude can now browse the live web for answers…",
    "Anthropic expands Claude's free plan worldwide…",
    "Claude's new tools put paid features in free hands…",
    "Real-time answers arrive in Claude's free tier…",
    "Claude update: search the web, get the sources…",
    "Anthropic makes Claude's best features free…",
]
PROJECT_LISTS = [
    ["Client Work", "Marketing", "Research"], ["Design System", "Content", "Growth"],
    ["Newsletter", "Landing Page", "Outreach"], ["Portfolio", "Side Hustle", "Studies"],
    ["Product Launch", "Support", "Docs"], ["YouTube", "Scripts", "Thumbnails"],
    ["Sales", "Onboarding", "Playbooks"], ["App Redesign", "User Tests", "Roadmap"],
    ["SEO", "Blog Posts", "Backlinks"], ["Pitch Deck", "Financials", "Hiring"],
]
THINKING_STEPS = [
    ["Analyzed the problem", "Reasoned step by step"],
    ["Broke the problem into steps", "Checked each assumption"],
    ["Mapped out the edge cases", "Verified the logic twice"],
    ["Outlined the approach", "Stress-tested the answer"],
    ["Split the task into parts", "Validated every step"],
    ["Explored three solutions", "Picked the strongest one"],
    ["Listed the constraints", "Worked through them in order"],
    ["Framed the problem clearly", "Reasoned to a conclusion"],
    ["Considered the trade-offs", "Justified the final choice"],
    ["Structured the reasoning", "Double-checked the result"],
]
ICON_ORDERS = [
    ["google", "microsoft", "slack", "notion"], ["google", "notion", "slack", "microsoft"],
    ["slack", "notion", "google", "microsoft"], ["notion", "google", "microsoft", "slack"],
    ["microsoft", "google", "notion", "slack"], ["google", "slack", "notion", "microsoft"],
    ["notion", "slack", "microsoft", "google"], ["slack", "google", "microsoft", "notion"],
    ["microsoft", "notion", "google", "slack"], ["google", "microsoft", "notion", "slack"],
]

variants = []
for i in range(10):
    variants.append({
        "id": f"v{i+1:02d}",
        "rotation_flip": i % 2 == 1,          # mirror card rotation signs on odd variants
        "memory_msg": MEMORY_MSGS[i],
        "search_result": SEARCH_RESULTS[i],
        "project_list": PROJECT_LISTS[i],
        "thinking_steps": THINKING_STEPS[i],
        "icon_order": ICON_ORDERS[i],
        "sfx_seed_ms": (i * 7) % 21 - 10,
    })

out = {
    "duration": 50.91, "fps": 30, "beats": BEATS,
    "captions_faceless": fc, "captions_split": phrases, "variants": variants,
}
(FACTORY / "pipeline/timeline.json").write_text(json.dumps(out, indent=1))
print(f"faceless captions={len(fc)} split phrases={len(phrases)} variants={len(variants)}")
for p in phrases[:8]:
    print(p)
