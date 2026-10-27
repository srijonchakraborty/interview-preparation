---
name: write-card
description: Turn a collected interview-question list into flashcards that follow CONTENT_SPEC.md. Use when the user asks to run write-card or to add cards from content/_inbox.
---

# Write cards

Turn a question list into cards. Leave every new card `unverified`.

## Steps

1. Read `CONTENT_SPEC.md`, `AGENTS.md`, and the topic file you will edit. If the topic is new, add it to `content/index.json` with an `order` array that includes every version you use.
2. Read the inbox list, usually `content/_inbox/<topic>.questions.md`. Skip any slug that already exists in the topic file.
3. Write each card in the topic's `content/<topic>.md` file using the spec. The answer states the rule first and the interview point second. If you are not sure of a sentence, delete it.
4. Set `status: unverified`. Do not upgrade the status in this skill.
5. Run `python scripts/validate_content.py` and fix every reported error.

## Done

Tell the user which file changed, how many cards were added, and that they are unverified until `verify-answers` runs.
