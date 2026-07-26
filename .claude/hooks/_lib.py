"""Shared helpers for the goalpost hooks.

Deliberately dependency-free: stdlib only, and a frontmatter parser that handles the
small YAML subset the brief template uses rather than pulling in PyYAML.
"""

import os
import re
import subprocess
from datetime import date
from pathlib import Path

# Paths the goal rule does not apply to. Editing these is either how you run the system
# (briefs, commands, hooks) or too minor to warrant a brief (docs, config, licence).
EXEMPT_PREFIXES = (
    "goals/",
    "decisions/",
    ".claude/",
    ".git/",
    "scratch/",
    "tmp/",
)

EXEMPT_FILES = (
    "README.md",
    "CLAUDE.md",
    "ORGANIZATION.md",
    "AGENTS.md",
    "LICENSE",
    ".gitignore",
    "install.sh",
)

STATUS_DIRS = ("scoped", "active", "review", "done", "closed")


def find_root(start=None):
    """Walk up for the repo root: a directory holding goals/, or failing that, .git/."""
    cur = Path(start or os.getcwd()).resolve()
    for candidate in (cur, *cur.parents):
        if (candidate / "goals").is_dir():
            return candidate
        if (candidate / ".git").exists():
            return candidate
    return None


def norm(path):
    """Strip a leading './' — but not the dot of a dotfile, which lstrip('./') would eat."""
    path = str(path).strip().replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    return path.lstrip("/")


def parse_frontmatter(text):
    """Parse the leading --- block. Handles scalars, `- ` lists, and one nesting level."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}

    data, key, parent = {}, None, None
    for raw in text[3:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw[0] in " \t"
        line = raw.strip()

        if line.startswith("- "):
            if key:
                # The key was seen with no value, so it holds a None placeholder;
                # setdefault would not replace it.
                if not isinstance(data.get(key), list):
                    data[key] = []
                data[key].append(line[2:].strip().strip("\"'"))
            continue

        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            continue
        name, value = match.group(1), match.group(2).strip().strip("\"'")

        if indented and parent:
            if not isinstance(data.get(parent), dict):
                data[parent] = {}
            data[parent][name] = value
            key = None
        elif value:
            data[name] = value
            key = None
        else:
            data[name] = None
            key, parent = name, name
    return data


def load_briefs(root, statuses=STATUS_DIRS):
    """Every brief in the given statuses, as (path, frontmatter) pairs."""
    out = []
    for status in statuses:
        folder = root / "goals" / status
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.md")):
            try:
                out.append((path, parse_frontmatter(path.read_text(encoding="utf-8"))))
            except OSError:
                continue
    return out


def declared_paths(briefs):
    """Deliverable paths declared across the given briefs, normalised."""
    paths = set()
    for _, meta in briefs:
        value = meta.get("deliverables")
        if isinstance(value, list):
            paths.update(norm(p) for p in value if p and p.strip())
        elif isinstance(value, str) and value.strip():
            paths.add(norm(value))
    return {p for p in paths if p and not p.startswith("path/to/")}


def is_exempt(rel):
    rel = norm(rel)
    return rel in EXEMPT_FILES or rel.startswith(EXEMPT_PREFIXES)


def covered_by(rel, declared):
    """True if rel is a declared deliverable, or sits under a declared directory."""
    rel = norm(rel)
    for target in declared:
        if rel == target or rel.startswith(target.rstrip("/") + "/"):
            return True
    return False


def changed_files(root):
    """Paths git reports as modified or untracked, relative to the repo root."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=root, capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if result.returncode != 0:
        return []

    files = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:  # a rename; the destination is what matters
            path = path.split(" -> ", 1)[1]
        files.append(path.strip().strip('"'))
    return files


def days_since(value):
    try:
        year, month, day = (int(part) for part in str(value).split("-")[:3])
        return (date.today() - date(year, month, day)).days
    except (ValueError, TypeError):
        return None
