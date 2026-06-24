#!/usr/bin/env bash
# Compile digests/YYYY-MM-DD.tex → PDF
# Usage: ./compile_digest.sh [YYYY-MM-DD]

set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=paths.env
source "${ROOT}/paths.env"

DATE="${1:-$(date +%Y-%m-%d)}"
TEX="${ARXIV_DIGESTS_DIR}/${DATE}.tex"
MACROS_SRC="${ARXIV_LATEX_MACROS:-/Users/Shao/Downloads/daniel/project1/assembly-bias-HOD/.cursor/skills/arxiv-digest-latex/templates/arxiv_scroll_macros.tex}"
MACROS_DST="${ARXIV_DIGESTS_DIR}/arxiv_scroll_macros.tex"

if [[ ! -f "${TEX}" ]]; then
  echo "Error: ${TEX} not found" >&2
  exit 1
fi

cp "${MACROS_SRC}" "${MACROS_DST}"
echo "Macros: ${MACROS_DST}"

cd "${ARXIV_DIGESTS_DIR}"
if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode "${DATE}.tex"
else
  pdflatex -interaction=nonstopmode "${DATE}.tex"
  pdflatex -interaction=nonstopmode "${DATE}.tex"
fi

echo "PDF: ${ARXIV_DIGESTS_DIR}/${DATE}.pdf"
