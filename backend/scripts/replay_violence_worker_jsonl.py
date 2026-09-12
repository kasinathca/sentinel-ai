from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from app.ai_integration.errors import AIIntegrationError, WorkerReportedFailure
from app.ai_integration.service import ViolenceWorkerResultService
from app.events.violence_conditions import RecordingViolenceConditionConsumer


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")

    consumer = RecordingViolenceConditionConsumer()
    service = ViolenceWorkerResultService(condition_consumer=consumer)

    accepted = 0
    worker_failures = 0

    with args.input.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            raw = raw.strip()
            if not raw:
                continue

            try:
                payload = json.loads(raw)
            except json.JSONDecodeError as exc:
                print(
                    f"line {line_number}: invalid JSON: {exc}",
                    file=sys.stderr,
                )
                return 2

            try:
                service.consume_payload(payload)
                accepted += 1
            except WorkerReportedFailure as exc:
                worker_failures += 1
                print(
                    f"line {line_number}: worker failure "
                    f"{exc.worker_code}: {exc.safe_message}",
                    file=sys.stderr,
                )
            except AIIntegrationError as exc:
                print(
                    f"line {line_number}: integration rejected payload: "
                    f"{exc.code}: {exc}",
                    file=sys.stderr,
                )
                return 3

    qualified = [
        evaluation
        for evaluation in consumer.evaluations
        if evaluation.candidate_condition
    ]

    summary = {
        "accepted_success_observations": accepted,
        "worker_failure_messages": worker_failures,
        "qualified_observations": len(qualified),
        "first_qualified_index": (
            consumer.evaluations.index(qualified[0]) if qualified else None
        ),
        "candidate_condition_seen": bool(qualified),
        "max_score": max(
            (evaluation.score for evaluation in consumer.evaluations),
            default=None,
        ),
    }

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
