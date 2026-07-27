#!/usr/bin/env python3
"""Draft, create, and update pull requests for Bitbucket Server/Data Center."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


PASSWORD_ENV = "BB_PASSWORD"
USER_ENV = "BB_USER"
BIN_ENV = "BITBUCKET_HELPER_BIN"
DESCRIPTION = "Draft, create, read, and update Bitbucket Server/Data Center pull requests"


@dataclass
class RepoInfo:
    base_url: str
    project: str
    repo: str


def run_git(repo_dir: str, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", repo_dir, *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def display_path(path: str) -> str:
    home = str(Path.home())
    if path == home:
        return "~"
    if path.startswith(home + os.sep):
        return "~" + path[len(home) :]
    return path


def quote_toon(value: object) -> str:
    text = "" if value is None else str(value)
    return json.dumps(text)


def print_lines(lines: list[str]) -> None:
    sys.stdout.write("\n".join(lines) + "\n")


def current_branch(repo_dir: str) -> str:
    return run_git(repo_dir, "branch", "--show-current")


def remote_url(repo_dir: str, remote: str) -> str:
    return run_git(repo_dir, "remote", "get-url", remote)


def infer_repo_info(url: str) -> RepoInfo:
    normalized = url.strip()
    if normalized.startswith("git@"):
        match = re.match(r"git@([^:]+):/?(.+)$", normalized)
        if not match:
            raise ValueError(f"unsupported ssh remote: {url}")
        normalized = f"https://{match.group(1)}/{match.group(2)}"

    parsed = urllib.parse.urlparse(normalized)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"unsupported remote URL: {url}")

    path = parsed.path.rstrip("/")
    scm_match = re.match(r"^/scm/([^/]+)/([^/]+?)(?:\.git)?$", path, re.IGNORECASE)
    browse_match = re.match(r"^/projects/([^/]+)/repos/([^/]+?)(?:/.*)?$", path, re.IGNORECASE)
    match = scm_match or browse_match
    if not match:
        raise ValueError(f"could not infer Bitbucket Server project/repo from {url}")

    base = f"{parsed.scheme}://{parsed.netloc}"
    return RepoInfo(base_url=base, project=match.group(1).upper(), repo=match.group(2))


def default_target_branch(repo_dir: str, remote: str) -> str:
    ref = run_git(repo_dir, "symbolic-ref", f"refs/remotes/{remote}/HEAD", check=False)
    if ref:
        return ref.rsplit("/", 1)[-1]
    for candidate in ("main", "master", "develop"):
        exists = run_git(repo_dir, "rev-parse", "--verify", f"{remote}/{candidate}", check=False)
        if exists:
            return candidate
    return "main"


def commits(repo_dir: str, remote: str, target: str, source: str) -> list[str]:
    out = run_git(repo_dir, "log", "--oneline", f"{remote}/{target}..{source}", check=False)
    return [line for line in out.splitlines() if line.strip()]


def changed_files(repo_dir: str, remote: str, target: str, source: str) -> list[str]:
    out = run_git(repo_dir, "diff", "--name-only", f"{remote}/{target}...{source}", check=False)
    return [line for line in out.splitlines() if line.strip()]


def jira_keys(*texts: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for text in texts:
        for key in re.findall(r"\b[A-Z][A-Z0-9]+-\d+\b", text):
            if key not in seen:
                seen.add(key)
                found.append(key)
    return found


def draft_description(repo_dir: str, remote: str, source: str, target: str) -> str:
    commit_lines = commits(repo_dir, remote, target, source)
    files = changed_files(repo_dir, remote, target, source)
    keys = jira_keys(source, "\n".join(commit_lines))

    changes = commit_lines[:12] or ["Describe the implementation changes."]
    file_sample = files[:20]

    lines = [
        "## Description",
        "- Describe what changed and why.",
        "",
        "- Key changes:",
    ]
    lines.extend(f"- {line}" for line in changes)
    if file_sample:
        lines.extend(["", "- Files touched:"])
        lines.extend(f"- `{path}`" for path in file_sample)
        if len(files) > len(file_sample):
            lines.append(f"- ...and {len(files) - len(file_sample)} more")
    lines.extend(
        [
            "",
            "## Test Plan",
            "- E2E: Planned/not applicable.",
            "- Ginkgo: Planned/not applicable.",
            "",
            "## Test Result",
            "- E2E: Not run yet.",
            "- Ginkgo: Not run yet.",
            "",
            "## Code Risk",
            "- Risk: Describe the main review/runtime risk.",
            "- Rollback: Revert this PR.",
            "",
            "## Related",
        ]
    )
    lines.extend(f"- {key}" for key in keys) if keys else lines.append("- Not applicable.")
    return "\n".join(lines) + "\n"


def home_view(repo_dir: str = ".", remote: str = "origin") -> None:
    bin_path = os.environ.get(BIN_ENV) or os.path.abspath(__file__)
    lines = [
        f"bin: {quote_toon(display_path(bin_path))}",
        f"description: {quote_toon(DESCRIPTION)}",
    ]
    try:
        source = current_branch(repo_dir)
        target = default_target_branch(repo_dir, remote)
        info = repo_info_from_args(
            argparse.Namespace(
                base_url=None,
                project=None,
                repo=None,
                repo_dir=repo_dir,
                remote=remote,
            )
        )
        lines.extend(
            [
                "repo:",
                f"  base_url: {quote_toon(info.base_url)}",
                f"  project: {quote_toon(info.project)}",
                f"  repo: {quote_toon(info.repo)}",
                "branch:",
                f"  source: {quote_toon(source or 'unknown')}",
                f"  target: {quote_toon(target)}",
            ]
        )
    except (SystemExit, ValueError):
        lines.append("repo: unknown")
    lines.extend(
        [
            "help[4]:",
            '  "Run `bitbucket-helper draft --repo-dir .` to draft a PR description"',
            '  "Run `bitbucket-helper create --repo-dir . --target main --title \\"...\\"` to create a PR"',
            '  "Run `bitbucket-helper get <pr_id> --repo-dir .` to read a PR"',
            '  "Add `--json` to create/get/update for raw Bitbucket API output"',
        ]
    )
    print_lines(lines)


def pr_branch(ref: dict) -> str:
    return str(ref.get("displayId") or ref.get("id", "")).removeprefix("refs/heads/")


def pr_links(pr: dict) -> str:
    links = pr.get("links", {})
    for link in links.get("self", []):
        href = link.get("href")
        if href:
            return href
    return ""


def print_pr_result(result: dict, action: str) -> None:
    if result.get("dryRun"):
        payload = result.get("payload", {})
        lines = [
            "dry_run:",
            f"  action: {quote_toon(action)}",
            f"  url: {quote_toon(result.get('url'))}",
            f"  title: {quote_toon(payload.get('title'))}",
            f"  from: {quote_toon(payload.get('fromRef', {}).get('id'))}",
            f"  to: {quote_toon(payload.get('toRef', {}).get('id'))}",
            f"  reviewers: {len(payload.get('reviewers', []))}",
            'help[1]: "Re-run without `--dry-run` to call Bitbucket Server"',
        ]
        print_lines(lines)
        return

    lines = [
        "pull_request:",
        f"  action: {quote_toon(action)}",
        f"  id: {result.get('id', result.get('number', ''))}",
        f"  title: {quote_toon(result.get('title'))}",
        f"  state: {quote_toon(result.get('state'))}",
        f"  version: {result.get('version', '')}",
        f"  from: {quote_toon(pr_branch(result.get('fromRef', {})))}",
        f"  to: {quote_toon(pr_branch(result.get('toRef', {})))}",
        f"  url: {quote_toon(pr_links(result))}",
    ]
    print_lines(lines)


def token_from_env() -> tuple[str, str] | tuple[None, None]:
    token = os.environ.get(PASSWORD_ENV)
    if token:
        return PASSWORD_ENV, token
    return None, None


def api_request(method: str, url: str, payload: dict | None, auth: str, user: str | None) -> dict:
    env_name, token = token_from_env()
    if not token:
        raise SystemExit(f"missing token; set {PASSWORD_ENV}")

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if auth == "basic":
        user = user or os.environ.get(USER_ENV)
        if not user:
            raise SystemExit(f"--user or {USER_ENV} is required with --auth basic")
        raw = f"{user}:{token}".encode()
        headers["Authorization"] = "Basic " + base64.b64encode(raw).decode()
    else:
        headers["Authorization"] = f"Bearer {token}"

    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise SystemExit(f"Bitbucket API failed: HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Bitbucket API failed using {env_name}: {exc.reason}") from exc


def repo_info_from_args(args: argparse.Namespace) -> RepoInfo:
    if args.base_url:
        if not args.project or not args.repo:
            raise SystemExit("--project and --repo are required with --base-url")
        return RepoInfo(args.base_url, args.project, args.repo)
    return infer_repo_info(remote_url(args.repo_dir, args.remote))


def pull_request_url(info: RepoInfo, pr_id: int | None = None) -> str:
    base = f"{info.base_url}/rest/api/1.0/projects/{urllib.parse.quote(info.project)}/repos/{urllib.parse.quote(info.repo)}/pull-requests"
    return f"{base}/{pr_id}" if pr_id is not None else base


def read_text_arg(value: str | None, file_path: str | None) -> str | None:
    if value is not None and file_path is not None:
        raise SystemExit("use either --description or --description-file, not both")
    if file_path is None:
        return value
    with open(file_path, "r", encoding="utf-8") as handle:
        return handle.read()


def create_pr(args: argparse.Namespace) -> dict:
    source = args.source or current_branch(args.repo_dir)
    target = args.target or default_target_branch(args.repo_dir, args.remote)
    if not source:
        raise SystemExit("could not determine source branch; pass --source")

    info = repo_info_from_args(args)
    title = args.title or source
    description = read_text_arg(args.description, args.description_file) or draft_description(args.repo_dir, args.remote, source, target)

    payload = {
        "title": title,
        "description": description,
        "state": "OPEN",
        "open": True,
        "closed": False,
        "fromRef": {"id": f"refs/heads/{source}", "repository": {"slug": info.repo, "project": {"key": info.project}}},
        "toRef": {"id": f"refs/heads/{target}", "repository": {"slug": info.repo, "project": {"key": info.project}}},
    }
    if args.reviewers:
        payload["reviewers"] = [{"user": {"name": name}} for name in args.reviewers]

    url = pull_request_url(info)
    if args.dry_run:
        return {"dryRun": True, "url": url, "payload": payload}
    return api_request("POST", url, payload, args.auth, args.user)


def ref_payload(ref: dict) -> dict:
    repository = ref.get("repository", {})
    project = repository.get("project", {})
    payload = {"id": ref["id"]}
    if repository:
        payload["repository"] = {
            "slug": repository["slug"],
            "project": {"key": project["key"]},
        }
    return payload


def reviewer_payload(reviewers: list[dict]) -> list[dict]:
    payload = []
    for reviewer in reviewers:
        user = reviewer.get("user", {})
        name = user.get("name")
        if name:
            payload.append({"user": {"name": name}})
    return payload


def get_pr(args: argparse.Namespace) -> dict:
    info = repo_info_from_args(args)
    url = pull_request_url(info, args.pr_id)
    return api_request("GET", url, None, args.auth, args.user)


def update_pr(args: argparse.Namespace) -> dict:
    info = repo_info_from_args(args)
    url = pull_request_url(info, args.pr_id)
    current = api_request("GET", url, None, args.auth, args.user)
    payload = {
        "title": current["title"],
        "description": current.get("description", ""),
        "version": current["version"],
        "fromRef": ref_payload(current["fromRef"]),
        "toRef": ref_payload(current["toRef"]),
        "reviewers": reviewer_payload(current.get("reviewers", [])),
    }
    if args.title is not None:
        payload["title"] = args.title
    description = read_text_arg(args.description, args.description_file)
    if description is not None:
        payload["description"] = description
    elif args.refresh_description:
        source = args.source or current_branch(args.repo_dir)
        target = args.target or default_target_branch(args.repo_dir, args.remote)
        payload["description"] = draft_description(args.repo_dir, args.remote, source, target)
    if args.dry_run:
        return {"dryRun": True, "url": url, "payload": payload}
    return api_request("PUT", url, payload, args.auth, args.user)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bitbucket-helper", description=DESCRIPTION)
    sub = parser.add_subparsers(dest="cmd")

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--repo-dir", default=".")
        p.add_argument("--remote", default="origin")
        p.add_argument("--source")
        p.add_argument("--target")

    draft = sub.add_parser("draft", help="print a PR description draft")
    add_common(draft)

    def add_api(p: argparse.ArgumentParser) -> None:
        add_common(p)
        p.add_argument("--base-url")
        p.add_argument("--project")
        p.add_argument("--repo")
        p.add_argument("--auth", choices=("bearer", "basic"), default="basic")
        p.add_argument("--user")
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--json", action="store_true", help="print raw Bitbucket API JSON")

    create = sub.add_parser("create", help="create a Bitbucket Server pull request")
    add_api(create)
    create.add_argument("--title")
    create.add_argument("--description")
    create.add_argument("--description-file")
    create.add_argument("--reviewers", nargs="*", default=[])

    get = sub.add_parser("get", help="read a Bitbucket Server pull request")
    add_api(get)
    get.add_argument("pr_id", type=int)

    update = sub.add_parser("update", help="update a Bitbucket Server pull request title/description")
    add_api(update)
    update.add_argument("pr_id", type=int)
    update.add_argument("--title")
    update.add_argument("--description")
    update.add_argument("--description-file")
    update.add_argument("--refresh-description", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.cmd is None:
        home_view()
        return 0
    if args.cmd == "draft":
        source = args.source or current_branch(args.repo_dir)
        target = args.target or default_target_branch(args.repo_dir, args.remote)
        sys.stdout.write(draft_description(args.repo_dir, args.remote, source, target))
        return 0
    if args.cmd == "create":
        result = create_pr(args)
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print_pr_result(result, "create")
        return 0
    if args.cmd == "get":
        result = get_pr(args)
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print_pr_result(result, "get")
        return 0
    if args.cmd == "update":
        result = update_pr(args)
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print_pr_result(result, "update")
        return 0
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
