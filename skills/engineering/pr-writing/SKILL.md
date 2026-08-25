---
name: pr-writing
description: "Draft PR descriptions from local git history."
---

# PR Writing

The helper script lives at `scripts/pr_writer.py` relative to this skill's directory (the harness resolves it). Run it from the user's repo with the script's absolute or skill-relative path:

```bash
python3 <skill-dir>/scripts/pr_writer.py
```

## Steps

1. Run helper or inspect branch. Done when source, target, commits, changed files known.
2. Detect profile or accept `--profile`. Draft with Description, Test Plan, Test Result, Code Risk, Links. Add Screenshot only for `frontend`.
3. Every claim must be supported by local context. Unknowns labeled, not invented.

Completion: body has applicable headings, profile matches repo, unknowns labeled.

## Commands

```bash
draft --repo-dir . [--target main] [--format toon] [--profile frontend]
```

## Profiles

| Signal | Profile |
|---|---|
| React, Next, Vue, Nuxt, Svelte, Angular, Astro, Preact, React Native | `frontend` |
| Flutter `pubspec.yaml` | `frontend` |
| Dart `pubspec.yaml` | `dart` |
| `go.mod` | `go` |
| None | `generic` |
