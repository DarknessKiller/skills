---
name: code-review
description: "Review a diff along two axes: Standards (repo rules and code smells) and Spec (does the change implement the requested behaviour). Use when the user wants a branch, PR, or work-in-progress diff reviewed."
---

# Code Review

Review the diff between `HEAD` and a fixed point. If none is supplied, discover it in this order: the upstream branch, the merge-base with the likely default branch, then a user question when more than one comparison is plausible.

Keep the two axes separate:

- **Standards** — does the diff follow this repo's documented standards and avoid obvious design smells?
- **Spec** — does the diff faithfully implement the originating issue, PRD, or user request?

## Process

1. **Pin the fixed point**
    - Use the user-supplied commit, branch, tag, or ref.
    - Otherwise inspect the current branch's upstream and likely default branch before asking.
    - Confirm `git rev-parse <fixed-point>` works and `git diff <fixed-point>...HEAD` is non-empty.
    - Completion: one valid comparison point is recorded, or the ambiguity is explicit.

2. **Find the spec source**
   - Prefer issue references in commits or branch names.
   - Then check paths the user supplied.
   - Then search `docs/`, `specs/`, `.scratch/`, and PR descriptions.
    - If no spec exists, the Spec axis reports "no spec available".
    - Completion: both axes have a named source or an explicit no-spec result.

3. **Find standards sources**
   - Read `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, and relevant skills.
   - Apply repo standards first.
   - Use design smells only as judgement calls: duplication, speculative generality, shotgun surgery, message chains, feature envy, primitive obsession, and middle men.

4. **Run independent review**
   - For meaningful diffs, spawn Standards and Spec sub-agents in parallel.
   - Give each the diff command, commit list, and only the context for its axis.
    - Do not let one axis rerank or suppress the other.
    - Completion: every meaningful changed area has been considered on both applicable axes.

5. **Report**
   - Use `## Standards` and `## Spec` headings.
   - Include file/line references and fixes.
    - End with counts per axis and the worst issue within each axis.
    - Completion: the report has `## Standards`, `## Spec`, file/line evidence, fixes, counts, and worst issue per axis.
