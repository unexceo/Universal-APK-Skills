# Troubleshooting

| Problem | Fix |
|---|---|
| Agent says "installed" but commands do nothing | Check files exist (`ls ~/.claude/skills/engineeringapk/SKILL.md`), restart the agent, run `/helpapk`. On chat products the install is conversation-only. |
| Slash command not recognized | Only Claude Code registers `commands/*.md`. Elsewhere type the command as text. |
| `detect-tools` shows tools MISSING but you installed them | Not on `PATH`. Add Android build-tools/platform-tools to `PATH` or set `ANDROID_HOME`. |
| APK upload not visible to the assistant | Re-upload; some chats limit file size/type. Provide hash and run the script locally. |
| `apktool d` fails: framework / resource errors | `apktool if framework-res.apk`; update apktool; try `apktool d -r` for read-only. |
| `apktool b` fails | Read the first error in `reports/build.log`; `git diff` in `decoded/` shows what you changed. |
| `apksigner: command not found` | It lives in `build-tools/<version>/`; add to `PATH`. Needs JDK. |
| App crashes after rebuild | `adb logcat -d | grep -i FATAL`; check removed resources, ABI libs, and integrity checks (reported, not bypassed). |
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | Signature differs; uninstall original (deletes app data). |
| Game works only online / refuses | Online games are limited to read-only analysis of your own build. |
| Validator fails | Run `python3 scripts/validate/validate.py`; each line names the file and problem. |
