---
description: "Controlled APK modification on a decoded copy with a diff"
argument-hint: "<apk> <change>"
---
# /modifyapk

**Skill:** `modifyapk` · **Section:** `### /modifyapk` in `skills/modifyapk/SKILL.md`

Use the `modifyapk` skill and follow its `### /modifyapk` section.
User arguments: $ARGUMENTS
Follow `AGENTS.md` global rules (authorization, honesty, never modify the original).

| | |
|---|---|
| Purpose | Controlled APK modification on a decoded copy with a diff |
| Needs | apktool; git |
| Produces | Edited decoded project, diff summary, handoff to rebuild |
| Usage | `/modifyapk <apk> <change>` |
