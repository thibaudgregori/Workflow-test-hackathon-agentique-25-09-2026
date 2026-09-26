"""Regression checks for source binding and the publish-before-write boundary."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from description_policy import validate_captions
import publish_short


class DescriptionPolicyTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pkg = Path(self.temp.name)
        self.source = self.pkg / "transcript.json"
        self.source.write_text(json.dumps({"text": "Change the reasoning level. Higher levels consume more tokens."}))
        self.caps = {
            "description_strategy": {
                "version": "2026-09-08", "content_type": "tutorial",
                "description_length": "concise", "reason": "One action with a cost caveat.",
                "resource_review": "No promised resources.", "transcript_path": "transcript.json",
                "transcript_sha256": hashlib.sha256(self.source.read_bytes()).hexdigest(),
                "evidence": ["Change the reasoning level."],
            },
            "youtube": {"description": "Change the reasoning level. Higher levels cost more tokens.\n#AITips"},
            "tiktok": {"caption": "Try another reasoning level; higher levels use more tokens."},
            "instagram": {"caption": "Change the reasoning level. Remember the token tradeoff."},
        }

    def test_single_action_tutorial_can_stay_concise(self):
        self.assertEqual(validate_captions(self.caps, self.pkg)["description_length"], "concise")

    def test_detailed_tutorial_and_concise_news_or_explainer(self):
        for kind, length in [("tutorial", "detailed"), ("news", "concise"), ("explainer", "concise")]:
            with self.subTest(kind=kind):
                caps = copy.deepcopy(self.caps)
                caps["description_strategy"].update(content_type=kind, description_length=length)
                self.assertEqual(validate_captions(caps, self.pkg)["content_type"], kind)

    def test_news_cannot_take_detailed_template(self):
        self.caps["description_strategy"].update(content_type="news", description_length="detailed")
        with self.assertRaisesRegex(ValueError, "Only tutorials"):
            validate_captions(self.caps, self.pkg)

    def test_legacy_copy_requires_review(self):
        del self.caps["description_strategy"]
        with self.assertRaisesRegex(ValueError, "Review and regenerate"):
            validate_captions(self.caps, self.pkg)

    def test_changed_transcript_rejects_stale_review(self):
        self.source.write_text(json.dumps({"text": "A different final take."}))
        with self.assertRaisesRegex(ValueError, "Transcript changed"):
            validate_captions(self.caps, self.pkg)

    def test_evidence_from_another_recording_rejected(self):
        self.caps["description_strategy"]["evidence"] = ["The tool launched today."]
        with self.assertRaisesRegex(ValueError, "not present"):
            validate_captions(self.caps, self.pkg)

    def test_youtube_limits_preserve_original_text(self):
        for content, error in [("x" * 5001, "5,000"), ("Copy #One #Two #Three #Four", "three topical")]:
            with self.subTest(error=error):
                self.caps["youtube"]["description"] = content
                with self.assertRaisesRegex(ValueError, error):
                    validate_captions(self.caps, self.pkg)
                self.assertEqual(self.caps["youtube"]["description"], content)

    def test_url_fragment_is_not_a_hashtag(self):
        self.caps["youtube"]["description"] = "Reference: https://www.genial-agency.com/en#book\n#One #Two #Three"
        validate_captions(self.caps, self.pkg)

    def test_pending_platforms_only(self):
        del self.caps["youtube"]
        validate_captions(self.caps, self.pkg, ["tiktok", "instagram"])

    def write_package(self):
        publishing = self.pkg / "Publishing"
        publishing.mkdir()
        (publishing / "captions.json").write_text(json.dumps(self.caps))
        (publishing / "status.json").write_text(json.dumps({"platforms": {p: {} for p in publish_short.ORDER}}))

    def test_publisher_rejects_bad_copy_before_any_upload(self):
        self.caps["instagram"]["caption"] = ""
        self.write_package()
        with patch("sys.argv", ["publish_short.py", "--package", str(self.pkg), "--now", "--write"]), \
             patch.object(publish_short, "publish_youtube") as youtube, \
             patch.object(publish_short, "upload_media") as media, \
             patch.object(publish_short.requests, "post") as post:
            with self.assertRaisesRegex(SystemExit, "instagram.caption"):
                publish_short.main()
            youtube.assert_not_called()
            media.assert_not_called()
            post.assert_not_called()

    def test_publisher_validates_and_passes_exact_copy_to_dry_run(self):
        self.write_package()
        with patch("sys.argv", ["publish_short.py", "--package", str(self.pkg), "--now", "--platforms", "youtube"]), \
             patch.object(publish_short, "latest_thumbnails", return_value=self.pkg), \
             patch.object(publish_short, "publish_youtube", return_value=None) as youtube:
            publish_short.main()
            self.assertEqual(youtube.call_args.args[1]["youtube"], self.caps["youtube"])
            self.assertFalse(youtube.call_args.args[4].write)


if __name__ == "__main__":
    unittest.main()
