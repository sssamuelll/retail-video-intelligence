import os
import unittest
from unittest.mock import patch

from retail_video_intelligence.config import Settings


class SettingsTest(unittest.TestCase):
    def test_defaults_are_valid(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings.from_env()
        self.assertEqual(settings.retention_days, 30)

    def test_invalid_retention_is_rejected(self) -> None:
        with patch.dict(os.environ, {"RVI_RETENTION_DAYS": "0"}, clear=True):
            with self.assertRaises(ValueError):
                Settings.from_env()
