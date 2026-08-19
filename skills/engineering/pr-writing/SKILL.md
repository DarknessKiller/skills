---
name: pr-writing
description: Use when drafting or refreshing pull request descriptions from local git history; when a PR body needs the standard Description, Test Plan, Test Result, Code Risk, Related shape; or when another skill needs a reusable PR-writing helper.
---

# PR Writing

Draft PR descriptions from local commits and changed files. The helper is pure Python, emits Markdown by default, and uses compact TOON for metadata. `--help` remains human-readable; `--version` is a bare fast-path.

```bash
python3 skills/engineering/pr-writing/scripts/pr_writer.py
```

## Process

1. Run the helper with no args or inspect the branch directly. Done when source, target, commits, and changed files are known or missing context is explicit.
2. Draft with exactly these top-level headings: Description, Test Plan, Test Result, Code Risk, Related. Done when every section is present.
3. Keep uncertainty inside the sections instead of adding headings. Done when the body is reviewable without pretending tests or risks are known.

Completion: the body has exactly the required headings, every claim is supported by local context, and unknown tests or risks are labeled rather than invented.

## Commands

```bash
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir .
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir . --target main
python3 skills/engineering/pr-writing/scripts/pr_writer.py draft --repo-dir . --format toon
```

`draft` outputs the Markdown body directly. Use `--format toon` when an agent needs source, target, commit, file, and count context without the multiline body. TOON includes explicit zero counts and hints when previews are capped. Invalid flags fail before git access with structured stdout and exit code `2`.

## PR body

```markdown
## Description
- What changed and why.

## Test Plan
- E2E: Planned/not applicable.
- Unit Tests: Planned/not applicable.

## Test Result
- E2E: Not run yet.
- Unit Tests: Not run yet.

## Code Risk
- Risk: Describe the main review/runtime risk.
- Rollback: Revert this PR.

## Related
- PROJ-123 or Not applicable.
```

Do not add extra top-level headings.
