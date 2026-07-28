Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=bitbucket-helper
```

```bash
npx skills update bitbucket-helper
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/bitbucket-helper)

## What it does

`bitbucket-helper` reads, creates, updates, and approves pull requests for self-hosted Bitbucket Server/Data Center. It also reads PR review context, changed files, targeted diffs, repository file contents, and commits. It uses a pure Python helper, infers Server project/repo from git remotes, and emits TOON by default.

It is not for Bitbucket Cloud, and it no longer owns PR body writing; use `pr-writing` for that.

## When to reach for it

Type `/bitbucket-helper`, or let the agent use it when a branch needs a self-hosted Bitbucket PR mutation, an existing PR needs reading/updating, or Cloud-only Bitbucket tooling would be wrong.

## Prerequisites

Live create/update/get/approve calls need:

```bash
BB_USER
BB_PASSWORD
```

## AXI-shaped Bitbucket API work

Run the helper with no args first. It prints the Python helper path, one-line purpose, inferred repo identity, branch context, and next useful commands as TOON.

Default commands return compact TOON summaries. `get <pr_id>` is metadata-only; add `--body` for the PR description preview. For review context, start with `review-context <pr_id>` to fetch PR metadata, changed files, and commits in one command, then use `diff <pr_id> --path <path>` or `file <path> --at <ref>` as needed. Use `approve <pr_id>` only after the user clearly asked for approval. Use `--full` only when the complete Bitbucket API response is necessary.

## PR body boundary

Draft or refresh the description with [pr-writing](https://github.com/darknesskiller/skills/tree/main/skills/engineering/pr-writing). This skill only moves that body through the Bitbucket Server REST API.

## It's working if

- The agent identifies the Server/Data Center repo before mutating anything.
- Live updates and approvals read the current PR version first.
- Review reads start with one compact `review-context` call, then stay scoped to the PR id, path, ref, or commit id.
- Output is TOON.
- Full API data appears only when `--full` is requested.

## Where it fits

Use this after [pr-writing](https://github.com/darknesskiller/skills/tree/main/skills/engineering/pr-writing) when a branch is ready for a Bitbucket PR. Use [git](https://github.com/darknesskiller/skills/tree/main/skills/engineering/git) first if branch history needs cleanup. The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
