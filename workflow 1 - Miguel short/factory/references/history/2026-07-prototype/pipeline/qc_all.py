"""Run the Gemini QC gate on every rendered output; write qc/SUMMARY.md.

Skips videos that already have a passing verdict JSON unless --force.
"""
import json
import subprocess
import sys
from pathlib import Path

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
PY = Path.home() / "Documents/Workspace/.venv/bin/python"
QC = FACTORY / "pipeline/qc_video.py"

force = "--force" in sys.argv
rows = []
for folder, fmt in [("faceless_hyperframes", "faceless"), ("split_hyperframes", "split"),
                    ("FINAL", "faceless")]:  # FINAL fmt resolved per-file below
    for mp4 in sorted((FACTORY / "output" / folder).glob("*.mp4")):
        if folder == "FINAL":
            fmt = "split" if mp4.name.startswith("S") else "faceless"
        label = mp4.stem
        vfile = FACTORY / f"qc/{label}.json"
        if vfile.exists() and not force:
            v = json.loads(vfile.read_text())
        else:
            print("QC", label, flush=True)
            r = subprocess.run([str(PY), str(QC), str(mp4), fmt, "--label", label],
                               capture_output=True, text=True)
            try:
                v = json.loads(vfile.read_text())
            except Exception:
                print("  QC ERROR", r.stderr[-500:], flush=True)
                v = {"pass": False, "summary": "QC harness error", "issues": []}
        rows.append((label, v))
        print(f"  {'PASS' if v['pass'] else 'FAIL'} {label}: {v['summary'][:100]}", flush=True)

lines = ["# QC Summary\n", "| video | verdict | layout | captions | timing | audio | style | issues |",
         "|---|---|---|---|---|---|---|---|"]
npass = 0
for label, v in rows:
    ok = "✅ PASS" if v["pass"] else "❌ FAIL"
    npass += 1 if v["pass"] else 0
    iss = "; ".join(f"[{i['severity']}] {i['description'][:60]}" for i in v.get("issues", [])[:3]) or "—"
    lines.append(f"| {label} | {ok} | {v.get('score_layout','-')} | {v.get('score_captions','-')} | "
                 f"{v.get('score_timing','-')} | {v.get('score_audio','-')} | {v.get('score_style_match','-')} | {iss} |")
lines.append(f"\n**{npass}/{len(rows)} passing**")
(FACTORY / "qc/SUMMARY.md").write_text("\n".join(lines))
print(f"\n{npass}/{len(rows)} passing -> qc/SUMMARY.md")
