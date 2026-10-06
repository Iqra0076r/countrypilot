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

CARD_STYLE_TAG = '<link rel="stylesheet" href="/assets/card-layout-fix.css?v=20261006a"/>'
CARD_STYLE_MARKER = "/assets/card-layout-fix.css"

PROOF_FUNDS_CTA_MARKER = "cp-proof-funds-tool-cta"

CARD_IMAGE_BASE = "/images/generated-cards/"
COUNTRY_AI_IMAGE_BASE = "/images/generated-countries/"
COUNTRY_FALLBACK_IMAGE_BASE = "/images/generated/"

PRIORITY_SEO_COUNTRIES = {
    "united-states": "United States",
    "canada": "Canada",
    "united-kingdom": "United Kingdom",
    "australia": "Australia",
    "germany": "Germany",
    "ireland": "Ireland",
    "netherlands": "Netherlands",
    "switzerland": "Switzerland",
    "united-arab-emirates": "UAE",
    "new-zealand": "New Zealand",
}

PRIORITY_TITLE_SUFFIXES = [
    ("visa-sponsorship-jobs-guide", "{country} Visa Sponsorship Jobs 2026 | CountryPilot"),
    ("skilled-worker-jobs-guide", "{country} Skilled Worker Jobs 2026 | CountryPilot"),
    ("proof-of-funds-explained", "{country} Visa Proof of Funds 2026 | CountryPilot"),
    ("travel-insurance-for-students", "{country} Student Travel Insurance Guide | CountryPilot"),
    ("student-health-insurance-guide", "{country} Student Health Insurance 2026 | CountryPilot"),
    ("comparing-student-insurance", "{country} Student Insurance Comparison | CountryPilot"),
    ("expat-medical-insurance-basics", "{country} Expat Health Insurance Guide | CountryPilot"),
    ("mandatory-health-cover-explained", "{country} Student Health Cover Guide | CountryPilot"),
    ("international-remittance-guide", "{country} International Money Transfer 2026 | CountryPilot"),
    ("transfer-fees-explained", "{country} Money Transfer Fees 2026 | CountryPilot"),
    ("fintech-transfer-guide", "{country} Money Transfer Apps Guide | CountryPilot"),
    ("bank-wire-guide", "{country} International Bank Transfer Guide | CountryPilot"),
    ("expat-banking-guide", "{country} Expat Banking Guide 2026 | CountryPilot"),
    ("opening-a-bank-account", "{country} Bank Account for Expats | CountryPilot"),
    ("student-bank-account-guide", "{country} Student Bank Account Guide | CountryPilot"),
    ("international-student-finance-guide", "{country} International Student Finance | CountryPilot"),
    ("tuition-financing-guide", "{country} Tuition Financing Guide | CountryPilot"),
    ("education-loan-eligibility", "{country} Student Loan Eligibility Guide | CountryPilot"),
    ("repayment-planning", "{country} Student Loan Repayment Guide | CountryPilot"),
    ("scholarships-versus-loans", "{country} Scholarships vs Student Loans | CountryPilot"),
]


HIGH_VALUE_COUNTRIES = {
    "united-states": "United States",
    "united-kingdom": "United Kingdom",
    "canada": "Canada",
    "australia": "Australia",
}

PRIORITY_REINDEX_DATE = "2026-10-06"

