#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(".")

NAV = '''<nav class="site-nav" aria-label="Primary navigation"><div class="container nav-inner"><div class="nav-scroll"><a href="/category/visas-immigration/">Visas &amp; Immigration</a><a href="/category/study-abroad/">Study Abroad</a><a href="/category/visa-sponsorship-jobs/">Sponsorship Jobs</a><a href="/category/jobs-work-permits/">Work &amp; Permits</a><a href="/countries/">195 Countries</a><details class="nav-more"><summary>More</summary><div class="nav-more-panel"><a href="/category/scholarships-funding/">Scholarships &amp; Funding</a><a href="/category/pr-citizenship/">PR &amp; Citizenship</a><a href="/category/relocation/">Relocation</a><a href="/category/banking/">Banking</a><a href="/country-tools/">Free Tools</a><a href="/moving-abroad/">Moving Abroad</a><a class="nav-more-search" href="/search/">Search CountryPilot →</a></div></details></div><button aria-controls="countryPilotMobileNav" aria-expanded="false" aria-label="Open navigation menu" class="nav-menu" type="button"><span aria-hidden="true" class="menu-icon">☰</span><span>Menu</span></button></div></nav><div aria-hidden="true" aria-label="Mobile navigation" class="mobile-nav" id="countryPilotMobileNav"><div class="mobile-nav-grid"><div class="mobile-nav-group"><b>Plan</b><a href="/category/visas-immigration/">Visas &amp; Immigration</a><a href="/category/study-abroad/">Study Abroad</a><a href="/category/scholarships-funding/">Scholarships &amp; Funding</a><a href="/category/pr-citizenship/">PR &amp; Citizenship</a></div><div class="mobile-nav-group"><b>Work &amp; Move</b><a href="/category/visa-sponsorship-jobs/">Visa Sponsorship Jobs</a><a href="/category/jobs-work-permits/">Jobs &amp; Work Permits</a><a href="/category/relocation/">Relocation</a><a href="/moving-abroad/">Moving Abroad</a></div><div class="mobile-nav-group"><b>Explore</b><a href="/countries/">195 Countries</a><a href="/category/banking/">Banking</a><a href="/country-tools/">Free Tools</a><a href="/search/">Search CountryPilot</a></div></div></div>'''

def replace_navigation(text: str) -> str:
    start = text.find('<nav class="site-nav"')
    if start < 0:
        return text
    main = text.find("<main", start)
    ticker = text.find('<div class="ticker"', start)
    candidates = [x for x in (main, ticker) if x >= 0]
    if not candidates:
        return text
    end = min(candidates)
    return text[:start] + NAV + text[end:]

changed = 0
missing = []
for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    if '<nav class="site-nav"' not in text:
        missing.append(str(path))
        continue
    new = replace_navigation(text)
    new = new.replace(
        "/assets/countrypilot-premium.css?v=20261006-ui1",
        "/assets/countrypilot-premium.css?v=20261006-nav2",
    )
    new = new.replace(
        "/assets/countrypilot-premium.css?v=20261006-ui2",
        "/assets/countrypilot-premium.css?v=20261006-nav2",
    )
    if new != text:
        path.write_text(new, encoding="utf-8")
        changed += 1

print(f"Changed {changed} HTML files")
print(f"HTML files without site-nav: {len(missing)}")
if missing:
    print("\n".join(missing[:20]))

# production deployment sync after navigation migration
