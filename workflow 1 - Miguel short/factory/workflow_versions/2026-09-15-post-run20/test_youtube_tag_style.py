#!/usr/bin/env python3
"""Tag casing regressions.

2026-09-15: `canonicalize_tag` upper-cased the unit on a number, turning the tag
"1080p AI Video" into "1080P AI Video". Two finished Shorts were refused at the
publish gate over it, and the mangled form was written into their captions
before the cause was found. A resolution, frame rate or parameter count is
written one way in the world; Title Case does not apply to it.
"""
import sys, pathlib, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from youtube_tag_style import canonicalize_tag, validate_tag_casing


class UnitsKeepTheirOwnCase(unittest.TestCase):
    def t(self, tag, want):
        self.assertEqual(canonicalize_tag(tag), want)

    def test_resolutions(self):
        self.t("1080p AI Video", "1080p AI Video")
        self.t("720P footage", "720p Footage")
        self.t("4k video", "4K Video")
        self.t("8K Video", "8K Video")

    def test_rates_and_sizes(self):
        self.t("60fps render", "60fps Render")
        self.t("7b model", "7B Model")
        self.t("100ms latency", "100ms Latency")

    def test_canonical_tags_are_left_alone(self):
        for tag in ("1080p AI Video", "AI Video Generation", "Grok Imagine",
                    "Native HD Video", "n8n and OpenAI", "3D Models"):
            self.t(tag, tag)

    def test_validate_accepts_a_real_shorts_tag_set(self):
        tags = ["Grok Imagine", "Grok", "1080p AI Video", "AI Video Generation",
                "Native HD Video", "AI Video Models", "AI News", "Generative AI"]
        self.assertEqual(validate_tag_casing(tags), tags)

    def test_validate_still_catches_real_mistakes(self):
        with self.assertRaises(ValueError):
            validate_tag_casing(["ai news"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
