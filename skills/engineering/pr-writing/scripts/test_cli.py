#!/usr/bin/env python3
"""Small no-dependency checks for the agent-facing CLI contract."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
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

print("CLI checks passed")