NEXT_BATCH_SEO = {
    "united-states-student-visa-guide": (
        "US Student Visa Guide 2026 | CountryPilot",
        "US student visa guide for F-1 and M-1 applicants: application sequence, finances, documents, work rules and official sources to verify before applying.",
        "US Student Visa Guide",
    ),
    "united-states-work-permit-guide": (
        "US Work Permit Guide 2026 | CountryPilot",
        "US work permit guide explaining employment authorization, visa and status distinctions, documents, route checks and official sources to verify.",
        "US Work Permit Guide",
    ),
    "united-states-visa-sponsorship-jobs-guide": (
        "US Visa Sponsorship Jobs 2026 | CountryPilot",
        "US visa sponsorship jobs guide covering employer sponsorship research, job-search checks, application preparation, scam prevention and official sources.",
        "US Visa Sponsorship Jobs",
    ),
    "united-states-it-sponsorship-jobs": (
        "US IT Visa Sponsorship Jobs 2026 | CountryPilot",
        "US IT visa sponsorship jobs guide with employer research, role targeting, sponsorship checks, application preparation and scam warning signs.",
        "US IT Sponsorship Jobs",
    ),
    "united-states-student-health-insurance-guide": (
        "US Student Health Insurance 2026 | CountryPilot",
        "US student health insurance guide covering university requirements, premiums, deductibles, networks, exclusions and comparison checks for international students.",
        "US Student Health Insurance",
    ),
    "united-states-expat-medical-insurance-basics": (
        "US Expat Health Insurance Guide | CountryPilot",
        "US expat health insurance guide covering plan types, deductibles, networks, exclusions, emergency cover and practical comparison checks.",
        "US Expat Health Insurance",
    ),
    "united-states-international-remittance-guide": (
        "US International Money Transfer Guide 2026 | CountryPilot",
        "US international money transfer guide covering fees, FX markup, transfer speed, bank wires, fintech options and scam checks.",
        "US International Money Transfers",
    ),
    "united-states-when-to-consider-an-immigration-lawyer": (
        "When to Hire a US Immigration Lawyer | CountryPilot",
        "Guide to when a US immigration lawyer may be useful, how to prepare for a consultation, verify credentials and understand common fee structures.",
        "US Immigration Lawyer Guide",
    ),
    "united-states-accredited-online-degrees": (
        "Accredited Online Degrees in the US | CountryPilot",
        "Guide to accredited online degrees in the US, covering accreditation checks, recognition, tuition, delivery format and questions to verify before enrolling.",
        "US Accredited Online Degrees",
    ),
    "united-states-online-cybersecurity-programs": (
        "Online Cybersecurity Programs in the US | CountryPilot",
        "Guide to online cybersecurity programs in the US, covering accreditation, curriculum, tuition, career fit and recognition checks before enrolling.",
        "US Online Cybersecurity Programs",
    ),

    "united-kingdom-skilled-worker-pathway": (
        "UK Skilled Worker Visa Guide 2026 | CountryPilot",
        "UK Skilled Worker visa guide covering sponsor checks, role eligibility, application evidence, costs to verify and official sources for current rules.",
        "UK Skilled Worker Visa",
    ),
    "united-kingdom-how-to-verify-a-sponsor": (
        "How to Check a UK Visa Sponsor 2026 | CountryPilot",
        "How to verify a UK visa sponsor using official registers, job-offer checks, employer research and scam warning signs before accepting an offer.",
        "Verify a UK Visa Sponsor",
    ),
    "united-kingdom-healthcare-sponsorship-jobs": (
        "UK Healthcare Visa Sponsorship Jobs 2026 | CountryPilot",
        "UK healthcare visa sponsorship jobs guide covering sponsor checks, role targeting, recruitment routes, application preparation and scam prevention.",
        "UK Healthcare Sponsorship Jobs",
    ),
    "united-kingdom-teaching-sponsorship-jobs": (
        "UK Teaching Visa Sponsorship Jobs 2026 | CountryPilot",
        "UK teaching visa sponsorship jobs guide covering sponsor checks, role targeting, qualification research, application preparation and scam prevention.",
        "UK Teaching Sponsorship Jobs",
    ),
    "united-kingdom-opening-a-bank-account": (
        "UK Bank Account for Expats & Students | CountryPilot",
        "UK bank account guide for international students and expats covering identity checks, address evidence, fees, account features and practical comparison steps.",
        "UK Bank Account Guide",
    ),
    "united-kingdom-travel-insurance-for-students": (
        "UK Student Travel Insurance Guide | CountryPilot",
        "UK student travel insurance guide covering medical cover, exclusions, deductibles, cancellation, visa-related checks and policy comparison questions.",
        "UK Student Travel Insurance",
    ),
    "united-kingdom-financial-aid-options": (
        "UK Financial Aid for International Students | CountryPilot",
        "UK financial aid guide for international students covering scholarships, grants, loans, university support and funding checks before committing to study.",
        "UK International Student Financial Aid",
    ),
    "united-kingdom-tuition-and-budgeting-guide": (
        "UK Tuition & Student Budget Guide 2026 | CountryPilot",
        "UK tuition and student budgeting guide covering fees, living costs, deposits, insurance, transport and first-year planning for international students.",
        "UK Tuition & Student Budget",
    ),
    "united-kingdom-how-to-verify-a-regulated-adviser": (
        "How to Verify a UK Immigration Adviser | CountryPilot",
        "Guide to checking a UK immigration adviser, verifying regulation and credentials, preparing questions and spotting warning signs before paying for advice.",
        "Verify a UK Immigration Adviser",
    ),
    "united-kingdom-international-job-search-guide": (
        "UK Jobs for International Applicants 2026 | CountryPilot",
        "UK international job-search guide covering sponsor research, role targeting, application preparation, employer checks and sponsorship scam prevention.",
        "UK International Job Search",
    ),

    "canada-work-visa-guide": (
        "Canada Work Visa Guide 2026 | CountryPilot",
        "Canada work visa guide covering work-permit routes, employer and eligibility checks, application evidence and official sources to verify before applying.",
        "Canada Work Visa Guide",
    ),
    "canada-skilled-worker-jobs-guide": (
        "Canada Skilled Worker Jobs 2026 | CountryPilot",
        "Canada skilled worker jobs guide covering role research, employer checks, immigration-route alignment, application preparation and scam prevention.",
        "Canada Skilled Worker Jobs",
    ),
    "canada-employer-sponsorship-basics": (
        "Canada Employer Sponsorship Guide 2026 | CountryPilot",
        "Canada employer sponsorship guide explaining employer-backed work routes, job-offer checks, evidence, recruitment research and official sources to verify.",
        "Canada Employer Sponsorship",
    ),
    "canada-university-admissions-guide": (
        "Canada University Admissions Guide 2026 | CountryPilot",
        "Canada university admissions guide for international students covering program research, entry requirements, documents, timelines and offer checks.",
        "Canada University Admissions",
    ),
    "canada-tuition-financing-guide": (
        "Canada Tuition Financing Guide | CountryPilot",
        "Canada tuition financing guide covering scholarships, student loans, payment planning, exchange-rate risk and questions to verify before borrowing.",
        "Canada Tuition Financing",
    ),
    "canada-education-loan-eligibility": (
        "Canada Student Loan Eligibility Guide | CountryPilot",
        "Canada student loan eligibility guide covering lender criteria, cosigners, documentation, borrowing costs and repayment checks for international students.",
        "Canada Student Loan Eligibility",
    ),
    "canada-expat-banking-guide": (
        "Canada Expat Banking Guide 2026 | CountryPilot",
        "Canada expat banking guide covering account opening, identity and address checks, fees, cards, transfers and practical comparison questions.",
        "Canada Expat Banking",
    ),
    "canada-fully-funded-scholarships": (
        "Fully Funded Scholarships in Canada 2026 | CountryPilot",
        "Canada fully funded scholarship guide covering eligibility research, award coverage, deadlines, documents and official scholarship sources to verify.",
        "Canada Fully Funded Scholarships",
    ),
    "canada-finding-accommodation-before-arrival": (
        "Finding Accommodation in Canada Before Arrival | CountryPilot",
        "Canada accommodation guide covering rental research, deposits, document checks, scam prevention and practical steps before arriving.",
        "Canada Accommodation Before Arrival",
    ),
    "canada-visa-refusal-options-overview": (
        "Canada Visa Refusal Options Guide 2026 | CountryPilot",
        "Canada visa refusal options overview covering decision review, reapplication research, evidence gaps, legal-help checks and official sources to verify.",
        "Canada Visa Refusal Options",
    ),

    "australia-it-sponsorship-jobs": (
        "Australia IT Visa Sponsorship Jobs 2026 | CountryPilot",
        "Australia IT visa sponsorship jobs guide covering employer research, role targeting, sponsorship checks, application preparation and scam warning signs.",
        "Australia IT Sponsorship Jobs",
    ),
    "australia-finance-sponsorship-jobs": (
        "Australia Finance Visa Sponsorship Jobs 2026 | CountryPilot",
        "Australia finance visa sponsorship jobs guide covering employer research, role targeting, sponsorship checks, application preparation and scam prevention.",
        "Australia Finance Sponsorship Jobs",
    ),
    "australia-scholarship-eligibility-guide": (
        "Australia Scholarship Eligibility Guide 2026 | CountryPilot",
        "Australia scholarship eligibility guide covering academic criteria, funding scope, documents, deadlines and official sources to verify before applying.",
        "Australia Scholarship Eligibility",
    ),
    "australia-phd-scholarships": (
        "Australia PhD Scholarships 2026 | CountryPilot",
        "Australia PhD scholarship guide covering funding research, eligibility, research proposals, supervisor checks, deadlines and official university sources.",
        "Australia PhD Scholarships",
    ),
    "australia-student-money-transfers": (
        "Australia Student Money Transfer Guide 2026 | CountryPilot",
        "Australia student money transfer guide covering fees, FX markup, transfer speed, bank and fintech options, limits and scam checks.",
        "Australia Student Money Transfers",
    ),
    "australia-insurance-claim-preparation": (
        "Australia Insurance Claim Preparation Guide | CountryPilot",
        "Australia insurance claim preparation guide covering documents, receipts, timelines, exclusions, insurer contact steps and evidence to keep.",
        "Australia Insurance Claim Preparation",
    ),
    "australia-family-visa-overview": (
        "Australia Family Visa Guide 2026 | CountryPilot",
        "Australia family visa overview covering route research, relationship and family evidence, application sequencing and official sources to verify.",
        "Australia Family Visa Guide",
    ),
    "australia-visa-entry-requirements-guide": (
        "Australia Visa & Entry Requirements 2026 | CountryPilot",
        "Australia visa and entry requirements guide covering visa-route checks, passport and document planning, arrival preparation and official sources.",
        "Australia Visa & Entry Requirements",
    ),
    "australia-choosing-a-university": (
        "How to Choose a University in Australia | CountryPilot",
        "Guide to choosing an Australian university using accreditation, program fit, tuition, location, graduate outcomes and international-student support checks.",
        "Choose a University in Australia",
    ),
    "australia-academic-intakes-guide": (
        "Australia University Intakes 2026 | CountryPilot",
        "Australia academic intakes guide covering application windows, offer timing, visa planning, scholarships and practical deadline checks.",
        "Australia University Intakes",
    ),
}

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

