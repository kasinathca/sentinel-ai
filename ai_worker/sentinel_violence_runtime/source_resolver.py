"""Trusted opaque-reference -> local-file resolver.

The request contract carries source_locator_ref, not an arbitrary filesystem
path. This adapter loads an operator-controlled map file.
"""

from __future__ import annotations

import json
from pathlib import Path

from .errors import InvalidRequestError, UnsupportedInputError


class MappingSourceResolver:
    def __init__(self, mapping: dict[str, str], *, mapping_base: Path | None = None):
        if not isinstance(mapping, dict):
            raise InvalidRequestError("Source mapping must be an object.")

        self._base = mapping_base.resolve() if mapping_base else None
        self._mapping: dict[str, str] = {}

        for key, value in mapping.items():
            if not isinstance(key, str) or not key.strip():
                raise InvalidRequestError("Source-map keys must be non-empty strings.")
            if not isinstance(value, str) or not value.strip():
                raise InvalidRequestError(
                    f"Source-map value for {key!r} must be a non-empty path string."
                )
            self._mapping[key.strip()] = value.strip()

    @classmethod
    def from_json_file(cls, path: Path) -> "MappingSourceResolver":
        path = path.resolve()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(path)

        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(data, mapping_base=path.parent)

    def resolve(self, source_locator_ref: str) -> Path:
        if source_locator_ref not in self._mapping:
            raise UnsupportedInputError(
                f"Unknown controlled source_locator_ref {source_locator_ref!r}."
            )

        raw = Path(self._mapping[source_locator_ref])
        if not raw.is_absolute():
            if self._base is None:
                raise InvalidRequestError(
                    "Relative source path requires a mapping_base."
                )
            raw = self._base / raw

        resolved = raw.resolve()

        if not resolved.exists() or not resolved.is_file():
            raise UnsupportedInputError(
                f"Configured source for {source_locator_ref!r} is unavailable."
            )

        return resolved
