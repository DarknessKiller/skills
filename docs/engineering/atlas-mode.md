Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills -s atlas-mode
```

```bash
npx skills update atlas-mode
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/atlas-mode)

## What it does

`atlas-mode` makes Atlas the main invoker. Atlas plans, hands work to subagents, stops. Subagents own discovery, design, implementation, tests, review, docs, operations.

## When to reach for it

Use `/atlas-mode <request>` when you want a plan handed to another agent instead of direct execution.

## User override

Your word wins. Name a form, tool, or flow: Atlas uses it as asked.

- Workflow, fan out, parallel run, orchestrate: workflow dispatch.
- Subagent, delegate, direct agent: direct dispatch.
- `/atlas-mode`, `/parallel-agents`, or any named flow: that flow runs.

## Dispatch routing

No explicit choice: Atlas picks by task shape.

- **Direct dispatch**: one subagent owns one task; main thread stays in control. Launch each `Agent`, integrate inline.
- **Workflow dispatch**: many subagents on one task; phases, fan-out, verify, resume matter. One `workflow` run, one artifact.
- **`/parallel-agents`**: user-invoked flow for parallel subagents on split lanes.

Small request: no dispatch. One-line lookup, small edit, question: answer or edit inline.

## Task writing

Atlas runs `/writing-for-agents` on every subagent task. Runs `/unslop` over task prose. One action per step. One-line completion after each step.

## Model and effort routing

Atlas assigns a model and effort per subagent.

| Work | Model | Effort |
| --- | --- | --- |
| Prose or judgment | `gpt-5.6-sol` | `high` |
| Normal code or tests | `gpt-5.6-luna` | `medium` |
| Hard cross-cutting judgment | `gpt-5.6-luna` | `max` |
| Hard instruction-following | `gpt-5.6-terra` | `max` |

Missing route stops dispatch until the registry is verified.

## Blocker behavior

Every blocker stops the flow. Verify with the smallest useful check. Record blockers with evidence, impact, owner, unblock action.

## TDD validation

Code work hands over with a `Red`, `Green`, `Refactor`, `Repeat` loop. Handover names first failing check, normal command, passing check, untestable edge.

## It's working if

Each subagent gets a bounded objective, scope, dependency, stop condition, evidence format. Subagents own execution.

## Where it fits

Use it before [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement) when another agent should execute. Pair with [tdd](https://github.com/darknesskiller/skills/tree/main/skills/engineering/tdd) for behavior changes. Complements [parallel-agents](https://github.com/darknesskiller/skills/tree/main/skills/engineering/parallel-agents), the fan-out flow.
