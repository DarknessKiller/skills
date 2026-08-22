---
name: tdd
description: "Red-green-refactor loop for new behaviour, bugs, or regressions."
---

# TDD

## Loop

1. **Red** — write one failing check for the next behaviour slice.
2. **Green** — make the smallest implementation pass.
3. **Refactor** — simplify while the check stays green.
4. Repeat until the contract is covered.

## Output

Name every phase: `Red`, `Green`, `Refactor`, `Repeat`. Finish with: `Passing check`, `Normal command`, `Untestable` (none or remaining edge).

Completion: every requested behavior has a passing check, the check ran in the repo's normal command, and any untestable edge is reported.

## Test choice

Prefer the highest-level test that proves the behaviour without brittle setup. HTTP paths: request/response tests. Service/repository: integration tests when practical. Go: table-driven with `testify/require` if project uses it. Keep mocks at boundaries. Do not mock what you can run cheaply. One `assert`-style self-check suffices for tiny cases.
