---
description: "Verify signature, alignment and package integrity"
argument-hint: "<apk>"
---
# /apkverify

**Skill:** `apksigning` · **Section:** `### /apkverify` in `skills/apksigning/SKILL.md`

Use the `apksigning` skill and follow its `### /apkverify` section.
User arguments: $ARGUMENTS
Follow `AGENTS.md` global rules (authorization, honesty, never modify the original).

| | |
|---|---|
| Purpose | Verify signature, alignment and package integrity |
| Needs | apksigner, zipalign, aapt2 |
| Produces | Pass/fail check list with output excerpts |
| Usage | `/apkverify <apk>` |
