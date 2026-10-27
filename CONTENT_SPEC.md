# Card format

Each topic is one UTF-8 Markdown file registered in `content/index.json`. The site and `scripts/validate_content.py` both use this format. A card is a `###` heading. The workflow counts those headings, so do not use `###` anywhere else.

```markdown
# Topic title

### card-id
- title: Short card title
- version: ES2020
- level: beginner
- status: verified
- source: https://example.com/official-doc

Question text. `code` and **bold** are safe. Blank lines split paragraphs. Lines that start with "- " become a list.

---

Answer text. State the rule, then the interview point. Do not put a line that is only --- in the answer.
```

## Fields

| Field | Rule |
| --- | --- |
| id | Heading text. Lowercase letters, digits, and single hyphens. Unique inside the file. |
| title | Plain text shown on the card. |
| version | Chip label. Must be listed in that topic's `order` array in `content/index.json`. |
| level | `beginner`, `intermediate`, or `experienced`. |
| status | `verified` only after the answer was checked against `source`. Otherwise `unverified`. |
| source | One `https://` URL to an official or primary document. |

`index.json` entries require `id`, `title`, `file`, `summary`, and `order`. `file` is a repo-root path such as `content/css.md`.

## Writing rules

- Prefer the official docs over a blog post. Name the version when behavior changed.
- Do not invent APIs, signatures, or release dates. If the source does not support a sentence, delete the sentence or mark the card `unverified`.
- Keep the question to something an interviewer can ask out loud. Put the precise rule in the answer.
- The app escapes card text. A code sample may contain tags such as `<div>`. Do not use HTML for formatting. Use paragraphs, `- ` lists, `` `code` ``, and fenced code blocks.
- Drafts belong in `content/_inbox/`, which is gitignored. Move a card into `content/` only when it follows this spec.
