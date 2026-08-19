Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=goal-loop
```

```bash
npx skills update goal-loop
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/goal-loop)

## What it does

`goal-loop` advances a concrete goal through at most five default rounds of meaningful action, verification, and internal critique. It reports a compact ledger and one terminal status instead of claiming progress from intent.

## When to reach for it

Type `/goal-loop <goal>` when one pass is unlikely to finish the work and each iteration can produce observable evidence. Add a positive integer round cap when the goal needs a tighter or larger budget.

## Boundaries

The loop is in-turn and transient. It does not schedule work, create a project backlog, replace implementation or review disciplines, or write a persistent goal ledger. It pauses before destructive actions and external mutations.

## It's working if

- The agent states observable completion criteria before acting.
- Every round has a meaningful action and evidence.
- Internal critique selects the smallest next action instead of producing repeated planning prose.
- The final response contains a compact ledger and exactly one of `completed`, `blocked`, or `max_rounds`.

## Where it fits

Use it after the goal is concrete and before or around [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement). It routes domain work to [tdd](https://github.com/darknesskiller/skills/tree/main/skills/engineering/tdd), [code-review](https://github.com/darknesskiller/skills/tree/main/skills/engineering/code-review), [git](https://github.com/darknesskiller/skills/tree/main/skills/engineering/git), and other relevant skills. The full routing map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
