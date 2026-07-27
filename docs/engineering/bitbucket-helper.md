Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=bitbucket-helper
```

```bash
npx skills update bitbucket-helper
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/bitbucket-helper)

## What it does

`bitbucket-helper` handles self-hosted Bitbucket Server/Data Center PR work. It infers project and repo identity from local git remotes, drafts reviewable PR descriptions, and uses the Server REST API.

The defining constraint is host type: it is for Bitbucket Server/Data Center, not Bitbucket Cloud.

## When to reach for it

Type `/bitbucket-helper`, or let the agent reach for it automatically when a task mentions self-hosted Bitbucket PRs. For GitHub or Bitbucket Cloud, use the repo's native tooling instead.

## Prerequisites

Requires `BB_USER` and `BB_PASSWORD` for live create/update calls. Drafting from local git history works without writing remote state.

## Server-first PRs

The leading phrase is **self-hosted**. The skill avoids Cloud-only APIs, keeps tokens out of output, and uses a fixed PR body shape: Description, Test Plan, Test Result, Code Risk, Related.

## It's working if

- The agent names the right source of truth before acting.
- The output uses the skill's leading words consistently.
- The next action is smaller and clearer than the original request.

## Where it fits

Use this after [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement) when the branch needs a Bitbucket PR. Use [git](https://github.com/darknesskiller/skills/tree/main/skills/engineering/git) first if the branch history still needs cleanup. The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
