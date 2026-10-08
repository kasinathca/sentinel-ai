@echo off
setlocal
set "SENTINEL_LAUNCHER_PATH=%~f0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$lines=Get-Content -LiteralPath '%~f0'; $marker=[Array]::IndexOf($lines,'# SENTINEL_POWERSHELL'); & ([scriptblock]::Create(($lines[($marker+1)..($lines.Length-1)] -join [Environment]::NewLine)))"
exit /b %ERRORLEVEL%
# SENTINEL_POWERSHELL
$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $env:SENTINEL_LAUNCHER_PATH
$backendProcess = $null
$frontendProcess = $null
$watchdogProcess = $null
$stopRequested = $false
$cleaned = $false
$runtimeDir = Join-Path ([IO.Path]::GetTempPath()) ("sentinel-launcher-" + [guid]::NewGuid().ToString("N"))

function Fail([string]$message) { throw $message }
function Require-File([string]$path, [string]$label) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { Fail "$label is missing: $path" }
}
function Require-Directory([string]$path, [string]$label) {
    if (-not (Test-Path -LiteralPath $path -PathType Container)) { Fail "$label is missing: $path" }
}
function Assert-Port-Free([int]$port, [string]$label) {
    $probe = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, $port)
    try { $probe.Start() } catch { Fail "$label port $port is already occupied. No process was stopped." } finally { $probe.Stop() }
}
function Wait-Http([string]$url, [string]$label, [int]$seconds = 45) {
    $deadline = [DateTime]::UtcNow.AddSeconds($seconds)
    do {
        try {
            $response = Invoke-WebRequest -UseBasicParsing -Uri $url -TimeoutSec 2
            if ($response.StatusCode -eq 200) { return $response }
        } catch { Start-Sleep -Milliseconds 500 }
    } while ([DateTime]::UtcNow -lt $deadline)
    Fail "$label did not become ready at $url"
}
function Stop-OwnedTree($process, [string]$label) {
    if ($null -eq $process) { return }
    try {
        if (-not $process.HasExited) {
            & taskkill.exe /PID $process.Id /T /F *> $null
        }
    } catch { Write-Warning "Could not stop launcher-owned $label process tree: $($_.Exception.Message)" }
}
function Cleanup {
    if ($cleaned) { return }
    $script:cleaned = $true
    Write-Host "`nStopping Sentinel AI safely..."
    if ($null -ne $backendProcess -and -not $backendProcess.HasExited) {
        try {
            Invoke-WebRequest -UseBasicParsing -Method Post -Uri "http://127.0.0.1:$backendPort/api/v1/demo/source/stop" -TimeoutSec 4 | Out-Null
            Write-Host "Demo source stop requested."
        } catch { Write-Host "Demo source was already stopped or unavailable." }
    }
    Stop-OwnedTree $frontendProcess "frontend"
    Stop-OwnedTree $backendProcess "backend"
    if (Test-Path -LiteralPath $runtimeDir) { Remove-Item -LiteralPath $runtimeDir -Recurse -Force -ErrorAction SilentlyContinue }
    Write-Host "Launcher-owned processes stopped."
}

[Console]::add_CancelKeyPress({
    param($sender, $eventArgs)
    $eventArgs.Cancel = $true
    $script:stopRequested = $true
})

