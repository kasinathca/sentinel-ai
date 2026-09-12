"""RFC3339/UTC and file-window timestamp helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .errors import InvalidRequestError


def parse_utc_timestamp(value: str) -> datetime:
    """Parse an RFC3339-ish timestamp and normalize it to timezone-aware UTC."""
    if not isinstance(value, str) or not value.strip():
        raise InvalidRequestError("Timestamp must be a non-empty string.")

    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(text)
    except ValueError as exc:
        raise InvalidRequestError(
            f"Invalid timestamp {value!r}; RFC3339/ISO-8601 expected."
        ) from exc

    if dt.tzinfo is None:
        raise InvalidRequestError(
            f"Timestamp {value!r} must contain an explicit timezone."
        )

    return dt.astimezone(timezone.utc)


def format_utc_timestamp(dt: datetime) -> str:
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware.")

    utc = dt.astimezone(timezone.utc)

    # Round to the nearest millisecond rather than relying on
    # datetime.isoformat(timespec="milliseconds"), which truncates.
    rounded = utc + timedelta(microseconds=500)
    rounded = rounded.replace(
        microsecond=(rounded.microsecond // 1000) * 1000
    )

    return rounded.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def feature_window_timestamps(
    *,
    source_started_at: datetime,
    feature_index: int,
    fps: float,
    duration_seconds: float | None,
    source_frames_per_feature_step: int,
) -> tuple[str, str]:
    if feature_index < 0:
        raise ValueError("feature_index must be >= 0")
    if fps <= 0:
        raise ValueError("fps must be > 0")
    if source_frames_per_feature_step <= 0:
        raise ValueError("source_frames_per_feature_step must be > 0")

    start_offset = (feature_index * source_frames_per_feature_step) / fps
    end_offset = ((feature_index + 1) * source_frames_per_feature_step) / fps

    if duration_seconds is not None:
        if duration_seconds <= 0:
            raise ValueError("duration_seconds must be > 0 when supplied")
        end_offset = min(end_offset, duration_seconds)

    if end_offset < start_offset:
        end_offset = start_offset

    started = source_started_at + timedelta(seconds=start_offset)
    ended = source_started_at + timedelta(seconds=end_offset)

    return format_utc_timestamp(started), format_utc_timestamp(ended)
