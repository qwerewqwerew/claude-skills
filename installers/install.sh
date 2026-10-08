#!/bin/sh
# Shared implementation for macOS and Linux. Invoke with sh.
set -eu
repo=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec python3 "$repo/tools/manage.py" "$@"
