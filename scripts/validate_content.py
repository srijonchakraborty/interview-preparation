"""Validate flashcard content and the static app shell."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "content" / "index.json"
LEVELS = {"beginner", "intermediate", "experienced"}
STATUSES = {"verified", "unverified"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
META_KEYS = {"title", "version", "level", "status", "source"}


def fail(errors):
    for error in errors:
        print(error, file=sys.stderr)
    sys.exit(1)


def parse_cards(text, path):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    errors = []
    if text.startswith("\ufeff"):
        errors.append(f"{path}: unexpected BOM")
    parts = re.split(r"(?m)^### ", text)
    cards = []
    for part in parts[1:]:
        lines = part.split("\n")
        card_id = lines[0].strip()
        meta = {}
        i = 1
        while i < len(lines) and lines[i].startswith("- "):
            raw = lines[i][2:]
            if ":" not in raw:
                errors.append(f"{path}: {card_id}: metadata line needs a colon")
                i += 1
                continue
            key, value = raw.split(":", 1)
            meta[key.strip()] = value.strip()
            i += 1
        if i < len(lines) and lines[i].strip() == "":
            i += 1
        body = "\n".join(lines[i:]).strip()
        separators = [line for line in body.split("\n") if line.strip() == "---"]
        question, answer = "", ""
        if len(separators) != 1:
            errors.append(f"{path}: {card_id}: need exactly one --- line between question and answer")
        else:
            question, answer = [chunk.strip() for chunk in body.split("\n---\n", 1)]
        cards.append((card_id, meta, question, answer))
    return cards, errors


def main():
    errors = []
    if not INDEX.exists():
        fail(["content/index.json is missing"])
    try:
        index = json.loads(INDEX.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail([f"content/index.json: {exc}"])

    topics = index.get("topics")
    if not isinstance(topics, list) or not topics:
        fail(["content/index.json: topics must be a non-empty list"])

    seen_topics = set()
    for topic in topics:
        for key in ("id", "title", "file", "summary", "order"):
            if key not in topic:
                errors.append(f"topic missing {key}: {topic!r}")
        topic_id = topic.get("id", "")
        if topic_id in seen_topics:
            errors.append(f"duplicate topic id: {topic_id}")
        seen_topics.add(topic_id)
        if not ID_RE.match(str(topic_id)):
            errors.append(f"{topic_id}: topic id must be a lowercase slug")
        order = topic.get("order")
        if not isinstance(order, list) or not order or any(not isinstance(v, str) or not v.strip() for v in order):
            errors.append(f"{topic_id}: order must be a non-empty list of version labels")
            order = []
        rel = topic.get("file", "")
        path = ROOT / rel
        if not rel.startswith("content/") or not rel.endswith(".md") or ".." in Path(rel).parts:
            errors.append(f"{topic_id}: file must be content/<name>.md")
            continue
        if not path.exists():
            errors.append(f"{topic_id}: missing {rel}")
            continue
        cards, parse_errors = parse_cards(path.read_text(encoding="utf-8"), rel)
        errors.extend(parse_errors)
        if not cards:
            errors.append(f"{rel}: no cards")
        seen_cards = set()
        used_versions = set()
        for card_id, meta, question, answer in cards:
            where = f"{rel}: {card_id or '(missing id)'}"
            if not ID_RE.match(card_id):
                errors.append(f"{where}: id must be a lowercase slug")
            if card_id in seen_cards:
                errors.append(f"{where}: duplicate id")
            seen_cards.add(card_id)
            if set(meta) != META_KEYS:
                errors.append(f"{where}: metadata keys must be {sorted(META_KEYS)}, got {sorted(meta)}")
            if meta.get("level") not in LEVELS:
                errors.append(f"{where}: bad level")
            if meta.get("status") not in STATUSES:
                errors.append(f"{where}: bad status")
            source = meta.get("source", "")
            if not source.startswith("https://") or source.startswith("https://javascript:"):
                errors.append(f"{where}: source must be an https URL")
            version = meta.get("version", "")
            used_versions.add(version)
            if not meta.get("title"):
                errors.append(f"{where}: empty title")
            if not question or not answer:
                errors.append(f"{where}: empty question or answer")
            for label, text in (("question", question), ("answer", answer)):
                if "###" in text:
                    errors.append(f"{where}: {label} contains ###")
        unknown = sorted(v for v in used_versions if v not in order)
        if unknown:
            errors.append(f"{rel}: versions not listed in order: {', '.join(unknown)}")
        print(f"{topic_id}: {len(cards)} cards")

    app = ROOT / "index.html"
    if not app.exists():
        errors.append("index.html is missing")
    else:
        html = app.read_text(encoding="utf-8")
        for needle in ("content/index.json", "function escapeHtml", "function parseCards", "localStorage"):
            if needle not in html:
                errors.append(f"index.html is missing {needle}")
        if "file://" in html:
            errors.append("index.html must not depend on file://")

    for name in ("404.html", ".nojekyll", ".github/workflows/pages.yml"):
        if not (ROOT / name).exists():
            errors.append(f"missing {name}")
    if (ROOT / "pages.yml").exists():
        errors.append("pages.yml must live in .github/workflows, not the repo root")

    if errors:
        fail(errors)
    print("ok")


if __name__ == "__main__":
    main()
