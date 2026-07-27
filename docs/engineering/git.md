Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=git
```

```bash
npx skills update git
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/git)

## What it does

`git` keeps Git history boring. It standardizes small diffs, Conventional Commits, and non-GPG commits for this setup.

The defining constraint is reviewability: history should make the change easier to inspect, not prettier at the cost of user work.

## When to reach for it

Type `/git`, or let the agent reach for it automatically when staging, committing, naming branches, or preparing a diff.

## Boring history

The leading word is **reviewable**. Inspect status first, keep subjects specific, and never overwrite user work just to tidy a branch.

## It's working if

- The agent names the right source of truth before acting.
- The output uses the skill's leading words consistently.
- The next action is smaller and clearer than the original request.

## Where it fits

This supports [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement), [creating-worktrees](https://github.com/darknesskiller/skills/tree/main/skills/engineering/creating-worktrees), and [bitbucket-helper](https://github.com/darknesskiller/skills/tree/main/skills/engineering/bitbucket-helper). The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
