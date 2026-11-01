---
name: androiddevelopment
description: Android app development support for source projects and decoded APK analysis results. Use for /androidmanifest, /androiddebug, /androidproject and /androidoptimize, and whenever the user wants to write or fix an AndroidManifest, debug logcat crashes or ANRs, scaffold or continue a Kotlin or Java Android project based on analysis of an app they own, or improve size, startup, memory, jank or battery.
license: MIT
compatibility: JDK 17+, Android SDK, Gradle wrapper, adb. Optional apkanalyzer, Perfetto, LeakCanary, Macrobenchmark. Chat-only mode gives code and commands.
metadata:
  version: "1.0.0"
---

# androiddevelopment — manifest, debugging, projects, optimization

## Safety
- Build only apps the user owns or open-source work whose license permits it. When "recreating" an analyzed app, do a **clean-room reimplementation from a behavior specification**; do not copy third-party proprietary code, assets, trademarks or backend credentials.
- Do not add licensing/ad/IAP bypasses, hidden data collection, or stealth behaviors. Never invent build or test results.

## Commands

### /androidmanifest
Author or fix `AndroidManifest.xml` in a source project (or decoded APK, then follow `modifyapk` for rebuild).
- Checklist: `package`/`namespace` in Gradle (AGP 8+ uses `namespace`), launcher `<activity>` with `MAIN`/`LAUNCHER`, `android:exported` explicit on every component with an intent-filter (required for targetSdk ≥ 31), `uses-permission` minimal and justified, runtime-permission request flow in code, `queries` for package visibility (Android 11+), `foregroundServiceType` and matching permission (Android 14+), `POST_NOTIFICATIONS` (Android 13+), `networkSecurityConfig`, `dataExtractionRules`/`fullBackupContent` (Android 12+), `usesCleartextTraffic="false"` for release, `debuggable` only in debug build type, `android:enableOnBackInvokedCallback`, deep links with `autoVerify`, `FileProvider` instead of `file://`.
- Validate: `./gradlew :app:processDebugMainManifest` (see merged manifest in `app/build/intermediates/merged_manifests/`), `./gradlew lint`, `apkanalyzer manifest print`.
- Output: the changed manifest hunks, rationale per change, and what you validated.

### /androiddebug
1. Reproduce and capture: `adb logcat -c`, reproduce, `adb logcat -d -v threadtime > reports/logcat.txt`; filter `adb logcat -d --pid=$(adb shell pidof -s <pkg>)` or `-s Tag:V`. Crash buffer: `adb logcat -b crash -d`.
2. Triage from the first `FATAL EXCEPTION`/`Caused by` frame in app code; deobfuscate with `retrace mapping.txt trace.txt` (R8 mapping from the matching build); native crashes with `ndk-stack`.
3. ANR: `/data/anr/` or `adb bugreport`; find the main thread state, lock owners, blocking I/O.
4. Tools: StrictMode, `adb shell dumpsys activity`, `dumpsys meminfo/gfxinfo`, Android Studio debugger/Profiler, `adb shell am start -W -n <pkg>/<activity>` for startup time.
5. Common causes: missing `exported`, permission denied (`SecurityException`), `ClassNotFoundException` after shrinking (keep rules), `UnsatisfiedLinkError` (ABI), `NetworkOnMainThreadException`, `ActivityNotFoundException`, `InflateException` (missing resource/theme), lifecycle/config-change bugs.
6. Output: root cause with evidence lines, minimal fix (diff), how to verify, and residual uncertainty.

### /androidproject
Scaffold or continue a project from an analysis report for an app the user owns or from an open-source base.
1. Confirm scope from the behavior spec (screens, flows, data, permissions). Ask only what blocks design.
2. Structure: Gradle Kotlin DSL with version catalog (`gradle/libs.versions.toml`), single `app` module to start, `namespace`/`applicationId` chosen by the user, package layout by feature, Jetpack Compose or Views per the user's preference, ViewModel + state, Room/DataStore if needed, Retrofit/OkHttp or Ktor for network, Hilt/Koin only when justified.
3. Set `compileSdk`/`targetSdk` to current platform requirements (verify the current Play requirement if publishing), sensible `minSdk`, release build with R8 and resource shrinking, no secrets in source (use `local.properties`/CI secrets).
4. Create real files (Gradle files, manifest, `MainActivity`, theme, one working feature), then run `/apkbuild` if the toolchain exists and report the true result. State what is stub vs implemented.
5. Provide a README for the project: build, run, structure.

### /androidoptimize
Measure first, then change.
- Size: `apkanalyzer apk summary|file-size|download-size|compare old.apk new.apk`, `apkanalyzer dex packages`; enable R8 (`isMinifyEnabled`) and `isShrinkResources`, remove unused libs, WebP/vector assets, ABI/density splits or AAB, `android:extractNativeLibs`, 16 KB page-size alignment for native libs targeting Android 15+.
- Startup: Macrobenchmark + Baseline Profiles, App Startup library, defer SDK init off the main thread, avoid heavy `Application.onCreate`; measure `am start -W`.
- Memory/leaks: LeakCanary in debug, `dumpsys meminfo`, bitmap sizing, lifecycle-aware collectors.
- Rendering: Layout Inspector, overdraw, `dumpsys gfxinfo` jank percentages, Compose recomposition counts, avoid main-thread I/O.
- Battery/network: WorkManager constraints, batching, avoid wakelocks/polling; `dumpsys batterystats`.
- Output: baseline numbers, changes made, after numbers (only if measured), trade-offs.
