#!/usr/bin/env python3
"""Bitbucket Server/Data Center and Cloud pull request helper."""

from __future__ import annotations

import argparse
import base64
import importlib.util
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
from typing import Any

PASSWORD_ENV = "BB_PASSWORD"
USER_ENV = "BB_USER"
CLOUD_API = "https://api.bitbucket.org/2.0"
DESCRIPTION = "Bitbucket Server/Cloud PRs, diffs, commits, approvals; SSH key management via agent"
PR_WRITER_PATH = Path(__file__).resolve().parents[2] / "pr-writing" / "scripts" / "pr_writer.py"

spec = importlib.util.spec_from_file_location("pr_writer", PR_WRITER_PATH)
if spec is None or spec.loader is None:
    raise SystemExit("could not load pr-writing helper")
pr_writer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pr_writer)


# ── Data ─────────────────────────────────────────────────────────────────────

@dataclass
class RepoInfo:
    base_url: str
    project: str
    repo: str
    cloud: bool


# ── Utilities ────────────────────────────────────────────────────────────────

def print_toon(data: dict[str, Any]) -> None:
    pr_writer.print_toon(data)


def q(value: object) -> str:
    return pr_writer.q(value)


def error(message: str, help_text: str | None = None, code: int = 1) -> int:
    data: dict[str, Any] = {"error": message}
    if help_text:
        data["help"] = help_text
    print_toon(data)
    return code


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise SystemExit(error(message, "Run `python3 bitbucket_server_pr.py --help`", 2))


