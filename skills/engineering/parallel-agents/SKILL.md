---
name: parallel-agents
description: "Fan out independent read and write lanes. Use for broad discovery, multi-axis review, or non-overlapping edits."
---

# Parallel Agents

Fan out every useful independent lane. The main agent owns decisions, synthesis, cross-seam edits, verification, and the final report.

## Process

1. **Slice lanes.**
   - Prefer read-only lanes first: one agent per independent question, directory, package, reviewer axis, or search space.
   - A lane is useful only IF it has a unique scope AND its answer can change the next action.
   - IF lanes are independent: launch them concurrently when the harness supports it.

   **Done when:**
   - [ ] Every independent unknown has a lane.
   - [ ] Each lane has a unique scope.

2. **Prompt tightly.**
   - Give each agent its lane, read/write mode, allowed paths, and forbidden paths.
   - For read lanes: ask for file:line evidence, commands run, and a short answer.
   - For write lanes: state exact files or dirs they may modify and the check they must run.

   **Done when:**
   - [ ] Another agent could not accidentally work the same lane.

3. **Write only when non-overlapping.**
   - Use write agents only for fixed-contract, non-overlapping file sets.
   - IF two lanes might touch the same file, shared type, migration, config, generated output, or public API: keep them sequential or in the main thread.
   - Use isolated worktrees for risky parallel writes.

   **Done when:**
   - [ ] Each write agent has exclusive paths.
   - [ ] No shared API decision is split across agents.

4. **Keep moving.**
   - While background agents run: do local reading, planning, or small safe edits.
   - Do NOT poll or sleep. Wait only when their result is needed.

   **Done when:**
   - [ ] Main-thread work cannot invalidate a running lane.

5. **Integrate.**
   - Read returned summaries.
   - For writers: verify actual diffs before trusting them.
   - Resolve seams in the main thread.
   - Run the narrowest useful check that covers the integrated change.

   **Done when:**
   - [ ] Agent findings and integrated changes are separated in the report.
   - [ ] Checks are named.

## Guardrails

- No duplicate lanes.
- No agents for one-line lookups.
- Never delegate ownership: no "research and then fix whatever you find" prompts.
- Prefer more read agents over more write agents. Reads can overlap. Writes cannot.
