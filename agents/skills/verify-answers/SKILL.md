---
name: verify-answers
description: Check flashcard answers against their official sources and mark only the supported ones verified. Use when the user asks to run verify-answers or to check cards against the docs.
---

# Verify answers

Confirm each answer against the card's `source` URL. Do not treat a fluent answer as a checked one.

## Steps

1. Read `CONTENT_SPEC.md` and the topic file the user named. If they did not name one, verify cards whose status is `unverified`.
2. Open the `source` URL. Check the version, the API names, and the behavior the answer claims.
3. If the source supports the answer, set `status: verified`. If a sentence is wrong, fix it from the source or delete it. If you cannot open the source, leave `status: unverified` and say so.
4. Do not add a fact the page does not support. Do not swap in a blog post to make a weak answer look verified.
5. Run `python scripts/validate_content.py`. It must print `ok`.

## Done

Report how many cards are verified, how many stayed unverified, and which claims you changed.
