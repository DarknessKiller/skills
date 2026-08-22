---
name: parallel-agents
description: "Fan out independent read and write lanes. Use for broad discovery, multi-axis review, or non-overlapping edits."
---

# Parallel Agents

Fan out independent lanes. Main agent owns decisions, synthesis, report.

## Steps

1. **Slice lanes.** Read-only first: one agent per independent question, directory, package, axis. Launch concurrently.

2. **Prompt tightly.** Give each agent: lane, read/write mode, allowed paths, forbidden paths, expected output shape.

3. **Write only when non-overlapping.** Fixed-contract, non-overlapping file sets. IF two lanes might touch same file: keep sequential.

4. **Keep moving.** While agents run: do local reading, planning, small safe edits. Do not poll.

5. **Integrate.** Read summaries. For writers: verify diffs. Resolve seams in main thread. Run narrowest useful check.

## Rules

- No duplicate lanes. No agents for one-line lookups.
- Never delegate ownership.
- Prefer more read agents over more write agents.
