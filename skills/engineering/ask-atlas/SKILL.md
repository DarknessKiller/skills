---
name: ask-atlas
description: Ask which Atlas skill or flow fits your situation. A router over Atlas skills and companion skills installed by the dotfiles.
disable-model-invocation: true
argument-hint: "What are you trying to do?"
---

# Ask Atlas

You don't need to remember every skill. Use this as the map.

This repo owns the Atlas skills. Additional skills may be installed in the system — reference them by name, don't copy them here.

A **flow** is a path through skills. User-invoked skills orchestrate; model-invoked skills carry reusable discipline.

## Main flow: request → verified change

1. **Stress-test the idea** — when the outcome, scope, or acceptance criteria are soft, use `/grilling` for one frontier round at a time. Ask the user, recompute the next frontier after each answer, and do not act until the contract is confirmed.
2. **`/implement`** — build scoped work from the current conversation, a spec, or an issue. It keeps ownership in the main agent, uses `/tdd` at seams, runs checks, and closes with `/code-review`.
3. **`/pr-writing`** — when the branch needs a PR body, draft it from the local diff.
4. **`/bitbucket-helper`** — when the branch needs a Bitbucket Server/Data Center or Cloud PR, create or update it through the appropriate REST API.

The bounded grilling rule is simple: clarify only decisions that can change the next action; once the contract is confirmed, stop grilling and route.

Keep the request, clarifications, and implementation plan in one context window until the work is split enough to hand off. Clear context between independent tickets or worktrees.

## On-ramps

- **Vague goal or competing approaches** → **`/grilling`**. Use one question round, then wait for answers before changing files.
- **Need to build or fix code** → **`/implement`**. It owns the verified change.
- **Need a review** → **`/code-review`**. It discovers the comparison point and reports Standards and Spec separately.
- **Need a PR description or mutation** → **`/pr-writing`**, then **`/bitbucket-helper`** when the remote is Bitbucket.
- **Need isolation** → **`/creating-worktrees`**. Create a repo-local `.worktrees/<slug>-<timestamp>` workspace before touching risky or parallel work.
- **Broad independent work** → **`/parallel-agents`**. Fan out read-only lanes first; use write lanes only when paths cannot overlap.
- **Something needs design pressure** → **`/codebase-design`**. Use the deep-module vocabulary before changing boundaries: handlers stay thin, services hold business logic, repositories persist.
- **Go code** → **`/go`**. Apply context propagation, explicit dependencies, standard-library-first choices, wrapped errors, and tests.
- **Git workflow** → **`/git`**. Use small diffs, Conventional Commits, and `git commit --no-gpg-sign`.

## Reusable disciplines underneath

- **`/tdd`** — red-green-refactor at the smallest useful seam.
- **`/code-review`** — two-axis review: Standards and Spec, kept separate.
- **`/codebase-design`** — module shape, boundaries, and depth.
- **`/go`** — Go-specific implementation rules.
- **`/parallel-agents`** — independent read lanes and safe non-overlapping write lanes.
- **`/pr-writing`** — standard PR description shape from local git history.
- **`/git`** — commit and branch hygiene.

## Routing boundaries

- Route only; do not implement, edit, or create a PR from this skill.
- If the request is already a confirmed implementation contract, skip grilling and route directly to `/implement`.
- If the user asks only for advice, return the smallest useful route and stop.

## Standalone

- **`/personal-knowledge`** — search or save personal memory in Blinko.
- **`/pr-writing`** — PR body drafting and refresh from local commits/files.
- **`/bitbucket-helper`** — Bitbucket Server/Data Center and Cloud PR reading, creating, and updating.
- **`/creating-worktrees`** — worktree creation without polluting shared ignore rules.

## External skills

Skills from other sources (e.g. Matt Pocock's collection) may be installed in the system. Use them by name — don't duplicate their definitions here.
