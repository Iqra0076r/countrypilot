#!/usr/bin/env python3
from pathlib import Path

ARTICLE_ROOT = Path("article")
ARTICLE_TAG = '<link rel="stylesheet" href="/assets/article-layout-fix.css?v=20261006b"/>'
ARTICLE_MARKER = "/assets/article-layout-fix.css"

SOCIAL_TAG = '<link rel="stylesheet" href="/assets/social-favicons.css?v=20261006a"/>'
SOCIAL_MARKER = "/assets/social-favicons.css"

article_updated = 0
social_updated = 0
skipped = 0

# Article layout fix only for article pages.
if ARTICLE_ROOT.exists():
    for path in ARTICLE_ROOT.rglob("*.html"):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            skipped += 1
            continue

        changed = False
        if ARTICLE_MARKER not in text and "</head>" in text:
            text = text.replace("</head>", ARTICLE_TAG + "\n</head>", 1)
            article_updated += 1
            changed = True

        if changed:
            path.write_text(text, encoding="utf-8")

# Official social favicon styling on every public HTML page.
for path in Path(".").rglob("*.html"):
    if any(part in {".git", ".wrangler", "node_modules"} for part in path.parts):
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        skipped += 1
        continue

    if SOCIAL_MARKER in text:
        continue
    if "</head>" not in text:
        skipped += 1
        continue

    text = text.replace("</head>", SOCIAL_TAG + "\n</head>", 1)
    path.write_text(text, encoding="utf-8")
    social_updated += 1

print(f"CountryPilot article layout fix injected into {article_updated} article pages.")
print(f"CountryPilot social favicon styling injected into {social_updated} HTML pages.")
print(f"Skipped {skipped} files.")
