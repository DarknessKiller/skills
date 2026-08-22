---
name: decision-drift-guard
description: "Catch midstream decision changes before plans drift. Use when a new instruction may replace, contradict, or branch an accepted decision."
---

# Decision Drift Guard

A supersession is a new accepted user decision replacing an earlier one. Users often make this implicitly. Make it explicit before consequential work.

## First pass

When a request changes an accepted decision, load, classify, show the conflict, ask `replace`, `branch`, or `refine`, then stop. Do not supersede the old decision before the user chooses.

Run this guard before planning, editing files, or calling consequential tools. Skip it for wording, formatting, or implementation details that preserve accepted behavior.

## Steps

1. **Load the ledger.**
   - Path: `.agents/decision-ledger/sessions/<session-id>.md`, relative to the worktree root (nearest directory containing `.git`; otherwise project root).
   - Use the host agent's session ID when available. Otherwise derive one from the first user request and store it in the ledger header.
   - Each session reads and writes only its own file. Import an older ledger only when the user asks.
   - IF filesystem writes fail: keep the ledger in context and say persistence is unavailable.

2. **Track decisions.**
   - One line per active decision: `D-<n> | scope | chosen approach | acceptance`.
   - Assistant suggestions stay proposed until the user accepts them.

3. **Classify each new statement** against active decisions in the same scope:

   | New statement means... | Class | Action |
   |---|---|---|
   | Same meaning and constraints | same | continue |
   | Adds detail or fixes an assistant mistake | refinement | update the record |
   | Separate scope or parallel option | branch | create a separate record |
   | "Use this instead" | supersession | run Gate 1 |
   | Old and new cannot both hold | conflict | run Gate 1 |
   | Cannot tell | unclear | ask one focused question |

   Watch for implicit change markers: "actually", "instead", "forget that", "on second thought". Compare meaning, not phrase overlap.

4. **Gate 1 — confirm intent** (only for supersession or conflict):
   - Show three lines: old decision, new instruction, impact.
   - Ask the user to choose: replace, branch, or refine.
   - Wait for an unambiguous choice. A bare "yes" counts only when exactly one option is plausible.

5. **Gate 2 — review material changes** (after Gate 1 confirms replacement):
   - IF the change touches architecture, public behavior, data shape, security, cost, deadlines, or irreversible actions: run `/grilling` — or `/codebase-design` for boundaries, `/tdd` for behavior regressions — and wait for its confirmation point.
   - Otherwise ask only: which old assumption dies, what changes, what must stay.

6. **Commit the supersession.**
   - Mark the old record superseded. Link the new record with `supersedes: D-<n>`.
   - Recompute the plan, tests, and tool actions against the new record. Label stale recommendations stale.
   - Continue with the smallest plan consistent with the ledger.

Completion: one active record per replaced scope, every downstream action uses it, and the response states the active decision in one sentence.

## Response style

First pass:

- Ledger: loaded or unavailable at `.agents/decision-ledger/sessions/<session-id>.md`.
- Classification: supersession or conflict.
- Old decision: `<old>`.
- New instruction: `<new>`.
- Impact: `<what changes>`.
- Plan paused.
- Choose: `replace`, `branch`, or `refine`.
