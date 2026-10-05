# CountryPilot — AdSense activation checklist

Prepared: 2026-10-05

## Already implemented in this package
- Expanded About, Contact, Privacy, Editorial, Sources, Corrections and Disclaimer pages.
- Contact email: hello@countrypilot.info.
- Facebook page: https://www.facebook.com/profile.php?id=61594161803722
- Site-wide trust links in the footer.
- CountryPilot Editorial Team author profile and linked article bylines.
- Transparent disclosure that software/AI assistance may be used and is not treated as a source.
- Article source-role labels and source-quality notes.
- Blanket “Last verified” wording replaced with truthful “Page updated” wording.
- 404 and Search pages marked noindex and data-ad-eligible=false.
- No AdSense code is inserted before an account-specific publisher ID exists.

## Must be completed inside AdSense after the site/account is approved or connected
1. Get the real AdSense publisher ID (ca-pub-...).
2. Add the exact AdSense site verification/ad code supplied by Google.
3. Configure a Google-certified CMP for EEA/UK/Switzerland traffic (Google Privacy & messaging or another certified TCF CMP) before personalized ads are served there.
4. Create /ads.txt using the exact seller line supplied in AdSense. Do not guess the publisher ID.
5. Keep ad code off /404.html and /search/ unless a results page has substantial publisher content and placement is separately reviewed.
6. Review Auto Ads placement so ads do not cover navigation, article text, buttons or other controls.

## Typical ads.txt format after AdSense supplies your ID
```
google.com, pub-REPLACE_WITH_REAL_ID, DIRECT, f08c47fec0942fa0
```
Do not upload this example as a live ads.txt record until the actual publisher ID is known.
