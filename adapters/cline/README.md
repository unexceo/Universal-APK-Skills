# Cline, Roo Code, Continue, Windsurf (rules-based agents)

These agents load rule files from a project folder; none of them auto-install this repository. Put the repo in your workspace
(e.g. `./universal-apk-skills/`) and copy `adapters/cline/apk-skills-rules.md` to the rules location:

| Agent | Copy to |
|---|---|
| Cline | `.clinerules/apk-skills.md` (or install skills with `--target cline` if your version supports Agent Skills) |
| Roo Code | `.roo/rules/apk-skills.md` |
| Continue | `.continue/rules/apk-skills.md` |
| Windsurf | `.windsurf/rules/apk-skills.md` |

Then ask "Install this repository" or type `/helpapk` as text (the agents' own slash-command systems are not used). These agents can run terminal commands with your approval, so local tools work if installed. Folder names change between versions; check each product's docs.
