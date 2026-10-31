#!/usr/bin/env python3
"""Read-only APK inventory using only the Python standard library.

Never extracts or executes anything. Reads the ZIP directory, DEX headers and the
APK Signing Block. If `androguard` is installed, also decodes the binary manifest.

Usage: python3 apk_inventory.py app.apk [--json]
"""
import hashlib
import json
import struct
import sys
import zipfile
from collections import defaultdict

SIG_BLOCK_MAGIC = b"APK Sig Block 42"
SIG_IDS = {0x7109871A: "v2", 0xF05368C0: "v3", 0x1B93AD61: "v3.1", 0x42726577: "verity-padding"}

ENGINE_HINTS = {
    "Unity": ("libunity.so", "libil2cpp.so", "global-metadata.dat", "assets/bin/Data/"),
    "Unreal Engine": ("libUE4.so", "libUnreal.so"),
    "Godot": ("libgodot_android.so", ".pck"),
    "Cocos2d-x": ("libcocos2dcpp.so", "libcocos2djs.so", "libcocos.so"),
    "Flutter": ("libflutter.so", "libapp.so", "flutter_assets/"),
    "React Native": ("index.android.bundle", "libreactnativejni.so", "libhermes.so"),
    "Xamarin/.NET MAUI": ("libmonodroid.so", "assemblies/"),
    "Cordova/Capacitor/WebView": ("assets/www/", "assets/public/"),
    "libGDX": ("libgdx.so",),
}
PACKER_HINTS = ("libjiagu", "libsecexe", "libprotectClass", "libDexHelper", "libshell", "libegis",
                "libmobisec", "libnesec", "libddog", "libexec.so", "libBugly_Native")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dex_info(zf, name):
    with zf.open(name) as f:
        head = f.read(112)
    if len(head) < 112 or head[:4] != b"dex\n":
        return {"name": name, "valid": False}
    version = head[4:7].decode("ascii", "replace")
    strings, = struct.unpack_from("<I", head, 56)
    types, = struct.unpack_from("<I", head, 64)
    fields, = struct.unpack_from("<I", head, 80)
    methods, = struct.unpack_from("<I", head, 88)
    classes, = struct.unpack_from("<I", head, 96)
    return {"name": name, "valid": True, "version": version, "strings": strings, "types": types,
            "fields": fields, "methods": methods, "classes": classes, "size": zf.getinfo(name).file_size}


