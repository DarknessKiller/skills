Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=go
```

```bash
npx skills update go
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/go)

## What it does

`go` is the Go coding standard for this agent setup. It prefers explicit code, request-context propagation, wrapped errors, standard-library solutions, and tests for new behaviour.

The defining constraint is context safety: request flows propagate the existing context instead of inventing a new one.

## When to reach for it

Type `/go`, or let the agent reach for it automatically when writing, reviewing, or refactoring Go.

## Context-safe Go

The leading phrase is **propagate context**. Constructors inject dependencies, packages avoid mutable globals, and errors carry enough context to debug the caller's path.

## It's working if

- The agent names the right source of truth before acting.
- The output uses the skill's leading words consistently.
- The next action is smaller and clearer than the original request.
- Context, dependencies, errors, local patterns, and relevant tests are accounted for.

## Where it fits

This is a language-specific discipline underneath [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement), [tdd](https://github.com/darknesskiller/skills/tree/main/skills/engineering/tdd), and [code-review](https://github.com/darknesskiller/skills/tree/main/skills/engineering/code-review). The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
