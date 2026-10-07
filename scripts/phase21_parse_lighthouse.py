from pathlib import Path
import json, statistics, re

root=Path("docs/performance/lighthouse")
raw=[]
for p in sorted(root.glob("route-*.json")):
    try:
        d=json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    audits=d.get("audits",{})
    cats=d.get("categories",{})
    m=re.match(r"route-(\d+)-(\d+)\.json$",p.name)
    if not m:
        continue
    raw.append({
        "route":int(m.group(1)),
        "run":int(m.group(2)),
        "file":p.name,
        "url":d.get("finalDisplayedUrl") or d.get("finalUrl"),
        "performance_score":round((cats.get("performance",{}).get("score") or 0)*100),
        "lcp_ms":round(audits.get("largest-contentful-paint",{}).get("numericValue") or 0),
        "cls":float(audits.get("cumulative-layout-shift",{}).get("numericValue") or 0),
        "tbt_ms":round(audits.get("total-blocking-time",{}).get("numericValue") or 0),
        "fcp_ms":round(audits.get("first-contentful-paint",{}).get("numericValue") or 0),
        "speed_index_ms":round(audits.get("speed-index",{}).get("numericValue") or 0),
    })

results=[]
for route in sorted({r["route"] for r in raw}):
    rows=[r for r in raw if r["route"]==route]
    def med(k):
        return statistics.median([r[k] for r in rows])
    results.append({
        "route":route,
        "url":rows[0]["url"],
        "runs":len(rows),
        "median_performance_score":round(med("performance_score")),
        "median_lcp_ms":round(med("lcp_ms")),
        "median_cls":round(med("cls"),4),
        "median_tbt_ms":round(med("tbt_ms")),
        "median_fcp_ms":round(med("fcp_ms")),
        "median_speed_index_ms":round(med("speed_index_ms")),
        "individual_runs":rows,
    })

summary={
  "generated_by":"3-run median Lighthouse mobile audit via GitHub Actions",
  "routes_tested":len(results),
  "total_lighthouse_runs":len(raw),
  "results":results,
}
(root/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
lines=["# Phase 21 Lighthouse median summary","","| Route | Runs | Perf median | LCP ms | CLS | TBT ms | FCP ms |","|---|---:|---:|---:|---:|---:|---:|"]
for r in results:
    lines.append(f"| {r['url']} | {r['runs']} | {r['median_performance_score']} | {r['median_lcp_ms']} | {r['median_cls']} | {r['median_tbt_ms']} | {r['median_fcp_ms']} |")
(root/"summary.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
