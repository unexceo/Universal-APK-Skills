# Installs Universal APK Skills (Windows). Not tested on every Windows/PowerShell version; see INSTALL.md.
# Usage: .\install.ps1 -Target claude|agents|gemini|cursor|copilot|cline|custom [-Scope user|project] [-ProjectDir DIR] [-Dest DIR] [-Force] [-Link]
param(
  [Parameter(Mandatory=$true)][ValidateSet("claude","agents","gemini","cursor","copilot","cline","custom")][string]$Target,
  [ValidateSet("user","project")][string]$Scope = "user",
  [string]$ProjectDir = "", [string]$Dest = "", [switch]$Force, [switch]$Link
)
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$home_ = $env:USERPROFILE
$map = @{
  claude  = @("$home_\.claude\skills",  ".claude\skills",  "$home_\.claude\commands", ".claude\commands")
  agents  = @("$home_\.agents\skills",  ".agents\skills",  "", "")
  gemini  = @("$home_\.gemini\skills",  ".gemini\skills",  "", "")
  cursor  = @("$home_\.cursor\skills",  ".cursor\skills",  "", "")
  copilot = @("$home_\.copilot\skills", ".github\skills",  "", "")
  cline   = @("$home_\.cline\skills",   ".cline\skills",   "", "")
  custom  = @($Dest, $Dest, "", "")
}
$m = $map[$Target]
if ($Target -eq "custom" -and -not $Dest) { throw "-Target custom requires -Dest" }
if ($Scope -eq "project") {
  if (-not $ProjectDir) { throw "-Scope project requires -ProjectDir" }
  $skillsDir = Join-Path $ProjectDir $m[1]; $cmdDir = if ($m[3]) { Join-Path $ProjectDir $m[3] } else { "" }
} else { $skillsDir = $m[0]; $cmdDir = $m[2] }
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
$skills = Get-ChildItem (Join-Path $repo "skills") -Directory | Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") }
foreach ($s in $skills) {
  $dst = Join-Path $skillsDir $s.Name
  if (Test-Path $dst) { if ($Force) { Remove-Item -Recurse -Force $dst } else { "skip    $($s.Name) (exists; use -Force)"; continue } }
  if ($Link) { New-Item -ItemType Junction -Path $dst -Target $s.FullName | Out-Null } else { Copy-Item -Recurse $s.FullName $dst }
  "install $($s.Name) -> $dst"
}
if ($cmdDir) {
  New-Item -ItemType Directory -Force -Path $cmdDir | Out-Null
  Get-ChildItem (Join-Path $repo "commands") -Filter *.md | Where-Object { $_.Name -ne "README.md" } | ForEach-Object {
    $t = Join-Path $cmdDir $_.Name
    if ((-not (Test-Path $t)) -or $Force) { Copy-Item $_.FullName $t -Force }
  }
  "commands -> $cmdDir"
}
$bad = $false
foreach ($s in $skills) { if (-not (Test-Path (Join-Path $skillsDir "$($s.Name)\SKILL.md"))) { "VERIFY FAILED: $($s.Name)"; $bad = $true } }
if (-not $bad) { "Verified $($skills.Count) skills in $skillsDir. Restart your agent if it caches skills." } else { exit 1 }
