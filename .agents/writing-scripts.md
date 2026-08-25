# Writing scripts for skills

How bundled helper scripts must be referenced and built so they work when the pack is installed flat (via `npx skills`) and when it is run from the repo root. Follows [agentskills using-scripts](https://github.com/agentskills/agentskills/blob/main/docs/skill-creation/using-scripts.mdx).

## Referencing scripts from SKILL.md

Use **relative paths from the skill directory root**. The harness resolves these automatically. Never use repo-relative paths (`skills/engineering/<name>/scripts/...`) — they break when the pack is installed to `~/.agents/skills/<name>/` or `<project>/.agents/skills/<name>/`, where the layout is flat.

- Bad: `python3 skills/engineering/pr-writing/scripts/pr_writer.py`
- Good: `python3 <skill-dir>/scripts/pr_writer.py` (the skill dir is where this SKILL.md lives)

List available scripts so the agent knows they exist:

```markdown
## Available scripts

- `scripts/validate.sh` — Validates configuration files
- `scripts/process.py` — Processes input data
```

Then instruct the agent to run them:

````markdown
## Workflow

1. Run the validation script:
   ```bash
   python3 <skill-dir>/scripts/validate.sh "$INPUT_FILE"
   ```
````

The same relative-path convention works in support files like `references/*.md`. Script execution paths are relative to the skill directory root.

## One-off commands

When an existing package already does what you need, reference it directly with a pinned version instead of bundling a script:

```bash
uvx ruff@0.8.0 check .
npx eslint@9 --fix .
go run golang.org/x/tools/cmd/goimports@v0.28.0 .
```

State prerequisites in `SKILL.md` ("Requires Node.js 18+"). When a command grows complex, move it into a tested `scripts/` file.

## Self-contained scripts

Bundle reusable logic in `scripts/` with inline dependencies, so the agent runs one command with no install step:

- Python: PEP 723 inline metadata, run with `uv run scripts/extract.py` or `pipx run scripts/extract.py`.
- Deno: `npm:`/`jsr:` import specifiers, run with `deno run scripts/extract.ts`.
- Bun: auto-installs pinned imports, run with `bun run scripts/extract.ts`.
- Ruby: `bundler/inline`, run with `ruby scripts/extract.rb`.

Pin versions. Prefer stdlib when it is enough.

## Designing scripts for agentic use

- **No interactive prompts.** Agents run non-interactive shells. Take all input via flags, env vars, or stdin. Fail with a clear error naming the missing flag and its options.
- **`--help` documents the interface.** Brief description, flags, examples. Concise — the output enters the agent's context.
- **Helpful errors.** Say what went wrong, what was expected, what to try next.
- **Structured output.** JSON/CSV/TSV on stdout; diagnostics to stderr. Data and diagnostics never mixed.
- **Idempotent.** Retries are normal; "create if not exists" over "fail on duplicate".
- **Dry-run and safe defaults.** Destructive operations need explicit confirm flags.
- **Meaningful exit codes.** Distinct codes for not-found vs invalid-args vs auth; document them in `--help`.
- **Bounded output.** Default to summaries; support `--limit`, `--offset`, or `--output` for large results.

## Cross-skill script imports

When one skill's script imports another skill's helper (e.g. `bitbucket-helper` imports `pr-writing`'s `pr_writer`), resolve via `Path(__file__).resolve().parents[N]` so it works in both the flat installed layout (siblings under `~/.agents/skills/`) and the repo layout (`skills/engineering/...` siblings). Never hardcode a repo-relative path inside a script.

## Verification

`npm run check` runs the CLI contract tests. When you add or change a script referenced from a `SKILL.md`, re-run the check and, for the affected skill, run the helper from a directory that is not the pack root to prove the relative path resolves.
