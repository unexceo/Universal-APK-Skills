# Modification workflow at a glance

```
original.apk (never edited)
   │ copy + sha256
   ▼
/apkscan ──► authorization / suitability check
   │
   ▼
apktool d ──► decoded/ (git init, base commit)
   │
   ▼
/changeappicon | /changeappname | /customizeapp | /modifyapk   (edit, git diff)
   │
   ▼
/rebuildapk ──► out/app-unsigned.apk + build.log
   │
   ▼
/apksign (zipalign → apksigner) ──► out/app-signed.apk
   │
   ▼
/apkverify ──► /apkinstall (optional) ──► report
```

Rules of thumb: one change set at a time; rebuild after each significant change; stop and report if the app enforces signature or integrity checks.
Data layout: `apk-work/<name>/{original,decoded,jadx,reports,out}`.
