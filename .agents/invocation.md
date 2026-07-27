# Model-invoked vs user-invoked

Every `SKILL.md` in this repo is a skill. The one axis that splits them is **invocation** — who can reach it.

- **User-invoked** — reachable only by the human typing its name. Set `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. The description is human-facing; strip trigger lists.
- **Model-invoked** — reachable by model or user. Omit `disable-model-invocation` and omit the `policy` block from `agents/openai.yaml`. The description is model-facing and keeps rich trigger phrasing like "Use when...".

Every skill carries `agents/openai.yaml` beside `SKILL.md` for Codex/OpenAI UI metadata:

```yaml
interface:
  display_name: "Code Review"
  short_description: "Review a diff on standards and spec"
```

For user-invoked skills, add:

```yaml
policy:
  allow_implicit_invocation: false
```

Keep the two harnesses in sync: a skill is user-invoked in both places or neither.

## Dependencies

Dependencies are prose invocations (`Run the /tdd skill`), not deep links into another skill's private files. Shared reference docs live inside the skill that owns them.
