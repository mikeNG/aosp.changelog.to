#!/bin/bash
#
# Serve the published changelog site locally for preview.
#
# Usage:
#   ./serve.sh [publish_dir] [port]
#
# Environment overrides:
#   PUBLISH_DIR  directory to serve (default: ../gh-pages, next to this script)
#   HOST         interface to bind  (default: 127.0.0.1)
#   PORT         port to listen on  (default: 8000)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

PUBLISH_DIR="${1:-${PUBLISH_DIR:-$SCRIPT_DIR/../gh-pages}}"
PORT="${2:-${PORT:-8000}}"
HOST="${HOST:-127.0.0.1}"

if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is required to serve the site locally." >&2
    exit 1
fi

if [ ! -d "$PUBLISH_DIR" ]; then
    echo "Publish directory not found: $PUBLISH_DIR" >&2
    exit 1
fi

PUBLISH_DIR="$(cd "$PUBLISH_DIR" && pwd -P)"

echo "Serving $PUBLISH_DIR"
echo "  http://$HOST:$PORT/"
echo "Press Ctrl+C to stop."

cd "$PUBLISH_DIR"
exec python3 -m http.server "$PORT" --bind "$HOST"
