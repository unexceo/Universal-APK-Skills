---
description: "MASVS-style static security assessment"
argument-hint: "<apk or project>"
---
# /securityaudit

**Skill:** `androidsecurity` · **Section:** `### /securityaudit` in `skills/androidsecurity/SKILL.md`

Use the `androidsecurity` skill and follow its `### /securityaudit` section.
User arguments: $ARGUMENTS
Follow `AGENTS.md` global rules (authorization, honesty, never modify the original).

| | |
|---|---|
| Purpose | MASVS-style static security assessment |
| Needs | apktool, jadx; MobSF optional |
| Produces | Findings table with severity, evidence, remediation |
| Usage | `/securityaudit <apk or project>` |