def optimize_priority_article_title(text: str, path: Path) -> str:
    parts = path.as_posix().split("/")
    if len(parts) < 3 or parts[0] != "article" or parts[-1] != "index.html":
        return text
    slug = parts[1].lower()
    for suffix, template in PRIORITY_TITLE_SUFFIXES:
        marker = "-" + suffix
        if not slug.endswith(marker):
            continue
        country_slug = slug[:-len(marker)]
        country = PRIORITY_SEO_COUNTRIES.get(country_slug)
        if not country:
            return text
        title = template.format(country=country)
        return re.sub(r"<title>[\s\S]*?</title>", f"<title>{title}</title>", text, count=1, flags=re.I)
    return text


def replace_meta_content(text: str, attr_name: str, attr_value: str, content: str) -> str:
    escaped = htmlmod.escape(content, quote=True)
    def repl(match):
        tag = match.group(0)
        if not re.search(rf'\b{re.escape(attr_name)}=["\']{re.escape(attr_value)}["\']', tag, flags=re.I):
            return tag
        if re.search(r'\bcontent=["\'][^"\']*["\']', tag, flags=re.I):
            return re.sub(r'\bcontent=["\'][^"\']*["\']', f'content="{escaped}"', tag, count=1, flags=re.I)
        return tag[:-2] + f' content="{escaped}"/>' if tag.endswith('/>') else tag[:-1] + f' content="{escaped}">'
    return re.sub(r'<meta\b[^>]*>', repl, text, flags=re.I)

