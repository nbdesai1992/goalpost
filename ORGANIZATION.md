# Where things go

The current-state map of this repository. Briefs declare their deliverable paths against
this file, and the `file-organization` skill checks the tree against it.

This starts nearly empty on purpose. A taxonomy invented before there is anything to
organize is as costly as no taxonomy at all. Grow it as real work arrives, one goal at a
time.

## Rules

1. Every file lives somewhere this document accounts for.
2. New categories are added here as part of the goal that needs them, not invented
   silently mid-task.
3. Directory names say what things *are*, not who made them or when.
4. If a folder has one file in it and no clear reason to expect a second, it shouldn't be
   a folder yet.

## Current map

| Path              | Holds                                                          |
| ----------------- | -------------------------------------------------------------- |
| `goals/`          | Goal briefs, one file each, filed by status. The project's memory. |
| `decisions/`      | Durable decisions promoted out of briefs. What is true now.     |
| `.claude/`        | Slash commands, skills, and hooks that run this system.         |
| `CLAUDE.md`       | The operating contract. Loaded every session.                   |
| `ORGANIZATION.md` | This file.                                                      |
| `README.md`       | What this repo is and how to use it.                            |

## Add your own

Whatever this repo is actually for goes below. Some shapes that tend to work:

| Path        | Holds                                                        |
| ----------- | ------------------------------------------------------------ |
| `src/`      | Code that ships.                                              |
| `research/` | Findings, analyses, notes — the output of `research` goals.   |
| `artifacts/`| Documents, decks, diagrams — things produced for someone else.|
| `data/`     | Inputs. Raw stays raw; derived files say what derived them.   |
| `scripts/`  | One-off and utility scripts.                                  |

Delete the rows you don't need. Don't create the directories until a goal calls for them.
