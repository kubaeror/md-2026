# Installs this repo as a local HoI4 mod:
#  - creates a directory junction in the user's mod folder (no copying)
#  - writes the launcher descriptor <mod>.mod
#
# Usage: pwsh -File tools/install_mod.ps1

param(
    [string]$ModName = "md-2026"
)

$ErrorActionPreference = "Stop"

$repo = Split-Path -Parent $PSScriptRoot
$modDir = Join-Path $env:USERPROFILE "Documents\Paradox Interactive\Hearts of Iron IV\mod"
$link = Join-Path $modDir $ModName
$modFile = Join-Path $modDir "$ModName.mod"

if (-not (Test-Path $modDir)) {
    throw "Mod folder not found: $modDir"
}

# The launcher descriptor. Kept in sync with descriptor.mod by hand (same fields).
$descriptor = @"
version="1.1.0"
tags={
	"Alternative History"
	"Technologies"
	"Balance"
	"Fixes"
	"Ideologies"
	"Military"
	"Utilities"
	"National Focuses"
	"Map"
}
name="Millennium Dawn 2026 Rework"
picture="thumbnail.png"
supported_version="1.19.*"
dependencies={
	"Millennium Dawn: A Modern Day Mod"
}
"@

if (Test-Path $link) {
    $item = Get-Item $link -Force
    if ($item.LinkType -eq "Junction") {
        Write-Host "Junction already present: $link"
    } else {
        throw "$link exists and is not a junction. Remove it manually."
    }
} else {
    New-Item -ItemType Junction -Path $link -Target $repo | Out-Null
    Write-Host "Created junction: $link -> $repo"
}

Set-Content -Path $modFile -Value $descriptor -Encoding UTF8
Write-Host "Wrote launcher descriptor: $modFile"
Write-Host "Done. Enable both 'Millennium Dawn' and 'Millennium Dawn 2026 Rework' in the launcher."
