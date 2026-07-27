# Atlas Skills Context

## Language

**Skill bucket**:
A top-level grouping under `skills/` that says whether a skill is daily engineering work, productivity work, personal glue, a draft, or deprecated.

**Promoted skill**:
A skill in `skills/engineering` or `skills/productivity`. Promoted skills are documented, listed in the top README, and shipped by the plugin manifest.

**User-invoked skill**:
A skill only the human can start. It has `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

**Model-invoked skill**:
A reusable discipline the model may reach for automatically. It omits both user-only guards.

**Router**:
A user-invoked skill that helps pick a flow. In this repo, `ask-atlas` is the router.

**Atlas flow**:
The path from understanding a request to verified code: clarify, implement at a seam, test, review, then optionally create a PR.

## Relationships

- A bucket contains skills.
- Promoted skills have README entries, docs pages, and plugin manifest entries.
- User-invoked skills orchestrate.
- Model-invoked skills hold reusable discipline.
- The router mentions every user-reachable flow.
