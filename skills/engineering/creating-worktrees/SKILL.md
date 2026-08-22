---
name: creating-worktrees
description: "Create repo-local Git worktrees under .worktrees/. Use when the user asks for a worktree or isolated workspace."
---

# Creating Worktrees

Create isolated work under the repo root, not a global scratch folder.

## Rules

- Worktree parent: `.worktrees/` at `git rev-parse --show-toplevel`.
- Worktree path: `<branch-or-task-slug>-<YYYYMMDD-HHMMSS>`.
- Ignore rule: add `.worktrees/` to local Git exclude, not shared `.gitignore`.
- Never create a nested worktree from inside an existing linked worktree.
- Never force checkout a branch already checked out elsewhere.

## Workflow

1. Find the repo root: `git rev-parse --show-toplevel`.
2. Get the branch or task name; ask once if missing.
3. Sanitize the slug: replace `/`, spaces, and unusual characters with `-`.
4. Add `.worktrees/` to `$(git rev-parse --git-path info/exclude)` if missing.
5. Create the worktree — existing branch: `git worktree add <path> <branch>`; new branch: `git worktree add -b <branch> <path>`.
6. Run `codegraph init <path>` only when the source repo has `.codegraph/` or the user explicitly asks.
7. Report path, branch, local exclude change, and CodeGraph result.

Completion: the worktree exists at the repository-local path, the branch is correct, local exclusion is recorded, and CodeGraph status is reported when applicable.

Stop if the directory is not a git repo, the branch name is missing, local exclude cannot be written, or `git worktree add` fails.
