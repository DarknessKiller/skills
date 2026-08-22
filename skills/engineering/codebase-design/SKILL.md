---
name: codebase-design
description: "Design deep modules and clean seams. Use for architecture pressure, boundary decisions, or refactoring."
---

# Codebase Design

Prefer deep modules: useful behaviour behind a small interface at a clean seam.

## Default flow

Handler → Service → Repository

- Handlers translate protocol concerns. Stay thin.
- Services own business rules and orchestration.
- Repositories own persistence only.
- Adapters isolate external systems.

## Rules

1. Preserve existing boundaries unless the change is explicitly about moving them.
2. Put a rule where all callers naturally pass through it.
3. Prefer explicit request flow over hidden magic.
4. Delete speculative layers, single-use interfaces, and config for values that never vary.
5. Name domain concepts with words from `CONTEXT.md` when the repo has one.

## Design check

A good seam is:
- Easy to test through.
- Hides implementation detail.
- Reduces the number of files future changes must touch.

**Done when:**
- [ ] Each changed behavior has one natural owner.
- [ ] Callers cross the intended seam.
- [ ] The resulting boundary is easier to test than the old one.
