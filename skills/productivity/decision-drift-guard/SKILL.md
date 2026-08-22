---
name: decision-drift-guard
description: "Catch midstream decision changes. Use when a new instruction may replace, contradict, or branch an accepted decision."
---

# Decision Drift Guard

A supersession is a new accepted user decision replacing an earlier one. Make it explicit before consequential work.

## Steps

1. **Load the ledger.** Path: `.agents/decision-ledger/sessions/<session-id>.md` relative to worktree root. Use host session ID or derive from first request. Each session reads/writes only its own file. IF filesystem fails: keep ledger in context, say persistence unavailable.

2. **Track decisions.** One line per active decision: `D-<n> | scope | chosen approach | acceptance`. Suggestions stay proposed until user accepts.

3. **Classify new statement** against active decisions in same scope:

| Statement means... | Class | Action |
|---|---|---|
| Same meaning | same | continue |
| Adds detail or fixes mistake | refinement | update record |
| Separate scope | branch | create record |
| "Use this instead" | supersession | run Gate 1 |
| Cannot both hold | conflict | run Gate 1 |
| Cannot tell | unclear | ask one question |

Watch for: "actually", "instead", "forget that", "on second thought". Compare meaning, not phrase overlap.

4. **Gate 1** (supersession or conflict only): Show old decision, new instruction, impact. Ask: replace, branch, or refine. Wait for choice.

5. **Gate 2** (after replacement confirmed): IF touches architecture, public behavior, data shape, security, cost, or irreversible actions: run `/grilling` and wait. Otherwise ask only: which old assumption dies, what changes, what must stay.

6. **Commit supersession.** Mark old record superseded. Link new with `supersedes: D-<n>`. Recompute plan, tests, tool actions. Label stale recommendations.

Completion: one active record per replaced scope, every downstream action uses it.

## First pass format

- Ledger: loaded or unavailable.
- Classification: supersession or conflict.
- Old: `<old>`. New: `<new>`. Impact: `<changes>`.
- Paused. Choose: `replace`, `branch`, or `refine`.