def high_value_country_for_slug(slug: str):
    for country_slug, country in HIGH_VALUE_COUNTRIES.items():
        if slug == country_slug or slug.startswith(country_slug + "-"):
            return country_slug, country
    return None, None

def optimize_next_batch_seo(text: str, path: Path) -> str:
    parts = path.as_posix().split("/")
    if len(parts) < 3 or parts[0] != "article" or parts[-1] != "index.html":
        return text
    slug = parts[1].lower()
    item = NEXT_BATCH_SEO.get(slug)
    if not item:
        return text
    title, description, _label = item
    escaped_title = htmlmod.escape(title)
    text = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escaped_title}</title>", text, count=1, flags=re.I)
    text = replace_meta_content(text, "name", "description", description)
    text = replace_meta_content(text, "property", "og:title", title)
    text = replace_meta_content(text, "property", "og:description", description)
    text = replace_meta_content(text, "name", "twitter:title", title)
    text = replace_meta_content(text, "name", "twitter:description", description)
    text = re.sub(
        r'"dateModified":"\d{4}-\d{2}-\d{2}"',
        f'"dateModified":"{PRIORITY_REINDEX_DATE}"',
        text,
        count=1,
    )
    return text

def inject_priority_article_links(text: str, path: Path) -> str:
    parts = path.as_posix().split("/")
    if len(parts) < 3 or parts[0] != "article" or parts[-1] != "index.html":
        return text
    slug = parts[1].lower()
    if slug not in NEXT_BATCH_SEO or "cp-priority-links" in text:
        return text
    country_slug, country = high_value_country_for_slug(slug)
    if not country_slug:
        return text
    candidates = []
    for other_slug, (_title, _description, label) in NEXT_BATCH_SEO.items():
        other_country_slug, _ = high_value_country_for_slug(other_slug)
        if other_country_slug == country_slug and other_slug != slug:
            candidates.append((other_slug, label))
    candidates = candidates[:6]
    links = "".join(
        f'<a href="/article/{other_slug}/" style="display:inline-block;margin:4px 8px 4px 0;font-weight:750">{htmlmod.escape(label)} →</a>'
        for other_slug, label in candidates
    )
    block = (
        f'<div class="info-box cp-priority-links" style="margin:18px 0;padding:16px 18px">'
        f'<strong>Popular {htmlmod.escape(country)} planning guides</strong>'
        f'<div style="margin-top:7px">{links}</div></div>'
    )
    pattern = r'(<section\b[^>]*class=["\'][^"\']*\bquick-answer\b[^"\']*["\'][^>]*>[\s\S]*?</section>)'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, r'\1' + block, text, count=1, flags=re.I)
    marker = '<div class="article-layout">'
    if marker in text:
        return text.replace(marker, block + marker, 1)
    return text

