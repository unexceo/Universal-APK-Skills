# Universal APK Skills

A modular AI skills framework for **legitimate Android APK reverse engineering, customization, rebuilding, signing, game modding and security analysis**. It uses the open Agent Skills format (`SKILL.md` folders) and ships adapters for Claude, Codex, Gemini, Cursor, Copilot, Cline/Roo/Continue/Windsurf and chat-only platforms such as ChatGPT.

> Use only on APKs you own or are authorized to analyze or modify. See [Safety](#safety-and-authorization).

## Install (quick start)
```bash
git clone https://github.com/unexceo/universal-apk-skills.git && cd universal-apk-skills
scripts/install/install.sh --target claude        # Claude Code: skills + slash commands
scripts/install/install.sh --target agents        # Codex and other .agents/skills readers
scripts/install/install.sh --target gemini        # Gemini CLI (skills directory)
```
Or give the repo to your agent and say **"Install this repository."** It follows [`AGENTS.md`](AGENTS.md) and replies with the command list. Chat-only products (ChatGPT, Gemini web): paste [`adapters/generic/UNIVERSAL_PROMPT.md`](adapters/generic/UNIVERSAL_PROMPT.md). Full instructions for every platform: [`INSTALL.md`](INSTALL.md).

Then run `/helpapk`.

## How skill installation works
Each folder in `skills/` has a `SKILL.md` with YAML metadata (name, description) and instructions. Agents keep the short metadata in context and load the full instructions only when a request matches or you name the command. `commands/` documents each command and doubles as Claude Code slash-command files. `AGENTS.md` is the router and rule set for agents that read it.

## Supported platforms
| Platform | Install | Slash commands | Runs tools locally |
|---|---|---|---|
| Claude Code | installer | Yes | Yes |
| Claude.ai / Desktop | skill upload / Project prompt | No (text) | Sandbox only |
| OpenAI Codex | `AGENTS.md` / installer | No (text) | Yes |
| Gemini CLI | extension / installer | No (text) | Yes |
| Cursor, GitHub Copilot, Cline, Roo Code, Continue, Windsurf | rules/loader or skills dir | No (text) | Yes, with approval |
| ChatGPT, Gemini web, other chat | paste prompt, attach files | No (text) | No |

Not every platform can install a repository or register slash commands. Where it cannot, the adapter gives the nearest working alternative and the agent must say so. Details: [`docs/installation/platforms.md`](docs/installation/platforms.md).

## Commands
Full index: [`commands/README.md`](commands/README.md). Each maps to one skill.

| Skill | Commands |
|---|---|
| [`engineeringapk`](skills/engineeringapk/SKILL.md) | `/engineeringapk` |
| [`analyzeapk`](skills/analyzeapk/SKILL.md) | `/analyzeapk` `/apkscan` `/apkdex` `/manifestcheck` `/apkresources` |
| [`modifyapk`](skills/modifyapk/SKILL.md) | `/modifyapk` `/customizeapp` `/changeappicon` `/changeapplogo` `/changeappname` |
| [`rebuildapk`](skills/rebuildapk/SKILL.md) | `/rebuildapk` `/apkbuild` |
| [`gamemodding`](skills/gamemodding/SKILL.md) | `/gameanalysis` `/gamedebug` `/gameassets` `/gameui` `/gameoptimization` |
| [`androidsecurity`](skills/androidsecurity/SKILL.md) | `/apksafety` `/securityaudit` `/permissionaudit` `/networkanalysis` `/malwareanalysis` |
| [`apksigning`](skills/apksigning/SKILL.md) | `/apksign` `/apkverify` `/apkinstall` |
| [`androiddevelopment`](skills/androiddevelopment/SKILL.md) | `/androidmanifest` `/androiddebug` `/androidproject` `/androidoptimize` |
| [`apkhelp`](skills/apkhelp/SKILL.md) | `/helpapk` |

## APK upload workflow and `/engineeringapk`
1. Run `/engineeringapk`. The agent checks tools and asks whether you are authorized to work on the app.
2. Upload your `.apk` (or place it in the working folder). The original is copied and hashed; it is never edited.
3. The agent inventories the APK: name, package, version, SDK levels, structure, manifest, permissions, components, resources, DEX files, native libraries, signing.
4. It asks: *"What type of reverse engineering or modification do you want to perform?"* with 14 options (structure analysis, DEX analysis, UI, icon, name/branding, manifest, resources, game modding, performance, network, security, debugging, rebuilding, custom development) or your own description.
5. It shows a plan, performs the work through the specialist skills, rebuilds, signs, validates, and delivers only files that really exist, plus a report and install notes.

Using the other skills: type the command with a file or goal, for example `/changeappname app.apk "My App"`, `/securityaudit app.apk`, `/apksign out/app-unsigned.apk`. Each skill's workflow is in its `SKILL.md`.

## Required external tools
JDK 17+, Python 3, Android SDK (adb, build-tools: aapt2, zipalign, apksigner; cmdline-tools: apkanalyzer), Apktool, JADX. Optional: Bundletool, Smali/Baksmali, Ghidra, Frida, MobSF, Androguard. Install guide for Windows, Linux and macOS: [`docs/installation/tools.md`](docs/installation/tools.md). Check what you have: `scripts/detect-tools/detect-tools.sh` (or `.ps1`).

## Platform limitations
- A chat interface cannot run local binaries. The agent works in **guidance mode** (gives commands, analyzes pasted output) unless it has a terminal or sandbox with the tools. The bundled Python inventory script needs only Python.
- Chat products keep installed instructions only inside that conversation, GPT, Gem or Project.
- A modified APK is re-signed, so it cannot update the original app, and features bound to the original signature may stop working.
- Obfuscated, packed or integrity-protected apps may not decode or rebuild; the agent reports this and does not defeat third-party protections.

## Safety and authorization
Intended for your own APKs, apps you are authorized to analyze, open-source apps, authorized security research, education, and legitimate game modding (own, open-source, offline, license-permitted).

The skills refuse: bypassing paid features or licensing; removing third-party anti-cheat or integrity protection to enable cheating; credential theft; covert surveillance; malware creation or deployment; unauthorized access; extracting or abusing private credentials, tokens or signing keys. Suspicious APKs are analyzed statically and reported safely. Details: [`AGENTS.md`](AGENTS.md), [`SECURITY.md`](SECURITY.md).

## Examples
- [Change icon and name (`/engineeringapk`)](examples/change-icon-and-name.md)
- [Security audit of your own app](examples/security-audit.md)
- [Suspicious APK triage](examples/suspicious-apk.md)

## Troubleshooting
See [`docs/troubleshooting/README.md`](docs/troubleshooting/README.md). Validate the repository: `pip install pyyaml && python3 scripts/validate/validate.py`.

## Repository layout
```
AGENTS.md  README.md  INSTALL.md  CONTRIBUTING.md  SECURITY.md  CHANGELOG.md  LICENSE
skills/<name>/SKILL.md      9 skills (+ analyzeapk/scripts/apk_inventory.py)
commands/<command>.md       31 command docs / Claude Code slash commands
adapters/                   claude cursor copilot codex gemini cline generic
scripts/                    install  detect-tools  validate
docs/                       installation  workflows  troubleshooting
examples/                   sample conversations
.github/                    CI workflow, issue and PR templates
```

License: MIT.
