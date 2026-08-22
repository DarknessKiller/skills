---
name: code-review
description: "Review a diff on two axes: Standards and Spec. Use when the user wants a diff, branch, or PR reviewed."
---

# Code Review

Review the diff between `HEAD` and a fixed point. Keep two axes separate:

- **Standards** — does the diff follow repo rules and avoid design smells?
- **Spec** — does the diff implement the originating issue, PRD, or request?

## Process

1. **Pin the fixed point.**
   - IF the user supplied a commit, branch, tag, or ref: use it.
   - Otherwise: inspect the current branch's upstream.
   - Otherwise: try the merge-base with the likely default branch.
   - Otherwise: ask the user when more than one comparison is plausible.
   - Run `git rev-parse <fixed-point>` to confirm it works.
   - Run `git diff <fixed-point>...HEAD` to confirm it is non-empty.

   **Done when:**
   - [ ] One valid comparison point is recorded.
   - [ ] The ambiguity is explicit if no point was found.

2. **Find the spec source.**
   - Check issue references in commits or branch names.
   - Check paths the user supplied.
   - Search `docs/`, `specs/`, `.scratch/`, and PR descriptions.
   - IF no spec exists: the Spec axis reports "no spec available".

   **Done when:**
   - [ ] Standards source is named.
   - [ ] Spec source is named or "no spec available" is stated.

3. **Find standards sources.**
   - Read `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`.
   - Read relevant skills.
   - Apply repo standards first.
   - Use design smells as judgement calls: duplication, speculative generality, shotgun surgery, message chains, feature envy, primitive obsession, middle men.

4. **Run independent review.**
   - IF the diff is meaningful: spawn Standards and Spec sub-agents in parallel.
   - Give each sub-agent the diff command, commit list, and only its axis context.
   - Do NOT let one axis rerank or suppress the other.

   **Done when:**
   - [ ] Every changed area is considered on both axes.

5. **Report.**
   - Use `## Standards` and `## Spec` headings.
   - Include file/line references and fixes for each finding.
   - End with counts per axis.
   - Name the worst issue within each axis.

   **Done when:**
   - [ ] Report has `## Standards` heading.
   - [ ] Report has `## Spec` heading.
   - [ ] Each finding has a file/line reference.
   - [ ] Each finding has a fix.
   - [ ] Counts per axis are listed.
   - [ ] Worst issue per axis is named.

## When NOT to use

- Do not use for a single-file typo fix with no behavior change.
- Do not use when the user asks for a walkthrough, not a review.
