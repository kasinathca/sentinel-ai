"""Frozen identities and runtime constants for Sentinel violence inference."""

from __future__ import annotations

SCHEMA_VERSION = "1"
TASK_VIOLENCE = "violence_fighting"

MODEL_EXPERIMENT_ID = "EXP-VIO-TEMPORAL-001"
MODEL_VERSION_LABEL = "MODEL-VIO-BIGRU-ATTN-XD-V1"

# Stable UUIDv5 derived from the immutable checkpoint SHA-256.
# This can be used as the model_versions.id when the application model registry
# is populated, preserving the same ID across local runs.
MODEL_VERSION_ID = "6d22f83d-17f8-5ecf-9f0f-246fa326ec72"

CHECKPOINT_RELATIVE = "sentinel_temporal/artifacts/best_model.pt"
TRAIN_SCRIPT_RELATIVE = "sentinel_temporal/train_temporal_gru.py"

CHECKPOINT_SHA256 = (
    "1fa01d1be82ab3c63d33b4d5f1d5ef4ab2a176d1d2842afc842955ff72896772"
)
TRAIN_SCRIPT_SHA256 = (
    "630c913060c7800c96214438e8e36064b946679aa83aad4b8fd4943b6717690c"
)
EXPECTED_MODEL_PARAMETERS = 822_530

EXACT_EXTRACTOR_PYTHON_RELATIVE = (
    "sentinel_runtime_validation/extractor_exact_jherng/.venv/Scripts/python.exe"
)
EXACT_EXTRACTOR_WORKER_RELATIVE = (
    "sentinel_runtime_validation/scripts/phase2g_persistent_extractor_worker.py"
)

# One exact I3D output feature step corresponds to one sequential 64-source-frame
# block in the qualified Jia-Herng preprocessing pipeline.
SOURCE_FRAMES_PER_FEATURE_STEP = 64

# Worker reports the positive-class model score. It does NOT create the event.
SCORE_SEMANTICS = (
    "uncalibrated sigmoid score for the fighting positive class from "
    "EXP-VIO-TEMPORAL-001; higher means more fighting-like"
)
SCORE_LABEL = "fighting"

# Validation-selected backend event criterion.
# Frozen after EXP-VIO-LIVE-WINDOW-003 and tested once in EXP-VIO-LIVE-WINDOW-004.
LIVE_SCORE_THRESHOLD = 0.906
LIVE_N_REQUIRED = 3
LIVE_M_HISTORY = 5
LIVE_STRIDE_FEATURE_STEPS = 1
LIVE_WINDOW_FEATURE_STEPS = 1

FINAL_TEST_CONFUSION = {
    "tn": 285,
    "fp": 15,
    "fn": 21,
    "tp": 86,
}
FINAL_TEST_METRICS = {
    "f1": 0.826923,
    "precision": 0.851485,
    "positive_video_coverage": 0.803738,
    "accuracy": 0.911548,
    "balanced_accuracy": 0.876869,
    "specificity": 0.950000,
    "normal_video_false_event_rate": 0.050000,
}
