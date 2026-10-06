#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import json
import re

ROOT = Path(".")
INDEX = ROOT / "data" / "content-index.json"
AUDIT = ROOT / "SITE_VISUAL_SYSTEM_AUDIT.json"

HIGH_VALUE_COUNTRIES = {
    "united-states", "united-kingdom", "canada", "australia", "germany",
    "united-arab-emirates", "ireland", "new-zealand", "netherlands", "switzerland",
}
COMMERCIAL_CATEGORIES = {
    "visas-immigration", "visa-sponsorship-jobs", "jobs-work-permits",
    "study-abroad", "student-insurance", "banking", "money-transfer",
    "student-loans", "immigration-legal", "pr-citizenship", "relocation",
    "travel-insurance",
}

FEATURE_RE = re.compile(
    r'<div class="article-feature media [^"]*">\s*'
    r'<img\b[^>]*?/?>\s*'
    r'<span class="media-fallback">[^<]*</span>\s*</div>',
    re.I,
)
CARD_IMG_RE = re.compile(
    r'(<a\b[^>]*class="[^"]*\bcard-image\b[^"]*"[^>]*>)\s*'
    r'<img\b[^>]*?/?>\s*',
    re.I,
)
LEAD_IMG_RE = re.compile(
    r'(<a\b[^>]*class="[^"]*\blead-media\b[^"]*"[^>]*>)\s*'
    r'<img\b[^>]*?/?>\s*',
    re.I,
)
SEARCH_IMG_RE = re.compile(
    r'\s*<img src="\$\{esc\(x\.image\)\}"[^>]*>\s*',
    re.I,
)
PREMIUM_CSS_RE = re.compile(
    r'/assets/countrypilot-premium\.css(?:\?v=[^"\']*)?',
    re.I,
)

def clean(value: str | None) -> str:
    return html.escape((value or "").strip(), quote=True)

def tier(country_slug: str, category_slug: str) -> str:
    hc = country_slug in HIGH_VALUE_COUNTRIES
    cc = category_slug in COMMERCIAL_CATEGORIES
    if hc and cc:
        return "a"
    if hc or cc:
        return "b"
    return "c"

def make_cover(item: dict) -> str:
    t = tier(item.get("country_slug", ""), item.get("category_slug", ""))
    country = clean(item.get("country") or "Global")
    category = clean(item.get("category") or "Country Guide")
    cat_slug = re.sub(r"[^a-z0-9-]+", "-", (item.get("category_slug") or "country-guides").lower())
    label = "CountryPilot Research Guide" if t == "a" else "CountryPilot Practical Guide"
    if t == "c":
        label = "CountryPilot Guide"
    return (
        f'<div class="article-feature cp-editorial-cover cp-cover-tier-{t} cp-topic-{cat_slug}" '
        f'data-country="{country}" data-category="{category}">'
        f'<span class="cp-cover-label">{label}</span>'
        f'<span class="media-fallback">{country}</span>'
        f'<span class="cp-cover-topic">{category}</span>'
        f'</div>'
    )

def main() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    by_slug = {x["slug"]: x for x in data if x.get("slug")}

    stats = {
        "articles_indexed": len(by_slug),
        "tier_a": 0,
        "tier_b": 0,
        "tier_c": 0,
        "article_heroes_replaced": 0,
        "card_images_removed": 0,
        "homepage_hidden_hero_img_removed": 0,
        "search_dynamic_images_removed": 0,
        "html_files_changed": 0,
        "premium_css_version_updates": 0,
        "unmatched_article_features": [],
    }

    for item in by_slug.values():
        stats["tier_" + tier(item.get("country_slug", ""), item.get("category_slug", ""))] += 1

    for path in ROOT.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        original = text

        # Article pages: replace repeated generated artwork with a deliberate editorial cover.
        parts = path.parts
        if len(parts) >= 3 and parts[0] == "article" and path.name == "index.html":
            slug = parts[1]
            item = by_slug.get(slug)
            if item:
                cover = make_cover(item)
                text, n = FEATURE_RE.subn(cover, text, count=1)
                if n:
                    stats["article_heroes_replaced"] += 1
                else:
                    # Already converted is valid; only flag truly unconverted pages.
                    if "cp-editorial-cover" not in text:
                        stats["unmatched_article_features"].append(str(path))

        # Cards become text-first or compact identity tiles. Keep the anchor and fallback label.
        text, n = CARD_IMG_RE.subn(r"\1", text)
        stats["card_images_removed"] += n

        # Homepage lead image was invisible under a CSS photo background; stop requesting it.
        if path == ROOT / "index.html":
            text, n = LEAD_IMG_RE.subn(r"\1", text, count=1)
            stats["homepage_hidden_hero_img_removed"] += n

        # Search-generated cards should not request the old per-article artwork.
        if path == ROOT / "search" / "index.html":
            text, n = SEARCH_IMG_RE.subn("\n      ", text)
            stats["search_dynamic_images_removed"] += n

        new, n = PREMIUM_CSS_RE.subn(
            "/assets/countrypilot-premium.css?v=20261006-visual3",
            text,
        )
        text = new
        stats["premium_css_version_updates"] += n

        if text != original:
            path.write_text(text, encoding="utf-8")
            stats["html_files_changed"] += 1

    AUDIT.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    if stats["unmatched_article_features"]:
        raise SystemExit(
            "Unmatched article features: " + ", ".join(stats["unmatched_article_features"][:20])
        )
    if stats["article_heroes_replaced"] < 1700:
        raise SystemExit(f"Expected to replace most article heroes, got {stats['article_heroes_replaced']}")

if __name__ == "__main__":
    main()
