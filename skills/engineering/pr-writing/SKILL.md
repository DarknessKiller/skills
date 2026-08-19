---
name: pr-writing
description: Use when drafting or refreshing pull request descriptions from local git history; when a PR body needs the standard Description, Test Plan, Test Result, Code Risk, Links, Screenshot shape; or when another skill needs a reusable PR-writing helper.
---

# PR Writing

Draft PR descriptions from local commits and changed files. The helper is pure Python, emits Markdown by default, and uses compact TOON for metadata. `--help` remains human-readable; `--version` is a bare fast-path.

```bash
python3 skills/engineering/pr-writing/scripts/pr_writer.py
```

## Process

1. Run the helper with no args or inspect the branch directly. Done when source, target, commits, and changed files are known or missing context is explicit.
2. Detect the repository profile or accept an explicit `--profile`; draft with Description, Test Plan, Test Result, Code Risk, and Links, adding Screenshot only for the `frontend` profile. Done when every applicable section is present.
3. Keep uncertainty inside the sections instead of adding headings. Done when the body is reviewable without pretending tests or risks are known.

Completion: the body has exactly the applicable headings, the profile matches the repository or explicit override, every claim is supported by local context, and unknown tests or risks are labeled rather than invented.

## Commands

```bash
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir .
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir . --target main
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir . --format toon
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir . --profile frontend
```

`draft` outputs the Markdown body directly. Use `--format toon` when an agent needs source, target, commit, file, and count context without the multiline body. TOON includes explicit zero counts and hints when previews are capped. Invalid flags fail before git access with structured stdout and exit code `2`.

## Profiles

The helper detects `frontend` when `package.json` includes common React, Next, Vue, Nuxt, Svelte, Angular, Astro, Preact, or React Native dependencies, detects Flutter from `pubspec.yaml`, uses the explicit `dart` profile for plain Dart, and detects Go from `go.mod`. It reports the detected framework or language in the template. Use `--profile generic`, `--profile frontend`, `--profile dart`, or `--profile go` when repository metadata is incomplete or a different review path is intended. Screenshot is emitted only for frontend work.

## PR body

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
