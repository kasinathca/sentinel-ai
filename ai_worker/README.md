# Sentinel AI — AI Worker / Frozen Violence Runtime

This package is the repository-side integration layer for the already-qualified Sentinel violence/fighting runtime.

The heavy XD-Violence experiment/model workspace remains **external** to Git. The repository contains source, contracts, tests, examples, and machine-independent configuration logic only.

The verified external inventory is machine-readable in
`qualified_runtime_assets.json`. It includes source revisions, exact hashes and
sizes, approved fixture metadata, and the recovered package versions. The full
Windows transfer/setup runbook is
`../docs/25-qualified-runtime-staging-setup.md`.

## Frozen identity — unchanged

```text
experiment:       EXP-VIO-TEMPORAL-001
model label:      MODEL-VIO-BIGRU-ATTN-XD-V1
model_version_id: 6d22f83d-17f8-5ecf-9f0f-246fa326ec72
checkpoint SHA256:
1fa01d1be82ab3c63d33b4d5f1d5ef4ab2a176d1d2842afc842955ff72896772

live criterion:
W1 / stride 1 / 3-of-5 / threshold 0.906
```

This update does **not** change model identity, threshold, windowing, score semantics, or checksum validation.

## Portable workspace configuration

No developer-specific home-directory path is used.

Configure the external workspace root:

```powershell
$env:SENTINEL_VIOLENCE_ROOT = "<path-to-XD-Violence-workspace>"
```

The default artifact layout below that root remains:

```text
sentinel_temporal/artifacts/best_model.pt
sentinel_temporal/train_temporal_gru.py
sentinel_runtime_validation/extractor_exact_jherng/.venv/
sentinel_runtime_validation/scripts/phase2g_persistent_extractor_worker.py
```

The extractor Python executable is resolved by platform:

```text
Windows: .venv/Scripts/python.exe
POSIX:   .venv/bin/python
```

Any machine with a different qualified layout may override paths without editing source:

```text
SENTINEL_TEMPORAL_CHECKPOINT
SENTINEL_TEMPORAL_TRAIN_SCRIPT
SENTINEL_EXTRACTOR_PYTHON
SENTINEL_EXTRACTOR_WORKER
SENTINEL_RUNTIME_WORK_DIR
```

Relative override values are resolved under `SENTINEL_VIOLENCE_ROOT`.

## Machine-local source map

Generate the ignored local map:

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\ai_worker\scripts\create_local_source_map.ps1
```

or:

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\ai_worker\scripts\create_local_source_map.ps1 `
  -XDViolenceRoot "<path-to-XD-Violence-workspace>"
```

If neither the argument nor `SENTINEL_VIOLENCE_ROOT` is supplied, the script fails with an explicit configuration error instead of guessing a developer path.

`ai_worker/examples/source_map.local.json` is ignored by Git.

## Pure/unit tests

```powershell
$env:PYTHONPATH = (Resolve-Path ".\ai_worker").Path
python -m unittest discover -s .\ai_worker\tests -p "test_*.py" -v
```

These tests do not claim that raw-video inference has run.

## Runtime preflight

With `SENTINEL_VIOLENCE_ROOT` configured:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\ai_worker\scripts\verify_qualified_runtime.ps1 `
  -XDViolenceRoot $env:SENTINEL_VIOLENCE_ROOT `
  -TemporalPython $env:SENTINEL_AI_PYTHON
```

This performs byte-level asset/media validation, source-revision checks, and
exact environment-version checks. It is deliberately stricter than merely
loading a tensor with the expected shape.

```powershell
$env:PYTHONPATH = (Resolve-Path ".\ai_worker").Path

python -m sentinel_violence_runtime.cli `
  --source-map ".\ai_worker\examples\source_map.local.json" `
  --preflight-only
```

`--root` may still be supplied explicitly and takes precedence over the environment variable:

```powershell
python -m sentinel_violence_runtime.cli `
  --root "<path-to-XD-Violence-workspace>" `
  --source-map ".\ai_worker\examples\source_map.local.json" `
  --preflight-only
```

## Controlled file-job smoke test

```powershell
python -m sentinel_violence_runtime.cli `
  --source-map ".\ai_worker\examples\source_map.local.json" `
  --request ".\ai_worker\examples\request.example.json" `
  --source-started-at "2026-09-12T07:00:00.000Z" `
  --output ".\ai_worker\runtime_work\demo-fighting-results.jsonl"
```

The CLI is a development adapter only. Final backend ↔ worker transport/security remains a separate project decision.

## Failure semantics

Model/decode/extractor failures remain explicit failed worker results. They must never be converted into a zero score or a successful `no violence` result.

## Integration boundary

The AI worker produces observations/model results. The backend owns domain-event lifecycle. This package does not implement or guess event cooldown, deduplication, acknowledgement, evidence, auth, or WebSocket behavior.
