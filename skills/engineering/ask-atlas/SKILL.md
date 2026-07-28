---
name: ask-atlas
description: Ask which Atlas skill or flow fits your situation. A router over Atlas skills and companion skills installed by the dotfiles.
disable-model-invocation: true
argument-hint: "What are you trying to do?"
---

# Ask Atlas

You don't need to remember every skill. Use this as the map.

This repo owns the Atlas skills. The dotfiles also install Matt Pocock's `/grill-me`, `/grilling`, and `/writing-great-skills` online; reference them, don't copy them here.

A **flow** is a path through skills. User-invoked skills orchestrate; model-invoked skills carry reusable discipline.

## Main flow: request → verified change

1. **`/grill-me`** — when the idea is still soft, stress-test the plan one question at a time before code.
2. **`/implement`** — build scoped work from the current conversation, a spec, or an issue. It keeps ownership in the main agent, uses `/tdd` at seams, runs checks, and closes with `/code-review`.
3. **`/pr-writing`** — when the branch needs a PR body, draft it from the local diff.
4. **`/bitbucket-helper`** — when the branch needs a self-hosted Bitbucket Server/Data Center PR, create or update it through Server REST.

Keep the request, clarifications, and implementation plan in one context window until the work is split enough to hand off. Clear context between independent tickets or worktrees.

## On-ramps

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
- **`/grilling`** — one-question-at-a-time interview primitive behind `/grill-me`.

## Standalone

- **`/grill-me`** — stateless decision-tree interview for any plan.
- **`/writing-great-skills`** — reference for editing this skill pack predictably.
- **`/personal-knowledge`** — search or save personal memory in Blinko.
- **`/pr-writing`** — PR body drafting and refresh from local commits/files.
- **`/bitbucket-helper`** — self-hosted Bitbucket PR reading, creating, and updating.
- **`/creating-worktrees`** — worktree creation without polluting shared ignore rules.
