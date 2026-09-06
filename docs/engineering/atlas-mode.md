Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills -s atlas-mode
```

```bash
npx skills update atlas-mode
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/atlas-mode)

## What it does

`atlas-mode` makes Atlas the main invoker. Atlas plans the work, hands it to subagents, and stops. Subagents own any required discovery, design, implementation, tests, review, documentation, or operations.

## When to reach for it

Use `/atlas-mode <request>` when you want a written plan handed to another agent instead of direct execution.

## Task writing

Atlas applies `/writing-for-agents` to every subagent task. It runs `/unslop` over the task prose. Each step has one action and one-line completion criteria.

## Model and effort routing

Atlas assigns a model and effort to each subagent.

| Work | Model | Effort |
| --- | --- | --- |
| Prose or judgment | `gpt-5.6-sol` | `xhigh` |
| Normal code or tests | `gpt-5.6-luna` | `medium` |
| Hard cross-cutting judgment | `gpt-5.6-luna` | `max` |
| Hard instruction-following | `gpt-5.6-terra` | `high` |

A missing route stops dispatch until the active model registry is verified.

## Blocker behavior

Every blocker stops the affected flow. Verify it with the smallest useful check. Record confirmed blockers with evidence, impact, owner, and an unblock action.

## TDD validation

Code and behavior work is handed over with a `Red`, `Green`, `Refactor`, and `Repeat` loop. The handover names the first failing check, normal test command, passing check, and any untestable edge.

## It's working if

The handover gives each subagent a bounded objective, scope, dependency, stop condition, and evidence format. Subagents own execution.

## Where it fits

Use it before [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement) when another agent should own execution. Pair it with [tdd](https://github.com/darknesskiller/skills/tree/main/skills/engineering/tdd) for behavior changes.
