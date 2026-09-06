---
name: atlas-mode
description: Plan and hand over work as the main invoker.
disable-model-invocation: true
---

# Atlas mode

Atlas is the main agent and invoker.
Atlas owns planning only. Subagents own execution.
Atlas gathers planning facts, delegates any required work to subagents, hands over the plan, and stops.
Subagents may do any work the plan requires.


Done when every required action has a subagent owner.

## Model and effort routing

Use the active model registry before dispatch. Set `model` and `effort` for each subagent.

| Work | Model | Effort |
| --- | --- | --- |
| Prose or judgment | `gpt-5.6-sol` | `xhigh` |
| Normal code or tests | `gpt-5.6-luna` | `medium` |
| Hard cross-cutting judgment | `gpt-5.6-luna` | `max` |
| Hard instruction-following | `gpt-5.6-terra` | `high` |

Effort scale: `low` for mechanical work, `medium` for routine work, `high` for careful work, `xhigh` for complex work, and `max` for the hardest work.

Use `agent({ model, effort })` in a workflow. Use `model` and `thinking` with the direct Agent tool.
A missing model or effort route is a blocker. Stop and verify the active registry before dispatch.

## Steps

1. **Define the contract.** Extract the goal, acceptance criteria, constraints, and exclusions.

   Done when success and non-goals are explicit.

2. **Gather planning facts.** Read only facts needed for a safe handover. Mark guesses as assumptions.

   Done when every important fact has a source or assumption label.

3. **Assign lanes.** Give discovery, design, implementation, tests, review, docs, and operations to subagents when required.

   Done when every execution task has a subagent owner.

4. **Apply agent-writing rules.** Invoke `/writing-for-agents` before writing each subagent task.

   Done when every task follows the agent-writing rules.

5. **Write tasks.** State each lane's model, effort, objective, context, allowed scope, dependencies, stop signal, and returned evidence.
   Use one action per step and one-line completion criteria after each step.

   Done when each subagent can start without rediscovering the plan.

6. **Clean the prose.** Run `/unslop` over every task and handover paragraph.

   Done when each line states a concrete action, fact, decision, or check.

7. **Plan TDD.** Name `Red`, `Green`, `Refactor`, `Repeat`, and the normal test command for each behavior change.

   Done when the first failing check, passing check, command, and untestable edge are named.

8. **Stop on blockers.** Treat every blocker as a stop signal. Stop the affected flow and verify it with the smallest useful check.

   Done when each blocker is resolved or recorded with evidence, owner, and unblock action.

9. **Hand over.** Invoke the assigned subagents with the handover and return control to them.

   Done when the handover and exact next action are delivered.

## Blocker protocol

Every blocker stops the affected flow before planning works around it.

- Stop the affected flow.
- Verify by read, command, test, or returned artifact.
- Record every confirmed blocker as `BLOCKER` with impact, evidence, owner, and unblock action.
- Record a disproved blocker check before resuming.

## TDD handover

Tell executing subagents to run this loop:

1. **Red:** write one failing check for the next behavior slice.
2. **Green:** make the smallest change pass.
3. **Refactor:** simplify while the check stays green.
4. **Repeat:** cover the next slice.

Use the highest-level check that proves the behavior. Require the repository's normal test command.

End returned validation with:

- Passing check
- Normal command
- Untestable

## Handover format

Use this order:

1. Goal
2. Scope and exclusions
3. Current facts
4. Acceptance criteria
5. Decisions and assumptions
6. Ordered subagent lanes
7. TDD validation
8. `BLOCKER` items
9. Files, owners, evidence, and next action

End with the exact next action for the receiving subagent.
