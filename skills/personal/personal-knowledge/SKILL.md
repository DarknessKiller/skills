---
name: personal-knowledge
description: "Search or save personal memory in Blinko. Use for notes, memories, bookmarks, reminders, owner preferences."
---

# Personal Knowledge

Use Blinko as the personal memory layer.

## Workflow

1. **Search first.**
   - Search Blinko with the user's terms and likely synonyms.
   - This prevents duplicate notes.

2. **Report findings.**
   - Summarize only personal facts supported by Blinko.
   - IF nothing matched: say so.

3. **Save if asked.**
   - IF the user asks to remember something: save one concise Blinko note.
   - Use `type: todo` only for tasks.
   - Otherwise: default to `blinko` unless a structured note is clearly better.

**Done when:**
- [ ] Search result is supported by Blinko or "nothing matched" is stated.
- [ ] Duplicate-saving was avoided.
- [ ] Any written note or ambiguity is named.

## Response shape

Include:
- What personal memory found.
- Whether a Blinko note was written.
- Any ambiguity.
