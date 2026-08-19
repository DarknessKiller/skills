Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=implement
```

```bash
npx skills update implement
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement)

## What it does

`implement` builds scoped work from a spec, issue, or the current conversation. It owns the path from contract to verified diff.

The defining constraint is feedback: pin the contract, build one slice at a time, use tests where a seam exists, then review before finishing. If the plan is soft, use bounded `/grilling` first.

## When to reach for it

You invoke this by typing `/implement` — the agent won't reach for it on its own. Reach for it when you want a concrete change built, not just investigated or planned.

## Feedback first

The leading word is **seam**. The skill finds the seam where behaviour can be proved cheaply, drives [tdd](https://github.com/darknesskiller/skills/tree/main/skills/engineering/tdd) there, and closes with [code-review](https://github.com/darknesskiller/skills/tree/main/skills/engineering/code-review).

## It's working if

- The agent names the right source of truth before acting.
- The output uses the skill's leading words consistently.
- The next action is smaller and clearer than the original request.
- Completion criteria, checks, and remaining risks are explicit.

## Where it fits

This is the main build step in the Atlas flow. If it needs a PR after implementation, use [bitbucket-helper](https://github.com/darknesskiller/skills/tree/main/skills/engineering/bitbucket-helper). The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
