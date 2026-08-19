#!/usr/bin/env python3
"""Small no-dependency checks for skill-pack metadata validation."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_skills", Path(__file__).with_name("check_skills.py"))
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


assert checker.check(ROOT) == []

with tempfile.TemporaryDirectory() as directory:
    fixture = Path(directory)
    (fixture / "skills/engineering/example/agents").mkdir(parents=True)
    (fixture / "skills/engineering/example/SKILL.md").write_text(
        "---\nname: wrong\ndescription: Example\n---\n\n# Example\n"
    )
    (fixture / "skills/engineering/example/agents/openai.yaml").write_text(
        'interface:\n  display_name: "Example"\n  short_description: "Example"\n'
    )
    (fixture / "README.md").write_text("")
    (fixture / ".claude-plugin").mkdir()
    (fixture / ".claude-plugin/plugin.json").write_text("{}")
    (fixture / "skills/engineering/README.md").write_text("")
    (fixture / "skills/engineering/ask-atlas/SKILL.md").parent.mkdir(parents=True)
    (fixture / "skills/engineering/ask-atlas/SKILL.md").write_text("")
    errors = checker.check(fixture)
    assert any("frontmatter name" in error for error in errors)
    assert any("missing docs page" in error for error in errors)

    model = fixture / "skills/misc/model"
    (model / "agents").mkdir(parents=True)
    (model / "SKILL.md").write_text(
        "---\nname: model\ndescription: Model\ndisable-model-invocation: false\n---\n\n# Model\n"
    )
    (model / "agents/openai.yaml").write_text(
        'interface:\n  display_name: "Model"\n  short_description: "Model"\n'
    )
    assert any("must omit disable-model-invocation" in error for error in checker.check(fixture))

print("Skill-pack checks passed")
