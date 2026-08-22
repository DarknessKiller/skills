---
name: goal-loop
description: "Advance a concrete goal in bounded verified rounds of action, evidence, and critique."
disable-model-invocation: true
argument-hint: "<goal> [max_rounds]"
---

# Goal Loop

Run a concrete goal through a bounded loop. Each round: one action, one verification, one critique. The loop owns iteration. Existing skills own domain work.

## Contract

1. Parse the goal. Read `max_rounds` (default `5`). Reject a cap that is not a positive integer.
2. Infer observable completion criteria from the goal and repo context. Record material uncertainty as a blocker only when it prevents a safe next action.
3. Choose the smallest useful next action. Route through an existing skill when one fits: `/implement`, `/tdd`, `/code-review`, `/git`, or a domain skill.
4. Verify with the narrowest useful check: test result, diff, command output, artifact, or external response.
5. Critique: what proves or disproves completion? What remains unverified? What is the smallest next action?
6. IF completion criteria are evidenced: stop with `completed`. IF `max_rounds` reached: stop with `max_rounds`. Otherwise repeat from step 3.

## Round boundary

A round is one state-changing or evidence-producing action plus verification. Tool calls are not rounds. Do not spend rounds restating the goal, polling without a state change, or speculative cleanup.

## Authorization

Pause before commits, pushes, PR creation/approval, deployment, production changes, credential use, or irreversible data operations. State the exact action needing authorization. Continue with safe local work when the contract is clear.

## Ledger

Keep a compact in-turn ledger: `round | action | evidence | critique | next action`. Transient — do not write to a file or personal memory. The final response contains the status and compact ledger.

## Terminal status

End with exactly one:
- `completed` — completion criteria evidenced.
- `blocked` — name the unblocker.
- `max_rounds` — name remaining criteria and strongest evidence.

Never claim completion from intent, an unchanged command, or an unverified assumption.
