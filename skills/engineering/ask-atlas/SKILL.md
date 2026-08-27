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
| Makes a rename-only or typo-only edit with no behavior change | `no skill needed` |
| Asks what existing code does or asks a casual question | `no skill needed` |
| Concrete feature, fix, or spec | `/implement` |
| Wants a test-first check for new behavior | Name `/tdd`; the user invokes it |
| Repeated progress across rounds | `/goal-loop` |
| Diff review | `/code-review` |
| Creates or updates a PR or pull request description | `/pr-writing` |
| Bitbucket PR | `/bitbucket-helper` |
| Isolation before risky work | `/creating-worktrees` |
| Explicitly requests parallel or multi-agent work | `/parallel-agents` |
| Asks whether to split a service into separate modules or reshape boundaries | `/codebase-design` |
| Go code | `/go` |
| Commit hygiene | `/git` |
| Vague goal or competing approaches | `/grilling` |
| Personal memory | `/personal-knowledge` |

On match, invoke the routed skill with your skill tool immediately.
Route will not load: name the exact command for the user.
`no skill needed`: answer directly, load nothing.

Do not implement from this skill.
