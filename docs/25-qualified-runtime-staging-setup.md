# Qualified violence runtime staging setup

Status: **verified on the source Windows workstation on 2026-10-09**. This runbook transfers the qualified external assets without committing model weights, videos, datasets, virtual environments, or private paths.

The corresponding executed commands and PASS/FAIL/BLOCKED results are recorded
in `docs/evidence/qualified-runtime-recovery-2026-10-09.md`.

## What is authoritative

The machine-readable inventory is `ai_worker/qualified_runtime_assets.json`. It records the frozen model identity, policy, file sizes and SHA-256 values, source revisions, approved fixture metadata, and the two observed Python environments. `ai_worker/scripts/verify_qualified_runtime.ps1` checks that inventory before the runtime starts.

The application still uses the established path:

```text
local video -> exact Jia-Herng I3D extraction -> frozen temporal scorer
-> structured worker result -> backend 3-of-5 criterion -> SQLite event
-> polling frontend alert
```

The current demo media catalog is directory-based. There is no required video `manifest.json`: the backend enumerates supported files beneath `SENTINEL_DEMO_MEDIA_ROOT`, assigns stable clip IDs from relative paths, and passes the same canonical path to FFmpeg and the worker. The new qualified-runtime manifest is an integrity inventory, not a replacement media catalog.

## External asset transfer

On the qualified source workstation, the authoritative workspace is `C:\Users\kasin\XD-Violence`. Copy these paths to an access-controlled `XD-Violence` directory on staging while preserving relative paths:

```text
sentinel_temporal/artifacts/best_model.pt
sentinel_temporal/train_temporal_gru.py
sentinel_runtime_validation/scripts/phase2g_persistent_extractor_worker.py
sentinel_runtime_validation/reports/EXP-VIO-RUNTIME-COMPAT-001-phase2d-exact-jherng.json
sentinel_runtime_validation/reports/EXP-VIO-LIVE-RUNTIME-001-phase2j-raw-video-parity.json
sentinel_runtime_validation/videos/A.Beautiful.Mind.2001__#00-40-52_00-42-01_label_A.mp4
sentinel_runtime_validation/videos/Braveheart.1995__#00-56-30_00-57-20_label_B1-0-0.mp4
```

Do not send these assets through Git. Use an approved local encrypted drive or team file-transfer mechanism. The videos remain research/demo footage and the model binaries remain external.

Recreate the exact source checkouts:

```powershell
$xdRoot = "D:\SentinelAssets\XD-Violence"
$extractorRoot = Join-Path $xdRoot "sentinel_runtime_validation\extractor_exact_jherng"
New-Item -ItemType Directory -Force -Path $extractorRoot | Out-Null

git clone https://github.com/hongjiaherng/inappropriate-video-detection.git `
  (Join-Path $extractorRoot "inappropriate-video-detection")
git -C (Join-Path $extractorRoot "inappropriate-video-detection") `
  checkout --detach 4900184eb9febf3f6c018faae14947772ce1ea57

git clone https://github.com/open-mmlab/mmaction2.git `
  (Join-Path $extractorRoot "mmaction2-v1.2.0-source")
git -C (Join-Path $extractorRoot "mmaction2-v1.2.0-source") `
  checkout --detach 4d6c93474730cad2f25e51109adcf96824efc7a3
```

Place the externally transferred I3D checkpoint at:

```text
sentinel_runtime_validation/extractor_exact_jherng/inappropriate-video-detection/feature-extractor/pretrained/i3d_imagenet-pretrained-r50-nl-dot-product_8xb8-32x2x1-100e_kinetics400-rgb_20220812-8e1f2148.pth
```

The extractor source is MIT licensed and MMAction2 is Apache-2.0 licensed. The checkpoint and research footage are not redistributed by this repository; confirm their terms before transferring them beyond the academic team.

## Exact observed environments

Both qualified environments used Python `3.10.11` and CUDA-capable NVIDIA hardware.

