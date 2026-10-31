# Installation

Replace `YOUR_USER` with the GitHub account that hosts this repository.

## 0. Get the repository
```bash
git clone https://github.com/YOUR_USER/universal-apk-skills.git
cd universal-apk-skills
python3 scripts/validate/validate.py     # optional: checks the repo (needs: pip install pyyaml)
```

## 1. One-line installer for file-capable agents
```bash
scripts/install/install.sh --target <claude|agents|gemini|cursor|copilot|cline|custom> [--scope user|project --project-dir DIR] [--dest DIR] [--link] [--force]
scripts/install/install.sh --target claude --uninstall      # remove
```
Windows: `.\scripts\install\install.ps1 -Target claude` (same options; not tested on every PowerShell version).

| Target | User scope | Project scope | Slash commands |
|---|---|---|---|
| `claude` | `~/.claude/skills` | `<project>/.claude/skills` | `~/.claude/commands`, `<project>/.claude/commands` |
| `agents` (Codex and other `.agents/skills` readers) | `~/.agents/skills` | `<project>/.agents/skills` | no |
| `gemini` | `~/.gemini/skills` | `<project>/.gemini/skills` | no |
| `cursor` | `~/.cursor/skills` | `<project>/.cursor/skills` | no |
| `copilot` | `~/.copilot/skills` | `<project>/.github/skills` | no |
| `cline` | `~/.cline/skills` | `<project>/.cline/skills` | no |
| `custom` | `--dest DIR` | `--dest DIR` | no |

The script copies each `skills/<name>/` folder (or symlinks with `--link`), skips existing ones unless `--force`, then verifies that every `SKILL.md` exists at the target. Restart the agent afterwards.
Third-party alternative: `npx skills add YOUR_USER/universal-apk-skills` installs Agent Skills repositories into many agents; check that tool's documentation.

## 2. Per platform
- **Claude Code:** `scripts/install/install.sh --target claude`, restart, run `/helpapk`. Details: `adapters/claude/README.md`.
- **Claude.ai / Desktop:** upload zipped skill folders or use Project instructions. See `adapters/claude/README.md`.
- **Codex:** open the repo (reads `AGENTS.md`) or `--target agents`. See `adapters/codex/README.md`.
- **Gemini CLI:** `gemini extensions install https://github.com/YOUR_USER/universal-apk-skills` or `--target gemini`. See `adapters/gemini/README.md`.
- **Cursor:** copy `adapters/cursor/apk-skills.mdc` to `.cursor/rules/`. See `adapters/cursor/README.md`.
- **GitHub Copilot:** copy `adapters/copilot/copilot-instructions.md` to `.github/copilot-instructions.md`. See `adapters/copilot/README.md`.
- **Cline, Roo Code, Continue, Windsurf:** copy the loader rule. See `adapters/cline/README.md`.
- **ChatGPT, Gemini web, any chat:** paste `adapters/generic/UNIVERSAL_PROMPT.md`. See `adapters/generic/README.md`.

## 3. "Install this repository" (agent-driven)
Give the agent the repository (URL or folder) and say: **Install this repository.** The agent follows the protocol in `AGENTS.md`: identify platform, read instructions, discover skills, load them, state limitations, and confirm only after verification. If it cannot write to its skills folder it will tell you what it did instead.

## 4. External tools
Skills work without tools in guidance mode, but decoding, building, signing and installing need them. See `docs/installation/tools.md` and run `scripts/detect-tools/detect-tools.sh`.

## 5. Verify
In the agent, run `/helpapk` (or ask "list the APK skills"). Expect the command table and the current mode (execute/guidance).
