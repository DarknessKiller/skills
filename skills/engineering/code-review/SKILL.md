---
name: code-review
description: "Review a diff along two axes: Standards (repo rules and code smells) and Spec (does the change implement the requested behaviour). Use when the user wants a branch, PR, or work-in-progress diff reviewed."
---

# Code Review

Review the diff between `HEAD` and a fixed point.

Keep the two axes separate:

- **Standards** — does the diff follow this repo's documented standards and avoid obvious design smells?
- **Spec** — does the diff faithfully implement the originating issue, PRD, or user request?

## Process

1. **Pin the fixed point**
   - Use the user-supplied commit, branch, tag, or ref.
   - If none is supplied, ask for one.
   - Confirm `git rev-parse <fixed-point>` works and `git diff <fixed-point>...HEAD` is non-empty.

2. **Find the spec source**
   - Prefer issue references in commits or branch names.
   - Then check paths the user supplied.
   - Then search `docs/`, `specs/`, `.scratch/`, and PR descriptions.
   - If no spec exists, the Spec axis reports "no spec available".

3. **Find standards sources**
   - Read `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, and relevant skills.
   - Apply repo standards first.
   - Use design smells only as judgement calls: duplication, speculative generality, shotgun surgery, message chains, feature envy, primitive obsession, and middle men.

4. **Run independent review**
   - For meaningful diffs, spawn Standards and Spec sub-agents in parallel.
   - Give each the diff command, commit list, and only the context for its axis.
   - Do not let one axis rerank or suppress the other.

5. **Report**
   - Use `## Standards` and `## Spec` headings.
   - Include file/line references and fixes.
   - End with counts per axis and the worst issue within each axis.
