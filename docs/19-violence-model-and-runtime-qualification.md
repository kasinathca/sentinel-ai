---
title: "Sentinel AI — Violence Model and Runtime Qualification Record"
document_id: "SEN-VIO-QUAL"
version: "1.0.0"
status: "FROZEN_EVIDENCE_RECORD"
project: "Sentinel AI"
academic_context: "Advanced Web Technologies course project"
last_updated: "2026-09-12"
authoritative_for:
  - "selected violence model identity"
  - "violence dataset split counts"
  - "live violence policy"
  - "violence threshold provenance"
  - "raw-video feature compatibility"
  - "violence runtime benchmark evidence"
  - "final held-out violence metrics"
  - "post-test no-retuning rule"
---

# Sentinel AI — Violence Model and Runtime Qualification Record

## 1. Purpose

This document is the authoritative evidence record for the Sentinel AI
violence/fighting subsystem as qualified on 2026-09-12.

It consolidates:

- dataset identity and frozen splits;
- baseline and temporal-model results;
- exact I3D extractor provenance;
- raw-video feature compatibility;
- live-window policy selection;
- validation-only threshold calibration;
- one-time official TEST result;
- persistent runtime benchmark;
- final raw-video live-policy parity.

This document does **not** claim that the complete Sentinel web application,
person detector, tracker, event persistence, evidence pipeline, WebSocket
delivery, or operator workflows are fully verified.

---

# 2. Final Model Identity

```text
experiment_id     = EXP-VIO-TEMPORAL-001
version_label     = MODEL-VIO-BIGRU-ATTN-XD-V1
model_version_id  = 6d22f83d-17f8-5ecf-9f0f-246fa326ec72
parameters        = 822,530
best epoch        = 3
```

Checkpoint:

```text
sentinel_temporal/artifacts/best_model.pt
SHA256:
1fa01d1be82ab3c63d33b4d5f1d5ef4ab2a176d1d2842afc842955ff72896772
```

Training implementation:

```text
sentinel_temporal/train_temporal_gru.py
SHA256:
630c913060c7800c96214438e8e36064b946679aa83aad4b8fd4943b6717690c
```

---

# 3. Dataset and Frozen Splits

Feature dataset:

```text
DATA-XD-I3D-FEATURES-V1
4750 .npy files
shape schema = (T, 5, 2048)
RGB
```

Derived strict binary task:

```text
DATA-DERIVED-XD-FIGHTING-BINARY-V1
Fighting = 1
Normal   = 0
```

All other XD-Violence categories are excluded from this strict experiment.

| Split | Normal | Fighting | Total |
|---|---:|---:|---:|
| TRAIN | 1636 | 302 | 1938 |
| VALIDATION | 410 | 75 | 485 |
| TEST | 300 | 107 | 407 |
| **Total** | **2346** | **484** | **2830** |

The official TEST split was not used for model/window/threshold selection.

The dataset labels are video-level weak labels.

Therefore:

- video-level classification metrics are valid;
- positive-video coverage is valid;
- Normal-window false-trigger analysis is valid;
- exact fighting-onset latency is not established;
- frame/window localization recall must not be claimed.

---

# 4. Frozen Temporal Model Architecture

Input:

```text
(T, 5, 2048)
```

Processing:

```text
mean across 5 crops
→ (T, 2048)
→ deterministic uniform temporal sampling to 64 steps
→ Linear(2048 → 256)
→ LayerNorm
→ GELU
→ Dropout(0.25)
→ one-layer BiGRU
   input = 256
   hidden = 128 per direction
→ (64, 256)
→ learned attention:
   Linear(256 → 1)
   softmax over temporal dimension
→ weighted temporal pooling
→ LayerNorm
→ Dropout(0.25)
→ Linear(256 → 1)
→ sigmoid Fighting score
```

---

# 5. Whole-Video Model Evaluation

Frozen validation threshold:

```text
0.8345891237258911
```

Validation:

```text
TN=405 FP=5 FN=15 TP=60

accuracy   = 0.958762887
precision  = 0.923076923
recall     = 0.800000000
F1         = 0.857142857
ROC-AUC    = 0.955837398
PR-AUC     = 0.890961330
```

