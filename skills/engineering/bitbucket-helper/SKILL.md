---
name: bitbucket-helper
description: Bitbucket pull requests — create, read, update, approve, diff; add SSH keys via agent. Auto-detects Server vs Cloud from remote.
---

# Bitbucket Helper

PR operations for Bitbucket Server/Data Center and Cloud. The helper auto-detects the type from the git remote URL (`bitbucket.org` → Cloud, everything else → Server). Draft PR bodies with `pr-writing`; use this for PRs, changed files, diffs, file contents, commits, approvals, and SSH key management.

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

# SSH key — reads from agent, file, or inline
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py ssh-key --repo-dir . --agent
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py ssh-key --repo-dir . --agent --agent-index 1 --label "work-key"
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py ssh-key --repo-dir . --key-file ~/.ssh/id_ed25519.pub
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py ssh-key --repo-dir . --key "ssh-ed25519 AAAA..."
```

`--full` for complete API results. `--body` for plain description preview. `--format text` for raw diff/file content.

## Auth

`BB_USER` and `BB_PASSWORD` env vars. For **Cloud**, generate an [App Password](https://bitbucket.org/account/settings/app-passwords/) with `Repositories: Read/Write` and `Pull Requests: Read/Write`. For **Server**, use your HTTP password or personal access token.

## SSH key

The `ssh-key` command adds public keys to Bitbucket:

| Flag | Source |
|------|--------|
| `--agent` | SSH agent (Bitwarden Desktop: Settings → SSH Agent) |
| `--key-file` | Public key file on disk |
| `--key` | Inline key text |

`--agent` reads from the running SSH agent via `ssh-add -L`. Keys must be loaded in the agent before running. Cloud keys become **deploy keys**; Server keys go to the user's SSH keys.

## Auto-detection

| Remote URL | Type |
|---|---|
| `git@bitbucket.org:workspace/repo.git` | Cloud |
| `https://bitbucket.org/workspace/repo.git` | Cloud |
| `git@host:scm/PROJECT/repo.git` | Server |
| `https://host/scm/PROJECT/repo.git` | Server |
| `https://host/projects/PROJECT/repos/repo` | Server |

Override with `--cloud` or `--base-url` (auto-detected if URL contains `bitbucket.org`).
