#!/usr/bin/env python3
from pathlib import Path
import re
import html as htmlmod

ARTICLE_ROOT = Path("article")
ARTICLE_TAG = '<link rel="stylesheet" href="/assets/article-layout-fix.css?v=20261006b"/>'
ARTICLE_MARKER = "/assets/article-layout-fix.css"

SOCIAL_TAG = '<link rel="stylesheet" href="/assets/social-favicons.css?v=20261006a"/>'
SOCIAL_MARKER = "/assets/social-favicons.css"

COUNTRY_STYLE_TAG = '<link rel="stylesheet" href="/assets/country-ai-images.css?v=20261006a"/>'
COUNTRY_STYLE_MARKER = "/assets/country-ai-images.css"

CARD_IMAGE_BASE = "/images/generated-cards/"
COUNTRY_IMAGE_BASE = "/images/generated-countries/"

COUNTRY_IMAGES = {
    "france": "france.webp",
    "ireland": "ireland.webp",
    "netherlands": "netherlands.webp",
    "portugal": "portugal.webp",
    "sweden": "sweden.webp",
    "switzerland": "switzerland.webp",
    "united-arab-emirates": "united-arab-emirates.webp",
    "singapore": "singapore.webp",
    "japan": "japan.webp",
    "south-korea": "south-korea.webp",
}

# Ordered from most specific to broadest.
CARD_IMAGE_RULES = [
    (("rental deposit", "security deposit", "bond refund", "deposit refund"), "rental-deposits.webp"),
    (("finding accommodation before arrival", "accommodation before arrival", "housing before arrival"), "finding-accommodation.webp"),
    (("short-term versus long-term housing", "short term versus long term housing", "short-term vs long-term", "long-term housing"), "short-long-term-housing.webp"),
    (("cost of living", "living costs", "student budget", "student budgeting"), "student-cost-of-living.webp"),
    (("visa interview", "interview preparation", "embassy interview"), "visa-interview-preparation.webp"),
    (("embassy appointment", "consular appointment", "document checklist", "visa documents checklist", "application checklist"), "embassy-document-checklist.webp"),
    (("ielts", "toefl", "pte", "gre", "language test", "english test"), "language-tests.webp"),
    (("immigration lawyer", "immigration legal", "legal guide", "immigration attorney"), "immigration-lawyers.webp"),
    (("international student insurance", "student insurance", "student health insurance"), "international-student-insurance.webp"),
    (("travel insurance", "travel health insurance", "medical evacuation", "travel health"), "travel-insurance.webp"),
    (("digital nomad", "remote work visa", "nomad visa"), "digital-nomad-visas.webp"),
    (("student loan", "education loan", "education financing", "tuition loan"), "education-student-loans.webp"),
    (("banking for expat", "banking for student", "expat banking", "student banking", "bank account abroad", "international money transfer"), "banking-expats-students.webp"),
    (("accommodation abroad", "student accommodation", "housing abroad", "renting abroad", "rental housing", "finding accommodation"), "accommodation-abroad.webp"),
    (("visa sponsorship job", "sponsorship job", "sponsored job", "employer sponsorship"), "visa-sponsorship-jobs.webp"),
    (("work permit", "jobs & work permits", "jobs and work permits", "work visa", "employment permit"), "jobs-work-permits.webp"),
    (("permanent residency", "permanent residence", "pr & citizenship", "pr and citizenship", "citizenship", "naturalization", "naturalisation"), "pr-citizenship.webp"),
    (("scholarship", "funding", "grant", "financial aid"), "scholarships-funding.webp"),
    (("study abroad", "student visa", "international student", "university abroad"), "study-abroad.webp"),
    (("visa", "immigration", "entry permit", "residence permit"), "visas-immigration.webp"),
]

