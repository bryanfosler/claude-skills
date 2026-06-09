#!/bin/bash
# recall.sh — search an Obsidian vault for relevant prior context.
# Usage: bash recall.sh "query terms"
# Requires: ripgrep (rg). Reads OBSIDIAN_VAULT_DIR from the environment.
set -uo pipefail

QUERY="${*:-}"
VAULT="${OBSIDIAN_VAULT_DIR:-}"

if [ -z "$VAULT" ]; then
  echo "recall: set OBSIDIAN_VAULT_DIR to your vault path." >&2
  exit 1
fi
if [ -z "$QUERY" ]; then
  echo "recall: usage: bash recall.sh \"query terms\"" >&2
  exit 2
fi
if ! command -v rg >/dev/null 2>&1; then
  echo "recall: ripgrep (rg) not found. Install it, or grep the vault manually." >&2
  exit 3
fi

# Search synthesis/decision/project folders first, then everything else.
# -i case-insensitive, -l list files, then show context for the top hits.
echo "── Summary-line matches in session logs ──"
rg -i --no-heading -g '*.md' "^summary:.*${QUERY// /.*}" "$VAULT" 2>/dev/null | head -15 || true

echo
echo "── Content matches (synthesis & sessions, top files) ──"
rg -i -l -g '*.md' "$QUERY" "$VAULT" 2>/dev/null | head -20 || true

echo
echo "── Context snippets (first few hits) ──"
rg -i -n --max-count=2 -C1 -g '*.md' "$QUERY" "$VAULT" 2>/dev/null | head -40 || true

echo
echo "(Open the most relevant files above; prefer synthesis/decision notes over raw session logs.)"
