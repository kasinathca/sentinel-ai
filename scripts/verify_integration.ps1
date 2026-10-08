param(
    [switch]$SkipFrontend,
    [switch]$SkipAiWorker
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$OldPythonPath = $env:PYTHONPATH
$OldDatabaseUrl = $env:SENTINEL_DATABASE_URL
$TempDb = Join-Path $env:TEMP ("sentinel_verify_" + [guid]::NewGuid().ToString("N") + ".db")
$TempDbUrlPath = $TempDb.Replace("\", "/")
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$PythonExecutable = if (Test-Path -LiteralPath $VenvPython -PathType Leaf) {
    $VenvPython
} else {
    "python"
}

function Invoke-Checked {
    param([scriptblock]$Command, [string]$Label)
    Write-Host ""
    Write-Host "=== $Label ==="
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

Push-Location $RepoRoot
try {
    $env:SENTINEL_DATABASE_URL = "sqlite+pysqlite:///$TempDbUrlPath"
    $env:PYTHONPATH = (Resolve-Path ".\backend").Path

    Invoke-Checked { & $PythonExecutable .\backend\scripts\init_database.py } "Disposable DB migration + seed"
    Invoke-Checked { & $PythonExecutable .\backend\scripts\check_database.py } "Database readiness"
    Invoke-Checked {
        & $PythonExecutable -m unittest discover -s .\backend\tests -p "test_*.py" -v
    } "Backend test suite"

    if (-not $SkipAiWorker) {
        $env:PYTHONPATH = (Resolve-Path ".\ai_worker").Path
        Invoke-Checked {
            & $PythonExecutable -m unittest discover -s .\ai_worker\tests -p "test_*.py" -v
        } "AI-worker pure/unit test suite"
    }

    if (-not $SkipFrontend) {
        Push-Location .\frontend
        try {
            Invoke-Checked { npm ci } "Frontend dependency install"
            Invoke-Checked { npm run lint } "Frontend lint"
            Invoke-Checked { npm run build } "Frontend production build"
        }
        finally {
            Pop-Location
        }
    }

    Write-Host ""
    Write-Host "Integration verification completed successfully."
    Write-Host "Raw-video model preflight is intentionally separate because it requires"
    Write-Host "the external qualified XD-Violence workspace and GPU runtime."
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:SENTINEL_DATABASE_URL = $OldDatabaseUrl
    Remove-Item -LiteralPath $TempDb -Force -ErrorAction SilentlyContinue
    Pop-Location
}
