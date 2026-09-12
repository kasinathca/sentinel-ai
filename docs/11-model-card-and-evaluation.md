---
title: "Sentinel AI — Model Cards and Evaluation Specification"
document_id: "SEN-MODEL-EVAL"
version: "0.2.0"
status: "DRAFT_FOR_TEAM_REVIEW"
project: "Sentinel AI"
academic_context: "Advanced Web Technologies course project"
last_updated: "2026-09-12"
owners:
  - "TBD"
reviewers:
  - "TBD"
authoritative_for:
  - "model card structure"
  - "AI evaluation methodology"
  - "performance claim evidence"
  - "detector evaluation"
  - "tracker evaluation"
  - "violence model evaluation"
  - "threshold calibration"
  - "latency and FPS measurement"
  - "false-positive and false-negative analysis"
  - "model deployment qualification"
  - "AI result reporting"
---

# Sentinel AI — Model Cards and Evaluation Specification

> **Document purpose**
>
> This document defines how Sentinel AI models and AI-assisted system behavior shall be evaluated, documented, and reported.
>
> It is intentionally conservative.
>
> Current implementation state as of 2026-09-12:
>
> - no person detector has yet been formally selected;
> - no tracker has yet been formally selected;
> - the violence/fighting model **has been selected and frozen**;
> - the strict XD-Violence Fighting-vs-Normal feature split is active;
> - whole-video model evaluation is complete;
> - the live `W1 / 3-of-5 / 0.906` policy is frozen;
> - the policy received one final held-out TEST evaluation;
> - raw-video exact-feature compatibility and final-policy parity are qualified;
> - final full-application event-to-client latency remains unmeasured.
>
> Quantitative violence results in this document are measured evidence.
> Detector/tracker and unfinished application-level metrics remain
> `NOT_YET_MEASURED` where applicable.
>
> This document does **not** contain placeholder accuracy values.
>
> Its purpose is to ensure that when numbers are eventually reported, they are:
>
> - measured;
> - reproducible;
> - traceable;
> - correctly defined;
> - interpreted honestly;
> - tied to exact model and dataset versions.

---

# 0. Document Control

## 0.1 Authority

After baseline approval, this document becomes authoritative for AI model evaluation and reporting.

It is subordinate to:

1. `PROJECT_HANDBOOK.md`
2. `02-srs.md`
3. `08-ai-ml-design.md`
4. `09-dataset-acquisition.md`
5. `10-dataset-registry.md`
6. accepted AI/model ADRs

The actual dataset identity and split must come from:

`10-dataset-registry.md`

The model architecture/design must come from:

`08-ai-ml-design.md`

## 0.2 Model-card status vocabulary

| Status | Meaning |
|---|---|
| `DRAFT` | Card structure exists but model not fully evaluated |
| `EXPERIMENTAL` | Model under active experimentation |
| `CANDIDATE` | Model suitable for comparison |
| `APPROVED_FOR_DEMO` | Model accepted for final integrated demonstration |
| `APPROVED_FOR_REPORTING` | Evidence sufficient for formal reported metrics |
| `RETIRED` | No longer used |
| `INVALIDATED` | Model results no longer trusted due to data/code/evaluation issue |

## 0.3 Measurement-state vocabulary

| State | Meaning |
|---|---|
| `NOT_YET_MEASURED` | No valid measurement exists |
| `MEASURED_PRELIMINARY` | Measurement exists but not frozen/final |
| `MEASURED_FINAL` | Final procedure executed and evidence stored |
| `NOT_APPLICABLE` | Metric is not meaningful for the task |
| `INVALIDATED` | Previously reported value is no longer valid |

## 0.4 Claim rule

A performance number shall not appear in the final report or presentation unless:

```text
model ID
+ model version
+ dataset ID
+ exact split
+ metric definition
+ evaluation script/version
+ hardware where relevant
+ result artifact
```

are known.

---

# 1. Evaluation Philosophy

## 1.1 Model quality is not system quality

Sentinel contains several layers:

```text
video
→ detector
→ tracker
→ rule/model result
→ event
→ alert
→ operator workflow
```

A high-performing model can still produce a poor system if:

- thresholds are wrong;
- zone geometry is wrong;
- duplicate suppression is broken;
- event persistence fails;
- alerts do not reach the client.

Therefore evaluation is divided into:

1. model-level evaluation;
2. subsystem-level evaluation;
3. rule/event evaluation;
4. end-to-end system evaluation.

## 1.2 Never collapse unrelated metrics

Do not combine:

- detector confidence;
- tracker association confidence;
- violence score;
- event reliability;

into one generic:

```text
AI accuracy
```

Each has different meaning.

---

# 2. Evaluation Layers

## Layer E1 — Person Detector

Evaluate:

- detection quality;
- misses;
- false detections;
- latency;
- compatibility with tracking.

## Layer E2 — Tracker

Evaluate:

- track continuity;
- ID switches;
- track loss;
- operational impact on rules;
- latency overhead.

## Layer E3 — Violence/Fighting Model

Evaluate:

- classification performance;
- threshold behavior;
- false positives;
- false negatives;
- temporal-window behavior;
- inference latency.

## Layer E4 — Deterministic Rule Engine

Evaluate:

- intrusion;
- loitering;
- crowd threshold;
- duplicate suppression.

## Layer E5 — End-to-End System

Evaluate:

- event creation;
- evidence;
- persistence;
- alert delivery;
- acknowledgement;
- recovery/failure behavior.

---

# 3. Model Registry Requirement

Every evaluated model must have:

```text
model_id
model_version_id
```

from the database/model registry design.

Example placeholder:

```yaml
model_id: "MODEL-DET-TBD"
model_version_id: "MODEL-DET-TBD-V1"
```

Do not use generic names such as:

```text
best_model
final_model
latest
```

as the only identity.

---

# 4. Model Card Master Template

Every deployed/evaluated model shall have a completed card.

```yaml
model_card:
  model_id: "TBD"
  model_version_id: "TBD"
  status: "DRAFT"

  task:
    name: "TBD"
    formulation: "TBD"

  source:
    architecture: "TBD"
    implementation_source: "TBD"
    pretrained_weights_source: "TBD"
    license: "TBD"

  provenance:
    trained_by_team: "TBD"
    fine_tuned_by_team: "TBD"
    base_weights: "TBD"
    training_commit: "TBD"
    experiment_id: "TBD"

  data:
    training_dataset_id: "TBD"
    validation_dataset_id: "TBD"
    test_dataset_id: "TBD"
    split_manifest: "TBD"
    split_manifest_sha256: "TBD"

  preprocessing:
    input_shape: "TBD"
    normalization: "TBD"
    temporal_window: "TBD"
    frame_sampling: "TBD"

  thresholds:
    inference_threshold: "TBD"
    event_threshold: "TBD"
    calibration_method: "TBD"

  metrics:
    status: "NOT_YET_MEASURED"

  performance:
    hardware: "TBD"
    latency: "NOT_YET_MEASURED"
    fps: "NOT_YET_MEASURED"

  limitations:
    - "TBD"

  approval:
    owner: "TBD"
    reviewer: "TBD"
    date: "TBD"
```

---

# 5. Person Detector Model Card

## 5.1 Required identity fields

```text
Model family
Exact model variant
Weight version
Framework
Framework version
Source URL
License
Pretrained dataset
Sentinel fine-tuning status
Input resolution
Inference device
Precision mode
Detection threshold
```

## 5.2 Required task definition

Task:

```text
detect persons in Sentinel-supported video frames
```

The model may detect additional classes internally, but Sentinel evaluation focuses on person detection unless otherwise stated.

---

# 6. Person Detector Evaluation Dataset

Detector evaluation data may be:

1. formal labeled dataset;
2. Sentinel-relevant manually annotated sample;
3. benchmark dataset.

The evaluation must state which.

## 6.1 Preferred practical strategy

For the short project:

```text
small Sentinel-relevant labeled evaluation set
+
recorded operational clips
```

is acceptable if custom mAP benchmarking is feasible.

If no labeled dataset is created:

- do not fabricate mAP;
- use operational detection statistics and failure analysis.

---

# 7. Detector Ground Truth

Formal detector metrics require ground-truth person boxes.

Ground-truth record should include:

```text
frame_id
camera/video ID
bbox
class = person
annotation source
```

## 7.1 Annotation quality

If team members annotate boxes:

- document tool;
- annotation instructions;
- reviewer;
- ambiguous cases.

---

# 8. Intersection over Union

For predicted box `B_p` and ground-truth box `B_g`:

