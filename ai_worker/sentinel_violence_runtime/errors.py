"""Worker error taxonomy aligned to docs/07-api-specification.md."""

from __future__ import annotations


MODEL_LOAD_FAILED = "MODEL_LOAD_FAILED"
UNSUPPORTED_INPUT = "UNSUPPORTED_INPUT"
VIDEO_DECODE_FAILED = "VIDEO_DECODE_FAILED"
INFERENCE_FAILED = "INFERENCE_FAILED"
TRACKING_FAILED = "TRACKING_FAILED"
INVALID_REQUEST = "INVALID_REQUEST"
INSUFFICIENT_TEMPORAL_INPUT = "INSUFFICIENT_TEMPORAL_INPUT"
INTERNAL_WORKER_ERROR = "INTERNAL_WORKER_ERROR"


class SentinelWorkerError(Exception):
    """Base exception carrying a stable worker error code."""

    code = INTERNAL_WORKER_ERROR

    def __init__(self, message: str):
        super().__init__(message)
        self.safe_message = str(message)


class InvalidRequestError(SentinelWorkerError):
    code = INVALID_REQUEST


class UnsupportedInputError(SentinelWorkerError):
    code = UNSUPPORTED_INPUT


class VideoDecodeError(SentinelWorkerError):
    code = VIDEO_DECODE_FAILED


class ModelLoadError(SentinelWorkerError):
    code = MODEL_LOAD_FAILED


class InferenceError(SentinelWorkerError):
    code = INFERENCE_FAILED
