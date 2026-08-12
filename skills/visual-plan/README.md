# visual-plan

Turn a text plan into a single self-contained, **editable** HTML document —
diagrams, file maps, schema/API changes, annotated code, wireframes, and an
open-questions form. No backend: no MCP connector, no hosted service, no account.

## What it does

```
text plan ─▶ plan.json (block model) ─▶ build_plan.py ─▶ self-contained .html ─▶ (optional) embed in Obsidian
```

The reader can inline-edit text blocks, check off steps, answer open questions, and
leave comments anchored to blocks. Changes autosave to the browser; **Save** writes
a fresh self-contained HTML with everything baked in (saves in place in Chrome via
the File System Access API, otherwise downloads).

## Build a plan manually

```
python3 ~/.claude/skills/visual-plan/bin/build_plan.py --data /tmp/myplan.json --out /tmp/myplan.html
```

See `references/block-catalog.md` for the JSON contract and `references/authoring.md`
for the quality bar.

## Layout

| Path | Purpose |
|------|---------|
| `bin/build_plan.py` | Builder (stdlib only). Shared with `visual-recap`. |
| `assets/template.html` | HTML shell with `__STYLES__`/`__PLAN_DATA__`/`__RUNTIME__` slots. |
| `assets/styles.css` | Runtime styles (dark, tokenized, self-contained). |
| `assets/runtime.js` | Render + edit + comments + localStorage + save-to-file. |
| `references/` | Block catalog + authoring guide. |
| `_archive-agent-native/` | Prior version that used the hosted Agent-Native Plans MCP service. |

## Deferred (stretch)

Multi-person shared editing/comments (state model lifts into a server unchanged),
in-browser structural editing (add/reorder/delete blocks), and the positioned
annotation canvas / live prototype tabs.