def signing_block(path):
    """Return list of v2+ scheme names found in the APK Signing Block."""
    with open(path, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        tail = min(size, 65535 + 22)
        f.seek(size - tail)
        data = f.read(tail)
        pos = data.rfind(b"PK\x05\x06")
        if pos < 0:
            return []
        cd_off, = struct.unpack_from("<I", data, pos + 16)
        if cd_off < 32:
            return []
        f.seek(cd_off - 24)
        footer = f.read(24)
        if footer[8:] != SIG_BLOCK_MAGIC:
            return []
        block_size, = struct.unpack_from("<Q", footer, 0)
        start = cd_off - block_size - 8
        if start < 0:
            return []
        f.seek(start + 8)
        pairs = f.read(block_size - 24) if block_size >= 24 else b""
    found, i = [], 0
    while i + 12 <= len(pairs):
        length, ident = struct.unpack_from("<QI", pairs, i)
        if length < 4:
            break
        found.append(SIG_IDS.get(ident, "id-0x%08x" % ident))
        i += 8 + length
    return found


def manifest_via_androguard(path):
    try:
        from androguard.core.apk import APK  # androguard >= 4
    except Exception:
        try:
            from androguard.core.bytecodes.apk import APK  # androguard 3.x
        except Exception:
            return None
    try:
        a = APK(path)
        return {
            "app_name": a.get_app_name(), "package": a.get_package(),
            "version_name": a.get_androidversion_name(), "version_code": a.get_androidversion_code(),
            "min_sdk": a.get_min_sdk_version(), "target_sdk": a.get_target_sdk_version(),
            "permissions": sorted(a.get_permissions()), "activities": a.get_activities(),
            "services": a.get_services(), "receivers": a.get_receivers(), "providers": a.get_providers(),
        }
    except Exception as exc:  # report, never guess
        return {"error": "androguard failed: %s" % exc}


def inventory(path):
    r = {"file": path, "sha256": sha256(path)}
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        r["size_bytes"] = sum(i.file_size for i in zf.infolist())
        r["entries"] = len(names)
        r["has_manifest"] = "AndroidManifest.xml" in names
        r["has_resources_arsc"] = "resources.arsc" in names
        r["is_aab"] = "BundleConfig.pb" in names
        dexes = sorted((n for n in names if n.startswith("classes") and n.endswith(".dex")),
                       key=lambda n: (len(n), n))
        r["dex"] = [dex_info(zf, n) for n in dexes]
        libs = defaultdict(list)
        for n in names:
            if n.startswith("lib/") and n.endswith(".so") and n.count("/") == 2:
                libs[n.split("/")[1]].append(n.split("/")[2])
        r["native_libs"] = {abi: sorted(v) for abi, v in sorted(libs.items())}
        r["res_files"] = sum(1 for n in names if n.startswith("res/"))
        r["asset_files"] = sum(1 for n in names if n.startswith("assets/"))
        r["largest_entries"] = [(i.filename, i.file_size) for i in
                                sorted(zf.infolist(), key=lambda i: -i.file_size)[:8]]
        meta = [n for n in names if n.startswith("META-INF/")]
        r["v1_signature_files"] = sorted(n for n in meta if n.upper().endswith((".RSA", ".DSA", ".EC", ".SF")))
        hints = [e for e, keys in ENGINE_HINTS.items() if any(k in n for n in names for k in keys)]
        r["framework_hints"] = sorted(hints)
        r["packer_hints"] = sorted({n for n in names for p in PACKER_HINTS if p in n})
    r["signing_block_schemes"] = signing_block(path)
    r["manifest"] = manifest_via_androguard(path)
    return r


def render(r):
    out = ["APK inventory (static, read-only)", "File: %s" % r["file"], "SHA-256: %s" % r["sha256"],
           "Uncompressed size: %.1f MB, entries: %d" % (r["size_bytes"] / 1048576, r["entries"])]
    if r["is_aab"]:
        out.append("NOTE: this is an Android App Bundle (.aab), not an installable APK.")
    out.append("Manifest present: %s | resources.arsc: %s" % (r["has_manifest"], r["has_resources_arsc"]))
    m = r["manifest"]
    if m and "error" not in m:
        out += ["Package: %s | Name: %s | Version: %s (%s)" % (m["package"], m["app_name"], m["version_name"], m["version_code"]),
                "minSdk %s / targetSdk %s" % (m["min_sdk"], m["target_sdk"]),
                "Permissions (%d), activities %d, services %d, receivers %d, providers %d" % (
                    len(m["permissions"]), len(m["activities"]), len(m["services"]), len(m["receivers"]), len(m["providers"]))]
    else:
        out.append("Manifest NOT decoded (%s). Use aapt2 dump badging, apkanalyzer manifest print, or apktool d." %
                   (m["error"] if m else "androguard not installed"))
    out.append("DEX files: %d" % len(r["dex"]))
    for d in r["dex"]:
        if d["valid"]:
            warn = "  <-- near 64K method limit" if d["methods"] > 60000 else ""
            out.append("  %s: dex v%s, %d classes, %d methods, %.1f KB%s" % (
                d["name"], d["version"], d["classes"], d["methods"], d["size"] / 1024, warn))
        else:
            out.append("  %s: INVALID or non-standard header (packed/encrypted?)" % d["name"])
    if r["native_libs"]:
        for abi, libs in r["native_libs"].items():
            out.append("Native libs [%s]: %d (%s%s)" % (abi, len(libs), ", ".join(libs[:6]), ", ..." if len(libs) > 6 else ""))
    else:
        out.append("Native libs: none")
    out.append("Resource files: %d | Asset files: %d" % (r["res_files"], r["asset_files"]))
    sig = []
    if r["v1_signature_files"]:
        sig.append("v1 (JAR)")
    sig += [s for s in r["signing_block_schemes"] if s != "verity-padding"]
    out.append("Signature schemes present: %s" % (", ".join(sig) if sig else "none found (unsigned)"))
    out.append("Certificate details are NOT read here. Run: apksigner verify --verbose --print-certs <apk>")
    if r["framework_hints"]:
        out.append("Framework hints (heuristic): %s" % ", ".join(r["framework_hints"]))
    if r["packer_hints"]:
        out.append("Possible packer/protector files (heuristic): %s" % ", ".join(r["packer_hints"]))
    out.append("Largest entries: " + "; ".join("%s (%.1f KB)" % (n, s / 1024) for n, s in r["largest_entries"][:5]))
    return "\n".join(out)


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    try:
        r = inventory(argv[1])
    except (OSError, zipfile.BadZipFile) as exc:
        print("ERROR: cannot read %s as a ZIP/APK: %s" % (argv[1], exc), file=sys.stderr)
        return 1
    print(json.dumps(r, indent=2) if "--json" in argv else render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
