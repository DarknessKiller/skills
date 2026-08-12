---
name: bitbucket-helper
description: Bitbucket pull requests — create, read, update, approve, diff. Auto-detects Server vs Cloud from remote.
---

# Bitbucket Helper

PR operations for Bitbucket Server/Data Center and Cloud. The helper auto-detects the type from the git remote URL (`bitbucket.org` → Cloud, everything else → Server). Default metadata is compact TOON with previews for large content, explicit empty states, and actionable next-step hints. Draft PR bodies with `pr-writing`; use this for PRs, changed files, diffs, file contents, commits, and approvals.

```bash
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py
```

## Process

1. Run the helper with no args in the repo. **Done** when source branch, target branch, project, repo, and helper path are known or the missing piece is explicit.
2. If the PR body needs drafting, use `pr-writing` first. **Done** when the body has Description, Test Plan, Test Result, Code Risk, Related.
3. Before live create/update/approve, confirm unless the user explicitly asked for the mutation. **Done** when intent is clear.
4. For review context, start with `review-context`; then use targeted `diff --path` or `file` only as needed. **Done** when the next API call is scoped by PR id, path, ref, or commit id.
5. For updates, read the PR version first and send only mutable fields: title, description, version, fromRef, toRef, reviewer user names. **Done** when read-only fields such as `author` are absent from the payload.

## Commands

```bash
# PR operations
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py get <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py get <pr_id> --repo-dir . --body
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py review-context <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py approve <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py files <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py diff <pr_id> --repo-dir . --path <path>
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py file <path> --repo-dir . --at refs/heads/main
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py commits <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py commit <sha> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py create --repo-dir . --target main --title "PROJ-123: concise title"
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py update <pr_id> --repo-dir . --refresh-description

`--full` for complete API results. `--body` for plain description preview. `--format text` for raw diff/file content. `-v`, `-V`, and `--version` print the bare helper version. Invalid flags fail before API access with structured stdout and exit code `2`.

## Auth

Use one credential pair for every Bitbucket installation:

```bash
BB_USER
BB_PASSWORD
```

Or keep Cloud and self-hosted credentials separate:

```bash
BB_CLOUD_USER
BB_CLOUD_PASSWORD
BB_SERVER_USER
BB_SERVER_PASSWORD
```

The scoped variables win for their detected installation type; the generic pair remains a fallback. For **Cloud**, use an App Password with `Repositories: Read/Write` and `Pull Requests: Read/Write`. For **Server**, use an HTTP password or personal access token.

## Auto-detection

| Remote URL | Type |
|---|---|
| `git@bitbucket.org:workspace/repo.git` | Cloud |
| `https://bitbucket.org/workspace/repo.git` | Cloud |
| `git@host:scm/PROJECT/repo.git` | Server |
| `https://host/scm/PROJECT/repo.git` | Server |
| `https://host/projects/PROJECT/repos/repo` | Server |

Override with `--cloud` or `--base-url` (auto-detected if URL contains `bitbucket.org`).
