Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=pr-writing
```

```bash
npx skills update pr-writing
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/pr-writing)

## What it does

`pr-writing` drafts pull request descriptions from local git history. It uses a pure Python helper and emits TOON so agents can read the branch context and copy the Markdown body from `pr.body`.

## When to reach for it

Type `/pr-writing`, or let the agent use it when a branch needs a PR description, an existing PR body needs refreshing from the diff, or another PR tool needs a reusable body draft.

## Prerequisites

A local git repository with the target branch available from the configured remote.

## AXI-shaped drafting

Run the helper with no args for content-first tool context, or `draft` for a TOON document containing source, target, commits, changed files, counts, and the escaped Markdown PR body.

## PR body boundary

The standard shape is Description, Test Plan, Test Result, Code Risk, Related. Unknowns stay inside those sections instead of becoming new headings.

## It's working if

- The draft names real commits and files from the branch.
- The output is TOON.
- The PR body has exactly the standard top-level headings.

## Where it fits

Use this before [bitbucket-helper](https://github.com/darknesskiller/skills/tree/main/skills/engineering/bitbucket-helper) when the branch needs a self-hosted Bitbucket PR. Use [git](https://github.com/darknesskiller/skills/tree/main/skills/engineering/git) first if branch history needs cleanup. The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
