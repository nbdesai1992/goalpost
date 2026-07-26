---
description: Scope, track, and close out goal briefs
argument-hint: "[<description> | log <note> | review | done | close <reason> | status]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(ls:*), Bash(date:*)
---

You are running the `/goal` command. Arguments: `$ARGUMENTS`

Read `CLAUDE.md` and `ORGANIZATION.md` first if they aren't already in context — they
define the statuses, the deliverables contract, and the folder map you're working against.

Dispatch on the arguments:

## No arguments → status

Report the current state, briefly:

- Active briefs, with how long each has been active. Anything active more than two weeks,
  say so plainly — stale goals are the main way this system rots.
- Anything sitting in `goals/review/` waiting on the human.
- What's in `goals/scoped/`, one line each.

Then stop. Don't start work.

## `status` → same as above

## `log <note>` → append to the active brief

Add a dated entry to the active brief's Log section. If more than one brief is active, ask
which. Keep the entry to what happened and why — no summarizing of things that didn't
change.

## `review` → hand back for human acceptance

Move the active brief to `goals/review/`, set `status: review`, update `goals/INDEX.md`.
Then run the `file-organization` skill and report divergence from `ORGANIZATION.md`.

Tell the user specifically what to check, keyed to the definition-of-done checkboxes. Then
stop. Do not move it to `done` yourself — that's the human's call, and it is the whole
reason this status exists.

## `done` → accept and close out

Only valid when the human is accepting the work. Fill in the Outcome section — what
shipped, what diverged from the plan and why, what we learned. Set `status: done`, move to
`goals/done/`, update `goals/INDEX.md`.

If the goal produced a decision that outlives it, promote that decision into `decisions/`.

## `close <reason>` → end without shipping

`reason` is one of `obsolete`, `superseded`, `descoped`, `blocked`, optionally followed by
an explanation. Set `status: closed` and `closed_reason:`, fill in the Outcome section with
why it ended and anything learned, move to `goals/closed/`, update `goals/INDEX.md`.

Never delete a closed brief. The reasoning behind a goal you decided not to pursue is
often worth more later than one you finished.

## Anything else → scope a new goal

Treat the arguments as a description of the goal and draft a brief from
`goals/TEMPLATE.md`.

**You draft it. The user approves it.** Never hand the template to the user to fill in —
that friction is what kills systems like this.

Before writing anything, resolve these. Ask only what you genuinely can't infer from the
description, the repo, or the conversation — one round of questions, not an interrogation:

1. **A testable definition of done.** If you can't write criteria someone uninvolved could
   check, the goal isn't scoped yet. Push until you can.
2. **Declared deliverable paths.** Every artifact, with where it lands. Check them against
   `ORGANIZATION.md`. If the work needs a category the map doesn't have, adding that
   category is part of this goal — say so.
3. **Non-goals.** At least one. If nothing is out of scope, the goal is too vague.
4. **Type** — `build`, `research`, `artifact`, or `ops`. It sets the shape of the
   done-criteria: research goals conclude, build goals ship, artifact goals get delivered
   to someone.

Match the brief to the goal. Something small gets four lines under the required headings —
goal, done-criteria, deliverables, non-goals. Reach for the full template when the work
warrants it.

Write to `goals/scoped/YYYY-MM-DD-short-slug.md` (use today's real date), show the user the
brief, and ask whether to activate. On approval, move it to `goals/active/`, set
`status: active`, and update `goals/INDEX.md`.