```text
IoU = area(B_p ∩ B_g) / area(B_p ∪ B_g)
```

IoU measures spatial overlap.

Range:

```text
0 <= IoU <= 1
```

The exact matching threshold must be specified for any precision/recall calculation.

---

# 9. Detector True/False Outcomes

At a defined IoU threshold:

## True Positive

A predicted person box correctly matches an unmatched ground-truth person.

## False Positive

A predicted person box does not match a ground-truth person sufficiently.

## False Negative

A ground-truth person is not detected.

---

# 10. Detector Precision

```text
Precision = TP / (TP + FP)
```

Meaning:

> Of predicted persons, how many were correct?

---

# 11. Detector Recall

```text
Recall = TP / (TP + FN)
```

Meaning:

> Of actual persons, how many were detected?

For surveillance rules, missed persons may be especially important because a missed person cannot generate:

- intrusion;
- loitering;
- crowd count.

---

# 12. Average Precision / mAP

If a formal COCO-style evaluation is performed, report:

```text
AP
mAP@0.5
mAP@0.5:0.95
```

only using a documented implementation.

Do not manually approximate mAP.

---

# 13. Detector Threshold Sweep

Detector confidence threshold shall be calibrated using validation data.

Recommended evaluation table:

| Threshold | Precision | Recall | FP | FN | Tracker stability note |
|---:|---:|---:|---:|---:|---|
| `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |

Do not fill this table until executed.

---

# 14. Detector Threshold Selection Rule

Select threshold based on:

- person recall;
- false detections;
- tracker continuity;
- downstream false events.

The threshold should not be selected solely to maximize one model metric if it harms system behavior.

---

# 15. Detector Operational Scenarios

Test at minimum:

## DET-SC-01 — Single clear person

Expected:

- person detected;
- stable bounding box.

## DET-SC-02 — No person

Expected:

- no person detections;
- no fabricated track.

## DET-SC-03 — Two people

Expected:

- two distinct detections where visually separable.

## DET-SC-04 — Partial occlusion

Observe:

- detection continuity;
- misses.

## DET-SC-05 — Small/distant person

Observe:

- detector limitations.

## DET-SC-06 — Low light

Observe:

- sensitivity to lighting.

---

# 16. Detector Failure Table

Final model card should include observed examples:

| Failure ID | Input scenario | Error type | Likely cause | Downstream effect |
|---|---|---|---|---|
| `TBD` | `TBD` | FN/FP/localization | `TBD` | `TBD` |

---

# 17. Detector Inference Performance

Required:

```text
model load time
steady-state frame inference latency
AI-worker detector-stage latency
processed FPS
```

Do not call source FPS "detector FPS".

---

# 18. Detector Model Card — Current Placeholder

```yaml
model_id: "MODEL-DET-TBD"
model_version_id: "TBD"
status: "DRAFT"

task:
  name: "person_detection"

architecture: "TBD"
weights: "TBD"
license: "TBD"

training:
  sentinel_trained: false
  sentinel_fine_tuned: "TBD"

data:
  evaluation_dataset_id: "TBD"

threshold:
  value: "TBD"
  calibration_status: "NOT_YET_MEASURED"

metrics:
  precision: "NOT_YET_MEASURED"
  recall: "NOT_YET_MEASURED"
  map_50: "NOT_YET_MEASURED"
  map_50_95: "NOT_YET_MEASURED"

performance:
  latency_ms: "NOT_YET_MEASURED"
  processed_fps: "NOT_YET_MEASURED"

approval:
  status: "NOT_APPROVED"
```

---

# 19. Tracker Model / Component Card

A tracker may not be a learned model, but it still requires a component card.

## 19.1 Required fields

```text
tracker name
algorithm
implementation source
version
license
detector dependency
configuration
ReID enabled?
camera-motion compensation?
track buffer
association thresholds
```

Exact configuration fields depend on selected tracker.

---

# 20. Tracker Evaluation Goals

The tracker exists to support Sentinel rules.

Therefore primary questions include:

- Does the same person keep the same track through zone entry?
- Does track survive long enough for loitering?
- Does crossing-person behavior cause severe ID switching?
- Does track fragmentation distort crowd count?

---

# 21. Tracker Formal Metrics

If benchmark evaluation is performed:

## IDF1

Measures identity-consistent detections.

## MOTA

Combines:

- false positives;
- false negatives;
- identity switches.

## HOTA

Balances:

- detection quality;
- association quality.

## ID switches

Counts identity changes across tracks.

Exact definitions/implementation shall follow the selected evaluator.

---

# 22. Tracker Operational Metrics

For Sentinel clips:

```text
track initialization success
track continuity duration
ID-switch count
track-loss count
recovery behavior
rule-impact errors
```

---

# 23. Tracker Test Scenario — Zone Crossing

## TRK-SC-01

Input:

```text
one person walks from outside into restricted zone
```

Expected:

```text
one track remains associated across crossing
```

Failure:

```text
track changes ID exactly at boundary
```

Potential downstream effect:

- duplicate intrusion;
- missed transition.

---

# 24. Tracker Test Scenario — Loitering

## TRK-SC-02

Input:

```text
person remains within zone for controlled duration
```

Expected:

- continuous track;
- timer remains associated.

Failure:

- repeated track resets.

Potential downstream effect:

- missed loitering event.

---

# 25. Tracker Test Scenario — Two-Person Crossing

## TRK-SC-03

Input:

- two people cross paths.

Record:

- ID switches;
- track merges;
- track splits.

---

# 26. Tracker Test Scenario — Occlusion

## TRK-SC-04

Input:

- person temporarily occluded.

Record:

- lost duration;
- recovered same/new ID;
- effect on loitering state.

---

# 27. Tracker Test Scenario — Crowd

## TRK-SC-05

Input:

- multiple visible people.

Record:

- active-track count vs visually observed count;
- duplicate tracks;
- missing tracks.

---

# 28. Tracker Configuration Evaluation Table

| Config ID | Tracker | Key settings | ID switches | Track losses | Rule impact | Latency |
|---|---|---|---:|---:|---|---:|
| `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |

---

# 29. Tracker Card — Current Placeholder

```yaml
component_id: "TRACKER-TBD"
status: "DRAFT"

algorithm: "TBD"
implementation: "TBD"
version: "TBD"
license: "TBD"

configuration:
  status: "TBD"

evaluation:
  mot17_used: false
  sentinel_clips_used: "TBD"

metrics:
  idf1: "NOT_YET_MEASURED"
  mota: "NOT_YET_MEASURED"
  hota: "NOT_YET_MEASURED"
  id_switches: "NOT_YET_MEASURED"
  operational_track_loss: "NOT_YET_MEASURED"

latency:
  overhead_ms: "NOT_YET_MEASURED"

approval:
  status: "NOT_APPROVED"
```

---

# 30. Violence/Fighting Model Card

This is the primary learned Sentinel-specific event model.

## 30.1 Required task statement

The final card must explicitly define whether the model predicts:

```text
fighting
```

or:

```text
general violence
```

or:

```text
anomaly
```

These are not equivalent.

---

# 31. Violence Model Input Definition

The final model card shall state:

```text
input modality
frame count
sampling FPS
window duration
stride
resize/crop
normalization
audio usage
```

No field may remain vague.

---

# 32. Violence Model Output Definition

The final card shall state:

```text
output classes
score range
score semantics
event threshold
temporal smoothing
```

Do not call a raw logit or uncalibrated score a probability.

---

# 33. Violence Evaluation Dataset

Must reference exact registry ID.

Example placeholder:

```text
DATA-DERIVED-XD-FIGHTING-BINARY-V1
```

Actual ID: `TBD`.

The model card shall also state:

```text
train samples
validation samples
test samples
class counts
split manifest hash
```

All values must come from the dataset registry.

---

# 34. Violence Confusion Matrix

For binary formulation:

| | Predicted Violence | Predicted Non-Violence |
|---|---:|---:|
| Actual Violence | TP | FN |
| Actual Non-Violence | FP | TN |

Every confusion matrix must identify:

- positive class;
- negative class;
- sample unit.

Sample unit may be:

```text
video
clip
temporal window
```

and must be explicit.

---

# 35. Violence Accuracy

```text
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

Accuracy may be misleading under class imbalance.

Therefore it shall not be the only reported violence metric.

---

# 36. Violence Precision

```text
Precision = TP / (TP + FP)
```

Operational interpretation:

> Of samples flagged violence, how many are actually violence according to the evaluation labels?

Low precision may lead to high operator alert burden.

---

# 37. Violence Recall

```text
Recall = TP / (TP + FN)
```

Operational interpretation:

> Of labeled violence samples, how many were detected?

Low recall means violence events are missed.

---

# 38. Violence F1 Score

```text
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

