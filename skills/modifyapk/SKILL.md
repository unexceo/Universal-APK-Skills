---
name: modifyapk
description: Controlled modification of Android APKs the user owns or may modify. Use for /modifyapk, /customizeapp, /changeappicon, /changeapplogo and /changeappname, and whenever the user wants to rebrand, rename, re-icon, retheme, edit strings, colors, layouts, manifest values or resources of an APK. Works on a decoded copy, produces a diff, then hands off to rebuildapk and apksigning.
license: MIT
compatibility: Needs apktool and a text editor or scripting. Image conversion uses ImageMagick or Python Pillow when available. Chat-only mode gives edit instructions.
metadata:
  version: "1.0.0"
---

# modifyapk — resource and manifest modification

## Safety
- Modify only APKs the user owns, open-source apps (respect the license and trademarks), or apps the user is authorized to change.
- Refuse: removing paywalls/licensing/ads/IAP checks, patching out integrity or anti-tamper in third-party apps, injecting credential capture or surveillance, repackaging someone else's app to impersonate it or redistribute it under their branding.
- Never edit the original. Never claim success before rebuild and verification (`rebuildapk`, `apksigning`).

## Common procedure (all commands)
1. `apk-work/<name>/original/app.apk` stays untouched. Decode: `apktool d original/app.apk -o decoded` then `cd decoded && git init -q && git add -A && git commit -qm base` so every change is a reviewable diff.
2. State the exact change set (files and values) before editing. Make the smallest edits that achieve the goal.
3. After editing: `git diff --stat` and `git diff` summary; confirm only intended files changed.
4. Hand off: `/rebuildapk` → `/apksign` → `/apkverify`. Tell the user the result has a **new signature**: it cannot update over the original (uninstall first, app data is lost), and features tied to the original signature (Google Sign-In, Play Integrity, signature-bound API keys, license checks) may stop working. Do not work around those in third-party apps.
5. Report: files changed, before/after values, build/verify status, anything not tested.

## Commands

### /modifyapk
General-purpose entry. Clarify the goal in one question if needed, route to the specific command below when it fits, otherwise apply the common procedure to the requested resource/manifest edit. Typical safe edits: strings, colors, styles, dimens, layouts, drawables, manifest attributes (`android:label`, `android:icon`, `android:theme`, screen orientation, `usesCleartextTraffic` for the user's own debug use), `res/xml/network_security_config.xml` for own-app debugging. Smali edits only when the user owns the app and no source exists; keep them minimal, comment the intent in the report, and test.

### /customizeapp
UI customization at the resource level.
- Theme/colors: `res/values/colors.xml`, `styles.xml`/`themes.xml`, `values-night/`. Change the referenced color names rather than hard-coded hex in layouts when possible; grep for hard-coded values (`grep -rn "#[0-9A-Fa-f]\{6,8\}" res/ smali*`).
- Layout/spacing/text: `res/layout*/`, `dimens.xml`, `strings.xml` (all locales you touch). Keep IDs unchanged so code bindings still resolve.
- Fonts: `res/font/` and `android:fontFamily`; drawables: vector XML preferred; 9-patch files must remain `.9.png` and be compiled by apktool unchanged unless edited correctly.
- Apps drawing UI in code (Compose, games, WebView/Flutter/React Native assets) cannot be restyled through resources alone; say so and point to `assets/` bundles or to `/androidproject` for source-level work.

### /changeappicon
Launcher icon replacement.
1. Locate the icon: manifest `android:icon` and `android:roundIcon` (often `@mipmap/ic_launcher`, `@mipmap/ic_launcher_round`), then files in `res/mipmap-*` and `res/mipmap-anydpi-v26/ic_launcher.xml` (adaptive; references `ic_launcher_foreground`/`background`, optionally `monochrome` for Android 13 themed icons).
2. Get the user's source image (square PNG, ideally ≥ 1024×1024, transparent background for foreground). Do not fabricate artwork.
3. Generate sizes. Legacy launcher: mdpi 48, hdpi 72, xhdpi 96, xxhdpi 144, xxxhdpi 192 px. Adaptive layers: 108dp canvas = mdpi 108, hdpi 162, xhdpi 216, xxhdpi 324, xxxhdpi 432 px; keep important art inside the central 66dp (≈61%) safe zone.
   Example (ImageMagick): `magick icon.png -resize 192x192 res/mipmap-xxxhdpi/ic_launcher.png`; for foreground add `-gravity center -background none -extent` after resizing to ~61% of the layer size.
4. Replace every variant that exists (png/webp, round, foreground, background, monochrome). Keep file names and extensions consistent with the manifest and XML references; remove a stale `.webp` if you add a `.png` of the same name.
5. Verify: `aapt2 dump badging` after rebuild lists the new icon paths; render check by viewing the PNGs.

### /changeapplogo
In-app logo, splash and branding images (not the launcher icon).
- Find candidates: `grep -rIl "logo\|splash" res/ smali*`, `find res assets -iname "*logo*" -o -iname "*splash*"`, `res/drawable*/` and `assets/`. Android 12+ system splash uses `windowSplashScreenAnimatedIcon` in the theme.
- Replace with same-name files at each density (`drawable-mdpi` … `xxxhdpi`, or `drawable-nodpi`), same format and similar aspect ratio; mind alpha and 9-patch.
- If the logo is baked into a texture atlas, game bundle or web asset, say what additional tooling is required instead of guessing.

### /changeappname
App name and branding text.
1. `android:label` on `<application>` and on launcher `<activity>` in `AndroidManifest.xml` — usually `@string/app_name`.
2. Edit `res/values/strings.xml` `app_name` and **every** `res/values-*/strings.xml` that overrides it (otherwise those locales keep the old name). Also search other label strings (`app_name_short`, widget/shortcut labels in `res/xml/*`, notification text): `grep -rn "OldName" res/ AndroidManifest.xml`.
3. Do not change `package` or `applicationId` unless the user explicitly needs it and understands the risks (new app identity, broken references, providers/authorities, deep links, Firebase/Google config bound to the package). If requested, do it as a separate, documented change.
4. Ask for the exact new name and whether to apply to all locales when not stated.
5. Verify via `aapt2 dump badging` (`application-label` per locale).

## Limits to state plainly
Resource-only edits cannot change logic compiled in code. Obfuscated/protected apps may fail to decode or rebuild. AAB/split APKs need all splits handled (`rebuildapk`).
