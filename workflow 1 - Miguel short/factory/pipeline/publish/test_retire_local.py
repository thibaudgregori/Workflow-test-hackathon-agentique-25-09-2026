"""retire_local.run_media picks exactly the recording's heavy run artifacts (2026-09-20)."""
import json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import retire_local as rl


class RunMediaTests(unittest.TestCase):
    def test_only_heavy_dirs_and_only_this_recording(self):
        with tempfile.TemporaryDirectory(dir=rl.FACTORY) as tmp:
            run = Path(tmp) / "shorts_run999"
            for d in ("cuts/grokwatch", "cuts/grokwatchdog", "cuts/grok", "matting/grokwatch", "matting_fallback/grokwatch_v2",
                      "output/frames_grokwatch_cutout", "stage/grokwatch_whiteboard", "staging/grokwatch", "projects_4k/grokwatch_split",
                      "gen", "projects/grokwatch_split", "review", "plans", "paperwork", "intake", "prep"):
                (run / d).mkdir(parents=True)
            for f in ("output/grokwatch_split.mp4", "output/other_split.mp4", "gen/grokwatch_scene.py", "projects/grokwatch_split/index.html",
                      "review/clerk_v3_grokwatch.md", "plans/grokwatch_plan.json", "cuts/grokwatch/master.mp4"):
                (run / f).write_text("x")
            (run / "projects/grokwatch_split/.fr_grokwatch").mkdir()
            pkg = Path(tmp) / "pkg"; (pkg / "Publishing").mkdir(parents=True)
            (pkg / "Publishing/package.json").write_text(json.dumps({"internal_source": {"run": str(run), "recording_id": "grokwatch"}}))
            got = sorted(str(x.relative_to(run)) for x in rl.run_media(pkg) if run in x.parents)
            self.assertEqual(got, sorted([
                "cuts/grokwatch", "matting/grokwatch", "matting_fallback/grokwatch_v2", "output/frames_grokwatch_cutout",
                "output/grokwatch_split.mp4", "stage/grokwatch_whiteboard", "staging/grokwatch", "projects_4k/grokwatch_split",
                "projects/grokwatch_split/.fr_grokwatch"]))
            for keep in ("gen/grokwatch_scene.py", "projects/grokwatch_split/index.html", "review/clerk_v3_grokwatch.md",
                         "plans/grokwatch_plan.json", "cuts/grokwatchdog", "cuts/grok", "output/other_split.mp4"):
                self.assertNotIn(keep, got)

    def test_run_outside_factory_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "elsewhere"; (run / "cuts/x").mkdir(parents=True)
            pkg = Path(tmp) / "pkg"; (pkg / "Publishing").mkdir(parents=True)
            (pkg / "Publishing/package.json").write_text(json.dumps({"internal_source": {"run": str(run), "recording_id": "x"}}))
            self.assertEqual(rl.run_media(pkg), [])


if __name__ == "__main__":
    unittest.main()
