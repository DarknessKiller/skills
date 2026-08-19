Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=codebase-design
```

```bash
npx skills update codebase-design
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/codebase-design)

## What it does

`codebase-design` gives the shared vocabulary for module shape and boundaries. It keeps behaviour behind useful seams instead of scattering it through handlers, services, and repositories.

The defining constraint is depth: a module should provide a lot of behaviour through a small interface.

## When to reach for it

Type `/codebase-design`, or let the agent reach for it automatically when architecture, refactoring, boundaries, or misplaced behaviour matter.

## Deep modules

The leading phrase is **deep module**. Handlers translate, services decide, repositories persist, and adapters isolate external systems. A good seam reduces future edits.

## It's working if

- The agent names the right source of truth before acting.
- The output uses the skill's leading words consistently.
- The next action is smaller and clearer than the original request.
- Each changed behavior has one natural owner and a testable seam.

## Where it fits

This is a model-invoked discipline under [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement), [tdd](https://github.com/darknesskiller/skills/tree/main/skills/engineering/tdd), and [code-review](https://github.com/darknesskiller/skills/tree/main/skills/engineering/code-review). The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
