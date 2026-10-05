#!/usr/bin/env python3
from pathlib import Path

ARTICLE_ROOT = Path("article")
TAG = '<link rel="stylesheet" href="/assets/article-layout-fix.css?v=20261006b"/>'
MARKER = "/assets/article-layout-fix.css"

updated = 0
skipped = 0

if ARTICLE_ROOT.exists():
    for path in ARTICLE_ROOT.rglob("*.html"):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            skipped += 1
            continue

        if MARKER in text:
            continue
        if "</head>" not in text:
            skipped += 1
            continue

        text = text.replace("</head>", TAG + "\n</head>", 1)
        path.write_text(text, encoding="utf-8")
        updated += 1

print(f"CountryPilot article layout fix injected into {updated} article pages; skipped {skipped}.")
