# Gemini adapter

## Gemini CLI
- **Extension:** `gemini extensions install https://github.com/unexceo/universal-apk-skills` (uses `gemini-extension.json` and `GEMINI.md` at the repo root, which points to `AGENTS.md`).
- **Skills directory (if your version supports Agent Skills):** `scripts/install/install.sh --target gemini` (user: `~/.gemini/skills`) or `--scope project --project-dir <dir>`.
- **Context only:** run `gemini` inside the cloned repo; it loads `GEMINI.md`.
- Commands are plain-text triggers; custom Gemini CLI TOML commands are not included.

## Gemini web / Gems
No repository install. Create a Gem with `adapters/generic/UNIVERSAL_PROMPT.md` as instructions and attach `AGENTS.md` plus the `skills/*/SKILL.md` files as knowledge. Guidance mode only (no local binaries).
