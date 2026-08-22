#!/usr/bin/env python3
"""Benchmark harness for skill format A/B testing on weak models.

Tests whether weak-model-friendly SKILL.md formatting improves:
  - Invocation accuracy (does the model pick the right skill?)
  - False-positive rate (does the model avoid wrong skills?)
  - Step adherence (does the model follow each step?)
  - Checklist coverage (does the model address checklist items?)

Usage:
  # Run with new format (current files)
  BENCH_MODEL=mimo-v2.5 python3 bench/run_bench.py

  # Run with old format (git HEAD~1)
  BENCH_MODEL=mimo-v2.5 python3 bench/run_bench.py --format old --output old.json

  # Compare two runs
  python3 bench/run_bench.py --compare old.json new.json

  # List scenarios
  python3 bench/run_bench.py --list

  # Self-test scoring functions
  python3 bench/run_bench.py --self-test

Environment:
  BENCH_API_BASE  API base URL (default: http://localhost:8000/v1)
  BENCH_API_KEY   API key (default: dummy)
  BENCH_MODEL     Model name (or use --model)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_DEFAULT = Path(__file__).parent / "scenarios.jsonl"

ROUTE_SKILL_SLASHES = {
    # The old snapshot predates decision-drift-guard.
    "old": [
        "/grilling", "/goal-loop", "/implement", "/code-review",
        "/pr-writing", "/bitbucket-helper", "/creating-worktrees",
        "/parallel-agents", "/codebase-design", "/go", "/git", "/tdd",
        "/personal-knowledge",
    ],
    "new": [
        "/grilling", "/goal-loop", "/implement", "/code-review",
        "/pr-writing", "/bitbucket-helper", "/creating-worktrees",
        "/parallel-agents", "/codebase-design", "/go", "/git", "/tdd",
        "/personal-knowledge", "/decision-drift-guard",
    ],
}

# Backwards-compatible name for callers importing the scoring helper.
ALL_SKILL_SLASHES = ROUTE_SKILL_SLASHES["new"]


# ---------------------------------------------------------------------------
# Skill content loading
# ---------------------------------------------------------------------------

def skill_path(skill_name: str) -> Path | None:
    for bucket in ("engineering", "productivity", "personal"):
        p = ROOT / "skills" / bucket / skill_name / "SKILL.md"
        if p.is_file():
            return p
    return None


def scenario_applies_to_format(scenario: dict, fmt: str) -> bool:
    return fmt in scenario.get("formats", ("old", "new"))


def load_skill(skill_name: str, fmt: str) -> str:
    p = skill_path(skill_name)
    if p is None:
        return f"ERROR: skill '{skill_name}' not found"
    if fmt == "old":
        rel = p.relative_to(ROOT)
        result = subprocess.run(
            ["git", "show", f"HEAD~1:{rel}"],
            capture_output=True, text=True, cwd=ROOT,
        )
        if result.returncode != 0:
            return f"ERROR: old format not available: {result.stderr.strip()}"
        return result.stdout
    return p.read_text()


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def call_api(base_url: str, api_key: str, model: str,
             system: str, user: str, max_tokens: int = 1024) -> str:
    url = f"{base_url.rstrip('/')}/chat/completions"
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0,
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return f"API_ERROR ({e.code}): {body}"
    except Exception as e:
        return f"API_ERROR: {e}"


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def is_api_error(response: str) -> bool:
    return response.startswith("API_ERROR")


def keyword_in_text(text: str, keyword: str) -> bool:
    pattern = rf"(?<!\w){re.escape(keyword.lower())}(?!\w)"
    return re.search(pattern, text.lower()) is not None


def score_route(response: str, scenario: dict, fmt: str = "new") -> dict:
    text = response.lower()
    should_trigger = scenario.get("should_trigger", True)

    invocation_correct = False
    false_positive = False

    if should_trigger:
        expected = scenario.get("expected_keywords", [])
        invocation_correct = any(kw.lower() in text for kw in expected)
    else:
        unexpected = scenario.get("unexpected_keywords")
        if unexpected is None:
            unexpected = ROUTE_SKILL_SLASHES.get(fmt, ALL_SKILL_SLASHES)
        if fmt == "old":
            new_only = set(ROUTE_SKILL_SLASHES["new"]) - set(ROUTE_SKILL_SLASHES["old"])
            unexpected = [kw for kw in unexpected if kw not in new_only]
        false_positive = any(kw.lower() in text for kw in unexpected)

    return {
        "invocation_correct": invocation_correct,
        "false_positive": false_positive,
        "step_adherence": None,
        "checklist_coverage": None,
    }


def score_execute(response: str, scenario: dict) -> dict:
    text = response.lower()
    should_trigger = scenario.get("should_trigger", True)

    if not should_trigger:
        unexpected = scenario.get("unexpected_keywords", [])
        triggered = any(keyword_in_text(text, kw) for kw in unexpected)
        return {
            "invocation_correct": None,
            "false_positive": triggered,
            "step_adherence": None,
            "checklist_coverage": None,
        }

    steps = scenario.get("expected_steps", [])
    covered = 0
    step_details = []
    for step in steps:
        keywords = step.get("keywords", [])
        hit = any(kw.lower() in text for kw in keywords)
        step_details.append({"name": step["name"], "covered": hit})
        if hit:
            covered += 1
    step_adherence = covered / len(steps) if steps else None

    checklist = scenario.get("checklist_items", [])
    checklist_covered = 0
    for item in checklist:
        if item.lower() in text:
            checklist_covered += 1
    checklist_coverage = checklist_covered / len(checklist) if checklist else None

    return {
        "invocation_correct": None,
        "false_positive": None,
        "step_adherence": step_adherence,
        "checklist_coverage": checklist_coverage,
        "step_details": step_details,
    }


def score_scenario(response: str, scenario: dict, fmt: str = "new") -> dict:
    if scenario["mode"] == "route":
        return score_route(response, scenario, fmt)
    return score_execute(response, scenario)


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------

def build_prompt(scenario: dict, skill_content: str) -> tuple[str, str, int]:
    if scenario["mode"] == "route":
        system = (
            "You are a routing assistant. Read the skill map below and route "
            "the user's request to the appropriate skill by naming it. "
            "If no skill fits, say 'no skill needed'.\n\n"
            "---\n" + skill_content + "\n---"
        )
        return system, scenario["task"], 256
    system = (
        "Follow the skill instructions below.\n\n"
        "---\n" + skill_content + "\n---"
    )
    return system, scenario["task"], 2048


# ---------------------------------------------------------------------------
# Main benchmark runner
# ---------------------------------------------------------------------------

def load_scenarios(path: Path) -> list[dict]:
    scenarios = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                scenarios.append(json.loads(line))
    return scenarios


def run_bench(args) -> int:
    base_url = os.environ.get("BENCH_API_BASE", "http://localhost:8000/v1")
    api_key = os.environ.get("BENCH_API_KEY", "dummy")
    model = args.model or os.environ.get("BENCH_MODEL")
    if not model:
        print("error: --model or BENCH_MODEL is required")
        return 2

    scenarios = [
        sc for sc in load_scenarios(Path(args.scenarios))
        if scenario_applies_to_format(sc, args.format)
    ]
    print(f"Benchmark: model={model}  format={args.format}  scenarios={len(scenarios)}\n")

    results = []
    for sc in scenarios:
        skill_content = load_skill(sc["skill"], args.format)
        if skill_content.startswith("ERROR"):
            print(f"  {sc['id']}: SKIP ({skill_content})")
            continue

        system, user, max_tokens = build_prompt(sc, skill_content)
        response = call_api(base_url, api_key, model, system, user, max_tokens)
        if is_api_error(response):
            print(f"  {sc['id']}: SKIP ({response[:120]})")
            continue
        scores = score_scenario(response, sc, args.format)
        results.append({**sc, "response": response[:500], "scores": scores})

        if sc["mode"] == "route":
            if sc.get("should_trigger", True):
                ok = scores["invocation_correct"]
                print(f"  {sc['id']}: {'PASS' if ok else 'FAIL'}  "
                      f"expected={sc.get('expected_keywords', [])}  "
                      f"got={response[:80]!r}")
            else:
                ok = not scores["false_positive"]
                print(f"  {sc['id']}: {'PASS' if ok else 'FAIL'}  "
                      f"(negative: {'false positive!' if not ok else 'clean'})")
        else:
            if not sc.get("should_trigger", True):
                ok = not scores["false_positive"]
                print(f"  {sc['id']}: {'PASS' if ok else 'FAIL'}  "
                      f"(negative: {'should not trigger but did!' if not ok else 'correctly skipped'})")
            else:
                sa = scores["step_adherence"] or 0
                cc = scores["checklist_coverage"] or 0
                ok = sa >= 0.5
                covered = sum(1 for s in scores.get("step_details", []) if s["covered"])
                total = len(scores.get("step_details", []))
                print(f"  {sc['id']}: {'PASS' if ok else 'FAIL'}  "
                      f"steps={covered}/{total}  checklist={cc:.0%}")

    print_summary(results, model, args.format)

    if args.output:
        save_results(results, model, args.format, args.output)
        print(f"\nResults saved to {args.output}")

    return 0


def print_summary(results: list[dict], model: str, fmt: str) -> None:
    route_pos = [r for r in results if r["mode"] == "route" and r.get("should_trigger", True)]
    route_neg = [r for r in results if r["mode"] == "route" and not r.get("should_trigger", True)]
    exec_pos = [r for r in results if r["mode"] == "execute" and r.get("should_trigger", True)]
    exec_neg = [r for r in results if r["mode"] == "execute" and not r.get("should_trigger", True)]

    inv_acc = sum(1 for r in route_pos if r["scores"]["invocation_correct"]) / len(route_pos) if route_pos else 0
    fp_route = sum(1 for r in route_neg if r["scores"]["false_positive"]) / len(route_neg) if route_neg else 0
    step_adh = sum(r["scores"]["step_adherence"] for r in exec_pos) / len(exec_pos) if exec_pos else 0
    check_cov = sum(r["scores"]["checklist_coverage"] for r in exec_pos) / len(exec_pos) if exec_pos else 0
    exec_fp = sum(1 for r in exec_neg if r["scores"]["false_positive"]) / len(exec_neg) if exec_neg else 0

    print(f"\n{'=' * 55}")
    print(f"  Model: {model}    Format: {fmt}")
    print(f"  Scenarios: {len(results)}")
    print(f"{'=' * 55}")
    print(f"  Invocation accuracy:  {inv_acc:>5.0%}  ({sum(1 for r in route_pos if r['scores']['invocation_correct'])}/{len(route_pos)} route positives)")
    print(f"  False-positive rate:  {fp_route:>5.0%}  ({sum(1 for r in route_neg if r['scores']['false_positive'])}/{len(route_neg)} route negatives)")
    print(f"  Step adherence:       {step_adh:>5.0%}  (avg across execute positives)")
    print(f"  Checklist coverage:   {check_cov:>5.0%}  (avg across execute positives)")
    print(f"  Exec false-positive:  {exec_fp:>5.0%}  ({sum(1 for r in exec_neg if r['scores']['false_positive'])}/{len(exec_neg)} execute negatives)")


def save_results(results: list[dict], model: str, fmt: str, path: str) -> None:
    route_pos = [r for r in results if r["mode"] == "route" and r.get("should_trigger", True)]
    route_neg = [r for r in results if r["mode"] == "route" and not r.get("should_trigger", True)]
    exec_pos = [r for r in results if r["mode"] == "execute" and r.get("should_trigger", True)]
    exec_neg = [r for r in results if r["mode"] == "execute" and not r.get("should_trigger", True)]

    output = {
        "model": model,
        "format": fmt,
        "summary": {
            "invocation_accuracy": sum(1 for r in route_pos if r["scores"]["invocation_correct"]) / len(route_pos) if route_pos else 0,
            "false_positive_rate": sum(1 for r in route_neg if r["scores"]["false_positive"]) / len(route_neg) if route_neg else 0,
            "step_adherence": sum(r["scores"]["step_adherence"] for r in exec_pos) / len(exec_pos) if exec_pos else 0,
            "checklist_coverage": sum(r["scores"]["checklist_coverage"] for r in exec_pos) / len(exec_pos) if exec_pos else 0,
            "exec_false_positive_rate": sum(1 for r in exec_neg if r["scores"]["false_positive"]) / len(exec_neg) if exec_neg else 0,
            "total_scenarios": len(results),
        },
        "scenarios": results,
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(output, indent=2))


# ---------------------------------------------------------------------------
# Compare
# ---------------------------------------------------------------------------

def compare(path1: str, path2: str) -> int:
    d1 = json.loads(Path(path1).read_text())
    d2 = json.loads(Path(path2).read_text())
    s1, s2 = d1["summary"], d2["summary"]

    metrics = [
        ("invocation_accuracy", "Invocation accuracy", True),
        ("false_positive_rate", "False-positive rate", False),
        ("step_adherence", "Step adherence", True),
        ("checklist_coverage", "Checklist coverage", True),
        ("exec_false_positive_rate", "Exec false-positive", False),
    ]

    print(f"\n{'Metric':<25} {'Old':>10} {'New':>10} {'Delta':>10}")
    print(f"{'-' * 55}")
    for key, label, higher_better in metrics:
        old, new = s1.get(key, 0), s2.get(key, 0)
        delta = new - old
        sign = "+" if delta >= 0 else ""
        good = (delta > 0 and higher_better) or (delta < 0 and not higher_better)
        marker = " *" if good and abs(delta) > 0.01 else ""
        print(f"  {label:<23} {old:>10.0%} {new:>10.0%} {sign}{delta:>9.0%}{marker}")

    print(f"\n  Old: model={d1['model']}  format={d1['format']}")
    print(f"  New: model={d2['model']}  format={d2['format']}")
    return 0


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def self_test() -> int:
    """Validate scoring functions on known inputs."""

    assert is_api_error("API_ERROR (408): timeout") is True
    assert is_api_error("no error") is False
    assert keyword_in_text("Untestable edge", "test") is False
    assert keyword_in_text("Write a test first", "test") is True

    # Format gates keep new-only skills out of the old baseline.
    assert scenario_applies_to_format({"formats": ["new"]}, "old") is False
    assert scenario_applies_to_format({"formats": ["new"]}, "new") is True
    assert skill_path("decision-drift-guard") is not None

    # Old format does not know the decision guard; new format does.
    decision_negative = {
        "mode": "route",
        "should_trigger": False,
        "unexpected_keywords": ["/decision-drift-guard"],
    }
    assert score_route("/decision-drift-guard", decision_negative, "old")["false_positive"] is False
    assert score_route("/decision-drift-guard", decision_negative, "new")["false_positive"] is True

    decision = next(
        sc for sc in load_scenarios(SCENARIOS_DEFAULT) if sc["id"] == "exec-06"
    )
    r = score_execute(
        "Loaded the ledger. Classified this as a supersession. Old decision: SQLite. "
        "New instruction: PostgreSQL. Impact: database migration. "
        "Choose replace, branch, or refine. Plan paused before acting.",
        decision,
    )
    assert r["step_adherence"] == 1.0
    assert r["checklist_coverage"] == 1.0

    # Route positive: correct invocation
    r = score_route("You should use /grilling for this", {
        "mode": "route", "should_trigger": True, "expected_keywords": ["grilling"],
    })
    assert r["invocation_correct"] is True, f"expected True, got {r}"
    assert r["false_positive"] is False

    # Route positive: missed invocation
    r = score_route("I think you should write some tests", {
        "mode": "route", "should_trigger": True, "expected_keywords": ["grilling"],
    })
    assert r["invocation_correct"] is False

    # Route negative: clean (no skill triggered)
    r = score_route("No skill needed, just explain the code", {
        "mode": "route", "should_trigger": False,
        "unexpected_keywords": ["/grilling", "/implement"],
    })
    assert r["false_positive"] is False

    # Route negative: false positive
    r = score_route("You should use /implement for this", {
        "mode": "route", "should_trigger": False,
        "unexpected_keywords": ["/grilling", "/implement"],
    })
    assert r["false_positive"] is True

    # Execute positive: all steps covered
    r = score_execute(
        "Step 1: find repo root with git rev-parse --show-toplevel. "
        "Step 2: branch is feature-auth-123. "
        "Step 3: sanitize slug by replacing / with -. "
        "Step 4: add to info/exclude. "
        "Step 5: git worktree add. "
        "Done when: worktree exists, branch is correct, exclusion recorded, codegraph not applicable. "
        "Step 7: report path, branch, exclude.",
        {
            "mode": "execute", "should_trigger": True,
            "expected_steps": [
                {"name": "s1", "keywords": ["git rev-parse", "show-toplevel"]},
                {"name": "s2", "keywords": ["feature-auth-123"]},
                {"name": "s3", "keywords": ["sanitize", "slug", "replace"]},
                {"name": "s4", "keywords": ["exclude", "info/exclude"]},
                {"name": "s5", "keywords": ["worktree add", "git worktree"]},
                {"name": "s6", "keywords": ["codegraph", "not applicable"]},
                {"name": "s7", "keywords": ["report", "path", "branch"]},
            ],
            "checklist_items": ["worktree exists", "branch", "exclusion", "codegraph"],
        },
    )
    assert r["step_adherence"] == 1.0, f"expected 1.0, got {r['step_adherence']}"
    assert r["checklist_coverage"] == 1.0

    # Execute positive: partial coverage
    r = score_execute(
        "First I'll find the repo root. Then create the worktree.",
        {
            "mode": "execute", "should_trigger": True,
            "expected_steps": [
                {"name": "s1", "keywords": ["repo root", "git rev-parse"]},
                {"name": "s2", "keywords": ["worktree add", "git worktree"]},
                {"name": "s3", "keywords": ["exclude", "info/exclude"]},
            ],
            "checklist_items": ["worktree exists", "exclusion"],
        },
    )
    assert r["step_adherence"] is not None
    assert 0 < r["step_adherence"] < 1.0
    assert r["checklist_coverage"] == 0.0

    # Execute negative: should not trigger
    r = score_execute("Just add the comment to the file.", {
        "mode": "execute", "should_trigger": False,
        "unexpected_keywords": ["red", "green", "refactor", "test"],
    })
    assert r["false_positive"] is False

    r = score_execute("First write a failing test (red), then make it green.", {
        "mode": "execute", "should_trigger": False,
        "unexpected_keywords": ["red", "green", "refactor", "test"],
    })
    assert r["false_positive"] is True

    print("Self-test passed")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", help="Model name (or BENCH_MODEL env)")
    parser.add_argument("--format", choices=["old", "new"], default="new", help="Skill format to test (default: new)")
    parser.add_argument("--scenarios", default=str(SCENARIOS_DEFAULT), help="Path to scenarios.jsonl")
    parser.add_argument("--output", help="Save results to JSON file")
    parser.add_argument("--compare", nargs=2, metavar=("OLD", "NEW"), help="Compare two result files")
    parser.add_argument("--list", action="store_true", help="List scenarios and exit")
    parser.add_argument("--self-test", action="store_true", help="Run scoring self-tests and exit")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    if args.list:
        scenarios = [
            sc for sc in load_scenarios(Path(args.scenarios))
            if scenario_applies_to_format(sc, args.format)
        ]
        for sc in scenarios:
            trigger = sc.get("should_trigger", True)
            mode = sc["mode"]
            skill = sc["skill"]
            print(f"  {sc['id']:<16} [{mode:<7}] skill={skill:<20} trigger={trigger}")
        print(f"\n{len(scenarios)} scenarios")
        return 0

    if args.compare:
        return compare(args.compare[0], args.compare[1])

    return run_bench(args)


if __name__ == "__main__":
    sys.exit(main())
