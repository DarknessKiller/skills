---
name: codebase-design
description: Shared discipline for designing deep modules and clean seams. Use when code needs architecture pressure, boundary decisions, refactoring, or review for misplaced behaviour.
---

# Codebase Design

Prefer deep modules: useful behaviour behind a small interface at a clean seam.

## Default flow

Handler → Service → Repository

- Handlers translate protocol concerns and stay thin.
- Services own business rules and orchestration.
- Repositories own persistence only.
- Adapters isolate external systems.

## Rules

- Preserve existing boundaries unless the change is explicitly about moving them.
- Put a rule where all callers naturally pass through it.
- Prefer explicit request flow over hidden magic.
- Delete speculative layers, single-use interfaces, and configuration for values that never vary.
- Name domain concepts with words from `CONTEXT.md` when the repo has one.

## Design check

A good seam is easy to test through, hides implementation detail, and reduces the number of files future changes must touch.
