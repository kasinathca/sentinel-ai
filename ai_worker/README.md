# Sentinel AI — AI Worker / Frozen Violence Runtime

This directory is the first application integration layer for the qualified
Sentinel violence/fighting subsystem.

The heavy experiment/model workspace remains external:

```text
C:\Users\kasin\XD-Violence
```

The Git repository contains only source, tests, contracts, and examples.

## Frozen violence configuration

```text
model:
EXP-VIO-TEMPORAL-001
MODEL-VIO-BIGRU-ATTN-XD-V1

checkpoint SHA256:
1fa01d1be82ab3c63d33b4d5f1d5ef4ab2a176d1d2842afc842955ff72896772

live policy:
W1 / stride 1 / 3-of-5 / threshold 0.906

model_version_id:
6d22f83d-17f8-5ecf-9f0f-246fa326ec72
```

The worker emits one structured Fighting score per qualified I3D feature step.

The backend owns:

```text
score >= 0.906
+
at least 3 qualifying observations in the latest 5
```

as a deterministic event criterion.

Persistent event creation, cooldown/retrigger, evidence, and notification remain
backend/domain responsibilities.

## Important architecture rule

This package is transport-neutral.

It does **not** decide the final backend ↔ AI-worker transport.

The CLI in this directory is a development adapter only.

## External runtime dependencies

The runtime expects the already-qualified files under the XD-Violence workspace:

```text
sentinel_temporal/
sentinel_runtime_validation/
```

including:

- frozen temporal checkpoint;
- frozen temporal training implementation used to reconstruct the model class;
- exact I3D extractor isolated environment;
- persistent exact-extractor worker;
- controlled raw-video fixtures for smoke tests.

These heavy/external artifacts must not be copied into Git merely to run this
package.

## Run pure unit tests

From the Sentinel repository root:

```powershell
cd "C:\Users\kasin\Projects\AWT PROJECT"

$env:PYTHONPATH = ".\ai_worker"

python -m unittest discover `
  -s .\ai_worker\tests `
  -p "test_*.py" `
  -v
```

Expected:

```text
Ran 14 tests
OK
```

## Create the machine-local source map

From the repo root:

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\ai_worker\scripts\create_local_source_map.ps1 `
  -XDViolenceRoot "C:\Users\kasin\XD-Violence"
```

This creates:

```text
ai_worker\examples\source_map.local.json
```

It is intentionally ignored by Git.

## Runtime preflight

From the repo root:

```powershell
$env:PYTHONPATH = ".\ai_worker"

python -m sentinel_violence_runtime.cli `
  --root "C:\Users\kasin\XD-Violence" `
  --source-map ".\ai_worker\examples\source_map.local.json" `
  --preflight-only
```

Expected high-level state:

```json
{
  "health": {
    "state": "ready",
    "process_alive": true,
    "extractor_ready": true,
    "temporal_model_ready": true
  }
}
```

## Controlled file-job smoke test

```powershell
$env:PYTHONPATH = ".\ai_worker"

python -m sentinel_violence_runtime.cli `
  --root "C:\Users\kasin\XD-Violence" `
  --source-map ".\ai_worker\examples\source_map.local.json" `
  --request ".\ai_worker\examples\request.example.json" `
  --source-started-at "2026-09-12T07:00:00.000Z" `
  --output ".\ai_worker\runtime_work\demo-fighting-results.jsonl"
```

The output is one structured worker result per W1 observation.

## Worker result semantics

Example:

```json
{
  "schema_version": "1",
  "job_id": "...",
  "correlation_id": "...",
  "camera_id": "...",
  "window": {
    "started_at": "...",
    "ended_at": "..."
  },
  "status": "success",
  "model": {
    "model_version_id": "6d22f83d-17f8-5ecf-9f0f-246fa326ec72",
    "task": "violence_fighting"
  },
  "result": {
    "label": "fighting",
    "score": 0.94,
    "score_semantics": "uncalibrated sigmoid score for the fighting positive class from EXP-VIO-TEMPORAL-001; higher means more fighting-like"
  }
}
```

`label = fighting` identifies the positive class whose score is being reported.
It does not mean the worker created a persistent violence event.

## Failure semantics

Inference/decode/model failures are explicit failed worker results.

They are never converted into:

```text
score = 0
non-violence
no event
```

because that would hide AI unavailability.

## Next backend step

After unit tests, runtime preflight, and the file-job smoke test pass:

1. implement backend validation for this result contract;
2. maintain rolling criterion state per `(camera_id, model_version_id)`;
3. feed `qualified=True` into the event-domain service;
4. add failure-injection integration tests;
5. decide backend ↔ worker transport separately.

Do not change the frozen model/window/threshold based on official TEST behavior.
