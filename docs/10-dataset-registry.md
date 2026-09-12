---
title: "Sentinel AI — Dataset Registry"
document_id: "SEN-DATA-REG"
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
  - "datasets actually used by Sentinel AI"
  - "dataset version identity"
  - "acquired file inventory"
  - "checksums"
  - "train validation test splits"
  - "derived subsets"
  - "preprocessing provenance"
  - "experiment-to-dataset linkage"
  - "dataset status and eligibility"
---

# Sentinel AI — Dataset Registry

> **Document purpose**
>
> This document is the authoritative registry of the **exact data actually acquired, prepared, split, evaluated, or used by Sentinel AI**.
>
> It is intentionally different from:
>
> `09-dataset-acquisition.md`
>
> which explains where datasets may be obtained.
>
> This registry answers:
>
> - What exact dataset did Sentinel AI use?
> - Was it actually acquired?
> - Which files were obtained?
> - What are their checksums?
> - What role did the dataset play?
> - Which train/validation/test split was used?
> - Which files belong to each split?
> - Was the dataset modified?
> - Which preprocessing script produced the final training data?
> - Which experiment used it?
> - Which model artifact was trained/evaluated from it?
> - What license/terms status was actually reviewed?
> - What limitations affect interpretation?
>
> **No field in this registry shall be populated from memory, assumption, or copied benchmark claims.**
>
> If a value has not been verified, it shall remain:
>
> `TBD`
>
> or:
>
> `NOT_YET_MEASURED`

---

# 0. Document Control

## 0.1 Authority

After baseline approval, this document is authoritative for actual project dataset use.

It is subordinate to:

1. `PROJECT_HANDBOOK.md`
2. `02-srs.md`
3. `08-ai-ml-design.md`
4. `09-dataset-acquisition.md`
5. accepted ADRs

Model result interpretation shall rely on this registry plus:

- experiment records;
- `11-model-card-and-evaluation.md`.

## 0.2 Registry rule

A dataset may be discussed elsewhere without being used.

Only a dataset with status:

```text
ACQUIRED
REGISTERED
ACTIVE
```

as applicable in this document may be treated as actual Sentinel data.

## 0.3 Dataset lifecycle statuses

| Status | Meaning |
|---|---|
| `CANDIDATE` | Under consideration |
| `NOT_YET_ACQUIRED` | Identified but not downloaded/obtained |
| `ACQUISITION_IN_PROGRESS` | Retrieval started |
| `ACQUIRED_UNVERIFIED` | Files obtained but not checksum/structure verified |
| `ACQUIRED_VERIFIED` | Files obtained and integrity recorded |
| `PREPROCESSING` | Being transformed |
| `REGISTERED` | Exact dataset identity and files recorded |
| `ACTIVE` | Used by at least one current experiment/system workflow |
| `EVALUATION_ONLY` | Used only for evaluation/benchmarking |
| `PRETRAINED_PROVENANCE_ONLY` | Not locally used as training/evaluation data; recorded because external weights were trained on it |
| `REJECTED_FOR_CURRENT_PLAN` | Explicitly not used |
| `RETIRED` | Previously used but no longer active |
| `INVALIDATED` | Data cannot be trusted for reported results |

## 0.4 Usage-role vocabulary

A dataset may have one or more roles:

```text
TRAIN
VALIDATION
TEST
BENCHMARK
DEMO_FIXTURE
SYSTEM_INTEGRATION_TEST
PRETRAINED_PROVENANCE
CALIBRATION
ERROR_ANALYSIS
```

## 0.5 Critical rule

A dataset marked:

```text
NOT_YET_ACQUIRED
```

shall not have fabricated:

- file counts;
- checksums;
- local paths;
- split counts;
- duration;
- derived subset sizes.

---

# 1. Current Registry Summary

As of 2026-09-12, the XD-Violence-derived RGB I3D feature corpus and the
strict Fighting-vs-Normal derived split have been acquired, structurally
verified, and used in frozen Sentinel experiments.

The complete original XD-Violence raw-video corpus is **not** claimed as fully
acquired by Sentinel. Raw MP4 acquisition is limited to controlled compatibility
fixtures used to qualify the exact feature-extraction path.

| Dataset ID | Dataset | Intended role | Current status |
|---|---|---|---|
| `DATA-SENT-DEMO-V1` | Team-controlled Sentinel demo/test videos | integration/system testing | `NOT_YET_REGISTERED` |
| `DATA-XD-VIOLENCE-V1` | XD-Violence parent dataset | provenance + limited raw compatibility fixtures | `ACQUISITION_IN_PROGRESS` |
| `DATA-XD-I3D-FEATURES-V1` | XD-Violence RGB I3D feature corpus | model development/evaluation | `ACTIVE` |
| `DATA-DERIVED-XD-FIGHTING-BINARY-V1` | Strict Fighting vs Normal split | TRAIN / VALIDATION / TEST | `ACTIVE` |
| `DATA-UCF-CRIME-V1` | UCF-Crime | secondary violence candidate | `NOT_YET_ACQUIRED` |
| `DATA-MOT17-V1` | MOT17 | optional tracking evaluation | `NOT_YET_ACQUIRED` |
| `DATA-COCO-2017` | COCO 2017 | pretrained detector provenance / optional fine-tuning | `PRETRAINED_PROVENANCE_ONLY` |
| `DATA-RWF-2000-V1` | RWF-2000 | violence candidate | `REJECTED_FOR_CURRENT_PLAN` |

This table must be updated immediately when acquisition/use changes.

---

# 2. Registry Record Requirements

Every accepted dataset record shall contain, where applicable:

1. Dataset identity
2. Project role
3. Source/provenance
4. Acquisition status
5. License/terms status
6. Retrieval date
7. Acquired files
8. Archive checksums
9. Extracted structure
10. File inventory
11. Label/annotation format
12. Class definitions
13. Original split
14. Sentinel split
15. Leakage controls
16. Preprocessing
17. Derived datasets
18. Statistics
19. Corruption/exclusions
20. Experiments using the data
21. Model artifacts produced
22. Limitations
23. Redistribution status
24. Reviewer approval

---

# 3. Canonical Dataset Record Template

Copy this template when a new dataset is accepted.

