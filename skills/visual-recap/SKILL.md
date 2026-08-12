---
name: visual-recap
description: >-
  Turn a PR, branch, commit, or git diff into an interactive visual recap with
  diagrams, file maps, API/schema summaries, annotated diffs, and review notes.
  Produces a single self-contained HTML file you can comment on and embed in
  Obsidian — no server, no sign-in, nothing leaves your machine.
metadata:
  visibility: exported
---

# Visual Recap

`/visual-recap` creates a visual document built **from** a diff, not toward one —
the reverse of `/visual-plan`. Instead of describing a change you're about to make,
it summarizes the change that was just made, at a higher altitude than line-by-line
review: a reviewer scans the *shape* of the change (file map, schema/API deltas,
key annotated hunks) before spending attention on literal lines.

It shares everything with `/visual-plan` — the same block JSON contract, the same
builder, the same self-contained editable/commentable runtime, and no backend.
(This replaced a hosted-service version — see `_archive-agent-native/`.)

## Procedure

1. **Get the real diff.** `git diff <base>...<head>`, `git show <commit>`, or a PR's
   files. Recap the whole work unit (implementation + fixes + tests on the thread),
   excluding unrelated pre-existing edits. Read-only — make no edits.

2. **Decompose into blocks**, following `references/recap.md` (canonical shape and
   budgets) and the block contract in
   `~/.claude/skills/visual-plan/references/block-catalog.md`. Set
   `meta.kind: "recap"`. Lead with UI wireframes if rendered UI changed, then a 1–3
   sentence outcome narrative, then `file-tree`, schema/API deltas, and the key
   `diff` hunks (split mode, annotated; or grouped in `tabs`).

3. **Write the JSON** to `/tmp/<slug>.json` with stable block ids.

4. **Build** (single line) — it reuses the visual-plan builder:
   `python3 ~/.claude/skills/visual-plan/bin/build_plan.py --data /tmp/<slug>.json --out /tmp/<slug>.html --kind recap`

5. **Verify it renders** (headless screenshot for anything substantial):
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars --window-size=1100,2200 --screenshot=/tmp/<slug>.png "file:///tmp/<slug>.html"`
   then Read the PNG.

6. **Deliver.** Give the file path and `open` it. To put it in the vault, compose
   with `/embed-artifact`.

## Editing, comments, embedding

Identical to `/visual-plan`: every block is commentable, text blocks are
inline-editable, changes autosave to the browser, **Save** writes a fresh
self-contained HTML (in place via File System Access in Chrome, else a download).
Edit/comment in a real browser; use Obsidian (via `/embed-artifact`) as the
read/scan surface. See the visual-plan SKILL.md for the full runtime description.

## Deferred

Same as visual-plan: multi-person shared review/comments (the stretch goal; the
state model lifts into a server unchanged), in-browser structural editing, and the
positioned annotation canvas / live prototype tabs.

## Files

- `references/recap.md` — recap-specific shape and budgets.
- Builder + runtime + block catalog live in `~/.claude/skills/visual-plan/`
  (`bin/`, `assets/`, `references/block-catalog.md`) — this skill reuses them.
- `_archive-agent-native/` — the prior hosted-service version.
