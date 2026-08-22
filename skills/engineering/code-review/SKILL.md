---
name: code-review
description: "Review a diff on two axes: Standards and Spec. Use when the user wants a diff, branch, or PR reviewed."
---

# Code Review

Review the diff between `HEAD` and a fixed point. Keep two axes separate:

- **Standards** — does the diff follow repo rules and avoid design smells?
- **Spec** — does the diff implement the originating issue, PRD, or request?

## Process

1. **Pin the fixed point.** Use the user-supplied commit/branch/tag/ref. Otherwise inspect upstream, then merge-base with likely default branch. Otherwise ask the user. Confirm `git rev-parse` works and `git diff` is non-empty.

2. **Find the spec source.** Check issue refs in commits/branch names, then user-supplied paths, then `docs/`, `specs/`, `.scratch/`, PR descriptions. IF no spec: Spec axis reports "no spec available".

3. **Find standards sources.** Read `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, and relevant skills. Apply repo standards first. Use design smells as judgement calls: duplication, speculative generality, shotgun surgery, message chains, feature envy, primitive obsession, middle men.

4. **Run independent review.** For meaningful diffs: spawn Standards and Spec sub-agents in parallel, each with only its axis context. Do not let one axis rerank or suppress the other.

5. **Report.** Use `## Standards` and `## Spec` headings. Include file/line references and fixes. End with counts per axis and the worst issue within each axis.

Completion: report has `## Standards`, `## Spec`, file/line evidence, fixes, counts, and worst issue per axis.
