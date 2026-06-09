---
name: sync-project-board
description: Use when the user says "sync the project board", "refresh the board", or invokes /sync-project-board — scans a configured set of repos for open GitHub issues not yet on a GitHub Projects (v2) board and adds them. Idempotent.
---

# Sync Project Board

Keeps a single GitHub Projects (v2) board up to date with open issues across
multiple repos.

GitHub Projects v2's built-in "Auto-add to project" workflow only watches **one**
repository per project. If you track several repos on one board, there's no native
way to auto-add issues from all of them. This skill fills that gap — run it on
demand or wire it into a wrap-up routine.

This skill is GitHub-only. It does NOT:
- Modify issues, only add references to the project board
- Touch local files or git

---

## Configure

Edit the variables at the top of `sync.sh`:

```bash
OWNER="your-github-username"          # the board owner (user or org)
PROJECT_NUM=1                          # the project number (from the board URL)
REPOS=(repo-one repo-two repo-three)   # repos to scan for open issues
```

Find `PROJECT_NUM` in the board URL: `https://github.com/users/OWNER/projects/PROJECT_NUM`.

---

## Procedure

Run the sync script:

```bash
bash sync.sh
```

It performs (idempotent):
1. Lists current items in the project board (URLs)
2. For each configured repo, lists open issues (URLs)
3. Diffs the two sets to find new issues
4. Adds each new issue to the board
5. Reports added count, skipped (already present), and any failures

Expected output:
```
sync: 28 already on board, 2 new added, 0 failed
```

---

## Edge cases

- **`gh` not authenticated**: script fails fast with non-zero exit → run `gh auth login`.
- **A repo in the list was deleted / renamed**: `gh issue list` errors for that repo; the script logs the failure and continues with the others.
- **Board grows past 500 items**: bump the `--limit` in the script.
- **No new issues to add**: clean exit, reports `0 new added`.
- **Offline**: all `gh` calls fail; script exits with an error message. No partial state.

---

## Why this exists

GitHub Projects v2's "Auto-add to project" workflow only watches one repository
per project. With several active repos, the alternatives are (a) deploy a GitHub
Action to every repo with a PAT secret, or (b) sync periodically. This skill is
option (b) — for personal or small-team projects, a short lag on new issues
appearing on the board is invisible, and there's nothing to maintain per-repo.
