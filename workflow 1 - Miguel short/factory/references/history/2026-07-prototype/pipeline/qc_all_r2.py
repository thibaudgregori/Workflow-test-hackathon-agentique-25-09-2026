"""Round-2 QC sweep: gate every *_r2_* render with the R2 rubric; write qc/SUMMARY_R2.md."""
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
    pattern = "*.mp4" if folder == "FINAL" else "*_r2_*.mp4"
    for mp4 in sorted((FACTORY / "output" / folder).glob(pattern)):
        if folder == "FINAL":
            fmt = "split" if mp4.name.startswith("S") else "faceless"
        label = mp4.stem
        vfile = FACTORY / f"qc/{label}.json"
        if vfile.exists() and not force:
            v = json.loads(vfile.read_text())
        else:
            print("QC", label, flush=True)
            subprocess.run([str(PY), str(QC), str(mp4), fmt, "--label", label, "--r2"],
                           capture_output=True, text=True)
            try:
                v = json.loads(vfile.read_text())
            except Exception:
                v = {"pass": False, "summary": "QC harness error", "issues": []}
        rows.append((label, v))
        print(f"  {'PASS' if v['pass'] else 'FAIL'} {label}: {v['summary'][:90]}", flush=True)

lines = ["# QC Summary — Round 2\n",
         "| video | verdict | layout | captions | timing | audio | style | issues |", "|---|---|---|---|---|---|---|---|"]
npass = 0
for label, v in rows:
    ok = "✅" if v["pass"] else "❌"
    npass += 1 if v["pass"] else 0
    iss = "; ".join(f"[{i['severity']}] {i['description'][:70]}" for i in v.get("issues", [])[:3]) or "—"
    lines.append(f"| {label} | {ok} | {v.get('score_layout','-')} | {v.get('score_captions','-')} | "
                 f"{v.get('score_timing','-')} | {v.get('score_audio','-')} | {v.get('score_style_match','-')} | {iss} |")
lines.append(f"\n**{npass}/{len(rows)} passing**")
(FACTORY / "qc/SUMMARY_R2.md").write_text("\n".join(lines))
print(f"\n{npass}/{len(rows)} passing -> qc/SUMMARY_R2.md")
