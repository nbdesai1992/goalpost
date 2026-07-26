---
name: file-organization
description: Check the repository tree against ORGANIZATION.md and propose fixes for anything misfiled, orphaned, or undeclared. Use before a goal brief moves to review, when files have accumulated in unclear places, when deciding where a new deliverable should live, or when the user asks whether the repo is organized. Proposes moves for approval; never reorganizes on its own.
---

# File organization

Keep the tree matching `ORGANIZATION.md`. That file is the contract; this skill checks
against it and proposes fixes. It does not rearrange things on its own judgment.

## Check

1. Read `ORGANIZATION.md`. If it doesn't exist, stop and say so — there is nothing to
   check against, and inventing a taxonomy on the spot is exactly what this skill is meant
   to prevent.
2. List the tree, skipping `.git/` and anything gitignored.
3. Compare, and collect four kinds of divergence:

   - **Unaccounted** — files in paths the map doesn't describe.
   - **Misfiled** — files that exist somewhere the map wouldn't put them.
   - **Undelivered** — paths declared by a brief in `active/` or `review/` that don't
     exist yet.
   - **Undeclared** — files that appeared but no brief claims as a deliverable. Cross-check
     against `deliverables` in every brief's frontmatter.

## Report

Group by kind, most consequential first. For each item give the path, why it diverges, and
the specific fix. Say "no divergence" when there is none rather than inventing something to
report.

If nothing diverges but the map has drifted from reality in spirit — a category that
describes nothing, a folder holding something other than what it claims — say that too.

## Propose, don't move

Never move files without approval. Present the moves as a list the user can accept whole or
in part, then execute what's approved with `git mv` so history follows the file.

When work genuinely needs a category the map doesn't have, propose amending
`ORGANIZATION.md` — as part of the goal that needs it, not as a silent side effect.

## Be conservative

Premature structure costs as much as none. Bias toward leaving things alone.

- One file with no clear reason to expect a second doesn't need a folder.
- Deep nesting for a handful of files makes things harder to find, not easier.
- Directory names should say what things *are* — not who made them, or when.
- A file that's genuinely temporary belongs in the scratchpad or `.gitignore`, not in a
  new `misc/` or `tmp/` directory.

## When to run

- Before a brief moves to `review` — the tree should match the map before a human is asked
  to accept the work.
- When picking the deliverable paths for a new brief.
- On request.
