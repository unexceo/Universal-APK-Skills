# Report templates

Fill only with verified data. Write "not checked" instead of guessing.

## Analysis report (`reports/analysis.md`)
```markdown
# APK analysis: <app name> <version>
- File: <name>  SHA-256: <hash>  Analyzed: <date>  Mode: execute | guidance
- Tools used: <list with versions>  Not available: <list>
## Summary (3-5 lines, verdict if relevant)
## Identity: package, versionName/versionCode, minSdk/targetSdk, ABIs, signing schemes + cert SHA-256
## Structure: DEX files (classes/methods), native libs, assets, notable files
## Components and permissions: table, exported items flagged
## Code findings: SDKs, entry points, obfuscation, notable APIs (path:line)
## Resources: branding strings, icons, themes
## Risks and limitations
## Recommended next commands
```

## Modification report (`reports/modification.md`)
```markdown
# Modification report: <app> -> <output file>
- Original SHA-256 / Output SHA-256: ...
- Request: <one sentence>
## Changes (file, before -> after)
## Build: tool+version, command, exit code, log path
## Signing: scheme(s), certificate SHA-256, keystore used (path only)
## Validation: archive test, badging, signature, zipalign, install/launch (pass / fail / not run)
## Known limitations: new signature (cannot update original), signature-bound features, untested devices
## Install: uninstall original (data loss), adb install -r <file>
```

## Security finding row
`| ID | Severity | MASVS area | Evidence (path:line / manifest) | Impact | Remediation | Confidence |`
