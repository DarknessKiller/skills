---
name: pr-writing
description: "Draft PR descriptions from local git history. Standard shape: Description, Test Plan, Test Result, Code Risk, Links, Screenshot."
---

# PR Writing

Draft PR descriptions from local commits and changed files. The helper is pure Python, emits Markdown by default, and uses compact TOON for metadata.

```bash
python3 skills/engineering/pr-writing/scripts/pr_writer.py
```

## Process

1. Run the helper with no args or inspect the branch directly. Done when source, target, commits, and changed files are known or missing context is explicit.
2. Detect the repository profile or accept an explicit `--profile`. Draft with Description, Test Plan, Test Result, Code Risk, and Links — add Screenshot only for `frontend`. Keep uncertainty inside sections, not in extra headings.
3. Every claim must be supported by local context. Unknown tests or risks are labeled, not invented.

Completion: the body has exactly the applicable headings, the profile matches the repo or explicit override, and unknown items are labeled.

## Commands

```bash
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir .
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir . --target main
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir . --format toon
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir . --profile frontend
```

`draft` outputs Markdown directly. `--format toon` gives metadata without the body. Invalid flags fail before git access with exit code `2`.

## Profiles

| Detection signal | Profile |
|---|---|
| `package.json` has React, Next, Vue, Nuxt, Svelte, Angular, Astro, Preact, or React Native | `frontend` |
| `pubspec.yaml` present | `flutter` |
| `go.mod` present | `go` |
| None of the above | `generic` |

Override with `--profile generic|frontend|dart|go`.

## PR body template

```markdown
## Description
- What changed and why.

## Test Plan
<!-- Give reviewers executable manual or automated test steps. -->

## Test Result
<!-- Record tests, analysis, formatting, and visual validation results. -->

## Code Risk
<!-- Describe runtime risk, mitigation, and rollback. -->
- Risk: Describe the main runtime or review risk.
- Mitigation: Describe safeguards or monitoring.
- Rollback: Revert this PR.

## Links
<!-- Figma, Confluence, Documentation, or related tickets. -->

## Screenshot
<!-- Frontend only: add screenshots or Figma Design Validation output for UI changes. -->
```

Do not add extra top-level headings.
