"""Integrity and environment validation for external qualified runtime assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from .constants import (
    CHECKPOINT_SHA256,
    EXPECTED_MODEL_PARAMETERS,
    LIVE_M_HISTORY,
    LIVE_N_REQUIRED,
    LIVE_SCORE_THRESHOLD,
    LIVE_STRIDE_FEATURE_STEPS,
    MODEL_EXPERIMENT_ID,
    MODEL_VERSION_ID,
)


DEFAULT_MANIFEST = Path(__file__).resolve().parents[1] / "qualified_runtime_assets.json"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _under_root(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Asset path escapes the configured root: {relative}") from exc
    return candidate


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "1":
        raise ValueError("Unsupported qualified-runtime manifest schema.")
    return payload


def validate_frozen_contract(manifest: dict[str, Any]) -> list[str]:
    q = manifest.get("qualification", {})
    policy = q.get("policy", {})
    expected = {
        "experiment_id": MODEL_EXPERIMENT_ID,
        "model_version_id": MODEL_VERSION_ID,
        "checkpoint_sha256": CHECKPOINT_SHA256,
        "parameter_count": EXPECTED_MODEL_PARAMETERS,
    }
    errors = [
        f"qualification.{key} does not match the runtime constant"
        for key, value in expected.items()
        if q.get(key) != value
    ]
    policy_expected = {
        "stride_feature_steps": LIVE_STRIDE_FEATURE_STEPS,
        "score_threshold": LIVE_SCORE_THRESHOLD,
        "positive_windows_required": LIVE_N_REQUIRED,
        "history_windows": LIVE_M_HISTORY,
    }
    errors.extend(
        f"qualification.policy.{key} does not match the runtime constant"
        for key, value in policy_expected.items()
        if policy.get(key) != value
    )
    if q.get("input_shape") != ["T", 5, 2048]:
        errors.append("qualification.input_shape must be [T,5,2048]")
    if q.get("sequence_length") != 64:
        errors.append("qualification.sequence_length must be 64")
    return errors


def validate_files(
    root: Path, manifest: dict[str, Any], *, include_media: bool
) -> list[str]:
    errors: list[str] = []
    entries = list(manifest.get("files", []))
    if include_media:
        entries.extend(manifest.get("media", []))
    for entry in entries:
        relative = entry["path"]
        try:
            path = _under_root(root, relative)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not path.is_file():
            errors.append(f"missing {entry['role']}: {path}")
            continue
        actual_size = path.stat().st_size
        if actual_size != entry["size"]:
            errors.append(
                f"size mismatch for {entry['role']}: expected {entry['size']}, "
                f"got {actual_size}"
            )
            continue
        actual_hash = _sha256(path)
        if actual_hash != entry["sha256"]:
            errors.append(
                f"SHA256 mismatch for {entry['role']}: expected "
                f"{entry['sha256']}, got {actual_hash}"
            )
    return errors


def validate_repositories(root: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for entry in manifest.get("repositories", []):
        repo = _under_root(root, entry["path"])
        if not (repo / ".git").exists():
            errors.append(f"source repository metadata missing: {repo}")
            continue
        completed = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
        )
        actual = completed.stdout.strip().lower()
        if completed.returncode != 0 or actual != entry["commit"]:
            errors.append(
                f"source revision mismatch for {repo}: expected {entry['commit']}, "
                f"got {actual or completed.stderr.strip()}"
            )
        remote = subprocess.run(
            ["git", "-C", str(repo), "config", "--get", "remote.origin.url"],
            check=False,
            capture_output=True,
            text=True,
        )
        actual_url = remote.stdout.strip().rstrip("/")
        expected_url = entry["url"].rstrip("/")
        if remote.returncode != 0 or actual_url != expected_url:
            errors.append(
                f"source origin mismatch for {repo}: expected {expected_url}, "
                f"got {actual_url or remote.stderr.strip()}"
            )
    return errors


def _probe_environment(python: Path, package_names: list[str]) -> dict[str, Any]:
    probe = (
        "import importlib.metadata as m,json,platform;"
        f"names={package_names!r};"
        "packages={n:m.version(n) for n in names};"
        "import torch;"
        "print(json.dumps({'python_version':platform.python_version(),"
        "'packages':packages,'cuda_available':torch.cuda.is_available(),"
        "'cuda_runtime':torch.version.cuda}))"
    )
    completed = subprocess.run(
        [str(python), "-c", probe],
        check=False,
        capture_output=True,
        text=True,
        timeout=90,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "environment probe failed")
    return json.loads(completed.stdout.strip())


def validate_environment(
    label: str, python: Path, expected: dict[str, Any]
) -> list[str]:
    if not python.is_file():
        return [f"{label} Python is missing: {python}"]
    try:
        actual = _probe_environment(python, list(expected["packages"]))
    except (OSError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        return [f"{label} environment probe failed: {exc}"]
    errors: list[str] = []
    if actual["python_version"] != expected["python_version"]:
        errors.append(
            f"{label} Python mismatch: expected {expected['python_version']}, "
            f"got {actual['python_version']}"
        )
    for package, version in expected["packages"].items():
        if actual["packages"].get(package) != version:
            errors.append(
                f"{label} package mismatch for {package}: expected {version}, "
                f"got {actual['packages'].get(package)}"
            )
    if expected.get("cuda_required") and not actual["cuda_available"]:
        errors.append(f"{label} environment cannot access CUDA")
    if str(actual.get("cuda_runtime")) != expected.get("cuda_runtime"):
        errors.append(
            f"{label} CUDA runtime mismatch: expected {expected.get('cuda_runtime')}, "
            f"got {actual.get('cuda_runtime')}"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--temporal-python", type=Path)
    parser.add_argument("--skip-media", action="store_true")
    parser.add_argument("--skip-environments", action="store_true")
    args = parser.parse_args()

    raw_root = args.root or os.environ.get("SENTINEL_VIOLENCE_ROOT")
    if raw_root is None:
        parser.error("provide --root or set SENTINEL_VIOLENCE_ROOT")
    root = Path(raw_root).expanduser().resolve()
    manifest = load_manifest(args.manifest.resolve())

    errors = validate_frozen_contract(manifest)
    errors.extend(validate_files(root, manifest, include_media=not args.skip_media))
    errors.extend(validate_repositories(root, manifest))

    if not args.skip_environments:
        environments = manifest["environments"]
        extractor_python = _under_root(root, environments["extractor"]["python_path"])
        errors.extend(
            validate_environment("extractor", extractor_python, environments["extractor"])
        )
        temporal_raw = args.temporal_python or os.environ.get("SENTINEL_AI_PYTHON")
        if temporal_raw is None:
            errors.append(
                "temporal Python is not configured; provide --temporal-python or set "
                "SENTINEL_AI_PYTHON"
            )
        else:
            errors.extend(
                validate_environment(
                    "temporal", Path(temporal_raw).expanduser().resolve(), environments["temporal"]
                )
            )

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(
        "PASS: qualified runtime assets, source revisions, frozen policy, "
        "media, and environments match the recorded manifest."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
