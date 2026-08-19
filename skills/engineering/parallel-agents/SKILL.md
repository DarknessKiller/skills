---
name: parallel-agents
description: "Use when work has independent questions, files, axes, or packages that can be delegated in parallel; especially broad read-only discovery, multi-axis review, safe non-overlapping edits, or explicit requests to spin up many sub-agents."
---

# Parallel Agents

Fan out every useful independent lane. The main agent owns decisions, synthesis, cross-seam edits, verification, and the final report.

## Process

1. **Slice lanes**
   - Prefer read-only lanes first: one agent per independent question, directory, package, reviewer axis, or search space.
   - A lane is useful only if it has a unique scope and its answer can change the next action.
    - If lanes are independent, launch them concurrently when the current harness supports concurrent work. Use that harness's native mechanism; do not assume a tool-specific flag.
    - Completion: every independent unknown has a lane or an explicit reason to stay in the main thread.

2. **Prompt tightly**
   - Give each agent its lane, read/write mode, allowed paths, forbidden paths, and expected output shape.
   - For read lanes, ask for file:line evidence, commands run, and a short answer.
   - For write lanes, state exact files or dirs they may modify and the check they must run.
   - Completion: another agent could not accidentally work the same lane from the prompt.

3. **Write only when non-overlapping**
   - Use write agents only for fixed-contract, non-overlapping file sets.
   - If two lanes might touch the same file, shared type, migration, config, generated output, or public API, keep them sequential or in the main thread.
   - Use isolated worktrees for risky parallel writes.
   - Completion: each write agent has exclusive paths and no shared API decision.

4. **Keep moving**
   - While background agents run, do local reading, planning, or small safe edits.
   - Do not poll or sleep; wait only when their result is needed.
   - Completion: main-thread work cannot invalidate a running lane.

5. **Integrate**
   - Read returned summaries; for writers, verify actual diffs before trusting them.
   - Resolve seams in the main thread.
   - Run the narrowest useful check that covers the integrated change.
   - Completion: the final answer separates agent findings, integrated changes, and checks.

## Guardrails

- Maximize useful parallelism, not noise: no duplicate lanes, no agents for one-line lookups.
- Never delegate ownership: no "research and then fix whatever you find" prompts.
- Prefer more read agents over more write agents. Reads can overlap; writes cannot.