Useful when balancing precision and recall.

---

# 39. Specificity

```text
Specificity = TN / (TN + FP)
```

Useful for understanding false-alert tendency on negative samples.

---

# 40. False Positive Rate

```text
FPR = FP / (FP + TN)
```

---

# 41. False Negative Rate

```text
FNR = FN / (FN + TP)
```

---

# 42. ROC-AUC

May be reported if:

- a continuous model score exists;
- evaluation implementation is documented.

Do not report ROC-AUC from binary class labels only.

---

# 43. Precision-Recall AUC

PR-AUC may be especially informative for imbalanced positive classes.

If reported:

- implementation;
- positive class;
- sample unit;

must be recorded.

---

# 44. Violence Threshold Calibration

Final threshold shall not be chosen on final test data.

Recommended:

```text
train model
→ validation score sweep
→ choose threshold
→ freeze
→ final test
```

---

# 45. Threshold Sweep Table

| Threshold | Precision | Recall | F1 | FPR | FN | FP |
|---:|---:|---:|---:|---:|---:|---:|
| `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |

---

# 46. Threshold Selection Rationale

The final card shall document why the threshold was selected.

Possible rationale:

- maximize validation F1;
- target higher recall;
- reduce false alerts;
- balance operator burden.

Do not write:

> 0.5 was used because that is standard.

unless justified by the model's actual score semantics.

---

# 47. Temporal Smoothing Evaluation

If smoothing is used, compare:

```text
single-window
vs
smoothed criterion
```

Measure:

- event stability;
- latency;
- FP reduction;
- FN increase.

---

# 48. Violence Error Analysis

Review representative:

- false positives;
- false negatives;
- uncertain/ambiguous samples.

For each:

```text
sample ID
ground-truth label
prediction
score
threshold
observed visual context
possible cause
```

---

# 49. Violence False Positive Categories

Potential categories after actual observation:

- sports/play;
- hugging;
- crowd movement;
- camera shake;
- low-light motion;
- compression artifacts;
- non-fighting aggressive motion.

Do not list a cause as observed unless supported by an actual error example.

---

# 50. Violence False Negative Categories

Potential:

- subtle fighting;
- small actors;
- distant camera;
- brief action;
- occlusion;
- low frame sampling.

Again, actual model card must record observed cases.

---

# 51. Violence Model Card — Frozen Selected Model

```yaml
model_id: "MODEL-VIO-BIGRU-ATTN-XD"
model_version_id: "6d22f83d-17f8-5ecf-9f0f-246fa326ec72"
version_label: "MODEL-VIO-BIGRU-ATTN-XD-V1"
status: "APPROVED_FOR_REPORTING"

task:
  formulation: "binary Fighting vs Normal temporal video classification"
  positive_class: "Fighting"
  negative_class: "Normal"
  label_granularity: "video-level weak label"

architecture:
  experiment_id: "EXP-VIO-TEMPORAL-001"
  name: "BiGRU + Temporal Attention"
  input_reference_shape: "(T, 5, 2048)"
  crop_reduction: "mean across 5 crops"
  temporal_resampling: "deterministic uniform resampling to 64 steps"
  projection_dim: 256
  gru_hidden_per_direction: 128
  bidirectional: true
  attention: "learned Linear(256 -> 1) temporal softmax"
  dropout: 0.25
  parameters: 822530

checkpoint:
  path: "sentinel_temporal/artifacts/best_model.pt"
  sha256: "1fa01d1be82ab3c63d33b4d5f1d5ef4ab2a176d1d2842afc842955ff72896772"
  best_epoch: 3

data:
  feature_dataset_id: "DATA-XD-I3D-FEATURES-V1"
  derived_dataset_id: "DATA-DERIVED-XD-FIGHTING-BINARY-V1"
  train:
    normal: 1636
    fighting: 302
    total: 1938
  validation:
    normal: 410
    fighting: 75
    total: 485
  test:
    normal: 300
    fighting: 107
    total: 407

whole_video_validation:
  threshold: 0.8345891237258911
  precision: 0.9230769231
  recall: 0.8000000000
  f1: 0.8571428571
  accuracy: 0.9587628866
  roc_auc: 0.9558373984
  pr_auc: 0.8909613305
  confusion: {tn: 405, fp: 5, fn: 15, tp: 60}

whole_video_test:
  precision: 0.9569892473
  recall: 0.8317757009
  specificity: 0.9866666667
  f1: 0.8900000000
  accuracy: 0.9459459459
  roc_auc: 0.9815576324
  pr_auc: 0.944877884
  confusion: {tn: 296, fp: 4, fn: 18, tp: 89}

live_policy:
  experiment_id: "EXP-VIO-LIVE-WINDOW-004"
  worker_window: "W1 exact I3D feature step"
  stride_feature_steps: 1
  score_threshold: 0.906
  smoothing: "3 positive scores among the most recent 5"
  selected_on: "validation only"
  official_test_evaluated_once: true

live_policy_test:
  accuracy: 0.911548
  balanced_accuracy: 0.876869
  precision: 0.851485
  positive_video_coverage: 0.803738
  specificity: 0.950000
  f1: 0.826923
  normal_video_false_event_rate: 0.050000
  confusion: {tn: 285, fp: 15, fn: 21, tp: 86}

runtime_qualification:
  raw_video_feature_parity: "PASS"
  persistent_exact_extractor: "PASS"
  final_raw_video_policy_parity: "PASS"
  final_verdict: "PHASE_2J_RAW_VIDEO_TEMPORAL_LIVE_PARITY_CONFIRMED"

approval:
  model_status: "APPROVED_FOR_REPORTING"
  live_policy_status: "FROZEN"
  test_driven_retuning_permitted: false
```

---

# 52. Confusion Matrix Evidence

A final confusion matrix shall be stored as:

- numeric data;
- rendered figure if desired.

Recommended machine-readable artifact:

```text
artifacts/evaluation/<experiment-id>/confusion_matrix.json
```

Example structure:

```json
{
  "labels": ["non_violence", "violence"],
  "matrix": [
    ["TBD", "TBD"],
    ["TBD", "TBD"]
  ]
}
```

Do not manually draw a confusion matrix with invented counts.

---

# 53. Evaluation Artifact Directory

Recommended:

```text
artifacts/
└── evaluation/
    ├── EXP-DET-.../
    ├── EXP-TRK-.../
    └── EXP-VIO-.../
