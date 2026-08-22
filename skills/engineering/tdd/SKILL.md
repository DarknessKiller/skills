---
name: tdd
description: "Red-green-refactor loop. Use when implementing new behaviour, fixing bugs, or locking down regressions with a small automated check."
---

# TDD

Use the shortest feedback loop that proves behaviour.

## Required sequence

For new behaviour, start with a failing check. Do not write the implementation first. Name each phase: Red, Green, Refactor.

## Loop

1. **Red** — write one failing check for the next behaviour slice.
2. **Green** — make the smallest implementation pass.
3. **Refactor** — simplify while the check stays green.
4. Repeat until the contract is covered.

## Output format

Name every phase: `Red`, `Green`, `Refactor`, `Repeat`.

Finish with:

- `Passing check`: the check that passes.
- `Normal command`: the command that ran it.
- `Untestable`: none, or the remaining edge.

Completion: every requested behavior has a passing check, the check ran in the repo's normal command, and any untestable edge is reported.

## Test choice

- Prefer the highest-level test that proves the behaviour without brittle setup.
- HTTP paths: prefer request/response tests.
- Service/repository/multi-layer: prefer integration tests when practical.
- Go: prefer table-driven tests and `testify/require` when the project already uses it.
- Keep mocks at boundaries. Do not mock code you can run cheaply.

Do not add a test framework, fixtures, or test helpers for one tiny case. A single `assert`-style self-check is enough when that is the repo's smallest runnable loop.