```yaml
dataset_id: "DATA-..."
name: "..."
registry_version: "1"
status: "NOT_YET_ACQUIRED"

purpose:
  - "TBD"

usage_roles:
  - "TBD"

source:
  original_project_url: "TBD"
  original_paper: "TBD"
  original_authors:
    - "TBD"
  official_download_route: "TBD"
  mirror_used: false
  mirror_details: null

acquisition:
  retrieved_at: "TBD"
  retrieved_by: "TBD"
  acquisition_manifest: "TBD"
  provider: "TBD"

terms:
  license_name: "TBD"
  terms_url: "TBD"
  terms_review_status: "TBD"
  redistribution_allowed: "TBD"
  notes: "TBD"

raw_files:
  - filename: "TBD"
    size_bytes: "TBD"
    sha256: "TBD"

local_layout:
  raw_root: "TBD"
  interim_root: "TBD"
  processed_root: "TBD"

annotations:
  format: "TBD"
  description: "TBD"

classes:
  - code: "TBD"
    meaning: "TBD"

splits:
  official_split_used: "TBD"
  sentinel_split_manifest: "TBD"
  train_count: "TBD"
  validation_count: "TBD"
  test_count: "TBD"
  leakage_check: "TBD"

preprocessing:
  script: "TBD"
  git_commit: "TBD"
  parameters: "TBD"
  output_dataset_id: "TBD"

statistics:
  file_count: "TBD"
  total_duration_seconds: "TBD"
  corrupted_files: "TBD"

experiments:
  - "TBD"

models:
  - "TBD"

limitations:
  - "TBD"

review:
  owner: "TBD"
  reviewer: "TBD"
  reviewed_at: "TBD"
```

---

# 4. Dataset ID Convention

Use:

```text
DATA-<SHORT-NAME>-<VERSION>
```

Examples:

```text
DATA-XD-VIOLENCE-V1
DATA-UCF-CRIME-V1
DATA-MOT17-V1
DATA-COCO-2017
DATA-SENT-DEMO-V1
```

Derived datasets use:

```text
DATA-DERIVED-<PURPOSE>-<VERSION>
```

Examples:

```text
DATA-DERIVED-XD-FIGHTING-BINARY-V1
DATA-DERIVED-UCF-FIGHTING-NORMAL-V1
```

Do not reuse an existing dataset ID to describe different files.

---

# 5. Dataset Versioning Rule

A new registry version is required when any material input changes:

- different source archive;
- updated official release;
- different subset selection;
- changed labels;
- changed split;
- changed preprocessing;
- removed corrupt files;
- different test set.

Do not overwrite:

```text
DATA-DERIVED-XD-FIGHTING-BINARY-V1
```

with a materially different dataset and keep the same ID.

Create:

```text
...-V2
```

---

# 6. Manifest Files

Each active dataset should have:

```text
data/manifests/<dataset-id>/
```

Recommended files:

```text
acquisition.yaml
files.csv
checksums.txt
statistics.json
exclusions.csv
splits/
  train.txt
  validation.txt
  test.txt
preprocessing.yaml
README.md
```

These metadata files should be committed.

The large dataset files should not.

---

# 7. File Inventory Schema

Recommended:

```csv
relative_path,size_bytes,sha256,label,split,source_video_id,status
```

Example structure only:

```csv
videos/example.mp4,123456,TBD,violence,train,video_001,valid
```

Do not populate fake values.

---

# 8. Split Manifest Rule

Every formal train/validation/test split shall be represented by committed manifests.

For example:

```text
data/manifests/DATA-DERIVED-XD-FIGHTING-BINARY-V1/splits/train.txt
data/manifests/DATA-DERIVED-XD-FIGHTING-BINARY-V1/splits/validation.txt
data/manifests/DATA-DERIVED-XD-FIGHTING-BINARY-V1/splits/test.txt
```

Each line should contain one stable sample/video/window identifier.

---

# 9. Split Immutability

Once a split is used for a formally reported model:

- do not silently move files between train/test;
- create a new split version;
- link new experiments to the new version.

---

# 10. Test Set Protection

The formal test set shall not be used for:

- fitting weights;
- routine threshold tuning;
- repeated hyperparameter optimization.

If this happens, record:

```text
test_set_integrity: COMPROMISED_FOR_FINAL_HOLDOUT
```

and disclose it in the model card.

---

# 11. Leakage Review

For video data, inspect whether different windows/clips come from the same original source.

A derived split should prefer grouping by:

```text
original video
```

so related windows do not leak across train and test.

Registry field:

```yaml
leakage_review:
  method: "group by original video ID"
  status: "TBD"
  findings: "TBD"
```

---

# 12. Dataset Statistics

Statistics must be computed from actual files.

Potential fields:

```text
video_count
positive_count
negative_count
total_duration
mean_duration
median_duration
resolution_distribution
FPS distribution
corrupted_count
missing_annotation_count
```

No count should be copied from a paper and represented as the local Sentinel subset count.

---

# 13. Original Dataset Statistics vs Sentinel Statistics

Keep these separate.

## Original authors' description

Example:

```text
XD-Violence authors describe 4,754 untrimmed videos.
```

## Sentinel local statistics

Example form:

```text
Sentinel locally acquired: TBD files.
Sentinel selected subset: TBD files.
```

Never mix them.

---

# 14. Exclusion Register

Every removed file from a selected dataset should be recorded if exclusion affects reproducibility.

Recommended:

```csv
relative_path,reason,detected_by,decision
```

Possible reasons:

```text
decode_failed
missing_annotation
duplicate
outside_task_definition
corrupt_archive_entry
privacy_review
```

---

# 15. Preprocessing Record

Each derived dataset shall record:

```yaml
script: "scripts/data/..."
git_commit: "..."
input_dataset_id: "..."
output_dataset_id: "..."
parameters:
  fps: "TBD"
  resize: "TBD"
  clip_length: "TBD"
  stride: "TBD"
```

Do not document preprocessing only in a notebook cell.

---

# 16. Deterministic Preprocessing

Where randomness is used:

- record seed;
- record library;
- save resulting split manifest.

This is more important than claiming perfect deterministic reproduction across all hardware.

---

# 17. Derived Dataset Chain

Example:

```text
DATA-XD-VIOLENCE-V1
    ↓ subset script
DATA-DERIVED-XD-FIGHTING-BINARY-V1
    ↓ feature transform
DATA-DERIVED-XD-FIGHTING-FEATURES-V1
```

Each stage receives a unique ID.

---

# 18. Experiment Linkage

An experiment record should include:

