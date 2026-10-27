---
name: collect-questions
description: Collect interview questions and official sources for a topic before any flashcard is written. Use when the user asks to run collect-questions or to research questions for a technology and version.
---

# Collect questions

Build a source-backed question list. Do not write cards into `content/` during this skill.

## Input

The user names a topic and, when it matters, a version range. Example: Angular v17 through v19.

## Steps

1. Read `CONTENT_SPEC.md` and `content/index.json`. Note questions that already exist so you do not collect duplicates.
2. Read the official docs, release notes, or language specification for that topic. Prefer those over blogs.
3. Keep a question only if you can attach one `https://` URL that a later pass can verify the answer against.
4. Cover beginner, intermediate, and experienced questions. Include version-specific behavior when the version changed the answer.

## Output

Write `content/_inbox/<topic>.questions.md`. Create `content/_inbox/` if it is missing. Use this shape:

```markdown
# Questions: Topic

### short-slug
- level: beginner
- version: v17
- source: https://example.com/official-doc

One sentence an interviewer could say out loud.
```

Do not include answers. Do not mark anything verified. Tell the user the file path and how many questions you collected.
