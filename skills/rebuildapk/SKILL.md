---
name: rebuildapk
description: Rebuild Android APKs from a decoded apktool project or build an APK/AAB from a Gradle source project. Use for /rebuildapk and /apkbuild, and whenever the user wants to recompile, repackage, rebuild, assemble or produce a new APK after edits, or to turn an AAB/split bundle into an installable APK set. Captures build logs and verifies the result.
license: MIT
compatibility: Needs Java 17+ and apktool for /rebuildapk; Android SDK, JDK and a Gradle wrapper for /apkbuild; bundletool for AAB. Must run in a terminal or sandbox; chat-only mode gives commands.
metadata:
  version: "1.0.0"
---

# rebuildapk — rebuild and build

## Safety
- Rebuild only projects/APKs the user owns or may modify. Never overwrite the original APK or the source folder's only copy.
- Do not state that a build succeeded unless the tool exited 0 **and** the output file exists. Show the real error otherwise.
- Output is unsigned or debug-signed until `apksigning` runs. Never publish debug-signed builds.

## Commands

### /rebuildapk
Rebuild a decoded APK (output of `apktool d`).
1. Confirm `decoded/` exists and `git diff --stat` shows the intended edits (see `modifyapk`). Confirm the tool: `apktool --version`.
2. Build with a log: `apktool b decoded -o out/app-unsigned.apk 2>&1 | tee reports/build.log`. Add `--use-aapt2` if the installed apktool defaults to aapt1 and you hit resource errors; add `-d` for a debuggable build only when the user asks.
3. Check: `test -s out/app-unsigned.apk`, `unzip -tq out/app-unsigned.apk`, `aapt2 dump badging out/app-unsigned.apk | head`.
4. Next: `/apksign` (zipalign then sign), `/apkverify`. Do not hand an unsigned APK to the user as "final".
5. Report: apktool version, command, exit code, output path and size, warnings in the log, what was not verified.

Common failures:
| Symptom | Likely cause and action |
|---|---|
| `resource ... not found` / `style/Theme.*` missing | Missing framework: `apktool if <framework-res.apk>` (vendor frameworks too), then rebuild |
| `Invalid ... XML`, `error: attribute not found` | Edit broke XML or used an unsupported attribute; fix the file shown in the log (`git diff`) |
| `Duplicate resource` / `public.xml` conflict | Duplicate names added; remove the duplicate or restore from base commit |
| Build passes, app crashes at launch | Check `adb logcat` (`/androiddebug`); often removed/renamed resource still referenced by code, or integrity checks in the app |
| `Could not decode` on `d`, or resources obfuscated | Try `apktool d -r` for read-only; rebuild from such a decode is unreliable, report it |
| `libs/` or `lib/` missing after rebuild | Check `extractNativeLibs`, keep `lib/` intact; compare entry lists of original vs rebuilt (`unzip -l`) |
| App checks its own signature/integrity | Report. Do not patch out protections in third-party apps |

AAB/XAPK/APKS input: `.aab` is not installable. Make installable APKs with bundletool: `bundletool build-apks --bundle=app.aab --output=app.apks --mode=universal` (add `--ks=… --ks-key-alias=…` to sign with the user's key; otherwise a debug key is used), then `unzip app.apks universal.apk`. For split APK sets (`base.apk` + `split_*.apk`), every split must be rebuilt and signed with the **same** key, installed together with `adb install-multiple`.

### /apkbuild
Build from an Android source project (Gradle).
1. Inspect: `ls`, `settings.gradle(.kts)`, `gradle/wrapper/gradle-wrapper.properties`, `app/build.gradle(.kts)` (`compileSdk`, `minSdk`, `targetSdk`, `applicationId`, `buildTypes`, `signingConfigs`, flavors). Require `local.properties` with `sdk.dir=…` or `ANDROID_HOME`; JDK version matching the Android Gradle Plugin (AGP 8.x needs 17+).
2. List tasks if unsure: `./gradlew tasks --all | grep -i assemble`.
3. Build: debug `./gradlew assembleDebug`; release `./gradlew assembleRelease` (needs a signing config from the user; never invent or commit keystores/passwords); bundle `./gradlew bundleRelease`. Use `--stacktrace` on failure; capture `2>&1 | tee reports/gradle.log`. Windows: `gradlew.bat`.
4. Outputs: `app/build/outputs/apk/<variant>/*.apk`, `app/build/outputs/bundle/<variant>/*.aab`, mapping file `app/build/outputs/mapping/<variant>/mapping.txt` (keep it for crash deobfuscation).
5. Run `./gradlew lint` / unit tests only if requested or cheap; report results honestly. Then `/apkverify`.
Offline sandboxes cannot download Gradle/AGP dependencies; say so and give the user the commands to run locally.
