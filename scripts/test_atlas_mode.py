#!/usr/bin/env python3
"""Regression checks for the Atlas-mode handover contract."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
skill = ROOT / "skills/engineering/atlas-mode/SKILL.md"
text = skill.read_text().lower()
metadata = (ROOT / "skills/engineering/atlas-mode/agents/openai.yaml").read_text().lower()

assert "disable-model-invocation: true" in text
assert "policy:" in metadata
assert "allow_implicit_invocation: false" in metadata
assert "persistence" not in text
assert "main agent" in text
assert "invoker" in text
assert "plan" in text and "handover" in text
assert "owns planning only" in text
assert "delegates any required work" in text
assert "model and effort routing" in text
assert "gpt-5.6-sol" in text
assert "gpt-5.6-luna" in text
assert "gpt-5.6-terra" in text
assert "effort" in text
assert "xhigh" in text and "medium" in text and "max" in text
assert "agent(" in text
assert "lane's model" in text
assert "/writing-for-agents" in text
assert "/unslop" in text
assert "one action per step" in text
assert "one-line completion" in text
assert "every blocker" in text
assert "stop" in text and "verify" in text
assert "red blocker" not in text
assert re.search(r"red.*green.*refactor", text, re.DOTALL)
assert "passing check" in text
assert "normal command" in text
assert "untestable" in text

print("Atlas-mode contract checks passed")
