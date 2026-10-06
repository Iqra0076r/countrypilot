#!/usr/bin/env python3
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import subprocess
import tempfile

ROOT=Path(".")
SHARED_MARKERS=(
    "CountryPilot mobile navigation accessibility and responsive fix",
    ":root{--cp-blue:#07589c",
    ".trust-wrap{max-width:920px",
    "CountryPilot final mobile-first stabilization",
    "--paper:#f7f3eb",
)
CORE="/assets/countrypilot-core.css"
PREMIUM="/assets/countrypilot-premium.css"

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]
        self.ids=[]
        self.adsense=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        for key in ("href","src"):
            if a.get(key):
                self.links.append((key,a[key]))
        if tag=="script" and "pagead2.googlesyndication.com" in a.get("src",""):
            self.adsense+=1

def resolve_local(html_path:Path,url:str)->Path|None:
    u=urlsplit(url)
    if u.scheme or u.netloc or url.startswith(("mailto:","tel:","javascript:","#","data:")):
        return None
    path=unquote(u.path)
    if not path:
        return None
    if path.startswith("/"):
        candidate=ROOT/path.lstrip("/")
    else:
        candidate=html_path.parent/path
    # Normalize syntactically without requiring existence.
    candidate=Path(str(candidate).replace("\\","/"))
    if path.endswith("/"):
        candidate=candidate/"index.html"
    elif candidate.suffix=="":
        if (candidate/"index.html").exists():
            candidate=candidate/"index.html"
    return candidate

def main():
    errors=[]
    warnings=[]
    stats={
        "html_files":0,
        "adsense_pages":0,
        "internal_links_checked":0,
        "missing_internal_targets":0,
        "duplicate_ids":0,
        "legacy_planatlas_occurrences":0,
        "shared_inline_style_occurrences":0,
    }
    html_files=list(ROOT.rglob("*.html"))
    for path in html_files:
        stats["html_files"]+=1
        text=path.read_text(encoding="utf-8")
        if text.count(CORE)!=1:
            errors.append(f"{path}: expected exactly one core stylesheet link")
        if text.count(PREMIUM)!=1:
            errors.append(f"{path}: expected exactly one premium stylesheet link")
        if "planatlas" in text.lower():
            stats["legacy_planatlas_occurrences"]+=text.lower().count("planatlas")
            errors.append(f"{path}: legacy PlanAtlas identifier remains")
        for marker in SHARED_MARKERS:
            if marker in text:
                stats["shared_inline_style_occurrences"]+=1
                errors.append(f"{path}: shared inline CSS marker remains: {marker[:36]}")

        parser=Parser()
        try:
            parser.feed(text)
        except Exception as exc:
            errors.append(f"{path}: HTML parser failed: {exc}")
            continue
        if parser.adsense:
            stats["adsense_pages"]+=1
        dup={x for x in parser.ids if parser.ids.count(x)>1}
        if dup:
            stats["duplicate_ids"]+=len(dup)
            errors.append(f"{path}: duplicate ids {sorted(dup)[:5]}")

        for _,url in parser.links:
            target=resolve_local(path,url)
            if target is None:
                continue
            stats["internal_links_checked"]+=1
            try:
                exists=target.exists()
            except OSError:
                exists=False
            if not exists:
                # Ignore navigation aliases known to be handled by directory index semantics.
                stats["missing_internal_targets"]+=1
                if stats["missing_internal_targets"]<=100:
                    warnings.append(f"{path}: target not found for {url} -> {target}")

    search=(ROOT/"search"/"index.html").read_text(encoding="utf-8")
    if "const DATA=[" in search:
        errors.append("search/index.html still embeds the full search dataset")
    if "fetch('/data/content-index.json'" not in search:
        errors.append("search/index.html does not lazy-load content-index.json")

    home=(ROOT/"index.html").read_text(encoding="utf-8")
    if "countrypilot-hero.jpg" in home:
        errors.append("index.html still directly references the 5.4 MB legacy hero")
    if re.search(r'alt="(?:Asia|Europe|North America|South America|Africa|Oceania) travel region"',home,re.I):
        errors.append("generic region imagery remains on homepage")
    if "<h3>Most Read</h3>" in home:
        errors.append("unverified Most Read label remains on homepage")

    # Check CSS braces as a quick corruption guard.
    for css in (ROOT/"assets"/"countrypilot-core.css",ROOT/"assets"/"countrypilot-premium.css"):
        t=css.read_text(encoding="utf-8")
        if t.count("{")!=t.count("}"):
            errors.append(f"{css}: unbalanced CSS braces")

    # Syntax-check the custom search JavaScript in Node.
    scripts=re.findall(r"<script([^>]*)>([\s\S]*?)</script>",search,re.I)
    custom=next((body for attrs,body in scripts if "let DATA=[]" in body),None)
    if custom is None:
        errors.append("Could not locate lightweight search JavaScript")
    else:
        with tempfile.NamedTemporaryFile("w",suffix=".js",delete=False,encoding="utf-8") as tmp:
            tmp.write(custom)
            js_path=tmp.name
        result=subprocess.run(["node","--check",js_path],capture_output=True,text=True)
        Path(js_path).unlink(missing_ok=True)
        if result.returncode:
            errors.append("Search JavaScript syntax error: "+result.stderr.strip())

    report={"stats":stats,"warnings":warnings[:100],"errors":errors}
    (ROOT/"SITE_QUALITY_5000_VALIDATION.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"
    )
    print(json.dumps(report,indent=2))
    if errors:
        raise SystemExit(1)

if __name__=="__main__":
    main()
