---
name: ask-atlas
description: "Router over Atlas skills. Tell it your situation; it names the next skill to run."
disable-model-invocation: true
argument-hint: "What are you trying to do?"
---

# Ask Atlas

This is the map. A **flow** is a path through skills. User-invoked skills orchestrate. Model-invoked skills carry reusable discipline.

This repo owns the Atlas skills. Other skills may be installed — reference by name, do not copy.

## Main flow: request to verified change

1. IF scope or acceptance criteria are soft: use `/grilling` — one question round, then wait. Do not act until the contract is confirmed.
2. IF one pass is unlikely to finish the goal: use `/goal-loop`.
3. Use `/implement` to build scoped work. It uses `/tdd` at seams, runs checks, closes with `/code-review`.
4. IF the branch needs a PR body: use `/pr-writing`.
5. IF the remote is Bitbucket: use `/bitbucket-helper`.

Route only. Do not implement, edit, or create a PR from this skill.

## Routing table

| IF the user... | THEN route to... |
|---|---|
| Has a vague goal or competing approaches | `/grilling` |
| Has a concrete goal needing repeated progress | `/goal-loop` |
| Needs to build or fix code | `/implement` |
| Needs a diff review | `/code-review` |
| Needs a PR description | `/pr-writing` |
| Needs a Bitbucket PR | `/bitbucket-helper` |
| Needs isolation before risky work | `/creating-worktrees` |
| Has broad independent work | `/parallel-agents` |
| Needs design pressure on boundaries | `/codebase-design` |
| Is writing Go code | `/go` |
| Needs commit hygiene | `/git` |
| Needs personal memory search/save | `/personal-knowledge` |

IF the request is already a confirmed implementation contract: skip grilling, route directly to `/implement`. IF the user asks only for advice: return the smallest useful route and stop.

## Reusable disciplines

- `/tdd` — red-green-refactor at the smallest useful seam.
- `/code-review` — two-axis review: Standards and Spec, kept separate.
- `/codebase-design` — module shape, boundaries, and depth.
- `/go` — Go-specific implementation rules.
- `/parallel-agents` — independent read lanes, safe non-overlapping write lanes.
- `/pr-writing` — standard PR description shape from local git history.
- `/git` — commit and branch hygiene.
