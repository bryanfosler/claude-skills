# Block catalog — the brief JSON contract

The builder (`bin/build_brief.py`) takes a JSON file and injects it into the
self-contained runtime. This is the full shape.

## Contents
- [Top level](#top-level)
- [The brief/detail convention](#the-briefdetail-convention)
- [Section blocks](#section-blocks)
- [The options block](#the-options-block)
- [What's editable](#whats-editable)

## Top level

```json
{
  "meta": {
    "title": "string (required) — the brief's headline",
    "question": "string — the decision being made; shown as the header subtitle",
    "owner": "string — who owns this (e.g. a person or team name)",
    "date": "YYYY-MM-DD",
    "status": "string? — e.g. 'For decision — A3 ~Jul 7'",
    "due": "string? — e.g. '~Jul 7'; shown as a 'Decision needed by …' tag on the recommendation hero",
    "stats": [ { "value": "May 2029", "label": "K4 design window" } ]
  },
  "blocks": [ { "id": "unique", "type": "...", ... } ]
}
```

## How the brief renders (the format)

The layout is a formal decision document, not an essay:

- **Header** — eyebrow ("Decision Brief"), title, the question (italic subtitle), and a
  meta line (owner · date · status).
- **Recommendation hero** — the `recommendation` block renders as a **solid accent-filled
  box** (white text) at the top, labelled `01 · RECOMMENDATION`, with a
  `Decision needed by <meta.due>` tag at its right when `meta.due` is set. This is the one
  place the accent leads — the unmissable answer.
- **Stat strip** — `meta.stats` renders as a row of cells (big value + small label)
  directly under the recommendation. The count is **flexible** — the strip draws exactly
  as many cells as the array has (2–4 reads best on the one-page exec). Omitted entirely
  when `meta.stats` is absent. Use it only for **concrete dates and hard facts** a reader
  anchors on; soft placeholders ("Unproven", "TBD") and doc-restating counts belong
  elsewhere (see `authoring.md`).
  **Never invent a number** — if it isn't known, the value cell says `"Unproven"` / `"TBD"`.
- **Numbered zones** — every other block renders as a bordered, numbered zone
  (`02 THE QUESTION`, `03 BACKGROUND`, …) with a hairline header band. Scannable, not prose.
- **Options as a table** — see below.
- **Page-break boundary** — on screen, a dashed rule marks where each printed Letter page
  ends (a visual rhythm aid). It's hidden in the actual print/PDF, which is authoritative.

Rules that matter:
- Every block needs a unique `id` (the builder backfills `b0,b1,…`, but stable ids
  make comments durable across rebuilds — set them).
- Author blocks in the answer-first spine order: `recommendation` → `problem` →
  `background` → `options` (optional) → `rationale` → `open-questions`. The builder
  **warns** if the first block isn't `recommendation`.
- Do **not** add a `state` object by hand — that's the user-edit layer the runtime owns.

## The brief/detail convention

Every prose section carries two fields:

- **`brief`** — markdown, shown in **both** altitudes. The skimmable claim. This is
  what lands on the Executive 1-pager, so keep it tight (see `authoring.md` caps).
- **`detail`** — markdown, optional, shown **only in the Detailed altitude**. The
  evidence, the nuance, the second-order reasoning. Rendered below the brief under a
  hairline rule.

One source of truth, two altitudes. Don't write a separate 1-pager and 3-pager —
write `brief` + `detail` once and the toggle does the rest.

Markdown supported in both fields: headings (`#`–`####` → rendered as subheads),
bold, italic, `code`, links, `-`/`1.` lists, `>` quotes, `---`, and pipe tables.

## Section blocks

All of these share the `brief` (+ optional `detail`) shape. The only difference is
the auto-label shown above them (override with `label`).

**recommendation** — the answer, up top. Rendered in the one accent-colored box
(the single place accent leads). 1–2 sentences in `brief`.
```json
{ "id":"rec", "type":"recommendation",
  "brief":"Commit now to **X** because…",
  "detail":"The ask is scoped to a business case, not a hardware commit, because…" }
```

**problem** — the decision/question. Auto-label "The Question".
```json
{ "id":"prob", "type":"problem", "brief":"Riders venture beyond coverage and…", "detail":"…" }
```

**background** — context the reader needs. Auto-label "Background". Bullets work well.

**rationale** — why this one, now + what it costs. Auto-label "Why This, Now".

**open-questions** — what's unresolved / the ask / next step. Auto-label
"Open Questions & Next Step". Rendered in a set-apart panel.

**evidence** — optional supporting data/quotes (best kept Detailed-only by putting
content in `detail`). Auto-label "Evidence".

**rich-text** — generic prose with no auto-label (set your own `label`). Escape hatch
for a section that doesn't fit the spine.

Override any auto-label with a `label` field, e.g. `"label":"Recommendation & Ask"`.

## The options block

Optional. Omit it entirely when there's no real choice among alternatives. When
present, list 2–4 options; the runtime renders them as a **ranked table**
(`#` | `Option` | `Tradeoff`), ordered by `rank`, with the recommended row tinted in
the accent wash + a "Recommended" badge. A table (not cards) is deliberate: 3+ options
read fastest when the eye can scan one column straight down. Per-option `detail` rides in
the Tradeoff cell and shows only in the Detailed altitude.

```json
{
  "id":"opts", "type":"options",
  "options": [
    { "name":"Iridium / nRF9151 NTN messaging", "rank":1, "recommended":true,
      "tradeoff":"Fits the antenna constraint and timeline; airtime cost unproven.",
      "detail":"Two-way text + location over Iridium NTN… (shown in Detailed only)." },
    { "name":"Partner handoff (paired phone / inReach)", "rank":2,
      "tradeoff":"Zero BOM cost; cedes the safety capability to a third device.",
      "detail":"…" }
  ]
}
```

Per-option fields:
- **`name`** — the option, one line. (required)
- **`rank`** — integer; lower = higher. The list renders in rank order, numbered.
- **`recommended`** — `true` on exactly one option → accent border + "Recommended" tag.
- **`tradeoff`** — one phrase, the headline cost/benefit. Shown in both altitudes.
- **`detail`** — the per-option analysis (pros/cons/cost). Shown only in Detailed.

Mark exactly one option `recommended` — that's the answer the recommendation block
already stated. Don't mark zero (the brief must conclude) or two (that's not a
decision).

## What's editable

The runtime lets the user inline-edit the **source** of any prose section
(`brief` in Executive, `detail` in Detailed), answer free-text in open-questions,
and attach comments to any section. Structural editing (add/reorder/delete blocks,
re-rank options) is deferred — regenerate the JSON and rebuild to restructure.
