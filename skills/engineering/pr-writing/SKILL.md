---
name: pr-writing
description: "Draft PR descriptions from local git history."
---

# PR Writing

```bash
python3 skills/engineering/pr-writing/scripts/pr_writer.py
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
| `pubspec.yaml` | `flutter` |
| `go.mod` | `go` |
| None | `generic` |
