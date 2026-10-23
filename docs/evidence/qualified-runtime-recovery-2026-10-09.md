# Qualified runtime recovery evidence — 2026-10-09

Branch: `codex/restore-qualified-ai-runtime`

This record covers recovery and staging publication of the already-qualified violence runtime. It does not claim retraining, retuning, or redistribution of external model/media binaries.

## Asset discovery

Searched the declared candidate roots under `C:\Users\kasin\Projects`, `C:\Users\kasin\XD-Violence`, and `C:\Users\kasin\Downloads`, excluding virtual environments and dependency trees from the checkpoint-name scan. One `best_model.pt` candidate was found:

```text
C:\Users\kasin\XD-Violence\sentinel_temporal\artifacts\best_model.pt
size:   3295541 bytes
sha256: 1fa01d1be82ab3c63d33b4d5f1d5ef4ab2a176d1d2842afc842955ff72896772
status: PASS — exact qualified checkpoint
```

The exact I3D checkpoint was found at the manifest-recorded relative path, size `141979657`, SHA-256 `8e1f21482dd3987f0b6329886fc61b00e45a782c4356797df1e4aaa088707bb0`. The extractor source revisions, custom worker, training implementation, qualification reports, and approved normal/fighting fixture hashes are recorded in `ai_worker/qualified_runtime_assets.json`.

## Commands and results

### External integrity and environment gate — PASS

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\ai_worker\scripts\verify_qualified_runtime.ps1 `
  -XDViolenceRoot 'C:\Users\kasin\XD-Violence' `
  -TemporalPython 'C:\Users\kasin\AppData\Local\Programs\Python\Python310\python.exe' `
  -ValidationPython '.\.venv\Scripts\python.exe'
```

Result: `PASS: qualified runtime assets, source revisions, frozen policy, media, and environments match the recorded manifest.`

### Actual model/extractor preflight — PASS

```powershell
$env:PYTHONPATH=(Resolve-Path '.\ai_worker').Path
& 'C:\Users\kasin\AppData\Local\Programs\Python\Python310\python.exe' `
  -m sentinel_violence_runtime.cli `
  --root 'C:\Users\kasin\XD-Violence' `
  --source-map '.\ai_worker\examples\source_map.local.json' `
  --preflight-only
```

Result: worker health `ready`; persistent exact extractor ready; frozen temporal model ready; model UUID `6d22f83d-17f8-5ecf-9f0f-246fa326ec72`.

### Fresh approved-fixture inference — PASS

The same CLI was run with the ignored machine-local source map and the normal/fighting request files. Outputs were written only to an untracked temporary directory and removed after summarization.

```text
normal:   26 windows, maximum score 0.0217826329171658, 0 scores >= 0.906
fighting: 19 windows, maximum score 0.995747625827789, 9 scores >= 0.906
```

This matches the checked qualification record: the normal fixture does not qualify; the fighting fixture satisfies the frozen `0.906`, 3-of-5 criterion. This was actual CUDA raw-video extraction and temporal inference, not cached features or mocked scores.

### Repository integration gate — PASS

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\verify_integration.ps1
```

Result:

- disposable SQLite migration/seed/readiness: PASS;
- backend: 96/96 tests PASS, including worker contract, qualified-event persistence, evidence context, and session deduplication;
- AI worker: 22/22 tests PASS;
- frontend `npm ci`: PASS, 0 vulnerabilities;
- frontend lint: PASS;
- frontend production build: PASS.

The first sandboxed attempt stalled at the first loopback/process-dependent backend contract test and was interrupted without a test result. The identical gate was rerun outside that restricted sandbox and completed successfully as reported above. The earlier browser-visible real alert and dynamic-ingest acceptance evidence remains in `docs/evidence/dynamic-ingest-2026-10-09.md`; a second manual browser session was not necessary for this asset-only change.

### Repository hygiene — PASS

`git diff --cached --check` passed. The staged secret-pattern scan found no credential-like assignments. The complete branch delta from `origin/staging` contains no `.pt`, `.pth`, `.ckpt`, `.onnx`, video, feature-array, private-key, or other prohibited artifact extensions. The largest changed tracked file is under 55 KB. Git LFS was not introduced.

## Status summary

- Qualified checkpoint identity: **PASS**
- Exact extractor source/weight provenance: **PASS**
- Extractor compatibility records: **PASS**
- Approved fixture hashes and roles: **PASS**
- Recovered environment identity and CUDA availability: **PASS**
- Real positive/negative inference: **PASS**
- Backend event contract and persistence: **PASS**
- Frontend build and notification view-model tests: **PASS**
- Fresh manual browser notification run for this asset-only commit: **NOT_YET_EXECUTED**; prior same-branch acceptance evidence exists
- Public installation source for temporal PyTorch `2.13.0+cu130`: **BLOCKED**; the locally qualified build exists and passes, but no public retrieval guarantee is asserted
