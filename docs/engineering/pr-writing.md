Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=pr-writing
```

```bash
npx skills update pr-writing
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/pr-writing)

## What it does

`pr-writing` drafts pull request descriptions from local git history. It uses a pure Python helper, detects generic, frontend, Dart, or Go review profiles, and emits the Markdown PR body directly by default. Help uses standard CLI text, `--version` is a fast bare response, and agents can opt into TOON with `--format toon` for compact branch context.

## When to reach for it

Type `/pr-writing`, or let the agent use it when a branch needs a PR description, an existing PR body needs refreshing from the diff, or another PR tool needs a reusable body draft.

## Prerequisites

A local git repository with the target branch available from the configured remote.

## Drafting

Run the helper with `--help` for clean command documentation, with no args for tool context, or `draft --repo-dir .` for the Markdown PR body. Use `draft --repo-dir . --format toon` when only source, target, commits, changed files, and counts are needed as machine-readable context; it omits the body to avoid embedding multiline text.

## Profiles and body boundary

The standard shape is Description, Test Plan, Test Result, Code Risk, Links, Screenshot. Frontend profiles add build, lint, typecheck, component/E2E, responsive, accessibility, and visual validation prompts. The Dart profile adds `dart format`, `dart analyze`, and `dart test` guidance; Flutter uses the frontend profile. The Go profile adds `gofmt`, `go vet`, and `go test ./...` guidance. The detector recognizes JavaScript frameworks, Dart and Flutter from `pubspec.yaml`, and Go from `go.mod`. Unknowns stay inside those sections instead of becoming new headings.

## It's working if

- The draft names real commits and files from the branch.
- The default draft output is Markdown.
- The PR body has exactly the standard top-level headings.
- `--help` is readable CLI text without TOON table formatting.
- `--format toon` returns metadata without embedding the multiline Markdown body.
- Invalid flags return structured stdout and exit code `2` before git access.
- Unknown tests or risks remain explicit instead of being invented.
- The detected profile supplies relevant validation prompts without inventing test results.

## Where it fits

Use this before [bitbucket-helper](https://github.com/darknesskiller/skills/tree/main/skills/engineering/bitbucket-helper) when the branch needs a Bitbucket Server/Data Center or Cloud PR. Use [git](https://github.com/darknesskiller/skills/tree/main/skills/engineering/git) first if branch history needs cleanup. The full map lives in [ask-atlas](https://github.com/darknesskiller/skills/tree/main/skills/engineering/ask-atlas).
