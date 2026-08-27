Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills -s api-e2e
```

```bash
npx skills update api-e2e
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/api-e2e)

## What it does

`api-e2e` is an opt-in extension for a TDD run. It runs a real HTTP request against a running API, checks status, body text, or exact JSON, and prints `header`, `request`, and `resp` records. Default `/tdd` behavior stays unchanged.

## When to reach for it

Type `/api-e2e` when you want to add the API gate to a TDD run. It is user-invoked only.

## Prerequisites

Python 3, a running API, and the project-local `./e2e-scripts/api_e2e.py` runner. The skill writes the runner when it is missing.

## Trace

The runner shows the request contract before sending it and the response after receiving it. Mocks, stubs, and in-process handlers do not satisfy the check.

## It's working if

- The request reaches a real running service.
- `header`, `request`, and `resp` are output in order.
- The expected response assertion passes.

## Where it fits

Use it as the user-invoked API gate inside [tdd](https://github.com/darknesskiller/skills/tree/main/skills/engineering/tdd). The main route lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
