from __future__ import annotations

from datetime import datetime, timezone
import unittest

from sentinel_violence_runtime.time_utils import (
    feature_window_timestamps,
    parse_utc_timestamp,
)


class TimeUtilsTests(unittest.TestCase):
    def test_parse_requires_timezone(self):
        with self.assertRaises(Exception):
            parse_utc_timestamp("2026-09-12T07:00:00")

    def test_24fps_first_feature_window(self):
        start = datetime(2026, 9, 12, 7, 0, 0, tzinfo=timezone.utc)
        a, b = feature_window_timestamps(
            source_started_at=start,
            feature_index=0,
            fps=24.0,
            duration_seconds=10.0,
            source_frames_per_feature_step=64,
        )
        self.assertEqual(a, "2026-09-12T07:00:00.000Z")
        self.assertEqual(b, "2026-09-12T07:00:02.667Z")

    def test_last_window_is_clamped_to_file_duration(self):
        start = datetime(2026, 9, 12, 7, 0, 0, tzinfo=timezone.utc)
        a, b = feature_window_timestamps(
            source_started_at=start,
            feature_index=1,
            fps=24.0,
            duration_seconds=3.0,
            source_frames_per_feature_step=64,
        )
        self.assertEqual(a, "2026-09-12T07:00:02.667Z")
        self.assertEqual(b, "2026-09-12T07:00:03.000Z")

    def test_rounding_can_roll_into_next_second(self):
        from sentinel_violence_runtime.time_utils import format_utc_timestamp
        dt = datetime(
            2026, 9, 12, 7, 0, 0, 999800, tzinfo=timezone.utc
        )
        self.assertEqual(
            format_utc_timestamp(dt),
            "2026-09-12T07:00:01.000Z",
        )


if __name__ == "__main__":
    unittest.main()
