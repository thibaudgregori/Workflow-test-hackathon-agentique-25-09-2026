"""Files copied verbatim into a Modal image must stay self-contained (2026-09-21).

The consolidation of 2026-09-20 made pipeline/sam2/ship.py import the shared media.py. ship.py is
baked into shorts-factory-matting as /opt/finish/ship.py and the client refuses a finish whose
ship_source_sha256 differs from the local file, so run 23's first two mattes failed with
"Deployed finishing source differs" and a redeploy was needed. A baked file may import only the
standard library and third-party packages, never a sibling module from pipeline/.
"""
import re, unittest
from pathlib import Path

PIPE = Path(__file__).resolve().parents[1]
BAKED = ["sam2/ship.py", "sam2/post.py", "matting/worker.py"]
SIBLINGS = ("media", "fsutil", "paths", "runs", "selection", "client")


class BakedSources(unittest.TestCase):
    def test_baked_files_import_no_pipeline_sibling(self):
        bad = []
        for rel in BAKED:
            for i, line in enumerate((PIPE / rel).read_text().splitlines(), 1):
                if re.match(r"\s*(from|import)\s+(" + "|".join(SIBLINGS) + r")\b", line):
                    bad.append(f"{rel}:{i}: {line.strip()}")
        self.assertEqual(bad, [], "baked-into-image files must stay self-contained:\n" + "\n".join(bad))


if __name__ == "__main__":
    unittest.main()
