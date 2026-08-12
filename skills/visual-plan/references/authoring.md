# Authoring quality bar

Distilled from the original document-quality rules. A visual plan is a serious
technical document with editable structure — not a slide deck.

**Document discipline**
- Outcome-first and prose-first: open with one `rich-text` block stating what we're doing and why, in plain language, before any tables or code.
- Standalone: a reader with no chat history should understand it. No "as discussed", "unlike the previous plan", revision language.
- Specific: real file paths, real symbols, real data shapes — never invented. For each step, name what it **reuses** before what it adds.
- Surface hard-to-reverse decisions early: wire formats, public ids, data-model shape, auth/ownership boundaries. Scope the first cut small enough to prove the approach without foreclosing options.
- No duplication: if a diagram or wireframe carries the story, don't restate it in prose. Each block earns its place.

**Block selection**
- Reach for the *specific* block, not prose-about-the-thing: a schema change → `data-model`; a route → `api-endpoint`; a file walkthrough → `annotated-code`; changed files → `file-tree`; relationships → `diagram`.
- `open-questions` appears **once, at the bottom**, and only if decisions are genuinely unresolved. Mark the recommended option. If nothing's open, omit it.
- Keep code excerpts tight (<~40 lines); annotate the lines that matter rather than pasting whole files.

**Wireframes (UI plans only)**
- Author semantic HTML with real layout (flex/grid) and real content; let the renderer own theme/font. No hard-coded hex or `font-family`, no `box-shadow`.
- Match the real surface footprint; only show mobile + desktop together if responsive behavior actually differs.
- For before/after, preserve unchanged controls in both states and label states with column headers (`columns` block), not text baked into the frame.

**Before handing off**
- The plan is built to be edited and commented on. Don't over-pack it; leave room for the reader to push back inline.
- Verify it renders (the builder prints block count + size; a headless screenshot is the ground-truth check for anything UI-heavy).
