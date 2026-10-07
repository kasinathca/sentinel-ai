param(
    [switch]$NoFetch
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $RepoRoot

try {
    if (-not $NoFetch) {
        git fetch origin --prune
        if ($LASTEXITCODE -ne 0) { throw "git fetch failed" }
    }

    $Branches = @(
        "main",
        "staging",
        "aaditi/frontend-operator-ui",
        "gouri/backend-domain"
    )

    Write-Host "Sentinel AI branch synchronization against origin/main"
    Write-Host ""

    foreach ($Branch in $Branches) {
        git show-ref --verify --quiet "refs/remotes/origin/$Branch"
        if ($LASTEXITCODE -ne 0) {
            Write-Host ("{0,-32} missing on origin" -f $Branch)
            continue
        }

        $Counts = (git rev-list --left-right --count "origin/main...origin/$Branch").Trim()
        if ($LASTEXITCODE -ne 0) { throw "git rev-list failed for $Branch" }

        $Parts = $Counts -split "\s+"
        $MainOnly = [int]$Parts[0]
        $BranchOnly = [int]$Parts[1]

        Write-Host (
            "{0,-32} main-only={1,-4} branch-only={2,-4}" -f `
            $Branch, $MainOnly, $BranchOnly
        )
    }

    Write-Host ""
    Write-Host "Interpretation:"
    Write-Host "  main-only > 0   => branch should merge/rebase from main before new work."
    Write-Host "  branch-only > 0 => branch contains work not yet present in main."
    Write-Host "This script is read-only except for git fetch. It never merges or pushes."
}
finally {
    Pop-Location
}
