"""Read-only media timing probe used by the file-source development adapter."""

from __future__ import annotations

from dataclasses import dataclass
import json
import subprocess
from pathlib import Path

from .errors import VideoDecodeError


@dataclass(frozen=True)
class MediaInfo:
    fps: float
    duration_seconds: float | None
    frame_count: int | None


def _parse_fraction(value: str) -> float:
    if "/" in value:
        left, right = value.split("/", 1)
        denominator = float(right)
        if denominator == 0:
            raise ValueError("zero denominator")
        return float(left) / denominator
    return float(value)


def probe_media(path: Path, ffprobe: str = "ffprobe") -> MediaInfo:
    command = [
        ffprobe,
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=avg_frame_rate,r_frame_rate,nb_frames,duration:format=duration",
        "-of",
        "json",
        str(path),
    ]

    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError as exc:
        raise VideoDecodeError(
            "ffprobe is not available on PATH; media timing cannot be determined."
        ) from exc
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise VideoDecodeError("ffprobe could not read the video source.") from exc

    try:
        payload = json.loads(completed.stdout)
        streams = payload.get("streams") or []
        if not streams:
            raise ValueError("no video stream")
        stream = streams[0]

        fps_value = stream.get("avg_frame_rate") or stream.get("r_frame_rate")
        fps = _parse_fraction(str(fps_value))
        if fps <= 0:
            raise ValueError("non-positive fps")

        duration_raw = stream.get("duration")
        if duration_raw in (None, "N/A"):
            duration_raw = (payload.get("format") or {}).get("duration")

        duration = None
        if duration_raw not in (None, "N/A"):
            duration = float(duration_raw)
            if duration <= 0:
                duration = None

        frames_raw = stream.get("nb_frames")
        frame_count = None
        if frames_raw not in (None, "N/A"):
            frame_count = int(frames_raw)
            if frame_count < 1:
                frame_count = None

        return MediaInfo(
            fps=float(fps),
            duration_seconds=duration,
            frame_count=frame_count,
        )
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        raise VideoDecodeError(
            "ffprobe returned media metadata that could not be interpreted."
        ) from exc