```yaml
dataset_id: "DATA-DERIVED-XD-FIGHTING-BINARY-V1"
split_manifest_hash: "..."
```

This binds model results to an exact data version.

---

# 19. Model Linkage

A model version should reference:

```text
dataset_id
experiment_id
training commit
```

The chain becomes:

```text
model version
→ experiment
→ dataset registry
→ acquisition manifest
→ original source
```

---

# 20. Dataset Hash Strategy

For raw archives:

```text
SHA-256 archive checksum
```

For split manifests:

```text
SHA-256 manifest checksum
```

For derived datasets:

- manifest hash is mandatory;
- per-file hashes are recommended when feasible.

---

# 21. Current Record — `DATA-SENT-DEMO-V1`

## 21.1 Identity

**Name:** Sentinel team-controlled demonstration/test videos  
**Status:** `NOT_YET_REGISTERED`  
**Role:** `SYSTEM_INTEGRATION_TEST`, `DEMO_FIXTURE`

## 21.2 Intended scenarios

Expected eventual fixtures:

```text
restricted-area entry
loitering
crowd threshold
no-person negative
violence positive if legitimate fixture available
violence negative
corrupted/invalid media
```

## 21.3 Current facts

The conversation/project plan requires controlled deterministic test media.

However, this registry does not currently have:

- confirmed filenames;
- hashes;
- durations;
- local paths;
- participant consent records.

Therefore all remain `TBD`.

## 21.4 Registry record

```yaml
dataset_id: "DATA-SENT-DEMO-V1"
name: "Sentinel Team-Controlled Test Videos"
status: "NOT_YET_REGISTERED"

purpose:
  - "deterministic integration testing"
  - "first vertical slice"
  - "system rule verification"

usage_roles:
  - "SYSTEM_INTEGRATION_TEST"
  - "DEMO_FIXTURE"

source:
  type: "team-controlled"
  provenance: "TBD"

acquisition:
  retrieved_at: "NOT_APPLICABLE_OR_TBD"
  recorded_by: "TBD"

terms:
  redistribution_allowed: "TBD"
  participant_permission_status: "TBD"

raw_files: []

splits:
  formal_ml_split: "NOT_APPLICABLE unless later used for model evaluation"

experiments: []

limitations:
  - "Not intended to replace formal violence-model evaluation data."
```

---

# 22. Demo Fixture Registry Template

For each video:

```yaml
fixture_id: "SENT-FIX-001"
dataset_id: "DATA-SENT-DEMO-V1"
filename: "TBD"
sha256: "TBD"

scenario:
  primary_event: "restricted_area_intrusion"

expected_timeline:
  - time: "TBD"
    behavior: "person visible outside zone"
  - time: "TBD"
    behavior: "person enters configured zone"

expected_events:
  - type: "restricted_area_intrusion"
    expected_count: 1

provenance:
  source: "TBD"
  permission: "TBD"

media:
  duration_seconds: "TBD"
  fps: "TBD"
  width: "TBD"
  height: "TBD"
```

---

# 23. Current Record — `DATA-XD-VIOLENCE-V1`

## 23.1 Identity

**Name:** XD-Violence  
**Status:** `NOT_YET_ACQUIRED`  
**Role:** Candidate violence/fighting training/evaluation source.

Official acquisition guidance is in:

`09-dataset-acquisition.md`

## 23.2 Registry state

No local acquired file has yet been verified in this project record.

Therefore:

```text
local file count = TBD
local duration = TBD
local checksum = TBD
actual split used = TBD
```

## 23.3 Candidate record

```yaml
dataset_id: "DATA-XD-VIOLENCE-V1"
name: "XD-Violence"
status: "NOT_YET_ACQUIRED"

purpose:
  - "candidate violence/fighting model development"

usage_roles:
  - "CANDIDATE_TRAIN"
  - "CANDIDATE_VALIDATION"
  - "CANDIDATE_TEST"

source:
  original_project_url: "https://roc-ng.github.io/XD-Violence/"
  original_paper: "Not only Look, but also Listen: Learning Multimodal Violence Detection under Weak Supervision"
  mirror_used: false

acquisition:
  retrieved_at: "TBD"
  acquisition_manifest: "TBD"

terms:
  license_name: "TBD_AFTER_REVIEW"
  terms_review_status: "NOT_YET_REVIEWED"
  redistribution_allowed: "TBD"

raw_files: []

annotations:
  format: "TBD_AFTER_ACQUISITION"
  description: "Weak-label/test-annotation structure to be inspected."

splits:
  official_split_used: "TBD"
  sentinel_split_manifest: "TBD"
  leakage_check: "TBD"

preprocessing:
  status: "NOT_STARTED"

statistics:
  local_file_count: "TBD"
  local_total_duration_seconds: "TBD"

experiments: []

models: []

limitations:
  - "Large weakly supervised violence/anomaly dataset."
  - "Task mapping to Sentinel fighting/violence must be defined before use."
```

---

# 24. XD-Violence Acceptance Gate

Change status from:

```text
NOT_YET_ACQUIRED
```

to:

```text
ACQUIRED_VERIFIED
```

only after:

- [ ] files physically obtained;
- [ ] original filename recorded;
- [ ] checksum calculated;
- [ ] archive validated;
- [ ] annotation format inspected;
- [ ] terms reviewed;
- [ ] acquisition manifest committed.

Change to:

```text
ACTIVE
```

only after an experiment actually references it.

---

# 25. XD-Violence Derived Dataset Placeholder

Potential future dataset:

```text
DATA-DERIVED-XD-FIGHTING-BINARY-V1
```

**Status:** `NOT_CREATED`

Do not create this registry entry as active until:

1. positive-class definition is approved;
2. negative-class definition is approved;
3. subset script exists;
4. split manifests exist;
5. counts are computed.

---

# 26. Potential XD Derived Record Template

```yaml
dataset_id: "DATA-DERIVED-XD-FIGHTING-BINARY-V1"
status: "NOT_CREATED"

parent_dataset_id: "DATA-XD-VIOLENCE-V1"

task_definition:
  positive_class: "TBD"
  negative_class: "TBD"

creation:
  script: "TBD"
  git_commit: "TBD"
  created_at: "TBD"

statistics:
  positive_samples: "TBD"
  negative_samples: "TBD"
  total_samples: "TBD"

splits:
  train_manifest: "TBD"
  validation_manifest: "TBD"
  test_manifest: "TBD"

leakage_review:
  status: "TBD"

experiments: []
```

