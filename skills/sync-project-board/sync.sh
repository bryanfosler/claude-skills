#!/bin/bash
# sync-project-board — scan configured repos for open GitHub issues and add them
# to a GitHub Projects (v2) board. Idempotent. Safe to run anytime.
set -uo pipefail

# ── Configure ──────────────────────────────────────────────────────
OWNER="your-github-username"            # board owner (user or org)
PROJECT_NUM=1                           # project number from the board URL
REPOS=(repo-one repo-two repo-three)    # repos to scan for open issues
# ───────────────────────────────────────────────────────────────────

# Preflight: gh auth
if ! gh auth status >/dev/null 2>&1; then
  echo "sync: gh not authenticated. Run 'gh auth login'." >&2
  exit 1
fi

TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

# Step 1: existing items on the board
gh project item-list "$PROJECT_NUM" --owner "$OWNER" --limit 500 --format json \
  | jq -r '.items[].content.url // empty' \
  | sort -u > "$TMP/existing.txt"

# Step 2: candidates across repos
: > "$TMP/candidates.txt"
repo_errors=0
for repo in "${REPOS[@]}"; do
  if ! gh issue list --repo "$OWNER/$repo" --state open --limit 100 --json url \
        --jq '.[].url' 2>/dev/null >> "$TMP/candidates.txt"; then
    echo "sync: failed to list issues for $repo (continuing)" >&2
    repo_errors=$((repo_errors+1))
  fi
done
sort -u "$TMP/candidates.txt" -o "$TMP/candidates.txt"

# Step 3: new = candidates - existing
comm -23 "$TMP/candidates.txt" "$TMP/existing.txt" > "$TMP/new.txt"

new_count=$(wc -l < "$TMP/new.txt" | tr -d ' ')
existing_count=$(wc -l < "$TMP/existing.txt" | tr -d ' ')

# Step 4: add each new issue
added=0
failed=0
while IFS= read -r url; do
  [ -z "$url" ] && continue
  if gh project item-add "$PROJECT_NUM" --owner "$OWNER" --url "$url" >/dev/null 2>&1; then
    added=$((added+1))
  else
    failed=$((failed+1))
    echo "sync: failed to add $url" >&2
  fi
done < "$TMP/new.txt"

# Step 5: report
echo "sync: $existing_count already on board, $added new added, $failed failed${repo_errors:+, $repo_errors repo error(s)}"