Held-out TEST:

```text
TN=296 FP=4 FN=18 TP=89

accuracy     = 0.945945946
precision    = 0.956989247
recall       = 0.831775701
specificity  = 0.986666667
F1           = 0.890000000
ROC-AUC      = 0.981557632
PR-AUC       = 0.944877884
```

---

# 6. Exact Raw-Video I3D Provenance

The correct reference-producing extractor was traced to the Jia-Herng
inappropriate-video-detection feature extractor.

Frozen backbone/config identity:

```text
i3d_imagenet-pretrained-r50-nl-dot-product_8xb8-32x2x1-100e_kinetics400-rgb
```

Checkpoint:

```text
i3d_imagenet-pretrained-r50-nl-dot-product_8xb8-32x2x1-100e_kinetics400-rgb_20220812-8e1f2148.pth
```

Key preprocessing:

```text
clip_len      = 32
sampling_rate = 2
resize        = 256
crop          = 224
crops         = 5
dtype         = float32 [0,1]
mean          = (0.485, 0.456, 0.406)
std           = (0.229, 0.224, 0.225)
layout        = CTHW
```

The exact extractor output is:

```text
(T, 5, 2048)
```

with sequential 64-source-frame sampling blocks.

---

# 7. Runtime Compatibility Experiment Lineage

## 7.1 Phase 2B / 2C — wrong extractor diagnosis

An earlier non-local-disabled I3D candidate produced only approximately
`0.33–0.38` cosine compatibility.

Temporal/crop/normalization searches did not recover compatibility.

Conclusion:

```text
root cause = wrong architecture/weights family
```

## 7.2 Phase 2D — exact feature reproduction

Normal fixture:

```text
shape       = (26, 5, 2048)
cosine      = 0.999999961
pearson     = 0.999999932
MAE         = 4.958858e-05
max error   = 7.944107e-04
```

Fighting fixture:

```text
shape       = (19, 5, 2048)
cosine      = 0.999999910
pearson     = 0.999999831
MAE         = 6.852957e-05
max error   = 1.071572e-03
```

Verdict:

```text
EXACT_PIPELINE_CONFIRMED
```

## 7.3 Phase 2E-A — frozen baseline classifier parity

Reference/generated feature scores produced matching classifications.

Maximum observed probability difference:

```text
≈ 5.0e-06
```

Verdict:

```text
PHASE_2E_A_BASELINE_PARITY_CONFIRMED
```

## 7.4 Phase 2F — raw-video baseline path

```text
MP4
→ exact I3D
→ frozen Logistic Regression baseline
→ score
→ decision
```

Both compatibility fixtures reproduced archived behavior.

Verdict:

```text
PHASE_2F_END_TO_END_PARITY_CONFIRMED
```

---

# 8. Persistent Runtime Benchmark

## 8.1 Cold-process benchmark

Aggregate median:

```text
13.634 s / video
```

## 8.2 Persistent exact-extractor benchmark

Normal fixture:

```text
source duration    = 69.041667 s
median total       = 9.306 s
median extraction  = 9.300 s
realtime factor    = 7.428x
peak allocated     = 337 MB
peak reserved      = 472 MB
```

Fighting fixture:

```text
source duration    = 50.0 s
median total       = 6.859 s
median extraction  = 6.852 s
realtime factor    = 7.293x
peak allocated     = 337 MB
peak reserved      = 472 MB
```

Aggregate warm median:

```text
8.126 s / video
```

Compared with cold-process median:

```text
13.634 s → 8.126 s
≈ 40.4% reduction
≈ 1.68x throughput improvement
```

The exact I3D extractor is the dominant runtime cost.

The downstream classifier cost is negligible by comparison.

These are controlled fixture measurements and do not prove final multi-camera
capacity.

---

# 9. Live Window Qualification

The whole-video model cannot be applied to an infinite live stream without an
explicit temporal policy.

No frame-level fighting localization labels were available for this strict
subset, so live-policy evaluation was designed around weak-label-safe metrics:

