---
name: goal-loop
description: "Advance a concrete goal in bounded verified rounds. Each round: action, evidence, critique."
disable-model-invocation: true
argument-hint: "<goal> [max_rounds]"
---

# Goal Loop

Bounded loop for concrete goals. Each round: one action, one verification, one critique.

## Steps

1. Parse goal. Read `max_rounds` (default `5`). Reject non-positive integer.
2. Infer completion criteria from goal and repo context. Record uncertainty as blocker only when it prevents safe next action.
3. Choose smallest useful next action. Route through existing skill when one fits.
4. Verify with narrowest useful check: test, diff, command output, artifact.
5. Critique: what proves or disproves completion? What remains? Smallest next action?
6. IF criteria evidenced: stop `completed`. IF max_rounds: stop `max_rounds`. Else repeat from 3.

## Rules

- A round = one state-changing action + verification. Tool calls are not rounds.
- Do not spend rounds restating goal, polling without change, or speculative cleanup.
- Pause before commits, pushes, PR, deploy, production, credentials, irreversible ops.

## Ledger

In-turn: `round | action | evidence | critique | next`. Transient only.

## Status

End with exactly one: `completed`, `blocked` (name unblocker), `max_rounds` (name remaining criteria).
