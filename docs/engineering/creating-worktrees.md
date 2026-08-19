Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=creating-worktrees
```

```bash
npx skills update creating-worktrees
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/creating-worktrees)

## What it does

`creating-worktrees` creates isolated repo-local Git worktrees. It uses `.worktrees/<slug>-<timestamp>` and keeps the ignore rule local unless you ask otherwise.

The defining constraint is locality: worktrees live inside the repo and do not require shared `.gitignore` churn.

## When to reach for it

Type `/creating-worktrees`, or let the agent reach for it automatically when you ask for a worktree, branch workspace, or isolated workspace.

## Repo-local isolation

The leading phrase is **repo-local**. The skill prevents nested worktrees, timestamps paths, and initializes CodeGraph only when the repo already uses it or you ask for it.

## It's working if

- The agent names the right source of truth before acting.
- The output uses the skill's leading words consistently.
- The next action is smaller and clearer than the original request.
- The path, branch, local exclusion, and applicable CodeGraph result are explicit.

## Where it fits

Use this before [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement) for risky work or parallel branches. Use [git](https://github.com/darknesskiller/skills/tree/main/skills/engineering/git) when you later commit from the worktree. The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