def inject_priority_country_hub(text: str, path: Path) -> str:
    parts = path.as_posix().split("/")
    if len(parts) < 3 or parts[0] != "country" or parts[-1] != "index.html":
        return text
    country_slug = parts[1].lower()
    country = HIGH_VALUE_COUNTRIES.get(country_slug)
    if not country or "cp-priority-country-hub" in text:
        return text
    cards = []
    for slug, (_title, description, label) in NEXT_BATCH_SEO.items():
        slug_country, _ = high_value_country_for_slug(slug)
        if slug_country != country_slug:
            continue
        cards.append(
            f'<a href="/article/{slug}/" style="display:block;padding:15px 16px;border:1px solid #d8e2ec;border-radius:12px;background:#fff;text-decoration:none;color:inherit">'
            f'<strong style="display:block;margin-bottom:5px">{htmlmod.escape(label)}</strong>'
            f'<span style="display:block;font-size:13px;line-height:1.45;color:#52606d">{htmlmod.escape(description)}</span></a>'
        )
    block = (
        f'<section class="container cp-priority-country-hub" style="padding:26px 0 10px">'
        f'<div class="section-head editorial"><div><span class="eyebrow">High-demand planning</span>'
        f'<h2>Popular {htmlmod.escape(country)} guides</h2></div></div>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px">{"".join(cards)}</div>'
        f'</section>'
    )
    pattern = r'(<section\b[^>]*class=["\'][^"\']*\barchive-hero\b[^"\']*["\'][^>]*>[\s\S]*?</section>)'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, r'\1' + block, text, count=1, flags=re.I)
    return text

