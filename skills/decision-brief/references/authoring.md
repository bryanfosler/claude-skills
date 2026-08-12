# Authoring quality bar

A decision brief is a formal recommendation memo a director could forward without
hesitation. It is not a recap, not a plan, not a slide deck, and not a chat
summary. Three things make it good: it **answers first**, it **fits the page it
promises**, and it **looks the part**.

## Answer-first discipline

- **Lead with the recommendation.** The first block states what to do now and why,
  in 1–2 sentences. Everything after it is support. If a reader reads only the
  recommendation box, they should still know the answer and roughly why.
- **The brief must conclude.** The whole genre is "we recommend X." If the source
  material doesn't support a single defensible recommendation or ranking, **do not
  invent one** — pause and ask the user. Name the specific gap ("the docs don't
  settle the airtime cost; what's your read?"). A confidently-wrong brief in front
  of leadership is worse than no brief, and erodes trust in every future one.
- **Rank, don't list.** If you include options, rank them and mark exactly one
  recommended. An unranked menu pushes the decision back onto the reader — the
  opposite of the job. Omit the Options block entirely when there's genuinely no
  alternative worth weighing; a brief that just reaches one conclusion is fine.
- **Standalone.** A reader with no chat history must understand it. No "as
  discussed", "per our last session", or revision language. Real names, real dates,
  real numbers — never invented. If a number isn't in the source, don't assert it.

## The Executive one-page promise (hard density caps)

The Executive altitude is a *true* one Letter page. The print CSS tightens
aggressively, but CSS can't save an over-stuffed brief. Budget the `brief` fields:

- **Recommendation:** ≤ ~3 sentences.
- **Problem:** ≤ 2 sentences.
- **Background:** ≤ 5 tight bullets (or ~4 sentences).
- **Options:** 2–4 options, each `name` + a one-phrase `tradeoff`. No per-option
  prose in the Executive view — that's what `detail` (Detailed-only) is for.
- **Rationale:** ≤ 3 sentences.
- **Open questions / next step:** ≤ 4 bullets.
- **Stat strip (`meta.stats`):** flexible count — the strip renders exactly as many
  cells as you provide. 2–4 reads best on the one-page exec; 5+ cramps the row and risks
  pushing past one page.

If it still overflows to a second page, the content is too long for a 1-pager —
**cut, don't shrink**. Move the depth into `detail` fields (which only appear in
Detailed) rather than fighting the page. The fullest realistic brief (all six
sections + three options) fits one page at these caps; if yours doesn't, something
is over-written.

Put the depth in `detail`: evidence, second-order reasoning, per-option pros/cons,
cost models, risks. Detailed paginates naturally (~3 pages) — it has room.

## The stat strip — concrete dates and facts only

The cells under the recommendation are the figures a reader anchors on while deciding.
Every tile must be a **concrete, verifiable datum**: a key **date** (a deadline, a launch
window, a when-it-happened), or a **hard fact** that frames the call (a real metric, a
named path, a known quantity). They earn their prominence by being concrete — so the bar
is high, and it's better to show fewer strong tiles than to pad the row.

- **No soft tiles.** Don't fill a cell with a qualitative placeholder (`"Unproven"`,
  `"TBD"`) or a count that just restates the document (`"3 — options on the table"`). They
  read as filler and dilute the strip. If a number isn't known, it does **not** go in the
  hero strip — it goes in **Open Questions** as a thing still to prove. (This is consistent
  with the never-fabricate rule: the strip elevates what you *know*, not what you don't.)
- **Never invent a number.** A confident fake number in a large stat cell is the fastest
  way to lose the room. If you can't source it, leave it out.
- **Value short, label explanatory.** `value` is the glanceable figure ("~Jul 7"); `label`
  is the small-caps gloss ("Prioritization · A3 with Jess"). Don't put a sentence in `value`.
- **Flexible count.** The strip renders however many tiles you give it. Prefer 2–4 genuinely
  strong date-facts over a padded row of four.
- Omit the strip entirely (drop `meta.stats`) if there are no hard facts worth elevating —
  a strip of soft, hand-wavy cells is worse than none.

## The formal-look ban list (and why)

The runtime ships a quiet typeset-memo aesthetic. Hold the same line in content,
because the *point* is that this reads as a serious document, not an AI artifact —
the moment it looks generated, leadership discounts it.

- **No emoji.** They read as casual and instantly "AI-generated". A memo uses words.
- **No decorative color or color-coding.** Exactly one accent exists, and it marks
  only the recommended answer/option. Don't tint backgrounds, don't color bullets,
  don't traffic-light statuses. Color here means "this is the pick" — nothing else.
- **No gradients, no shadows-for-flair, no big rounded cards.** A document has
  hairlines and whitespace, not UI chrome.
- **No fake branding or logos.** Don't fabricate a company or product mark or a
  letterhead. The clean header (title / question / owner / date) is the identity.
- **No filler structure.** No "Executive Summary:" heading inside the recommendation
  (the whole doc is the summary), no restating the brief in the detail, no
  "In conclusion". Every section earns its place; if a section has nothing real to
  say, drop it.
- **Plain, declarative prose.** Short sentences. Concrete nouns. No hype adjectives
  ("game-changing", "robust", "seamless"), no hedging throat-clearing. State the
  claim and the cost.

## Before handing off

- Verify it renders (the builder prints block count + size; screenshot **both**
  altitudes and confirm the Executive prints to one page — this is the ground-truth
  check, not a guess).
- Re-read the recommendation alone: does it stand as the answer? Re-read the
  Executive view alone: could a director act on just that page?
- Leave room to push back — the brief is built to be edited and commented on inline.
