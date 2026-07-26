# goalpost

A small system for tracking what an agent is actually doing, and why.

Work starts as a **goal brief** — a markdown file with a testable definition of done and
the paths its deliverables will land at. Work is logged against that brief as it happens.
When it's finished, the brief records what shipped and what was learned. The folder of
briefs becomes the project's memory: what has been done here, what was tried and dropped,
and the reasoning behind both.

It works the same whether the goal is shipping code, running an analysis, or writing a
document. Nothing in it assumes a build step.

```
/goal migrate the auth service off the legacy token store
/goal work out whether our churn spike is seasonal
/goal draft the Q3 board update
```

## Why

Agents are good at doing things and bad at leaving a trace. Three months later the repo
shows *what* the code looks like and git shows *when* it changed, but the reasoning is
gone — what was being attempted, what was ruled out, what was deliberately left undone.

goalpost puts a cheap, structured record in front of the work instead of trying to
reconstruct one after. The cost is a brief you approve rather than write; the payoff is a
project that can explain itself.

## Install

Into an existing repository — this is the common case:

```bash
curl -fsSL https://raw.githubusercontent.com/nbdesai1992/goalpost/main/install.sh | bash
```

Or clone it as a starting point for something new:

```bash
gh repo create my-project --template nbdesai1992/goalpost --private --clone
```

Requires Claude Code and `python3`. No other dependencies.

## How it works

**One command.**

| Command                | Does                                                      |
| ---------------------- | --------------------------------------------------------- |
| `/goal <description>`  | Scopes a goal and drafts the brief for you to approve.     |
| `/goal`                | What's active, what's waiting on you, what's gone stale.   |
| `/goal log <note>`     | Appends a dated entry to the active brief.                 |
| `/goal review`         | Hands the work back for acceptance, and stops.             |
| `/goal done`           | Accepts it, writes the outcome, files it.                  |
| `/goal close <reason>` | Ends it without shipping. `obsolete`, `superseded`, `descoped`, `blocked`. |

**Five statuses**, one directory each:

```
goals/
  scoped/   defined, not started
  active/   being worked
  review/   done enough for a human to look at — the agent stops here
  done/     accepted, outcome recorded
  closed/   ended without shipping; closed_reason says why
```

`review` exists because the agent shouldn't be the one deciding its own work is finished.
`closed` is neutral by design — the directory records that a goal ended, the
`closed_reason` records which kind of ending. Closed briefs are kept. A goal you decided
*not* to pursue, with the reasoning attached, is often worth more later than one you
completed.

**Deliverables declared up front.** Every brief names the paths it will produce, before
work starts. This is the part that makes the rest work: it forces the scoping to be
concrete, it makes completion checkable instead of a matter of opinion, and it gives the
hooks something to compare the tree against.

**Two hooks, both advisory.** A write-time nudge when a file falls outside the active
brief's declared paths, and a reconciliation pass that diffs the working tree against what
the briefs claim and flags anything unattributed.

The reconciliation matters more than the nudge. Git already records every change no matter
how it was made — an `Edit`, a `sed`, a shell redirect — so checking against that ledger
catches drift a write-time hook would miss, and it can't deadlock the way a blocking hook
can. Neither hook stops you from working. A hook that blocks too often gets switched off,
and then you have nothing.

**A file-organization skill** that checks the tree against `ORGANIZATION.md` and proposes
moves. It proposes; it doesn't rearrange.

## Layout

```
CLAUDE.md              the operating contract, loaded every session
ORGANIZATION.md        where things go and why — the current-state map
goals/                 briefs, filed by status · TEMPLATE.md · INDEX.md
decisions/             durable decisions promoted out of briefs
.claude/
  commands/goal.md     the /goal command
  skills/              file-organization
  hooks/               goal_guard.py · goal_check.py
  settings.json        hook wiring
```

The brief archive is the history; `ORGANIZATION.md` and `decisions/` are the current
state. Different questions, different files — "how did we get here" and "how do things
work now" shouldn't require reading the same forty documents.

## Checking by hand

```bash
python3 .claude/hooks/goal_check.py
```

Lists stale goals, work awaiting review, changed files no brief accounts for, and declared
deliverables that never appeared.

## Turning bits off

| Variable                | Effect                                  |
| ----------------------- | --------------------------------------- |
| `GOALPOST_GUARD=0`      | Silences the write-time nudge.          |
| `GOALPOST_STOP_CHECK=0` | Silences the end-of-session pass.       |

Exempt paths live in `EXEMPT_PREFIXES` and `EXEMPT_FILES` in `.claude/hooks/_lib.py`.
Docs, config, and the brief folder itself are exempt out of the box — you shouldn't need a
goal to fix a typo, and you certainly shouldn't need one to write the brief.

## Keeping it small

This is a folder of markdown files, one command, and two hooks. There is no queue, no
runner, no state machine beyond five directories, no orchestrator. That's the design, not
a missing feature. Systems like this die of ceremony — the moment a brief takes twenty
minutes to write, it stops getting written, and an abandoned process is worse than none.

Match the brief to the goal. Something small gets four lines. Save the full template for
work that earns it.

## Licence

MIT
