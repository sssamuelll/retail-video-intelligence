import unittest
from datetime import UTC, datetime, timedelta

from retail_video_intelligence.domain import BoundingBox, RecordingRef


class DomainTest(unittest.TestCase):
    def test_valid_recording_reference(self) -> None:
        start = datetime.now(UTC)
        recording = RecordingRef(
            "camera-1", "file:///recording.mp4", start, start + timedelta(seconds=1)
        )
        self.assertEqual(recording.camera_id, "camera-1")

    def test_invalid_box_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            BoundingBox(0.8, 0.1, 0.2, 0.9)
