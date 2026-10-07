# CountryPilot Mission — Phase 14: Google Indexing Activation

**Started:** 2026-10-07  
**Status:** ACTIVE — do not mark complete until all Phase-14 priority URLs are indexed.

## Strict completion rule
Phase 14 is complete only when **59/59 priority URLs** in `sitemap-priority.xml` are reported indexed by Google Search Console. Successful sitemap submission, discovery, crawling, or “Discovered — currently not indexed” does **not** count as completion.

## Phase-14 priority set
The set contains:
- 48 unique four-market keyword/target pages.
- 4 priority country hubs: US, UK, Canada, Australia.
- 3 priority category hubs: Visas & Immigration, Visa Sponsorship Jobs, Jobs & Work Permits.
- Canada LMIA guide.
- Australia Visa Sponsorship Jobs guide.
- Canada CRS score resource.
- US Diversity Visa verification guide.

Total: **59 unique URLs**.

## Technical/indexability checks completed
- 59/59 pages have a valid canonical matching the target URL.
- 59/59 have no `noindex` directive.
- 59/59 have valid HTML doctype, title and H1.
- 0 orphan pages in the priority crawl graph.
- Weak crawl paths were strengthened from relevant country/tool hubs.
- `sitemap-priority.xml` was created and added to the sitemap index.
- Google Search Console accepted the focused sitemap and sitemap index with 0 errors / 0 warnings at submission.

## Content-quality closeout
A 59-page quality audit identified six thin pages and six near-duplicate pairs. All controllable flags were then fixed.

### Former thin pages — current word counts
- US Immigration Lawyer Cost Planner: 617 words.
- Visa Document Checklist: 532 words.
- UK Skilled Worker Visa Cost Calculator: 674 words.
- Canada Study Permit Proof of Funds Calculator: 632 words.
- Moving Abroad from Canada: 722 words.
- Canada CRS score resource: 672 words.

### Former near-duplicate pairs — current Jaccard similarity
- Australia Choosing a University vs Academic Intakes: 0.524.
- Australia Scholarship Eligibility vs PhD Scholarships: 0.469.
- Moving Abroad Canada vs Australia: 0.357.
- Moving Abroad US vs Australia: 0.337.
- Moving Abroad US vs Canada: 0.338.
- US IT Sponsorship Jobs vs US Work Permit Guide: 0.437.

Configured concern threshold: 0.55. All flagged pairs are now below it.

## Current external dependency
Google decides when and whether eligible pages are crawled and indexed. CountryPilot cannot force Google indexing through the Search Console API. The indexing tracker remains the source of truth.

## Rule
Do not mark Phase 14 green until **59/59 indexed**. Until then, status is ACTIVE.

## Live GSC recheck and sitemap repair — 2026-10-07 22:50 PKT
- Exact priority-set reconciliation refreshed from Google URL Inspection history: **0/59 indexed, 17 discovered — currently not indexed, 42 unknown to Google**.
- A source audit found literal `\\n` escape text inside `sitemap-core.xml` and `sitemap-money.xml` near recently appended URLs.
- `sitemap-core.xml` repaired in commit `3dc7ceb5591d6b967eef5bdde551090ddcb35bc6`.
- `sitemap-money.xml` repaired in commit `fb0cd86424dc58a2f8b171b69148028a00b4ad43`.
- `sitemap.xml`, `sitemap-core.xml`, `sitemap-money.xml`, and `sitemap-priority.xml` were re-submitted through Google Search Console.
- The sitemap index, core and money submissions showed 0 warnings / 0 errors at re-submission. The priority sitemap still surfaced the previously recorded 1 error while pending a fresh Google download, so it must be rechecked after Google refetches it.
- Phase 14 remains ACTIVE under the strict **59/59 indexed** completion rule.
