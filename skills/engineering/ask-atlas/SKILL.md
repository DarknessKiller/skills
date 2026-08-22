---
name: ask-atlas
description: "Router over Atlas skills. Tell it your situation; it names the next skill to run."
disable-model-invocation: true
argument-hint: "What are you trying to do?"
---

# Ask Atlas

This is the map. You do not need to remember every skill.

A **flow** is a path through skills. User-invoked skills orchestrate. Model-invoked skills carry reusable discipline.

This repo owns the Atlas skills. Other skills may be installed in the system. Reference them by name. Do not copy them here.

## Main flow: request to verified change

Follow these steps in order. Skip a step only when its IF condition is false.

1. **Stress-test the idea.**
   - IF the outcome, scope, or acceptance criteria are soft: use `/grilling`.
   - Ask one question round. Wait for the answer.
   - Recompute the next question after each answer.
   - Do not act until the contract is confirmed.

2. **Run the goal loop.**
   - IF one pass is unlikely to finish the goal: use `/goal-loop`.
   - It bounds action, verification, and internal critique.

3. **Implement.**
   - Use `/implement` to build scoped work.
   - It keeps ownership in the main agent.
   - It uses `/tdd` at seams, runs checks, and closes with `/code-review`.

4. **Draft the PR body.**
   - IF the branch needs a PR body: use `/pr-writing`.

5. **Create or update the PR.**
   - IF the remote is Bitbucket: use `/bitbucket-helper`.

**Done when:**
- [ ] The user's request is matched to a skill or flow.
- [ ] The next action is named.
- [ ] You have not implemented, edited, or created a PR from this skill.

## Routing table

| IF the user... | THEN route to... |
|---|---|
| Has a vague goal or competing approaches | `/grilling` — one question round, then wait |
| Has a concrete goal needing repeated verified progress | `/goal-loop` — default 5 rounds |
| Needs to build or fix code | `/implement` |
| Needs a review of a diff | `/code-review` |
| Needs a PR description | `/pr-writing` |
| Needs a Bitbucket PR created or updated | `/bitbucket-helper` |
| Needs isolation before risky or parallel work | `/creating-worktrees` |
| Has broad independent work to fan out | `/parallel-agents` — read lanes first, write lanes only when paths do not overlap |
| Needs design pressure on boundaries | `/codebase-design` |
| Is writing Go code | `/go` |
| Needs commit hygiene | `/git` |
| Needs to search or save personal memory | `/personal-knowledge` |

## Reusable disciplines

These are model-invoked. The agent reaches for them automatically.

- `/tdd` — red-green-refactor at the smallest useful seam.
- `/code-review` — two-axis review: Standards and Spec, kept separate.
- `/codebase-design` — module shape, boundaries, and depth.
- `/go` — Go-specific implementation rules.
- `/parallel-agents` — independent read lanes and safe non-overlapping write lanes.
- `/pr-writing` — standard PR description shape from local git history.
- `/git` — commit and branch hygiene.

## When NOT to use

- Do not implement, edit, or create a PR from this skill. Route only.
- IF the request is already a confirmed implementation contract: skip grilling and route directly to `/implement`.
- IF the user asks only for advice: return the smallest useful route and stop.

## Context management

- Keep the request, clarifications, and implementation plan in one context window until the work is split.
- Clear context between independent tickets or worktrees.
