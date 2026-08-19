Quickstart:

```bash
npx skills add https://github.com/darknesskiller/skills --skill=parallel-agents
```

```bash
npx skills update parallel-agents
```

[Source](https://github.com/darknesskiller/skills/tree/main/skills/engineering/parallel-agents)

## What it does

`parallel-agents` makes the agent fan out every useful independent lane instead of reading or reviewing broad work serially.

It prefers read-only agents, then allows write agents only when their file sets and API decisions cannot overlap. It describes concurrency in harness-neutral terms and leaves the actual launch mechanism to the runtime.

## When to reach for it

Reach for it when a task has independent questions, directories, review axes, packages, or mechanical edits. It also fits explicit requests to use many sub-agents.

Do not use it for one-line lookups or edits that all converge on the same file or public API.

## Fan-out discipline

The main agent keeps ownership. Sub-agents gather evidence or make bounded non-overlapping edits; the main thread integrates, verifies diffs, and reports.

Read lanes should return file:line evidence and short answers. Write lanes need exclusive paths and a runnable check.

## It's working if

- Multiple read lanes start together for broad discovery.
- Write lanes only touch exclusive paths.
- The final answer separates findings, integrated changes, and checks.
- Each lane has a unique scope and a checkable completion result.

## Where it fits

Use this inside [implement](https://github.com/darknesskiller/skills/tree/main/skills/engineering/implement) when the discovery or edits split cleanly. It complements [code-review](https://github.com/darknesskiller/skills/tree/main/skills/engineering/code-review), which already splits Standards and Spec review axes.