---

# 27. Current Record — `DATA-UCF-CRIME-V1`

## 27.1 Identity

**Name:** UCF-Crime  
**Status:** `NOT_YET_ACQUIRED`  
**Role:** Secondary violence/anomaly candidate.

## 27.2 Important registry caution

Current acquisition guidance identifies an official note concerning corrected anomaly-training split data.

Therefore the exact split file used must be recorded.

Do not write:

```text
used official split
```

without identifying the exact file/version.

## 27.3 Candidate record

```yaml
dataset_id: "DATA-UCF-CRIME-V1"
name: "UCF-Crime"
status: "NOT_YET_ACQUIRED"

purpose:
  - "secondary candidate for violence/fighting evaluation or training"

usage_roles:
  - "CANDIDATE_TRAIN"
  - "CANDIDATE_TEST"

source:
  original_project_url: "https://www.crcv.ucf.edu/research/real-world-anomaly-detection-in-surveillance-videos/"
  official_download_route: "See 09-dataset-acquisition.md"
  mirror_used: false

acquisition:
  retrieved_at: "TBD"
  acquisition_manifest: "TBD"

terms:
  license_name: "TBD"
  terms_review_status: "NOT_YET_REVIEWED"

raw_files: []

splits:
  official_split_used: "TBD"
  corrected_split_file_verified: "TBD"

preprocessing:
  status: "NOT_STARTED"

statistics:
  local_file_count: "TBD"
  local_total_duration_seconds: "TBD"

experiments: []
models: []

limitations:
  - "Broad anomaly dataset rather than a simple fighting-only binary dataset."
  - "Task definition must match selected classes."
```

---

# 28. UCF Derived Dataset Placeholder

Potential:

```text
DATA-DERIVED-UCF-FIGHTING-NORMAL-V1
```

Status:

```text
NOT_CREATED
```

Required decisions before creation:

- Fighting only vs broader violence;
- definition of negative/normal;
- official split preservation;
- original-video grouping.

---

# 29. Current Record — `DATA-MOT17-V1`

## 29.1 Identity

**Name:** MOT17  
**Status:** `NOT_YET_ACQUIRED`  
**Role:** `OPTIONAL_EVALUATION`

## 29.2 Important scope rule

MOT17 shall not be treated as required tracker training data.

Use only if formal tracking benchmark adds value within schedule.

## 29.3 Candidate record

```yaml
dataset_id: "DATA-MOT17-V1"
name: "MOT17"
status: "NOT_YET_ACQUIRED"

purpose:
  - "optional tracker evaluation"

usage_roles:
  - "BENCHMARK"

source:
  original_project_url: "https://motchallenge.net/data/MOT17/"

acquisition:
  retrieved_at: "TBD"

terms:
  license_name: "TBD_AFTER_REVIEW"
  terms_review_status: "NOT_YET_REVIEWED"

raw_files: []

evaluation:
  evaluator: "TBD"
  metrics:
    - "HOTA"
    - "IDF1"
    - "MOTA"
    - "ID switches"

experiments: []

limitations:
  - "Optional benchmark; Sentinel operational clips may be more directly relevant."
```

---

# 30. MOT17 Status Transition

If the team decides not to benchmark tracking formally:

change:

```text
NOT_YET_ACQUIRED
```

to:

```text
REJECTED_FOR_CURRENT_PLAN
```

with reason:

```text
operational tracker validation sufficient within schedule
```

Do not leave unused downloads ambiguously listed.

---

# 31. Current Record — `DATA-COCO-2017`

## 31.1 Identity

**Name:** COCO 2017  
**Status:** `PRETRAINED_PROVENANCE_ONLY`

## 31.2 Meaning

The project may use detector weights trained on COCO.

That does **not** mean Sentinel locally trains/evaluates on COCO.

Current default:

```text
no full COCO download required
```

## 31.3 Registry record

```yaml
dataset_id: "DATA-COCO-2017"
name: "COCO 2017"
status: "PRETRAINED_PROVENANCE_ONLY"

purpose:
  - "record provenance of pretrained object detector weights"

usage_roles:
  - "PRETRAINED_PROVENANCE"

source:
  original_project_url: "https://cocodataset.org/"

acquisition:
  local_dataset_downloaded: false
  retrieved_at: "NOT_APPLICABLE"

raw_files: []

splits:
  sentinel_local_split: "NOT_APPLICABLE"

experiments:
  - "TBD — link only if a selected detector explicitly uses COCO-pretrained weights"

limitations:
  - "Sentinel shall not claim to have trained on COCO unless a local training experiment is actually performed."
```

---

# 32. COCO Status Change Rule

If team later downloads COCO for actual fine-tuning/evaluation:

1. create acquisition manifest;
2. change status to `ACQUIRED_VERIFIED`;
3. list exact archives/checksums;
4. create experiment-specific derived dataset ID;
5. record actual fine-tuning.

Do not merely change the status because a dependency internally references COCO class labels.

---

# 33. Current Record — `DATA-RWF-2000-V1`

## 33.1 Identity

**Name:** RWF-2000  
**Status:** `REJECTED_FOR_CURRENT_PLAN`

## 33.2 Reason

Official acquisition is currently unavailable under the project's verified source review.

The short project schedule cannot depend on uncertain access.

## 33.3 Registry record

```yaml
dataset_id: "DATA-RWF-2000-V1"
name: "RWF-2000"
status: "REJECTED_FOR_CURRENT_PLAN"

purpose:
  - "originally considered as violence/fighting dataset"

usage_roles: []

source:
  original_project_url: "https://github.com/mchengny/RWF2000-Video-Database-for-Violence-Detection"

acquisition:
  retrieved_at: "NOT_ACQUIRED"
  official_access_available_to_team: false

raw_files: []

experiments: []
models: []

rejection:
  reason: "Official video files unavailable for current project plan; do not depend on unverifiable mirrors."
  reconsider_if: "Legitimate official access is obtained with sufficient schedule remaining."
```

---

# 34. Rejected Dataset Rule

Rejected datasets remain in the registry to preserve decision history.

Do not delete the entry and later make it appear as though the dataset was never considered.

---

# 35. Dataset Selection Decision Record

