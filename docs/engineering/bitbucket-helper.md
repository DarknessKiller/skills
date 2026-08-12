Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=bitbucket-helper
```

```bash
npx skills update bitbucket-helper
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/bitbucket-helper)

## What it does

`bitbucket-helper` reads, creates, updates, and approves pull requests for Bitbucket Server/Data Center and Cloud. It reads PR review context, changed files, targeted diffs, repository file contents, and commits. It uses a pure Python helper, infers the installation type and project/repo from git remotes, and emits compact TOON metadata by default.

## When to reach for it

Type `/bitbucket-helper`, or let the agent use it when a branch needs a Bitbucket PR mutation, an existing PR needs reading/updating, or review context is needed.

## Prerequisites

Live create/update/get/approve calls need either one shared pair:

```bash
BB_USER
BB_PASSWORD
```

or separate credentials for multiple installations:

```bash
BB_CLOUD_USER
BB_CLOUD_PASSWORD
BB_SERVER_USER
BB_SERVER_PASSWORD
```

Scoped credentials are selected from the detected installation type and override the shared pair.

## AXI-shaped Bitbucket API work

Run the helper with `--help` for clean command documentation. Run it with no args for tool context: it prints the Python helper path, one-line purpose, inferred repo identity, branch context, and next useful commands as TOON.

Default commands return compact TOON metadata. `get <pr_id>` is metadata-only; add `--body` to fetch a plain Markdown description preview, adjusting `--limit-chars` when needed. `diff` and `file` return size-aware previews by default; add `--format text` or `--full` for complete content. Invalid flags fail before API access with structured stdout and exit code `2`; `-v`, `-V`, and `--version` return the bare helper version. For review context, start with `review-context <pr_id>` to fetch PR metadata, changed files, and commits in one command, then use `diff <pr_id> --path <path> --format text` or `file <path> --at <ref> --format text` as needed. Use `approve <pr_id>` only after the user clearly asked for approval. Use `--full` only when the complete Bitbucket API response is necessary.

## PR body boundary

Draft or refresh the description with [pr-writing](https://github.com/darknesskiller/skills/tree/main/skills/engineering/pr-writing). This skill only moves that body through the Bitbucket REST API.

## It's working if

- The agent identifies the Bitbucket repo before mutating anything.
- Live updates and approvals read the current PR version first.
- Review reads start with one compact `review-context` call, then stay scoped to the PR id, path, ref, or commit id.
- Metadata results are compact TOON; `--help` and explicit content fetches are human-readable text.
- Full API data appears only when `--full` is requested.

## Where it fits

Use this after [pr-writing](https://github.com/darknesskiller/skills/tree/main/skills/engineering/pr-writing) when a branch is ready for a Bitbucket PR. Use [git](https://github.com/darknesskiller/skills/tree/main/skills/engineering/git) first if branch history needs cleanup. The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