try {
    Set-Location -LiteralPath $repoRoot
    $backendPort = if ($env:SENTINEL_BACKEND_PORT) { [int]$env:SENTINEL_BACKEND_PORT } else { 8000 }
    $frontendPort = if ($env:SENTINEL_FRONTEND_PORT) { [int]$env:SENTINEL_FRONTEND_PORT } else { 5173 }
    $startupTimeout = if ($env:SENTINEL_STARTUP_TIMEOUT_SECONDS) { [int]$env:SENTINEL_STARTUP_TIMEOUT_SECONDS } else { 45 }
    $uvicornApp = if ($env:SENTINEL_UVICORN_APP) { $env:SENTINEL_UVICORN_APP } else { "app.main:app" }
    $viteScript = if ($env:SENTINEL_VITE_SCRIPT) { $env:SENTINEL_VITE_SCRIPT } else { "dev" }
    $mediaRoot = if ($env:SENTINEL_DEMO_MEDIA_ROOT) { $env:SENTINEL_DEMO_MEDIA_ROOT } else { Join-Path $env:USERPROFILE "Downloads\Ai training\SELECTED VIDEOS" }
    $violenceRoot = if ($env:SENTINEL_VIOLENCE_ROOT) { $env:SENTINEL_VIOLENCE_ROOT } else { Join-Path $env:USERPROFILE "XD-Violence" }
    $venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
    $defaultAiPython = Join-Path $env:LOCALAPPDATA "Programs\Python\Python310\python.exe"
    $aiPython = if ($env:SENTINEL_AI_PYTHON) { $env:SENTINEL_AI_PYTHON } elseif (Test-Path -LiteralPath $defaultAiPython) { $defaultAiPython } else { (Get-Command python.exe -ErrorAction Stop).Source }
    $ffmpeg = if ($env:SENTINEL_FFMPEG_BINARY) { $env:SENTINEL_FFMPEG_BINARY } else { (Get-Command ffmpeg.exe -ErrorAction Stop).Source }
    $ffprobe = if ($env:SENTINEL_FFPROBE_BINARY) { $env:SENTINEL_FFPROBE_BINARY } else { (Get-Command ffprobe.exe -ErrorAction Stop).Source }
    $npm = if ($env:SENTINEL_NPM) { $env:SENTINEL_NPM } else { (Get-Command npm.cmd -ErrorAction Stop).Source }

    Require-File $venvPython "Repository virtual-environment Python"
    Require-Directory (Join-Path $repoRoot "backend") "Backend directory"
    Require-Directory (Join-Path $repoRoot "frontend") "Frontend directory"
    Require-Directory (Join-Path $repoRoot "ai_worker") "AI worker directory"
    Require-Directory $mediaRoot "Demo media folder"
    Require-Directory $violenceRoot "XD-Violence workspace"
    Require-File (Join-Path $violenceRoot "sentinel_temporal\artifacts\best_model.pt") "Frozen checkpoint"
    Require-File (Join-Path $violenceRoot "sentinel_temporal\train_temporal_gru.py") "Frozen temporal model source"
    Require-File (Join-Path $violenceRoot "sentinel_runtime_validation\extractor_exact_jherng\.venv\Scripts\python.exe") "Exact extractor Python"
    Require-File (Join-Path $violenceRoot "sentinel_runtime_validation\scripts\phase2g_persistent_extractor_worker.py") "Exact extractor worker"
    Require-File $aiPython "Qualified AI Python"
    Require-File $ffmpeg "FFmpeg"
    Require-File $ffprobe "FFprobe"
    Require-File $npm "npm"
    Assert-Port-Free $backendPort "Backend"
    Assert-Port-Free $frontendPort "Frontend"

    New-Item -ItemType Directory -Path $runtimeDir | Out-Null
    $sourceMap = Join-Path $runtimeDir "source-map.json"
    [IO.File]::WriteAllText($sourceMap, "{}", [Text.UTF8Encoding]::new($false))
    $env:SENTINEL_DEMO_MEDIA_ROOT = $mediaRoot
    $env:SENTINEL_VIOLENCE_ROOT = $violenceRoot
    $env:SENTINEL_AI_PYTHON = $aiPython
    $env:SENTINEL_FFMPEG_BINARY = $ffmpeg
    $env:SENTINEL_FFPROBE_BINARY = $ffprobe
    $env:PYTHONPATH = Join-Path $repoRoot "ai_worker"

    Write-Host "Running frozen AI preflight..."
    & $aiPython -m sentinel_violence_runtime.cli --root $violenceRoot --source-map $sourceMap --preflight-only
    if ($LASTEXITCODE -ne 0) { Fail "Frozen AI preflight failed with exit code $LASTEXITCODE." }

    Write-Host "Initializing and checking the database..."
    $env:PYTHONPATH = Join-Path $repoRoot "backend"
    & $venvPython (Join-Path $repoRoot "backend\scripts\init_database.py")
    if ($LASTEXITCODE -ne 0) { Fail "Database initialization failed with exit code $LASTEXITCODE." }
    & $venvPython (Join-Path $repoRoot "backend\scripts\check_database.py")
    if ($LASTEXITCODE -ne 0) { Fail "Database readiness check failed with exit code $LASTEXITCODE." }

    $nodeModules = Join-Path $repoRoot "frontend\node_modules"
    if (-not (Test-Path -LiteralPath $nodeModules -PathType Container)) {
        Write-Host "Installing frontend dependencies (first launch only)..."
        Push-Location (Join-Path $repoRoot "frontend")
        try { & $npm ci; if ($LASTEXITCODE -ne 0) { Fail "npm ci failed with exit code $LASTEXITCODE." } } finally { Pop-Location }
    }

    $backendOut = Join-Path $runtimeDir "backend.out.log"
    $backendErr = Join-Path $runtimeDir "backend.err.log"
    $backendArgs = @("-m", "uvicorn", $uvicornApp, "--app-dir", "backend", "--host", "127.0.0.1", "--port", "$backendPort")
    $backendProcess = Start-Process -FilePath $venvPython -ArgumentList $backendArgs -WorkingDirectory $repoRoot -PassThru -WindowStyle Hidden -RedirectStandardOutput $backendOut -RedirectStandardError $backendErr
    $pidState = Join-Path $runtimeDir "owned-processes.json"
    @{ backend_pid = $backendProcess.Id; frontend_pid = 0 } | ConvertTo-Json | Set-Content -LiteralPath $pidState -Encoding ASCII
    $watchdogPath = Join-Path $runtimeDir "cleanup-watchdog.ps1"
    $watchdogCode = @'
param([int]$ParentPid, [int]$BackendPort, [string]$StatePath, [string]$RuntimePath)
while (Get-Process -Id $ParentPid -ErrorAction SilentlyContinue) { Start-Sleep -Milliseconds 500 }
try { Invoke-WebRequest -UseBasicParsing -Method Post -Uri "http://127.0.0.1:$BackendPort/api/v1/demo/source/stop" -TimeoutSec 4 | Out-Null } catch {}
try {
    $state = Get-Content -Raw -LiteralPath $StatePath | ConvertFrom-Json
    foreach ($ownedPid in @($state.frontend_pid, $state.backend_pid)) {
        if ($ownedPid -gt 0 -and (Get-Process -Id $ownedPid -ErrorAction SilentlyContinue)) {
            & taskkill.exe /PID $ownedPid /T /F *> $null
        }
    }
} catch {}
Remove-Item -LiteralPath $RuntimePath -Recurse -Force -ErrorAction SilentlyContinue
'@
    [IO.File]::WriteAllText($watchdogPath, $watchdogCode, [Text.UTF8Encoding]::new($false))
    $watchdogArgs = "-NoProfile -ExecutionPolicy Bypass -File `"$watchdogPath`" -ParentPid $PID -BackendPort $backendPort -StatePath `"$pidState`" -RuntimePath `"$runtimeDir`""
    $watchdogProcess = Start-Process -FilePath "powershell.exe" -ArgumentList $watchdogArgs -PassThru -WindowStyle Hidden
    Wait-Http "http://127.0.0.1:$backendPort/api/v1/health" "Backend health" $startupTimeout | Out-Null
    Wait-Http "http://127.0.0.1:$backendPort/api/v1/health/readiness" "Backend readiness" $startupTimeout | Out-Null
    $catalogResponse = Invoke-RestMethod -Uri "http://127.0.0.1:$backendPort/api/v1/demo/clips" -TimeoutSec 5
    $clips = @($catalogResponse.data)

    $env:VITE_API_PROXY_TARGET = "http://127.0.0.1:$backendPort"
    $frontendOut = Join-Path $runtimeDir "frontend.out.log"
    $frontendErr = Join-Path $runtimeDir "frontend.err.log"
    $frontendArgs = @("run", $viteScript, "--", "--host", "127.0.0.1", "--port", "$frontendPort", "--strictPort")
    $frontendProcess = Start-Process -FilePath $npm -ArgumentList $frontendArgs -WorkingDirectory (Join-Path $repoRoot "frontend") -PassThru -WindowStyle Hidden -RedirectStandardOutput $frontendOut -RedirectStandardError $frontendErr
    @{ backend_pid = $backendProcess.Id; frontend_pid = $frontendProcess.Id } | ConvertTo-Json | Set-Content -LiteralPath $pidState -Encoding ASCII
    Wait-Http "http://127.0.0.1:$frontendPort" "Frontend" $startupTimeout | Out-Null

    $sha = (& git -C $repoRoot rev-parse HEAD).Trim()
    Write-Host "`nSentinel AI Demo"
    Write-Host "------------------------------------------------"
    Write-Host "Repository       : $sha"
    Write-Host "Media root       : $mediaRoot"
    Write-Host "Input videos     : $($clips.Count)"
    Write-Host "Ready canonical  : $($catalogResponse.meta.ready)"
    Write-Host "Need preparation : $($catalogResponse.meta.preparing)"
    Write-Host "Rejected         : $($catalogResponse.meta.rejected)"
    Write-Host "FFmpeg           : PASS"
    Write-Host "FFprobe          : PASS"
    Write-Host "AI preflight     : PASS"
    Write-Host "Database         : PASS"
    Write-Host "Backend          : READY (http://127.0.0.1:$backendPort)"
    Write-Host "Frontend         : READY (http://127.0.0.1:$frontendPort)"
    Write-Host "`nDrop another ordinary supported video into:"
    Write-Host $mediaRoot
    Write-Host "Then use Camera Monitoring -> Refresh Videos."
    Write-Host "No manifest and no manual FFmpeg command are required."
    Write-Host "Press Ctrl+C to stop Sentinel AI safely."
    if ($env:SENTINEL_LAUNCH_NO_BROWSER -ne "1") { Start-Process "http://127.0.0.1:$frontendPort" }

    while (-not $stopRequested) {
        if ($backendProcess.HasExited) { Fail "Backend exited unexpectedly. See $backendErr" }
        if ($frontendProcess.HasExited) { Fail "Frontend exited unexpectedly. See $frontendErr" }
        Start-Sleep -Milliseconds 250
    }
} catch {
    Write-Host "`nSentinel AI launcher error: $($_.Exception.Message)" -ForegroundColor Red
    foreach ($log in @($backendErr, $frontendErr)) {
        if ($log -and (Test-Path -LiteralPath $log)) {
            Write-Host "--- $(Split-Path -Leaf $log) ---"
            Get-Content -LiteralPath $log -Tail 20
        }
    }
    $script:exitCode = 1
} finally {
    Cleanup
}
if ($exitCode) { exit $exitCode }
