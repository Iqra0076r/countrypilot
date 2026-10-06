#!/usr/bin/env python3
"""
CountryPilot $5k UI/performance refactor.

This script deliberately does NOT rewrite article copy, SEO metadata, canonicals,
schema, AdSense code, sitemaps or source citations. It only normalizes the
presentation layer and a few trust/UX labels.

Main effects:
1. Extracts the repeated five-block inline design system into one cacheable CSS.
2. Loads the premium design layer after the compatibility core.
3. Replaces legacy PlanAtlas DOM ids.
4. Fixes duplicated US footer links and truthful "Popular Guides" labeling.
5. Removes misleading region photos from the homepage (CSS renders editorial tiles).
6. Converts the 1+ MB search page from embedded data to lazy JSON loading.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(".")
CORE = ROOT / "assets" / "countrypilot-core.css"
PREMIUM = "/assets/countrypilot-premium.css?v=20261006-ui1"
CORE_LINK = "/assets/countrypilot-core.css?v=20261006-ui1"

STYLE_RE = re.compile(r"<style(?:\s[^>]*)?>([\s\S]*?)</style>", re.I)
LINK_CORE_RE = re.compile(r'<link[^>]+href=["\']/assets/countrypilot-core\.css[^"\']*["\'][^>]*>\s*', re.I)
LINK_PREMIUM_RE = re.compile(r'<link[^>]+href=["\']/assets/countrypilot-premium\.css[^"\']*["\'][^>]*>\s*', re.I)
LINK_HOME_FIX_RE = re.compile(r'<link[^>]+href=["\']/assets/home-layout-fix\.css[^"\']*["\'][^>]*>\s*', re.I)

STYLE_MARKERS = (
    "CountryPilot mobile navigation accessibility and responsive fix",
    ":root{--cp-blue:#07589c",
    ".trust-wrap{max-width:920px",
    "CountryPilot final mobile-first stabilization",
)

def is_legacy_core(css: str) -> bool:
    return "--paper:#f7f3eb" in css and ".article-body" in css and ".editorial-footer" in css

def is_shared_style(css: str) -> bool:
    return is_legacy_core(css) or any(marker in css for marker in STYLE_MARKERS)

def get_style_blocks(text: str) -> list[str]:
    return [m.group(1) for m in STYLE_RE.finditer(text)]

def choose_block(blocks: list[str], marker: str) -> str:
    for block in blocks:
        if marker in block:
            return block.strip()
    return ""

def build_core_css() -> None:
    if CORE.exists() and CORE.stat().st_size > 45000:
        return

    category = ROOT / "category" / "visas-immigration" / "index.html"
    home = ROOT / "index.html"
    if not category.exists() or not home.exists():
        raise SystemExit("Required source pages are missing; refusing to build shared CSS.")

    category_text = category.read_text(encoding="utf-8")
    home_text = home.read_text(encoding="utf-8")
    blocks = get_style_blocks(category_text)

    legacy_candidates = [b for b in blocks if is_legacy_core(b)]
    if not legacy_candidates:
        raise SystemExit("Could not locate the canonical legacy core style block.")
    legacy = max(legacy_candidates, key=len).strip()

    pieces = [
        "/* CountryPilot compatibility core — extracted from repeated inline styles. */",
        legacy,
        choose_block(blocks, "CountryPilot mobile navigation accessibility and responsive fix"),
        choose_block(blocks, ":root{--cp-blue:#07589c"),
        choose_block(blocks, ".trust-wrap{max-width:920px"),
        choose_block(blocks, "CountryPilot final mobile-first stabilization"),
    ]

    # Homepage had two tiny rules appended to its shorter legacy block.
    home_blocks = get_style_blocks(home_text)
    home_legacy = next((b for b in home_blocks if is_legacy_core(b)), "")
    for selector in (".newsletter-cta", ".newsletter-cta:hover"):
        m = re.search(re.escape(selector) + r"\{[^}]*\}", home_legacy)
        if m:
            pieces.append(m.group(0))

    # Preserve the existing homepage flow repair, but make it cacheable site-wide.
    home_fix = ROOT / "assets" / "home-layout-fix.css"
    if home_fix.exists():
        pieces.append("\n/* Former home-layout-fix.css */\n" + home_fix.read_text(encoding="utf-8"))

    CORE.parent.mkdir(parents=True, exist_ok=True)
    CORE.write_text("\n\n".join(p for p in pieces if p).strip() + "\n", encoding="utf-8")

def strip_shared_styles(text: str) -> tuple[str, int]:
    removed = 0
    def repl(m: re.Match[str]) -> str:
        nonlocal removed
        css = m.group(1)
        if is_shared_style(css):
            removed += len(m.group(0).encode("utf-8"))
            return ""
        return m.group(0)
    return STYLE_RE.sub(repl, text), removed

def ensure_stylesheets(text: str) -> str:
    text = LINK_CORE_RE.sub("", text)
    text = LINK_PREMIUM_RE.sub("", text)
    text = LINK_HOME_FIX_RE.sub("", text)
    tags = (
        f'<link rel="stylesheet" href="{CORE_LINK}"/>'
        f'<link rel="stylesheet" href="{PREMIUM}"/>'
    )
    if "</head>" not in text:
        return text
    return text.replace("</head>", tags + "</head>", 1)

def cleanup_global_markup(text: str) -> tuple[str, dict]:
    counts = {"legacy_ids": 0, "footer_duplicates": 0, "most_read": 0}
    old = text
    text = text.replace("planatlasMobileNav", "countryPilotMobileNav")
    text = text.replace("planatlas-mobile-nav-script", "countrypilot-mobile-nav-script")
    counts["legacy_ids"] = (len(re.findall("planatlasMobileNav", old)) +
                            len(re.findall("planatlas-mobile-nav-script", old)))

    # Some pages contained both an absolute and relative US destination link back-to-back.
    dup_re = re.compile(
        r'(<a href="/country/united-states/">United States</a>)'
        r'<a href="(?:\.\./)*country/united-states/index\.html">United States</a>',
        re.I
    )
    text, n = dup_re.subn(r"\1", text)
    counts["footer_duplicates"] = n

    text, n = re.subn(r"<h3>Most Read</h3>", "<h3>Popular Guides</h3>", text, flags=re.I)
    counts["most_read"] = n
    return text, counts

def cleanup_home(text: str) -> tuple[str, int]:
    # The six region tiles previously used generic topic imagery that did not
    # actually depict the named region. Premium CSS now renders honest abstract tiles.
    region_img_re = re.compile(
        r'<img\s+alt="(?:Asia|Europe|North America|South America|Africa|Oceania) travel region"[^>]*?/?>',
        re.I
    )
    return region_img_re.subn("", text)

def lightweight_search_script() -> str:
    return r"""<script>
