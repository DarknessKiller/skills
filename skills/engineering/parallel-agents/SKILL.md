---
name: parallel-agents
description: "Fan out independent read and write lanes. Use for broad discovery, multi-axis review, or non-overlapping edits."
---

# Parallel Agents

Fan out every useful independent lane. The main agent owns decisions, synthesis, cross-seam edits, verification, and the final report.

## Process

1. **Slice lanes.** Prefer read-only lanes first: one agent per independent question, directory, package, axis, or search space. A lane is useful only if it has a unique scope and its answer can change the next action. Launch concurrently when the harness supports it.

2. **Prompt tightly.** Give each agent its lane, read/write mode, allowed paths, forbidden paths, and expected output shape. Read lanes: ask for file:line evidence, commands run, short answer. Write lanes: state exact files/dirs they may modify and the check they must run.

3. **Write only when non-overlapping.** Use write agents only for fixed-contract, non-overlapping file sets. IF two lanes might touch the same file, shared type, migration, config, generated output, or public API: keep sequential or in main thread. Use isolated worktrees for risky parallel writes.

4. **Keep moving.** While background agents run: do local reading, planning, or small safe edits. Do not poll or sleep; wait only when their result is needed.

5. **Integrate.** Read returned summaries. For writers: verify actual diffs before trusting. Resolve seams in main thread. Run the narrowest useful check that covers the integrated change.

## Guardrails

- No duplicate lanes, no agents for one-line lookups.
- Never delegate ownership: no "research and then fix whatever you find" prompts.
- Prefer more read agents over more write agents. Reads can overlap; writes cannot.
