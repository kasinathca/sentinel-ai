"""Development-only file/JSON adapter for the transport-neutral violence runtime.

This is NOT a declaration of the project's final worker transport.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .contracts import WorkerProcessingRequest, WorkerFailureResult
from .errors import InvalidRequestError, SentinelWorkerError
from .runtime import ViolenceRuntime
from .source_resolver import MappingSourceResolver


def _write_json_line(handle, payload: dict) -> None:
    handle.write(json.dumps(payload, separators=(",", ":"), ensure_ascii=False))
    handle.write("\n")
    handle.flush()


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--source-map", type=Path, required=True)
    parser.add_argument("--request", type=Path)
    parser.add_argument("--source-started-at")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--preflight-only", action="store_true")

    args = parser.parse_args()

    root = args.root.resolve()

    runtime = ViolenceRuntime(project_root=root)

    if args.preflight_only:
        try:
            runtime.start()
            print(json.dumps({
                "health": runtime.health().to_dict(),
                "capabilities": runtime.capabilities(),
            }, indent=2))
            return 0
        finally:
            runtime.close()

    if args.request is None:
        parser.error("--request is required unless --preflight-only is used.")
    if not args.source_started_at:
        parser.error(
            "--source-started-at is required for the file-source development adapter."
        )

    resolver = MappingSourceResolver.from_json_file(args.source_map)

    try:
        request_data = json.loads(
            args.request.read_text(encoding="utf-8")
        )
        request = WorkerProcessingRequest.from_dict(request_data)
        source = resolver.resolve(request.source.source_locator_ref)
    except (OSError, json.JSONDecodeError, InvalidRequestError, SentinelWorkerError) as exc:
        print(f"Request/source configuration error: {exc}", file=sys.stderr)
        return 2

    output_handle = sys.stdout

    if args.output:
        # Runtime output directories are generated artifacts and may not exist
        # in a fresh checkout. Create the parent explicitly before opening.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        output_handle = args.output.open("w", encoding="utf-8")

    try:
        with runtime:
            result = runtime.process_file(
                request=request,
                source_path=source,
                source_started_at=args.source_started_at,
            )

            if isinstance(result, WorkerFailureResult):
                _write_json_line(output_handle, result.to_dict())
                return 1

            for window_result in result:
                _write_json_line(output_handle, window_result.to_dict())

            return 0
    finally:
        if args.output:
            output_handle.close()


if __name__ == "__main__":
    raise SystemExit(main())
