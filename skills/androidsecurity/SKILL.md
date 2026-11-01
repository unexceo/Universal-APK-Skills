---
name: androidsecurity
description: Android app security analysis and safe handling of suspicious APKs. Use for /apksafety, /securityaudit, /permissionaudit, /networkanalysis and /malwareanalysis, and whenever the user asks if an APK is safe, wants a vulnerability or MASVS-style assessment, a permission review, network endpoint or TLS review, or a safe static analysis of suspected malware. Static-first, evidence-based, never runs samples on the host.
license: MIT
compatibility: Python 3 plus apktool, jadx, aapt2, apksigner; optional MobSF (Docker), androguard, Frida, mitmproxy or Burp for authorized dynamic tests on the user's own app and device. Chat-only mode analyzes pasted output.
metadata:
  version: "1.0.0"
---

# androidsecurity — security assessment and safe malware handling

## Safety
- Authorization first: own apps, apps the user is authorized to test (ask once; for third-party apps, written permission), open source, educational samples, or malware samples for defensive analysis.
- Refuse: building, improving, packaging or deploying malware or stalkerware; credential theft; using any credential, token, API key or private key found in an APK; attacking servers, C2 or backends; evading protections of third-party apps to enable abuse; weaponizing findings.
- Redact secrets: report type, file, line, and a masked prefix (e.g. `AKIA…****`), never the full value.
- Never invent findings. Every finding needs evidence (file path, manifest snippet, command output) and a confidence level. "Not found" means "not found by these checks".
- Work on a copy; static analysis only unless the user explicitly asks for dynamic work on their own app/device.

## Commands

### /apksafety
Pre-install safety verdict for an APK the user is considering installing.
1. Hash (`sha256sum`) and suggest the user check the hash on reputable services (e.g. VirusTotal hash lookup) themselves; do not upload their file without consent.
2. Run `/apkscan` (inventory, permissions, flags). Verify signing: `apksigner verify --print-certs`; compare the certificate SHA-256 against the publisher's published value or the installed/Play version (`adb shell dumpsys package <pkg> | grep -i sign`). A mismatch with the claimed publisher is a strong red flag.
3. Red flags: debug certificate, high-risk permissions unrelated to purpose (SMS, accessibility, device admin, overlay, install packages), packer/dropper hints, dynamic code loading, hard-coded unknown endpoints, `testOnly`, package name impersonating a known app.
4. Output: **Low / Medium / High risk / Cannot determine**, a bullet list of evidence, what was not checked, and the safest next step (install from the official store, analyze deeper with `/malwareanalysis`). State that no static check can prove an app is safe.

### /securityaudit
OWASP MASVS-oriented static assessment (areas: storage, crypto, auth, network, platform interaction, code quality, resilience).
1. `/manifestcheck` logic: debuggable, allowBackup, cleartext, exported components/providers, deep links, permissions, `networkSecurityConfig`.
2. Code (`jadx`): hard-coded secrets (`grep -rnE "(api[_-]?key|secret|token|password|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35})"`), insecure storage (`MODE_WORLD_*`, external storage, plain SharedPreferences/SQLite for sensitive data, `Log.*` of sensitive values), weak crypto (`DES`, `ECB`, `MD5`/`SHA1` for security, static IV/keys, `java.util.Random` for tokens), WebView (`setJavaScriptEnabled`, `addJavascriptInterface`, `setAllowFileAccess*`, `loadUrl` of untrusted input), TLS (`TrustManager` that accepts all, `HostnameVerifier` returning true, `onReceivedSslError` → `proceed()`), intent redirection/PendingIntent mutability, SQL string concatenation, zip-slip, clipboard/screenshot protection (`FLAG_SECURE`).
3. Resilience (informational): obfuscation, root detection, integrity checks — report presence; do not remove them in third-party apps.
4. Output table: ID, severity (Critical/High/Medium/Low/Info), MASVS area, evidence (path:line), impact, remediation, confidence. Optionally run MobSF (`docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest`) and treat its output as leads to verify.

### /permissionaudit
1. List permissions from `aapt2 dump permissions app.apk` (or decoded manifest), including `uses-permission-sdk-23`, custom permissions, and `maxSdkVersion`.
2. Classify: normal vs dangerous (runtime) vs special/appop (`SYSTEM_ALERT_WINDOW`, `MANAGE_EXTERNAL_STORAGE`, `REQUEST_INSTALL_PACKAGES`, `BIND_ACCESSIBILITY_SERVICE`, `BIND_DEVICE_ADMIN`, `QUERY_ALL_PACKAGES`, `READ_SMS/RECEIVE_SMS`, `READ_CALL_LOG`, `ACCESS_BACKGROUND_LOCATION`, `POST_NOTIFICATIONS`, `FOREGROUND_SERVICE_*`).
3. Compare against the app's stated purpose and evidence of use in code (`grep` for the matching APIs). Mark each: justified / questionable / unused-looking (candidate for removal).
4. Output table with permission, protection level, purpose, usage evidence, verdict, recommendation. For the user's own app, recommend minimum permissions and runtime-request UX; for third-party apps, informative only.

### /networkanalysis
Static first.
1. Extract endpoints: `grep -rhoE "https?://[A-Za-z0-9./:_?=&%-]+" jadx/sources decoded/res decoded/assets | sort -u`; also `wss://`, IP literals, Firebase/Google/ad/analytics hosts. Classify first-party vs SDK. Redact tokens in URLs.
2. Transport security: `usesCleartextTraffic`, `res/xml/network_security_config.xml` (domain configs, user-CA trust, pinning `<pin-set>`), custom `TrustManager`, OkHttp `CertificatePinner`, WebView SSL handling.
3. API behavior: libraries (Retrofit/OkHttp/Volley/gRPC/GraphQL), auth headers/token storage hints, request signing, endpoints requiring user data.
4. Dynamic capture only for the user's own app or with written authorization, on a user device/emulator via a proxy (mitmproxy/Burp). For the user's own debug build, allow the proxy CA with a debug-only `network-security-config`. Do not provide bypass tooling or scripts to defeat pinning/integrity in third-party apps. Frida use is limited to the user's own app and authorized tests.
5. Output: endpoint table (host, scheme, purpose guess, evidence), transport findings, privacy notes (data sent to third parties, if evidenced), recommendations.

### /malwareanalysis
Defensive analysis of a suspicious APK.
- Handling: never run it on the host or a personal phone. Static analysis only unless the user has an isolated emulator/VM with snapshots and no personal accounts; if so, run networking off or through a controlled sink and say that dynamic analysis is the user's responsibility. Do not contact any C2 or server found.
- Triage: hash, `/apkscan`, signing, packer hints, native libs, assets that are DEX/ELF/APK/encrypted blobs.
- Behavior indicators (cite evidence): accessibility-service abuse, overlay attacks, SMS/call-log access, device admin, `REQUEST_INSTALL_PACKAGES`, dynamic code loading, reflection-heavy string decoding, hidden launcher/icon hiding (`setComponentEnabledSetting`), foreground-service persistence, screen capture/`MediaProjection`, keylogging via accessibility, exfil endpoints, crypto/stealer patterns. Map to MITRE ATT&CK for Mobile technique IDs when confident.
- Output: verdict (Malicious / Suspicious / Unwanted / Benign-appearing / Inconclusive) with confidence, IOC list (hashes, domains, IPs, package, certificate SHA-256, file names) defanged (`hxxp://`, `example[.]com`), behavior summary, user remediation (uninstall steps, revoke accessibility/admin rights, change credentials from a clean device, report to the platform/CERT). No functioning exploit or improved malware code.
