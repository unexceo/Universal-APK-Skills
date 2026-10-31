---
description: "Rebuild a decoded APK with apktool and capture logs"
argument-hint: "<decoded dir>"
---
# /rebuildapk

**Skill:** `rebuildapk` · **Section:** `### /rebuildapk` in `skills/rebuildapk/SKILL.md`

Use the `rebuildapk` skill and follow its `### /rebuildapk` section.
User arguments: $ARGUMENTS
Follow `AGENTS.md` global rules (authorization, honesty, never modify the original).

| | |
|---|---|
| Purpose | Rebuild a decoded APK with apktool and capture logs |
| Needs | Java 17+, apktool |
| Produces | out/app-unsigned.apk, reports/build.log |
| Usage | `/rebuildapk <decoded dir>` |
