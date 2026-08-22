---
name: pr-writing
description: "Draft PR descriptions from local git history. Shape: Description, Test Plan, Test Result, Code Risk, Links."
---

# PR Writing

Draft PR descriptions from local commits and changed files.

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

## Template

```markdown
## Description
- What changed and why.

## Test Plan
<!-- Manual or automated test steps. -->

## Test Result
<!-- Tests, analysis, formatting results. -->

## Risk
- Risk: main runtime or review risk.
- Mitigation: safeguards or monitoring.
- Rollback: revert this PR.

## Links
<!-- Figma, Confluence, tickets. -->

## Screenshot
<!-- Frontend only. -->
```
