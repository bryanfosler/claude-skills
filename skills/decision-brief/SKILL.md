---
name: decision-brief
description: >-
  Turn a body of work, a document, or a set of documents into a formal,
  answer-first executive decision brief — a recommendation memo, not a recap or
  a plan. Produces ONE self-contained HTML file with a two-altitude toggle:
  an Executive 1-pager for leadership and a Detailed ~3-pager for the team that
  has to defend or build it. Use this whenever the user wants a "decision brief",
  "exec summary", "executive summary", "one-pager", "1-pager for leadership", a
  "brief for the team", a recommendation memo, or asks to summarize work/docs
  "into a recommendation" or "at the altitude each team needs" — even if they
  don't say "HTML". Light/cream, typeset-memo look; per-section clean copy for
  pasting into Teams/email; prints to a clean PDF from Chrome. No server, no
  sign-in, nothing leaves the machine.
metadata:
  visibility: exported
---

# Decision Brief

`/decision-brief` turns a body of work — the current conversation, a document, or
a set of documents — into a **formal executive recommendation memo**. It answers
first (the recommendation up top), then supports the answer. The output is one
self-contained `.html` file with an **altitude toggle**: **Executive** (a true
1-pager leadership can skim and act on) and **Detailed** (a ~3-pager the working
team can read to defend or build the decision). Same content, one source of
truth — Detailed just reveals the depth the Executive view hides.

This is a different genre from its siblings: `/visual-recap` is retrospective
("what we did"), `/visual-plan` is forward execution detail. A decision brief
**comes to a conclusion** — it recommends, and ideally ranks options.

## How it works

```
work / doc(s) ──▶ you author brief.json ──▶ build_brief.py ──▶ self-contained .html ──▶ (optional) embed in Obsidian / print to PDF
```

You build a **brief JSON** (the block data model) and run a tiny Python builder
that injects it into the runtime (HTML/CSS/JS in `assets/`). The runtime renders
the memo, owns the altitude toggle, clean-copy, editing, comments, and
persistence. See `references/block-catalog.md` for the JSON contract and
`references/authoring.md` for the quality bar — **read authoring.md before you
write the brief**; the one-page discipline and the formal-look rules live there.

## The answer-first spine

