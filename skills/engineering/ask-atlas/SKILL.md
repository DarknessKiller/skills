---
name: ask-atlas
description: "Route to the next skill. Tell it your situation; it names the skill."
disable-model-invocation: true
argument-hint: "What are you trying to do?"
---

# Ask Atlas

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
