# Platform compatibility and limitations

Reviewed October 2026 against public ecosystem documentation. **This repository's file layout is validated by `scripts/validate/validate.py` and the installer was exercised on a Linux filesystem. It has not been tested inside each vendor's product.** Vendors change folder names and features; check their docs if something is not picked up.

| Platform | How to install | Persistent | Real slash commands | Can run local tools | Notes |
|---|---|---|---|---|---|
| Claude Code | `install.sh --target claude` | Yes (skills + commands) | Yes (`commands/*.md`) | Yes (Bash tool) | Best experience |
| Claude.ai / Desktop | Upload zipped skill folders, or Project instructions | While uploaded | No | Sandbox only; usually no network, no Android tools | Guidance mode + Python inventory |
| OpenAI Codex | `AGENTS.md` at repo root; `install.sh --target agents` | Yes | No | Yes, per sandbox/approval settings | Skills path `.agents/skills` (legacy `~/.codex/skills`) |
| Gemini CLI | `gemini extensions install <repo URL>` or `--target gemini` | Yes | No (TOML commands not included) | Yes, with approval | `GEMINI.md` → `AGENTS.md` |
| Cursor | Loader rule in `.cursor/rules/`; optional `--target cursor` | Per project | No | Yes (terminal) | Skills support depends on version |
| GitHub Copilot | `.github/copilot-instructions.md`; optional `--target copilot` | Per project | No | Agent mode terminal with approval | Skills support depends on client |
| Cline / Roo Code / Continue / Windsurf | Loader rule in the agent's rules folder | Per project | No | Yes, with approval | See `adapters/cline/README.md` |
| ChatGPT / Gemini web / any chat | Paste `adapters/generic/UNIVERSAL_PROMPT.md` | Only inside that GPT/Gem/Project | No | No (code sandbox at most) | Guidance mode |
| Other Agent Skills agents | `install.sh --target agents` or `--target custom --dest DIR` | Yes | Varies | Varies | Anything reading `SKILL.md` directories |

## What "installed" means
- **Skills installed:** the agent discovers `SKILL.md` metadata and loads a skill when the request matches or the command is named.
- **Slash commands:** only Claude Code registers the `commands/*.md` files. Elsewhere `/engineeringapk` is a text trigger that the agent maps to a skill via `AGENTS.md`.
- **Conversation-only:** chat products keep the instructions only in that conversation, GPT, Gem or Project.

## Features that need a local execution environment
Decoding/rebuilding (`apktool`), decompiling (`jadx`), signing (`apksigner`, `zipalign`), installing (`adb`), Gradle builds (`/apkbuild`), `bundletool`, Frida, MobSF, Ghidra. Without a terminal the assistant can only give commands and analyze pasted output, plus the Python inventory when a code sandbox exists.