```

Each experiment directory may contain:

```text
config.yaml
metrics.json
predictions.csv
confusion_matrix.json
latency.csv
failure_examples.csv
environment.txt
stdout.log
```

Large/private media should not be committed unless permitted.

---

# 54. Metrics JSON

Recommended:

```json
{
  "experiment_id": "EXP-VIO-TBD",
  "model_version_id": "TBD",
  "dataset_id": "TBD",
  "split_manifest_sha256": "TBD",
  "metrics": {
    "precision": "NOT_YET_MEASURED",
    "recall": "NOT_YET_MEASURED",
    "f1": "NOT_YET_MEASURED"
  }
}
```

---

# 55. Prediction Record

For classification evaluation:

```csv
sample_id,ground_truth,predicted_label,score,threshold,correct
```

For detector:

```csv
frame_id,gt_count,pred_count,tp,fp,fn
```

For tracker:

```csv
sequence_id,id_switches,track_losses,notes
```

---

# 56. Performance Evaluation Environment

Every latency/FPS claim must record environment.

Required:

```text
machine identifier
OS
CPU
RAM
GPU
GPU memory
Python
framework
framework version
CUDA if applicable
model version
input resolution
source FPS
processed FPS
precision mode
```

---

# 57. Hardware Table Template

| Field | Value |
|---|---|
| CPU | `TBD` |
| RAM | `TBD` |
| GPU | `TBD` |
| GPU memory | `TBD` |
| OS | `TBD` |
| Python | `TBD` |
| PyTorch/framework | `TBD` |
| CUDA | `TBD` |
| precision | `TBD` |

---

# 58. Cold Start Measurement

Definition:

```text
worker process start
→ all required models loaded and worker ready
```

Metric:

```text
cold_start_ms
```

If model loading is excluded from runtime inference latency, cold start should be measured separately if operationally relevant.

---

# 59. Steady-State Detector Latency

Definition:

```text
preprocessed frame available
→ detector output available
```

Does not include:

- source decoding;
- tracking;
- backend rules;
- WebSocket.

---

# 60. Tracker Overhead

Definition:

```text
detector output available
→ updated track result available
```

Metric:

```text
tracker_latency_ms
```

---

# 61. Violence Inference Latency

Definition:

```text
preprocessed temporal window available
→ model score/class available
```

Record whether feature extraction is included.

---

# 62. AI Worker Pipeline Latency

Definition:

```text
input accepted by worker
→ structured AI result emitted
```

Includes:

- decode/preprocessing as specified;
- detector/model;
- tracker as applicable;
- serialization.

---

# 63. End-to-End Event Latency

Definition:

```text
event-triggering source observation
→ event visible to connected authorized frontend
```

This is a system metric, not model latency.

It may include:

- model inference;
- rule evaluation;
- persistence;
- real-time update.

---

# 64. Latency Measurement Boundaries

Every latency result shall explicitly state:

```text
start point
end point
included stages
excluded stages
```

Without boundaries, the number is not meaningful.

---

# 65. Repetition

Do not report one run.

Preferred procedure:

1. warm up model;
2. run multiple observations;
3. record each value;
4. report:
   - mean;
   - median;
   - p95 where useful;
   - min/max if useful.

Exact repetition count may be set by test plan.

---

# 66. Mean Latency

```text
mean = sum(latencies) / N
```

Sensitive to outliers.

---

# 67. Median Latency

The middle value after sorting.

Useful for typical performance.

---

# 68. p95 Latency

The 95th percentile indicates high-end latency behavior.

Only report if enough samples exist for percentile interpretation.

---

# 69. FPS Definition

Processed FPS:

```text
number of frames processed by detector / elapsed processing time
```

This is different from:

```text
source video FPS
```

---

# 70. Throughput vs Latency

High FPS does not necessarily imply low event latency if a backlog accumulates.

Therefore record:

- processed FPS;
- queue/backlog behavior;
- latency.

---

# 71. Real-Time Claim Gate

Do not call Sentinel:

```text
real-time
```

as a measured performance claim unless:

- event latency is measured;
- actual hardware/source is documented;
- terminology is defined.

Safer academic phrase before measurement:

> real-time-oriented monitoring workflow

or:

> live event update mechanism

---

# 72. Multi-Stream Performance

No multi-camera scaling claim shall be made unless tested.

If only one source is tested:

```text
tested_stream_count = 1
```

Do not infer performance for:

```text
5
10
100
```

cameras.

---

# 73. Performance Test Matrix

| Test ID | Model/System | Input | Streams | Hardware | Metric |
|---|---|---|---:|---|---|
| `PERF-DET-001` | Detector | `TBD` | 1 | `TBD` | inference latency/FPS |
| `PERF-TRK-001` | Tracker | `TBD` | 1 | `TBD` | overhead |
| `PERF-VIO-001` | Violence | `TBD` | 1 | `TBD` | window inference latency |
| `PERF-E2E-001` | Full system | `TBD` | 1 | `TBD` | event-to-client latency |

---

# 74. System Rule Evaluation

The deterministic rule engine needs its own evaluation.

Model accuracy does not prove rule correctness.

---

# 75. Intrusion Rule Evaluation

Test cases:

| Case | Expected |
|---|---|
| person remains outside | no event |
| person enters once | one event |
| person stays inside | no frame-by-frame duplication |
| person exits and re-enters | behavior per retrigger policy |
| invalid track geometry | no event |
| disabled rule | no event |

---

# 76. Intrusion Rule Metrics

Possible:

```text
scenario pass rate
duplicate event count
missed expected events
unexpected events
```

For controlled scenarios:

```text
expected event count
actual event count
```

is highly interpretable.

---

# 77. Loitering Rule Evaluation

Cases:

- below threshold;
- exactly threshold;
- above threshold;
- exit before threshold;
- temporary track loss;
- sustained presence after event.

---

# 78. Loitering Timer Accuracy

With controlled timestamps, compare:

```text
expected dwell duration
vs
measured dwell duration
```

Do not rely on wall-clock subjective observation.

---

# 79. Crowd Rule Evaluation

Cases:

- count below threshold;
- count equal threshold;
- count above threshold;
- sustained exceedance;
- drop below then re-cross.

---

# 80. Crowd Count Error

For controlled frames/windows:

```text
count_error = predicted_active_count - reference_count
```

Potential aggregate:

```text
mean absolute count error
```

only if sufficient labeled samples exist.

---

# 81. Camera Offline Evaluation

Cases:

- healthy source;
- brief transient interruption;
- sustained failure;
- intentionally disabled source;
- recovery.

Expected:

- disabled ≠ offline;
- sustained offline produces one event episode.

---

# 82. Duplicate Suppression Evaluation

For each event type:

record:

```text
observation count
qualifying-condition duration
expected events
actual events
duplicate events
```

A model producing many positive windows should not imply many operational events.

---

# 83. End-to-End Golden Path Evaluation

Required path:

```text
video
→ person detection
→ tracking
→ restricted-zone rule
→ event persistence
→ frontend notification
→ acknowledgement
→ persisted acknowledgement
```

This is the highest-priority integrated acceptance scenario.

---

# 84. E2E Evidence Record

For golden path, retain:

```text
test ID
video fixture ID
camera config
zone config
rule config
model version
event ID
database evidence
frontend evidence
acknowledgement ID
timestamps
pass/fail
```

---

# 85. End-to-End Pass Criteria

Golden path passes only if:

1. correct event generated;
2. event persisted;
3. event reaches frontend;
4. operator can open it;
5. acknowledgement succeeds;
6. acknowledgement persists;
7. no duplicate event flood occurs.

---

# 86. Failure-Path Evaluation

Required failure scenarios:

- AI worker unavailable;
- malformed worker result;
- missing model artifact;
- evidence storage failure;
- real-time client disconnect;
- database failure where feasible;
- invalid zone/rule configuration.

---

# 87. Worker Failure Acceptance

Expected:

```text
worker unavailable
→ backend remains available for unrelated operations
→ AI-dependent processing degraded
→ no fake negative AI result
```

---

# 88. Evidence Failure Acceptance

Expected:

```text
event exists
evidence status = failed/unavailable
frontend does not claim evidence exists
```

---

# 89. Real-Time Disconnect Acceptance

If WebSocket is baselined:

```text
disconnect
→ UI indicates disconnected
→ reconnect
→ reconcile persisted events
```

---

# 90. Model Selection Comparison

When comparing candidates, use the same:

- dataset;
- split;
- evaluation script;
- hardware where possible;
- threshold-selection policy.

Otherwise comparisons are not controlled.

---

# 91. Candidate Comparison Table — Detector

| Criterion | Detector A | Detector B |
|---|---|---|
| Model/version | `TBD` | `TBD` |
| License | `TBD` | `TBD` |
| Precision | `TBD` | `TBD` |
| Recall | `TBD` | `TBD` |
| mAP | `TBD` | `TBD` |
| Latency | `TBD` | `TBD` |
| FPS | `TBD` | `TBD` |
| Tracker compatibility | `TBD` | `TBD` |
| Integration effort | `TBD` | `TBD` |
| Selected? | `TBD` | `TBD` |

---

# 92. Candidate Comparison Table — Tracker

| Criterion | Tracker A | Tracker B |
|---|---|---|
| Tracker/version | `TBD` | `TBD` |
| License | `TBD` | `TBD` |
| ID switches | `TBD` | `TBD` |
| Track losses | `TBD` | `TBD` |
| Loitering continuity | `TBD` | `TBD` |
| Latency | `TBD` | `TBD` |
| Selected? | `TBD` | `TBD` |

---

# 93. Candidate Comparison Table — Violence

| Criterion | Model A | Model B |
|---|---|---|
| Architecture | `TBD` | `TBD` |
| Dataset | `TBD` | `TBD` |
| Precision | `TBD` | `TBD` |
| Recall | `TBD` | `TBD` |
| F1 | `TBD` | `TBD` |
| Latency | `TBD` | `TBD` |
| Training cost | `TBD` | `TBD` |
| Integration complexity | `TBD` | `TBD` |
| Selected? | `TBD` | `TBD` |

---

# 94. Model Approval Criteria

A model may become:

```text
APPROVED_FOR_DEMO
```

only if:

- model loads reproducibly;
- source/license recorded;
- input/output contract valid;
- evaluation executed;
- failures understood;
- latency measured;
- no critical unresolved integration issue.

---

# 95. Approval for Formal Reporting

Stricter:

```text
APPROVED_FOR_REPORTING
```

requires:

- exact dataset split;
- reproducible metrics;
- final evaluation artifact;
- no known leakage issue;
- model version frozen;
- metric definitions documented;
- reviewer approval.

---

# 96. Evaluation Leakage Gate

If leakage is discovered:

1. mark affected result:
   `INVALIDATED`;
2. fix dataset split;
3. rerun training/evaluation;
4. do not keep old number in final report.

---

# 97. Test-Set Overfitting Gate

If model/threshold repeatedly tuned on final test:

mark:

```text
final_test_integrity = COMPROMISED
```

Then:

- obtain a new holdout if feasible; or
- disclose limitation.

---

# 98. Metric Recalculation Rule

Metrics should be generated by script.

Do not manually calculate final metric tables in a spreadsheet unless independently verified.

Recommended:

```text
scripts/evaluation/evaluate_violence.py
scripts/evaluation/evaluate_detector.py
```

---

# 99. Evaluation Script Requirements

Script should print/save:

```text
model version
dataset ID
split hash
sample count
threshold
metrics
timestamp
software version
```

---

# 100. Evaluation Reproducibility Command

Final model card should include an actual tested command, for example:

```text
python scripts/evaluation/evaluate_violence.py --config ...
```

This is a placeholder pattern.

Do not invent a command before implementation.

---

# 101. Training vs Evaluation Environment

Training hardware and inference/demo hardware may differ.

Record both separately.

Do not report training GPU performance as demo-device inference performance.

---

# 102. External Benchmark Metrics

Published paper numbers may be included only as:

```text
external reference / comparison
```

They shall never be presented as Sentinel results.

Preferred wording:

> The source paper reports X under its own evaluation setup; Sentinel's measured result under the project setup is Y.

Only use if both values are actually sourced/measured.

---

# 103. No Benchmark Cherry-Picking

If comparing external models:

use comparable metric/dataset conditions.

Do not compare:

```text
Model A F1 on Dataset X
```

against:

```text
Model B accuracy on Dataset Y
```

and conclude one is better.

---

# 104. Model Confidence Reporting

Detector/violence scores may be shown in UI if useful.

If shown:

- label score source;
- avoid implying certainty;
- do not call uncalibrated score "probability."

---

# 105. Calibration

Formal probabilistic calibration is optional.

If calibration is not performed:

do not claim score `0.87` means:

```text
87% chance of violence
```

unless model semantics truly support that interpretation.

---

# 106. Event Confidence

There is no default universal:

```text
event confidence
```

because intrusion/loitering/crowd events are rule decisions based on model observations.

If UI needs confidence, the design must define which component's score is shown.

---

# 107. Human Review

Model outputs are support signals.

Final operator workflow should preserve:

- acknowledgement;
- false-positive feedback where implemented;
- evidence review.

---

# 108. Human Feedback Metrics

Optional operational metrics:

```text
percentage of alerts marked false positive
false-positive reasons
acknowledgement rate
```

These are not model ground-truth accuracy unless labels are curated.

---

# 109. Operational False Alert Rate

If measured, define denominator.

Possible:

```text
false alerts / hour
```

or:

```text
false alerts / 100 events
```

Never report:

```text
false alert rate = 2%
```

without defining denominator and labeling method.

---

# 110. Missed Event Rate

Requires a controlled scenario with known expected events.

Example:

```text
missed expected events / expected events
```

This is possible in scripted test clips.

---

# 111. Controlled Scenario Matrix

| Scenario | Expected event | Actual event | Pass |
|---|---|---|---|
| Intrusion positive | 1 | `TBD` | `TBD` |
| Intrusion negative | 0 | `TBD` | `TBD` |
| Loitering positive | 1 | `TBD` | `TBD` |
| Loitering below threshold | 0 | `TBD` | `TBD` |
| Crowd positive | 1 | `TBD` | `TBD` |
| Violence positive | 1 | `TBD` | `TBD` |
| Violence negative | 0 | `TBD` | `TBD` |
| Camera offline | 1 | `TBD` | `TBD` |

---

# 112. Evaluation Sample Unit

Every metric must identify sample unit:

```text
frame
detection
track
video
clip
temporal window
event
```

Do not mix these in one table without labels.

---

# 113. Macro vs Micro Metrics

For multiclass tasks:

- macro averages classes equally;
- micro aggregates individual decisions.

If reported, specify which.

For binary violence, ordinary positive-class precision/recall/F1 may be sufficient.

---

# 114. Confidence Intervals

Optional.

If sample size is small, confidence intervals may be useful.

Do not add statistically sophisticated intervals unless methodology is correct.

The MVP does not require formal confidence intervals.

---

# 115. Statistical Significance

The project does not need significance testing unless comparing models rigorously with enough repeated data.

Do not add p-values merely to make the report look more academic.

---

# 116. Small Test Set Warning

If test set is small:

state limitation explicitly.

Example:

> Metrics are preliminary because the held-out test set contains a limited number of independent source videos.

Do not hide small sample size.

---

# 117. Class Distribution Reporting

Every violence test result should state:

```text
positive count
negative count
```

This helps interpret accuracy and precision.

---

# 118. Dataset Shift Evaluation

Where possible, compare performance across conditions:

- indoor/outdoor;
- high/low light;
- close/distant person;
- dense/sparse scene.

This is optional but useful for limitations.

---

# 119. Error Severity

Not every model error has same operational impact.

Example:

- detector box slightly misaligned but track stable → minor;
- person completely missed at zone entry → severe.

Error analysis may include:

```text
operational impact
```

rather than only model label.

---

# 120. Root-Cause Taxonomy

Suggested final categories:

```text
DETECTOR_FP
DETECTOR_FN
TRACK_ID_SWITCH
TRACK_LOSS
ZONE_CONFIGURATION
RULE_CONFIGURATION
RULE_IMPLEMENTATION
VIOLENCE_FP
VIOLENCE_FN
EVIDENCE_FAILURE
REALTIME_DELIVERY
UNKNOWN
```

Use only after evidence supports classification.

---

# 121. Model Limitations Section

Every final model card must contain limitations.

Examples categories:

- domain shift;
- camera angle;
- lighting;
- occlusion;
- crowd density;
- dataset bias;
- class ambiguity;
- hardware dependence.

Do not use generic:

```text
may sometimes fail
```

without concrete context.

---

# 122. Intended Use

Every model card should define:

```text
intended use
```

Example detector:

> Assist person-based monitoring rules in controlled Sentinel camera streams.

Example violence model:

> Generate a violence/fighting model score for operator-reviewable event generation.

---

# 123. Out-of-Scope Use

Explicitly prohibit unsupported interpretations.

Examples:

- identity recognition;
- criminal intent inference;
- legal judgement;
- autonomous enforcement;
- medical/emergency diagnosis.

---

# 124. Ethical Limitations

Model evaluation does not prove:

- fairness across all populations;
- universal generalization;
- legal reliability;
- identity accuracy.

Do not imply such claims.

---

# 125. Privacy

Evaluation media shall follow dataset registry permissions.

Do not publish:

- restricted clips;
- private CCTV;
- raw participant footage;

in public repositories unless permitted.

---

# 126. Model Card Citation

Each third-party model/dataset should include:

- original paper;
- official implementation/project;
- license source.

Final report references should use original academic sources where available.

---

# 127. Academic Claim Gate

A statement such as:

> The violence model achieved an F1-score of X.

requires:

- actual value X measured;
- exact dataset/split;
- positive class definition;
- threshold;
- model version;
- evaluation script;
- sample count.

---

# 128. Accuracy Claim Gate

Avoid:

> Sentinel AI is 95% accurate.

This is ambiguous.

Preferred:

> On the held-out `DATA-...` test split, violence classification achieved an F1-score of X under threshold Y.

only after measured.

---

# 129. Performance Claim Gate

Avoid:

> Sentinel processes video in real time.

Preferred after measurement:

> On hardware H, detector configuration M processed a median of X frames per second at input resolution R.

---

# 130. Latency Claim Gate

Avoid:

> Alerts are instant.

Preferred:

> Under the documented local test environment, median event-to-client notification latency was X ms over N controlled runs.

---

# 131. Model Selection Decision Record

When a model is selected:

```yaml
decision_id: "MODEL-DEC-..."
selected_model_version_id: "..."
alternatives:
  - "..."