- video-level positive coverage;
- precision;
- F1;
- Normal-video false-event rate;
- Normal-window trigger rate.

## 9.1 Logistic Regression live-window study

Best evaluated Logistic policy:

```text
W12 / stride 1 / 3-of-5
F1                       = 0.545455
precision                = 0.439024
positive-video coverage  = 0.720000
Normal-video false-event = 0.168293
```

Conclusion:

```text
not selected for live deployment
```

## 9.2 Temporal model live-window study

Best structural policy before live-threshold recalibration:

```text
W1 / stride 1 / 3-of-5
threshold = original whole-video threshold 0.8345891237

F1                       = 0.659341
precision                = 0.560748
positive-video coverage  = 0.800000
Normal-video false-event = 0.114634
```

Selected structure:

```text
W1 / stride 1 / 3-of-5
```

---

# 10. Validation-Only Live Threshold Calibration

The structure was held fixed.

Only the live score threshold was evaluated on VALIDATION.

Selected threshold:

```text
0.906
```

Validation operating point:

```text
TN=381 FP=29 FN=16 TP=59

F1                       = 0.723926
precision                = 0.670455
positive-video coverage  = 0.786667
Normal-video false-event = 0.070732
```

Reason for selecting `0.906` instead of the validation maximum-F1 point
`0.940`:

- `0.940` achieved a slightly higher F1;
- coverage fell to `0.72`;
- Sentinel is an alerting system where excessive loss of positive coverage is
  an undesirable trade for that F1 gain;
- `0.906` preserved near-0.80 coverage while materially reducing false events;
- `0.906` had the same video-level confusion as `0.904` with fewer raw
  threshold-triggering windows.

The policy was frozen before opening official TEST.

---

# 11. Frozen Live Policy

```text
policy_id = EXP-VIO-LIVE-WINDOW-004

model:
EXP-VIO-TEMPORAL-001

worker observation:
W1 exact I3D feature step

stride:
1 feature step

positive score:
fighting_score >= 0.906

backend temporal criterion:
at least 3 positive scores among the most recent 5
```

This criterion determines a candidate violence condition.

It does not define:

- event deduplication;
- episode cooldown;
- evidence;
- acknowledgement;
- alert delivery.

---

# 12. One-Time Official TEST

The official TEST was accessed after the policy was frozen.

No threshold/window search was performed on TEST.

Result:

```text
TN=285 FP=15 FN=21 TP=86

accuracy                  = 0.911548
balanced accuracy         = 0.876869
precision                 = 0.851485
positive-video coverage   = 0.803738
specificity               = 0.950000
F1                        = 0.826923
Normal-video false-event  = 0.050000
normal-window raw trigger = 0.014838
false episodes / 1000
Normal windows            = 1.0635
```

After this run:

```text
TEST-driven model/window/threshold retuning is prohibited.
```

---

# 13. Final Raw-Video Temporal Policy Parity

`EXP-VIO-LIVE-RUNTIME-001` evaluated the frozen policy over newly regenerated
raw-video features and compared it with the stored reference feature path.

## Normal fixture

```text
feature shape       = (26, 5, 2048)
feature cosine      = 0.999999960759
feature MAE         = 4.958858e-05
max score diff      = 4.060008e-05
raw flags match     = true
3-of-5 flags match  = true
reference event     = false
generated event     = false
```

## Fighting fixture

```text
feature shape       = (19, 5, 2048)
feature cosine      = 0.999999910273
feature MAE         = 6.852958e-05
max score diff      = 2.856553e-04
raw flags match     = true
3-of-5 flags match  = true
reference event     = true
generated event     = true
```

Final verdict:

```text
PHASE_2J_RAW_VIDEO_TEMPORAL_LIVE_PARITY_CONFIRMED
```

---

# 14. Runtime Environment

## 14.1 Temporal classifier environment

Observed:

```text
PyTorch = 2.13.0+cu130
CUDA    = available
GPU     = NVIDIA GeForce RTX 3050 6GB Laptop GPU
```

