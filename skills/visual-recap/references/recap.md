# Recap-specific guidance

A recap is a visual plan built **from** a diff instead of toward one. Same JSON
contract, same builder, same runtime — see
`~/.claude/skills/visual-plan/references/block-catalog.md`. Set `meta.kind` to
`"recap"` (the toolbar then reads "Visual Recap").

## Ingesting the change

Work from the **real diff**, never inferred:
- `git diff <base>...<head>`, `git show <commit>`, or a PR's file list.
- Recap the whole work unit — original implementation **plus** follow-up fixes and
  tests on the same branch/thread — not just the latest commit. Exclude unrelated
  pre-existing edits.

## Canonical shape

1. **(UI changes only) wireframe(s)** showing the resulting or before/after state.
   If the diff changed rendered UI, you MUST show it — a diff alone doesn't convey it.
2. **Outcome narrative** — one `rich-text` block, 1–3 sentences: what changed and why.
   No "here's what changed" boilerplate; the structured blocks carry the rest.
3. **`data-model` / `api-endpoint`** for schema/contract changes — flag changed
   fields/entities/params with `change`; mark removed endpoints `deprecated: true`.
4. **`file-tree`** of every touched file with `change` flags — this carries the
   context, so you rarely need prose to list files.
5. **Key changes** — group the important hunks as `diff` blocks (`mode: "split"`)
   with `annotations` on the lines that matter, or under a `tabs` block (3–8 tabs)
   when there are several files worth showing.
6. Optional supporting diffs.

## Budgets & discipline

- Title < 70 chars; outcome narrative 1–3 sentences.
- Each diff excerpt < ~150 lines; annotate, don't dump.
- A reviewer should grasp the **shape** of the change before reading any literal
  line. If a block doesn't help them do that, cut it.
- The same edit/comment/resolve runtime applies — a reviewer can comment on any
  block and check items off as they review.
