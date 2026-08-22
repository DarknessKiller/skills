# Writing SKILL.md files

The skill-specific companion to [`writing-for-agents`](https://github.com/darknesskiller/skills/tree/main/.agents). The universal principles (context pointers, information hierarchy, completion criteria, leading words, pruning) live there. This file adds the format rules that make skills work on weaker models.

## Why a separate format

Weaker models (7B-13B class) lose track of:

- Long content — attention thins across excess tokens, even when every line is live.
- Implicit routing that requires semantic matching, not pattern matching.
- Completion criteria buried in a sentence at paragraph end.
- False-positive invocation — firing a skill when the task does not match.
- Multi-step reasoning stated as a single compound instruction.

The format below reduces inference load. Each rule trades prose for structure a weak model can parse deterministically — but every rule is budgeted against length, because length itself is the dominant cost on weak models.

## Format rules

### 1. Shortest content wins

Length is the dominant cost on weak models. Every additional word thins attention. Before adding structure, cut words. A shorter skill with less structure beats a longer skill with more structure. Benchmark this: if a structural addition does not measurably improve the target metric, cut it.

### 2. One action per step

Each numbered step is one action. No compound steps joined by semicolons or "then."

### 3. One-line completion criteria

After a step or group of steps, state completion as one sentence. Do not use `[ ]` checklists — they add length and weak models do not reproduce them in output, so they score nothing and cost tokens.

### 4. Routing tables for router skills

Router skills use explicit pattern → action tables. A weak model matches patterns; it does not do semantic similarity. The table replaces prose on-ramps and is shorter.

### 5. Inline conditionals, not IF/THEN blocks

For decision points within steps, use inline format: "existing branch: `git worktree add <path> <branch>`; new branch: `git worktree add -b <branch> <path>`." IF/THEN blocks add tokens and decision load. Reserve IF/THEN for routing tables and one-line guards only.

### 6. Frontmatter description: front-load the trigger

The description is a context pointer. Front-load the leading word. Keep it under 20 words. One trigger per branch.

### 7. Short sentences

One idea per line. No semicolons joining independent clauses. If a sentence has more than 15 words, split it.

### 8. Max two levels of nesting

No deeply nested sub-bullets. If a step needs sub-items, use a flat list or inline format.

### 9. No "When NOT to use" sections unless they fix a measured false-positive

Weaker models over-trigger, but a "When NOT to use" section adds length. Only add one when a benchmark shows it reduces false-positive rate. Otherwise the length cost outweighs the guard.

### 10. Benchmark before and after

Every format change should be benchmarked with `bench/run_bench.py` on at least one weak model. If the new format does not beat the old format on the target metrics, cut structure until it does.
