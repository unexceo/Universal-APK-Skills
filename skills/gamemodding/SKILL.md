---
name: gamemodding
description: Analysis and legitimate modding of Android game APKs. Use for /gameanalysis, /gamedebug, /gameassets, /gameui and /gameoptimization, and whenever the user wants to understand a game's engine and assets, debug crashes or lag, extract or replace permitted assets, adjust UI/HUD/fonts/scaling, or optimize performance, for their own games, open-source games, offline single-player games or where the license permits. Refuses cheating, anti-cheat bypass and monetization bypass.
license: MIT
compatibility: apktool, jadx, adb and Python 3. Engine-specific tools (e.g. AssetStudio, UABE for Unity, Il2CppDumper) are user-installed and optional. Chat-only mode gives guidance.
metadata:
  version: "1.0.0"
---

# gamemodding — game APK analysis and legitimate modding

## Safety gate (run first, every command)
Allowed: the user's own game, open-source games, offline/single-player games where modification is permitted by license or terms, learning and debugging.
Refuse, briefly, and offer a legitimate alternative (e.g. build your own mod in the open-source version, or a bug report to the developer):
- Cheating in online/multiplayer/server-validated games, aimbots, ESP, speed hacks, resource or currency injection.
- Removing or evading anti-cheat, root/emulator detection, integrity checks or obfuscation protections of third-party games.
- Bypassing licensing, paid unlocks, IAP, subscriptions or ads; stealing or redistributing copyrighted assets, or publishing modified copies.
Ask once if status is unclear: "Is this your game, open source, or a single-player offline game you're allowed to modify?" If the game has multiplayer, a server economy or anti-cheat, limit work to **read-only analysis and debugging of the user's own build**.
Never modify the original; work under `apk-work/<name>/`. Never invent tool output.

## Commands

### /gameanalysis
1. Inventory (`analyzeapk` script): ABIs, DEX count, native libs, large assets.
2. Identify engine by files (heuristic, confirm by opening them):
   | Engine | Indicators |
   |---|---|
   | Unity (IL2CPP) | `lib/*/libunity.so`, `libil2cpp.so`, `assets/bin/Data/Managed/Metadata/global-metadata.dat` |
   | Unity (Mono) | `libunity.so`, `libmono*.so`, `assets/bin/Data/Managed/Assembly-CSharp.dll` |
   | Unreal | `libUE4.so`/`libUnreal.so`, `.pak` files under `assets` or OBB |
   | Godot | `libgodot_android.so`, `assets/*.pck` |
   | Cocos2d-x | `libcocos2dcpp.so`/`libcocos2djs.so`, `assets/res`, `.jsc` |
   | libGDX | `libgdx.so`, `com.badlogic.gdx` classes |
   | Defold/GameMaker/Construct | engine libs, `game.arcd`/`game.droid`, `assets/www` |
3. Check `AndroidManifest.xml`, expansion files (OBB under `Android/obb/<pkg>`), network SDKs/server hosts (hand off `/networkanalysis`), anti-tamper/packer hints, online features.
4. Decide mod feasibility and risk, and state which parts are editable (resources, config, assets, scripts) versus compiled (IL2CPP/native).
5. Report: engine/version hints, structure, asset formats, online/offline verdict, safe next steps, and anything that must be refused.

### /gamedebug
Investigate crashes, freezes, ANRs, black screens, GPU issues for permitted builds.
- Device log: `adb logcat -b crash -d`, `adb logcat -d | grep -iE "FATAL|AndroidRuntime|Unity|libc|DEBUG|ANR"`; Unity prints under tag `Unity`.
- Native crash: pull tombstones/`adb bugreport`; symbolicate with `ndk-stack -sym <dir with .so symbols>` or `addr2line` using unstripped libs from the build.
- Java/Kotlin crash with R8: `retrace mapping.txt trace.txt`.
- ANR: `adb pull /data/anr/` (device-dependent) or bugreport; main-thread blocking, asset loading, shader compilation.
- Common causes: ABI mismatch (`INSTALL_FAILED_NO_MATCHING_ABIS` or `UnsatisfiedLinkError`), missing OBB/asset bundles, out-of-memory (`lowmemorykiller`, `OutOfMemoryError`), GPU driver shader issues (Vulkan vs GLES; engine settings), 16 KB page-size alignment problems on Android 15+ devices with `.so` files, `targetSdk` permission changes.
- Report: evidence excerpt, root-cause hypothesis ranked by confidence, a test to confirm, a fix or workaround.

### /gameassets
For permitted games only.
- List and size assets: `unzip -l`, `apkanalyzer files list`; OBB/expansion contents; engine containers (Unity `.assets`/`.unity3d` bundles, Unreal `.pak`, Godot `.pck`, Cocos `.jsc`/`.ccz`).
- Extraction with engine tools the user installs (AssetStudio / UABE for Unity bundles, `godotpcktool` for `.pck`, `u4pak`/`repak` for Unreal paks). Only run what the user has locally; do not claim extraction happened without the output files.
- Replacement: keep formats, dimensions, compression (ASTC/ETC2/PNG), mipmaps, atlas coordinates and file names; repack in the engine's format; mismatched sizes in atlases crash or garble rendering. Encrypted/signed bundles or server-verified assets → stop and report, do not break protection.
- Respect copyright: assets stay with the user's own project; do not redistribute extracted third-party assets.

### /gameui
Permitted games with resource- or asset-based UI.
- Native Android UI (splash, loading screens, native dialogs): `res/` edits per `modifyapk` conventions.
- Engine UI lives in assets (Unity UI prefabs/atlases, Godot scenes, Cocos JSON/`.jsc`, HTML5 in `assets/www`). Editable only when stored in an open or documented format and when rebuilding is feasible; compiled IL2CPP UI logic is not editable via resources.
- Typical safe changes: font replacement, text scaling/readability, HUD scale and safe-area offsets (notch/cutout: `layoutInDisplayCutoutMode`), orientation, colors/theme, localization strings.
- Test on at least one real/emulated screen aspect ratio and report the result, or "not tested".

### /gameoptimization
- Baseline: `adb shell dumpsys gfxinfo <pkg> framestats`, `adb shell dumpsys meminfo <pkg>`, `adb shell dumpsys batterystats`, Perfetto/Android GPU Inspector for traces, engine profiler for the user's own build.
- Size and load: texture compression (ASTC for modern devices, ETC2 fallback), atlasing, mip levels, audio compression, strip unused assets, split ABIs, Play Asset Delivery for large assets (own game).
- Runtime: frame pacing (Android Frame Pacing/Swappy), target FPS, draw call batching, overdraw, shader variants, GC allocations, thread priorities, thermal throttling; Vulkan vs GLES selection.
- Output: measured before/after numbers (only if measured), ranked recommendations with expected impact and risk. For own source projects hand off to `androiddevelopment` (`/androidoptimize`).
