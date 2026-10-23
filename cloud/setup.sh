#!/usr/bin/env bash
# One-time setup for a question-bank cloud session. Safe to run more than once.
set -u
cd "$(dirname "$0")/.."
python3 -c "import pymupdf, scipy, numpy, PIL" 2>/dev/null || \
  pip install --break-system-packages -q pymupdf scipy numpy pillow
if ! command -v pdflatex >/dev/null; then
  (apt-get update -qq && apt-get install -y -qq texlive-latex-base texlive-latex-recommended texlive-latex-extra \
     texlive-fonts-recommended texlive-science lmodern) >/dev/null 2>&1 || echo "WARN: pdflatex missing"
fi
command -v pdftoppm >/dev/null || (apt-get install -y -qq poppler-utils >/dev/null 2>&1 || true)
git config user.email >/dev/null || git config user.email "qbank-cloud@users.noreply.github.com"
git config user.name  >/dev/null || git config user.name  "Question bank cloud session"
mkdir -p /tmp/qb
echo "--- check"
python3 -c "import pymupdf, scipy; print('python packages ok')"
for t in pdflatex pdftoppm git; do command -v $t >/dev/null && echo "$t ok" || echo "$t MISSING"; done
python3 tools/bank_tools.py difficulty >/dev/null && echo "bank_tools ok (difficulty rubric present)"
python3 -c "import json,collections; print(dict(collections.Counter(t[\"status\"] for t in json.load(open(\"bank-manifest.json\"))[\"tests\"])))"
