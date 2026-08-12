# Block catalog — the plan JSON contract

The builder (`bin/build_plan.py`) takes a JSON file and injects it into the
self-contained runtime. This is the full shape. Top level:

```json
{
  "meta": { "title": "string (required)", "kind": "plan|recap",
            "subtitle": "string?", "generated": "YYYY-MM-DD?", "source": "string?" },
  "blocks": [ { "id": "unique", "type": "...", "summary": "optional label", ... } ]
}
```

Rules that matter:
- Every block needs a unique `id` (the builder backfills `b0,b1,…` if missing, but stable ids make comments durable across rebuilds — set them).
- `summary` (or `title`) renders as a small label above the block and is what the comment sidebar uses to name an anchor. Worth setting on most blocks.
- Do **not** add a `state` object by hand — that's the user-edit layer the runtime owns.

## Block types

**rich-text** — prose. The workhorse. `markdown` field; supports headings (`#`–`####`), bold, italic, `code`, links, `-`/`1.` lists, `>` quotes, `---`, fenced code, and pipe tables. Editable.
```json
{ "id":"b1", "type":"rich-text", "summary":"Objective", "markdown":"We need **X** because…" }
```

**callout** — bounded note/decision box. `tone`: `info` | `warning` | `decision`. `markdown` body. Editable.

**table** — same as rich-text but semantically a table; put a markdown pipe table in `markdown`. Editable.

**code** — plain snippet. `filename?`, `language?`, `code`. Editable.

**annotated-code** — `code` plus `annotations: [{ "lines":"12" | "12-15", "label?":"…", "note":"…" }]`. Highlights those lines and prints margin notes. Editable.

**diff** — `filename`, `before`, `after`, `mode`: `split` (default) | `unified`, `summary?`. Renders red/green panes. (For recap, prefer `split`.)

**file-tree** — `files: [{ "path", "change":"added|modified|removed|renamed", "note?" }]`.

**data-model** — `entities: [{ "name", "description?", "change?", "fields":[{ "name","type?","change?","note?" }] }]`. `change` values render as colored tags.

**api-endpoint** — `method`, `path`, `change?`, `deprecated?`, `description?` (markdown), `request?:{example}`, `response?:[{status, example}]`. Examples are raw strings (show them as-is).

**checklist** — `items: [{ "id","label","checked?" }]`. Toggling persists to user state.

**open-questions** — `title?`, `questions:[{ "id","title","mode":"single|multi|freeform","options?":[{ "label","recommended?" }] }]`. Put this **once, at the bottom**, only if real decisions are open. Answers persist.

**diagram** / **mermaid** — `mermaid:"<mermaid source>"` (rendered via CDN, degrades to readable source offline). Or `data:{html, css}` for a hand-built diagram using the runtime tokens.

**columns** — `cols:[{ "label?", "blocks":[ …nested blocks… ] }]`. Side-by-side; auto-stacks on narrow screens. Use for before/after.

**tabs** — `tabs:[{ "label", "blocks":[ … ] }]`. Horizontal tabs; full width per tab.

**wireframe** — `surface`: `browser|mobile|panel|popover`, `html`: semantic HTML only (no `<style>`/`<script>`, no hard-coded colors). Use the helper classes the runtime ships: `.wf-card`/`.wf-box`, `.wf-pill`/`.wf-chip` (+`.accent`), `.wf-muted`, `button.primary`, `<span data-icon="…">`. The renderer owns the theme.

## What's editable in v1
The runtime lets the user inline-edit the **source** of: rich-text, callout, table, code, annotated-code. It lets them toggle checklist items, answer open-questions, and attach comments to **any** block. Structural editing (add/reorder/delete blocks) and a positioned annotation canvas are deliberately deferred — see SKILL.md "Deferred".
