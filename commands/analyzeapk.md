---
description: "Full static analysis report of an APK"
argument-hint: "<apk>"
---
# /analyzeapk

**Skill:** `analyzeapk` · **Section:** `### /analyzeapk` in `skills/analyzeapk/SKILL.md`

Use the `analyzeapk` skill and follow its `### /analyzeapk` section.
User arguments: $ARGUMENTS
Follow `AGENTS.md` global rules (authorization, honesty, never modify the original).

| | |
|---|---|
| Purpose | Full static analysis report of an APK |
| Needs | Python 3; apktool, jadx, aapt2, apksigner recommended |
| Produces | reports/analysis.md, inventory.json |
| Usage | `/analyzeapk <apk>` |