evaluation_basis:
  dataset_id: "..."
  metrics:
    - "..."
  hardware: "..."
rationale: "..."
approved_by:
  - "..."
date: "..."
```

---

# 132. Model Retirement

Retire a model when:

- new version replaces it;
- license issue discovered;
- evaluation invalidated;
- artifact corrupted;
- integration incompatible.

Old events still retain provenance to retired model version.

---

# 133. Model Artifact Integrity

Final artifact should have:

```text
SHA-256
```

stored in model registry.

Evaluation script should verify or at least record the actual artifact identity.

---

# 134. Environment Snapshot

Recommended:

```text
pip freeze
```

or dependency lock file.

Also record:

```text
git commit
```

for final evaluation.

---

# 135. Final Evaluation Freeze

Before final model evaluation:

1. freeze dataset;
2. freeze split;
3. freeze model artifact;
4. freeze threshold;
5. freeze code commit;
6. record environment;
7. execute evaluation;
8. store outputs;
9. review;
10. mark metrics final.

---

# 136. Final Evaluation Checklist — Detector

- [ ] Model ID/version fixed.
- [ ] Weights checksum recorded.
- [ ] Evaluation data fixed.
- [ ] Ground-truth annotation reviewed.
- [ ] Confidence threshold fixed.
- [ ] IoU/matching policy fixed.
- [ ] Precision measured.
- [ ] Recall measured.
- [ ] mAP measured if applicable.
- [ ] Operational clips reviewed.
- [ ] Latency measured.
- [ ] FPS measured.
- [ ] Failure cases documented.
- [ ] Reviewer signs off.

---

# 137. Final Evaluation Checklist — Tracker

- [ ] Tracker/version fixed.
- [ ] Detector dependency fixed.
- [ ] Configuration fixed.
- [ ] Operational scenarios executed.
- [ ] ID switches measured/observed.
- [ ] Track losses measured/observed.
- [ ] Loitering continuity tested.
- [ ] Crowd count impact tested.
- [ ] Formal benchmark performed if claimed.
- [ ] Latency overhead measured.
- [ ] Limitations documented.

---

# 138. Final Evaluation Checklist — Violence

- [ ] Model version fixed.
- [ ] Task definition fixed.
- [ ] Train/val/test dataset IDs fixed.
- [ ] Split hashes fixed.
- [ ] Test set not used for training.
- [ ] Preprocessing fixed.
- [ ] Temporal window fixed.
- [ ] Threshold calibrated on validation data.
- [ ] Confusion matrix generated.
- [ ] Precision measured.
- [ ] Recall measured.
- [ ] F1 measured.
- [ ] Accuracy measured if reported.
- [ ] ROC/PR metrics measured only if valid.
- [ ] False positives reviewed.
- [ ] False negatives reviewed.
- [ ] Inference latency measured.
- [ ] Hardware recorded.
- [ ] Reviewer signs off.

---

# 139. Final Evaluation Checklist — End-to-End System

- [ ] Golden intrusion path passes.
- [ ] Event persisted.
- [ ] Frontend receives alert.
- [ ] Evidence handling verified.
- [ ] Acknowledgement persists.
- [ ] Duplicate suppression verified.
- [ ] Worker failure tested.
- [ ] Evidence failure tested.
- [ ] Real-time disconnect tested if applicable.
- [ ] Event-to-client latency measured.
- [ ] No fake metrics/demo state used.

---

# 140. Model Card Approval Record

Template:

| Field | Value |
|---|---|
| Model ID | `TBD` |
| Model Version | `TBD` |
| Status | `DRAFT` |
| Owner | `TBD` |
| Reviewer | `TBD` |
| Evaluation Date | `TBD` |
| Approved for Demo | `No` |
| Approved for Reporting | `No` |

---

# 141. Current Model Card Summary

As of this draft:

| Component | Model/Algorithm | Status | Metrics |
|---|---|---|---|
| Person detector | `TBD` | `NOT_SELECTED` | `NOT_YET_MEASURED` |
| Tracker | `TBD` | `NOT_SELECTED` | `NOT_YET_MEASURED` |
| Violence/fighting model | `MODEL-VIO-BIGRU-ATTN-XD-V1` | `APPROVED_FOR_REPORTING` | whole-video + frozen live-policy metrics measured |
| Intrusion rule | deterministic | design accepted, semantics partly TBD | `NOT_YET_TESTED` |
| Loitering rule | deterministic | semantics TBD | `NOT_YET_TESTED` |
| Crowd rule | deterministic | counting method TBD | `NOT_YET_TESTED` |
| Camera offline | deterministic health logic | criteria TBD | `NOT_YET_TESTED` |

This table shall be updated as implementation progresses.

---

# 142. Evidence Naming Convention

Recommended:

```text
EVAL-<component>-<date>-<sequence>
```

Examples:

```text
EVAL-DET-202608XX-001
EVAL-TRK-202608XX-001
EVAL-VIO-202608XX-001
EVAL-E2E-202608XX-001
```

---

# 143. Evaluation Report Record

Each final run:

```yaml
evaluation_id: "EVAL-VIO-..."
experiment_id: "EXP-VIO-..."
model_version_id: "..."
dataset_id: "..."
split_manifest_sha256: "..."
evaluation_commit: "..."
environment_file: "..."
metrics_file: "..."
predictions_file: "..."
review_status: "..."
```

---

# 144. Metrics Versioning

If evaluation implementation changes materially:

- create new evaluation ID;
- do not overwrite old output without explanation.

Example changes:

- different label mapping;
- different IoU policy;
- different threshold;
- bug fix in evaluator.

---

# 145. Evaluation Bug Procedure

If a metric bug is found:

1. mark old result `INVALIDATED`;
2. record issue;
3. fix evaluator;
4. rerun;
5. update model card;
6. update report/presentation if necessary.

Never silently replace a number.

---

# 146. Reproducibility Review

Another teammate should be able to answer:

```text
Which model?
Which exact artifact?
Which exact test data?
Which script?
Which command?
Which threshold?
Which environment?
Where is output?
```

If not, evaluation is incomplete.

---

# 147. External Reproducibility

Because source datasets may not be redistributable, external reproducibility may rely on:

- official acquisition instructions;
- checksums;
- manifests;
- scripts;
- config;
- model registry.

This is acceptable.

---

# 148. Model Card vs Final Report

The model card is detailed engineering evidence.

The final report may summarize:

- model choice;
- dataset;
- key metrics;
- limitations.

The report shall not introduce new metric values absent from the model card/evaluation artifacts.

---

# 149. Presentation Rules

Slides may round metrics for readability.

Example:

```text
F1 = 0.8732
```

may appear as:

```text
F1 = 0.87
```

only if original value exists and rounding is mathematically correct.

Do not exaggerate through rounding.

---

# 150. Visualization Rules

Appropriate figures:

- confusion matrix;
- precision-recall curve;
- threshold vs F1;
- detector precision/recall;
- latency distribution;
- event-count test table.

Every chart must state:

- dataset;
- model;
- metric;
- units.

---

# 151. Confusion Matrix Labeling

Do not show unlabeled axes.

Required:

```text
Actual
Predicted
class names
counts
```

Optional normalized percentages may accompany raw counts.

---

# 152. ROC/PR Curve Provenance

Curve generation script and underlying prediction file should be retained.

Do not recreate curves manually.

---

# 153. Threshold Plot

Useful:

```text
threshold
vs
precision
recall
F1
```

This makes event-threshold rationale visible.

---

# 154. Latency Plot

Potential:

- histogram;
- box plot;
- percentile table.

Do not use chart if only one latency observation exists.

---

# 155. Failure Example Visualization

For detector failures, screenshots may show:

- missed person;
- false box;
- occlusion.

For violence failures, use only media that can be displayed ethically/legally.

---

# 156. No Sensitive Media in Public Artifacts

If violence dataset terms restrict redistribution:

- do not place frames in public report/repo;
- use descriptions, aggregate metrics, or team-controlled examples.

---

# 157. Model Explainability

Advanced explainability methods are optional.

Not required:

- Grad-CAM;
- SHAP;
- attention maps.

Only add if they answer a real evaluation question.

Do not use decorative explainability visualizations without interpretation.

---

# 158. Detector Localization Review

Even when detection is correct, bounding-box quality affects zone logic.

Therefore inspect:

- bottom-center placement;
- box truncation;
- person partially outside frame.

---

# 159. Zone Boundary Sensitivity

A person near polygon edge may produce event instability due to box jitter.

Evaluation should include at least one boundary-adjacent scenario once intrusion semantics are fixed.

---

# 160. Hysteresis / Smoothing

If rule/event logic adds hysteresis:

record its effect separately from model score.

Do not attribute rule smoothing improvement to the model itself.

---

# 161. Crowd Counting Evaluation

If active-track count is selected:

evaluate:

```text
reference people in zone
vs
active qualifying tracks
```

Potential metrics:

```text
MAE
exact count accuracy
threshold-event accuracy
```

Only calculate with labeled count data.

---

# 162. Count MAE

```text
MAE = (1/N) * Σ |predicted_count_i - actual_count_i|
```

Useful if enough sampled frames/scenes are annotated.

---

# 163. Threshold-Event Accuracy

For crowd rule, the operational question may be binary:

```text
threshold met?
```

This may be more important than exact count MAE.

---

# 164. Loitering Temporal Error

Potential metric:

```text
absolute error in detected threshold-crossing time
```

Requires controlled timing.

Useful for verifying the rule/timestamp pipeline.

---

# 165. Offline Detection Delay

Potential system metric:

```text
offline event time - actual source failure time
```

This should reflect configured policy.

No target is baselined yet.

---

# 166. Event-to-Client Latency Decomposition

Possible measurements:

```text
T0 source event condition
T1 AI result emitted
T2 backend event persisted
T3 real-time message emitted
T4 frontend receives
T5 frontend renders
```

Then:

```text
AI latency = T1 - T0
backend event latency = T2 - T1
delivery latency = T4 - T3
render latency = T5 - T4
end-to-end = T5 - T0
```

Exact timestamps collected depend on implementation.

---

# 167. Clock Synchronization

If components run on different machines, timestamp comparison requires synchronized clocks.

For local single-machine MVP this is simpler.

If distributed, document clock-sync assumptions.

---

# 168. Measurement Instrumentation

Prefer monotonic timers for duration measurement within one process.

Wall-clock timestamps are suitable for event occurrence/audit but can be affected by clock adjustments.

---

# 169. Python Timing

Potential implementation:

```python
from time import perf_counter

