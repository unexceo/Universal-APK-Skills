# Commands

Each command maps to one skill section. In Claude Code the files in this folder (except this one) are installed as slash commands
(`.claude/commands/`). On other platforms the command name is a plain-text trigger: the agent routes it using `AGENTS.md`.

| Command | Skill | Purpose |
|---|---|---|
| [`/engineeringapk`](engineeringapk.md) | `engineeringapk` | Guided end-to-end APK reverse engineering: upload, inspect, choose task, execute, rebuild, validate, deliver |
| [`/analyzeapk`](analyzeapk.md) | `analyzeapk` | Full static analysis report of an APK |
| [`/apkscan`](apkscan.md) | `analyzeapk` | Fast triage summary with red flags |
| [`/apkdex`](apkdex.md) | `analyzeapk` | DEX and source analysis: packages, SDKs, entry points, obfuscation |
| [`/manifestcheck`](manifestcheck.md) | `analyzeapk` | AndroidManifest audit: components, exported state, flags |
| [`/apkresources`](apkresources.md) | `analyzeapk` | Resource, asset and string inventory |
| [`/modifyapk`](modifyapk.md) | `modifyapk` | Controlled APK modification on a decoded copy with a diff |
| [`/customizeapp`](customizeapp.md) | `modifyapk` | UI customization: colors, themes, layouts, strings, fonts |
| [`/changeappicon`](changeappicon.md) | `modifyapk` | Replace launcher icon (adaptive and legacy densities) |
| [`/changeapplogo`](changeapplogo.md) | `modifyapk` | Replace in-app logo or splash images |
| [`/changeappname`](changeappname.md) | `modifyapk` | Change app name and labels across locales |
| [`/rebuildapk`](rebuildapk.md) | `rebuildapk` | Rebuild a decoded APK with apktool and capture logs |
| [`/apkbuild`](apkbuild.md) | `rebuildapk` | Build APK/AAB from an Android Gradle project |
| [`/gameanalysis`](gameanalysis.md) | `gamemodding` | Identify game engine, assets and online/offline status; check modding eligibility |
| [`/gamedebug`](gamedebug.md) | `gamemodding` | Investigate game crashes, freezes, ANRs and GPU issues |
| [`/gameassets`](gameassets.md) | `gamemodding` | Inventory and handle assets for permitted games |
| [`/gameui`](gameui.md) | `gamemodding` | HUD, menu, font and scaling changes for permitted games |
| [`/gameoptimization`](gameoptimization.md) | `gamemodding` | Game performance, memory and size tuning |
| [`/apksafety`](apksafety.md) | `androidsecurity` | Pre-install safety verdict with evidence |
| [`/securityaudit`](securityaudit.md) | `androidsecurity` | MASVS-style static security assessment |
| [`/permissionaudit`](permissionaudit.md) | `androidsecurity` | Permission review against app purpose and code usage |
| [`/networkanalysis`](networkanalysis.md) | `androidsecurity` | Endpoints, TLS/cleartext and pinning configuration review |
| [`/malwareanalysis`](malwareanalysis.md) | `androidsecurity` | Safe static analysis of a suspicious APK |
| [`/apksign`](apksign.md) | `apksigning` | Zipalign and sign an APK with the user's keystore |
| [`/apkverify`](apkverify.md) | `apksigning` | Verify signature, alignment and package integrity |
| [`/apkinstall`](apkinstall.md) | `apksigning` | Install and launch an APK via adb and diagnose failures |
| [`/androidmanifest`](androidmanifest.md) | `androiddevelopment` | Write or fix AndroidManifest.xml in a project or decoded APK |
| [`/androiddebug`](androiddebug.md) | `androiddevelopment` | Logcat, crash, ANR and R8 stack-trace triage |
| [`/androidproject`](androidproject.md) | `androiddevelopment` | Scaffold or continue an Android project from analysis |
| [`/androidoptimize`](androidoptimize.md) | `androiddevelopment` | Size, startup, memory, rendering and battery optimization |
| [`/helpapk`](helpapk.md) | `apkhelp` | List all commands and the current execution mode |

Use `/helpapk` for the grouped list and current execution mode. To add a command see `CONTRIBUTING.md`.
