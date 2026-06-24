#!/usr/bin/env bash
# Fetch an arXiv listing into arxiv_scroll/digests/YYYY-MM-DD.raw.json
#
# Usage:
#   ./fetch.sh "https://arxiv.org/list/astro-ph/new"
#   ./fetch.sh "https://arxiv.org/list/astro-ph/new" 2026-06-24
#   ./fetch.sh "URL" 2026-06-24 --with-abstracts

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=paths.env
source "${ROOT}/paths.env"

URL="${1:?Usage: ./fetch.sh <arxiv-list-url> [YYYY-MM-DD] [--with-abstracts]}"
shift

DATE="$(date +%Y-%m-%d)"
EXTRA=()
for arg in "$@"; do
  case "$arg" in
    --with-abstracts) EXTRA+=(--with-abstracts) ;;
    *) DATE="$arg" ;;
  esac
done

OUT="${ARXIV_DIGESTS_DIR}/${DATE}.raw.json"
mkdir -p "${ARXIV_DIGESTS_DIR}"

echo "Listing:  ${URL}"
echo "Output:   ${OUT}"
echo "Script:   ${ARXIV_FETCH_SCRIPT}"
if ((${#EXTRA[@]})); then
  python3 "${ARXIV_FETCH_SCRIPT}" "${URL}" "${EXTRA[@]}" -o "${OUT}"
else
  python3 "${ARXIV_FETCH_SCRIPT}" "${URL}" -o "${OUT}"
fi

python3 - <<PY
import json
d = json.load(open("${OUT}"))
print(f"papers: {d['count']}, abstracts_missing: {d.get('abstracts_missing', '?')}")
PY
