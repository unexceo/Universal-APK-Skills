# Cursor adapter

1. Put the repository in your workspace (clone or submodule), e.g. `./universal-apk-skills/`.
2. Copy the loader rule: `mkdir -p .cursor/rules && cp universal-apk-skills/adapters/cursor/apk-skills.mdc .cursor/rules/`.
3. Optional, if your Cursor version supports Agent Skills: `universal-apk-skills/scripts/install/install.sh --target cursor --scope project --project-dir .`
4. In chat, say "Install this repository" or `/helpapk` (typed as text; Cursor does not register these as slash commands from this repo).

Cursor runs commands in its integrated terminal, so tools such as apktool and adb work if installed.
