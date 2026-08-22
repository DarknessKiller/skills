---
name: codebase-design
description: "Design deep modules and clean seams."
---

# Codebase Design

Prefer deep modules: useful behaviour behind a small interface at a clean seam.

## Default flow

Handler → Service → Repository. Handlers translate protocol concerns (thin). Services own business rules and orchestration. Repositories own persistence only. Adapters isolate external systems.

## Rules

1. Preserve existing boundaries unless the change is explicitly about moving them.
2. Put a rule where all callers naturally pass through it.
3. Prefer explicit request flow over hidden magic.
4. Delete speculative layers, single-use interfaces, and config for values that never vary.
5. Name domain concepts with words from `CONTEXT.md` when the repo has one.

Completion: each changed behavior has one natural owner, callers cross the intended seam, and the resulting boundary is easier to test than the old one.
