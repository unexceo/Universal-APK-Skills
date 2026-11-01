# Example: security audit of your own app (illustrative transcript)

> Illustrative only; findings are examples, not a real run.

**You:** /securityaudit app-release.apk (my company's app, I'm authorized)
**Agent:** Running manifest checks, jadx decompile, targeted searches.
| ID | Severity | Area | Evidence | Remediation |
|---|---|---|---|---|
| F1 | High | Network | `network_security_config.xml` allows cleartext for `api.example.com` | Remove cleartext, enforce TLS |
| F2 | Medium | Platform | Exported service `SyncService` without permission (manifest line 48) | Set `exported=false` or add signature permission |
| F3 | Medium | Storage | API token in plain `SharedPreferences` (`AuthStore.java:61`) | Use EncryptedSharedPreferences/Keystore |
| F4 | Info | Resilience | R8 enabled; no root detection | Optional |
Secrets found: one key matching `AIza…****` in `res/values/strings.xml` (value redacted). Not checked: dynamic behavior, server side.
