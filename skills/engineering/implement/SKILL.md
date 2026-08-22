---
name: implement
description: "Build scoped work from a spec, issue, or conversation."
disable-model-invocation: true
argument-hint: "What should be implemented?"
---

# Implement

## Steps

1. **Pin contract.** Identify source of truth: spec, issue, conversation. List done criteria. Too vague: ask one question, wait.

2. **Find seam.** Read current flow before editing. Reuse helpers, tests, patterns. Broad or risky: explore before changing files.

3. **Build with feedback.** Use `/tdd` where possible. One vertical slice at a time. Narrowest useful check after each.

4. **Review.** Run formatter, lint, typecheck, tests. `/code-review` for non-trivial changes. Fix confirmed findings only.

5. **Close out.** Summarize changed files and checks. Commit only when asked. `/git` rules. PR needed: `/bitbucket-helper`.

## Blocked

If context missing, state plan before asking: source of truth, done criteria, seam, callers, passing check, review command, changed files.

Completion: changed files, checks, risks, blocked follow-up named.
