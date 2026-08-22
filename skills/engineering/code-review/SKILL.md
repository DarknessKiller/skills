---
name: code-review
description: "Review a diff on Standards and Spec axes. Use for diff, branch, or PR review."
---

# Code Review

Review diff between `HEAD` and a fixed point. Two axes:

- **Standards** — repo rules, design smells.
- **Spec** — implements originating issue, PRD, or request.

## Steps

1. **Pin fixed point.** Use supplied ref. Otherwise upstream then merge-base with default. Confirm `git rev-parse` works, `git diff` non-empty.

2. **Find spec.** Check issue refs in commits/branch names, then paths, `docs/`, `specs/`, PR descriptions. IF no spec: "no spec available".

3. **Find standards.** Read `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, relevant skills. Apply repo standards first.

4. **Run review.** For meaningful diffs: spawn Standards and Spec sub-agents in parallel. Do not let one axis rerank the other.

5. **Report.** `## Standards` and `## Spec` headings. file:line evidence and fixes. Counts per axis. Worst issue per axis.

Completion: report has both headings, file:line evidence, fixes, counts, worst issue.
