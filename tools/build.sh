#!/usr/bin/env bash
# Baut die Seiten neu, prüft sie und packt site/ als ZIP (Reserve für einen manuellen Upload).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/build.py
python3 tools/check.py
mkdir -p dist
rm -f dist/auraarbor-website.zip
(cd site && zip -qr ../dist/auraarbor-website.zip . -x '.DS_Store')
echo "dist/auraarbor-website.zip erstellt"
