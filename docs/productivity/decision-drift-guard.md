Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=decision-drift-guard
```

```bash
npx skills update decision-drift-guard
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/productivity/decision-drift-guard)

## What it does

Keeps accepted requirements in a plain-Markdown ledger at `.agents/decision-ledger/sessions/<session-id>.md`, scoped to the current worktree and session. When a new message may replace or contradict an earlier decision, it pauses for an explicit replace/branch/refine choice. It does not supersede the old decision until the user chooses, then runs a targeted review before consequential work.

Storage is generic filesystem state — no Pi, Claude, or Codex session APIs. If writes fail, the ledger stays in context and the agent says persistence is unavailable.

## When to reach for it

The model fires this automatically when a user changes direction midstream — planning, architecture, data design, safety-sensitive work, or anything costly to undo. Watch phrases include "actually", "instead", and "on second thought".

It stays out of the way for wording changes, harmless refinements, and implementation details that preserve accepted behavior.

## The gates

Two gates stand between a detected change and action:

1. **Confirm intent** — show old decision, new instruction, impact; get an unambiguous replace/branch/refine choice.
2. **Review material changes** — hand architecture, data, security, cost, deadline, or irreversible changes to `/grilling`, `/codebase-design`, or `/tdd` and wait for its confirmation point.

## It's working if

The agent names the affected decision, pauses before acting on a material conflict, gets an unambiguous user choice, carries only the confirmed decision forward, and never mixes ledgers from another worktree or session.

## Where it fits

This is a model-invoked, agent-neutral productivity discipline. It runs before implementation flows and hands material changes to [grilling](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement) flows, [codebase-design](https://github.com/darknesskiller/skills/tree/main/skills/engineering/codebase-design), or [tdd](https://github.com/darknesskiller/skills/tree/main/skills/engineering/tdd). The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
