# Writing SKILL.md files

The skill-specific companion to [`writing-for-agents`](https://github.com/darknesskiller/skills/tree/main/.agents). The universal principles (context pointers, information hierarchy, completion criteria, leading words, pruning) live there. This file adds the format rules that make skills work on weaker models.

## Why a separate format

Weaker models (7B-13B class) lose track of:

- Dense prose with embedded clauses and semicolons.
- Implicit routing that requires semantic matching, not pattern matching.
- Completion criteria buried in a sentence at the end of a paragraph.
- False-positive invocation — firing a skill when the task does not match.
- Multi-step reasoning stated as a single compound instruction.

The format below reduces inference load. Each rule trades prose for structure a weak model can parse deterministically.

## Format rules

### 1. One action per step

Each numbered step is one action. No compound steps joined by semicolons or "then."

Bad:
> Read the current flow before editing, reuse existing helpers, and spawn read-only exploration for broad work.

Good:
> 1. Read the current flow before editing.
> 2. Reuse existing helpers, tests, patterns, and tooling.

### 2. Checklist completion criteria

After each step, state completion as a checklist. A weak model can verify each item. A prose sentence gets skimmed.

Bad:
> Completion: the source of truth, acceptance criteria, constraints, and unresolved risks are explicit.

Good:
> **Done when:**
> - [ ] Source of truth is named.
> - [ ] Acceptance criteria are listed.
> - [ ] Constraints are listed.
> - [ ] Unresolved risks are named or "none" is stated.

### 3. IF/THEN routing for router skills

Router skills use explicit pattern → action tables. A weak model matches patterns; it does not do semantic similarity.

Bad:
> Vague goal or competing approaches → /grilling. Use one question round, then wait.

Good:
> | IF the user... | THEN route to... |
> |---|---|
> | Has a vague goal or competing approaches | `/grilling` — one question round, then wait |
> | Has a concrete goal needing repeated progress | `/goal-loop` |

### 4. "When NOT to use" section

Every model-invoked skill states what it does NOT cover. Weak models over-trigger; an explicit exclusion list prevents false positives.

### 5. Leading words up front

List 2-3 leading words at the top of complex skills. A weak model uses them as anchors.

### 6. One concrete example

For skills with non-obvious input → output, include one concrete example block. Weak models calibrate from examples better than from prose.

### 7. Short sentences

One idea per line. No semicolons joining independent clauses. If a sentence has more than 15 words, split it.

### 8. Max two levels of nesting

No deeply nested sub-bullets. If a step needs sub-items, use a flat list under it, not a sub-list of a sub-list.

### 9. Frontmatter description: front-load the trigger

The description is a context pointer. Front-load the leading word. Keep it under 20 words. One trigger per branch.

### 10. Explicit decision points

Where a step requires a decision, state the branches explicitly:

```
IF <condition A>: do X.
IF <condition B>: do Y.
IF <neither>: ask the user.
```

Not: "Choose the appropriate approach based on context."
