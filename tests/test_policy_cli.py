import unittest

from retail_video_intelligence.cli import smoke
from retail_video_intelligence.policy import PROHIBITED_CAPABILITIES, assert_capability_allowed


class PolicyAndSmokeTest(unittest.TestCase):
    def test_all_required_guardrails_exist(self) -> None:
        self.assertEqual(
            PROHIBITED_CAPABILITIES,
            {
                "emotion_inference",
                "facial_recognition",
                "license_plate_recognition",
                "persistent_reidentification",
            },
        )

    def test_prohibited_capability_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            assert_capability_allowed("facial_recognition")

    def test_smoke_has_no_external_side_effects(self) -> None:
        result = smoke()
        self.assertEqual(result["status"], "ok")
        self.assertFalse(result["network_used"])
        self.assertFalse(result["models_loaded"])
