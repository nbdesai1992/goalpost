# Operating contract

Work in this repository is tracked as **goal briefs**. Anything of consequence starts as a
brief and ends as a record of what actually happened. The brief folder is the project's
memory: it answers "what have we done here, and why."

This system is deliberately small — a folder of markdown files, one slash command, and two
advisory hooks. There is no queue, no runner, no orchestrator. If it ever grows one, that
was a mistake.

## The rule

Before making a substantive change to this repository, there should be an active goal
brief that covers it.

Substantive means: creating or reorganizing deliverables, writing code that ships,
producing research output, changing how the project works.

Not substantive (just do it): fixing a typo, tightening a README sentence, poking at
something to debug it, running read-only commands, throwaway exploration you're going to
delete.

If you're unsure, the tell is whether a future reader would want to know *why* it
happened. If yes, it wants a brief.

## Statuses

| Status   | Directory       | Meaning                                                        |
| -------- | --------------- | -------------------------------------------------------------- |
| `scoped` | `goals/scoped/` | Brief written and agreed. Work has not started.                 |
| `active` | `goals/active/` | Being worked right now.                                         |
| `review` | `goals/review/` | Deliverables exist. Awaiting human acceptance. **Agent stops.** |
| `done`   | `goals/done/`   | Accepted. Outcome section filled in.                            |
| `closed` | `goals/closed/` | Ended without shipping. `closed_reason` says why.               |

`closed` is neutral on purpose. A goal can end because it became `obsolete`, was
`superseded` by a better approach, got `descoped`, or is `blocked` indefinitely. The
directory records that it ended; the `closed_reason` field records which. Closed briefs
are kept, never deleted — a goal you decided not to pursue, and the reasoning behind it,
is often worth more later than one you completed.

`review` exists because some work needs a human to look at it before it counts as done.
An agent moves a brief to `review` and stops there. Only a human moves it to `done`.

## Deliverables are declared up front

Every brief lists the paths its deliverables will land at, before work starts. This is the
load-bearing part of the system.

It forces the scoping to be real — you cannot name paths for a goal you haven't thought
through. It makes completion checkable rather than a matter of opinion: did the declared
files appear, and does the tree still match `ORGANIZATION.md`? And it gives the hooks
something concrete to compare against.

If work reveals that the declared paths were wrong, change them in the brief and note it
in the log. Drifting silently is the failure mode.

## Working a goal

1. **Scope it.** Draft the brief. The bar: a testable definition of done, declared
   deliverable paths, and explicit non-goals. Get agreement before starting.
2. **Activate it.** Move to `goals/active/`.
3. **Work it.** Append dated entries to the brief's log as you go — decisions made,
   surprises hit, paths changed. Write them when they happen, not reconstructed at the end.
4. **Hand it back.** Move to `goals/review/` and stop. Say what to check.
5. **Close it out.** Once accepted, fill in the Outcome section and move to `goals/done/`.
   An Outcome section is not optional — a completed brief without one is just a stale plan.

Update `goals/INDEX.md` on every status change.

## Keeping the repo organized

`ORGANIZATION.md` declares where things go and why. It is the current-state map; the brief
archive is the history. Both matter, for different questions.

Before a brief leaves `review`, the tree should match the map. Run the
`file-organization` skill to check. If the work genuinely needs a new category, amend
`ORGANIZATION.md` as part of the goal rather than quietly inventing a folder.

## Two kinds of memory

Briefs are episodic — what happened, when, why. `ORGANIZATION.md` and `decisions/` are
semantic — what is true now. When a goal produces a durable decision that outlives it,
promote that decision out of the brief into `decisions/` so the next person doesn't have
to read forty briefs to learn how things work here.

## Writing briefs

The agent drafts, the human approves. Nobody should be hand-writing these; that friction
is what kills systems like this.

Match the brief to the goal. A small goal gets a short brief — goal, done-criteria, paths,
maybe four lines total. Save the full template for work that warrants it. A brief that
takes twenty minutes to write is a planning failure, not thoroughness.
