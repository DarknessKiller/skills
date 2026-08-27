Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills -s tdd
```

```bash
npx skills update tdd
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/tdd)

## What it does

`tdd` drives changes through red-green-refactor. It proves one behaviour slice, makes it pass, then simplifies while the check stays green. HTTP behaviour also needs a real API E2E check.

The defining constraint is the tight loop: no broad implementation before the next failing check exists. A mocked client or in-process handler does not satisfy the API gate.

## When to reach for it

Type `/tdd`, or let the agent reach for it automatically when a feature, bug fix, or regression can be proved by a small automated check.

## Red-green-refactor

The leading phrase is **tight feedback loop**. The skill chooses the highest-level cheap test that proves behaviour, avoids brittle mocks, and keeps fixtures out unless they earn their keep.

## API E2E gate

For each HTTP behaviour slice, point the user to `/api-e2e`. That user-invoked extension owns the project-local stdlib runner at `./e2e-scripts/api_e2e.py` and checks status, body text, or exact JSON.

Prerequisites: Python 3 and a running API. Pass the base URL, startup command, and required environment through the project test plan. The runner outputs `header`, `request`, and `resp` records in that order.

```bash
python3 ./e2e-scripts/api_e2e.py \
  --url "$API_BASE_URL/health" \
  --expect-status 200 \
  --expect-json '{"status":"ok"}'
```

## It's working if

- The agent names the right source of truth before acting.
- The output uses the skill's leading words consistently.
- The next action is smaller and clearer than the original request.
- Red, Red API, Green, API gate, Refactor, Repeat, the passing checks, normal command, and any untestable edge are explicit.

## Where it fits

This is the build discipline inside [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement). [code-review](https://github.com/darknesskiller/skills/tree/main/skills/engineering/code-review) checks the resulting diff; [codebase-design](https://github.com/darknesskiller/skills/tree/main/skills/engineering/codebase-design) helps choose seams. The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
