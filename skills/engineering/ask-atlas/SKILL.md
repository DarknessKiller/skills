---
name: ask-atlas
description: "Router over Atlas skills. Tell it your situation; it names the next skill to run."
disable-model-invocation: true
argument-hint: "What are you trying to do?"
---

# Ask Atlas

The map. A flow is a path through skills.

## Routing

| Request... | Route to |
|---|---|
| Changes accepted decision (`actually`, `instead`, `forget that`) | `/decision-drift-guard` |
| Concrete feature, fix, or spec | `/implement` |
| Repeated progress across rounds | `/goal-loop` |
| Diff review | `/code-review` |
| PR description | `/pr-writing` |
| Bitbucket PR | `/bitbucket-helper` |
| Isolation before risky work | `/creating-worktrees` |
| Broad independent work | `/parallel-agents` |
| Split, merge, reshape services | `/codebase-design` |
| Go code | `/go` |
| Commit hygiene | `/git` |
| What code does, casual question, rename/typo | `no skill needed` |
| Vague goal or competing approaches | `/grilling` |
| Personal memory | `/personal-knowledge` |

Route only. Do not implement from this skill.

## Disciplines

- `/tdd` — red-green-refactor loop.
- `/code-review` — Standards and Spec axes.
- `/codebase-design` — module boundaries.
- `/go` — Go-specific rules.
- `/parallel-agents` — independent lanes.
- `/pr-writing` — PR description shape.
- `/git` — commit hygiene.