def inject_us_footer_destination(text: str) -> str:
    marker = '<div><h4>Destinations</h4>'
    injected = '<div><h4>Destinations</h4><a href="/country/united-states/">United States</a>'
    if injected in text or marker not in text:
        return text
    return text.replace(marker, injected, 1)

def priority_reindex_urls():
    urls = [f"https://countrypilot.info/article/{slug}/" for slug in NEXT_BATCH_SEO]
    urls.extend(f"https://countrypilot.info/country/{slug}/" for slug in HIGH_VALUE_COUNTRIES)
    return urls

def refresh_priority_sitemaps():
    urls = priority_reindex_urls()
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in urls:
        sitemap_lines.append(
            f'  <url><loc>{url}</loc><lastmod>{PRIORITY_REINDEX_DATE}</lastmod></url>'
        )
    sitemap_lines.append('</urlset>')
    Path("sitemap-money.xml").write_text("\n".join(sitemap_lines) + "\n", encoding="utf-8")

    main_sitemap = Path("sitemap.xml")
    if main_sitemap.exists():
        text = main_sitemap.read_text(encoding="utf-8")
        for url in urls:
            pattern = rf'(<url>\s*<loc>{re.escape(url)}</loc>)(?:<lastmod>[^<]+</lastmod>)?(\s*</url>)'
            text = re.sub(
                pattern,
                rf'\1<lastmod>{PRIORITY_REINDEX_DATE}</lastmod>\2',
                text,
                count=1,
            )
        main_sitemap.write_text(text, encoding="utf-8")

    robots = Path("robots.txt")
    if robots.exists():
        text = robots.read_text(encoding="utf-8")
        money_line = "Sitemap: https://countrypilot.info/sitemap-money.xml"
        if money_line not in text:
            text = text.rstrip() + "\n" + money_line + "\n"
            robots.write_text(text, encoding="utf-8")

def inject_proof_funds_cta(text: str, path: Path) -> str:
    p = path.as_posix().lower()
    if not (p.startswith("article/") and p.endswith("-proof-of-funds-explained/index.html")):
        return text
    if PROOF_FUNDS_CTA_MARKER in text:
        return text
    cta = '''<aside class="cp-proof-funds-tool-cta" style="width:min(900px,calc(100% - 36px));margin:0 auto 24px;padding:18px 20px;border:1px solid #d7eafa;border-left:5px solid #0b67b2;background:#f3f9ff"><strong>Check your available funds</strong><p style="margin:6px 0 10px">Use CountryPilot's Visa Proof of Funds Calculator with the current official requirement for your route.</p><a href="/country-tools/proof-of-funds-calculator/" style="font-weight:800;color:#0b67b2">Open the Proof of Funds Calculator →</a></aside>'''
    marker = '<section class="keyfacts">'
    if marker in text:
        return text.replace(marker, cta + marker, 1)
    marker = '<div class="article-layout">'
    if marker in text:
        return text.replace(marker, cta + marker, 1)
    return text

