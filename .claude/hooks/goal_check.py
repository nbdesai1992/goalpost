#!/usr/bin/env python3
"""Reconcile the working tree against the goal briefs.

Runs two ways:

    python3 .claude/hooks/goal_check.py     report to stdout, exit 0
    (as a Stop hook)                        reads hook JSON on stdin

Reconciliation beats prevention. Git already records every change no matter how it was
made — Write, Edit, sed, a shell redirect — so comparing that ledger against what the
briefs claim catches drift a write-time hook would miss, and can never deadlock.

As a Stop hook it speaks up at most once per session (Claude Code's stop_hook_active flag
guards the loop). Silence it with GOALPOST_STOP_CHECK=0.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _lib import (
    changed_files, covered_by, days_since, declared_paths, find_root, is_exempt,
    load_briefs,
)

STALE_DAYS = 14


def report(root):
    """Return (lines, has_findings)."""
    lines = []

    active = load_briefs(root, ("active",))
    review = load_briefs(root, ("review",))

    for path, meta in active:
        age = days_since(meta.get("updated") or meta.get("created"))
        if age is not None and age > STALE_DAYS:
            lines.append(
                f"Stale: {path.stem} has been active {age} days with no update. "
                "Still real? /goal log it, or /goal close it."
            )

    for path, _ in review:
        lines.append(f"Awaiting review: {path.stem} — needs a human to accept or send back.")

    declared = declared_paths(active + review)
    unattributed = [
        f for f in changed_files(root)
        if not is_exempt(f) and not covered_by(f, declared)
    ]
    if unattributed:
        shown = ", ".join(unattributed[:8])
        more = f" (+{len(unattributed) - 8} more)" if len(unattributed) > 8 else ""
        lines.append(
            f"Unattributed changes: {shown}{more}. No brief claims these. Add them to an "
            "active brief's deliverables, log why they changed, or scope a goal for them."
        )

    missing = [p for p in declared if not (root / p).exists()]
    if missing:
        lines.append(
            f"Declared but not produced: {', '.join(sorted(missing)[:8])}. "
            "Either still to come, or the brief's deliverables need correcting."
        )

    return lines, bool(lines)


def main():
    stdin_data = ""
    if not sys.stdin.isatty():
        stdin_data = sys.stdin.read()

    payload = {}
    if stdin_data.strip():
        try:
            payload = json.loads(stdin_data)
        except (json.JSONDecodeError, ValueError):
            payload = {}

    as_hook = payload.get("hook_event_name") == "Stop"
    root = find_root(payload.get("cwd"))

    if not root or not (root / "goals").is_dir():
        if not as_hook:
            print("No goals/ directory found — is this a goalpost repo?")
        return

    lines, found = report(root)

    if not as_hook:
        print("\n".join(f"- {line}" for line in lines) if found
              else "Clean: every change is attributed and nothing is stale.")
        return

    if not found:
        return
    if os.environ.get("GOALPOST_STOP_CHECK") == "0":
        return
    if payload.get("stop_hook_active"):
        return  # already continuing from this hook; don't loop

    print(json.dumps({
        "decision": "block",
        "reason": (
            "Before finishing, reconcile the goal briefs:\n"
            + "\n".join(f"- {line}" for line in lines)
            + "\n\nHandle these, then stop. If they're genuinely fine as-is, say why and stop."
        ),
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # a broken hook must never break the session
