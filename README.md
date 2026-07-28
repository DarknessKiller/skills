# Atlas Skills

An Agent Skills pack shaped after Matt Pocock's [`skills`](https://github.com/mattpocock/skills) design: bucketed skills, explicit invocation rules, a router, per-skill OpenAI metadata, docs pages, Pi package metadata, and a Claude plugin manifest.

## Quickstart

Install into the shared `~/.agents/skills` store only:

```bash
npx -y skills@latest add https://github.com/darknesskiller/skills -g -y --full-depth
```

Update already-installed skills:

```bash
npx -y skills@latest update -g
```

Sync new skills from this repo too:

```bash
npx -y skills@latest add https://github.com/darknesskiller/skills -g -y --full-depth
```

## Why this layout

Skills are small, composable runbooks. User-invoked skills orchestrate workflows; model-invoked skills provide reusable discipline the agent can reach for automatically.

See [`AGENTS.md`](./AGENTS.md) for repository rules and [`CONTEXT.md`](./CONTEXT.md) for the shared vocabulary.

## Reference

### Engineering

Daily code work.

**User-invoked**

- **[ask-atlas](./skills/engineering/ask-atlas/SKILL.md)** — Ask which skill or flow fits your situation.
- **[implement](./skills/engineering/implement/SKILL.md)** — Build scoped work with tests and review.

**Model-invoked**

- **[bitbucket-helper](./skills/engineering/bitbucket-helper/SKILL.md)** — Draft, read, create, and update self-hosted Bitbucket Server/Data Center PRs.
- **[code-review](./skills/engineering/code-review/SKILL.md)** — Review a diff on Standards and Spec as separate axes.
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)** — Keep modules deep and boundaries clean.
- **[creating-worktrees](./skills/engineering/creating-worktrees/SKILL.md)** — Create repo-local Git worktrees under `.worktrees/`.
- **[git](./skills/engineering/git/SKILL.md)** — Keep commits small, conventional, and reviewable.
- **[go](./skills/engineering/go/SKILL.md)** — Write explicit, context-safe Go.
- **[parallel-agents](./skills/engineering/parallel-agents/SKILL.md)** — Fan out independent read and safe write lanes.
- **[pr-writing](./skills/engineering/pr-writing/SKILL.md)** — Draft pull request descriptions from local git history.
- **[tdd](./skills/engineering/tdd/SKILL.md)** — Drive changes with a red-green-refactor loop.

### Productivity

Non-code workflow tools.

**User-invoked**

- None yet.

**Model-invoked**

- None yet.

## Buckets

- [`skills/engineering`](./skills/engineering/README.md)
- [`skills/productivity`](./skills/productivity/README.md)
- [`skills/misc`](./skills/misc/README.md)
- [`skills/personal`](./skills/personal/README.md)
- [`skills/in-progress`](./skills/in-progress/README.md)
- [`skills/deprecated`](./skills/deprecated/README.md)
