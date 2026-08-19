#!/usr/bin/env python3
"""Draft pull request descriptions from local git history."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

DESCRIPTION = "Draft reviewable pull request descriptions from local git history"
VERSION = "0.1.0"
PROFILES = ("generic", "frontend", "dart", "go")


def q(value: object) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    return q(value)


def emit_toon(data: dict[str, Any], indent: int = 0) -> list[str]:
    lines: list[str] = []
    pad = " " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{pad}{key}:")
            lines.extend(emit_toon(value, indent + 2))
        elif isinstance(value, list):
            if not value:
                lines.append(f"{pad}{key}: []")
            elif all(not isinstance(item, (dict, list)) for item in value):
                lines.append(f"{pad}{key}[{len(value)}]: " + ",".join(scalar(item) for item in value))
            elif all(isinstance(item, dict) and item.keys() == value[0].keys() for item in value):
                fields = list(value[0].keys())
                lines.append(f"{pad}{key}[{len(value)}]{{{','.join(fields)}}}:")
                for item in value:
                    lines.append(" " * (indent + 2) + ",".join(scalar(item[field]) for field in fields))
            else:
                lines.append(f"{pad}{key}[{len(value)}]:")
                for item in value:
                    if isinstance(item, dict):
                        lines.append(" " * (indent + 2) + "-")
                        lines.extend(emit_toon(item, indent + 4))
                    else:
                        lines.append(" " * (indent + 2) + f"- {scalar(item)}")
        else:
            lines.append(f"{pad}{key}: {scalar(value)}")
    return lines


def print_toon(data: dict[str, Any]) -> None:
    sys.stdout.write("\n".join(emit_toon(data)) + "\n")


def error(message: str, help_text: str | None = None, code: int = 1) -> int:
    data: dict[str, Any] = {"error": message}
    if help_text:
        data["help"] = help_text
    print_toon(data)
    return code


def valid_flags(parser: argparse.ArgumentParser) -> str:
    flags = sorted({flag for action in parser._actions for flag in action.option_strings})
    return ", ".join(flags) or "none"


def usage_help(parser: argparse.ArgumentParser, message: str) -> str:
    return f"{message}; valid flags: {valid_flags(parser)}; run `{parser.prog} --help`"


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        help_text = usage_help(self, message)
        raise SystemExit(error(message, help_text, 2))


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


def current_branch(repo_dir: str) -> str:
    return run_git(repo_dir, "branch", "--show-current")


def default_target_branch(repo_dir: str, remote: str) -> str:
    ref = run_git(repo_dir, "symbolic-ref", f"refs/remotes/{remote}/HEAD", check=False)
    if ref:
        return ref.rsplit("/", 1)[-1]
    for candidate in ("main", "master", "develop"):
        if run_git(repo_dir, "rev-parse", "--verify", f"{remote}/{candidate}", check=False):
            return candidate
    return "main"


def commits(repo_dir: str, remote: str, target: str, source: str) -> list[str]:
    out = run_git(repo_dir, "log", "--oneline", f"{remote}/{target}..{source}", check=False)
    return [line for line in out.splitlines() if line.strip()]


def changed_files(repo_dir: str, remote: str, target: str, source: str) -> list[str]:
    out = run_git(repo_dir, "diff", "--name-only", f"{remote}/{target}...{source}", check=False)
    return [line for line in out.splitlines() if line.strip()]


def jira_keys(*texts: str) -> list[str]:
    seen: set[str] = set()
    keys: list[str] = []
    for text in texts:
        for key in re.findall(r"\b[A-Z][A-Z0-9]+-\d+\b", text):
            if key not in seen:
                seen.add(key)
                keys.append(key)
    return keys


def detect_framework(repo_dir: str) -> str | None:
    if (Path(repo_dir) / "go.mod").is_file():
        return "Go"

    pubspec = Path(repo_dir) / "pubspec.yaml"
    if pubspec.is_file():
        try:
            text = pubspec.read_text()
        except OSError:
            text = ""
        if re.search(r"(?m)^\s*(sdk:\s*flutter|flutter(?:_test|_lints)?\s*:)", text):
            return "Flutter"
        return "Dart"

    package = Path(repo_dir) / "package.json"
    if not package.is_file():
        return None
    try:
        data = json.loads(package.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    dependencies = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    for framework, markers in (
        ("Next.js", {"next"}),
        ("Nuxt", {"nuxt"}),
        ("Angular", {"@angular/core"}),
        ("Svelte", {"svelte"}),
        ("Vue", {"vue"}),
        ("React", {"react", "react-native"}),
        ("Preact", {"preact"}),
        ("Astro", {"astro", "@astrojs/react", "@astrojs/vue"}),
    ):
        if markers & dependencies.keys():
            return framework
    return None


def detect_profile(repo_dir: str) -> str:
    framework = detect_framework(repo_dir)
    if framework == "Dart":
        return "dart"
    if framework == "Go":
        return "go"
    return "frontend" if framework else "generic"


def profile_guidance(profile: str, repo_dir: str) -> list[str]:
    framework = detect_framework(repo_dir)
    if profile == "dart":
        return [
            "<!-- Framework: Detected Dart; verify dart format, dart analyze, and dart test results. -->",
        ]
    if profile == "go":
        return [
            "<!-- Language: Detected Go; verify gofmt, go vet, and go test ./... results. -->",
        ]
    if profile == "frontend":
        guidance = [
            "<!-- Framework validation: Run the project's build, lint, typecheck, and relevant component or end-to-end tests. -->",
            "<!-- Visual validation: Record responsive, accessibility, and visual checks, or explain why they are not applicable. -->",
        ]
        if framework:
            guidance.insert(0, f"<!-- Framework: Detected {framework}; verify the framework-specific behavior and conventions. -->")
        return guidance
    return ["<!-- Automated checks: List the relevant tests, lint, typecheck, formatting, or analysis commands. -->"]


def supports_screenshot(profile: str) -> bool:
    return profile == "frontend"


def draft_body(repo_dir: str, remote: str, source: str, target: str, profile: str | None = None) -> str:
    commit_lines = commits(repo_dir, remote, target, source)
    files = changed_files(repo_dir, remote, target, source)
    keys = jira_keys(source, "\n".join(commit_lines))
    profile = profile or detect_profile(repo_dir)
    changes = commit_lines[:12] or ["Describe the implementation changes."]

    lines = ["## Description", "<!-- Summarize what changed, why, scope, and non-goals. -->", "", "- Key changes:"]
    lines.extend(f"- {line}" for line in changes)
    if files:
        lines.extend(["", "- Files touched:"])
        lines.extend(f"- `{path}`" for path in files[:20])
        if len(files) > 20:
            lines.append(f"- ...and {len(files) - 20} more")
    lines.extend([
        "",
        "## Test Plan",
        "<!-- Give reviewers executable manual or automated test steps. -->",
        *profile_guidance(profile, repo_dir),
        "",
        "## Test Result",
        "<!-- Record tests, analysis, formatting, and visual validation results. -->",
        "- Tests: Not run yet.",
        "",
        "## Code Risk",
        "<!-- Describe runtime risk, mitigation, and rollback. -->",
        "- Risk: Describe the main runtime or review risk.",
        "- Mitigation: Describe safeguards or monitoring.",
        "- Rollback: Revert this PR.",
        "",
        "## Links",
        "<!-- Figma, Confluence, Documentation, or related tickets. -->",
    ])
    lines.extend(f"- {key}" for key in keys) if keys else lines.append("- Not applicable.")
    if supports_screenshot(profile):
        lines.extend([
            "",
            "## Screenshot",
            "<!-- Add screenshots or Figma Design Validation output for UI changes; skip if irrelevant. -->",
            "- Not applicable.",
        ])
    return "\n".join(lines) + "\n"


def draft(repo_dir: str, remote: str, source: str | None, target: str | None) -> dict[str, Any]:
    source = source or current_branch(repo_dir)
    target = target or default_target_branch(repo_dir, remote)
    if not source:
        raise RuntimeError("could not determine source branch; pass --source")
    commit_lines = commits(repo_dir, remote, target, source)
    files = changed_files(repo_dir, remote, target, source)
    help_text = ["Run `draft --format markdown` to print the PR body"]
    if len(commit_lines) > 12:
        help_text.append(f"Run `draft --format toon` after narrowing the branch; {len(commit_lines)} commits found")
    if len(files) > 20:
        help_text.append(f"{len(files)} changed files found; the TOON preview shows the first 20")
    if not commit_lines:
        help_text.append("No commits found between the target and source branches")
    if not files:
        help_text.append("No changed files found between the target and source branches")
    return {
        "pr": {"source": source, "target": target},
        "commits": [{"index": i + 1, "summary": line} for i, line in enumerate(commit_lines[:12])],
        "files": [{"path": path} for path in files[:20]],
        "counts": {"commits": len(commit_lines), "files": len(files)},
        "help": help_text,
    }


def display_path(path: str) -> str:
    home = str(Path.home())
    return "~" + path[len(home):] if path.startswith(home) else path


def home(repo_dir: str = ".", remote: str = "origin") -> dict[str, Any]:
    data: dict[str, Any] = {
        "tool": {"path": display_path(os.path.abspath(__file__)), "description": DESCRIPTION},
        "commands": [
            {"name": "draft", "usage": "python3 pr_writer.py draft --repo-dir ."},
        ],
    }
    source = current_branch(repo_dir)
    if source:
        data["branch"] = {"source": source, "target": default_target_branch(repo_dir, remote)}
    return data


def build_parser() -> argparse.ArgumentParser:
    parser = Parser(prog="pr_writer.py", description=DESCRIPTION)
    sub = parser.add_subparsers(dest="cmd", title="Available Commands", parser_class=Parser)
    draft_cmd = sub.add_parser(
        "draft",
        help="Draft a pull request description",
        description="Draft a reviewable pull request description from local git history.",
    )
    draft_cmd.add_argument("--repo-dir", default=".", help="git repository directory (default: .)")
    draft_cmd.add_argument("--remote", default="origin", help="git remote used for target comparison (default: origin)")
    draft_cmd.add_argument("--source", help="source branch (default: current branch)")
    draft_cmd.add_argument("--target", help="target branch (default: remote HEAD)")
    draft_cmd.add_argument("--format", choices=("markdown", "toon"), default="markdown", help="output format (default: markdown)")
    draft_cmd.add_argument("--profile", choices=PROFILES, help="PR template profile (default: detect from repository)")
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv in (["-v"], ["-V"], ["--version"]):
        print(VERSION)
        return 0
    if not argv:
        try:
            print_toon(home())
        except (OSError, RuntimeError) as exc:
            return error(str(exc))
        return 0
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "draft":
            data = draft(args.repo_dir, args.remote, args.source, args.target)
            if args.format == "toon":
                print_toon(data)
            else:
                sys.stdout.write(draft_body(args.repo_dir, args.remote, data["pr"]["source"], data["pr"]["target"], args.profile))
            return 0
        return error("unknown command", "Run `python3 pr_writer.py --help`", 2)
    except (OSError, RuntimeError, ValueError) as exc:
        return error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
