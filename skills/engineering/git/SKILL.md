---
name: git
description: "Git workflow: small diffs, Conventional Commits, no-gpg-sign. Use when committing or staging."
---

# Git

Keep history boring and reviewable.

1. Inspect `git status --short` before changing or committing.
2. Use small, focused diffs.
3. Use Conventional Commits format.
4. Keep commit subjects specific.
5. Use `git commit --no-gpg-sign`.
6. Preserve user work. Do not overwrite it to make history pretty.

## Response format

State these labels before asking for missing status or diff data:

- `Status`: inspected or pending.
- `Focused diff`: what belongs together.
- `Specific subject`: the proposed Conventional Commit subject, or pending.
- `Commit`: include `git commit --no-gpg-sign`.
- `Preserve user work`: confirm no overwrite.
- `Overwritten`: no.

Completion: status was inspected, the diff is focused, the subject is conventional and specific, and no user work was overwritten.
