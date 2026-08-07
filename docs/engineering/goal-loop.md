Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=goal-loop
```

```bash
npx skills update goal-loop
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/goal-loop)

## What it does

`goal-loop` runs a user-defined goal through bounded progress-and-critique rounds. It defaults to 10 rounds, accepts a custom positive round cap, grills each result for missing evidence and failure modes, and stops on verified completion or a clear blocker.

## When to reach for it

Use `/goal-loop <goal>` when one pass is unlikely to be enough and the work can be judged by observable completion criteria. Add a round cap when the goal needs a tighter or larger budget.

## Boundaries

The loop is in-turn and bounded; it is not a scheduled or cross-session job. It does not replace implementation, testing, review, or Git skills: it delegates each round to the smallest relevant existing skill and keeps only the iteration and self-grill contract.

## Where it fits

Use it after the idea is clear and before or around `/implement`. Use `/tdd`, `/code-review`, `/git`, and other domain skills inside rounds when their discipline applies. The full routing map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).

## Done when

The final response contains a compact round ledger and exactly one terminal status: `completed`, `max_rounds`, or `blocked`, with evidence or the unblocker.