## 14.2 Exact extractor isolated environment

Observed qualified stack:

```text
Python       = 3.10.x
NumPy        = 1.26.4
torch        = 2.1.2+cu118
torchvision  = 0.16.2+cu118
decord       = 0.6.0
mmcv         = 2.1.0
mmengine     = 0.10.7
mmaction2    = 1.2.0 source override
```

The MMAction2 source override is part of the qualified environment.

Do not silently upgrade these dependencies without rerunning compatibility
qualification.

---

# 15. Evidence Artifacts

Key report paths in the local workspace:

```text
sentinel_runtime_validation/reports/
├── EXP-VIO-RUNTIME-COMPAT-001-phase2d-exact-jherng.json
├── EXP-VIO-RUNTIME-COMPAT-001-phase2e-baseline-parity.json
├── EXP-VIO-RUNTIME-COMPAT-001-phase2f-end-to-end-fixtures.json
├── EXP-VIO-RUNTIME-COMPAT-001-phase2g-persistent-*.json
├── EXP-VIO-LIVE-WINDOW-001-phase2h-validation-window-policy.json
├── EXP-VIO-LIVE-WINDOW-002-phase2h-temporal-validation-v2.json
├── EXP-VIO-LIVE-WINDOW-003-phase2h-threshold-calibration.json
├── EXP-VIO-LIVE-WINDOW-004-frozen-policy.json
├── EXP-VIO-LIVE-WINDOW-004-final-test.json
└── EXP-VIO-LIVE-RUNTIME-001-phase2j-raw-video-parity.json
```

Do not commit large external video/model/feature artifacts merely to make these
reports reproducible.

Record hashes and acquisition/recreation instructions instead.

---

# 16. What Is Qualified

The following are qualified:

- selected Fighting-vs-Normal dataset split;
- temporal-model architecture/checkpoint identity;
- whole-video temporal metrics;
- exact raw-video I3D compatibility;
- persistent exact-extractor feasibility on the qualification hardware;
- live W1 scoring formulation;
- 3-of-5 criterion;
- threshold `0.906`;
- one-time held-out live-policy metrics;
- raw-video final-policy parity.

---

# 17. What Is Not Yet Qualified

This record does **not** establish:

- final person detector;
- final tracker;
- final backend ↔ worker transport;
- final camera/live-stream adapter;
- multi-camera capacity;
- event duplicate/retrigger semantics;
- persistent event creation;
- evidence generation;
- WebSocket delivery;
- acknowledgement;
- operator UI behavior;
- event-to-client latency;
- complete application E2E acceptance.

These remain separate engineering/test tasks.

---

# 18. Post-Test Freeze Rule

After `EXP-VIO-LIVE-WINDOW-004`:

```text
do not change:
- selected model from TEST behavior
- W1 policy from TEST behavior
- 3-of-5 criterion from TEST behavior
- threshold 0.906 from TEST behavior
```

A future model/policy change requires:

1. a new experiment/version ID;
2. development using TRAIN/VALIDATION only;
3. a new independently protected final evaluation procedure.

The current official TEST result shall not be reused as a tuning loop.

---

# 19. Architectural Boundary

The AI worker owns:

- exact feature extraction;
- frozen temporal model inference;
- structured score result;
- explicit model/runtime failure.

The backend owns:

- worker-result validation;
- rolling per-camera 3-of-5 criterion state;
- application-domain event creation;
- duplicate/cooldown/retrigger policy;
- persistence;
- evidence;
- notification;
- acknowledgement.

Worker transport remains a separate architecture decision.

---

# 20. Final Qualification Statement

As of 2026-09-12:

```text
Sentinel AI's Fighting-vs-Normal temporal model,
validation-selected live scoring policy,
and exact raw-video feature/inference path
have completed model-level and runtime-compatibility qualification.

Final live policy:
W1 / stride 1 / 3-of-5 / threshold 0.906

Official held-out TEST F1:
0.826923

Raw-video final-policy parity:
CONFIRMED
```

This statement shall not be broadened into a claim that the complete Sentinel
application is production-ready or fully verified.
