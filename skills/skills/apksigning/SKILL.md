---
name: apksigning
description: Align, sign, verify and install Android APKs. Use for /apksign, /apkverify and /apkinstall, and whenever the user needs to sign a rebuilt or modified APK, create a test keystore, check signatures, certificates or zipalign alignment, compare signing keys, or install and launch an APK on a device or emulator with adb, including INSTALL_FAILED errors.
license: MIT
compatibility: Needs Android build-tools (apksigner, zipalign), JDK keytool, and adb for installs. Must run where those binaries exist; chat-only mode gives commands.
metadata:
  version: "1.0.0"
---

# apksigning — sign, verify, install

## Safety
- Sign only with keys the user owns. Never extract, request, guess, reuse or transmit someone else's private signing key or keystore password. Never ask the user to paste a keystore password into chat; have them export `KS_PASS` locally or use `--ks-pass env:KS_PASS`.
- Do not "fix" signature checks by removing protections from third-party apps.
- Debug/test keystores are for testing only; releases need the user's real release key kept offline.
- Do not claim signed/verified/installed without running the command and reading its output.

## Commands

### /apksign
Order matters: **zipalign first, then apksigner** (signing v2+ invalidates later alignment changes).
1. Align: `zipalign -p -f -v 4 out/app-unsigned.apk out/app-aligned.apk`
2. Keystore. If the user has one, use it. For a throw-away test key (user runs locally):
   `keytool -genkeypair -v -keystore test.keystore -alias test -keyalg RSA -keysize 2048 -validity 10000`
3. Sign: `apksigner sign --ks test.keystore --ks-key-alias test --ks-pass env:KS_PASS --out out/app-signed.apk out/app-aligned.apk`
   Options: `--v1-signing-enabled`/`--v2-signing-enabled`/`--v3-signing-enabled`/`--v4-signing-enabled true` (v4 produces an `.idsig` for incremental install), `--min-sdk-version N` to control whether v1 is added for old devices (apps with minSdk < 24 need v1 for pre-Nougat devices).
4. Always run `/apkverify` next. Report scheme list, certificate SHA-256 (from verify output), and the keystore path used (never the password).
Secondary: if `apksigner` is absent but a JDK exists, `jarsigner` produces v1-only signatures, which Android 11+ rejects for apps targeting API 30+; say so rather than silently using it.

### /apkverify
1. Signature: `apksigner verify --verbose --print-certs out/app-signed.apk`. Expect `Verified using v2 scheme: true` (and v3 as applicable). Print the certificate SHA-256 digest.
2. Alignment: `zipalign -c -v 4 out/app-signed.apk` (exit 0 = aligned).
3. Integrity and parse: `unzip -tq`, `aapt2 dump badging out/app-signed.apk | head -5`, optionally `apkanalyzer apk summary`.
4. Compare to original when relevant: signer digests differ → expected for re-signed apps; state consequences (cannot update over original, signature-bound features fail).
5. Report each check as pass / fail / not run, with the command output excerpt.

### /apkinstall
Requires a device or emulator and the user's consent for installation.
1. `adb devices -l` (state must be `device`; `unauthorized` → accept the RSA prompt; multiple devices → pass `-s <serial>` on every command).
2. Install: `adb install -r out/app-signed.apk` (`-d` allow downgrade, `-t` allow test-only, `-g` grant runtime permissions, `--user 0`). Split sets: `adb install-multiple base.apk split_*.apk`. AAB: `bundletool install-apks --apks=app.apks`.
3. Same package, different signature → `INSTALL_FAILED_UPDATE_INCOMPATIBLE`. **Ask before** `adb uninstall <package>` because it deletes app data; offer `adb shell pm path <pkg>` and a backup option first (`adb backup` is deprecated and often blocked; the user may need in-app export).
4. Launch check: `adb shell monkey -p <package> -c android.intent.category.LAUNCHER 1`, then `adb logcat -d -t 200 | grep -iE "AndroidRuntime|FATAL|<package>"`. Report crash or clean start.

| Error | Meaning / action |
|---|---|
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | Signature differs from installed app; uninstall (data loss) |
| `INSTALL_FAILED_VERSION_DOWNGRADE` | Lower versionCode; use `-d` (debuggable only) or uninstall |
| `INSTALL_PARSE_FAILED_NO_CERTIFICATES` / `...SIGNATURE...` | Unsigned or bad signature; re-run `/apksign` |
| `INSTALL_FAILED_OLDER_SDK` / `NEWER_SDK` | minSdk above device API; check `aapt2 dump badging` |
| `INSTALL_FAILED_NO_MATCHING_ABIS` | Native libs lack device ABI (e.g. arm64 APK on x86 emulator) |
| `INSTALL_FAILED_MISSING_SPLIT` | Split APK set incomplete; use `install-multiple` |
| `INSTALL_FAILED_USER_RESTRICTED` / `INSTALL_FAILED_ABORTED` | Device policy (e.g. USB install disabled); user must allow |
| `INSTALL_FAILED_INSUFFICIENT_STORAGE` | Free space |
