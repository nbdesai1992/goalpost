#!/usr/bin/env bash
# Install goalpost into an existing repository.
#
#   curl -fsSL https://raw.githubusercontent.com/nbdesai1992/goalpost/main/install.sh | bash
#
# Copies the goals scaffold, the /goal command, the file-organization skill, and the
# hooks. Never overwrites a file you already have — existing files are reported and left
# alone. Merges hook wiring into .claude/settings.json if one is already there.

set -euo pipefail

REPO="${GOALPOST_REPO:-https://github.com/nbdesai1992/goalpost.git}"
REF="${GOALPOST_REF:-main}"
TARGET="${1:-$PWD}"

info() { printf '  %s\n' "$1"; }
skip() { printf '  \033[2m%s (exists, left alone)\033[0m\n' "$1"; }

command -v git >/dev/null || { echo "git is required"; exit 1; }
command -v python3 >/dev/null || { echo "python3 is required"; exit 1; }

TARGET="$(cd "$TARGET" && pwd)"
if [ -d "$TARGET/goals" ] && [ -f "$TARGET/.claude/commands/goal.md" ]; then
  echo "goalpost is already installed in $TARGET"
  exit 0
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git clone --quiet --depth 1 --branch "$REF" "$REPO" "$TMP/src"

echo "Installing goalpost into $TARGET"

copy() {
  local rel="$1"
  if [ -e "$TARGET/$rel" ]; then skip "$rel"; return; fi
  mkdir -p "$(dirname "$TARGET/$rel")"
  cp -R "$TMP/src/$rel" "$TARGET/$rel"
  info "$rel"
}

for f in \
  goals/TEMPLATE.md \
  goals/INDEX.md \
  ORGANIZATION.md \
  .claude/commands/goal.md \
  .claude/skills/file-organization \
  .claude/hooks/_lib.py \
  .claude/hooks/goal_guard.py \
  .claude/hooks/goal_check.py
do
  copy "$f"
done

for d in scoped active review done closed; do
  mkdir -p "$TARGET/goals/$d"
  [ -e "$TARGET/goals/$d/.gitkeep" ] || touch "$TARGET/goals/$d/.gitkeep"
done
mkdir -p "$TARGET/decisions"

# The seeded index lists this repo's own bootstrap brief; a fresh install starts empty.
if [ ! -d "$TARGET/goals/done" ] || [ -z "$(ls -A "$TARGET/goals/done" 2>/dev/null | grep -v .gitkeep)" ]; then
  python3 - "$TARGET/goals/INDEX.md" <<'PY'
import re, sys
p = sys.argv[1]
try:
    text = open(p, encoding="utf-8").read()
except OSError:
    sys.exit()
text = re.sub(r"(## Done\n\n)- \[2026-07-26-bootstrap-goalpost\].*?\n", r"\1_none_\n", text)
open(p, "w", encoding="utf-8").write(text)
PY
fi

# Hook wiring: merge into an existing settings.json rather than clobbering it.
python3 - "$TARGET" "$TMP/src" <<'PY'
import json, pathlib, sys

target, src = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
dest = target / ".claude" / "settings.json"
incoming = json.loads((src / ".claude" / "settings.json").read_text())["hooks"]

if not dest.exists():
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({"hooks": incoming}, indent=2) + "\n")
    print("  .claude/settings.json")
    sys.exit()

try:
    settings = json.loads(dest.read_text())
except json.JSONDecodeError:
    print("  .claude/settings.json is not valid JSON — add the hooks by hand")
    sys.exit()

hooks = settings.setdefault("hooks", {})
added = False
for event, entries in incoming.items():
    existing = hooks.setdefault(event, [])
    for entry in entries:
        commands = {
            h.get("command", "")
            for group in existing for h in group.get("hooks", [])
        }
        if any("goal_guard.py" in c or "goal_check.py" in c for c in commands):
            continue
        existing.append(entry)
        added = True

if added:
    dest.write_text(json.dumps(settings, indent=2) + "\n")
    print("  .claude/settings.json (hooks merged)")
else:
    print("  .claude/settings.json (hooks already present)")
PY

cat <<'EOF'

Done. Two things left:

  1. Add the operating rules to your CLAUDE.md — copy from:
     https://github.com/nbdesai1992/goalpost/blob/main/CLAUDE.md
     Append them if you already have one.

  2. Edit ORGANIZATION.md to describe where things actually go in this repo.

Then: /goal <what you want to get done>
EOF
