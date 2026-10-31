---
description: "AndroidManifest audit: components, exported state, flags"
argument-hint: "<apk or decoded dir>"
---
# /manifestcheck

**Skill:** `analyzeapk` · **Section:** `### /manifestcheck` in `skills/analyzeapk/SKILL.md`

Use the `analyzeapk` skill and follow its `### /manifestcheck` section.
User arguments: $ARGUMENTS
Follow `AGENTS.md` global rules (authorization, honesty, never modify the original).

| | |
|---|---|
| Purpose | AndroidManifest audit: components, exported state, flags |
| Needs | apktool or aapt2/apkanalyzer |
| Produces | Component table and prioritized findings |
| Usage | `/manifestcheck <apk or decoded dir>` |