```yaml
decision_id: "DATA-DEC-001"
selected_feature_dataset_id: "DATA-XD-I3D-FEATURES-V1"
selected_derived_dataset_id: "DATA-DERIVED-XD-FIGHTING-BINARY-V1"
decision_date: "2026-09-12"
selection_basis:
  - "strict Fighting-vs-Normal task fit"
  - "available reproducible RGB I3D feature representation"
  - "frozen train/validation/test manifests"
  - "feasible on available student hardware"

parent_raw_dataset:
  dataset_id: "DATA-XD-VIOLENCE-V1"
  note: "complete raw corpus not claimed as fully acquired"

alternatives:
  - dataset_id: "DATA-UCF-CRIME-V1"
    outcome: "not required for frozen MVP violence model"
  - dataset_id: "DATA-UCF-CRIME-V1"
    outcome: "TBD"
  - dataset_id: "DATA-RWF-2000-V1"
    outcome: "REJECTED_FOR_CURRENT_PLAN"

criteria:
  task_fit: "TBD"
  acquisition_reliability: "TBD"
  terms: "TBD"
  compute_feasibility: "TBD"
  schedule_fit: "TBD"

rationale: "TBD"
```

This should align with the relevant ADR/model-selection documentation.

---

# 36. Dataset Terms Review Record

For every ACTIVE external dataset:

```yaml
terms_review:
  reviewed_at: "..."
  reviewed_by: "..."
  official_terms_source: "..."
  redistribution: "allowed / prohibited / unclear"
  modification: "..."
  academic_use: "..."
  commercial_use: "..."
  unresolved_questions:
    - "..."
```

This is a project record, not legal advice.

---

# 37. Dataset Redistribution Classification

Use one:

```text
REDISTRIBUTION_ALLOWED
REDISTRIBUTION_PROHIBITED
REDISTRIBUTION_RESTRICTED
REDISTRIBUTION_UNCLEAR
```

Until reviewed:

```text
REDISTRIBUTION_UNCLEAR
```

Default Git policy remains:

```text
do not commit external dataset media
```

---

# 38. External Mirror Record

If a mirror is ever used:

```yaml
mirror:
  used: true
  original_source: "..."
  mirror_url: "..."
  provider: "..."
  retrieved_at: "..."
  reason: "..."
  identity_verification:
    filenames_match: "TBD"
    sizes_match: "TBD"
    checksums_known: "TBD"
  uncertainty: "..."
```

The final academic citation still points to original authors/paper.

---

# 39. Dataset Validation Record

Example template:

```yaml
validation:
  archive_integrity:
    status: "PASS/FAIL/TBD"
    command: "..."
  video_decode:
    files_checked: "TBD"
    valid: "TBD"
    failed: "TBD"
  annotation_validation:
    status: "TBD"
    notes: "TBD"
```

---

# 40. Video Metadata Registry

For selected videos, store:

```text
duration
fps
width
height
codec
frame_count if reliable
```

These should be generated automatically.

Do not manually type hundreds of video metadata rows.

---

# 41. Statistics File Example

Recommended generated JSON:

```json
{
  "dataset_id": "DATA-DERIVED-...",
  "generated_at": "TBD",
  "file_count": "TBD",
  "class_counts": {},
  "total_duration_seconds": "TBD",
  "corrupt_files": []
}
```

---

# 42. Class Taxonomy Record

The registry must define exactly what model labels mean.

Example template:

```yaml
classes:
  - code: "violence"
    definition: "TBD"
    source_labels:
      - "TBD"

  - code: "non_violence"
    definition: "TBD"
    source_labels:
      - "TBD"
```

This is critical when source dataset has categories broader than Sentinel's final task.

---

# 43. Label Mapping

For every derived classification dataset, record source-to-Sentinel mapping.

Example form:

```yaml
label_mapping:
  Fighting: "violence"
  Normal: "non_violence"
  Assault: "TBD_INCLUDE_OR_EXCLUDE"
```

Never leave mapping implicit inside training code.

---

# 44. Excluded Classes

If source classes are excluded:

```yaml
excluded_source_classes:
  - source_label: "Explosion"
    reason: "Outside selected fighting/violence task definition."
```

Actual labels/reasons must reflect the chosen task.

---

# 45. Weak-Label Handling

If source data uses video-level weak labels:

record:

```yaml
annotation_strength: "weak"
temporal_localization_available: "TBD"
window_labeling_strategy: "TBD"
```

Do not imply frame-level ground truth when only video-level labels exist.

---

# 46. Temporal Window Registry

For a derived video-window dataset:

```yaml
windowing:
  frames_per_window: "TBD"
  sampling_fps: "TBD"
  duration_seconds: "TBD"
  stride_seconds: "TBD"
  overlap: "TBD"
  label_assignment_rule: "TBD"
```

---

# 47. Pre-Extracted Feature Dataset

If using authors' I3D features, create a derived/feature record.

Example:

```yaml
dataset_id: "DATA-XD-I3D-FEATURES-V1"
status: "ACTIVE"
parent_dataset_id: "DATA-XD-VIOLENCE-V1"

local_inventory:
  npy_files: 4750
  observed_shape_schema: "(T, 5, 2048)"

representation:
  producer: "Jia-Herng re-extraction pipeline / published Hugging Face corpus"
  feature_type: "RGB I3D ResNet-50 non-local"
  extraction_by_sentinel_for_training_corpus: false

sentinel_runtime_reproduction:
  exact_pipeline_qualified: true
  raw_video_fixtures: 2
  purpose: "compatibility verification only; not model performance evaluation"
```

Do not describe these as team-generated features.

---

# 48. Audio Feature Record

If VGGish features are used:

```yaml
representation:
  modality: "audio"
  feature_type: "VGGish"
  produced_by: "dataset authors"
```

If not used, no need to acquire/register them beyond acquisition-candidate notes.

---

# 49. Dataset Experiment Matrix

Maintain a table:

| Dataset ID | Experiment ID | Role | Status | Result artifact |
|---|---|---|---|---|
| `TBD` | `TBD` | TRAIN | `TBD` | `TBD` |

Only actual experiments belong here.

---

# 50. Experiment-to-Split Record

For each experiment:

```yaml
experiment_id: "EXP-VIO-..."
dataset_id: "DATA-DERIVED-..."
train_manifest: "..."
validation_manifest: "..."
test_manifest: "..."
train_manifest_sha256: "..."
validation_manifest_sha256: "..."
test_manifest_sha256: "..."
```

This makes metrics reproducible.

---

# 51. Threshold Calibration Dataset

If a dedicated calibration subset is used:

record it explicitly.

