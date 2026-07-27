---
name: tdd
description: Test-driven development with a red-green-refactor loop. Use when implementing new behaviour, fixing bugs, or locking down regressions where a small automated check can prove the change.
---

# TDD

Use the shortest feedback loop that proves behaviour.

## Loop

1. **Red** — write one failing check for the next behaviour slice.
2. **Green** — make the smallest implementation pass.
3. **Refactor** — simplify while the check stays green.
4. Repeat until the contract is covered.

## Test choice

- Prefer the highest-level test that proves the behaviour without brittle setup.
- HTTP paths: prefer request/response tests.
- Service, repository, or multi-layer behaviour: prefer integration tests when practical.
- Go: prefer table-driven tests and `testify/require` when the project already uses it.
- Keep mocks at boundaries. Do not mock code you can run cheaply.

## Boundaries

Do not add a test framework, fixtures, or test helpers for one tiny case. A single `assert`-style self-check is enough when that is the repo's smallest runnable loop.
