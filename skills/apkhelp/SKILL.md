---
name: apkhelp
description: Shows the full list of Universal APK Skills commands, what each does, and which need a local terminal. Use when the user runs /helpapk, asks what commands or skills are available, asks how to use this repository, or seems unsure where to start with an APK.
license: MIT
compatibility: No tools required.
metadata:
  version: "1.0.0"
---

# /helpapk — command help

## Commands

### /helpapk

Print the table below, then one line: "Start with `/engineeringapk` if you have an APK and are unsure what to do."
State the current mode in one line: **execute** (terminal and tools available) or **guidance** (chat only: you provide commands, the user runs them). If you have not checked tools, say "tools not checked yet". Do not ask questions.

| Group | Command | What it does |
|---|---|---|
| Main | `/engineeringapk` | Guided end-to-end workflow: upload, inspect, choose task, execute, rebuild, validate, deliver |
| Analysis | `/analyzeapk` | Full static analysis report |
| | `/apkscan` | Fast triage summary and red flags |
| | `/apkdex` | DEX/source analysis (packages, SDKs, entry points, obfuscation) |
| | `/manifestcheck` | Manifest audit (exported components, flags, config) |
| | `/apkresources` | Resource and asset inventory |
| Modification | `/modifyapk` | General controlled modification with diff |
| | `/customizeapp` | Colors, themes, layouts, strings |
| | `/changeappicon` | Launcher icon replacement (adaptive + legacy) |
| | `/changeapplogo` | In-app logo/splash images |
| | `/changeappname` | App name and labels (all locales) |
| | `/rebuildapk` | Rebuild a decoded APK |
| Game | `/gameanalysis` | Identify engine, assets, structure; online/offline check |
| | `/gamedebug` | Crash, ANR, GPU and log investigation |
| | `/gameassets` | Inventory/extract permitted assets |
| | `/gameui` | HUD/menu/font/scaling changes for permitted games |
| | `/gameoptimization` | Performance, memory, size tuning |
| Security | `/apksafety` | Pre-install safety verdict with evidence |
| | `/securityaudit` | MASVS-style static assessment |
| | `/permissionaudit` | Permission review against app purpose |
| | `/networkanalysis` | Endpoints, TLS/cleartext, pinning config |
| | `/malwareanalysis` | Safe static analysis of suspicious APKs |
| Build/Sign | `/apkbuild` | Build from an Android project (Gradle) |
| | `/apksign` | Align and sign |
| | `/apkverify` | Verify signature, alignment, integrity |
| | `/apkinstall` | Install and launch via adb |
| Development | `/androidmanifest` | Write/fix manifests in source projects |
| | `/androiddebug` | Logcat, crash and ANR triage |
| | `/androidproject` | Scaffold/continue an Android project from analysis |
| | `/androidoptimize` | Size, startup, memory, battery |
| Help | `/helpapk` | This list |

Commands needing a local terminal with tools: everything that decodes, builds, signs, installs or runs `adb`. Pure chat can still do guided analysis from pasted output.
