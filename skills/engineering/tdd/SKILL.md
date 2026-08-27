---
name: tdd
description: "Red-green-refactor loop with a real API E2E gate for HTTP behaviour."
disable-model-invocation: true
---

# TDD

## Loop

1. **Red** — write one failing check for the next behaviour slice.
2. **Red API** — for HTTP behaviour, add one live API scenario in `./e2e-scripts`.
3. **Green** — make the smallest implementation pass.
4. **API gate** — run the scenario against the running service over HTTP.
5. **Refactor** — simplify while every check stays green.
6. Repeat until the contract is covered.

## API E2E

Every HTTP behaviour slice needs a real request and response check.
Use or create `./e2e-scripts/api_e2e.py`.
Run it against a real running service.
Do not replace the service with a mock, stub, or in-process handler.

```bash
python3 ./e2e-scripts/api_e2e.py \
  --url "$API_BASE_URL/health" \
  --method GET \
  --expect-status 200 \
  --expect-json '{"status":"ok"}'
```

Record the service startup command and required environment in the test plan.
If the change has no HTTP boundary, report `Untestable: no API boundary`.

## Output

Name every phase: `Red`, `Red API`, `Green`, `API gate`, `Refactor`, `Repeat`. Finish with: `Passing check`, `API trace` (`header`, `request`, `resp`), `Normal command`, `Untestable` (none or remaining edge).

Completion: every requested behavior has a passing check, every HTTP behavior has a passing real API E2E check, checks ran in the repo's normal command, and any untestable edge is reported.

## Test choice

Prefer the highest-level test that proves the behaviour without brittle setup. HTTP paths: real API request/response tests plus focused lower-level checks. Service/repository: integration tests when practical. Go: table-driven with `testify/require` if project uses it. Keep mocks at boundaries. Do not mock what you can run cheaply. One `assert`-style self-check suffices for tiny cases.

## Local script

If `./e2e-scripts/api_e2e.py` is missing, write it before implementing the HTTP behaviour.
Keep project-local E2E scripts in `./e2e-scripts`.
