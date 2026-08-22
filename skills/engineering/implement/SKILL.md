---
name: implement
description: "Build scoped work from a spec, issue, or conversation. Pins contract, builds with feedback, reviews."
disable-model-invocation: true
argument-hint: "What should be implemented?"
---

# Implement

Implement the work the user points at: a spec, an issue, or the current conversation. The main agent owns decisions, edits, verification, and the final report.

## Process

1. **Pin the contract.** Identify the source of truth: spec, issue, diff request, or conversation. List done criteria and constraints. IF the contract is too vague: ask one focused question and wait.

2. **Find the seam.** Read the current flow before editing. Reuse existing helpers, tests, patterns, and tooling. IF the work is broad or risky: spawn read-only exploration before changing files.

3. **Build with feedback.** Use `/tdd` where possible: red test, smallest green, refactor. Work one vertical slice at a time. Run the narrowest useful check after each slice.

4. **Review before finish.** Run the repo's formatter, lint, typecheck, and tests that fit the change. Run `/code-review` when the change is non-trivial. Fix confirmed findings, skip speculative ones.

5. **Close out.** Summarize changed files and checks. Commit only when the user asked; use `/git` rules. IF a PR is needed: use `/bitbucket-helper`.

Completion: changed files, checks, remaining risks, and blocked follow-up are named.

## Stop conditions

Stop when required credentials, external data, destructive actions, or missing acceptance criteria block a safe implementation.

IF the plan is still soft: route to `/grilling` before editing. Keep grilling bounded to decisions that can change the implementation, then wait for confirmation.
