# Contributing

## Add a skill
1. Create `skills/<name>/SKILL.md` (lowercase letters, digits, hyphens; folder name equals `name`). Frontmatter: `name`, `description` (what it does and when to use it, at most 1024 chars, a little "pushy" so it triggers), optional `license`, `compatibility`, `metadata` (string values).
2. Body under 500 lines: a short Safety section, then `## Commands` with one `### /command` heading per command. Put long reference material in `references/` inside the skill, scripts in `scripts/`. Skills must stay self-contained; do not link to files outside the skill folder.
3. For each command add `commands/<command>.md` (copy an existing one; it needs a `description`, and the `**Skill:** \`name\`` line).
4. Register the command in `AGENTS.md`, `skills/apkhelp/SKILL.md`, `README.md` and `commands/README.md`.
5. Run `python3 scripts/validate/validate.py` (needs `pip install pyyaml`). CI runs the same check.

## Rules
- No empty or placeholder skills; every command needs a real workflow.
- Never add workflows for licensing/paywall bypass, anti-cheat evasion, credential theft, surveillance or malware creation.
- Tool commands must be real; mark anything unverified. Do not invent results in examples that claim to be output from a real run.
- Keep instructions concise; avoid duplicating content that already lives in another skill.

## Pull requests
Describe the change, which commands are affected, and what you tested (platform, tool versions).
