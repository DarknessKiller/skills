---
name: implement
description: Build scoped work from a spec, issue, or current conversation.
disable-model-invocation: true
argument-hint: "What should be implemented?"
---

# Implement

Implement the work the user points at: a spec, an issue, or the current conversation.

Use the smallest loop that proves the change works. The main agent owns decisions, edits, verification, and the final report.

## Process

1. **Pin the contract**
   - Identify the source of truth: spec, issue, diff request, or conversation.
   - Extract done criteria and constraints.
    - Ask one focused question if the contract is missing enough to make implementation risky.
    - Completion: the source of truth, acceptance criteria, constraints, and unresolved risks are explicit.

2. **Find the seam**
   - Read the current flow before editing.
   - Reuse existing helpers, tests, patterns, and tooling.
    - For broad or risky work, spawn read-only exploration before changing files.
    - Completion: the change seam, affected callers, existing patterns, and relevant checks are known.

3. **Build with feedback**
   - Use `/tdd` where possible: red test, smallest green implementation, refactor.
   - Work one vertical slice at a time.
    - Run the narrowest useful check after each non-trivial slice.
    - Completion: each slice has a passing focused check and the requested behavior is covered.

4. **Review before finish**
   - Run the repo's formatter/lint/typecheck/tests that fit the change.
   - Run `/code-review` on the diff when the change is non-trivial.
    - Fix confirmed findings; do not chase speculative ones.
    - Completion: applicable formatter, lint, typecheck, tests, and review findings are resolved or reported.

5. **Close out**
   - Summarize changed files and checks.
   - Commit only when the user asked the flow to finish with a commit; use `/git` rules.
    - If a PR is needed for Bitbucket Server/Data Center or Cloud, use `/bitbucket-helper`.
    - Completion: the final report names changed files, checks, remaining risks, and any blocked follow-up.

## Stop conditions

Stop and report when required credentials, external data, destructive actions, or missing acceptance criteria block a safe implementation.

When the plan is still soft, route to `/grilling` before editing. Keep grilling bounded to decisions that can change the implementation, then wait for confirmation.
