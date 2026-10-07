"""Portable filesystem configuration for the frozen violence runtime.

Model identity/checksums remain frozen. Only machine-specific locations are
externalized so the same repository can run on different workstations.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from .constants import (
    CHECKPOINT_RELATIVE,
    EXACT_EXTRACTOR_ENV_RELATIVE,
    EXACT_EXTRACTOR_WORKER_RELATIVE,
    TRAIN_SCRIPT_RELATIVE,
)


ENV_PROJECT_ROOT = "SENTINEL_VIOLENCE_ROOT"
ENV_CHECKPOINT = "SENTINEL_TEMPORAL_CHECKPOINT"
ENV_TRAIN_SCRIPT = "SENTINEL_TEMPORAL_TRAIN_SCRIPT"
ENV_EXTRACTOR_PYTHON = "SENTINEL_EXTRACTOR_PYTHON"
ENV_EXTRACTOR_WORKER = "SENTINEL_EXTRACTOR_WORKER"
ENV_WORK_DIR = "SENTINEL_RUNTIME_WORK_DIR"


@dataclass(frozen=True)
class RuntimePaths:
    project_root: Path
    checkpoint: Path
    training_script: Path
    extractor_python: Path
    extractor_worker: Path
    work_dir: Path


def _clean_env_value(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _resolve(root: Path, value: str | Path) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def resolve_project_root(explicit_root: Path | str | None = None) -> Path:
    raw = explicit_root if explicit_root is not None else _clean_env_value(
        os.environ.get(ENV_PROJECT_ROOT)
    )
    if raw is None:
        raise ValueError(
            "XD-Violence workspace root is not configured. Provide --root or set "
            f"{ENV_PROJECT_ROOT}."
        )
    return Path(raw).expanduser().resolve()


def _default_extractor_python(root: Path) -> Path:
    env_root = root / EXACT_EXTRACTOR_ENV_RELATIVE
    if os.name == "nt":
        return (env_root / "Scripts" / "python.exe").resolve()
    return (env_root / "bin" / "python").resolve()


def resolve_runtime_paths(
    project_root: Path | str,
    *,
    work_dir: Path | str | None = None,
) -> RuntimePaths:
    root = Path(project_root).expanduser().resolve()

    checkpoint_override = _clean_env_value(os.environ.get(ENV_CHECKPOINT))
    training_override = _clean_env_value(os.environ.get(ENV_TRAIN_SCRIPT))
    extractor_python_override = _clean_env_value(os.environ.get(ENV_EXTRACTOR_PYTHON))
    extractor_worker_override = _clean_env_value(os.environ.get(ENV_EXTRACTOR_WORKER))
    work_override = _clean_env_value(os.environ.get(ENV_WORK_DIR))

    resolved_work_dir = (
        _resolve(root, work_dir)
        if work_dir is not None
        else _resolve(root, work_override)
        if work_override is not None
        else (root / "sentinel_runtime_validation" / "runtime_work").resolve()
    )

    return RuntimePaths(
        project_root=root,
        checkpoint=(
            _resolve(root, checkpoint_override)
            if checkpoint_override is not None
            else (root / CHECKPOINT_RELATIVE).resolve()
        ),
        training_script=(
            _resolve(root, training_override)
            if training_override is not None
            else (root / TRAIN_SCRIPT_RELATIVE).resolve()
        ),
        extractor_python=(
            _resolve(root, extractor_python_override)
            if extractor_python_override is not None
            else _default_extractor_python(root)
        ),
        extractor_worker=(
            _resolve(root, extractor_worker_override)
            if extractor_worker_override is not None
            else (root / EXACT_EXTRACTOR_WORKER_RELATIVE).resolve()
        ),
        work_dir=resolved_work_dir,
    )
