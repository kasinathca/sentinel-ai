param(
    [string]$XDViolenceRoot = "C:\Users\kasin\XD-Violence"
)

$ErrorActionPreference = "Stop"

$Out = Join-Path $PSScriptRoot "..\examples\source_map.local.json"
$Out = [System.IO.Path]::GetFullPath($Out)

$Normal = Join-Path $XDViolenceRoot "sentinel_runtime_validation\videos\A.Beautiful.Mind.2001__#00-40-52_00-42-01_label_A.mp4"
$Fighting = Join-Path $XDViolenceRoot "sentinel_runtime_validation\videos\Braveheart.1995__#00-56-30_00-57-20_label_B1-0-0.mp4"

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
[System.IO.File]::WriteAllText($Out, $Json + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))

Write-Host "Created local source map:"
Write-Host "  $Out"
Write-Host ""
Write-Host "This file is ignored by Git via *.local.json."
