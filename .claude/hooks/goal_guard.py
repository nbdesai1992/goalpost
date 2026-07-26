#!/usr/bin/env python3
"""PreToolUse nudge: writing outside the active goal's declared deliverables.

Advisory, never blocking. It hands the agent a note and lets it use judgment, because a
hook that blocks too often gets switched off, and then you have nothing. The real
accounting happens in goal_check.py, which reconciles against git and so also catches
edits made through Bash.

Disable with GOALPOST_GUARD=0.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import os

from _lib import covered_by, declared_paths, find_root, is_exempt, load_briefs


def note(text):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": text,
        }
    }))


def main():
    if os.environ.get("GOALPOST_GUARD") == "0":
        return

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return

    target = (payload.get("tool_input") or {}).get("file_path")
    if not target:
        return

    root = find_root(payload.get("cwd"))
    if not root or not (root / "goals").is_dir():
        return

    try:
        rel = Path(target).resolve().relative_to(root).as_posix()
    except ValueError:
        return  # outside the repo; not this system's business

    if is_exempt(rel):
        return

    active = load_briefs(root, ("active",))
    if not active:
        scoped = load_briefs(root, ("scoped",))
        hint = (
            f" There {'is' if len(scoped) == 1 else 'are'} {len(scoped)} brief"
            f"{'' if len(scoped) == 1 else 's'} in goals/scoped/ — one may cover this."
            if scoped else ""
        )
        note(
            f"No goal brief is active, and `{rel}` is a substantive path.{hint} "
            "If this change is worth a future reader knowing the reason for, scope it with "
            "/goal first. If it's a typo fix, a doc tweak, or debugging, carry on."
        )
        return

    if covered_by(rel, declared_paths(active)):
        return

    names = ", ".join(path.stem for path, _ in active)
    note(
        f"`{rel}` is not among the declared deliverables of the active brief ({names}). "
        "Either it belongs to this goal — in which case add it to the brief's "
        "`deliverables` and note the change in the log — or it's a different goal. "
        "Declared paths drifting silently is the failure mode this system exists to stop."
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # a broken hook must never break the session
