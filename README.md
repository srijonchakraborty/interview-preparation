# Interview Flashcards

A static flashcard app for interview prep, from beginner to experienced developer. Plain HTML, CSS and JavaScript. No build, no dependencies.

Topics: CSS, JavaScript (by ES version), TypeScript, .NET (by version), Angular (by version), AI, RAG, Azure Foundry.

## Run locally
```
python -m http.server 8000
```
Open http://localhost:8000. Opening `index.html` directly will not work because browsers block `fetch` on `file://`.

## Repository
https://github.com/srijonchakraborty/interview-preparation

## Publish on GitHub Pages (free)
1. On GitHub open Settings, Pages, and under Build and deployment set Source to **GitHub Actions**.
2. Open the Actions tab. The workflow "Deploy to GitHub Pages" runs on every push to `main`.
3. When it is green, the site is at `https://srijonchakraborty.github.io/interview-preparation/`.

Notes
- Free accounts can publish Pages from public repositories only.
- `pages.yml` is the Pages workflow. Move it to `.github/workflows/pages.yml` before the first deploy. It checks that every file in `content/index.json` exists, then publishes `index.html` and `content/`.
- Add cards by editing a `content/*.md` file and pushing. The site updates in about a minute.
- If the site is blank, press Ctrl+Shift+R. If it is a 404, confirm Pages source is GitHub Actions.

## Structure
```
index.html              the whole app
content/index.json      topic list
content/<topic>.md      cards (see CONTENT_SPEC.md)
AGENTS.md               rules for AI agents
agents/skills/          collect-questions, write-card, verify-answers
```

## Using the app
- Pick a topic, then a version chip to study only that version.
- Click the card or press Space to flip.
- Mark cards as known or review. Progress is stored in your browser only.
- Cards labelled Unverified have not been checked against official docs yet. Run the `verify-answers` skill.

## Add content with agents
Ask your agent: "Run collect-questions for Angular v17-18, then write-card, then verify-answers."
This repository is the base project. Card content is not included yet.
