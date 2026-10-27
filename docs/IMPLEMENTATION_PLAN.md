# Implementation plan

The product is the static flashcard site described in `README.md`: one `index.html`, Markdown decks in `content/`, progress in the browser, and GitHub Pages. This plan records what was missing in the starter commit and what remains.

## 1. App shell

- Objective: open a topic, filter by version, flip a card, and mark it known or review.
- Started from: `README.md`, `404.html`, and a root `pages.yml`. No `index.html`.
- Implementation: `index.html` loads `content/index.json`, parses `CONTENT_SPEC.md` cards, and stores marks in `localStorage` under `interview-prep.v1`.
- Acceptance: topic list, version chips, flip, known, review, shuffle, reset, and export/import work over `python -m http.server`. `file://` shows a server hint.
- Status: implemented. `scripts/validate_content.py` passes. Headless Chrome loaded the topic list, flipped a CSS card, marked it known, filtered to Modern and to ES2024, and showed the saved mark on the topic list.

## 2. Decks

- Objective: real questions for CSS, JavaScript, TypeScript, .NET, Angular, AI, RAG, and Azure Foundry, with a version chip where the version changes the answer.
- Started from: no `content/` files. The README said card content was not included.
- Implementation: eight topic files plus `content/index.json`. A card is `verified` only when its `source` URL was opened and the answer was trimmed to that page.
- Acceptance: `python scripts/validate_content.py` prints `ok`. Every version used on a card is listed in that topic's `order`.
- Status: first deck is in place and verified against the linked docs. It is a starter set, not a complete interview corpus. More cards go through the skills below.

## 3. Content workflow

- Objective: add cards without inventing APIs.
- Implementation: `CONTENT_SPEC.md`, `AGENTS.md`, and `agents/skills/collect-questions`, `write-card`, and `verify-answers`. Drafts stay in `content/_inbox/`, which is gitignored.
- Acceptance: a new card fails validation until it has the required fields and one `---` separator.
- Status: skills and validator are in place. They have not been run as a second content pass yet.

## 4. Publish

- Objective: GitHub Pages deploys only a deck that validates.
- Started from: `pages.yml` in the repo root. The README said to move it before the first deploy.
- Implementation: `.github/workflows/pages.yml` runs the validator, then publishes `index.html`, `404.html`, `.nojekyll`, and `content/`.
- Acceptance: the workflow file is in `.github/workflows/`, and the validator exits 0 locally.
- Status: workflow is moved. The GitHub Pages source still has to be set to GitHub Actions in the repository settings. That setting is not in git.

## 5. Later, only if the static app is holding up

- Spaced repetition beyond known/review.
- More cards per version, still through collect, write, and verify.
- A browser test that clicks flip, known, and the version chips.

Do not add a backend, a login, or a model runtime. The study loop is the static site. Agents improve the decks. They are not a service inside the page.
