---
name: goal-loop
description: "Advance a concrete goal in bounded verified rounds of action, evidence, and critique."
disable-model-invocation: true
argument-hint: "<goal> [max_rounds]"
---

# Goal Loop

Run a concrete goal through a bounded loop. Each round is one action, one verification, one critique. The loop owns iteration. Existing skills own domain work.

## Contract

1. **Parse the goal and round cap.**
   - Read the goal from the argument.
   - Read `max_rounds` from the argument. Default to `5`.
   - IF `max_rounds` is not a positive integer: reject it and stop.

2. **Infer completion criteria.**
   - Look at the goal and the repository context.
   - List observable criteria that prove the goal is done.
   - IF a criterion is uncertain but does not block the next action: record it and proceed.
   - IF a criterion is uncertain and blocks the next action: record it as a blocker.

3. **Choose the next action.**
   - Pick the smallest useful action.
   - Route it through an existing skill when one fits: `/implement`, `/tdd`, `/code-review`, `/git`, or a domain skill.

4. **Verify the action.**
   - Run the narrowest useful check.
   - Evidence is: a test result, a diff, a command output, an inspected artifact, or an explicit external response.

5. **Critique the result.**
   - What evidence proves or disproves completion?
   - What remains unverified or assumed?
   - What is the smallest next action that can change the state?

6. **Check for completion.**
   - IF the completion criteria are evidenced: stop with `completed`.
   - IF the round cap is reached: stop with `max_rounds`.
   - Otherwise: repeat from step 3.

**Done when:**
- [ ] Completion criteria are listed.
- [ ] Each round has one action, one verification, and one critique.
- [ ] The final status is exactly one of: `completed`, `blocked`, `max_rounds`.

## Round boundary

A round is one state-changing or evidence-producing action plus its verification. Tool calls are implementation details, not rounds.

Do NOT spend rounds on:
- Restating the goal.
- Polling without a state change.
- Speculative cleanup.

## Authorization

Pause before these actions. State the exact action that needs authorization.

- Commits, pushes, PR creation or approval.
- Deployment, production changes.
- Credential use.
- Irreversible data operations.

Continue with safe local inspection and edits when the contract is clear.

## Ledger

Keep a compact in-turn ledger:

```text
round | action | evidence | critique | next action
```

- The ledger is transient. Do not write it to a file or personal memory.
- The final response contains the status and the compact ledger.

## Terminal status

End with exactly one:

- `completed` — completion criteria are evidenced.
- `blocked` — name the unblocker (missing access, authorization, unresolved choice, or failing dependency).
- `max_rounds` — name the remaining criteria and strongest evidence.

Never claim completion from intent, an unchanged command, or an unverified assumption.
