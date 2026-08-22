---
name: implement
description: "Build scoped work from a spec, issue, or conversation. Pins contract, builds with feedback, reviews."
disable-model-invocation: true
argument-hint: "What should be implemented?"
---

# Implement

Implement the work the user points at: a spec, an issue, or the current conversation. The main agent owns decisions, edits, verification, and the final report.

## Process

1. **Pin the contract.**
   - Identify the source of truth: spec, issue, diff request, or conversation.
   - List the done criteria.
   - List the constraints.
   - IF the contract is too vague to implement safely: ask one focused question. Wait for the answer.

   **Done when:**
   - [ ] Source of truth is named.
   - [ ] Done criteria are listed.
   - [ ] Constraints are listed.
   - [ ] Unresolved risks are named or "none" is stated.

2. **Find the seam.**
   - Read the current flow before editing.
   - Reuse existing helpers, tests, patterns, and tooling.
   - IF the work is broad or risky: spawn read-only exploration before changing files.

   **Done when:**
   - [ ] Change seam is identified.
   - [ ] Affected callers are listed.
   - [ ] Existing patterns are named.
   - [ ] Relevant checks are known.

3. **Build with feedback.**
   - Use `/tdd` where possible: red test, smallest green, refactor.
   - Work one vertical slice at a time.
   - Run the narrowest useful check after each slice.

   **Done when:**
   - [ ] Each slice has a passing focused check.
   - [ ] The requested behavior is covered.

4. **Review before finish.**
   - Run the repo's formatter, lint, typecheck, and tests that fit the change.
   - Run `/code-review` on the diff when the change is non-trivial.
   - Fix confirmed findings. Skip speculative ones.

   **Done when:**
   - [ ] Formatter passed or not applicable.
   - [ ] Lint passed or not applicable.
   - [ ] Typecheck passed or not applicable.
   - [ ] Tests passed or not applicable.
   - [ ] Review findings are resolved or reported.

5. **Close out.**
   - Summarize changed files and checks.
   - IF the user asked for a commit: use `/git` rules.
   - IF a PR is needed for Bitbucket: use `/bitbucket-helper`.

   **Done when:**
   - [ ] Changed files are listed.
   - [ ] Checks are summarized.
   - [ ] Remaining risks are named.
   - [ ] Blocked follow-up is named or "none" is stated.

## Stop conditions

Stop and report when:
- Required credentials are missing.
- External data is missing.
- A destructive action is needed without authorization.
- Acceptance criteria are missing and cannot be inferred.

## When the plan is soft

IF the plan is still soft: route to `/grilling` before editing. Keep grilling bounded to decisions that can change the implementation. Wait for confirmation.
