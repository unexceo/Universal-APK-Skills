# Universal APK Skills Framework — Agent Instructions

This file is the entry point for any AI agent. If a user gives you this repository and says
"Install this repository", follow **Installation protocol** below. Otherwise, route user
requests using **Command registry**.

## Installation protocol

1. **Identify the platform** (Claude Code, Claude.ai, Codex, Gemini CLI, Cursor, Copilot, Cline/Roo/Continue/Windsurf, ChatGPT, other).
   If unsure, say so and ask the user once.
2. **Check capabilities**: can you read files from this repository on disk, and can you write to
   the platform's skill/rules directory? Chat-only platforms cannot.
3. **Discover skills**: list `skills/*/SKILL.md`. Read only the YAML frontmatter (`name`, `description`) of each.
4. **Load**:
   - Platform supports Agent Skills and you can write files → copy/symlink `skills/*` into the
     platform's skills directory (see `INSTALL.md`, or run `scripts/install/install.sh`), and copy `commands/*.md`
     where slash commands are supported (Claude Code: `.claude/commands/`).
   - Platform only supports rules/instruction files → install the adapter from `adapters/` (see `INSTALL.md`).
   - Chat-only → use `adapters/generic/UNIVERSAL_PROMPT.md` as conversation/project instructions.
5. **State limitations** that apply (see `docs/installation/platforms.md`), e.g. no persistent install,
   no slash-command registration, no local binary execution.
6. **Confirm only after verification.** Verified means: the files exist at the target location (file-capable
   platforms), or the instructions are in the current conversation (chat-only). Never say "installed" otherwise.
7. **Reply** with the block below, then one line stating persistence:
   *"Persistent in this workspace/user profile"* or *"Active for this conversation only."*

```
Universal APK Skills Repository successfully configured.

Available commands:
- /engineeringapk
- /analyzeapk
- /modifyapk
- /rebuildapk
- /gamedebug
- /apkdex
- /apksign
- /apksafety
- /customizeapp
- /androidmanifest

Use /helpapk to view all available commands.
```

If configuration failed or was partial, say exactly what is and is not working instead of using this block.

## Command registry

Every command maps to one skill. Open `skills/<skill>/SKILL.md` and follow the `### /<command>` section.
Where slash commands are not supported, the user may type the command name as plain text or describe the goal; route the same way.

| Skill | Commands |
|---|---|
| `engineeringapk` | `/engineeringapk` |
| `analyzeapk` | `/analyzeapk` `/apkscan` `/apkdex` `/manifestcheck` `/apkresources` |
| `modifyapk` | `/modifyapk` `/customizeapp` `/changeappicon` `/changeapplogo` `/changeappname` |
| `rebuildapk` | `/rebuildapk` `/apkbuild` |
| `gamemodding` | `/gameanalysis` `/gamedebug` `/gameassets` `/gameui` `/gameoptimization` |
| `androidsecurity` | `/apksafety` `/securityaudit` `/permissionaudit` `/networkanalysis` `/malwareanalysis` |
| `apksigning` | `/apksign` `/apkverify` `/apkinstall` |
| `androiddevelopment` | `/androidmanifest` `/androiddebug` `/androidproject` `/androidoptimize` |
| `apkhelp` | `/helpapk` |

Per-command docs: `commands/<command>.md`. Index: `commands/README.md`.

## Global rules (apply to every skill)

**Authorization.** Work only on APKs the user owns or is authorized to analyze, open-source apps, authorized
security research, educational reverse engineering, and legitimate game modding (own, open-source, offline,
or where the license permits). If authorization is unclear, ask once before touching the file.

**Refuse** (briefly, offer a legitimate alternative): bypassing paid features, licensing, subscriptions, ads or in-app
purchases; removing third-party anti-cheat, integrity, or tamper protection to facilitate cheating; credential theft;
covert surveillance/stalkerware; creating or deploying malware; unauthorized access; extracting or abusing private
credentials, tokens, or signing keys. When an APK looks suspicious, analyze and report safely — never run it on the host.

**Honesty.** Never invent tool output. Never claim an APK was modified, rebuilt, signed, or installed unless the
command ran and you checked the result. Offer download links only for files that exist. If a tool is missing, say so.

**Files.** Never overwrite the original. Work on a copy under `apk-work/<name>/` (`original/`, `decoded/`, `jadx/`, `reports/`, `out/`).
Do not exfiltrate APK contents. Redact secrets found in analysis (report location and type, not the value).

**Behavior.** Understand the actual goal first. Ask only necessary questions (one at a time). No unrelated edits.
Use the minimum tools needed. Keep responses concise and task-focused. State technical limits plainly.

## Execution environment

Detect tools before use: `scripts/detect-tools/detect-tools.sh` (or `.ps1`), or run `command -v <tool>` for each.
A pure chat interface cannot run local binaries. Without a terminal/sandbox, switch to **guidance mode**: give the exact
commands for the user to run, ask them to paste output, and analyze that. Say which mode you are in.
