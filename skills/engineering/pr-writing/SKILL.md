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

1. **Gather context.**
   - Run the helper with no args, or inspect the branch directly.
   - IF context is missing: state what is missing.

   **Done when:**
   - [ ] Source branch is known.
   - [ ] Target branch is known.
   - [ ] Commits are listed.
   - [ ] Changed files are listed.

2. **Draft the body.**
   - Detect the repository profile or accept an explicit `--profile`.
   - Include: Description, Test Plan, Test Result, Code Risk, Links.
   - Add Screenshot only for the `frontend` profile.
   - Keep uncertainty inside sections. Do not add extra headings.

   **Done when:**
   - [ ] Every applicable section is present.
   - [ ] The body is reviewable without pretending tests or risks are known.

3. **Check claims.**
   - Every claim must be supported by local context.
   - Unknown tests or risks are labeled, not invented.

   **Done when:**
   - [ ] The body has exactly the applicable headings.
   - [ ] The profile matches the repository or explicit override.
   - [ ] Unknown tests or risks are labeled.

## Commands

```bash
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir .
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir . --target main
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir . --format toon
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir . --profile frontend
```

- `draft` outputs the Markdown body directly.
- `--format toon` gives source, target, commit, file, and count context without the multiline body.
- Invalid flags fail before git access with structured stdout and exit code `2`.

## Profiles

| Detection signal | Profile |
|---|---|
| `package.json` has React, Next, Vue, Nuxt, Svelte, Angular, Astro, Preact, or React Native | `frontend` |
| `pubspec.yaml` present | `flutter` |
| `go.mod` present | `go` |
| None of the above | `generic` |

Use `--profile generic`, `--profile frontend`, `--profile dart`, or `--profile go` to override.

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
