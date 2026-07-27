# ADR 0001: Bucketed skill pack

## Decision

Store agent skills under `skills/<bucket>/<skill>/` with one `SKILL.md` and one `agents/openai.yaml` per skill.

## Reason

This matches the Agent Skills shape used by Matt Pocock's skills repo while keeping personal dotfile glue separate from promoted reusable workflows.

## Consequences

Promoted skills need README entries, docs pages, and plugin manifest entries. Non-promoted buckets stay out of public/plugin surfaces.
