# CountryPilot

Deployment source for https://countrypilot.info/.

## Cloudflare Pages

Use these settings when connecting this repository to Cloudflare Pages:

- Production branch: `main`
- Build command: `bash build.sh`
- Build output directory: `dist`
- Root directory: repository root

The full static site is stored as four archive parts under `.site-parts/`. The build script joins those parts into the CountryPilot ZIP and extracts the complete site into `dist/`.

## Site archive parts

Expected files:

- `.site-parts/CountryPilot.zip.part-00`
- `.site-parts/CountryPilot.zip.part-01`
- `.site-parts/CountryPilot.zip.part-02`
- `.site-parts/CountryPilot.zip.part-03`

Do not rename the parts. Cloudflare will automatically rebuild after commits to `main`.
