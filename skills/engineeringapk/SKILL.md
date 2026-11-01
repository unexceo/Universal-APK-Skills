---
name: engineeringapk
description: Master workflow for Android APK reverse engineering and modification. Use when the user runs /engineeringapk or asks to reverse engineer, decompile, inspect, customize, rebrand, debug, rebuild or assess an APK, even if they name no tool. Collects the APK, inventories it, asks what to do, plans, delegates to the specialist skills, rebuilds, validates and delivers a report.
license: MIT
compatibility: Works best in an agent with a terminal. Needs Java 17+, Python 3 and the tools reported by scripts/detect-tools. Chat-only mode gives commands for the user to run.
metadata:
  version: "1.0.0"
---

# /engineeringapk — APK reverse engineering orchestrator

Coordinates the other skills: `analyzeapk`, `modifyapk`, `rebuildapk`, `apksigning`, `gamemodding`,
`androidsecurity`, `androiddevelopment`. Read the specialist skill before executing its part.

## Safety (applies to every step)
- Proceed only with APKs the user owns or is authorized to analyze, open-source apps, authorized security research, education, or legitimate game modding.
- Refuse: license/paywall/IAP/ads bypass, removing third-party anti-cheat or integrity protection to enable cheating, credential theft, covert surveillance, malware creation/deployment, unauthorized access, extracting or abusing keys/tokens.
- Never modify the original. Never invent tool output. Never claim modified/rebuilt/signed/installed without running and checking it.

## Commands

### /engineeringapk

#### Step 0 — Environment and authorization
1. Run `scripts/detect-tools/detect-tools.sh` (or `.ps1` on Windows), or `command -v java apktool jadx aapt2 apksigner zipalign adb python3`. Record what is available.
2. Decide the mode: **execute** (terminal/sandbox with tools) or **guidance** (chat only: give commands, ask the user to paste output). Tell the user which one in one line.
3. Ask once if not already clear: "Do you own this app or have permission to analyze/modify it?" Stop on a clear no or on a prohibited goal.

#### Step 1 — Get the APK
Ask: "Please upload your APK file." Accept `.apk`; for `.aab`/`.xapk`/`.apks` see `rebuildapk` (bundletool) before continuing.
If the file is not visible (check `/mnt/user-data/uploads` or the working directory), say so; do not assume it exists.
Copy it to `apk-work/<name>/original/` and record `sha256sum`. All later work uses copies.

#### Step 2 — Inspect and identify
Use the `analyzeapk` skill's inventory (`/apkscan` level) and report these fields, marking any that could not be determined:

| Item | Source |
|---|---|
| App name, package, version name/code | `aapt2 dump badging` / `apkanalyzer manifest print` |
| minSdk / targetSdk / compileSdk | badging, manifest |
| APK structure, DEX files, native libs (ABIs), assets, resources | `apk_inventory.py` (zip listing) |
| Permissions, activities, services, receivers, providers | badging / decoded manifest |
| Signing scheme and certificate | `apksigner verify --print-certs` |

Keep it to a compact summary (10–20 lines). Flag anything notable (debuggable, obfuscation, packers, split APK, game engine).

#### Step 3 — Ask what to do
Ask exactly: **"What type of reverse engineering or modification do you want to perform?"** and show:

1. Complete APK structure analysis → `/analyzeapk`
2. Source code and DEX analysis → `/apkdex`
3. Application UI customization → `/customizeapp`
4. App logo and icon replacement → `/changeappicon`, `/changeapplogo`
5. App name and branding modification → `/changeappname`
6. AndroidManifest analysis and modification → `/manifestcheck`, then `/modifyapk`
7. Resource modification → `/apkresources`, then `/modifyapk`
8. Game APK analysis and legitimate modding → `/gameanalysis` (+ `/gameui`, `/gameassets`, `/gamedebug`)
9. Performance and optimization analysis → `/androidoptimize` (`/gameoptimization` for games)
10. Network and API behavior analysis → `/networkanalysis`
11. Security vulnerability assessment → `/securityaudit` (`/permissionaudit`, `/apksafety`)
12. Debugging and crash investigation → `/androiddebug` (`/gamedebug` for games)
13. APK rebuilding → `/rebuildapk`
14. Custom Android application development based on analysis → `/androidproject`

Say they can also describe a custom requirement. Suspected malware → `/malwareanalysis`.

#### Step 4 — Understand the requirement
Restate the goal in one sentence. Ask a question only if the answer changes what you do (e.g. replacement image supplied? new app name text?). One question at a time.

#### Step 5 — Execution plan
Write a short plan before acting:
```
Goal: <one sentence>
Skills: <skill/commands in order>
Steps: 1) … 2) … 3) …
Tools: <available> | Missing: <and impact>
Risks: <signature change, resource limits, integrity checks, …>
Outputs: <files you will actually produce>
```
If tools are missing and the plan cannot run, switch to guidance mode or offer the reduced version.

#### Step 6 — Analyze and perform the work
Run the planned skills in order. Keep logs in `apk-work/<name>/reports/`. After each stage, verify the result (file exists, tool exit code 0, diff shows only intended changes). Stop and report on unexpected failures instead of improvising unrelated fixes.

#### Step 7 — Rebuild
Hand off to `rebuildapk`, then `apksigning` (`/apksign`). If rebuild is not possible, explain why and deliver what exists (analysis, edited sources, exact commands for the user to finish).

#### Step 8 — Validate
Use `/apkverify`: archive integrity, `aapt2 dump badging` still parses, signature verifies, zipalign check, and — only if a device/emulator is attached and the user agrees — `/apkinstall` plus a launch check via `adb logcat`. Report each check as passed/failed/not run.

#### Step 9 — Deliver
Provide only artifacts that exist: modified APK (`out/…-signed.apk`), decoded/edited source, build and signing logs, a modification report (changes before/after, build command and exit code, signing, validation results, limitations; template in the repo at `docs/workflows/report-templates.md`), and installation instructions (the signature differs from the original, so the user must uninstall the original first; warn that app data is lost). Present files with the platform's file-delivery mechanism.

## Failure handling
- Tool missing → name it, point to `docs/installation/tools.md`, offer guidance mode.
- Build error → read the error, fix the root cause once, rerun; after two failed attempts report the log excerpt and options.
- App enforces signature/integrity checks → report it. Do not patch out protections in third-party apps. For the user's own app, change the app's source instead.