Do not call the test set a calibration set after repeatedly selecting thresholds on it.

---

# 52. Model Evaluation Data

For each final reported model:

```yaml
final_evaluation:
  dataset_id: "..."
  test_manifest: "..."
  test_manifest_sha256: "..."
  evaluated_once_after_selection: "yes/no/TBD"
```

---

# 53. Demo Data vs Formal Test Data

A demo clip may be intentionally easy and known.

It should not be used to support general accuracy claims.

Registry roles:

```text
DEMO_FIXTURE
```

and:

```text
TEST
```

are conceptually distinct.

---

# 54. Error Analysis Dataset

If misclassified clips are collected into a review set:

```yaml
dataset_id: "DATA-ERROR-ANALYSIS-V1"
parent_evaluation_dataset: "..."
selection_rule: "misclassified samples from experiment ..."
usage_role: "ERROR_ANALYSIS"
```

Do not retrain on them without creating a new training dataset version.

---

# 55. Human Feedback Dataset

Operator false-positive feedback is not automatically training data.

Potential future registry:

```text
DATA-HUMAN-FEEDBACK-CURATED-V1
```

Status:

```text
DEFERRED
```

It would require manual review/ground-truth curation.

---

# 56. No Self-Updating Dataset

The MVP shall not automatically append every operator action into the training set.

Reasons:

- label quality;
- privacy;
- reproducibility;
- online-learning risk.

---

# 57. Dataset Ownership

Each active dataset should have:

```text
Owner
Reviewer
```

Suggested:

- AI/Data Lead owns;
- Backend/System Lead or another teammate reviews provenance.

No dataset should be sole-person undocumented knowledge.

---

# 58. Registry Update Triggers

Update this document when:

- dataset acquired;
- checksum calculated;
- terms reviewed;
- subset created;
- split created;
- corruption detected;
- class mapping changed;
- dataset used in experiment;
- model selected;
- dataset retired.

---

# 59. Registry PR Rule

A dataset-related PR must state:

```text
Dataset IDs affected:
Experiment IDs affected:
Model IDs affected:
Splits changed:
Metrics invalidated?:
```

---

# 60. Metric Invalidation Rule

If test split changes:

previous final metrics may no longer be directly comparable.

Mark:

```text
SUPERSEDED
```

or:

```text
NOT_COMPARABLE
```

where appropriate.

---

# 61. Data Provenance Audit Checklist

For any model result, reviewer should be able to follow:

```text
metric
→ experiment ID
→ model version
→ test split
→ dataset ID
→ file manifest
→ raw dataset acquisition
→ original source
```

If any link is missing, provenance is incomplete.

---

# 62. Registry Review Checklist — External Dataset

Before `ACTIVE`:

- [ ] Dataset ID unique.
- [ ] Official source recorded.
- [ ] Paper/authors recorded.
- [ ] Acquisition date recorded.
- [ ] Actual files listed.
- [ ] Archive checksum recorded.
- [ ] Archive integrity checked.
- [ ] Terms reviewed.
- [ ] Redistribution status recorded.
- [ ] Local root defined.
- [ ] Annotations inspected.
- [ ] Classes defined.
- [ ] Split manifest committed.
- [ ] Leakage review done.
- [ ] Preprocessing script committed.
- [ ] Dataset statistics generated.
- [ ] Corrupt/excluded files recorded.
- [ ] Experiment linkage established.

---

# 63. Registry Review Checklist — Demo Fixture

Before use in final demonstration:

- [ ] Fixture ID assigned.
- [ ] File checksum recorded.
- [ ] Provenance/permission recorded.
- [ ] Expected event behavior documented.
- [ ] Camera/zone/rule configuration documented.
- [ ] Fixture is not secretly part of training if presented as independent validation.
- [ ] Redistribution status known before putting it in Git.

---

# 64. Registry Review Checklist — Pretrained Provenance

For pretrained detector/model:

- [ ] Model source recorded.
- [ ] Weight version recorded.
- [ ] Original training dataset recorded if documented.
- [ ] License recorded.
- [ ] Sentinel did not falsely claim to train it.
- [ ] Local weight checksum recorded where practical.

---

# 65. Data Folder README Template

Recommended `data/README.md`:

```markdown
# Sentinel AI Data

Large datasets and private media are intentionally not stored in Git.

See:

- `docs/09-dataset-acquisition.md`
- `docs/10-dataset-registry.md`

Active dataset IDs:
- TBD

Expected local roots:
- `data/raw/`
- `data/interim/`
- `data/processed/`
- `data/manifests/`

Do not commit raw CCTV footage or external dataset archives.
```

---

# 66. Acquisition Manifest vs Registry

## Acquisition manifest

Answers:

```text
What did I download?
```

## Dataset registry

Answers:

```text
What did the project actually use and how?
```

A downloaded dataset may never become active.

---

# 67. Raw Dataset vs Derived Dataset

## Raw

Exact source data.

Example:

```text
DATA-XD-VIOLENCE-V1
```

## Derived

Sentinel-generated subset/features/windows/split.

Example:

```text
DATA-DERIVED-XD-FIGHTING-BINARY-V1
```

Final model experiments should generally reference derived dataset IDs where transformations were applied.

---

# 68. Dataset Naming on Disk

Prefer stable IDs:

```text
data/raw/DATA-XD-VIOLENCE-V1/
data/processed/DATA-DERIVED-XD-FIGHTING-BINARY-V1/
```

This is preferable to ambiguous:

```text
data/new/
data/final/
data/final2/
```

---

# 69. Local Path Independence

Registry records should use repository-relative paths where possible.

Good:

```text
data/raw/DATA-XD-VIOLENCE-V1/
```

Bad:

```text
C:\Users\<person>\Downloads\XD
```

Machine-specific paths belong only in local configuration.

---

# 70. Data Restoration Procedure

A contributor should be able to reconstruct an active dataset from:

1. acquisition guide;
2. acquisition manifest;
3. original source;
4. checksum;
5. preprocessing script;
6. split manifest.

If not, reproducibility is incomplete.

---

# 71. Missing Official Source

If official source becomes unavailable after acquisition:

retain:

- retrieval date;
- original URL;
- checksums;
- citation;
- terms record.

Do not re-upload restricted data publicly to "fix" reproducibility.

---

# 72. Data Retention for Project Team

At project completion:

- retain metadata/manifests in repository;
- retain external raw data only according to applicable terms and team needs;
- do not publish restricted media;
- document any deletion.