start = perf_counter()
# operation
elapsed_s = perf_counter() - start
```

This is an example, not a mandated implementation.

---

# 170. Warm-Up Bias

First inference can be slower due to:

- model initialization;
- kernel compilation;
- memory allocation.

Therefore final steady-state benchmarks should distinguish warm-up.

---

# 171. Data-Loader Bias

Training throughput is not the same as inference throughput.

Do not report data-loader batch speed as model FPS.

---

# 172. Batch Size

Inference batch size must be recorded.

Real-time camera processing may use:

```text
batch size = 1
```

while offline evaluation may use larger batches.

Performance comparisons must account for this.

---

# 173. Video Decode Cost

If AI pipeline latency includes decode:

state so.

A model-only benchmark that excludes decode may not represent system latency.

---

# 174. Evidence Generation Cost

Evidence clip encoding may affect event workflow latency.

Measure separately if it blocks notification.

Preferred architecture should allow event notification without waiting for full clip encoding if design permits.

---

# 175. Performance Under Evidence Load

Optional test:

```text
event generated
+ snapshot/clip encoding
```

observe whether API remains responsive.

---

# 176. Database Impact

Event persistence latency can be measured independently.

Do not blame model if DB dominates event delivery.

---

# 177. WebSocket Impact

Real-time client delivery should be tested independently from model latency.

---

# 178. Demo Hardware Qualification

The final demo should use the same class of hardware on which the integrated system was tested.

If presentation machine differs:

rerun smoke/performance tests.

---

# 179. CPU Fallback

If GPU is unavailable and CPU fallback is supported:

evaluate CPU separately.

Do not combine GPU and CPU metrics.

---

# 180. Model Comparison Hardware Rule

Compare candidate models on same hardware/configuration where possible.

If not, mark:

```text
NOT_DIRECTLY_COMPARABLE
```

---

# 181. Dataset Comparison Rule

Two models evaluated on different datasets are not directly comparable by raw metrics.

---

# 182. Task Comparison Rule

General violence detection and fighting-only detection are not equivalent tasks.

Metrics cannot be compared without context.

---

# 183. Reporting External Dataset Size

If citing original dataset size:

label:

```text
authors report
```

If reporting local Sentinel subset:

label:

```text
Sentinel used
```

---

# 184. Evaluation Data Table Template

| Dataset ID | Role | Sample unit | Samples | Positives | Negatives | Split hash |
|---|---|---|---:|---:|---:|---|
| `TBD` | TEST | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |

---

# 185. Final Metric Table Template — Detector

| Metric | Value | Status |
|---|---:|---|
| Precision | `NOT_YET_MEASURED` | Draft |
| Recall | `NOT_YET_MEASURED` | Draft |
| mAP@0.5 | `NOT_YET_MEASURED` | Draft |
| mAP@0.5:0.95 | `NOT_YET_MEASURED` | Draft |
| Median latency | `NOT_YET_MEASURED` | Draft |
| Processed FPS | `NOT_YET_MEASURED` | Draft |

---

# 186. Final Metric Table Template — Tracker

| Metric | Value | Status |
|---|---:|---|
| IDF1 | `NOT_YET_MEASURED` | Draft |
| MOTA | `NOT_YET_MEASURED` | Draft |
| HOTA | `NOT_YET_MEASURED` | Draft |
| ID switches | `NOT_YET_MEASURED` | Draft |
| Track losses | `NOT_YET_MEASURED` | Draft |
| Median overhead | `NOT_YET_MEASURED` | Draft |

---

# 187. Final Metric Table — Violence

| Metric | Value | Status |
|---|---:|---|
| Accuracy | `0.911548` | Final live-policy TEST |
| Precision | `0.851485` | Final live-policy TEST |
| Recall / positive-video coverage | `0.803738` | Final live-policy TEST; weak video-level labels |
| F1 | `0.826923` | Final live-policy TEST |
| Specificity | `0.950000` | Final live-policy TEST |
| ROC-AUC | `0.981557632` | Frozen whole-video temporal TEST |
| PR-AUC | `0.944877884` | Frozen whole-video temporal TEST |
| Runtime | persistent exact extractor ≈ `7.15–7.43x` realtime on two qualification fixtures | Fixture benchmark, not full system latency |

---

# 188. Final Metric Table Template — End-to-End

| Metric | Value | Status |
|---|---:|---|
| Golden intrusion scenario | `NOT_YET_TESTED` | Draft |
| Duplicate events | `NOT_YET_MEASURED` | Draft |
| Event-to-client median latency | `NOT_YET_MEASURED` | Draft |
| Event-to-client p95 latency | `NOT_YET_MEASURED` | Draft |
| Evidence generation success | `NOT_YET_MEASURED` | Draft |
| Acknowledgement persistence | `NOT_YET_TESTED` | Draft |

---

# 189. Model Card File Organization

Recommended future files:

```text
models/registry/
├── detector_model_card.yaml
├── tracker_card.yaml
└── violence_model_card.yaml
```

This Markdown document defines the schema/standards.

Machine-readable cards may be added later.

---

# 190. Model Card Change Control

If a deployed parameter changes:

- threshold;
- input size;
- weights;
- tracker config;
- temporal window;

update model card version.

Material changes may require new model version.

---

# 191. When New Model Version Is Required

Create new version when:

- weights change;
- fine-tuning changes;
- architecture changes;
- preprocessing materially changes;
- output class mapping changes.

Threshold-only changes may be model-policy/config version rather than model binary version, but must still be traceable.

---

# 192. Threshold Versioning

For violence, event threshold belongs to deployment policy.

Record:

```text
model version
+
threshold
+
policy version
```

This matters because the same model can yield different event behavior under different thresholds.

---

# 193. Detector Threshold Versioning

Similarly, detector threshold affects downstream rules.

Record it in deployed config/model card.

---

# 194. Tracker Config Versioning

Tracker thresholds/buffer may materially affect loitering.

Record selected configuration.

---

# 195. Model Card Reviewer Questions

Reviewer should ask:

1. What exact model is this?
2. Where did weights come from?
3. What license applies?
4. Was it fine-tuned?
5. On what exact data?
6. What was the test split?
7. Was threshold tuned on validation?
8. Are metrics reproducible?
9. What hardware was used?
10. What are common failure cases?
11. What claims are valid?
12. What claims are not valid?

---

# 196. AI Evaluation Risk Register

| Risk | Impact | Mitigation |
|---|---:|---|
| Test leakage | Critical | split manifest + grouping |
| Fabricated/copied metric | Critical | evidence gate |
| Model version ambiguity | High | registry/checksum |
| Threshold tuned on test | High | validation-only calibration |
| Small evaluation set | High | disclose limitation |
| Hardware mismatch | Medium | record environment |
| Inference benchmark excludes major cost | Medium | define boundaries |
| Tracker metric not relevant to rules | Medium | operational clips |
| Dataset task mismatch | High | explicit task definition |
| Score misrepresented as probability | High | score semantics |
| Demo fixture included in training | High | separate registry roles |

---

# 197. Evaluation Anti-Patterns

## Anti-pattern A — "Accuracy = 95%"

No dataset, split, task, sample count.

Rejected.

## Anti-pattern B — Paper metric copied into Sentinel table

Rejected.

## Anti-pattern C — One easy demo video used as test set

Insufficient for general model claims.

## Anti-pattern D — Test set used to choose threshold

Compromised final holdout.

## Anti-pattern E — Source video FPS reported as model FPS

Incorrect.

## Anti-pattern F — Model score called probability without calibration

Incorrect.

## Anti-pattern G — Detector works visually, therefore model is "100% accurate"

Rejected.

---

# 198. Evaluation Evidence Chain

Every final number should trace:

```text
final report metric
→ model card
→ evaluation ID
→ metrics artifact
→ prediction artifact
→ model version
→ experiment
→ test dataset ID
→ split manifest hash
→ raw dataset provenance
```

---

# 199. SRS Traceability

| Evaluation area | SRS requirements |
|---|---|
| model identity | MLR-MOD-001/002 |
| dataset linkage | MLR-DATA-* |
| detector evaluation | MLR-DET-002/003 |
| tracker evaluation | MLR-TRK-002 |
| violence baseline | MLR-VIO-003 |
| violence metrics | MLR-VIO-004/005/006 |
| latency | MLR-INF-003 |
| reproducibility | MLR-EXP-* |
| performance claims | NFR-ACAD-001 |
| implementation disclosure | NFR-ACAD-002 |
| end-to-end test | NFR-TEST-003 |
| privacy | NFR-PRIV-* |

---

# 200. Use-Case Traceability

| Evaluation | Use Case |
|---|---|
| detector/tracker | UC-AI-001 |
| violence model | UC-AI-002 |
| intrusion operational test | UC-EVT-001 |
| loitering operational test | UC-EVT-002 |
| crowd operational test | UC-EVT-003 |
| violence event integration | UC-EVT-004 |
| camera offline | UC-EVT-005 |
| acknowledgement | UC-EVT-006 |
| worker failure | UC-SYS-001 |
| malformed result | UC-SYS-002 |
| deterministic replay | UC-SYS-005 |

---

# 201. Immediate Evaluation Work Order

After model/data decisions:

```text
1. create controlled intrusion fixture
2. evaluate detector qualitatively/quantitatively
3. evaluate tracker continuity
4. integrate intrusion vertical slice
5. measure detector/tracker latency
6. establish violence baseline
7. calibrate violence threshold on validation
8. run held-out violence test
9. record confusion matrix/error examples
10. integrate violence event
11. measure end-to-end event latency
12. complete model cards
13. approve metrics for reporting
```

---

# 202. Current Open Evaluation Decisions

| ID | Decision | Status |
|---|---|---|
| EVAL-OD-001 | Detector evaluation dataset | `TBD` |
| EVAL-OD-002 | Detector IoU matching threshold | `TBD` |
| EVAL-OD-003 | Detector confidence threshold | `TBD` |
| EVAL-OD-004 | Tracker formal benchmark required? | `TBD` |
| EVAL-OD-005 | Tracker operational test set | `TBD` |
| EVAL-OD-006 | Violence task formulation | `TBD` |
| EVAL-OD-007 | Violence final test dataset | `TBD` |
| EVAL-OD-008 | Violence threshold metric/rationale | `TBD` |
| EVAL-OD-009 | Temporal smoothing evaluation | `TBD` |
| EVAL-OD-010 | Performance benchmark repetition count | `TBD` |
| EVAL-OD-011 | Demo hardware | `TBD` |
| EVAL-OD-012 | Event-to-client latency instrumentation | `TBD` |
| EVAL-OD-013 | Whether p95 is reported | `TBD` |
| EVAL-OD-014 | Whether ROC/PR-AUC are meaningful | `TBD` |
| EVAL-OD-015 | Whether formal crowd count MAE is needed | `TBD` |

---

# 203. Baseline Checklist

Before changing this document to `BASELINED`:

- [ ] Model card schema accepted.
- [ ] Measurement status vocabulary accepted.
- [ ] Detector metrics accepted.
- [ ] Tracker operational evaluation accepted.
- [ ] Violence metric set accepted.
- [ ] Threshold calibration policy accepted.
- [ ] Test-set protection accepted.
- [ ] Latency boundaries accepted.
- [ ] FPS definition accepted.
- [ ] Hardware recording fields accepted.
- [ ] End-to-end event latency definition accepted.
- [ ] Root-cause analysis taxonomy accepted.
- [ ] Approval gates accepted.
- [ ] No unmeasured metric is represented as actual.
- [ ] Final report claim rules accepted.

---

# 204. AI Assistant Rules

An AI assistant shall never:

1. invent model accuracy;
2. invent precision/recall/F1;
3. invent mAP;
4. invent latency;
5. invent FPS;
6. copy source-paper metrics into Sentinel result fields;
7. claim a metric is final without evaluation artifact;
8. alter a test split silently;
9. choose threshold using final test data without disclosure;
10. label a raw score as probability without evidence;
11. claim "real-time" without measured context;
12. claim model trained from scratch when pretrained weights were used;
13. claim Sentinel used a dataset not active in the registry;
14. replace `NOT_YET_MEASURED` with plausible values;
15. mark a model `APPROVED_FOR_REPORTING` without review evidence.

---

# 205. Final Model Evaluation Rule

> **A model result is not a project fact until it is reproducible and traceable.**
>
> Sentinel AI shall only report metrics that can be reconstructed through:
>
> ```text
> model version
> → exact artifact
> → exact dataset
> → exact split
> → exact threshold
> → exact evaluation code
> → exact environment
> → stored output
> ```
>
> Until that chain exists, the correct value is:
>
> ```text
> NOT_YET_MEASURED
> ```
>
> This rule applies equally to:
>
> - detector precision;
> - tracking quality;
> - violence F1;
> - inference latency;
> - FPS;
> - event-to-client latency;
> - false-alert rates.
>
> The academic quality of Sentinel AI depends on being able to distinguish:
>
> **what was designed, what was implemented, what was tested, and what was actually measured.**


---

# 106. Violence Evaluation Evidence Update — 2026-09-12

## 106.1 Live-policy selection discipline

Selection sequence:

```text
freeze model
→ reproduce validation baseline
→ compare live window/smoothing structures on VALIDATION
→ freeze W1 / stride 1 / 3-of-5
→ calibrate live threshold on VALIDATION
→ freeze threshold 0.906
→ evaluate official TEST exactly once
→ prohibit further TEST-driven tuning
```

This process satisfies the requirement that the final threshold shall not be
selected on final TEST data.

## 106.2 Validation-selected live operating point

At threshold `0.906`:

```text
validation confusion:
TN=381 FP=29 FN=16 TP=59

