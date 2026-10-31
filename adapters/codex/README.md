# OpenAI Codex adapter

- Codex reads `AGENTS.md` from the repository root, so opening this repo as the working directory already provides the routing and rules.
- Agent Skills: `scripts/install/install.sh --target agents` (user: `~/.agents/skills`) or `--scope project --project-dir <dir>` (`.agents/skills`). Older Codex builds read `~/.codex/skills`: use `--target custom --dest ~/.codex/skills`.
- Invoke by naming the skill or command in your prompt (for example "use the analyzeapk skill, /apkscan on app.apk"). Custom slash commands are not provided.
- Codex can run shell commands per your approval/sandbox settings. Network-restricted sandboxes cannot download tools or Gradle dependencies; install tools beforehand.