def inject_revenue_tool_callout(text: str, path: Path) -> str:
    parts = path.as_posix().split("/")
    if len(parts) < 3 or parts[0] != "article" or parts[-1] != "index.html":
        return text
    slug = parts[1].lower()

    if slug.endswith("-proof-of-funds-explained"):
        callout = (
            '<div class="info-box revenue-tool-callout"><strong>Free planning tool:</strong> '
            'Use the <a href="/country-tools/proof-of-funds-calculator/">Visa Proof of Funds Calculator</a> '
            'to estimate a personal financial buffer, then verify the official minimum for your exact route.</div>'
        )
    elif any(term in slug for term in (
        "visa-document-checklist", "document-checklist", "embassy-appointment",
        "consular-appointment", "visa-interview"
    )):
        callout = (
            '<div class="info-box revenue-tool-callout"><strong>Build your preparation list:</strong> '
            'Use the <a href="/country-tools/visa-document-checklist/">Visa Document Checklist Builder</a> '
            'to organise common documents before verifying the exact official requirements for your route.</div>'
        )
    elif any(term in slug for term in (
        "rental-deposit", "accommodation-before-arrival", "finding-accommodation",
        "short-term-versus-long-term-housing", "short-term-vs-long-term-housing",
        "cost-of-living", "relocation-cost", "moving-cost"
    )):
        callout = (
            '<div class="info-box revenue-tool-callout"><strong>Plan the move:</strong> '
            'Use the <a href="/country-tools/relocation-budget-calculator/">Relocation Budget Calculator</a> '
            'to estimate deposits, advance rent, flights, setup costs and an emergency reserve.</div>'
        )
    elif any(term in slug for term in (
        "student-cost-of-living", "study-abroad-cost", "tuition-cost",
        "student-budget", "education-cost", "study-budget"
    )):
        callout = (
            '<div class="info-box revenue-tool-callout"><strong>Estimate your first year:</strong> '
            'Use the <a href="/country-tools/study-abroad-budget-calculator/">Study Abroad Budget Calculator</a> '
            'to combine tuition, rent, food, transport, insurance and one-off setup costs.</div>'
        )
    elif any(term in slug for term in (
        "travel-insurance-for-students", "comparing-student-insurance",
        "student-health-insurance", "student-insurance"
    )):
        callout = (
            '<div class="info-box revenue-tool-callout"><strong>Compare student insurance costs:</strong> '
            'Use the <a href="/country-tools/student-insurance-cost-calculator/">International Student Insurance Cost Calculator</a> '
            'to compare premiums, deductibles and expected out-of-pocket costs before checking policy benefits and official requirements.</div>'
        )
    elif any(term in slug for term in (
        "student-loan", "education-loan", "repayment-planning", "tuition-financing",
        "international-student-finance", "currency-risk-for-education-loans",
        "loan-documents", "scholarships-versus-loans", "cosigner-basics",
        "financial-aid-options"
    )):
        callout = (
            '<div class="info-box revenue-tool-callout"><strong>Estimate loan repayment:</strong> '
            'Use the <a href="/country-tools/student-loan-repayment-calculator/">Student Loan Repayment Calculator</a> '
            'to model monthly payments and total interest using your own amount, APR and repayment term.</div>'
        )
    elif any(term in slug for term in (
        "international-remittance", "student-money-transfers", "transfer-fees",
        "exchange-rates", "bank-wire", "fintech-transfer", "moving-savings",
        "transfer-speed", "transfer-limits", "remittance-scams"
    )):
        callout = (
            '<div class="info-box revenue-tool-callout"><strong>Compare transfer costs:</strong> '
            'Use the <a href="/country-tools/money-transfer-fee-calculator/">International Money Transfer Fee Calculator</a> '
            'to model fees and FX markup using your own transfer amount and reference rate.</div>'
        )
    else:
        return text

    if callout in text:
        return text

    pattern = r'(<section\b[^>]*class=["\'][^"\']*\bquick-answer\b[^"\']*["\'][^>]*>[\s\S]*?</section>)'
    return re.sub(pattern, r'\1' + callout, text, count=1, flags=re.I)

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
    # Prefer the URL slug because it is canonical and ASCII-safe.
    href = re.search(r'\bhref=["\'][^"\']*country/([^/"\']+)/index\.html["\']', card_html, flags=re.I)
    if href:
        return href.group(1).strip().lower()
    data = re.search(r'\bdata-country=["\']([^"\']+)["\']', card_html, flags=re.I)
    if data:
        value = data.group(1).strip().lower()
        value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
        return value
    return None

