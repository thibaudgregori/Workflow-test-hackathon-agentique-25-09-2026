"""The watcher reads THIS run's tight transcript, never another run's (run 16 audit:
a newer run's render was watched against an older run's transcript because the old
lookup globbed every run and took the lexically last path)."""
import tempfile, unittest
from pathlib import Path
from clerk_video_gemini import resolve_transcript


class RunBoundTranscriptTest(unittest.TestCase):
    def setUp(self):
        td = tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        self.tmp = Path(td.name).resolve()
        for run in ("shorts_run998", "shorts_run999"):
            d = self.tmp / run / "cuts" / "minimaxh3"; d.mkdir(parents=True)
            (d / "transcript_tight.json").write_text('{"run": "%s"}' % run)
        (self.tmp / "shorts_run999" / "output").mkdir()
        self.render = self.tmp / "shorts_run999" / "output" / "minimaxh3_cutout.mp4"; self.render.write_bytes(b"x")

    def test_render_in_run16_resolves_run16_not_lexically_last(self):
        p = resolve_transcript(self.render, "minimaxh3", None, factory=self.tmp)
        self.assertEqual(p, self.tmp / "shorts_run999" / "cuts" / "minimaxh3" / "transcript_tight.json")
        self.assertIn("shorts_run999", p.read_text())

    def test_explicit_wins_and_must_exist(self):
        explicit = self.tmp / "shorts_run998" / "cuts" / "minimaxh3" / "transcript_tight.json"
        self.assertEqual(resolve_transcript(self.render, "minimaxh3", explicit, factory=self.tmp), explicit)
        with self.assertRaises(SystemExit):
            resolve_transcript(self.render, "minimaxh3", self.tmp / "missing.json", factory=self.tmp)

    def test_no_cross_run_fallback(self):
        (self.tmp / "shorts_run999" / "cuts" / "minimaxh3" / "transcript_tight.json").unlink()
        with self.assertRaises(SystemExit):
            resolve_transcript(self.render, "minimaxh3", None, factory=self.tmp)


if __name__ == "__main__":
    unittest.main()
