# GitHub Copilot adapter

- **Instructions file (works broadly):** copy `adapters/copilot/copilot-instructions.md` to `.github/copilot-instructions.md` in your project, and keep the repository folder in the workspace. Copilot agent mode also reads a root `AGENTS.md` in recent versions; check your client's docs.
- **Agent Skills (where supported, e.g. recent VS Code agent mode):** `scripts/install/install.sh --target copilot --scope project --project-dir /path/to/project` installs into `.github/skills/`.
- Slash commands are not registered; type the command name as text.
- Terminal execution is available in agent mode with user approval; Copilot Chat on github.com cannot run local tools (guidance mode).
