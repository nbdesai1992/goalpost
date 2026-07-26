---
id: 2026-07-26-bootstrap-goalpost
title: Build and publish the initial version of the goal brief system
type: build
status: done
created: 2026-07-26
updated: 2026-07-26
deliverables:
  - CLAUDE.md
  - README.md
  - ORGANIZATION.md
  - install.sh
  - goals/TEMPLATE.md
  - goals/INDEX.md
  - decisions/README.md
  - .claude/commands/goal.md
  - .claude/skills/file-organization/SKILL.md
  - .claude/hooks/_lib.py
  - .claude/hooks/goal_guard.py
  - .claude/hooks/goal_check.py
  - .claude/settings.json
links:
  related: This is the system describing its own construction.
---

# Bootstrap goalpost

## Goal

A repository that codifies goal-brief tracking for Claude Code work, installable into any
project, published and usable.

## Why now

Agents leave a thin trace. Git records what changed and when; the reasoning — what was
attempted, what was ruled out, what was deliberately skipped — evaporates. A structured
record placed in front of the work is cheaper and truer than one reconstructed after it.

## Definition of done

- [x] Five statuses with one directory each, `review` among them so a human gates
      acceptance.
- [x] `/goal` covers the full lifecycle: scope, log, review, done, close.
- [x] Briefs declare deliverable paths up front, and the hooks check against them.
- [x] Hooks are advisory and cannot deadlock.
- [x] A file-organization skill that proposes rather than rearranges.
- [x] Installs into an existing repo without clobbering anything.
- [x] Works for research and documents as readily as for code.
- [x] Published to GitHub under `nbdesai1992`.

## Deliverables

| Path                                        | What it is                          |
| ------------------------------------------- | ----------------------------------- |
| `CLAUDE.md`                                 | The operating contract              |
| `README.md`                                 | What it is, how to install and use  |
| `ORGANIZATION.md`                           | Where-things-go map                 |
| `install.sh`                                | Non-destructive installer           |
| `goals/TEMPLATE.md`, `goals/INDEX.md`       | Brief scaffold and index            |
| `decisions/README.md`                       | Semantic-memory convention          |
| `.claude/commands/goal.md`                  | The `/goal` command                 |
| `.claude/skills/file-organization/SKILL.md` | Tree-vs-map check                   |
| `.claude/hooks/*.py`                        | Guard, reconciliation, shared lib   |
| `.claude/settings.json`                     | Hook wiring                         |

## Non-goals

- No queue, runner, or orchestrator. Five directories are the entire state machine.
- No enforcement of *quality* — the system tracks that work was scoped and recorded, not
  that it was any good.
- No integration with issue trackers. The brief folder is the record.
- No automatic file moves. The organization skill proposes; a human accepts.

## Approach

Design first, in conversation, then build in one pass. The load-bearing choice is that
briefs declare deliverable paths before work starts — that single field is what turns
"is the repo organized" from an aesthetic judgment into a diff, and gives the hooks
something concrete to check.

## Log

- **2026-07-26** — Design discussion. Considered a hard-blocking `PreToolUse` hook and
  rejected it: it deadlocks on writing the very brief that would unblock it, it can't see
  edits made through Bash, and a hook that blocks too often gets switched off. Settled on
  an advisory nudge plus reconciliation against `git status`, which catches everything
  regardless of how it was written and cannot deadlock.
- **2026-07-26** — Replaced `abandoned` with `closed` + a `closed_reason` field
  (`obsolete | superseded | descoped | blocked`). One word can't carry four distinct
  endings, and `abandoned` reads as a judgment on work that was often correctly stopped.
- **2026-07-26** — Added `review` between `active` and `done`. An agent shouldn't decide
  its own work is finished; this is where it hands back and stops.
- **2026-07-26** — Built all deliverables and tested the hooks against this repo. Testing
  caught two bugs in the frontmatter parser, both of which would have made the system
  quietly useless rather than visibly broken: `setdefault` failed to replace the `None`
  placeholder left by a valueless key, so every `deliverables` list parsed as empty; and
  `lstrip("./")` strips a character *set*, so `.claude/...` normalised to `claude/...` and
  broke both the exemption check and path matching. A guard that silently approves
  everything is worse than no guard, since nothing signals the failure.
- **2026-07-26** — Verified `install.sh` end-to-end from the published URL: merges into an
  existing `.claude/settings.json` without disturbing existing hooks or permissions, leaves
  existing files alone, and is idempotent. Published at
  https://github.com/nbdesai1992/goalpost.
- **2026-07-26** — Third bug, found by the tooling hanging on me rather than by reading it:
  `goal_check.py` used `isatty()` to decide whether to read stdin, which is wrong. Stdin can
  be a pipe with no writer — inside a shell pipeline, a CI step, a subshell — and then
  `read()` blocks forever. Now polls with `select` before committing to a read. Verified
  across all six invocation modes: CLI in a pipeline, CLI with stdin closed, and Stop-hook
  mode both clean and with drift.

## Outcome

**What shipped:** The full system as listed above. Five statuses, one `/goal` command with
six modes, two advisory hooks, one skill, and a non-destructive installer that merges into
an existing `.claude/settings.json` rather than overwriting it.

**What diverged from the plan, and why:** The original sketch had the hook preventing
unattributed writes. It became a nudge plus a reconciliation pass instead — prevention is
brittle where reconciliation is thorough, since git sees every change no matter which tool
made it. A `decisions/` folder was added mid-build once it was clear the brief archive
answers "what happened" but nothing answered "what is true now."

**What we learned:** Declaring deliverable paths up front is the keystone. Nearly every
other property — checkable completion, a meaningful organization check, hooks with
something concrete to compare against — falls out of that one field. Without it the system
would be a folder of aspirational documents.

The real risk to a system like this is ceremony, not laxity. Hence: the agent drafts and
the human approves, small goals get four-line briefs, and both hooks stay advisory.