---

# 73. Dataset Privacy Classification

Recommended internal categories:

```text
PUBLIC_RESEARCH_DATA
RESTRICTED_RESEARCH_DATA
TEAM_CONTROLLED_MEDIA
PRIVATE_MEDIA
```

Do not classify footage as public merely because it is reachable by URL.

---

# 74. Violence Dataset Handling

Violence datasets may contain disturbing real-world footage.

Registry should record:

```yaml
content_warning: true
manual_review_minimized: true/false
```

where relevant.

This is not an ML metric but is useful responsible-research documentation.

---

# 75. Dataset Bias Record

Each active dataset should include limitations such as:

```text
surveillance angle bias
day/night imbalance
country/environment bias
staged vs real footage
compression
class ambiguity
weak labels
```

Only record limitations that are actually supported by dataset inspection/documentation.

---

# 76. Dataset Fit Score

Optional decision table:

| Criterion | Score / Finding |
|---|---|
| Task alignment | `TBD` |
| Access reliability | `TBD` |
| Annotation usefulness | `TBD` |
| Compute fit | `TBD` |
| License/terms clarity | `TBD` |
| Domain similarity | `TBD` |
| Schedule risk | `TBD` |

Avoid fake numerical scoring unless the team defines a scoring rubric.

---

# 77. Dataset Approval Record

When a dataset becomes ACTIVE:

```yaml
approval:
  decision: "APPROVED_FOR_SENTINEL_USE"
  date: "..."
  owner: "..."
  reviewer: "..."
  approved_roles:
    - "TRAIN"
    - "VALIDATION"
    - "TEST"
  restrictions:
    - "..."
```

---

# 78. Dataset Rejection Record

When rejected:

```yaml
rejection:
  date: "..."
  reason: "..."
  reconsideration_condition: "..."
```

This prevents repeated investigation of the same dead end.

---

# 79. Current Dataset Decision Risks

## XD-Violence

Risk:

- large;
- weak labels;
- potentially broader violence task.

## UCF-Crime

Risk:

- anomaly-oriented;
- class mapping/preprocessing complexity.

## MOT17

Risk:

- consumes time without directly improving core MVP.

## COCO

Risk:

- unnecessary large download if pretrained detector already works.

## RWF-2000

Risk:

- official access blocker.

---

# 80. Minimum Viable Dataset Strategy

If violence-model training becomes schedule-critical:

minimum acceptable project data strategy may be:

```text
pretrained person detector
+
controlled deterministic videos for rule events
+
one reproducible violence baseline using officially obtained features/data
+
honest evaluation
```

This is preferable to partially downloading many datasets and completing none.

---

# 81. Dataset Registry Quality Gate

No final model metric may be reported if its dataset record lacks:

- dataset ID;
- split identity;
- sample count;
- provenance;
- experiment linkage.

---

# 82. Dataset Registry and Final Report

The final report should derive dataset facts from this registry.

Do not manually retype counts from memory.

Recommended report table fields:

```text
Dataset
Purpose
Samples used
Classes
Split
Source
Key limitation
```

All values should be traceable here.

---

# 83. Dataset Registry and Model Card

`11-model-card-and-evaluation.md` should reference:

```text
dataset_id
split manifest
experiment ID
```

rather than duplicating uncontrolled dataset descriptions.

---

# 84. Dataset Registry and Code

Training scripts should accept:

```text
dataset_id
manifest path
```

or configuration equivalent.

Avoid hidden file discovery that changes the dataset depending on local folder contents.

---

# 85. File Discovery Rule

Bad:

```python
glob("data/**/*.mp4")
```

if it unintentionally includes test/demo videos.

Better:

```text
load exact manifest
```

for formal experiments.

---

# 86. Hidden Data Leakage Rule

Do not place:

```text
test videos
```

inside a generic folder that training scripts automatically scan.

Use explicit manifests.

---

# 87. Experiment Freeze Procedure

Before final evaluation:

1. choose model candidate;
2. freeze code commit;
3. freeze dataset ID;
4. freeze test split;
5. hash split manifest;
6. run evaluation;
7. store output;
8. register result.

---

# 88. Data Registry Validation Script — Recommended

A future script should verify:

- every manifest file exists;
- no duplicate IDs;
- train/val/test are disjoint;
- source-video grouping constraints;
- checksums where configured;
- labels valid;
- excluded files absent;
- statistics match manifests.

Potential path:

```text
scripts/data/validate_registry.py
```

Status: `PROPOSED`.

---

# 89. Machine-Readable Registry

This Markdown file remains human-authoritative.

For automation, individual dataset YAML manifests are recommended.

Do not make AI assistants parse narrative prose to discover exact training files.

---

# 90. Registry Conflict Rule

If:

```text
Markdown registry
```

and:

```text
machine-readable manifest
```

conflict:

1. stop;
2. inspect actual data;
3. resolve;
4. update both;
5. rerun affected experiments if necessary.

Do not choose whichever file is more convenient.

---

# 91. Dataset Registry Change Log

Recommended section once active use begins:

| Date | Dataset ID | Change | Reason | Approved by |
|---|---|---|---|---|
| `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |

---

# 92. Current Open Dataset Decisions

| ID | Decision | Status |
|---|---|---|
| DATA-OD-001 | Which violence dataset becomes primary? | `RESOLVED: XD-derived I3D feature corpus` |
| DATA-OD-002 | Raw video vs pre-extracted features? | `RESOLVED: pre-extracted RGB I3D for model development; raw fixtures for runtime qualification` |
| DATA-OD-003 | Exact violence task label mapping? | `RESOLVED: Fighting=1, Normal=0; other classes excluded` |
| DATA-OD-004 | Whether UCF-Crime is required at all | `TBD` |
| DATA-OD-005 | Whether MOT17 formal benchmark is worth time | `TBD` |
| DATA-OD-006 | Whether COCO is downloaded locally | `PROPOSED: NO` |
| DATA-OD-007 | Which team-controlled demo videos are created | `TBD` |
| DATA-OD-008 | Formal violence validation/test split | `RESOLVED/FROZEN: VAL 410/75; TEST 300/107 Normal/Fighting` |
| DATA-OD-009 | Whether XD pre-extracted/derived RGB I3D features are used | `RESOLVED: yes; active feature corpus` |
| DATA-OD-010 | Dataset retention after project | `TBD` |

---

# 93. Immediate Registry Actions

The AI/Data Lead should next:

1. create `data/manifests/`;
2. create `DATA-SENT-DEMO-V1` fixture manifest;
3. acquire/inspect XD-Violence annotations or smallest feasibility package;
4. calculate checksum;
5. change XD status only after verification;
6. inspect task labels;
7. decide whether raw video or features are feasible;
8. create derived dataset only after label mapping is accepted;
9. link first violence experiment to exact dataset ID.

---

# 94. Registry Baseline Checklist

Before setting this file to `BASELINED`:

- [ ] Dataset lifecycle/status vocabulary accepted.
- [ ] Dataset ID convention accepted.
- [ ] Manifest structure accepted.
- [ ] Current candidate statuses verified.
- [ ] No external dataset is falsely marked acquired.
- [ ] COCO is correctly separated as pretrained provenance unless locally used.
- [ ] RWF-2000 remains rejected unless access changes.
- [ ] Controlled demo-video governance accepted.
- [ ] Split-manifest policy accepted.
- [ ] Leakage rules accepted.
- [ ] Terms/redistribution fields accepted.
- [ ] Experiment/model linkage accepted.
- [ ] Derived-dataset versioning accepted.
- [ ] No fabricated counts/checksums exist.

---

# 95. AI Assistant Rules for Dataset Registry

An AI assistant shall never:

1. mark a dataset `ACQUIRED` without evidence;
2. invent a checksum;
3. invent local file counts;
4. invent class distributions;
5. assume the team's split from a paper's split;
6. mark public download as redistribution permission;
7. treat a mirror as the original source;
8. invent a license;
9. move test samples into training silently;
10. change a dataset ID while preserving incompatible contents;
11. claim a model used a dataset unless experiment linkage proves it;
12. copy original dataset-wide statistics into Sentinel local-statistics fields;
13. treat operator feedback as ground truth automatically;
14. populate `TBD` fields with plausible-looking values.

---

# 96. SRS Traceability

| Registry concern | SRS requirements |
|---|---|
| dataset registry | MLR-DATA-001 |
| acquisition provenance | MLR-DATA-002 |
| split separation | MLR-DATA-003 |
| leakage | MLR-DATA-004 |
| limitations | MLR-DATA-005 |
| model provenance | MLR-MOD-001/002 |
| experiment reproducibility | MLR-EXP-001/002 |
| licensing | MLR-LIC-001 |
| academic claims | NFR-ACAD-001/002 |
| privacy | NFR-PRIV-* |

---

# 97. Relationship to Other Documents

## `09-dataset-acquisition.md`

Where/how to obtain data.

## `10-dataset-registry.md`

What exact data was used.

## `08-ai-ml-design.md`

How the AI pipeline uses data.

## `11-model-card-and-evaluation.md`

What performance was measured using that data.

## `15-requirements-traceability.md`

Which model/data verification satisfies which requirements.

---

# 98. Example Provenance Chain — Placeholder

Once actual data exists, a complete chain should look like:

```text
Official XD-Violence project
    ↓
DATA-XD-VIOLENCE-V1 acquisition manifest
    ↓
archive SHA-256
    ↓
DATA-DERIVED-XD-FIGHTING-BINARY-V1
    ↓
train/validation/test manifest hashes
    ↓
EXP-VIO-2026XXXX-001
    ↓
MODEL-VIO-V1
    ↓
final evaluation metrics
```

Every placeholder above must be replaced by actual verified IDs before final reporting.

---

# 99. Final Dataset Registry Rule

> **The registry records evidence, not intentions.**
>
> A dataset becomes part of Sentinel AI only when its exact files, provenance, role, split, transformations, and experiment linkage are recorded.
>
> The safest default for an unknown value is:
>
> ```text
> TBD
> ```
>
> not a plausible guess.
>
> By project completion, every reported model result must be traceable through:
>
> ```text
> metric
> → model version
> → experiment
> → exact dataset ID
> → exact split
> → exact files/manifests
> → acquisition record
> → original source
> ```
>
> If that chain cannot be reconstructed, the result is not sufficiently reproducible for Sentinel AI's final academic documentation.


---

# 74. Active XD-Violence-Derived Records — 2026-09-12

## 74.1 `DATA-XD-I3D-FEATURES-V1`

**Status:** `ACTIVE`

Local inventory used for Sentinel model development:

```text
4750 .npy feature files
schema: (T, 5, 2048)
modality: RGB
```

The five spatial crops are preserved in the stored feature tensor.

Exact feature provenance was resolved to the Jia-Herng feature extractor using
the MMAction2 I3D ResNet-50 non-local Kinetics-400 checkpoint.

Sentinel later reproduced this feature pipeline from raw MP4 with near-exact
numeric equivalence. That reproduction does not change the provenance of the
training corpus: Sentinel did not claim that the original 4,750 feature files
were generated locally.

## 74.2 `DATA-DERIVED-XD-FIGHTING-BINARY-V1`

**Status:** `ACTIVE`

Task mapping:

```text
Fighting → positive class 1
Normal   → negative class 0
all other XD-Violence categories → excluded from this strict experiment
```

Frozen splits:

| Split | Normal | Fighting | Total |
|---|---:|---:|---:|
| TRAIN | 1636 | 302 | 1938 |
| VALIDATION | 410 | 75 | 485 |
| TEST | 300 | 107 | 407 |
| **Total** | **2346** | **484** | **2830** |

The TEST split was held out from live-window and threshold selection.

## 74.3 Raw-video compatibility fixtures

Two raw MP4 files were obtained only to verify feature/runtime compatibility:

```text
Normal:
A.Beautiful.Mind.2001__#00-40-52_00-42-01_label_A.mp4

Fighting:
Braveheart.1995__#00-56-30_00-57-20_label_B1-0-0.mp4
```

Roles:

```text
SYSTEM_INTEGRATION_TEST
RUNTIME_COMPATIBILITY
```

They are **not** treated as a performance benchmark or as substitutes for the
frozen TEST split.

## 74.4 Weak-label limitation

The strict Fighting-vs-Normal derived labels remain video-level labels.

Therefore:

- video-level precision/coverage/F1 are reportable;
- Normal-window false-trigger analysis is meaningful;
- exact fighting-onset latency is not reportable from these weak labels;
- positive-window localization recall must not be claimed.

Detailed experiment usage is recorded in
`19-violence-model-and-runtime-qualification.md`.
