---
name: creating-worktrees
description: "Create repo-local Git worktrees under .worktrees/. Use when the user asks for a worktree or isolated workspace."
---

# Creating Worktrees

Create isolated work under the repo root. Do not use a global scratch folder.

## Rules

- Worktree parent: `.worktrees/` at `git rev-parse --show-toplevel`.
- Worktree path: `<branch-or-task-slug>-<YYYYMMDD-HHMMSS>`.
- Ignore rule: add `.worktrees/` to local Git exclude, not shared `.gitignore`.
- Never create a nested worktree from inside an existing linked worktree.
- Never force checkout a branch already checked out elsewhere.

## Workflow

1. Find the repo root: `git rev-parse --show-toplevel`.
2. Get the branch or task name. Ask once if missing.
3. Sanitize the slug: replace `/`, spaces, and unusual characters with `-`.
4. Add `.worktrees/` to `$(git rev-parse --git-path info/exclude)` if missing.
5. Create the worktree:
   - IF the branch exists: `git worktree add <path> <branch>`
   - IF the branch is new: `git worktree add -b <branch> <path>`
6. IF the source repo has `.codegraph/` or the user explicitly asks: run `codegraph init <path>`.
7. Report path, branch, local exclude change, and CodeGraph result.

**Done when:**
- [ ] The worktree exists at the repository-local path.
- [ ] The branch is correct.
- [ ] Local exclusion is recorded.
- [ ] CodeGraph status is reported or "not applicable" is stated.

## Stop conditions

Stop if:
- The directory is not a git repo.
- The branch name is missing.
- Local exclude cannot be written.
- `git worktree add` fails.
