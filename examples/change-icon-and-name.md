# Example: change icon and name (illustrative transcript)

> Illustrative only. Package names, hashes and results are made up to show the flow; they are not output from a real run.

**You:** /engineeringapk
**Agent:** Tools found: java, apktool, aapt2, apksigner, zipalign, adb (execute mode). Do you own this app or have permission to modify it?
**You:** Yes, it's my own app. (uploads `notes.apk`)
**Agent:** Copied to `apk-work/notes/original/`, SHA-256 recorded.
Package `com.example.notes`, version 2.1 (21), minSdk 24 / targetSdk 34, 2 DEX files, arm64-v8a + armeabi-v7a libs, signed with v2/v3 (debug certificate: no).
What type of reverse engineering or modification do you want to perform? (1–14 or describe)
**You:** 4 and 5. New name "Notes Plus", icon is `plus.png`.
**Agent:** Plan: decode → replace launcher icon (all mipmap densities + adaptive layers) → set `app_name` in all 6 locales → rebuild → zipalign + sign with your keystore → verify. Risk: the new signature cannot update the installed original. Proceed?
**You:** Go.
**Agent:** (runs the commands, shows `git diff --stat`, build exit code 0, `apksigner verify` output)
Delivered: `out/notes-signed.apk`, `reports/modification.md`. Install: uninstall the original (app data is lost), then `adb install out/notes-signed.apk`. Not tested on a physical device.
