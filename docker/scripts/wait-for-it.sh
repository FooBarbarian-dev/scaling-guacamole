#!/usr/bin/env bash
# wait-for-it.sh — Wait for a TCP host:port to become available
# Usage: wait-for-it.sh HOST PORT [--timeout=SECONDS]

set -euo pipefail

HOST="${1:-localhost}"
PORT="${2:-5432}"
TIMEOUT=30

# Parse optional arguments
shift 2 || true
for arg in "$@"; do
    case $arg in
        --timeout=*)
            TIMEOUT="${arg#*=}"
            ;;
    esac
done

echo "Waiting for ${HOST}:${PORT} (timeout: ${TIMEOUT}s)..."

start_time=$(date +%s)
while ! bash -c "echo > /dev/tcp/${HOST}/${PORT}" 2>/dev/null; do
    elapsed=$(( $(date +%s) - start_time ))
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "Timeout reached waiting for ${HOST}:${PORT}"
        exit 1
    fi
    sleep 1
done

echo "${HOST}:${PORT} is available."
