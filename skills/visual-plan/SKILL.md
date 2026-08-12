---
name: visual-plan
description: >-
  Turn ordinary text plans into rich interactive visual plans with diagrams,
  file maps, annotated code, open questions, and UI wireframes. Produces a
  single self-contained HTML file you can edit, comment on, and embed in
  Obsidian — no server, no sign-in, nothing leaves your machine.
metadata:
  visibility: exported
---

# Visual Plan

`/visual-plan` turns a text plan into a scannable, **editable** HTML document:
prose mixed with the right structured blocks — diagrams, file maps, schema and
API changes, annotated code, a wireframe when it's a UI plan, and an open-questions
form at the end. The output is one self-contained `.html` file. The reader can
inline-edit any text block, check off steps, answer the open questions, and leave
comments — and it all persists locally. There is no backend: no MCP connector, no
hosted service, no account. (This replaced an earlier version that depended on the
hosted Agent-Native Plans service — see `_archive-agent-native/`.)

## How it works

The skill builds a **plan JSON** (the block data model) and runs a tiny Python
builder that injects it into a shared runtime (HTML/CSS/JS in `assets/`). The
runtime renders the blocks and owns all the editing/commenting/persistence.

```
text plan ──▶ you author plan.json ──▶ build_plan.py ──▶ self-contained .html ──▶ (optional) embed in Obsidian
```

## Procedure

1. **Start from the user's plan.** Use whatever plan already exists in the
   conversation (or write one first if asked). Planning is read-only — make no
   source edits while building.

2. **Decompose into blocks.** Map the plan onto the block types in
   `references/block-catalog.md`. Lead with a `rich-text` objective; reach for the
   *specific* block for each idea (schema → `data-model`, route → `api-endpoint`,
   changed files → `file-tree`, file walkthrough → `annotated-code`, relationships
   → `diagram`/`mermaid`, UI → `wireframe`). Put a single `open-questions` block at
   the very end, and only if decisions are genuinely open. Follow
   `references/authoring.md` for the quality bar.

3. **Write the JSON** to a temp file, e.g. `/tmp/<slug>.json`. Give every block a
   stable, meaningful `id` (comments anchor to ids, so they survive rebuilds).

4. **Build** (single line):
   `python3 ~/.claude/skills/visual-plan/bin/build_plan.py --data /tmp/<slug>.json --out /tmp/<slug>.html`
   The builder validates JSON, checks block ids, and prints block count + size.

5. **Verify it renders.** For anything UI-heavy or large, screenshot it headless
   before handing off (the visual protocol — ground truth, not a guess):
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars --window-size=1100,2200 --screenshot=/tmp/<slug>.png "file:///tmp/<slug>.html"`
   then Read the PNG. Mermaid diagrams render via CDN when online and degrade to
   readable source offline — don't treat a missing diagram offline as a failure.

6. **Deliver.** Tell the user the file path and `open` it for them. If they want it
   in the vault, compose with `/embed-artifact` (see below).

## Editing, comments, persistence (runtime features — tell the user)

- **Edit text:** hover a text block → `✎ edit` → edit the source → Done. An
  "edited" badge appears; "Reset to original" reverts.
- **Resolve:** check off checklist items; pick answers in the open-questions form.
- **Comment:** hover any block → 💬 to open a thread anchored to it; resolve/delete
  from the Comments panel.
- **Autosave:** every change saves to the browser (`localStorage`) instantly.
- **Save to file:** the **Save** button writes a fresh self-contained HTML with all
  edits/comments baked in. In Chrome it saves **in place** (File System Access API);
  elsewhere it downloads — drop that file back over the vault copy. **Revert**
  discards unsaved local changes.

## Embedding in Obsidian

Editing is best done with the HTML open in a real browser; Obsidian is the
read/scan surface (its embedded iframe sandboxes localStorage). To embed, compose
with `/embed-artifact`: it copies the `.html` into the vault project folder and
scaffolds a `.md` wrapper with an absolute `file://` iframe plus a native-Mermaid
fallback, refreshing the latest rev in place. The Save-to-file model and the embed
pipeline line up: Save overwrites the vault copy, the wrapper iframe shows it.

## Deferred (say so if the user asks for these)

- **Multi-person / shared editing & live comments** — the explicit stretch goal.
  The JSON state model is built to lift into a server unchanged when that day comes;
  nothing here forecloses it.
- **Structural editing in the browser** (add/reorder/delete blocks) — v1 edits text,
  resolves, and comments only. To restructure, regenerate the JSON and rebuild.
- **Positioned annotation canvas / artboard lanes** and **live prototype tabs** —
  the runtime ships static wireframes (framed surfaces with the `--wf-*` token kit),
  not the full canvas system the old hosted version had.

## Files

- `bin/build_plan.py` — the builder (stdlib only; shared with `/visual-recap`).
- `assets/template.html`, `assets/styles.css`, `assets/runtime.js` — the runtime.
- `references/block-catalog.md` — the JSON contract for every block.
- `references/authoring.md` — the quality bar.
- `_archive-agent-native/` — the prior hosted-service version, kept for reference.