Author the blocks in this order (this is the memo's whole point):

1. **recommendation** — the answer, up top. 1–2 sentences: what to do now and why.
   The fragment someone could paste straight into a Teams message.
2. **problem** — the decision/question being made, in 1–2 lines.
3. **background** — only the context a reader needs. Tight.
4. **options** — *optional*. 2–4 candidate solutions, **ranked**, each with a
   one-phrase tradeoff, the recommended one marked. **Omit this block entirely**
   when the work reaches a single conclusion with no real choice among alternatives.
5. **rationale** — why this one, now: the reasoning + what it costs / what we give up.
6. **open-questions** — what's unresolved, or the ask / next step.

Each prose section carries a **`brief`** field (shown in Executive) and an
optional **`detail`** field (revealed only in Detailed). Write both: the brief is
the skimmable claim; the detail is the evidence and nuance. One source of truth,
two altitudes.

## The format (how it renders)

The brief renders as a scannable **decision document**, not flowing prose:

- The **recommendation** is a **solid accent-filled hero box** at the top (white text,
  labelled `01 · RECOMMENDATION`) — the unmissable answer. Set **`meta.due`** (e.g.
  `"~Jul 7"`) to show a `Decision needed by …` tag on it.
- A **stat strip** of 3–4 hard facts sits directly under it — set **`meta.stats`**:
  `[{ "value": "May 2029", "label": "K4 design window" }, …]`. Dates, counts, the one
  metric that frames the call. **Never invent a number** — unknown → `"Unproven"`/`"TBD"`.
  Omit `meta.stats` and the strip disappears.
- Every other block renders as a **numbered, bordered zone** (`02 THE QUESTION`,
  `03 BACKGROUND`, …); **options** render as a **ranked table** with the recommended row
  tinted + badged. See `references/block-catalog.md`.
- On screen, a dashed **page-break boundary** marks where each Letter page ends (a visual
  aid; the print/PDF is authoritative).

## Never fabricate a conclusion

A decision brief is only useful if its recommendation is real. **If the source
material doesn't clearly support a single recommendation or a defensible ranking,
stop and ask the user** — surface the gap ("the docs don't settle X; what's your
read?") rather than inventing a confident answer. A confidently-wrong brief in
front of leadership is worse than no brief. This matters more than producing the
artifact on the first pass.

## Procedure

1. **Get the material.** No arguments → summarize the **current conversation**.
   Given a path or paths → read those doc(s)/folder first, then synthesize. (A
   vault project folder or a stack of session logs is just the multi-doc path.)
   Building is read-only — make no source edits.

2. **Find the answer.** Decompose the work into: the recommendation, the question,
   the background that matters, the real options (if any), the rationale, the open
   questions. If you can't land a defensible recommendation, **ask** (see above).

3. **Write the JSON** to a temp file, e.g. `/tmp/<slug>.json`, following
   `references/block-catalog.md`. Give every block a stable, meaningful `id`
   (comments anchor to ids). Respect the Executive density caps in
   `references/authoring.md` — the 1-pager promise is real.

4. **Build** (single line):
   `python3 ~/.claude/skills/decision-brief/bin/build_brief.py --data /tmp/<slug>.json --out /tmp/decision-brief-<slug>-<YYYY-MM-DD>.html`
   The builder validates JSON, checks ids, and warns if the brief doesn't lead
   with a recommendation.

5. **Verify it renders** (Bryan's visual protocol — ground truth, not a guess).
   Screenshot **both** altitudes headless and confirm the Executive fits one page:
   - `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars --window-size=1100,1700 --screenshot=/tmp/<slug>-exec.png "file:///tmp/<file>.html?view=exec"`
   - same with `?view=detailed` (use a taller window, e.g. `1100,2400`).
   Read the PNGs. For the one-page check, print the exec view to PDF and confirm
   it's a single page:
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=/tmp/<slug>-exec.pdf "file:///tmp/<file>.html?view=exec"`

6. **Deliver.** Give the user the file path and `open` it. Tell them: it opens in
   the **Executive** altitude; the toggle (top-left) reveals **Detailed**; the
   **Copy 1-pager** / **Copy full** buttons (and per-section **copy**) put clean
   text on the clipboard for Teams/email; and **⌘P → Save as PDF** prints whichever
   altitude is showing (Executive → one page) for sending to leadership.

## Altitude, copy, print, persistence (runtime features — tell the user)

- **Altitude toggle** (top-left): **Executive** ↔ **Detailed**. The file opens in
  Executive. The choice persists per-browser. A `?view=exec` / `?view=detailed`
  URL param forces an altitude (used for headless print/screenshot).
- **Clean copy:** **Copy 1-pager** copies the Executive brief as plain Markdown;
  **Copy full** copies the Detailed brief; each section has its own **copy** on
  hover. This is the paste-into-Teams / paste-into-email path — no HTML junk.
- **Print to PDF:** ⌘P → Destination *Save as PDF*. The print stylesheet hides the
  UI, sets Letter margins, and prints the **current** altitude. Executive is
  budgeted to one page; Detailed paginates (~3 pages).
- **Edit text:** hover a section → `edit` → the editor edits the field for the
  altitude you're in (Executive edits the brief, Detailed edits the detail).
  "Reset to original" reverts.
- **Comment:** hover any section → `comment` to open a thread anchored to it.
- **Autosave:** every change saves to the browser (`localStorage`). **Save** writes
  a fresh self-contained HTML with edits/comments baked in (in place in Chrome,
  download elsewhere). **Revert** discards unsaved local changes.

## Formal aesthetic — the hard rule

This is a leadership document, not a playful AI artifact. The runtime enforces a
formal document look (clean sans type, numbered bordered zones, a solid-accent
recommendation hero, generous whitespace, near-black on warm white, **one**
restrained accent used only to mark the recommended answer/option). When you write
content, hold the same line — see the **ban list** in `references/authoring.md`:
no emoji, no gradients, no decorative color, no faux color-coding, no fake
branding, no "AI-weird" formatting. Professional and quiet. A director should be
able to forward it without a second thought.

## Embedding in Obsidian

Editing is best in a real browser; Obsidian is the read/scan surface. To embed,
compose with `/embed-artifact` — it copies the `.html` into the vault project
folder and scaffolds a `.md` wrapper with an absolute `file://` iframe. Offer this;
don't auto-write to the vault (briefs are often drafts). **Save** overwrites the
vault copy; the wrapper iframe shows it.

## Files

- `bin/build_brief.py` — the builder (stdlib only).
- `assets/template.html`, `assets/styles.css`, `assets/runtime.js` — the runtime.
- `references/block-catalog.md` — the JSON contract for every block.
- `references/authoring.md` — the quality bar: answer-first discipline, one-page
  density caps, the formal-look ban list, when to omit Options, never-fabricate.
