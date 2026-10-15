import math
import os


SCHEMA_VERSION="1"
VIOLENCE_TASK="violence_fighting"
VIOLENCE_LABEL="fighting"
MODEL_EXPERIMENT_ID="EXP-VIO-TEMPORAL-001"
MODEL_VERSION_LABEL="MODEL-VIO-BIGRU-ATTN-XD-V1"
MODEL_VERSION_ID="6d22f83d-17f8-5ecf-9f0f-246fa326ec72"
MODEL_CHECKPOINT_SHA256="1fa01d1be82ab3c63d33b4d5f1d5ef4ab2a176d1d2842afc842955ff72896772"
QUALIFIED_LIVE_THRESHOLD=0.906
EXPERIMENTAL_LIVE_THRESHOLD=0.80
EXPERIMENTAL_THRESHOLD_ENV="SENTINEL_EXPERIMENTAL_THRESHOLD"


def _resolve_live_threshold()->tuple[float,bool]:
    raw=os.environ.get(EXPERIMENTAL_THRESHOLD_ENV)
    if raw is None:
        return QUALIFIED_LIVE_THRESHOLD,False
    try:
        value=float(raw)
    except ValueError as exc:
        raise RuntimeError(
            f"{EXPERIMENTAL_THRESHOLD_ENV} must be a finite number within [0, 1]."
        ) from exc
    if not math.isfinite(value) or not 0.0<=value<=1.0:
        raise RuntimeError(
            f"{EXPERIMENTAL_THRESHOLD_ENV} must be a finite number within [0, 1]."
        )
    if value!=EXPERIMENTAL_LIVE_THRESHOLD:
        raise RuntimeError(
            f"{EXPERIMENTAL_THRESHOLD_ENV} only supports the isolated 0.80 experiment."
        )
    return value,True


LIVE_THRESHOLD,EXPERIMENTAL_THRESHOLD_ACTIVE=_resolve_live_threshold()
LIVE_N_REQUIRED=3
LIVE_M_HISTORY=5
LIVE_STRIDE_FEATURE_STEPS=1
LIVE_WINDOW_FEATURE_STEPS=1
SCORE_SEMANTICS=("uncalibrated sigmoid score for the fighting positive class from "
                 "EXP-VIO-TEMPORAL-001; higher means more fighting-like")
ALLOWED_WORKER_ERROR_CODES=frozenset({"MODEL_LOAD_FAILED","UNSUPPORTED_INPUT","VIDEO_DECODE_FAILED","INFERENCE_FAILED","TRACKING_FAILED","INVALID_REQUEST","INSUFFICIENT_TEMPORAL_INPUT","INTERNAL_WORKER_ERROR"})
