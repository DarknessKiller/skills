---
name: bitbucket-helper
description: "Bitbucket PR operations: create, read, update, approve, diff. Auto-detects Server vs Cloud from remote."
---

# Bitbucket Helper

PR operations for Bitbucket Server/Data Center and Cloud. Auto-detects from git remote: `bitbucket.org` → Cloud, everything else → Server. Draft PR bodies with `/pr-writing`. Use this for PRs, changed files, diffs, file contents, commits, and approvals.

```bash
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py
```

## Process

1. Run the helper with no args in the repo. Done when source branch, target branch, project, repo, and helper path are known or the missing piece is explicit.
2. IF the PR body needs drafting: use `/pr-writing` first. Done when body has Description, Test Plan, Test Result, Code Risk, Links (plus Screenshot for frontend).
3. Before live create/update/approve: confirm unless the user explicitly asked. Done when intent is clear.
4. For review context: start with `review-context`, then targeted `diff --path` or `file` only as needed. Done when the next API call is scoped by PR id, path, ref, or commit id.
5. For updates: read the PR version first, send only mutable fields (title, description, version, fromRef, toRef, reviewer user names). Read-only fields like `author` must be absent.

Completion: the operation is scoped to the detected repository and PR/ref/path, mutations are authorized, and the response or blocking prerequisite is reported.

## Commands

```bash
# Read
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py get <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py get <pr_id> --repo-dir . --body
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py review-context <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py files <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py diff <pr_id> --repo-dir . --path <path>
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py file <path> --repo-dir . --at refs/heads/main
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py commits <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py commit <sha> --repo-dir .

# Mutate
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py approve <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py create --repo-dir . --target main --title "PROJ-123: concise title"
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py create --repo-dir . --target main --title "PROJ-123: WIP" --draft
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py update <pr_id> --repo-dir . --refresh-description
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py update <pr_id> --repo-dir . --ready
```

Flags: `--full` for complete API results. `--body` for description preview. `--format text` for raw content. `create --draft` for a draft PR. `update --ready` to mark ready for review. `-v`/`-V`/`--version` print version. Invalid flags fail with exit code `2`.

## Auth

One pair for all installations: `BB_USER` / `BB_PASSWORD`. Or scoped: `BB_CLOUD_USER` / `BB_CLOUD_PASSWORD` / `BB_SERVER_USER` / `BB_SERVER_PASSWORD` (scoped win, generic is fallback). Cloud: App Password with Repositories and Pull Requests Read/Write. Server: HTTP password or PAT.

## Auto-detection

| Remote URL | Type |
|---|---|
| `git@bitbucket.org:workspace/repo.git` | Cloud |
| `https://bitbucket.org/workspace/repo.git` | Cloud |
| `git@host:scm/PROJECT/repo.git` | Server |
| `https://host/scm/PROJECT/repo.git` | Server |
| `https://host/projects/PROJECT/repos/repo` | Server |

Override with `--cloud` or `--base-url`.