def run_git(repo_dir: str, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", repo_dir, *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def display_path(path: str) -> str:
    home = str(Path.home())
    return "~" + path[len(home):] if path.startswith(home) else path


def current_branch(repo_dir: str) -> str:
    return run_git(repo_dir, "branch", "--show-current")


def remote_url(repo_dir: str, remote: str) -> str:
    return run_git(repo_dir, "remote", "get-url", remote)


def default_target_branch(repo_dir: str, remote: str) -> str:
    return pr_writer.default_target_branch(repo_dir, remote)


def read_text_arg(value: str | None, file_path: str | None) -> str | None:
    if value is not None and file_path is not None:
        raise RuntimeError("use either --description or --description-file, not both")
    if file_path is None:
        return value
    return Path(file_path).read_text(encoding="utf-8")


def preview(text: str, limit: int = 1000) -> tuple[str, bool]:
    return (text, False) if len(text) <= limit else (text[:limit].rstrip() + f"... (truncated, {len(text)} chars total)", True)


def print_text(text: str) -> None:
    if text:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")


# ── SSH agent ────────────────────────────────────────────────────────────────

def ssh_agent_public_keys() -> list[str]:
    """List public keys loaded in the SSH agent."""
    result = subprocess.run(["ssh-add", "-L"], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError("ssh-add -L failed — is the SSH agent running? (Bitwarden Desktop Settings → SSH Agent)")
    keys = [k for k in result.stdout.strip().splitlines() if k.strip()]
    if not keys:
        raise RuntimeError("no keys loaded in SSH agent")
    return keys


def get_key_from_agent(index: int = 0) -> str:
    """Return a single public key from the SSH agent by index."""
    keys = ssh_agent_public_keys()
    if index >= len(keys):
        raise RuntimeError(f"SSH agent has {len(keys)} key(s), index {index} out of range")
    return keys[index]


def read_key_file(path: str) -> str:
    """Read a public key from a file."""
    text = Path(path).read_text(encoding="utf-8").strip()
    if not text.startswith(("ssh-", "ecdsa-", "sk-")):
        raise RuntimeError(f"{path} does not look like a public key")
    return text.splitlines()[0]


# ── Repo info ────────────────────────────────────────────────────────────────

def infer_repo_info(url: str) -> RepoInfo:
    normalized = url.strip()

    if normalized.startswith("git@"):
        match = re.match(r"git@([^:]+):/?(.+)$", normalized)
        if not match:
            raise RuntimeError(f"unsupported ssh remote: {url}")
        host, path = match.group(1), match.group(2)
        if host == "bitbucket.org":
            parts = path.rstrip("/").removesuffix(".git").split("/", 1)
            if len(parts) != 2:
                raise RuntimeError(f"could not parse Bitbucket Cloud remote: {url}")
            return RepoInfo(CLOUD_API, parts[0], parts[1], True)
        normalized = f"https://{host}/{path}"

    parsed = urllib.parse.urlparse(normalized)
    if not parsed.scheme or not parsed.netloc:
        raise RuntimeError(f"unsupported remote URL: {url}")

    if parsed.netloc == "bitbucket.org":
        path = parsed.path.rstrip("/").removesuffix(".git").strip("/")
        parts = path.split("/", 1)
        if len(parts) != 2:
            raise RuntimeError(f"could not parse Bitbucket Cloud remote: {url}")
        return RepoInfo(CLOUD_API, parts[0], parts[1], True)

    path = parsed.path.rstrip("/")
    match = re.match(r"^/scm/([^/]+)/([^/]+?)(?:\.git)?$", path, re.IGNORECASE) or re.match(
        r"^/projects/([^/]+)/repos/([^/]+?)(?:/.*)?$", path, re.IGNORECASE
    )
    if not match:
        raise RuntimeError(f"could not infer Bitbucket project/repo from {url}")
    return RepoInfo(f"{parsed.scheme}://{parsed.netloc}", match.group(1).upper(), match.group(2), False)


def repo_info_from_args(args: argparse.Namespace) -> RepoInfo:
    if args.base_url:
        if not args.project or not args.repo:
            raise RuntimeError("--project and --repo are required with --base-url")
        cloud = getattr(args, "cloud", False) or "bitbucket.org" in args.base_url
        base = CLOUD_API if cloud else args.base_url
        return RepoInfo(base, args.project, args.repo, cloud)
    return infer_repo_info(remote_url(args.repo_dir, args.remote))


# ── URL construction ─────────────────────────────────────────────────────────

def repo_api_url(info: RepoInfo, path: str = "", params: dict[str, object] | None = None) -> str:
    if info.cloud:
        base = f"{CLOUD_API}/repositories/{urllib.parse.quote(info.project)}/{urllib.parse.quote(info.repo)}"
    else:
        base = f"{info.base_url}/rest/api/1.0/projects/{urllib.parse.quote(info.project)}/repos/{urllib.parse.quote(info.repo)}"
    url = f"{base}/{path.lstrip('/')}" if path else base
    if params:
        clean = {k: v for k, v in params.items() if v is not None}
        if clean:
            url += "?" + urllib.parse.urlencode(clean)
    return url


def pull_request_url(info: RepoInfo, pr_id: int | None = None, path: str = "", params: dict[str, object] | None = None) -> str:
    if info.cloud:
        base = f"{CLOUD_API}/repositories/{urllib.parse.quote(info.project)}/{urllib.parse.quote(info.repo)}/pullrequests"
        if pr_id is not None:
            base += f"/{pr_id}"
        if path:
            base += "/" + path.lstrip("/")
        if params:
            clean = {k: v for k, v in params.items() if v is not None}
            if clean:
                base += "?" + urllib.parse.urlencode(clean)
        return base
    pr_path = "pull-requests" if pr_id is None else f"pull-requests/{pr_id}"
    if path:
        pr_path += "/" + path.lstrip("/")
    return repo_api_url(info, pr_path, params)


# ── API ──────────────────────────────────────────────────────────────────────

def token_from_env() -> str:
    token = os.environ.get(PASSWORD_ENV)
    if not token:
        raise RuntimeError(f"missing token; set {PASSWORD_ENV}")
    return token


def _auth_headers(auth: str, user: str | None) -> dict[str, str]:
    token = token_from_env()
    if auth == "basic":
        user = user or os.environ.get(USER_ENV)
        if not user:
            raise RuntimeError(f"--user or {USER_ENV} is required with --auth basic")
        return {"Authorization": "Basic " + base64.b64encode(f"{user}:{token}".encode()).decode()}
    return {"Authorization": f"Bearer {token}"}


def api_request(method: str, url: str, payload: dict | None, auth: str, user: str | None) -> dict:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    headers.update(_auth_headers(auth, user))
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")[:500]
        raise RuntimeError(f"Bitbucket API failed: HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Bitbucket API failed: {exc.reason}") from exc


def api_request_text(method: str, url: str, auth: str, user: str | None) -> str:
    """Make an API request and return raw text (for Cloud diff endpoint)."""
    headers = {"Accept": "text/plain"}
    headers.update(_auth_headers(auth, user))
    request = urllib.request.Request(url, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read().decode()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")[:500]
        raise RuntimeError(f"Bitbucket API failed: HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Bitbucket API failed: {exc.reason}") from exc


# ── PR helpers ───────────────────────────────────────────────────────────────

def ref(info: RepoInfo, branch: str) -> dict:
    return {"id": f"refs/heads/{branch}", "repository": {"slug": info.repo, "project": {"key": info.project}}}


def ref_payload(value: dict) -> dict:
    repository = value.get("repository", {})
    project = repository.get("project", {})
    payload = {"id": value["id"]}
    if repository:
        payload["repository"] = {"slug": repository["slug"], "project": {"key": project["key"]}}
    return payload


def reviewer_payload_server(reviewers: list[dict]) -> list[dict]:
    return [{"user": {"name": r["user"]["name"]}} for r in reviewers if r.get("user", {}).get("name")]


def branch_name(ref_data: dict) -> str:
    return str(ref_data.get("displayId") or ref_data.get("id", "")).removeprefix("refs/heads/")


def pr_url(pr: dict) -> str:
    for link in pr.get("links", {}).get("self", []):
        if link.get("href"):
            return link["href"]
    return ""


# ── PR operations ────────────────────────────────────────────────────────────

def create_pr(args: argparse.Namespace) -> dict:
    source = args.source or current_branch(args.repo_dir)
    target = args.target or default_target_branch(args.repo_dir, args.remote)
    if not source:
        raise RuntimeError("could not determine source branch; pass --source")
    info = repo_info_from_args(args)
    description = read_text_arg(args.description, args.description_file) or pr_writer.draft_body(args.repo_dir, args.remote, source, target)

    if info.cloud:
        payload: dict[str, Any] = {
            "title": args.title or source,
            "description": description,
            "source": {"branch": {"name": source}, "repository": {"full_name": f"{info.project}/{info.repo}"}},
            "destination": {"branch": {"name": target}, "repository": {"full_name": f"{info.project}/{info.repo}"}},
        }
        if args.reviewers:
            payload["reviewers"] = [{"username": name} for name in args.reviewers]
    else:
        payload = {
            "title": args.title or source,
            "description": description,
            "state": "OPEN",
            "open": True,
            "closed": False,
            "fromRef": ref(info, source),
            "toRef": ref(info, target),
        }
        if args.reviewers:
            payload["reviewers"] = [{"user": {"name": name}} for name in args.reviewers]

    url = pull_request_url(info)
    return {"dryRun": True, "url": url, "payload": payload} if args.dry_run else api_request("POST", url, payload, args.auth, args.user)


def get_pr(args: argparse.Namespace) -> dict:
    info = repo_info_from_args(args)
    return api_request("GET", pull_request_url(info, args.pr_id), None, args.auth, args.user)


def update_pr(args: argparse.Namespace) -> dict:
    info = repo_info_from_args(args)
    url = pull_request_url(info, args.pr_id)
    current = api_request("GET", url, None, args.auth, args.user)

    if info.cloud:
        payload = {
            "title": current["title"],
            "description": current.get("description", ""),
            "source": current.get("source", {}),
            "destination": current.get("destination", {}),
        }
    else:
        payload = {
            "title": current["title"],
            "description": current.get("description", ""),
            "version": current["version"],
            "fromRef": ref_payload(current["fromRef"]),
            "toRef": ref_payload(current["toRef"]),
            "reviewers": reviewer_payload_server(current.get("reviewers", [])),
        }

    if args.title is not None:
        payload["title"] = args.title
    description = read_text_arg(args.description, args.description_file)
    if description is not None:
        payload["description"] = description
    elif args.refresh_description:
        source = args.source or current_branch(args.repo_dir)
        target = args.target or default_target_branch(args.repo_dir, args.remote)
        payload["description"] = pr_writer.draft_body(args.repo_dir, args.remote, source, target)

    return {"dryRun": True, "url": url, "payload": payload} if args.dry_run else api_request("PUT", url, payload, args.auth, args.user)


def approve_pr(args: argparse.Namespace) -> dict:
    info = repo_info_from_args(args)
    if info.cloud:
        url = pull_request_url(info, args.pr_id, "approve")
        return {"dryRun": True, "url": url, "version": None} if args.dry_run else api_request("POST", url, None, args.auth, args.user)
    version = args.version
    if version is None:
        version = api_request("GET", pull_request_url(info, args.pr_id), None, args.auth, args.user)["version"]
    url = pull_request_url(info, args.pr_id, "approve", {"version": version})
    return {"dryRun": True, "url": url, "version": version} if args.dry_run else api_request("POST", url, None, args.auth, args.user)


def review_context(args: argparse.Namespace) -> dict:
    return {
        "pr": get_pr(args),
        "changes": pr_changes(argparse.Namespace(**{**vars(args), "limit": args.files_limit})),
        "commits": pr_commits(argparse.Namespace(**{**vars(args), "limit": args.commits_limit})),
    }


# ── PR data ──────────────────────────────────────────────────────────────────

def pr_changes(args: argparse.Namespace) -> dict:
    info = repo_info_from_args(args)
    if info.cloud:
        return api_request("GET", pull_request_url(info, args.pr_id, "diffstat", {"pagelen": args.limit}), None, args.auth, args.user)
    return api_request("GET", pull_request_url(info, args.pr_id, "changes", {"limit": args.limit}), None, args.auth, args.user)


def pr_commits(args: argparse.Namespace) -> dict:
    info = repo_info_from_args(args)
    return api_request("GET", pull_request_url(info, args.pr_id, "commits", {"limit": args.limit}), None, args.auth, args.user)


def pr_diff(args: argparse.Namespace) -> dict:
    info = repo_info_from_args(args)
    if info.cloud:
        url = pull_request_url(info, args.pr_id, "diff")
        return {"_raw_diff": api_request_text("GET", url, args.auth, args.user)}
    path = "diff" + ("/" + urllib.parse.quote(args.path.strip("/"), safe="/") if args.path else "")
    return api_request("GET", pull_request_url(info, args.pr_id, path, {"contextLines": args.context}), None, args.auth, args.user)


def repo_file(args: argparse.Namespace) -> dict:
    info = repo_info_from_args(args)
    if info.cloud:
        ref = (args.at or args.source or "main").removeprefix("refs/heads/")
        api_path = f"src/{urllib.parse.quote(ref, safe='')}/{urllib.parse.quote(args.path.strip('/'), safe='/')}"
        return api_request("GET", repo_api_url(info, api_path), None, args.auth, args.user)
    api_path = "browse/" + urllib.parse.quote(args.path.strip("/"), safe="/")
    at = args.at or (f"refs/heads/{args.source}" if args.source else None)
    return api_request("GET", repo_api_url(info, api_path, {"at": at, "limit": args.limit}), None, args.auth, args.user)


def repo_commit(args: argparse.Namespace) -> dict:
    info = repo_info_from_args(args)
    endpoint = f"commit/{urllib.parse.quote(args.commit_id)}" if info.cloud else "commits/" + urllib.parse.quote(args.commit_id)
    return api_request("GET", repo_api_url(info, endpoint), None, args.auth, args.user)


# ── SSH key management ───────────────────────────────────────────────────────

def add_ssh_key(args: argparse.Namespace) -> dict:
    info = repo_info_from_args(args)

    if args.agent:
        key_text = get_key_from_agent(args.agent_index)
    elif args.key_file:
        key_text = read_key_file(args.key_file)
    elif args.key:
        key_text = args.key.strip()
    else:
        raise RuntimeError("provide --key, --key-file, or --agent")

    label = args.label or "bitbucket-helper"

    if info.cloud:
        url = repo_api_url(info, "deploy-keys")
        payload: dict[str, Any] = {"key": key_text, "label": label}
    else:
        url = f"{info.base_url}/rest/ssh/1.0/keys"
        payload = {"text": key_text, "label": label}

    return {"dryRun": True, "url": url, "payload": payload} if args.dry_run else api_request("POST", url, payload, args.auth, args.user)


# ── Summarize ────────────────────────────────────────────────────────────────

def summarize_pr(result: dict, action: str, full: bool = False) -> dict[str, Any]:
    if full:
        return {"api_result": result}
    if result.get("dryRun"):
        payload = result["payload"]
        from_val = payload.get("fromRef", {}).get("id") or payload.get("source", {}).get("branch", {}).get("name")
        to_val = payload.get("toRef", {}).get("id") or payload.get("destination", {}).get("branch", {}).get("name")
        return {
            "dry_run": {"action": action, "url": result["url"], "title": payload.get("title"), "from": from_val, "to": to_val, "reviewers": len(payload.get("reviewers", []))},
            "help": ["Re-run without `--dry-run` to call Bitbucket"],
        }
    data: dict[str, Any] = {
        "pull_request": {
            "action": action,
            "id": result.get("id", result.get("number", "")),
            "title": result.get("title"),
            "state": result.get("state"),
            "version": result.get("version", ""),
            "from": branch_name(result.get("fromRef", {})) or result.get("source", {}).get("branch", {}).get("name", ""),
            "to": branch_name(result.get("toRef", {})) or result.get("destination", {}).get("branch", {}).get("name", ""),
            "url": pr_url(result),
        }
    }
    return data


def summarize_changes(result: dict, pr_id: int, full: bool = False) -> dict[str, Any]:
    if full:
        return {"api_result": result}
    values = result.get("values", [])
    files = []
    for item in values:
        if "path" in item:
            # Server format
            path = item.get("path", {})
            src = item.get("srcPath") or {}
            files.append({
                "path": path.get("toString") or path.get("displayId") or path.get("name") or "",
                "type": item.get("type", ""),
                "src": src.get("toString", "") if isinstance(src, dict) else "",
            })
        elif "new" in item:
            # Cloud diffstat format
            new = item.get("new", {})
            old = item.get("old", {})
            files.append({
                "path": new.get("path", ""),
                "type": item.get("status", ""),
                "src": old.get("path", ""),
                "added": item.get("lines_added", 0),
                "removed": item.get("lines_removed", 0),
            })
    data: dict[str, Any] = {"changes": {"pr": pr_id, "count": result.get("size", len(files)), "is_last_page": result.get("isLastPage", True)}, "files": files}
    if not result.get("isLastPage", True):
        data["help"] = ["Re-run with a higher `--limit` to include more changed files"]
    return data


def summarize_commits(result: dict, pr_id: int, full: bool = False) -> dict[str, Any]:
    if full:
        return {"api_result": result}
    commits = []
    for item in result.get("values", []):
        author = item.get("author") or {}
        commits.append({
            "id": str(item.get("id") or item.get("hash", ""))[:12],
            "message": str(item.get("message", "")).splitlines()[0],
            "author": author.get("displayName") or author.get("display_name") or author.get("name") or "",
        })
    data: dict[str, Any] = {"commits": commits, "page": {"pr": pr_id, "count": result.get("size", len(commits)), "is_last_page": result.get("isLastPage", True)}}
    if not result.get("isLastPage", True):
        data["help"] = ["Re-run with a higher `--limit` to include more commits"]
    return data


def diff_lines(result: dict) -> list[str]:
    lines: list[str] = []
    for diff in result.get("diffs", []):
        path = (diff.get("destination") or diff.get("source") or {}).get("toString", "")
        if path:
            lines.append(f"diff -- {path}")
        for hunk in diff.get("hunks", []):
            if hunk.get("sourceLine") is not None or hunk.get("destinationLine") is not None:
                lines.append(f"@@ -{hunk.get('sourceLine', '')} +{hunk.get('destinationLine', '')} @@")
            for segment in hunk.get("segments", []):
                marker = {"ADDED": "+", "REMOVED": "-", "CONTEXT": " "}.get(segment.get("type"), " ")
                for line in segment.get("lines", []):
                    lines.append(marker + str(line.get("line", "")))
    return lines or [json.dumps(result, separators=(",", ":"))]


def summarize_diff(result: dict, pr_id: int, full: bool = False, limit: int = 4000) -> dict[str, Any]:
    if full:
        return {"api_result": result}
    if "_raw_diff" in result:
        text = result["_raw_diff"]
    else:
        text = "\n".join(diff_lines(result))
    _, truncated = preview(text, limit)
    data: dict[str, Any] = {"diff": {"pr": pr_id, "chars": len(text), "truncated": truncated}}
    data["help"] = ["Re-run with `--format text` to print the diff"]
    return data


def summarize_file(result: dict, path: str, full: bool = False, limit: int = 4000) -> dict[str, Any]:
    if full:
        return {"api_result": result}
    lines = [str(line.get("text", "")) for line in result.get("lines", [])]
    text = "\n".join(lines)
    _, truncated = preview(text, limit)
    data: dict[str, Any] = {"file": {"path": path, "chars": len(text), "lines": len(lines), "truncated": truncated}}
    data["help"] = ["Re-run with `--format text` to print the file"]
    if result.get("isLastPage") is False:
        data["help"].append("Use a higher `--limit` to fetch all file lines")
    return data


def summarize_commit(result: dict, full: bool = False) -> dict[str, Any]:
    if full:
        return {"api_result": result}
    author = result.get("author") or {}
    return {"commit": {"id": str(result.get("id") or result.get("hash", ""))[:12], "message": str(result.get("message", "")).splitlines()[0], "author": author.get("displayName") or author.get("display_name") or author.get("name") or ""}}


def summarize_approval(result: dict, pr_id: int, full: bool = False) -> dict[str, Any]:
    if full:
        return {"api_result": result}
    if result.get("dryRun"):
        return {"dry_run": {"action": "approve", "pr": pr_id, "version": result["version"], "url": result["url"]}, "help": ["Re-run without `--dry-run` to approve"]}
    user = result.get("user") or {}
    return {"approval": {"pr": pr_id, "approved": result.get("approved"), "user": user.get("name") or user.get("displayName") or user.get("display_name") or ""}}


def summarize_review_context(result: dict, pr_id: int, full: bool = False) -> dict[str, Any]:
    if full:
        return {"api_result": result}
    data = summarize_pr(result["pr"], "get")
    data.update(summarize_changes(result["changes"], pr_id))
    data.update(summarize_commits(result["commits"], pr_id))
    return data


def summarize_ssh_key(result: dict, full: bool = False) -> dict[str, Any]:
    if full:
        return {"api_result": result}
    if result.get("dryRun"):
        return {"dry_run": {"url": result["url"], "label": result["payload"].get("label"), "key_preview": result["payload"].get("key", result["payload"].get("text", ""))[:40] + "..."}, "help": ["Re-run without `--dry-run` to add the key"]}
    key_id = result.get("id") or (result.get("key") or {}).get("id")
    label = result.get("label") or (result.get("key") or {}).get("label") or ""
    return {"ssh_key": {"id": key_id, "label": label}}


# ── Home ─────────────────────────────────────────────────────────────────────

def home(repo_dir: str = ".", remote: str = "origin") -> dict[str, Any]:
    data: dict[str, Any] = {"tool": {"path": display_path(os.path.abspath(__file__)), "description": DESCRIPTION}}
    try:
        info = repo_info_from_args(argparse.Namespace(base_url=None, project=None, repo=None, repo_dir=repo_dir, remote=remote, cloud=False))
        data["repo"] = {"base_url": info.base_url, "project": info.project, "repo": info.repo, "type": "cloud" if info.cloud else "server"}
        data["branch"] = {"source": current_branch(repo_dir) or "unknown", "target": default_target_branch(repo_dir, remote)}
    except RuntimeError:
        data["repo"] = "unknown"
    data["commands"] = [
        {"name": "get", "usage": "python3 bitbucket_server_pr.py get <pr_id> --repo-dir ."},
        {"name": "create", "usage": "python3 bitbucket_server_pr.py create --repo-dir . --target main --title \"...\""},
        {"name": "update", "usage": "python3 bitbucket_server_pr.py update <pr_id> --repo-dir . --refresh-description"},
        {"name": "approve", "usage": "python3 bitbucket_server_pr.py approve <pr_id> --repo-dir ."},
        {"name": "review-context", "usage": "python3 bitbucket_server_pr.py review-context <pr_id> --repo-dir ."},
        {"name": "files", "usage": "python3 bitbucket_server_pr.py files <pr_id> --repo-dir ."},
        {"name": "diff", "usage": "python3 bitbucket_server_pr.py diff <pr_id> --repo-dir . --format text"},
        {"name": "file", "usage": "python3 bitbucket_server_pr.py file <path> --repo-dir . --format text"},
        {"name": "commits", "usage": "python3 bitbucket_server_pr.py commits <pr_id> --repo-dir ."},
        {"name": "commit", "usage": "python3 bitbucket_server_pr.py commit <sha> --repo-dir ."},
        {"name": "ssh-key", "usage": "python3 bitbucket_server_pr.py ssh-key --repo-dir . --agent"},
    ]
    return data


# ── Parser ───────────────────────────────────────────────────────────────────

def add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--repo-dir", default=".", help="git repository directory (default: .)")
    p.add_argument("--remote", default="origin", help="git remote (default: origin)")
    p.add_argument("--source", help="source branch")
    p.add_argument("--target", help="target branch")


def add_api(p: argparse.ArgumentParser) -> None:
    add_common(p)
    p.add_argument("--base-url", help="Bitbucket base URL (auto-detects Cloud vs Server)")
    p.add_argument("--project", help="Bitbucket project/workspace key (with --base-url)")
    p.add_argument("--repo", help="Bitbucket repo slug (with --base-url)")
    p.add_argument("--cloud", action="store_true", help="force Bitbucket Cloud API")
    p.add_argument("--auth", choices=("bearer", "basic"), default="basic", help="authentication mode (default: basic)")
    p.add_argument("--user", help=f"Bitbucket username (default: ${USER_ENV})")
    p.add_argument("--dry-run", action="store_true", help="show the request without sending it")
    p.add_argument("--full", action="store_true", help="emit the complete API result")


def build_parser() -> argparse.ArgumentParser:
    parser = Parser(prog="bitbucket_server_pr.py", description=DESCRIPTION)
    sub = parser.add_subparsers(dest="cmd", title="Available Commands", parser_class=Parser)

    create = sub.add_parser("create", help="Create a pull request")
    add_api(create)
    create.add_argument("--title")
    create.add_argument("--description")
    create.add_argument("--description-file")
    create.add_argument("--reviewers", nargs="*", default=[])

    get = sub.add_parser("get", help="Show pull request metadata")
    add_api(get)
    get.add_argument("pr_id", type=int, help="pull request id")
    get.add_argument("--body", action="store_true", help="print the description preview as plain Markdown")
    get.add_argument("--limit-chars", type=int, default=1000)

    update = sub.add_parser("update", help="Update a pull request")
    add_api(update)
    update.add_argument("pr_id", type=int)
    update.add_argument("--title")
    update.add_argument("--description")
    update.add_argument("--description-file")
    update.add_argument("--refresh-description", action="store_true")

    approve = sub.add_parser("approve", help="Approve a pull request")
    add_api(approve)
    approve.add_argument("pr_id", type=int)
    approve.add_argument("--version", type=int)

    review = sub.add_parser("review-context", help="Show PR review context")
    add_api(review)
    review.add_argument("pr_id", type=int)
    review.add_argument("--files-limit", type=int, default=100)
    review.add_argument("--commits-limit", type=int, default=50)

    files = sub.add_parser("files", help="List changed files")
    add_api(files)
    files.add_argument("pr_id", type=int)
    files.add_argument("--limit", type=int, default=100)

    commits = sub.add_parser("commits", help="List pull request commits")
    add_api(commits)
    commits.add_argument("pr_id", type=int)
    commits.add_argument("--limit", type=int, default=50)

    diff = sub.add_parser("diff", help="Show a pull request diff")
    add_api(diff)
    diff.add_argument("pr_id", type=int)
    diff.add_argument("--path")
    diff.add_argument("--context", type=int, default=3)
    diff.add_argument("--limit-chars", type=int, default=4000)
    diff.add_argument("--format", choices=("toon", "text"), default="toon")

    file_cmd = sub.add_parser("file", help="Show repository file contents")
    add_api(file_cmd)
    file_cmd.add_argument("path")
    file_cmd.add_argument("--at")
    file_cmd.add_argument("--limit", type=int, default=500)
    file_cmd.add_argument("--limit-chars", type=int, default=4000)
    file_cmd.add_argument("--format", choices=("toon", "text"), default="toon")

    commit = sub.add_parser("commit", help="Show commit details")
    add_api(commit)
    commit.add_argument("commit_id")

    ssh_key = sub.add_parser("ssh-key", help="Add an SSH public key to Bitbucket")
    add_api(ssh_key)
    ssh_key.add_argument("--key", help="SSH public key text (inline)")
    ssh_key.add_argument("--key-file", help="path to SSH public key file")
    ssh_key.add_argument("--agent", action="store_true", help="read public key from SSH agent (Bitwarden Desktop)")
    ssh_key.add_argument("--agent-index", type=int, default=0, help="key index in agent (default: 0)")
    ssh_key.add_argument("--label", help="key label (default: bitbucket-helper)")

    return parser


# ── Main ─────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print_toon(home())
        return 0
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "create":
            print_toon(summarize_pr(create_pr(args), "create", args.full))
        elif args.cmd == "get":
            result = get_pr(args)
            if args.body:
                print_text(preview(str(result.get("description", "")), args.limit_chars)[0])
            else:
                print_toon(summarize_pr(result, "get", args.full))
        elif args.cmd == "update":
            print_toon(summarize_pr(update_pr(args), "update", args.full))
        elif args.cmd == "approve":
            print_toon(summarize_approval(approve_pr(args), args.pr_id, args.full))
        elif args.cmd == "review-context":
            print_toon(summarize_review_context(review_context(args), args.pr_id, args.full))
        elif args.cmd == "files":
            print_toon(summarize_changes(pr_changes(args), args.pr_id, args.full))
        elif args.cmd == "commits":
            print_toon(summarize_commits(pr_commits(args), args.pr_id, args.full))
        elif args.cmd == "diff":
            result = pr_diff(args)
            if args.format == "text":
                if "_raw_diff" in result:
                    print_text(preview(result["_raw_diff"], args.limit_chars)[0])
                else:
                    print_text(preview("\n".join(diff_lines(result)), args.limit_chars)[0])
            else:
                print_toon(summarize_diff(result, args.pr_id, args.full, args.limit_chars))
        elif args.cmd == "file":
            result = repo_file(args)
            if args.format == "text":
                print_text(preview("\n".join(str(line.get("text", "")) for line in result.get("lines", [])), args.limit_chars)[0])
            else:
                print_toon(summarize_file(result, args.path, args.full, args.limit_chars))
        elif args.cmd == "commit":
            print_toon(summarize_commit(repo_commit(args), args.full))
        elif args.cmd == "ssh-key":
            print_toon(summarize_ssh_key(add_ssh_key(args), args.full))
        else:
            return error("unknown command", "Run `python3 bitbucket_server_pr.py --help`", 2)
        return 0
    except RuntimeError as exc:
        return error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
