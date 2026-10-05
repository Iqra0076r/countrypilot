#!/usr/bin/env bash
set -euo pipefail

mkdir -p dist
rm -rf dist/*

cat .site-parts/CountryPilot.zip.part-* > /tmp/CountryPilot-site.zip
unzip -q /tmp/CountryPilot-site.zip -d dist

echo "CountryPilot site unpacked to dist/"
