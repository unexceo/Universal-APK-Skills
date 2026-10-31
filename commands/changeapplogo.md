---
description: "Replace in-app logo or splash images"
argument-hint: "<apk> <logo image>"
---
# /changeapplogo

**Skill:** `modifyapk` · **Section:** `### /changeapplogo` in `skills/modifyapk/SKILL.md`

Use the `modifyapk` skill and follow its `### /changeapplogo` section.
User arguments: $ARGUMENTS
Follow `AGENTS.md` global rules (authorization, honesty, never modify the original).

| | |
|---|---|
| Purpose | Replace in-app logo or splash images |
| Needs | apktool; ImageMagick or Pillow |
| Produces | Updated drawables/assets and diff |
| Usage | `/changeapplogo <apk> <logo image>` |
