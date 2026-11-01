#!/usr/bin/env bash
# Detects which Android reverse-engineering tools are available. Read-only.
# Usage: detect-tools.sh [--json]
set -u
JSON=0; [ "${1:-}" = "--json" ] && JSON=1

# Android SDK build-tools are often not on PATH; look in the newest build-tools dir.
SDK="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}"
[ -z "$SDK" ] && for d in "$HOME/Android/Sdk" "$HOME/Library/Android/sdk"; do [ -d "$d" ] && SDK="$d" && break; done
BT=""
if [ -n "$SDK" ] && [ -d "$SDK/build-tools" ]; then
  BT="$(ls -1 "$SDK/build-tools" 2>/dev/null | sort -V | tail -n1)"; [ -n "$BT" ] && BT="$SDK/build-tools/$BT"
fi

find_tool() { # name
  if command -v "$1" >/dev/null 2>&1; then command -v "$1"; return 0; fi
  for d in "$BT" "$SDK/platform-tools" "$SDK/cmdline-tools/latest/bin"; do
    [ -n "$d" ] && [ -x "$d/$1" ] && { echo "$d/$1"; return 0; }
  done
  return 1
}
version_of() { # name path
  case "$1" in
    java) java -version 2>&1 | head -n1 ;;
    python3) python3 --version 2>&1 ;;
    apktool) apktool --version 2>&1 | head -n1 ;;
    jadx) jadx --version 2>&1 | head -n1 ;;
    aapt2) "$2" version 2>&1 | head -n1 ;;
    adb) "$2" version 2>&1 | head -n1 ;;
    zipalign|apksigner|apkanalyzer|bundletool|keytool|baksmali|smali|frida|androguard|git|docker) "$2" --version 2>&1 | head -n1 ;;
    *) echo "present" ;;
  esac
}

TOOLS="java python3 keytool apktool jadx aapt2 aapt apkanalyzer apksigner zipalign adb bundletool smali baksmali analyzeHeadless frida androguard docker git magick unzip"
first=1
[ $JSON -eq 1 ] && printf '{'
for t in $TOOLS; do
  if p="$(find_tool "$t")"; then
    v="$(version_of "$t" "$p" | tr -d '\r' | head -c 120)"
    if [ $JSON -eq 1 ]; then [ $first -eq 0 ] && printf ','; printf '"%s":{"found":true,"path":"%s","version":"%s"}' "$t" "$p" "$(printf '%s' "$v" | sed 's/"/\\"/g')"
    else printf '%-15s OK       %s  (%s)\n' "$t" "$p" "$v"; fi
  else
    if [ $JSON -eq 1 ]; then [ $first -eq 0 ] && printf ','; printf '"%s":{"found":false}' "$t"
    else printf '%-15s MISSING\n' "$t"; fi
  fi
  first=0
done
if [ $JSON -eq 1 ]; then printf ',"android_sdk":"%s"}\n' "${SDK:-}"; else
  echo "Android SDK: ${SDK:-not found} ${BT:+(build-tools: $BT)}"
  echo "Notes: MobSF runs via Docker; Ghidra's headless tool is 'analyzeHeadless'; Frida needs a device."
  echo "Install help: docs/installation/tools.md"
fi
exit 0
