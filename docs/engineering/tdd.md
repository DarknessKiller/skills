Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=tdd
```

```bash
npx skills update tdd
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/tdd)

## What it does

`tdd` drives changes through red-green-refactor. It proves one behaviour slice, makes it pass, then simplifies while the check stays green.

The defining constraint is the tight loop: no broad implementation before the next failing check exists.

## When to reach for it

Type `/tdd`, or let the agent reach for it automatically when a feature, bug fix, or regression can be proved by a small automated check.

## Red-green-refactor

The leading phrase is **tight feedback loop**. The skill chooses the highest-level cheap test that proves behaviour, avoids brittle mocks, and keeps fixtures out unless they earn their keep.

## It's working if

- The agent names the right source of truth before acting.
- The output uses the skill's leading words consistently.
- The next action is smaller and clearer than the original request.
- Red, Green, Refactor, Repeat, the passing check, normal command, and any untestable edge are explicit.

## Where it fits

This is the build discipline inside [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement). [code-review](https://github.com/darknesskiller/skills/tree/main/skills/engineering/code-review) checks the resulting diff; [codebase-design](https://github.com/darknesskiller/skills/tree/main/skills/engineering/codebase-design) helps choose seams. The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
