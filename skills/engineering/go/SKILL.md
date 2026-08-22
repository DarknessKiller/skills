---
name: go
description: "Go standards: context propagation, explicit deps, stdlib-first, wrapped errors. Use when writing or reviewing Go."
---

# Go

Correctness first. Standard library first.

## Rules

1. Propagate the existing request context through downstream work.
2. Use `context.Background()` only at process bootstrap or intentionally detached workers.
3. Prefer explicit code and constructor injection.
4. Avoid package-level mutable state.
5. Wrap errors with useful context. Never silently ignore them.
6. Match existing project patterns before adding helpers.
7. Add tests for new behaviour.
8. Avoid dependencies unless the standard library or installed packages fall short.

**Done when:**
- [ ] Request context is preserved.
- [ ] Dependencies are explicit.
- [ ] Errors are wrapped with useful context.
- [ ] Local package patterns are followed.
- [ ] Narrowest relevant tests pass.
