---
description: "Zipalign and sign an APK with the user's keystore"
argument-hint: "<apk> [keystore]"
---
# /apksign

**Skill:** `apksigning` · **Section:** `### /apksign` in `skills/apksigning/SKILL.md`

Use the `apksigning` skill and follow its `### /apksign` section.
User arguments: $ARGUMENTS
Follow `AGENTS.md` global rules (authorization, honesty, never modify the original).

| | |
|---|---|
| Purpose | Zipalign and sign an APK with the user's keystore |
| Needs | build-tools (zipalign, apksigner), keytool |
| Produces | out/app-signed.apk, signing summary |
| Usage | `/apksign <apk> [keystore]` |
