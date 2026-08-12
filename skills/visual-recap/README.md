# visual-recap

Turn a PR, branch, commit, or git diff into a self-contained, commentable HTML
recap — file map, schema/API deltas, annotated diffs, and review notes. The
reverse of `visual-plan`: it summarizes a change that was just made so a reviewer
can scan the *shape* of it before reading literal lines. No backend.

## Build a recap manually

It reuses the `visual-plan` builder and runtime — just set `kind` to `recap`:

```
python3 ~/.claude/skills/visual-plan/bin/build_plan.py --data /tmp/recap.json --out /tmp/recap.html --kind recap
```

See `references/recap.md` for the canonical recap shape and budgets, and
`~/.claude/skills/visual-plan/references/block-catalog.md` for the JSON contract.

## Layout

| Path | Purpose |
|------|---------|
| `references/recap.md` | Recap-specific shape + budgets. |
| `_archive-agent-native/` | Prior hosted-service version. |

Builder, runtime, and the block catalog live in `~/.claude/skills/visual-plan/`.

## Deferred (stretch)

Same as visual-plan: multi-person shared review/comments, in-browser structural
editing, positioned annotation canvas / live prototype tabs.
