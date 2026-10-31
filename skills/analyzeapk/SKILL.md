---
name: analyzeapk
description: Static analysis of Android APKs. Use for /analyzeapk, /apkscan, /apkdex, /manifestcheck and /apkresources, and whenever the user wants to inspect, decompile, triage or understand an APK's structure, manifest, DEX code, resources, assets, native libraries or signing, even if they only say "what's inside this APK". Read-only; never executes the app.
license: MIT
compatibility: Python 3 for the bundled inventory script. Optional apktool, jadx, aapt2, apkanalyzer, apksigner, baksmali, androguard. Chat-only mode works from pasted tool output.
metadata:
  version: "1.0.0"
---

# analyzeapk — static APK analysis

## Safety
- Only analyze APKs the user owns or is authorized to analyze, open-source apps, or educational samples. Ask once if unclear.
- Static only. Never install or run the sample on the host. For suspected malware use `androidsecurity` (`/malwareanalysis`).
- Report secrets by location and type, never the value. Never invent tool output. Work on a copy under `apk-work/<name>/`.

## Setup (all commands)
1. Copy the APK to `apk-work/<name>/original/` and record `sha256sum`.
2. Detect tools (`scripts/detect-tools/detect-tools.sh` or `command -v apktool jadx aapt2 apkanalyzer apksigner python3`). Use the minimum set; note what was missing and what it limited.
3. Always start with the inventory (no external tools needed):
   `python3 <this skill's folder>/scripts/apk_inventory.py original/app.apk` (from a repo checkout: `skills/analyzeapk/scripts/apk_inventory.py`) (add `--json` to save to `reports/inventory.json`).
   It lists ZIP structure, DEX headers (class/method counts), native libs by ABI, signature schemes present, framework/packer hints (heuristic). It does not decode the manifest or read certificates.
4. Decode once and reuse: `apktool d original/app.apk -o decoded` (resources, manifest, smali) and `jadx -d jadx original/app.apk` (Java/Kotlin-like source; expect decompile errors, use `--show-bad-code`).

## Commands

### /analyzeapk
Full static report. Run Setup, then:
1. Identity: `aapt2 dump badging app.apk` (package, version, SDKs, label, launchable activity, ABIs, densities).
2. Manifest and components: `/manifestcheck` logic. Resources: `/apkresources` logic. Code: `/apkdex` logic.
3. Signing: `apksigner verify --verbose --print-certs app.apk` (schemes v1–v4, cert SHA-256, debug-cert warning).
4. Native: list `lib/<abi>/*.so`; run `file`/`strings`/`readelf -d` on notable libs; Ghidra only if the user wants native depth.
5. Write `reports/analysis.md` (template: `docs/workflows/report-templates.md` in the repo): summary, identity, structure, components, permissions, code findings, resources, signing, risks, recommended next commands.
Verify every claim against tool output. Mark anything not checked as "not analyzed".

### /apkscan
Fast triage in under ~25 lines: inventory output, package/version/SDK, permission count with the 5 most sensitive, exported-component count, debuggable/allowBackup/cleartext flags, signature schemes, framework/packer hints, one-line verdict ("normal", "needs review", "suspicious: run /malwareanalysis") with the evidence for it. No decompile unless asked.

### /apkdex
Code-level analysis of DEX.
- Sizes and limits: method/class counts per DEX (inventory); multidex notes.
- Structure: top-level packages (`find jadx/sources -maxdepth 3 -type d`), main Application class, launcher activity, entry points from the manifest.
- Third-party SDKs: match package prefixes (e.g. `com.google.firebase`, `com.facebook`, `io.sentry`, ad/analytics SDKs) and list them with versions if present in `META-INF/*.version`.
- Obfuscation level: share of 1–2 letter class/method names (R8/ProGuard), presence of string encryption, reflection (`Class.forName`, `getMethod`), dynamic loading (`DexClassLoader`, `InMemoryDexClassLoader`), `System.loadLibrary`, JNI `native` methods, WebView `addJavascriptInterface`, `Runtime.exec`.
- Targeted search: `grep -rE "pattern" jadx/sources` for URLs, crypto (`Cipher.getInstance`, `MessageDigest`), storage, SQL, intents. Cross-check smali via `baksmali d classes.dex -o smali` when decompile output is `/* JADX WARN */` or missing.
- Output: package map, entry-point chain, SDK list, notable APIs with file:line, obfuscation rating, and what could not be decompiled. Do not paste large code dumps; quote minimal relevant snippets.

### /manifestcheck
Read `decoded/AndroidManifest.xml` (or `apkanalyzer manifest print`). Report:
- Identity/SDK: package, `versionCode`, `minSdkVersion`, `targetSdkVersion` (flag old targets: weaker platform protections).
- Application flags: `debuggable` (must be false in release), `allowBackup`, `usesCleartextTraffic`, `networkSecurityConfig`, `requestLegacyExternalStorage`, `extractNativeLibs`, `testOnly`.
- Components: every activity/service/receiver/provider with `exported` value and intent filters. Flag exported components without permission protection, implicit exports (intent-filter with no `exported` on targetSdk ≥ 31 is a build error), providers with `grantUriPermissions`, deep-link filters (`android:autoVerify`, browsable schemes).
- Permissions: declared custom permissions and their `protectionLevel`; `queries`; `foregroundServiceType`.
- Output a table (component, type, exported, filters, protection, note) plus a prioritized findings list. Editing the manifest is `modifyapk` or `androiddevelopment` (`/androidmanifest`).

### /apkresources
Inventory `decoded/res`, `assets`, `resources.arsc`.
- Counts and sizes by type and density (`drawable-*`, `mipmap-*`, `layout*`, `values*`, `xml`, `raw`, `font`, `anim`), locales (`values-xx`), night mode, adaptive icons (`mipmap-anydpi-v26`).
- Key values: `app_name` and other branding strings, colors, themes/styles, launcher icon files and manifest `android:icon`/`roundIcon`.
- Large/duplicated files (`sha256sum` dedupe), unused-resource hints (only if `apkanalyzer`/lint available; otherwise say "not checked"), unusual assets (databases, embedded APK/DEX/ELF, certificates, JSON configs). `apkanalyzer resources packages|configs|names` and `apkanalyzer files list` help.
- Output: summary table plus a list of files relevant to the user's goal (e.g. which files hold the icon, name, theme). Editing is `modifyapk`.

## Chat-only mode
Give the exact commands, ask the user to paste output (or upload the decoded `AndroidManifest.xml`, `strings.xml`), and analyze that. State that results come from pasted data. Uploaded APKs can still be inventoried with the Python script if the platform has a code sandbox.

## Common problems
- `apktool d` fails on framework resources → `apktool if framework-res.apk`; obfuscated resources → try `apktool d -r` (keep raw resources) for read-only inspection.
- `jadx` shows `Code decompiled incorrectly` → use baksmali/smali for that method; this is normal, not an APK defect.
- DEX header invalid or only a tiny stub DEX plus `lib*shell*.so` → likely packed; report it, don't attempt to unpack third-party protection.
