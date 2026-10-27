# Agent rules

This repository is a static flashcard site. The app is `index.html`. Cards live in `content/*.md` and are registered in `content/index.json`. Follow `CONTENT_SPEC.md`.

## Change the product, do not replace it

Keep the site static: plain HTML, CSS, and JavaScript, no build step and no dependencies. Progress stays in the browser. Do not add a backend, a framework, or an account system for card review.

## Cards

- Research from the official doc linked on the card. Do not invent APIs, signatures, or release dates.
- A card is `verified` only after its answer has been checked against that source. Anything else is `unverified`.
- Draft in `content/_inbox/`. That folder is gitignored.
- Run `python scripts/validate_content.py` before you finish. It must print `ok`.

## Skills

Use these in order when adding a topic:

1. `agents/skills/collect-questions` gathers questions and sources. It does not write cards into `content/`.
2. `agents/skills/write-card` turns that list into spec-compliant cards marked `unverified`.
3. `agents/skills/verify-answers` checks each answer against its source, then runs the validator.

## Git

Do not commit ignored local notes, secrets, or `_site/`. Do not revert unrelated user changes.
