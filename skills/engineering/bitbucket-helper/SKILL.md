---
name: bitbucket-helper
description: Use when creating, reading, or updating pull requests for self-hosted Bitbucket Server/Data Center; when inferring Bitbucket project/repo from /scm/PROJECT/repo.git or /projects/PROJECT/repos/repo remotes; or when avoiding Bitbucket Cloud-only tooling.
---

# Bitbucket Helper

Self-hosted Bitbucket Server/Data Center API work only. Draft PR bodies with `pr-writing`; use this pure Python helper for PRs, changed files, diffs, file contents, and commits. All stdout is TOON.

```bash
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py
```

## Process

1. Run the helper with no args in the repo. Done when source branch, target branch, project, repo, and helper path are known or the missing piece is explicit.
2. If the PR body needs drafting, use `pr-writing` first. Done when the body has Description, Test Plan, Test Result, Code Risk, Related.
3. Before live create/update, confirm unless the user explicitly asked for the mutation. Done when intent is clear.
4. For review context, prefer compact reads in this order: `files`, targeted `diff --path`, `file`, then `commits`. Done when the next API call is scoped by PR id, path, ref, or commit id instead of fetching full payloads.
5. For updates, read the PR version first and send only mutable fields: title, description, version, fromRef, toRef, reviewer user names. Done when read-only fields such as `author` are absent from the payload.

## Commands

```bash
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py get <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py get <pr_id> --repo-dir . --body
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py files <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py diff <pr_id> --repo-dir . --path <path>
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py file <path> --repo-dir . --at refs/heads/main
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py commits <pr_id> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py commit <sha> --repo-dir .
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py create --repo-dir . --target main --title "PROJ-123: concise title"
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py update <pr_id> --repo-dir . --refresh-description
```

Use `--full` only when the compact TOON summary omits data you need.

## Auth

Live API calls use the existing self-hosted Bitbucket environment:

```bash
BB_USER
BB_PASSWORD
```

Use raw `BB_PASSWORD`. Never print or store credentials.

## Server REST shape

- create: `POST {base}/rest/api/1.0/projects/{PROJECT}/repos/{repo}/pull-requests`
- read: `GET {base}/rest/api/1.0/projects/{PROJECT}/repos/{repo}/pull-requests/{id}`
- update: `PUT {base}/rest/api/1.0/projects/{PROJECT}/repos/{repo}/pull-requests/{id}` after reading the current PR version

Remote identity patterns:

- clone URL: `https://host/scm/PROJECT/repo.git`
- browser URL: `https://host/projects/PROJECT/repos/repo`

Do not use Bitbucket Cloud APIs.
