param(
    [string]$XDViolenceRoot = $env:SENTINEL_VIOLENCE_ROOT
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($XDViolenceRoot)) {
    throw @"
XD-Violence workspace root is not configured.
Provide it explicitly:
  -XDViolenceRoot <path>
or set:
  SENTINEL_VIOLENCE_ROOT=<path>
No developer-specific default path is used.
"@
}

$ResolvedRoot = (Resolve-Path -LiteralPath $XDViolenceRoot).Path
$Out = Join-Path $PSScriptRoot "..\examples\source_map.local.json"
$Out = [System.IO.Path]::GetFullPath($Out)

$Normal = Join-Path $ResolvedRoot "sentinel_runtime_validation\videos\A.Beautiful.Mind.2001__#00-40-52_00-42-01_label_A.mp4"
$Fighting = Join-Path $ResolvedRoot "sentinel_runtime_validation\videos\Braveheart.1995__#00-56-30_00-57-20_label_B1-0-0.mp4"

foreach ($Path in @($Normal, $Fighting)) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Required fixture not found: $Path"
    }
}

$Map = [ordered]@{
    "demo:normal"   = $Normal
    "demo:fighting" = $Fighting
}

$Json = $Map | ConvertTo-Json -Depth 3
[System.IO.File]::WriteAllText(
    $Out,
    $Json + [Environment]::NewLine,
    [System.Text.UTF8Encoding]::new($false)
)

Write-Host "Created machine-local source map:"
Write-Host "  $Out"
Write-Host ""
Write-Host "This file is ignored by Git via *.local.json."
