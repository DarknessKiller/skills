---
name: creating-worktrees
description: "Create repo-local Git worktrees under .worktrees/."
---

# Creating Worktrees

## Steps

1. Find repo root: `git rev-parse --show-toplevel`.
2. Get branch or task name; ask once if missing.
3. Sanitize slug: replace `/`, spaces, unusual chars with `-`.
4. Add `.worktrees/` to `$(git rev-parse --git-path info/exclude)` if missing.
5. Create: existing branch → `git worktree add <path> <branch>`; new branch → `git worktree add -b <branch> <path>`.
6. `codegraph init <path>` only when source has `.codegraph/` or user asks. Else `CodeGraph: not applicable`.
7. Report path, branch, exclude status, CodeGraph result.

Completion: worktree exists, branch correct, exclusion recorded, CodeGraph reported.
