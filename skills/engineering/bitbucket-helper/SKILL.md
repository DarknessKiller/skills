---
name: bitbucket-helper
description: "Bitbucket PR operations: create, read, update, approve, diff. Auto-detects Server vs Cloud from remote."
---

# Bitbucket Helper

PR operations for Bitbucket Server/Data Center and Cloud. The helper auto-detects the type from the git remote URL.

- `bitbucket.org` in remote → Cloud.
- Anything else in remote → Server.

Draft PR bodies with `/pr-writing`. Use this skill for PRs, changed files, diffs, file contents, commits, and approvals.

```bash
python3 skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py
```

## Process

1. **Gather context.**
   - Run the helper with no args in the repo.

   **Done when:**
   - [ ] Source branch is known.
   - [ ] Target branch is known.
   - [ ] Project is known.
   - [ ] Repo is known.
   - [ ] Helper path is known.
   - [ ] Or the missing piece is stated explicitly.

2. **Draft the PR body if needed.**
   - Use `/pr-writing` first.

   **Done when:**
   - [ ] Body has Description, Test Plan, Test Result, Code Risk, Links.
   - [ ] Screenshot is included for frontend work.

3. **Confirm mutations.**
   - Before live create, update, or approve: confirm with the user.
   - IF the user explicitly asked for the mutation: skip confirmation.

   **Done when:**
   - [ ] Intent is clear.

4. **Read review context.**
   - Start with `review-context`.
   - Use targeted `diff --path` or `file` only as needed.

   **Done when:**
   - [ ] The next API call is scoped by PR id, path, ref, or commit id.

5. **Update with mutable fields only.**
   - Read the PR version first.
   - Send only: title, description, version, fromRef, toRef, reviewer user names.
   - Do NOT send read-only fields like `author`.

   **Done when:**
   - [ ] Read-only fields are absent from the payload.

**Completion:**
- [ ] Operation is scoped to the detected repository and PR/ref/path.
- [ ] Mutations are authorized.
- [ ] Response or blocking prerequisite is reported.

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

Flags:
- `--full` for complete API results.
- `--body` for plain description preview.
- `--format text` for raw diff/file content.
- `create --draft` for a draft PR.
- `update --ready` to mark a draft ready for review.
- `-v`, `-V`, `--version` print the bare helper version.
- Invalid flags fail before API access with structured stdout and exit code `2`.

## Auth

Use one credential pair for every installation:

```bash
BB_USER
BB_PASSWORD
```

Or keep Cloud and Server separate:

```bash
BB_CLOUD_USER
BB_CLOUD_PASSWORD
BB_SERVER_USER
BB_SERVER_PASSWORD
```

Scoped variables win for their type. Generic pair is the fallback.

- **Cloud**: App Password with `Repositories: Read/Write` and `Pull Requests: Read/Write`.
- **Server**: HTTP password or personal access token.

## Auto-detection

| Remote URL | Type |
|---|---|
| `git@bitbucket.org:workspace/repo.git` | Cloud |
| `https://bitbucket.org/workspace/repo.git` | Cloud |
| `git@host:scm/PROJECT/repo.git` | Server |
| `https://host/scm/PROJECT/repo.git` | Server |
| `https://host/projects/PROJECT/repos/repo` | Server |

Override with `--cloud` or `--base-url`.
