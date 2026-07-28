Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=pr-writing
```

```bash
npx skills update pr-writing
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/pr-writing)

## What it does

`pr-writing` drafts pull request descriptions from local git history. It uses a pure Python helper and emits the Markdown PR body directly by default. Agents can opt into TOON with `--format toon` when they need branch context.

## When to reach for it

Type `/pr-writing`, or let the agent use it when a branch needs a PR description, an existing PR body needs refreshing from the diff, or another PR tool needs a reusable body draft.

## Prerequisites

A local git repository with the target branch available from the configured remote.

## Drafting

Run the helper with no args for tool context, or `draft --repo-dir .` for the Markdown PR body. Use `draft --repo-dir . --format toon` only when source, target, commits, changed files, counts, and the escaped Markdown body are needed as machine-readable context.

## PR body boundary

The standard shape is Description, Test Plan, Test Result, Code Risk, Related. Unknowns stay inside those sections instead of becoming new headings.

## It's working if

- The draft names real commits and files from the branch.
- The default draft output is Markdown.
- The PR body has exactly the standard top-level headings.
- `--format toon` still returns machine-readable context when needed.

## Where it fits

Use this before [bitbucket-helper](https://github.com/darknesskiller/skills/tree/main/skills/engineering/bitbucket-helper) when the branch needs a self-hosted Bitbucket PR. Use [git](https://github.com/darknesskiller/skills/tree/main/skills/engineering/git) first if branch history needs cleanup. The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
