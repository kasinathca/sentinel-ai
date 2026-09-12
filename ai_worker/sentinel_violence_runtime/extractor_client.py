"""Persistent client for the already-qualified exact I3D extractor subprocess."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any, TextIO

from .errors import InferenceError, ModelLoadError


class PersistentExactExtractor:
    def __init__(
        self,
        *,
        python_exe: Path,
        worker_script: Path,
        project_root: Path,
        stderr_log: Path,
    ) -> None:
        self.python_exe = python_exe.resolve()
        self.worker_script = worker_script.resolve()
        self.project_root = project_root.resolve()
        self.stderr_log = stderr_log.resolve()

        self._proc: subprocess.Popen[str] | None = None
        self._stderr_handle: TextIO | None = None
        self.ready_payload: dict[str, Any] | None = None

    @property
    def is_ready(self) -> bool:
        return (
            self._proc is not None
            and self._proc.poll() is None
            and self.ready_payload is not None
        )

    def start(self) -> dict[str, Any]:
        if self.is_ready:
            assert self.ready_payload is not None
            return self.ready_payload

        for path, label in (
            (self.python_exe, "exact extractor Python"),
            (self.worker_script, "exact extractor worker script"),
        ):
            if not path.exists() or not path.is_file():
                raise ModelLoadError(f"Required {label} is missing.")

        self.stderr_log.parent.mkdir(parents=True, exist_ok=True)
        self._stderr_handle = self.stderr_log.open("a", encoding="utf-8")

        try:
            self._proc = subprocess.Popen(
                [
                    str(self.python_exe),
                    str(self.worker_script),
                    "--root",
                    str(self.project_root),
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=self._stderr_handle,
                text=True,
                bufsize=1,
                cwd=str(self.project_root),
            )
            payload = self._read_json_line("startup")
        except Exception:
            self.close(force=True)
            raise

        if payload.get("type") != "ready":
            self.close(force=True)
            raise ModelLoadError(
                "Exact extractor did not emit the expected ready payload."
            )

        if payload.get("device") != "cuda":
            self.close(force=True)
            raise ModelLoadError(
                "Qualified exact extractor is required to run on CUDA."
            )

        self.ready_payload = payload
        return payload

    def _read_json_line(self, context: str) -> dict[str, Any]:
        if self._proc is None or self._proc.stdout is None:
            raise InferenceError("Exact extractor process is not running.")

        raw = self._proc.stdout.readline()
        if raw == "":
            rc = self._proc.poll()
            raise InferenceError(
                f"Exact extractor exited during {context}; return code={rc}."
            )

        try:
            payload = json.loads(raw.strip())
        except json.JSONDecodeError as exc:
            raise InferenceError(
                f"Exact extractor emitted non-JSON stdout during {context}."
            ) from exc

        if not isinstance(payload, dict):
            raise InferenceError("Exact extractor returned an invalid payload.")

        return payload

    def extract(self, *, video_path: Path, output_path: Path) -> dict[str, Any]:
        if not self.is_ready:
            self.start()

        assert self._proc is not None
        assert self._proc.stdin is not None

        if not video_path.exists() or not video_path.is_file():
            raise InferenceError("Configured video source is unavailable.")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.exists():
            output_path.unlink()

        request = {
            "cmd": "extract",
            "video": str(video_path.resolve()),
            "output": str(output_path.resolve()),
        }

        self._proc.stdin.write(json.dumps(request, separators=(",", ":")) + "\n")
        self._proc.stdin.flush()

        response = self._read_json_line(f"extracting {video_path.name}")

        if response.get("type") != "result" or response.get("ok") is not True:
            raise InferenceError("Exact I3D extraction failed.")

        if not output_path.exists() or not output_path.is_file():
            raise InferenceError(
                "Exact extractor reported success but did not create output."
            )

        return response

    def close(self, *, force: bool = False) -> None:
        proc = self._proc
        self._proc = None
        self.ready_payload = None

        try:
            if proc is not None and proc.poll() is None:
                if not force and proc.stdin is not None:
                    try:
                        proc.stdin.write('{"cmd":"shutdown"}\n')
                        proc.stdin.flush()
                    except OSError:
                        force = True

                if force:
                    proc.kill()

                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
        finally:
            if self._stderr_handle is not None:
                self._stderr_handle.close()
                self._stderr_handle = None

    def __enter__(self) -> "PersistentExactExtractor":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.close(force=exc_type is not None)
        return False
