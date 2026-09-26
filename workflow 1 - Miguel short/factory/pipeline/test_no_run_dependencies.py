"""NOTHING PERMANENT LIVES IN A RUN (Miguel, 2026-09-20).

Run folders are disposable. This test fails the moment a permanent file names a run by
number, because that is how 100 GB of run media became undeletable: STANDARD, the skill
and the workflow pointed at tools, reference builds and evidence inside shorts_run3,
run5, run9, run15... The homes are pipeline/, formats/, references/, workflow_versions/.
LEARNINGS.md is exempt (a dated ledger). `shorts_run99x` are the test fixture names.
"""
import re
import unittest
from pathlib import Path

F = Path(__file__).resolve().parents[1]
WS = Path.home() / "Documents/Workspace"
FORBIDDEN = re.compile(r"shorts_run(?!99\d\b)\d+|shorts_tiktok_remake_\d+|format_lab/|/\.tmp[_/]|\.pre-[a-z0-9]+\b|\.bak\b")
# 2026-09-20, second audit: a run under another name, the retired lab, factory-root scratch and
# suffix backups beside a live tool are the same disease as a run number.
PERMANENT = [F / "STANDARD.md", F / "PRODUCTION.md", F / "STAGES.md", F / "README.md", F / "references/README.md",
             WS / ".claude/skills/shorts-factory/SKILL.md", WS / ".agents/skills/shorts-factory/SKILL.md",
             WS / ".claude/workflows/daily-shorts.js"]
TREES = [F / "pipeline", F / "formats"]
SKIP_DIRS = {"__pycache__", "sessions", "node_modules", "fixtures", ".venv-birefnet", "source", "_shared"}  # fixtures are frozen DATA and may record old run paths
CODE = {".py", ".md", ".mjs", ".js", ".sh", ".json", ".txt"}


def files():
    for p in PERMANENT:
        if p.exists():
            yield p
    for tree in TREES:
        for p in tree.rglob("*"):
            if p.is_file() and p.suffix in CODE and not (SKIP_DIRS & set(p.parts)) \
                    and ".pre-" not in p.name and ".bak" not in p.name and p.name != Path(__file__).name:
                yield p


class NoRunDependencies(unittest.TestCase):
    def test_no_permanent_file_names_a_run(self):
        hits = []
        for p in files():
            try:
                text = p.read_text(errors="ignore")
            except OSError:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if FORBIDDEN.search(line):
                    hits.append(f"{p.relative_to(WS)}:{i}: {line.strip()[:120]}")
        self.assertEqual(hits, [], "permanent files must not name a run by number:\n" + "\n".join(hits[:40]))

    def test_references_home_exists(self):
        for sub in ("builds/hermes_icon/hermes_icon_gen.py", "builds/graphic_chart/geminitools_scene.py",
                    "evidence/clerk_v3_calibration/review/clerk_v3_calibration.md", "ab/impeccable_2026-08_compare_ab", "README.md"):
            self.assertTrue((F / "references" / sub).exists(), sub)
        for tool in ("qc/gate3_gemini.py", "asset_judge_v3.py", "ink_double_scan.py", "runs.py"):
            self.assertTrue((F / "pipeline" / tool).exists(), tool)


if __name__ == "__main__":
    unittest.main()
