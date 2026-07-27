---
name: bitbucket-helper
description: Use when drafting, creating, getting, reading, or updating pull requests for self-hosted Bitbucket Server/Data Center repositories; when inferring Bitbucket project/repo from local git remotes such as /scm/PROJECT/repo.git or /projects/PROJECT/repos/repo; or when avoiding Bitbucket Cloud-only tools for self-hosted Bitbucket.
---

# Bitbucket Helper

Use this for self-hosted Bitbucket Server/Data Center PR work. Avoid Bitbucket Cloud-only APIs.

Prefer the bundled helper CLI for repeatable repo detection, Markdown drafting, and REST calls:

```bash
bin/bitbucket-helper
```

Use `bitbucket-helper` from `PATH` when available; otherwise run the bundled `bin/bitbucket-helper` in this skill folder.

## Workflow

1. Inspect local branch, target branch, commits, and diff before drafting.
2. Infer Bitbucket identity from `git remote -v`:
   - clone URL: `https://host/scm/PROJECT/repo.git`
   - browser URL: `https://host/projects/PROJECT/repos/repo`
3. Draft a PR body with exactly these top-level sections: Description, Test Plan, Test Result, Code Risk, Related.
4. Ask before creating or updating live PRs unless the user explicitly requested it.
5. Use Bitbucket Server REST API:
   - create: `POST {base}/rest/api/1.0/projects/{PROJECT}/repos/{repo}/pull-requests`
   - read: `GET {base}/rest/api/1.0/projects/{PROJECT}/repos/{repo}/pull-requests/{id}`
   - update: `PUT {base}/rest/api/1.0/projects/{PROJECT}/repos/{repo}/pull-requests/{id}` after reading the current PR version
6. For updates, send a minimal payload only: title, description, version, fromRef, toRef, and reviewer user names. Do not echo read-only fields such as `author`.

## Auth

Use the repo's existing self-hosted Bitbucket environment variables:

```bash
BB_USER
BB_PASSWORD
```

Use raw `BB_PASSWORD`, not an escaped variant. Never print or store tokens.

## CLI usage

Draft only:

```bash
bitbucket-helper draft --repo-dir .
```

Create a PR:

```bash
bitbucket-helper create --repo-dir . --target main --title "PROJ-123: concise title"
```

Read an existing PR:

```bash
bitbucket-helper get 123 --repo-dir .
```

Update an existing PR:

```bash
bitbucket-helper update 123 --repo-dir . --title "PROJ-123: concise title"
```

Refresh an existing PR description from the local branch:

```bash
bitbucket-helper update 123 --repo-dir . --refresh-description
```

## PR body shape

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

Be explicit about uncertainty. If target branch is guessed, state it before creating. Do not add extra top-level headings.