The exact extractor environment used PyTorch `2.1.2+cu118`, torchvision `0.16.2+cu118`, NumPy `1.26.4`, OpenCV `4.8.1.78`, MMCV `2.1.0`, MMEngine `0.10.7`, MMAction2 `1.2.0`, and Decord `0.6.0`. It reported CUDA runtime `11.8`.

The temporal environment used PyTorch `2.13.0+cu130`, NumPy `2.2.6`, pandas `2.3.3`, scikit-learn `1.7.2`, and SciPy `1.15.3`. It reported CUDA runtime `13.0`. That PyTorch build is the locally qualified build; this repository does not assert that it is available from the public PyPI index. Obtain the approved wheel/source through the same controlled channel as the qualified workstation. Do not silently replace it with a nearby version.

Create the extractor venv at the manifest-recorded location and install the exact packages. Install the checked-out MMAction2 source into that venv. If an exact wheel cannot be obtained, stop and report the environment as blocked instead of claiming equivalence.

## Validate before startup

From the Sentinel repository root:

```powershell
$env:SENTINEL_VIOLENCE_ROOT = "D:\SentinelAssets\XD-Violence"
$env:SENTINEL_DEMO_MEDIA_ROOT = Join-Path $env:SENTINEL_VIOLENCE_ROOT `
  "sentinel_runtime_validation\videos"
$env:SENTINEL_AI_PYTHON = "D:\SentinelPython\temporal\Scripts\python.exe"
$env:PYTHONPATH = (Resolve-Path ".\ai_worker").Path

powershell -NoProfile -ExecutionPolicy Bypass `
  -File ".\ai_worker\scripts\verify_qualified_runtime.ps1" `
  -XDViolenceRoot $env:SENTINEL_VIOLENCE_ROOT `
  -TemporalPython $env:SENTINEL_AI_PYTHON

& $env:SENTINEL_AI_PYTHON -m sentinel_violence_runtime.cli `
  --root $env:SENTINEL_VIOLENCE_ROOT `
  --source-map ".\ai_worker\examples\source_map.example.json" `
  --preflight-only
```

The integrity command fails on missing assets, incorrect sizes/hashes, source revision drift, package/version drift, or missing CUDA. Runtime preflight then loads the actual checkpoint, verifies its training-source hash and parameter count, starts the persistent exact extractor, and reports capabilities.

## Start the integrated application

Install the normal application dependencies, then use the owned launcher:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\backend\requirements-dev.txt
Set-Location .\frontend
npm ci
Set-Location ..

$env:SENTINEL_VIOLENCE_ROOT = "D:\SentinelAssets\XD-Violence"
$env:SENTINEL_DEMO_MEDIA_ROOT = Join-Path $env:SENTINEL_VIOLENCE_ROOT `
  "sentinel_runtime_validation\videos"
$env:SENTINEL_AI_PYTHON = "D:\SentinelPython\temporal\Scripts\python.exe"
$env:SENTINEL_FFMPEG_BINARY = "C:\ffmpeg\bin\ffmpeg.exe"
$env:SENTINEL_FFPROBE_BINARY = "C:\ffmpeg\bin\ffprobe.exe"
.\launch_sentinel_demo.cmd
```

The launcher binds the backend and frontend to loopback, performs AI and database preflight, and owns child-process cleanup. In the browser, start the normal fixture first and confirm no qualified event. Stop it, start the fighting fixture, and confirm a genuine qualified alert and a persisted event. The UI filenames come from the external folder and must not be interpreted as model output; the alert is emitted only after real model scores satisfy the frozen backend criterion.

## Failure rules

- A missing or mismatched checkpoint, I3D weight, source file, environment, or video is a hard failure.
- `candidate_condition=true` is not a persisted event. The backend alone applies the frozen rolling criterion and persists the qualified event.
- Do not copy a checkpoint from another experiment, retrain, resave, retune the threshold, or replace the extractor.
- Do not expose the local development worker, backend, or footage beyond the loopback-only academic demo.
