# Decisions

Durable decisions, promoted out of the goal briefs that produced them.

A brief answers "what happened, and why did we do it that way." That's episodic — tied to
a moment, and mostly of interest later as history. Some of what a brief produces outlives
it: a convention, a constraint, a rejected approach that shouldn't be relitigated. Those
belong here, where the answer to "how do things work around here" doesn't require reading
the whole archive.

Promote a decision when it will still matter after the goal is filed. One file each,
`YYYY-MM-DD-slug.md`, short:

```markdown
# What was decided

**Date** · **From** [brief-id](../goals/done/brief-id.md)

## Context
What forced the choice.

## Decision
What we settled on.

## Alternatives rejected
And why. This is the part people come back for.

## Consequences
What this commits us to.
```

Supersede rather than edit. When a decision is overturned, add a new file that links back
to the old one and mark the old one superseded — the fact that something changed, and
when, is usually as useful as the current answer.
