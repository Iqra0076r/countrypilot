# Phase 21 — Performance / Core Web Vitals — progress

**Updated:** 2026-10-07
**Status:** YELLOW / NOT CLOSED

## Audit findings
Representative templates use only the two intended shared stylesheets:
- `/assets/countrypilot-core.css` — about 72.9 KB source
- `/assets/countrypilot-premium.css` — about 27.5 KB source

Representative image loading audit:
- Homepage: 11 images, 10 lazy-loaded; the remaining image is the brand logo.
- Countries directory: 196 images, 195 lazy-loaded; the remaining image is the brand logo.
- Visa category template: lead editorial image is `loading="eager"` + `fetchpriority="high"`.
- Canada country hub: lead editorial image is `loading="eager"` + `fetchpriority="high"`.
- Priority article/tool examples contain no unnecessary below-the-fold eager image loading.

Existing layout-stability safeguards include explicit logo dimensions, width/height on static imagery, responsive 16:9 article media, mobile overflow controls, and tested responsive navigation.

## Safe improvement made
The homepage visual LCP candidate is a CSS background:
`/images/travel-tools-planning.webp` (212,632 bytes).

Because CSS-background images are discovered only after stylesheet processing, the homepage now explicitly preloads this image with high fetch priority.

Commit: `957323c1a02046ea02e89a0e83d0545515684aa1`

## Cloudflare delivery audit
Verified on the zone:
- Brotli: ON
- HTTP/2: ON
- HTTP/3: ON
- TLS 1.3: ON
- cache level: aggressive
- development mode: OFF
- RUM/Web Analytics: ON
- browser cache TTL: 14,400 seconds
- edge cache TTL: 7,200 seconds

Speed Brain is OFF. An attempted API enable was rejected with Cloudflare authentication error, so no unverified account change is claimed.

## Why Phase 21 is still yellow
The repo-side safe optimization pass is materially advanced, but a strict Core Web Vitals closeout still needs verifiable lab or field measurements after deployment (LCP, INP and CLS) and confirmation that no remaining actionable regression exists. The current connected tools do not expose those field metrics and the public-site fetch path used in this run could not inspect the live HTML.

Do not mark Phase 21 green merely because the preload commit succeeded.


## 2026-10-07 deep optimization pass

### Live Lighthouse evidence
A GitHub Actions Lighthouse workflow now audits five representative production routes:
- homepage
- Canada country hub
- Visas & Immigration category
- Canada LMIA priority article
- Canada CRS calculator

Evidence lives under `docs/performance/lighthouse/`.

The pass found render-blocking legacy CSS injected during `postinstall`. Four legacy override files were consolidated into `assets/countrypilot-premium.css`, and `scripts/inject-article-layout-fix.py` was changed so those styles are no longer injected as separate requests.

After deployment, representative runs reached:
- category: up to 98 performance, ~2.2s LCP, CLS 0
- priority article: 98 performance, ~2.1s LCP, CLS 0
- calculator: 98 performance, ~2.1s LCP, CLS 0
- country hub: up to 94 performance, CLS 0
- homepage: synthetic results remained variable; one stable post-fix run showed ~2.9s LCP and CLS 0, but TBT was elevated by third-party ad execution

A direct-image homepage experiment caused a CLS regression and was immediately rolled back. The stable background-hero structure is restored with a lighter 153 KB asset.

### Cloudflare delivery / runtime verification
The live site is served by Cloudflare Worker `countrypilot5` with static assets, routed to both:
- `countrypilot.info/*`
- `www.countrypilot.info/*`

The Worker was observed updating after the performance commits, and the Lighthouse workflow now gates on the optimized live deployment before testing.

### Remaining strict closeout boundary
Cloudflare documentation confirms Web Analytics RUM collects real-user LCP, INP and CLS. RUM is enabled for CountryPilot. However, the current Cloudflare connector exposes RUM/Web Analytics configuration but not the Core Web Vitals metric table itself.

Therefore Phase 21 remains NOT GREEN under the strict rule until real-user LCP/INP/CLS values can be directly read/verified. Code-side performance work is not left undone; the remaining item is metric access/observation.
