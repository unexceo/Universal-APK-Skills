# External tools

Run `scripts/detect-tools/detect-tools.sh` (Linux/macOS) or `detect-tools.ps1` (Windows) to see what is installed. Versions and package names change; prefer official project pages when a command fails.

| Tool | Used for | Commands |
|---|---|---|
| JDK 17+ (includes `keytool`) | Everything Java-based | all build/sign |
| Python 3.9+ | Inventory script, validator | `/apkscan`, `/analyzeapk` |
| Android SDK: platform-tools (`adb`), build-tools (`aapt2`, `zipalign`, `apksigner`), cmdline-tools (`apkanalyzer`) | Inspect, sign, install | most |
| Apktool | Decode/rebuild resources and smali | `/modifyapk`, `/rebuildapk` |
| JADX | Decompile DEX to Java | `/apkdex`, `/securityaudit` |
| Smali/Baksmali | Edit/inspect Dalvik bytecode | `/apkdex` |
| Bundletool | AAB → APKs | `/rebuildapk` |
| Ghidra | Native `.so` analysis | optional |
| Frida | Dynamic instrumentation of **your own** app | optional, `/networkanalysis` |
| MobSF (Docker) | Automated mobile static analysis | optional, `/securityaudit` |
| Androguard (`pip install androguard`) | Python APK/manifest parsing; enriches inventory output | optional |
| ImageMagick or Pillow | Icon/logo resizing | `/changeappicon` |

## Linux (Debian/Ubuntu)
```bash
sudo apt update && sudo apt install -y openjdk-17-jdk python3 python3-pip unzip git imagemagick adb apktool jadx
pip install --user androguard
```
Distro packages for `apktool`/`jadx` may be outdated or absent. Then use the official releases: Apktool (`apktool.jar` + wrapper script from the Apktool site), JADX (release zip from the jadx GitHub project), and install the SDK command-line tools from developer.android.com, then:
```bash
sdkmanager "platform-tools" "build-tools;<latest>" "cmdline-tools;latest"
export ANDROID_HOME="$HOME/Android/Sdk"; export PATH="$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/<version>:$ANDROID_HOME/cmdline-tools/latest/bin"
```

## macOS (Homebrew)
```bash
brew install openjdk@17 python git imagemagick apktool jadx android-platform-tools
brew install --cask android-commandlinetools
pip3 install --user androguard
```
Then `sdkmanager "build-tools;<latest>"` and add build-tools to `PATH`.

## Windows
Use winget/Scoop/Chocolatey where packages exist, or official downloads:
```powershell
winget install EclipseAdoptium.Temurin.17.JDK Python.Python.3.12 Git.Git
scoop install apktool jadx adb   # Scoop (https://scoop.sh), if you use it
```
Install Android command-line tools from developer.android.com, run `sdkmanager`, add `platform-tools` and `build-tools\<version>` to `PATH`, set `ANDROID_HOME`. WSL2 (Ubuntu) is a good alternative: follow the Linux steps (USB `adb` needs extra setup; use network `adb` or Windows `adb`).

## MobSF (optional)
```bash
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest
```

## Verify
```bash
java -version && apktool --version && jadx --version && aapt2 version && apksigner --version && adb version
```
