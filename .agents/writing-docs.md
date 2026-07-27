# Writing docs pages

Every promoted skill has a docs page at `docs/<bucket>/<skill-name>.md`. The docs page is not a copy of `SKILL.md`; it helps a human remember when to reach for the skill.

Use this frame:

```markdown
Quickstart:

\`\`\`bash
npx skills add https://github.com/darknesskiller/skills --skill=<name>
\`\`\`

\`\`\`bash
npx skills update <name>
\`\`\`

[Source](https://github.com/darknesskiller/skills/tree/main/skills/<bucket>/<name>)

## What it does

## When to reach for it

## Prerequisites

## <free-form middle>

## It's working if

## Where it fits
```

Rules:

- No H1; the publishing layer owns the title.
- Always include Quickstart, Source, What it does, When to reach for it, and Where it fits.
- Include Prerequisites only when the skill needs setup.
- Use absolute links.
- Explain why and boundaries, not the whole runbook.
- When a promoted skill changes behaviour, update its docs page in the same change.
