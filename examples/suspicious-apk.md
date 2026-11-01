# Example: suspicious APK triage (illustrative transcript)

> Illustrative only.

**You:** /apksafety free-wallpapers.apk (a friend sent it, not from the Play Store)
**Agent:** I will not run it. SHA-256 recorded; check it yourself on a reputable hash-lookup service.
Evidence: requests `BIND_ACCESSIBILITY_SERVICE`, `RECEIVE_SMS`, `REQUEST_INSTALL_PACKAGES` (unrelated to wallpapers); contains an encrypted blob in `assets/`; uses `DexClassLoader`; debug certificate; package name resembles a known app.
Risk: **High**. Not checked: dynamic behavior, network traffic.
Next steps: do not install; if already installed, uninstall, revoke accessibility/device-admin rights, change passwords from a clean device. For a deeper static report use `/malwareanalysis`.
