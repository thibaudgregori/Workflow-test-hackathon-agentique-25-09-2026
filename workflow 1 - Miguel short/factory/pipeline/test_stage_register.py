"""STAGES.md is the map: every workflow phase and every agent label prefix in
daily-shorts.js must have a row there, and the numbering must stay 1..N."""
import re, unittest
from pathlib import Path
F = Path(__file__).resolve().parents[1]
WF = F.parents[3] / '.claude/workflows/daily-shorts.js'


class StageRegisterTest(unittest.TestCase):
    def setUp(self):
        self.reg = (F / 'STAGES.md').read_text()
        self.wf = WF.read_text()
        rows = [l for l in self.reg.splitlines() if re.match(r'^\| \d+ \|', l)]
        self.numbers = [int(l.split('|')[1]) for l in rows]
        self.labels_col = ' '.join(l.split('|')[8] for l in rows)

    def test_numbering_is_contiguous_from_one(self):
        self.assertEqual(self.numbers, list(range(1, len(self.numbers) + 1)))

    def test_every_workflow_phase_is_in_the_register(self):
        phases = set(re.findall(r"title: '([^']+)'", self.wf.split('phases:')[1].split(']')[0]))
        for ph in phases:
            self.assertIn(f'**{ph}**', self.reg, ph)

    def test_every_agent_label_prefix_has_a_row(self):
        prefixes = set(re.findall(r"label:\s*'([a-z_]+):", self.wf)) | set(re.findall(r"label:\s*([a-z_]+)\s*\+\s*':'", self.wf))
        prefixes -= {'fmt'}   # the lane label is `fmt + ':' + id`; fmt is split | whiteboard | cutout, each checked by name
        for p in prefixes:
            self.assertIn(p, self.labels_col, f'agent label prefix {p!r} has no register row')


if __name__ == '__main__':
    unittest.main()
