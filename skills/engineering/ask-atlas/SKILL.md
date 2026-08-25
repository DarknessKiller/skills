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
| Wants a test-first check for new behavior | `/tdd` |
| Repeated progress across rounds | `/goal-loop` |
| Diff review | `/code-review` |
| Creates, updates, or asks for a PR or pull request description | `/pr-writing` |
| Bitbucket PR | `/bitbucket-helper` |
| Isolation before risky work | `/creating-worktrees` |
| Broad independent work | `/parallel-agents` |
| Asks whether to split a service into separate modules or reshape boundaries | `/codebase-design` |
| Go code | `/go` |
| Commit hygiene | `/git` |
| Vague goal or competing approaches | `/grilling` |
| Personal memory | `/personal-knowledge` |

On match, invoke the routed skill with your skill tool immediately. Do not name it and wait.
If the route will not load, name the exact command for the user to run.
`no skill needed`: answer directly, load nothing.

Do not implement the work inside this skill. Routing ends when the routed skill takes over.
