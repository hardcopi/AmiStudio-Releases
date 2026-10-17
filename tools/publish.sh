#!/bin/sh
# tools/publish.sh APP VER dist/AmiStudio<App>-<VER>.lha [--variant NAME FILE] [--extra FILE] [--beta] [--notes FILE] [--publish]
# For app bots. Without --publish it is a dry run that prints the release, SHA256SUMS and the new manifest block.
# Only add --publish when Rich has said to publish this version. See README.md "Publishing".
cd "$(dirname "$0")/.." || exit 1
exec python3 tools/amsrel.py publish "$@"
