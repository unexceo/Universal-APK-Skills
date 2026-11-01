#!/usr/bin/env python3
"""Validate the repository: skill format, command mapping, links, config files, script syntax.

Usage: python3 scripts/validate/validate.py      (exit 1 on any error)
Requires PyYAML (pip install pyyaml).
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[2]
errors, notes = [], []


def err(msg):
    errors.append(msg)


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        err(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return None, text
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as exc:
        err(f"{path.relative_to(ROOT)}: invalid YAML frontmatter: {exc}")
        return None, m.group(2)
    return data, m.group(2)


# --- Skills (Agent Skills format) -------------------------------------------------
skills = {}
for skill_md in sorted((ROOT / "skills").glob("*/SKILL.md")):
    d = skill_md.parent.name
    fm, body = frontmatter(skill_md)
    rel = skill_md.relative_to(ROOT)
    if fm is None:
        continue
    name, desc = fm.get("name"), fm.get("description")
    if name != d:
        err(f"{rel}: name '{name}' must equal directory '{d}'")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name or "") or len(name) > 64:
        err(f"{rel}: invalid name")
    if not isinstance(desc, str) or not desc.strip():
        err(f"{rel}: description missing")
    elif len(desc) > 1024:
        err(f"{rel}: description is {len(desc)} chars (max 1024)")
    comp = fm.get("compatibility")
    if comp is not None and (not isinstance(comp, str) or len(comp) > 500):
        err(f"{rel}: compatibility must be a string of at most 500 chars")
    meta = fm.get("metadata")
    if meta is not None and not (isinstance(meta, dict) and all(isinstance(v, str) for v in meta.values())):
        err(f"{rel}: metadata values must be strings")
    lines = len(body.splitlines())
    if lines > 500:
        err(f"{rel}: body has {lines} lines (recommended max 500)")
    if len(body.strip()) < 400:
        err(f"{rel}: body too short to be a real skill")
    skills[d] = {"path": skill_md, "body": body,
                 "commands": set(re.findall(r"^### /([a-z]+)\s*$", body, re.M))}

# --- Commands ---------------------------------------------------------------------
cmd_files = {p.stem: p for p in (ROOT / "commands").glob("*.md") if p.name != "README.md"}
for cmd, p in sorted(cmd_files.items()):
    fm, body = frontmatter(p)
    rel = p.relative_to(ROOT)
    if fm is None:
        continue
    if not isinstance(fm.get("description"), str):
        err(f"{rel}: description must be a string")
    m = re.search(r"\*\*Skill:\*\* `([a-z-]+)`", body)
    if not m:
        err(f"{rel}: missing '**Skill:** `name`' line")
        continue
    s = m.group(1)
    if s not in skills:
        err(f"{rel}: skill '{s}' does not exist")
    elif cmd not in skills[s]["commands"]:
        err(f"{rel}: skills/{s}/SKILL.md has no '### /{cmd}' section")
declared = {c for s in skills.values() for c in s["commands"]}
for c in sorted(declared - set(cmd_files)):
    err(f"skill section '### /{c}' has no commands/{c}.md")

# --- Registry / help / README consistency -------------------------------------------
agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
helpbody = skills.get("apkhelp", {}).get("body", "")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
cmd_index = (ROOT / "commands" / "README.md").read_text(encoding="utf-8")
for c in sorted(cmd_files):
    for label, text in (("AGENTS.md", agents), ("apkhelp skill", helpbody), ("README.md", readme), ("commands/README.md", cmd_index)):
        if f"/{c}`" not in text and f"/{c}]" not in text:
            err(f"/{c} missing from {label}")

# --- Markdown: fences balanced, relative links resolve, referenced repo paths exist ------
md_files = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
link_re = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
path_re = re.compile(r"`((?:skills|commands|adapters|scripts|docs|examples)/[A-Za-z0-9_./-]+)`")
for p in md_files:
    text = p.read_text(encoding="utf-8")
    rel = p.relative_to(ROOT)
    if sum(1 for ln in text.splitlines() if ln.lstrip().startswith("```")) % 2:
        err(f"{rel}: unbalanced code fences")
    for target in link_re.findall(text):
        if re.match(r"(https?:|mailto:|#)", target):
            continue
        t = target.split("#")[0]
        if t and not (p.parent / t).resolve().exists():
            err(f"{rel}: broken link {target}")
    if rel.parts[0] in ("skills", "commands") or rel.name in ("README.md", "INSTALL.md", "AGENTS.md", "CONTRIBUTING.md"):
        for ref in path_re.findall(text):
            if any(ch in ref for ch in "*<>") or ref.endswith("/"):
                continue
            if not (ROOT / ref).exists():
                err(f"{rel}: references missing path {ref}")

# --- Config files ----------------------------------------------------------------------
for jf in ROOT.rglob("*.json"):
    if ".git" in jf.parts:
        continue
    try:
        json.loads(jf.read_text(encoding="utf-8"))
    except ValueError as exc:
        err(f"{jf.relative_to(ROOT)}: invalid JSON: {exc}")
for yf in list(ROOT.rglob("*.yml")) + list(ROOT.rglob("*.yaml")):
    try:
        yaml.safe_load(yf.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        err(f"{yf.relative_to(ROOT)}: invalid YAML: {exc}")
for mdc in (ROOT / "adapters").rglob("*.mdc"):
    frontmatter(mdc)

# --- Scripts -----------------------------------------------------------------------------
for sh in ROOT.rglob("*.sh"):
    r = subprocess.run(["bash", "-n", str(sh)], capture_output=True, text=True)
    if r.returncode:
        err(f"{sh.relative_to(ROOT)}: bash syntax error: {r.stderr.strip()}")
    elif not os.access(sh, os.X_OK):
        err(f"{sh.relative_to(ROOT)}: not executable")
for py in ROOT.rglob("*.py"):
    try:
        compile(py.read_text(encoding="utf-8"), str(py), "exec")
    except SyntaxError as exc:
        err(f"{py.relative_to(ROOT)}: syntax error: {exc}")

# --- Required files -----------------------------------------------------------------------
for req in ("README.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md", "INSTALL.md", "AGENTS.md"):
    if not (ROOT / req).exists():
        err(f"missing required file {req}")

print(f"Skills: {len(skills)} | Commands: {len(cmd_files)} | Markdown files: {len(md_files)}")
if errors:
    print(f"\n{len(errors)} problem(s):")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK: all checks passed")
