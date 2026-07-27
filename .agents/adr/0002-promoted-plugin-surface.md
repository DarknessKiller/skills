# ADR 0002: Promoted skills are the plugin surface

## Decision

`.claude-plugin/plugin.json` lists only `skills/engineering/*` and `skills/productivity/*`.

## Reason

The plugin should install stable daily workflows, not drafts, owner-only glue, or deprecated experiments.

## Consequences

Adding or moving a promoted skill requires updating the plugin manifest, README, bucket README, docs page, and `ask-atlas` when it changes a user-reachable flow.
