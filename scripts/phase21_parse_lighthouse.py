from pathlib import Path
import json

root=Path("docs/performance/lighthouse")
rows=[]
for p in sorted(root.glob("*.json")):
    try:
        d=json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    audits=d.get("audits",{})
    cats=d.get("categories",{})
    rows.append({
        "file":p.name,
        "url":d.get("finalDisplayedUrl") or d.get("finalUrl"),
        "performance_score":round((cats.get("performance",{}).get("score") or 0)*100),
        "lcp_ms":round(audits.get("largest-contentful-paint",{}).get("numericValue") or 0),
        "cls":round(audits.get("cumulative-layout-shift",{}).get("numericValue") or 0,4),
        "tbt_ms":round(audits.get("total-blocking-time",{}).get("numericValue") or 0),
        "fcp_ms":round(audits.get("first-contentful-paint",{}).get("numericValue") or 0),
        "speed_index_ms":round(audits.get("speed-index",{}).get("numericValue") or 0),
    })
summary={
  "generated_by":"Lighthouse CI-style GitHub Actions audit",
  "routes_tested":len(rows),
  "results":rows,
}
(root/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")

lines=["# Phase 21 Lighthouse summary","","| Route | Perf | LCP ms | CLS | TBT ms | FCP ms |","|---|---:|---:|---:|---:|---:|"]
for r in rows:
    lines.append(f"| {r['url']} | {r['performance_score']} | {r['lcp_ms']} | {r['cls']} | {r['tbt_ms']} | {r['fcp_ms']} |")
(root/"summary.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
