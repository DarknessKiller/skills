---
name: go
description: Go implementation standards. Use when writing, reviewing, or refactoring Go code.
---

# Go

Correctness first, standard library first.

## Rules

- Propagate the existing request context through downstream work.
- Use `context.Background()` only at process bootstrap or intentionally detached workers.
- Prefer explicit code and constructor injection.
- Avoid package-level mutable state.
- Wrap errors with useful context; never silently ignore them.
- Match existing project patterns before adding helpers.
- Add tests for new behaviour.
- Avoid dependencies unless the standard library or installed packages fall short.
