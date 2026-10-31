---
description: "Replace launcher icon (adaptive and legacy densities)"
argument-hint: "<apk> <icon image>"
---
# /changeappicon

**Skill:** `modifyapk` · **Section:** `### /changeappicon` in `skills/modifyapk/SKILL.md`

Use the `modifyapk` skill and follow its `### /changeappicon` section.
User arguments: $ARGUMENTS
Follow `AGENTS.md` global rules (authorization, honesty, never modify the original).

| | |
|---|---|
| Purpose | Replace launcher icon (adaptive and legacy densities) |
| Needs | apktool; ImageMagick or Pillow |
| Produces | Updated mipmap/drawable files and diff |
| Usage | `/changeappicon <apk> <icon image>` |
