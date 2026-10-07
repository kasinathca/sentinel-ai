"""Load registered demo clips without accepting browser-supplied paths.

The manifest is local operator configuration beneath SENTINEL_DEMO_MEDIA_ROOT.
Resolved paths stay internal to this module; callers should expose only the
opaque clip ID and display name.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


DEMO_MEDIA_ROOT_ENV = "SENTINEL_DEMO_MEDIA_ROOT"
MANIFEST_NAME = "manifest.json"
SUPPORTED_MANIFEST_SCHEMA = "1"


class DemoCatalogError(ValueError):
    """Safe configuration or lookup failure for the local demo catalog."""


class DemoClipNotFound(DemoCatalogError):
    """The requested opaque clip ID is not registered."""


@dataclass(frozen=True)
class DemoClip:
    clip_id: str
    display_name: str
    relative_path: str
    resolved_path: Path

    def to_public_dict(self) -> dict[str, str]:
        """Return the public catalog contract without local path information."""
        return {"clip_id": self.clip_id, "display_name": self.display_name}


class DemoClipCatalog:
    """Resolve registered clip IDs beneath a machine-local media root."""

    def __init__(self, media_root: Path | str):
        self._media_root = Path(media_root).expanduser()

    @classmethod
    def from_environment(cls) -> "DemoClipCatalog":
        configured_root = os.environ.get(DEMO_MEDIA_ROOT_ENV, "").strip()
        if not configured_root:
            raise DemoCatalogError(
                f"Demo media is not configured; set {DEMO_MEDIA_ROOT_ENV}."
            )
        return cls(configured_root)

    def list_clips(self) -> list[DemoClip]:
        """Load and validate the complete server-controlled clip manifest."""
        root = self._resolve_root()
        payload = self._read_manifest(root)
        raw_clips = payload.get("clips")
        if not isinstance(raw_clips, list):
            raise DemoCatalogError("Demo manifest clips must be a list.")

        clips: list[DemoClip] = []
        seen_ids: set[str] = set()
        for index, raw_clip in enumerate(raw_clips):
            if not isinstance(raw_clip, dict):
                raise DemoCatalogError(f"Demo manifest clip {index} must be an object.")
            clip_id = self._required_text(raw_clip, "clip_id", index)
            display_name = self._required_text(raw_clip, "display_name", index)
            relative_path = self._required_text(raw_clip, "relative_path", index)
            if clip_id in seen_ids:
                raise DemoCatalogError("Demo manifest contains duplicate clip IDs.")
            seen_ids.add(clip_id)
            resolved_path = self._resolve_registered_path(root, relative_path)
            clips.append(
                DemoClip(
                    clip_id=clip_id,
                    display_name=display_name,
                    relative_path=relative_path,
                    resolved_path=resolved_path,
                )
            )
        return clips

    def get_clip(self, clip_id: str) -> DemoClip:
        if not isinstance(clip_id, str) or not clip_id.strip():
            raise DemoClipNotFound("Unknown demo clip ID.")
        for clip in self.list_clips():
            if clip.clip_id == clip_id:
                return clip
        raise DemoClipNotFound("Unknown demo clip ID.")

    def _resolve_root(self) -> Path:
        if not self._media_root.is_absolute():
            raise DemoCatalogError("Configured demo media root must be absolute.")
        try:
            root = self._media_root.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise DemoCatalogError("Configured demo media root is unavailable.") from exc
        if not root.is_dir():
            raise DemoCatalogError("Configured demo media root is not a directory.")
        return root

    @staticmethod
    def _read_manifest(root: Path) -> dict[str, Any]:
        manifest_path = root / MANIFEST_NAME
        try:
            manifest_path = manifest_path.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise DemoCatalogError("Demo manifest is missing or unavailable.") from exc
        try:
            manifest_path.relative_to(root)
        except ValueError as exc:
            raise DemoCatalogError("Demo manifest path escapes the media root.") from exc
        if not manifest_path.is_file():
            raise DemoCatalogError("Demo manifest is not a file.")
        try:
            raw_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise DemoCatalogError("Demo manifest could not be read.") from exc
        if not isinstance(raw_payload, dict):
            raise DemoCatalogError("Demo manifest must be an object.")
        if raw_payload.get("schema_version") != SUPPORTED_MANIFEST_SCHEMA:
            raise DemoCatalogError("Demo manifest schema version is unsupported.")
        return raw_payload

    @staticmethod
    def _required_text(clip: dict[str, Any], field: str, index: int) -> str:
        value = clip.get(field)
        if not isinstance(value, str) or not value.strip():
            raise DemoCatalogError(
                f"Demo manifest clip {index} requires a non-empty {field}."
            )
        return value.strip()

    @staticmethod
    def _resolve_registered_path(root: Path, relative_path: str) -> Path:
        # Parse both separator styles so a Windows path cannot bypass checks
        # when the backend happens to run on a POSIX host (or vice versa).
        windows_path = PureWindowsPath(relative_path)
        posix_path = PurePosixPath(relative_path.replace("\\", "/"))
        if windows_path.is_absolute() or windows_path.drive or posix_path.is_absolute():
            raise DemoCatalogError("Registered demo clip path must be relative.")
        if any(part in {"", ".", ".."} for part in posix_path.parts):
            raise DemoCatalogError("Registered demo clip path is invalid.")

        try:
            resolved_path = root.joinpath(*posix_path.parts).resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise DemoCatalogError("Registered demo clip file is unavailable.") from exc
        try:
            resolved_path.relative_to(root)
        except ValueError as exc:
            raise DemoCatalogError("Registered demo clip path escapes the media root.") from exc
        if not resolved_path.is_file():
            raise DemoCatalogError("Registered demo clip is not a file.")
        return resolved_path
