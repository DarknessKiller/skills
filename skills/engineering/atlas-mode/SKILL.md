---
name: atlas-mode
description: Plan and hand over work as the main invoker.
disable-model-invocation: true
---

# Atlas mode

Atlas is the main agent and invoker.
Atlas owns planning only. Subagents execute.
Atlas gathers planning facts, delegates any required work, hands over the plan, stops.

## Workflow dispatch

Use for many lanes on one task, parallel work, phases, verify, resume.

Run the `workflow` tool. Set `model` and `effort` per lane:

`agent({ model, effort })`

One run owns its lanes. One run returns one artifact.

## Direct dispatch

Use for one task, one agent. Main thread stays in control.

Run the `Agent` tool. Set `model` and `thinking`.

Done when every action has a subagent owner.

## User override

User's word wins. User names a form, tool, or flow: use it as asked.

- Workflow, fan out, parallel, orchestrate: workflow dispatch.
- Subagent, delegate, direct agent: direct dispatch.
- `/parallel-agents` or any named flow: run that flow.

Work already in progress: let it finish before dispatch.

## Dispatch routing

No user choice: pick by shape.

| Shape | Dispatch |
| --- | --- |
| One task; main thread in control | Direct: launch `Agent`, integrate inline |
| Many lanes; parallel or phased; verify, judge, resume | Workflow: one `workflow` run, one artifact |
| Split lanes for parallel subagents; safe writes; read fan-out | `/parallel-agents` |

Small request: no dispatch. One-line lookup, small edit, question: answer or edit inline.

Run `npm run check` after edits.

## Model and effort routing

Check active model registry first. Set `model` and `effort` per agent.

| Work | Model | Effort |
| --- | --- | --- |
| Prose or judgment | `gpt-5.6-sol` | `high` |
| Normal code or tests | `gpt-5.6-luna` | `medium` |
| Hard cross-cutting judgment | `gpt-5.6-luna` | `max` |
| Hard instruction-following | `gpt-5.6-terra` | `max` |

Effort scale: `low` mechanical, `medium` routine, `high` careful, `xhigh` complex, `max` hardest.

Workflow: `agent({ model, effort })`. Direct: `Agent` with `model`, `thinking`.

Missing route is a blocker. Verify registry first.

## Steps

1. **Define contract.** State goal, acceptance criteria, constraints, exclusions.

   Done when success and non-goals are explicit.

2. **Gather planning facts.** Read only facts needed for a safe handover. Mark guesses as assumptions.

   Done when every fact has a source or assumption label.

3. **Assign lanes.** Give discovery, design, implementation, tests, review, docs, operations to subagents.

   Done when every task has a subagent owner.

4. **Apply writing rules.** Invoke `/writing-for-agents` before each task.

   Done when every task follows the rules.

5. **Write tasks.** State each lane's model, effort, objective, context, scope, dependencies, stop signal, evidence.
   One action per step. One-line completion after each step.

   Done when each subagent starts without rediscovery.

6. **Clean prose.** Run `/unslop` over tasks and handover.

   Done when each line states one action, fact, decision, or check.

7. **Plan TDD.** Name `Red`, `Green`, `Refactor`, `Repeat`, and normal test command.

   Done when first failing check, passing check, command, untestable edge are named.

8. **Stop on blockers.** Verify with the smallest useful check.

   Done when each blocker is resolved or recorded with evidence, owner, unblock action.

9. **Hand over.** Launch subagents. Return control.

   Done when handover and next action are delivered.

## Blocker protocol

Every blocker stops the flow first.

- Stop the flow.
- Verify by read, command, test, artifact.
- Record blocker: impact, evidence, owner, unblock action.
- Record a disproved check before resuming.

## TDD handover

Executing subagents run:

1. **Red:** write one failing check.
2. **Green:** make the smallest change pass.
3. **Refactor:** simplify while the check stays green.
4. **Repeat:** cover the next slice.

Use the highest-level check that proves behavior. Use the repo's normal test command.

End validation with:

- Passing check
- Normal command
- Untestable

## Handover format

In order:

1. Goal
2. Scope and exclusions
3. Current facts
4. Acceptance criteria
5. Decisions and assumptions
6. Ordered subagent lanes
7. TDD validation
8. `BLOCKER` items
9. Files, owners, evidence, next action

End with the exact next action for the receiving subagent.
