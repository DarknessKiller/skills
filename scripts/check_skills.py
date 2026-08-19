#!/usr/bin/env python3
"""Check the skill pack's source, metadata, docs, and plugin surfaces."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PROMOTED_BUCKETS = {"engineering", "productivity"}
BUCKETS = PROMOTED_BUCKETS | {"misc", "personal", "in-progress", "deprecated"}
REQUIRED_DOC_HEADINGS = {
    "## What it does",
    "## When to reach for it",
    "## Where it fits",
}


def skill_dirs(root: Path) -> list[tuple[str, str, Path]]:
    result = []
    skills_root = root / "skills"
    for bucket in sorted(skills_root.iterdir()):
        if not bucket.is_dir() or bucket.name not in BUCKETS:
            continue
        for skill in sorted(bucket.iterdir()):
            if (skill / "SKILL.md").is_file():
                result.append((bucket.name, skill.name, skill))
    return result


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    values = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([\w-]+):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"')
    return values


def yaml_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", text)
    return match.group(1).strip().strip('"') if match else None


def linked_names(text: str, marker: str) -> set[str]:
    return set(re.findall(rf"\./skills/[^/]+/([^/]+)/{re.escape(marker)}", text))


def manifest_names(text: str) -> set[str]:
    return set(re.findall(r'"\./skills/(?:engineering|productivity)/([^/"]+)"', text))


def check(root: Path) -> list[str]:
    errors: list[str] = []
    skills = skill_dirs(root)
    promoted = {(bucket, name) for bucket, name, _ in skills if bucket in PROMOTED_BUCKETS}
    all_names = {name for _, name, _ in skills}

    if not skills:
        return ["no skills found under skills/"]

    readme = (root / "README.md").read_text()
    plugin = (root / ".claude-plugin/plugin.json").read_text()
    router = (root / "skills/engineering/ask-atlas/SKILL.md").read_text()

    if not (root / "scripts/check_skills.py").is_file():
        errors.append("scripts/check_skills.py is missing")

    readme_names = linked_names(readme, "SKILL.md")
    manifest = manifest_names(plugin)
    if readme_names != {name for _, name in promoted}:
        errors.append("README.md promoted skill links do not match promoted skills")
    if manifest != {name for _, name in promoted}:
        errors.append("plugin.json skills do not match promoted skills")

    for bucket, name, directory in skills:
        skill_file = directory / "SKILL.md"
        metadata_file = directory / "agents/openai.yaml"
        text = skill_file.read_text()
        metadata = metadata_file.read_text() if metadata_file.is_file() else ""
        values = frontmatter(text)

        if values.get("name") != name:
            errors.append(f"{skill_file}: frontmatter name must be {name!r}")
        if not values.get("description"):
            errors.append(f"{skill_file}: missing frontmatter description")
        if not metadata_file.is_file():
            errors.append(f"{directory}: missing agents/openai.yaml")
        else:
            if not re.search(r"(?m)^interface:\s*$", metadata):
                errors.append(f"{metadata_file}: missing interface block")
            if yaml_value(metadata, "display_name") is None:
                errors.append(f"{metadata_file}: missing display_name")
            if yaml_value(metadata, "short_description") is None:
                errors.append(f"{metadata_file}: missing short_description")

        user_invoked = values.get("disable-model-invocation") == "true"
        has_policy = re.search(r"(?m)^policy:\s*$", metadata) is not None
        allow_implicit = yaml_value(metadata, "allow_implicit_invocation")
        if user_invoked and allow_implicit != "false":
            errors.append(f"{name}: user-invoked skills need allow_implicit_invocation: false")
        if user_invoked and not has_policy:
            errors.append(f"{name}: user-invoked skills need a policy block")
        if not user_invoked and "disable-model-invocation" in values:
            errors.append(f"{name}: model-invoked skills must omit disable-model-invocation")
        if not user_invoked and (has_policy or allow_implicit is not None):
            errors.append(f"{name}: model-invoked skills must omit the policy block")

        if bucket in PROMOTED_BUCKETS:
            doc = root / "docs" / bucket / f"{name}.md"
            if not doc.is_file():
                errors.append(f"{name}: missing docs page {doc}")
            else:
                doc_text = doc.read_text()
                if "Quickstart:" not in doc_text or "[Source](" not in doc_text:
                    errors.append(f"{doc}: missing Quickstart or Source")
                errors.extend(f"{doc}: missing {heading}" for heading in REQUIRED_DOC_HEADINGS - set(doc_text.splitlines()))

            bucket_readme = root / "skills" / bucket / "README.md"
            if f"./{name}/SKILL.md" not in bucket_readme.read_text():
                errors.append(f"{bucket_readme}: missing {name}")
        else:
            if name in readme_names or name in manifest:
                errors.append(f"{name}: non-promoted skill appears on a promoted surface")

    expected_router_names = {name for _, name in promoted if name != "ask-atlas"}
    missing_routes = expected_router_names - {name for name in all_names if re.search(rf"(?<![\w-])/{re.escape(name)}(?![\w-])", router)}
    errors.extend(f"ask-atlas: missing route for /{name}" for name in sorted(missing_routes))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check(args.root.resolve())
    if errors:
        print("Skill pack checks failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Skill pack checks passed ({len(skill_dirs(args.root.resolve()))} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
