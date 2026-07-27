Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=ask-atlas
```

```bash
npx skills update ask-atlas
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas)

## What it does

`ask-atlas` is the router over this skill pack. It turns a vague goal into the next skill to run, without making you remember the whole map.

The defining constraint is that it only routes; it does not implement the work itself.

## When to reach for it

You invoke this by typing `/ask-atlas` — the agent won't reach for it on its own. Reach for it when you know the outcome you want but not the workflow to use.

## The map

The leading word is **flow**. `ask-atlas` separates user-invoked orchestration from model-invoked discipline, then points you at the smallest flow that fits: implement, PR, worktree, parallel agents, personal memory, or codebase design.

## It's working if

- The agent names the right source of truth before acting.
- The output uses the skill's leading words consistently.
- The next action is smaller and clearer than the original request.

## Where it fits

This is the router over the whole set. Use it before [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement) when the next step is unclear. The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
