---
name: recall
description: Use when the user asks "what did we decide about X", "have we worked on Y before", "recall <topic>", "search my notes/vault for X", or invokes /recall — searches an Obsidian vault (session logs + synthesis notes) for relevant prior context and answers with citations. The on-demand read half of the Obsidian agent-brain loop; pairs with /log-session (write) and the on-load context hook.
---

# Recall from Obsidian

Pull prior context out of an Obsidian vault on demand — answer a question using
what past sessions and notes already captured, instead of re-deriving it. This
is the **on-demand read** half of the agent-brain loop.

---

## Configure

```
OBSIDIAN_VAULT_DIR: ~/path/to/vault
```

If unset, STOP and ask the user to set it.

---

## Procedure

### Step 1 — Search, synthesis-first

Search in priority order (matches the AGENTS.md schema's Query operation —
synthesis before raw):

1. **Synthesis & decisions** — `Decisions/`, `Knowledge Systems/`, `Concepts/`, `Projects/`
2. **Session logs** — `sessions/` (time-bounded history; the `summary:` line is the cheapest signal)
3. **Raw sources** — `Clippings/`, transcripts — only if synthesis is missing

Use the helper, or `rg` directly:

```bash
bash recall.sh "<query terms>"
```

`recall.sh` runs ripgrep across the vault, ranks session logs by `summary:`
match, and prints matching files with a few lines of context.

### Step 2 — Read the top matches

Open the 2–4 most relevant files. Prefer a synthesis/decision note over a raw
session log when both match — it's already distilled.

### Step 3 — Answer with citations

- Answer the question directly from what you found.
- **Cite the vault files** you used (path or `[[wikilink]]`).
- If the vault has a partial answer, say what's covered and what's missing:
  "There's a decision note on X but nothing on Y."
- If nothing relevant exists, say so plainly — don't invent. Offer to capture
  the current answer with `/log-session` so next time it's recallable.

---

## Why synthesis-first matters

A neglected wiki *lies confidently* — a stale synthesis note still reads as true.
Searching synthesis first gets you the distilled answer fast, but always check
the `date:` on what you cite, and fall back to recent session logs when the
synthesis looks stale. (See the workflow guide's note on write-time vs
query-time failure modes.)

See `obsidian-agent-brain/workflow-guide.md` in this repo for how `/recall`,
`/log-session`, and the on-load hook fit together.
