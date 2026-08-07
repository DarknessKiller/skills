---
name: goal-loop
description: Work toward a user-defined goal in bounded iterations, self-grilling after each round and stopping on evidence or a configurable round cap.
disable-model-invocation: true
argument-hint: "<goal> [max_rounds]"
---

# Goal Loop

Use when a goal needs repeated progress-and-critique cycles rather than one pass.

## Run

1. Parse the goal and optional `max_rounds`; default to `10`. Reject a cap that is not a positive integer.
2. Define observable completion criteria before acting. If the goal is ambiguous, ask one focused clarification instead of guessing.
3. Run the smallest useful next action. Reuse the relevant skill (`/implement`, `/tdd`, `/code-review`, `/git`, or another domain skill) instead of recreating its process.
4. Grill the result before the next round:
   - What evidence says the goal is complete?
   - What remains or is merely assumed?
   - What could make the result wrong, incomplete, or fragile?
   - What is the smallest next action?
5. Stop immediately when the completion criteria are evidenced. Otherwise continue until `max_rounds`.
6. If progress is blocked by missing access, an unresolved choice, or a failing external dependency, stop with `blocked` and state the unblocker.

## Contract

Keep a compact round ledger: round number, action, evidence, grill finding, and next action. Never claim completion without evidence. End with exactly one status: `completed`, `max_rounds`, or `blocked`, plus the evidence or unblocker.

A round is one meaningful action followed by its grill. Do not spend rounds restating the goal, polling without a state change, or making speculative cleanup.
