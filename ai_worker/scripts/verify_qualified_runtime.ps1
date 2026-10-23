[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$XDViolenceRoot = $env:SENTINEL_VIOLENCE_ROOT,

    [Parameter(Mandatory = $false)]
    [string]$TemporalPython = $env:SENTINEL_AI_PYTHON,

    [Parameter(Mandatory = $false)]
    [string]$ValidationPython = "python",

    [switch]$SkipMedia,
    [switch]$SkipEnvironments
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

if ([string]::IsNullOrWhiteSpace($XDViolenceRoot)) {
    throw "Provide -XDViolenceRoot or set SENTINEL_VIOLENCE_ROOT."
}

$resolvedRoot = (Resolve-Path -LiteralPath $XDViolenceRoot).Path
$previousPythonPath = $env:PYTHONPATH
$env:PYTHONPATH = Join-Path $repoRoot "ai_worker"

try {
    $arguments = @(
        "-m", "sentinel_violence_runtime.asset_validation",
        "--root", $resolvedRoot
    )
    if (-not [string]::IsNullOrWhiteSpace($TemporalPython)) {
        $arguments += @("--temporal-python", $TemporalPython)
    }
    if ($SkipMedia) { $arguments += "--skip-media" }
    if ($SkipEnvironments) { $arguments += "--skip-environments" }

    & $ValidationPython @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Qualified runtime validation failed with exit code $LASTEXITCODE."
    }
}
finally {
    $env:PYTHONPATH = $previousPythonPath
}
