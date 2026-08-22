---
name: bitbucket-helper
description: "Bitbucket PR operations: create, read, update, approve, diff. Auto-detects Server vs Cloud."
---

# Bitbucket Helper

Auto-detects from git remote: `bitbucket.org` → Cloud, else → Server.

```bash
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py
```

## Steps

1. Run helper with no args to detect type and PR context. Done when source, target, project, repo known.
2. IF PR body needed: use `/pr-writing` first. Done when body has Description, Test Plan, Test Result, Code Risk, Links.
3. Before live create/update/approve: confirm unless user explicitly asked.
4. For review: start with `review-context`, then targeted `diff --path` or `file`.
5. For updates: read PR version first, send only mutable fields (title, description, version, fromRef, toRef, reviewers). Never send `author`.

Completion: operation scoped to detected repo and PR, mutations authorized.

## Commands

```bash
# Read
get <pr_id> --repo-dir . [--body]
review-context <pr_id> --repo-dir .
files <pr_id> --repo-dir .
diff <pr_id> --repo-dir . --path <path>
file <path> --repo-dir . --at refs/heads/main
commits <pr_id> --repo-dir .
commit <sha> --repo-dir .

# Mutate
approve <pr_id> --repo-dir .
create --repo-dir . --target main --title "PROJ-123: title" [--draft]
update <pr_id> --repo-dir . [--refresh-description | --ready]
```

Flags: `--full`, `--body`, `--format text`, `--cloud`, `--base-url`.

## Auth

`BB_USER` / `BB_PASSWORD` or scoped: `BB_CLOUD_*` / `BB_SERVER_*` (scoped win). Cloud: App Password with Repositories and Pull Requests Read/Write.

## Detection

| Remote | Type |
|---|---|
| `bitbucket.org` in URL | Cloud |
| `host/scm/` or `host/projects/` | Server |

Override: `--cloud` or `--base-url`.