def country_image_for_slug(slug: str):
    if not slug:
        return None
    filename = COUNTRY_IMAGES.get(slug)
    if filename:
        return COUNTRY_AI_IMAGE_BASE + filename
    # CountryPilot already has a dedicated complete-guide graphic for every
    # country desk. Use it for all remaining countries so every destination
    # receives relevant, correctly matched artwork.
    return COUNTRY_FALLBACK_IMAGE_BASE + slug + "-complete-country-travel-guide.svg"

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
    image = country_image_for_slug(slug or "")
    if not image:
        return card_html

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
    if slug not in COUNTRY_IMAGES:
        opening = add_class_to_opening_tag(opening, "country-fallback-graphic")
    opening = add_style_to_opening_tag(opening, f"background-image:url('{image}')")
    return opening + card_html[open_match.end():]

def apply_country_page_hero(text: str, path: Path):
    parts = path.as_posix().split("/")
    if len(parts) < 3 or parts[0] != "country" or parts[-1] != "index.html":
        return text
    slug = parts[1].lower()
    image = country_image_for_slug(slug)
    if not image:
        return text
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

    # Repair CountryPilot Organization structured data consistently.
    repaired_text = text.replace(
        '"@type":"Organization","@id":"https://countrypilot.info/#organization","name":"CountryPilot","url":"https://countrypilot.info/"',
        '"@type":"Organization","@id":"https://countrypilot.info/#organization","name":"CountryPilot","url":"https://countrypilot.info/","logo":{"@type":"ImageObject","url":"https://countrypilot.info/images/countrypilot-mark.svg"}'
    )
    repaired_text = repaired_text.replace(
        '"author":{"@type":"Organization","name":"CountryPilot Editorial Team","url":"https://countrypilot.info/authors/countrypilot-editorial-team/"',
        '"author":{"@type":"Organization","name":"CountryPilot Editorial Team","url":"https://countrypilot.info/authors/countrypilot-editorial-team/","logo":{"@type":"ImageObject","url":"https://countrypilot.info/images/countrypilot-mark.svg"}'
    )
    if repaired_text != text:
        text = repaired_text
        changed = True

    priority_text = optimize_priority_article_title(text, path)
    if priority_text != text:
        text = priority_text
        changed = True

    next_batch_text = optimize_next_batch_seo(text, path)
    if next_batch_text != text:
        text = next_batch_text
        changed = True

    priority_links_text = inject_priority_article_links(text, path)
    if priority_links_text != text:
        text = priority_links_text
        changed = True

    priority_hub_text = inject_priority_country_hub(text, path)
    if priority_hub_text != text:
        text = priority_hub_text
        changed = True

    footer_text = inject_us_footer_destination(text)
    if footer_text != text:
        text = footer_text
        changed = True

    revenue_text = inject_revenue_tool_callout(text, path)
    if revenue_text != text:
        text = revenue_text
        changed = True

    proof_cta_text = inject_proof_funds_cta(text, path)
    if proof_cta_text != text:
        text = proof_cta_text
        changed = True

    if SOCIAL_MARKER not in text and "</head>" in text:
        text = text.replace("</head>", SOCIAL_TAG + "\n</head>", 1)
        social_updated += 1
        changed = True

    if COUNTRY_STYLE_MARKER not in text and "</head>" in text:
        text = text.replace("</head>", COUNTRY_STYLE_TAG + "\n</head>", 1)
        changed = True

    if CARD_STYLE_MARKER not in text and "</head>" in text:
        text = text.replace("</head>", CARD_STYLE_TAG + "\n</head>", 1)
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

refresh_priority_sitemaps()

print(f"CountryPilot article layout fix injected into {article_updated} article pages.")
print(f"CountryPilot social favicon styling injected into {social_updated} HTML pages.")
print(f"CountryPilot AI topic images applied to {cards_updated} editorial cards across {card_pages_updated} pages.")
print(f"CountryPilot country images applied to {country_cards_updated} country cards across {country_card_pages_updated} pages.")
print(f"CountryPilot country hero images applied to {country_hero_pages_updated} country pages.")
print(f"Skipped {skipped} files.")
