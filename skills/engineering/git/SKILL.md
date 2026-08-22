---
name: git
description: "Git workflow: small diffs, Conventional Commits, no-gpg-sign. Use when committing or staging."
---

# Git

Keep history boring and reviewable.

## Rules

1. Inspect `git status --short` before changing or committing.
2. Use small, focused diffs.
3. Use Conventional Commits format.
4. Keep commit subjects specific.
5. Use `git commit --no-gpg-sign`.
6. Preserve user work. Do not overwrite it to make history pretty.

**Done when:**
- [ ] `git status --short` was inspected.
- [ ] The diff is focused on one concern.
- [ ] The subject follows Conventional Commits.
- [ ] The subject is specific.
- [ ] No user work was overwritten.
