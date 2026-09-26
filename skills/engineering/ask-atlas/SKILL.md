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
| Acts as the main invoker and hands a plan to subagents | `/atlas-mode` |
| Diff review | `/code-review` |
| Creates or updates a PR title or description | `/pr-writing` |
| Bitbucket PR | `/bitbucket-helper` |
| Isolation before risky work | `/creating-worktrees` |
| Explicitly requests parallel or multi-agent work | `/parallel-agents` |
| Asks whether to split a service into separate modules or reshape boundaries | `/codebase-design` |
| Go code | `/go` |
| Commit hygiene | `/git` |
| Vague goal or competing approaches | `/grilling` |
| Personal memory | `/personal-knowledge` |

On match: read `<skill-dir>/../<route name>/SKILL.md` relative to this skill's directory (the harness resolves it), then follow it.
Read the file directly. A route with `disable-model-invocation: true` is still readable.
Do not invoke the route through a skill tool.
File missing: try `../../<bucket>/<route name>/SKILL.md`.
Still missing: name the exact command for the user.
`no skill needed`: answer directly, load nothing.

Do not implement from this skill.
