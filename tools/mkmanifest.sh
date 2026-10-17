#!/bin/sh
# tools/mkmanifest.sh [--remote [--sha]]
# Checks manifest.txt and writes manifest.json from it. With --remote, also checks that every released asset is on
# GitHub with the listed size (--sha: downloads them and compares SHA-256).
cd "$(dirname "$0")/.." || exit 1
python3 tools/amsrel.py json || exit 1
python3 tools/amsrel.py check "$@"