precision                = 0.670455
positive-video coverage  = 0.786667
F1                       = 0.723926
Normal-video false-event = 0.070732
```

Threshold `0.940` had a slightly higher validation F1 but reduced coverage to
`0.72`; it was deliberately not selected because the system is a safety-alert
application and the 0.906 operating point retained substantially more positive
coverage.

## 106.3 Final held-out live result

One-time official TEST:

```text
TN=285 FP=15 FN=21 TP=86

precision                = 0.851485
positive-video coverage  = 0.803738
F1                       = 0.826923
accuracy                 = 0.911548
balanced accuracy        = 0.876869
specificity              = 0.950000
Normal-video false-event = 0.050000
```

No further threshold/window tuning is permitted from these TEST results.

## 106.4 Runtime qualification evidence

Feature-level exact-pipeline reproduction:

```text
Normal cosine    = 0.999999960759
Normal MAE       = 4.958858e-05
Fighting cosine  = 0.999999910273
Fighting MAE     = 6.852958e-05
```

Final temporal live-policy parity over regenerated raw-video features:

```text
raw threshold flags match = true
3-of-5 flags match        = true
final event decision      = true
fixtures confirmed        = 2 / 2
```

The qualified runtime therefore reproduces the selected model behavior from raw
MP4 through final live-policy scoring on the controlled compatibility fixtures.

Full application event persistence/alert-delivery performance remains a separate
system-level evaluation item.

See `19-violence-model-and-runtime-qualification.md`.