def plain_text(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = htmlmod.unescape(text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

def choose_card_image(card_html: str):
    hay = plain_text(card_html)
    # Include href slugs as normalized words for stronger matching.
    hrefs = " ".join(re.findall(r'href=["\']([^"\']+)["\']', card_html, flags=re.I))
    hay += " " + hrefs.lower().replace("-", " ").replace("_", " ")
    for terms, filename in CARD_IMAGE_RULES:
        if any(term in hay for term in terms):
            return CARD_IMAGE_BASE + filename
    return None

def replace_card_image(card_html: str) -> str:
    image = choose_card_image(card_html)
    if not image:
        return card_html

    # Replace only the first img src inside the editorial card.
    def repl(match):
        tag = match.group(0)
        if re.search(r'\bsrc=["\'][^"\']*["\']', tag, flags=re.I):
            tag = re.sub(
                r'\bsrc=["\'][^"\']*["\']',
                f'src="{image}"',
                tag,
                count=1,
                flags=re.I,
            )
        else:
            tag = tag[:-1] + f' src="{image}">'
        # Generated WebP dimensions are 1200x675; browser may render responsively.
        tag = re.sub(r'\bwidth=["\'][^"\']*["\']', 'width="1200"', tag, count=1, flags=re.I)
        tag = re.sub(r'\bheight=["\'][^"\']*["\']', 'height="675"', tag, count=1, flags=re.I)
        return tag

    return re.sub(r'<img\b[^>]*>', repl, card_html, count=1, flags=re.I)

def country_slug_from_card(card_html: str):
    data = re.search(r'\bdata-country=["\']([^"\']+)["\']', card_html, flags=re.I)
    if data:
        return data.group(1).strip().lower().replace(" ", "-")
    href = re.search(r'\bhref=["\'][^"\']*country/([^/"\']+)/index\.html["\']', card_html, flags=re.I)
    if href:
        return href.group(1).strip().lower()
    return None

def add_class_to_opening_tag(tag: str, class_name: str) -> str:
    m = re.search(r'\bclass=["\']([^"\']*)["\']', tag, flags=re.I)
    if m:
        classes = m.group(1).split()
        if class_name not in classes:
            classes.append(class_name)
        replacement = 'class="' + " ".join(classes) + '"'
        return tag[:m.start()] + replacement + tag[m.end():]
    return tag[:-1] + f' class="{class_name}">'

def add_style_to_opening_tag(tag: str, style_value: str) -> str:
    m = re.search(r'\bstyle=["\']([^"\']*)["\']', tag, flags=re.I)
    if m:
        current = m.group(1).strip().rstrip(";")
        replacement = f'style="{current};{style_value}"'
        return tag[:m.start()] + replacement + tag[m.end():]
    return tag[:-1] + f' style="{style_value}">'

def apply_country_card_image(card_html: str) -> str:
    slug = country_slug_from_card(card_html)
    filename = COUNTRY_IMAGES.get(slug or "")
    if not filename:
        return card_html

    image = COUNTRY_IMAGE_BASE + filename

    # Existing photo cards already have an image element: replace that image.
    if re.search(r'<img\b', card_html, flags=re.I):
        def repl_img(match):
            tag = match.group(0)
            if re.search(r'\bsrc=["\'][^"\']*["\']', tag, flags=re.I):
                tag = re.sub(r'\bsrc=["\'][^"\']*["\']', f'src="{image}"', tag, count=1, flags=re.I)
            else:
                tag = tag[:-1] + f' src="{image}">'
            tag = re.sub(r'\bwidth=["\'][^"\']*["\']', 'width="1200"', tag, count=1, flags=re.I)
            tag = re.sub(r'\bheight=["\'][^"\']*["\']', 'height="675"', tag, count=1, flags=re.I)
            return tag
        return re.sub(r'<img\b[^>]*>', repl_img, card_html, count=1, flags=re.I)

    # Plain A-Z directory cards become photo cards without altering their text.
    open_match = re.match(r'<a\b[^>]*>', card_html, flags=re.I)
    if not open_match:
        return card_html
    opening = open_match.group(0)
    opening = add_class_to_opening_tag(opening, "ai-country-photo")
    opening = add_style_to_opening_tag(opening, f"background-image:url('{image}')")
    return opening + card_html[open_match.end():]

def apply_country_page_hero(text: str, path: Path):
    parts = path.as_posix().split("/")
    if len(parts) < 3 or parts[0] != "country" or parts[-1] != "index.html":
        return text
    slug = parts[1].lower()
    filename = COUNTRY_IMAGES.get(slug)
    if not filename:
        return text
    image = COUNTRY_IMAGE_BASE + filename
    m = re.search(r'<section\b[^>]*class=["\'][^"\']*\barchive-hero\b[^"\']*["\'][^>]*>', text, flags=re.I)
    if not m:
        return text
    opening = m.group(0)
    opening = add_class_to_opening_tag(opening, "has-country-image")
    opening = add_style_to_opening_tag(opening, f"--country-image:url('{image}')")
    return text[:m.start()] + opening + text[m.end():]

article_updated = 0
social_updated = 0
card_pages_updated = 0
cards_updated = 0
country_card_pages_updated = 0
country_cards_updated = 0
country_hero_pages_updated = 0
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

# Site-wide pass: social favicon stylesheet + topic-matched editorial card images.
for path in Path(".").rglob("*.html"):
    if any(part in {".git", ".wrangler", "node_modules"} for part in path.parts):
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        skipped += 1
        continue

    changed = False

    if SOCIAL_MARKER not in text and "</head>" in text:
        text = text.replace("</head>", SOCIAL_TAG + "\n</head>", 1)
        social_updated += 1
        changed = True

    if COUNTRY_STYLE_MARKER not in text and "</head>" in text:
        text = text.replace("</head>", COUNTRY_STYLE_TAG + "\n</head>", 1)
        changed = True

    # Add country-specific imagery to country cards wherever those countries appear.
    country_page_count_holder = [0]
    def country_card_repl(match):
        before = match.group(0)
        after = apply_country_card_image(before)
        if after != before:
            country_page_count_holder[0] += 1
        return after

    country_text = re.sub(
        r'<a\b[^>]*class=["\'][^"\']*\bcountry-card\b[^"\']*["\'][^>]*>.*?</a>',
        country_card_repl,
        text,
        flags=re.I | re.S,
    )
    if country_text != text:
        text = country_text
        country_cards_updated += country_page_count_holder[0]
        country_card_pages_updated += 1
        changed = True

    # Give each matching country desk a visual hero using the same country artwork.
    hero_text = apply_country_page_hero(text, path)
    if hero_text != text:
        text = hero_text
        country_hero_pages_updated += 1
        changed = True

    # Match each editorial card independently, preserving all text/links/SEO.
    page_card_count = 0
    def card_repl(match):
        nonlocal_holder[0] += 1
        before = match.group(0)
        after = replace_card_image(before)
        if after != before:
            page_card_count_holder[0] += 1
        return after

    # Python nested-scope counters that work inside the replacement function.
    nonlocal_holder = [0]
    page_card_count_holder = [0]
    new_text = re.sub(
        r'<article\b[^>]*class=["\'][^"\']*\beditorial-card\b[^"\']*["\'][^>]*>.*?</article>',
        card_repl,
        text,
        flags=re.I | re.S,
    )
    if new_text != text:
        text = new_text
        cards_updated += page_card_count_holder[0]
        card_pages_updated += 1
        changed = True

    if changed:
        path.write_text(text, encoding="utf-8")

print(f"CountryPilot article layout fix injected into {article_updated} article pages.")
print(f"CountryPilot social favicon styling injected into {social_updated} HTML pages.")
print(f"CountryPilot AI topic images applied to {cards_updated} editorial cards across {card_pages_updated} pages.")
print(f"CountryPilot country images applied to {country_cards_updated} country cards across {country_card_pages_updated} pages.")
print(f"CountryPilot country hero images applied to {country_hero_pages_updated} country pages.")
print(f"Skipped {skipped} files.")
