# Claude adapter

## Claude Code (recommended: skills + slash commands)
```bash
git clone https://github.com/unexceo/AI-SKILLS-ENGINEERING.git
cd universal-apk-skills
scripts/install/install.sh --target claude                                  # user-wide: ~/.claude/skills + ~/.claude/commands
scripts/install/install.sh --target claude --scope project --project-dir /path/to/project   # one project
```
Then restart Claude Code and run `/helpapk`. Each file in `commands/` becomes a slash command; each folder in `skills/` is a skill Claude can also load on its own when your request matches its description.
Alternative without installing: open the repo as the working directory. `CLAUDE.md` imports `AGENTS.md`, which routes commands to `skills/`.

## Claude.ai, Claude Desktop (skills upload, guidance mode)
1. Zip each skill folder so the folder (containing `SKILL.md`) is the zip root's single entry, e.g. `cd skills && zip -r engineeringapk.zip engineeringapk`.
2. Upload through the Skills area in Settings (availability depends on your plan and feature flags; the menu name may change).
3. Skills are not slash commands there: type the command name or describe the goal.
4. The built-in code sandbox generally has no internet and none of the Android tools, so expect **guidance mode**: Claude gives commands, you run them locally and paste output. The Python inventory script can run in the sandbox on an uploaded APK.

No Skills upload? Use `adapters/generic/UNIVERSAL_PROMPT.md` as Project instructions.
