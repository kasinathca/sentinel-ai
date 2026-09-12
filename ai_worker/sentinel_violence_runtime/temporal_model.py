"""Frozen EXP-VIO-TEMPORAL-001 scorer."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys

import numpy as np
import torch

from .constants import (
    CHECKPOINT_SHA256,
    EXPECTED_MODEL_PARAMETERS,
    MODEL_EXPERIMENT_ID,
    TRAIN_SCRIPT_SHA256,
)
from .errors import InferenceError, ModelLoadError


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class FrozenTemporalScorer:
    def __init__(
        self,
        *,
        training_script: Path,
        checkpoint: Path,
        batch_size: int = 64,
    ) -> None:
        self.training_script = training_script.resolve()
        self.checkpoint = checkpoint.resolve()
        self.batch_size = int(batch_size)

        if self.batch_size < 1:
            raise ValueError("batch_size must be >= 1")

        self.module = None
        self.model = None
        self.device = None
        self.checkpoint_payload = None

    @property
    def is_ready(self) -> bool:
        return (
            self.module is not None
            and self.model is not None
            and self.device is not None
        )

    def load(self) -> None:
        if self.is_ready:
            return

        for path, label in (
            (self.training_script, "training script"),
            (self.checkpoint, "checkpoint"),
        ):
            if not path.exists() or not path.is_file():
                raise ModelLoadError(f"Frozen temporal {label} is missing.")

        if _sha256(self.training_script) != TRAIN_SCRIPT_SHA256:
            raise ModelLoadError("Frozen temporal training-script SHA256 mismatch.")
        if _sha256(self.checkpoint) != CHECKPOINT_SHA256:
            raise ModelLoadError("Frozen temporal checkpoint SHA256 mismatch.")

        spec = importlib.util.spec_from_file_location(
            "sentinel_temporal_runtime_frozen",
            self.training_script,
        )
        if spec is None or spec.loader is None:
            raise ModelLoadError("Could not import frozen temporal training module.")

        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        if int(getattr(module, "SEQ_LEN", -1)) != 64:
            raise ModelLoadError("Frozen temporal SEQ_LEN identity mismatch.")
        if int(getattr(module, "INPUT_DIM", -1)) != 2048:
            raise ModelLoadError("Frozen temporal INPUT_DIM identity mismatch.")
        if not hasattr(module, "TemporalGRU"):
            raise ModelLoadError("Frozen temporal model class is unavailable.")

        checkpoint = torch.load(self.checkpoint, map_location="cpu")
        if checkpoint.get("experiment_id") != MODEL_EXPERIMENT_ID:
            raise ModelLoadError("Frozen temporal checkpoint experiment mismatch.")

        model = module.TemporalGRU()
        model.load_state_dict(checkpoint["model_state_dict"], strict=True)

        count = sum(p.numel() for p in model.parameters())
        if count != EXPECTED_MODEL_PARAMETERS:
            raise ModelLoadError(
                f"Frozen temporal parameter count mismatch: {count:,}."
            )

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if device.type != "cuda":
            raise ModelLoadError(
                "Qualified frozen temporal runtime requires CUDA in this setup."
            )

        model.to(device)
        model.eval()

        self.module = module
        self.model = model
        self.device = device
        self.checkpoint_payload = checkpoint

    def _resample_w1(self, raw_step: np.ndarray) -> np.ndarray:
        assert self.module is not None

        if raw_step.shape != (1, 5, 2048):
            raise InferenceError(
                f"Expected one exact I3D feature step (1,5,2048); got "
                f"{raw_step.shape}."
            )

        seq = np.asarray(raw_step, dtype=np.float32).mean(axis=1)
        idx = np.rint(
            np.linspace(0, seq.shape[0] - 1, int(self.module.SEQ_LEN))
        ).astype(np.int64)
        idx = np.clip(idx, 0, seq.shape[0] - 1)
        out = seq[idx].astype(np.float32, copy=False)

        if out.shape != (64, 2048):
            raise InferenceError(
                f"Frozen temporal preprocessing produced shape {out.shape}."
            )
        return out

    def score_feature_array(self, features: np.ndarray) -> np.ndarray:
        self.load()

        assert self.model is not None
        assert self.device is not None

        array = np.asarray(features)
        if array.ndim != 3 or array.shape[1:] != (5, 2048):
            raise InferenceError(
                f"Expected exact I3D feature array (T,5,2048); got {array.shape}."
            )
        if array.shape[0] < 1:
            raise InferenceError("Exact I3D feature array is empty.")

        sequences = [
            self._resample_w1(array[i : i + 1])
            for i in range(array.shape[0])
        ]

        outputs: list[np.ndarray] = []

        with torch.inference_mode():
            for start in range(0, len(sequences), self.batch_size):
                batch_np = np.stack(
                    sequences[start : start + self.batch_size],
                    axis=0,
                ).astype(np.float32, copy=False)

                batch = torch.from_numpy(batch_np).to(self.device)
                logits, _ = self.model(batch)
                probs = torch.sigmoid(logits)

                outputs.append(
                    probs.detach()
                    .cpu()
                    .numpy()
                    .astype(np.float64, copy=False)
                )

        scores = np.concatenate(outputs, axis=0)

        if scores.shape != (array.shape[0],):
            raise InferenceError(
                f"Frozen temporal scorer produced unexpected shape {scores.shape}."
            )
        if not np.all(np.isfinite(scores)):
            raise InferenceError("Frozen temporal scorer produced non-finite output.")
        if np.any(scores < 0.0) or np.any(scores > 1.0):
            raise InferenceError("Frozen temporal scorer output is outside [0,1].")

        return scores