let DATA=[];
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function render(){
  const q=$('q').value.toLowerCase().trim(),c=$('cat').value,co=$('country').value;
  const rows=DATA.filter(x=>
    (!q||((x.title||'')+' '+(x.excerpt||'')+' '+(x.category||'')+' '+(x.country||'')).toLowerCase().includes(q))&&
    (!c||x.category_slug===c)&&(!co||x.country_slug===co)
  );
  $('count').textContent=rows.length+' guides';
  $('results').innerHTML=rows.slice(0,72).map(x=>`<article class="editorial-card">
    <a class="card-image" href="../article/${encodeURIComponent(x.slug)}/index.html">
      <img src="${esc(x.image)}" alt="${esc(x.title)}" width="1600" height="900" loading="lazy" decoding="async" onerror="this.style.display='none'">
      <span class="image-fallback">${esc(x.country||x.category)}</span>
    </a>
    <div class="card-copy">
      <div class="eyebrow">${esc(x.country?x.country+' · ':'')}${esc(x.category)}</div>
      <h3><a href="../article/${encodeURIComponent(x.slug)}/index.html">${esc(x.title)}</a></h3>
      <p>${esc(x.excerpt)}</p>
    </div>
  </article>`).join('');
}
async function initSearch(){
  const u=new URL(location.href);
  $('q').value=u.searchParams.get('q')||'';
  $('count').textContent='Loading guides…';
  try{
    const response=await fetch('/data/content-index.json',{cache:'force-cache'});
    if(!response.ok) throw new Error('Search index unavailable');
    DATA=await response.json();
    render();
  }catch(error){
    $('count').textContent='Search is temporarily unavailable';
    $('results').innerHTML='<p>Please use the country and category directories while the search index reloads.</p>';
  }
}
$('searchForm').addEventListener('submit',e=>{e.preventDefault();render()});
$('cat').addEventListener('change',render);
$('country').addEventListener('change',render);
initSearch();
</script>"""

def optimize_search(text: str) -> tuple[str, int]:
    scripts = list(re.finditer(r"<script([^>]*)>([\s\S]*?)</script>", text, re.I))
    target = next((m for m in scripts if m.group(2).lstrip().startswith("const DATA=[")), None)
    if not target:
        return text, 0
    old_bytes = len(target.group(0).encode("utf-8"))
    replacement = lightweight_search_script()
    text = text[:target.start()] + replacement + text[target.end():]
    return text, old_bytes - len(replacement.encode("utf-8"))

def main() -> None:
    build_core_css()
    stats = {
        "html_files": 0,
        "changed_files": 0,
        "html_bytes_before": 0,
        "html_bytes_after": 0,
        "inline_css_bytes_removed": 0,
        "search_embedded_bytes_removed": 0,
        "legacy_ids_replaced": 0,
        "duplicate_footer_links_fixed": 0,
        "most_read_labels_fixed": 0,
        "region_images_removed": 0,
    }

    for path in ROOT.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        before = len(text.encode("utf-8"))
        stats["html_files"] += 1
        stats["html_bytes_before"] += before

        new, removed_css = strip_shared_styles(text)
        stats["inline_css_bytes_removed"] += removed_css
        new = ensure_stylesheets(new)
        new, c = cleanup_global_markup(new)
        stats["legacy_ids_replaced"] += c["legacy_ids"]
        stats["duplicate_footer_links_fixed"] += c["footer_duplicates"]
        stats["most_read_labels_fixed"] += c["most_read"]

        if path == ROOT / "index.html":
            new, n = cleanup_home(new)
            stats["region_images_removed"] += n

        if path == ROOT / "search" / "index.html":
            new, saved = optimize_search(new)
            stats["search_embedded_bytes_removed"] += saved

        after = len(new.encode("utf-8"))
        stats["html_bytes_after"] += after
        if new != text:
            path.write_text(new, encoding="utf-8")
            stats["changed_files"] += 1

    stats["html_mb_before"] = round(stats["html_bytes_before"] / 1048576, 2)
    stats["html_mb_after"] = round(stats["html_bytes_after"] / 1048576, 2)
    stats["html_mb_saved"] = round((stats["html_bytes_before"] - stats["html_bytes_after"]) / 1048576, 2)
    stats["core_css_bytes"] = CORE.stat().st_size
    stats["premium_css_bytes"] = (ROOT / "assets" / "countrypilot-premium.css").stat().st_size
    stats["notes"] = [
        "No article body copy, schema, canonicals, AdSense loader, sitemap or robots directives are rewritten.",
        "The 5.4 MB legacy hero is no longer the computed homepage hero background; a much smaller existing WebP is used.",
        "Search data is loaded from /data/content-index.json instead of embedding ~1 MB of JSON in search/index.html.",
    ]
    (ROOT / "SITE_QUALITY_5000_AUDIT.json").write_text(
        json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main()
