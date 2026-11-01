# Detects available Android reverse-engineering tools on Windows. Read-only.
# Usage: powershell -ExecutionPolicy Bypass -File detect-tools.ps1
$sdk = if ($env:ANDROID_HOME) { $env:ANDROID_HOME } elseif ($env:ANDROID_SDK_ROOT) { $env:ANDROID_SDK_ROOT } elseif (Test-Path "$env:LOCALAPPDATA\Android\Sdk") { "$env:LOCALAPPDATA\Android\Sdk" } else { "" }
$bt = ""
if ($sdk -and (Test-Path "$sdk\build-tools")) {
  $latest = Get-ChildItem "$sdk\build-tools" -Directory | Sort-Object { [version]($_.Name -replace '[^0-9.]','') } -ErrorAction SilentlyContinue | Select-Object -Last 1
  if ($latest) { $bt = $latest.FullName }
}
$tools = "java","python","keytool","apktool","jadx","aapt2","aapt","apkanalyzer","apksigner","zipalign","adb","bundletool","smali","baksmali","analyzeHeadless","frida","androguard","docker","git","magick"
foreach ($t in $tools) {
  $cmd = Get-Command $t -ErrorAction SilentlyContinue
  $path = if ($cmd) { $cmd.Source } else {
    $found = $null
    foreach ($d in @($bt, "$sdk\platform-tools", "$sdk\cmdline-tools\latest\bin")) {
      if ($d) { foreach ($ext in "",".exe",".bat",".cmd") { if (Test-Path "$d\$t$ext") { $found = "$d\$t$ext"; break } } }
      if ($found) { break }
    }
    $found
  }
  if ($path) { "{0,-15} OK       {1}" -f $t, $path } else { "{0,-15} MISSING" -f $t }
}
"Android SDK: " + $(if ($sdk) { $sdk } else { "not found" })
"Install help: docs/installation/tools.md"
exit 0
