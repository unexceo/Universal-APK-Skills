#!/usr/bin/env bash
# Installs Universal APK Skills into an agent's skills directory.
# Usage: install.sh --target TARGET [--scope user|project] [--project-dir DIR] [--dest DIR] [--link] [--force] [--uninstall]
# TARGET: claude | agents (Codex and other .agents/skills readers) | gemini | cursor | copilot | cline | custom (needs --dest)
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET=""; SCOPE="user"; PROJECT_DIR=""; DEST=""; LINK=0; FORCE=0; UNINSTALL=0

usage() { sed -n '2,5p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit "${1:-2}"; }
while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --scope) SCOPE="${2:-}"; shift 2 ;;
    --project-dir) PROJECT_DIR="${2:-}"; shift 2 ;;
    --dest) DEST="${2:-}"; shift 2 ;;
    --link) LINK=1; shift ;;
    --force) FORCE=1; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    -h|--help) usage 0 ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done
[ -n "$TARGET" ] || usage

# Directory conventions (user scope / project scope), per the Agent Skills ecosystem.
case "$TARGET" in
  claude)  U="$HOME/.claude/skills";   P=".claude/skills";   CU="$HOME/.claude/commands"; CP=".claude/commands" ;;
  agents)  U="$HOME/.agents/skills";   P=".agents/skills";   CU=""; CP="" ;;
  gemini)  U="$HOME/.gemini/skills";   P=".gemini/skills";   CU=""; CP="" ;;
  cursor)  U="$HOME/.cursor/skills";   P=".cursor/skills";   CU=""; CP="" ;;
  copilot) U="$HOME/.copilot/skills";  P=".github/skills";   CU=""; CP="" ;;
  cline)   U="$HOME/.cline/skills";    P=".cline/skills";    CU=""; CP="" ;;
  custom)  [ -n "$DEST" ] || { echo "--target custom requires --dest" >&2; exit 2; }; U="$DEST"; P="$DEST"; CU=""; CP="" ;;
  *) echo "Unknown target: $TARGET" >&2; usage ;;
esac

if [ "$SCOPE" = "project" ]; then
  [ -n "$PROJECT_DIR" ] || { echo "--scope project requires --project-dir DIR" >&2; exit 2; }
  [ -d "$PROJECT_DIR" ] || { echo "Not a directory: $PROJECT_DIR" >&2; exit 2; }
  SKILLS_DIR="$PROJECT_DIR/$P"; CMD_DIR=""; [ -n "$CP" ] && CMD_DIR="$PROJECT_DIR/$CP"
elif [ "$SCOPE" = "user" ]; then
  SKILLS_DIR="${DEST:-$U}"; CMD_DIR="$CU"
else
  echo "--scope must be user or project" >&2; exit 2
fi

SKILLS=(); for d in "$REPO"/skills/*/; do [ -f "$d/SKILL.md" ] && SKILLS+=("$(basename "$d")"); done
[ ${#SKILLS[@]} -gt 0 ] || { echo "No skills found in $REPO/skills" >&2; exit 1; }

if [ $UNINSTALL -eq 1 ]; then
  for s in "${SKILLS[@]}"; do rm -rf "${SKILLS_DIR:?}/$s"; done
  if [ -n "$CMD_DIR" ]; then for f in "$REPO"/commands/*.md; do b="$(basename "$f")"; [ "$b" = README.md ] || rm -f "$CMD_DIR/$b"; done; fi
  echo "Removed Universal APK Skills from $SKILLS_DIR${CMD_DIR:+ and $CMD_DIR}"; exit 0
fi

mkdir -p "$SKILLS_DIR"
for s in "${SKILLS[@]}"; do
  dst="$SKILLS_DIR/$s"
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    if [ $FORCE -eq 1 ]; then rm -rf "$dst"; else echo "skip   $s (exists; use --force)"; continue; fi
  fi
  if [ $LINK -eq 1 ]; then ln -s "$REPO/skills/$s" "$dst"; else cp -R "$REPO/skills/$s" "$dst"; fi
  echo "install $s -> $dst"
done
if [ -n "$CMD_DIR" ]; then
  mkdir -p "$CMD_DIR"
  for f in "$REPO"/commands/*.md; do
    b="$(basename "$f")"; [ "$b" = README.md ] && continue
    if [ -e "$CMD_DIR/$b" ] && [ $FORCE -eq 0 ]; then continue; fi
    if [ $LINK -eq 1 ]; then ln -sf "$f" "$CMD_DIR/$b"; else cp "$f" "$CMD_DIR/$b"; fi
  done
  echo "commands -> $CMD_DIR"
fi

# Verify
bad=0
for s in "${SKILLS[@]}"; do [ -f "$SKILLS_DIR/$s/SKILL.md" ] || { echo "VERIFY FAILED: $SKILLS_DIR/$s/SKILL.md missing" >&2; bad=1; }; done
[ $bad -eq 0 ] && echo "Verified ${#SKILLS[@]} skills in $SKILLS_DIR. Restart/reload your agent if it caches skills."
exit $bad
