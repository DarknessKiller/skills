#!/usr/bin/env python3
"""Small no-dependency checks for the agent-facing CLI contract."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PR_WRITER = Path(__file__).with_name("pr_writer.py")
BITBUCKET = ROOT / "skills/engineering/bitbucket-helper/scripts/bitbucket_server_pr.py"

spec = importlib.util.spec_from_file_location("pr_writer", PR_WRITER)
assert spec and spec.loader
pr_writer = importlib.util.module_from_spec(spec)
sys.modules["pr_writer"] = pr_writer
spec.loader.exec_module(pr_writer)

spec = importlib.util.spec_from_file_location("bitbucket_helper", BITBUCKET)
assert spec and spec.loader
bitbucket = importlib.util.module_from_spec(spec)
sys.modules["bitbucket_helper"] = bitbucket
spec.loader.exec_module(bitbucket)


assert pr_writer.emit_toon({"items": [{"id": "1", "title": "Fix"}]}) == [
    "items[1]{id,title}:",
    '  "1","Fix"',
]

with tempfile.TemporaryDirectory() as directory:
    frontend_repo = Path(directory)
    (frontend_repo / "package.json").write_text(json.dumps({"dependencies": {"next": "1.0.0"}}))
    assert pr_writer.detect_framework(str(frontend_repo)) == "Next.js"
    assert pr_writer.detect_profile(str(frontend_repo)) == "frontend"
    assert pr_writer.profile_guidance("frontend", str(frontend_repo))[0] == "<!-- Framework: Detected Next.js; verify the framework-specific behavior and conventions. -->"

    flutter_repo = frontend_repo / "flutter"
    flutter_repo.mkdir()
    (flutter_repo / "pubspec.yaml").write_text("dependencies:\n  flutter:\n    sdk: flutter\n")
    assert pr_writer.detect_framework(str(flutter_repo)) == "Flutter"
    assert pr_writer.detect_profile(str(flutter_repo)) == "frontend"

    dart_repo = frontend_repo / "dart"
    dart_repo.mkdir()
    (dart_repo / "pubspec.yaml").write_text("name: example\ndependencies:\n  args: ^2.0.0\n")
    assert pr_writer.detect_framework(str(dart_repo)) == "Dart"
    assert pr_writer.detect_profile(str(dart_repo)) == "dart"
    assert pr_writer.profile_guidance("dart", str(dart_repo)) == [
        "<!-- Framework: Detected Dart; verify dart format, dart analyze, and dart test results. -->",
    ]

    go_repo = frontend_repo / "go"
    go_repo.mkdir()
    (go_repo / "go.mod").write_text("module example.com/project\n\ngo 1.23\n")
    assert pr_writer.detect_framework(str(go_repo)) == "Go"
    assert pr_writer.detect_profile(str(go_repo)) == "go"
    assert pr_writer.profile_guidance("go", str(go_repo)) == [
        "<!-- Language: Detected Go; verify gofmt, go vet, and go test ./... results. -->",
    ]

    generic_repo = frontend_repo / "generic"
    generic_repo.mkdir()
    (generic_repo / "package.json").write_text(json.dumps({"dependencies": {"express": "1.0.0"}}))
    assert pr_writer.detect_framework(str(generic_repo)) is None
    assert pr_writer.detect_profile(str(generic_repo)) == "generic"
assert bitbucket.summarize_diff({"_raw_diff": "abcdefghij"}, 7, limit=5)["diff"]["truncated"]
assert bitbucket.summarize_file({"lines": [{"text": "hello"}]}, "a.txt")["file"]["preview"] == "hello"

for script in (PR_WRITER, BITBUCKET):
    version = subprocess.run([sys.executable, str(script), "--version"], text=True, capture_output=True, check=True)
    assert version.stdout.strip() == pr_writer.VERSION
    assert version.stderr == ""

invalid = subprocess.run([sys.executable, str(PR_WRITER), "--wat"], text=True, capture_output=True)
assert invalid.returncode == 2
assert "valid flags" in invalid.stdout
assert invalid.stderr == ""

create = bitbucket.build_parser().parse_args(["create", "--draft"])
assert create.draft is True
update = bitbucket.build_parser().parse_args(["update", "7", "--ready"])
assert update.draft is False

original_repo_info = bitbucket.repo_info_from_args
original_api_request = bitbucket.api_request
bitbucket.repo_info_from_args = lambda args: bitbucket.RepoInfo("https://example.test", "P", "r", True)
bitbucket.api_request = lambda info, method, url, payload, auth, user: payload if method == "POST" else {"title": "x", "description": "", "source": {}, "destination": {}} if method == "GET" else payload
created = bitbucket.create_pr(bitbucket.build_parser().parse_args([
    "create", "--draft", "--description", "x", "--source", "feature", "--target", "main"
]))
assert created["draft"] is True
ready = bitbucket.update_pr(bitbucket.build_parser().parse_args([
    "update", "7", "--ready", "--description", "x"
]))
assert ready["draft"] is False
bitbucket.repo_info_from_args = original_repo_info
bitbucket.api_request = original_api_request

print("CLI checks passed")
