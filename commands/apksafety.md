---
description: "Pre-install safety verdict with evidence"
argument-hint: "<apk>"
---
# /apksafety

**Skill:** `androidsecurity` · **Section:** `### /apksafety` in `skills/androidsecurity/SKILL.md`

Use the `androidsecurity` skill and follow its `### /apksafety` section.
User arguments: $ARGUMENTS
Follow `AGENTS.md` global rules (authorization, honesty, never modify the original).

| | |
|---|---|
| Purpose | Pre-install safety verdict with evidence |
| Needs | Python 3; apksigner, aapt2 recommended |
| Produces | Risk rating, evidence, unchecked areas |
| Usage | `/apksafety <apk>` |
