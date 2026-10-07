# CountryPilot Mission — Phase 19: CMP / Consent / ads.txt / Ad Implementation

**Started:** 2026-10-07  
**Status:** ACTIVE — site-side controls complete; AdSense account-side CMP/Auto Ads verification still required.

## Strict completion rule
Phase 19 must NOT be marked complete until all of the following are verified:
1. AdSense publisher code is deployed correctly on ad-eligible pages.
2. Search and 404 are excluded from ad serving.
3. ads.txt is correct and live at the root.
4. A Google-certified CMP integrated with the IAB TCF is published for CountryPilot for EEA/UK/Switzerland traffic.
5. Consent choices and consent revocation are available as required.
6. Auto Ads or another deliberate ad-unit implementation is enabled in the AdSense account.
7. Ad placement is reviewed so ads do not obstruct navigation, article text, buttons or other controls.

## Site-side controls — VERIFIED
- Publisher ID: ca-pub-2387877582529863.
- Current AdSense publisher script is present on all 2,028 ad-eligible HTML pages audited in Phase 18.
- Search and 404 are noindex and contain no AdSense publisher script.
- No manual adsbygoogle ad-unit markup is present in the repository. The site is therefore prepared for AdSense Auto Ads rather than a mixed manual-unit implementation.
- Root ads.txt contains exactly:
  google.com, pub-2387877582529863, DIRECT, f08c47fec0942fa0
- Privacy policy discloses Google advertising, cookies/local storage, personalized advertising, consent and EEA/UK/Switzerland treatment.
- Trust/footer infrastructure and ad-readiness checks passed in Phase 18.
- No repository-level fundingchoices/googlefc/TCF implementation is present. This does NOT by itself prove the Google CMP is absent because Google Privacy & messaging messages are configured account-side and use the existing AdSense code on web.

## Current Google requirements verified 2026-10-07
Google requires publishers using AdSense to use a Google-certified CMP integrated with the IAB Transparency & Consent Framework when serving personalized ads to users in the EEA, UK and Switzerland.

Google's own CMP is configured in AdSense under Privacy & messaging. For web, Google instructs publishers to have the AdSense code placed on the site, then create and publish a European regulations message for the selected site and privacy-policy URL.

Google's Privacy & messaging program also requires consent revocability. When a European regulations message is active on an approved site with AdSense code, Google automatically adds the required privacy/cookie-settings revocation link; publishers can optionally expose the revocation function themselves.

## Account-side controls — NOT YET VERIFIED
These cannot be inferred from GitHub source and there is no connected AdSense account tool in this chat.

### A. European regulations CMP
In AdSense:
- Privacy & messaging
- European regulations
- Create/Manage message
- Select countrypilot.info
- Privacy policy URL: https://countrypilot.info/privacy/
- Publish the message
- Use the Google CMP or another Google-certified TCF CMP
- Review English and any additional languages
- Confirm the desired Do not consent / manage-options behavior

Recommended account safety control:
- Review the current "Maximize message coverage" setting so missing TC-string cases do not silently reduce eligible EEA/UK/Swiss monetization.

### B. Auto Ads
In AdSense:
- Ads
- countrypilot.info
- Edit
- Turn on Auto ads
- Use the preview on mobile and desktop
- Review in-page, anchor, side-rail, vignette and Multiplex formats
- Add page or area exclusions if any placement overlaps navigation, buttons or article content
- Apply to site

The repository has no manual ad units; if Auto Ads is OFF, the publisher script alone does not create a deliberate manual placement strategy.

## Account evidence searched
A connected Gmail search for recent AdSense messages returned no matching mail, so email did not provide independent confirmation of CMP publication, Auto Ads status or AdSense approval state.

## Completion boundary
Do not mark Phase 19 complete until account-side CMP publication and Auto Ads/ad-placement status are directly verified.

No code change can substitute for those AdSense account settings.


## 2026-10-07 follow-up verification
- Re-checked available ChatGPT integrations: no direct Google AdSense account connector is available.
- Searched the connected Gmail account for recent AdSense/Google AdSense messages: no matching messages were found.
- Therefore CMP publication, Auto Ads state and live placement cannot be inferred or truthfully marked complete.
- Site-side implementation remains complete and unchanged.
- Phase 19 is now classified as **ACCOUNT-ACCESS BLOCKED / NOT GREEN** until direct AdSense account access is available.
