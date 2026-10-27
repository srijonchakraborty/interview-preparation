# Interview Flashcards

A static flashcard app for interview prep, from beginner to experienced developer. Plain HTML, CSS and JavaScript. No build, no dependencies.

Topics: CSS, JavaScript (by ES version), TypeScript, .NET (by version), Angular (by version), AI, RAG, Azure Foundry.

## Open the site
https://srijonchakraborty.github.io/interview-preparation/

The app is `index.html` (HTML, CSS, and JavaScript) plus the decks in `content/`. Nothing to install, and no Python process is part of the site.

Opening `index.html` from the file explorer will not load the decks, because browsers block `fetch` on `file://`. Use the link above.

## Repository
https://github.com/srijonchakraborty/interview-preparation

## Publish
GitHub Pages serves the `main` branch. Push to `main` and the site updates in about a minute.

`scripts/validate_content.py` only checks the card files before a push. It is not the application.

## Structure
```
index.html              the app (HTML, CSS, and JavaScript)
404.html                missing-page redirect
content/index.json      topic list
content/<topic>.md      cards (see CONTENT_SPEC.md)
scripts/validate_content.py   card checker only, not the site
```

## Using the app
- Pick a topic, then a version chip to study only that version.
- Click the card or press Space to flip.
- Mark cards as known or review. Progress is stored in your browser only.
- Cards labelled Unverified have not been checked against official docs yet. Run the `verify-answers` skill.

## Add content with agents
Ask your agent: "Run collect-questions for Angular v17-18, then write-card, then verify-answers."
The first decks are already in `content/`. A card is verified only when its `source` supports the answer. Unverified cards are labelled in the app.
