---
name: ask-atlas
description: "Router over Atlas skills. Tell it your situation; it names the next skill to run."
disable-model-invocation: true
argument-hint: "What are you trying to do?"
---

# Ask Atlas

This is the map. A **flow** is a path through skills. User-invoked skills orchestrate. Model-invoked skills carry reusable discipline.

This repo owns the Atlas skills. Other skills may be installed — reference by name, do not copy.

## Routing table

Use the first matching row. Specific skill rows beat the generic direct-answer row.

| IF the request... | THEN... |
|---|---|
| Changes an accepted decision (`actually`, `instead`, `forget that`) | Route to `/decision-drift-guard` |
| Gives a concrete feature, fix, or implementation spec | Route to `/implement` |
| Needs repeated progress across rounds | Route to `/goal-loop` |
| Needs a diff review | Route to `/code-review` |
| Needs a PR description | Route to `/pr-writing` |
| Needs a Bitbucket PR | Route to `/bitbucket-helper` |
| Needs isolation before risky work | Route to `/creating-worktrees` |
| Has broad independent work | Route to `/parallel-agents` |
| Asks whether to split, merge, or reshape services or modules | Route to `/codebase-design` |
| Needs design pressure on boundaries | Route to `/codebase-design` |
| Is writing Go code or asks about Go code | Route to `/go` |
| Needs commit hygiene | Route to `/git` |
| Asks what existing code does, asks a casual question, or requests a one-line rename/typo | Return `no skill needed` and stop |
| Has a vague goal or competing approaches | Route to `/grilling` |
| Needs personal memory search/save | Route to `/personal-knowledge` |

Route only. Do not implement, edit, or create a PR from this skill.

## Reusable disciplines

- `/tdd` — red-green-refactor at the smallest useful seam.
- `/code-review` — two-axis review: Standards and Spec, kept separate.
- `/codebase-design` — module shape, boundaries, and depth.
- `/go` — Go-specific implementation rules.
- `/parallel-agents` — independent read lanes, safe non-overlapping write lanes.
- `/pr-writing` — standard PR description shape from local git history.
- `/git` — commit and branch hygiene.
