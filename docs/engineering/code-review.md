Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=code-review
```

```bash
npx skills update code-review
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/code-review)

## What it does

`code-review` inspects a diff against a fixed point. It reports Standards and Spec separately so convention failures do not hide requirement failures, and vice versa.

The defining constraint is separation: two review axes, no merged ranking.

## When to reach for it

Type `/code-review`, or let the agent reach for it automatically when reviewing a branch, PR, or work-in-progress diff. Reach for it whenever a change should be checked before commit or PR.

## Two axes

The leading phrase is **Standards and Spec**. Standards checks repo rules and design smells; Spec checks the originating request. Keeping them apart makes review findings easier to act on.

## It's working if

- The agent names the right source of truth before acting.
- The output uses the skill's leading words consistently.
- The next action is smaller and clearer than the original request.

## Where it fits

This is the review step inside [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement) and a standalone PR review tool. It uses [codebase-design](https://github.com/darknesskiller/skills/tree/main/skills/engineering/codebase-design) vocabulary when judging boundaries. The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
