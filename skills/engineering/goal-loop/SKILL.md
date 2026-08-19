---
name: goal-loop
description: Advance a concrete goal in bounded verified rounds.
disable-model-invocation: true
argument-hint: "<goal> [max_rounds]"
---

# Goal Loop

Run a concrete goal through a bounded loop of action, evidence, and internal critique. The loop owns iteration; existing skills own domain work.

## Contract

1. Parse the goal and optional `max_rounds`; default to `5`. Reject a cap that is not a positive integer.
2. Infer observable completion criteria from the goal and repository context. Proceed with those criteria; record material uncertainty as a blocker only when it prevents a safe next action.
3. Choose the smallest useful next action and route it through an existing skill when one fits: `/implement`, `/tdd`, `/code-review`, `/git`, or a domain skill.
4. Verify the action with the narrowest useful check. Evidence is a test result, diff, command output, inspected artifact, or explicit external response.
5. Internally critique the result:
   - What evidence proves or disproves completion?
   - What remains unverified or assumed?
   - What is the smallest next action that can change the state?
6. Stop as soon as the completion criteria are evidenced. Otherwise continue until `max_rounds`.

## Round Boundary

A round is one meaningful state-changing or evidence-producing action followed by verification. Tool calls are implementation details, not rounds. Do not spend rounds restating the goal, polling without a state change, or making speculative cleanup.

## Authorization

Pause before destructive actions or external mutations: commits, pushes, PR creation or approval, deployment, production changes, credential use, or irreversible data operations. State the exact action that needs authorization. Continue with safe local inspection and edits when the contract is clear.

## Ledger

Keep a compact in-turn ledger with:

```text
round | action | evidence | critique | next action
```

Do not write a repository ledger or personal-memory note. The ledger is transient execution state.

## Terminal Status

End with exactly one status:

- `completed` — completion criteria are evidenced.
- `blocked` — progress requires missing access, authorization, an unresolved material choice, or a failing external dependency; name the unblocker.
- `max_rounds` — the cap was reached before completion; name the remaining criteria and strongest evidence.

The final response contains the status and compact ledger. Never claim completion from intent, an unchanged command, or an unverified assumption.
