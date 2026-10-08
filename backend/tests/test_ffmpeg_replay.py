from __future__ import annotations

import unittest
from pathlib import Path

from app.demo.clip_catalog import DemoClip
from app.demo.ffmpeg_replay import FFmpegReplayAdapter


class FFmpegReplayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clip = DemoClip(
            clip_id="approved-demo",
            display_name="Approved demo",
            relative_path="clips/demo.mp4",
            resolved_path=Path("/approved-media/clips/demo.mp4"),
        )
        self.adapter = FFmpegReplayAdapter("ffmpeg")

    def test_command_uses_natural_rate_and_jpeg_pipe(self) -> None:
        command = self.adapter._build_command(self.clip)
        self.assertIn("-re", command)
        self.assertIn("image2pipe", command)
        self.assertIn("mjpeg", command)
        self.assertEqual(command[-1], "pipe:1")
        self.assertIn(str(self.clip.resolved_path), command)

    def test_jpeg_extractor_handles_partial_and_concatenated_frames(self) -> None:
        buffer = bytearray(b"noise\xff\xd8first")
        self.assertEqual(self.adapter._extract_jpeg_frames(buffer), [])
        buffer.extend(b"\xff\xd9\xff\xd8second\xff\xd9tail")
        frames = self.adapter._extract_jpeg_frames(buffer)
        self.assertEqual(frames, [b"\xff\xd8first\xff\xd9", b"\xff\xd8second\xff\xd9"])
        self.assertEqual(buffer, bytearray(b"l"))

    def test_oversized_unterminated_frame_is_rejected(self) -> None:
        from app.demo.ffmpeg_replay import MAX_JPEG_FRAME_BYTES

        with self.assertRaises(ValueError):
            self.adapter._extract_jpeg_frames(
                bytearray(b"\xff\xd8" + b"x" * (MAX_JPEG_FRAME_BYTES + 1))
            )


if __name__ == "__main__":
    unittest.main()
