---
name: log-session
description: Use when the user says "log this session", "log to obsidian", "save this session", "write a session log", or invokes /log-session — writes a clean, retrieval-optimized session log to an Obsidian vault (markdown). Text-only — no git, issues, or time tracking. The write half of the Obsidian agent-brain loop; pairs with /recall (on-demand read) and the on-load context hook.
---

# Log Session to Obsidian

Capture the current session as a clean, structured markdown log in an Obsidian
vault. This is the **write** half of an agent-brain loop: logs written here are
shaped so a future session can pull them back as context — on load (via the
SessionStart hook) or on demand (via `/recall`).

This skill is **text-only**. It does NOT commit/push, touch GitHub issues, log
time/tokens, or update project files. For a full session close-out, use a
wrap-up skill instead.

---

## Configure

```
OBSIDIAN_SESSIONS_DIR: ~/path/to/vault/sessions
```

If unset, STOP and tell the user to set it. If the directory doesn't exist
(e.g. the vault isn't synced yet), STOP — do not silently write elsewhere.
Quote all paths in shell commands; vault paths usually contain spaces.

---

## Procedure

### Step 1 — Sanity check

Look at the conversation. If nothing meaningful happened (no file edits, no
non-trivial commands, no decisions, no investigation), ask before writing:
"Session looks light — log anyway?" When unsure, lean toward writing; a thin
log beats no log.

### Step 2 — Identify THIS session's file

**One file per SESSION, not per day.** If you run several agent sessions in
parallel, each owns its own file. **Never select a file by "most recent" or
mtime** — appending to a different session's file corrupts it.

```bash
today=$(date '+%Y-%m-%d')
now_hhmm=$(date '+%H%M')
now_colon=$(date '+%H:%M')
dir="$OBSIDIAN_SESSIONS_DIR"
```

Decide first-run vs. re-run **for this session**:

1. **Did this conversation already write a log today?** You know its path from
   your own context → that's your file → **Step 4 (append)**.
2. **First `/log-session` of this session?** → **Step 3 (create new)**.
3. **Lost the path (context compacted)?** Find your file by the `session_key`
   you recorded: `grep -l "^session_key: <your-key>" "$dir"/${today}-*.md`.
   No match or no recorded key → treat as first run → Step 3.

When in doubt, create a NEW file. Never append to a file you can't confirm is
this session's.

### Step 3 — First run: write a new session log

1. Generate a 3–7 word kebab-case slug naming the actual work
   (e.g. `oauth-token-rotation-fix`, not `session-work-done`).
2. Filename: `$dir/${today}-${now_hhmm}-<slug>.md`
3. Generate this session's stable key (record it — you'll reuse it on re-run):
   `session_key=$(uuidgen | tr 'A-Z' 'a-z' | cut -c1-8)`
4. Write this frontmatter — **the `summary` field is what the on-load hook and
   `/recall` read first, so make it a sharp one-liner; `session_key` is the
   per-session anchor a re-run uses to find this file under parallelism:**

   ```yaml
   ---
   date: YYYY-MM-DD
   type: session-log
   project: <repo-or-project-slug, or "general">
   session_key: <8-char key from step 3>
   summary: <one sentence — what this session accomplished>
   tags: [session-log, <2-4 topical tags>]
   ---
   ```

5. Write the body using this structure. **Repeat the summary as the first line**
   so it's grabbable without parsing frontmatter. Omit any section that's empty.

   ```markdown
   # <Session title>

   > <one-line summary — same as frontmatter `summary`>

   ## What We Did
   <narrative naming actual files, commands, decisions>

   ## Decisions Made
   - <decision> — <why> (omit section if none)

   ## Current State
   <one or two lines: what works now, what doesn't>

   ## Open Questions
   - <unresolved> (omit section if none)

   ## Next Steps
   - <single concrete next action>
   ```

### Step 4 — Re-run in the same session: append an update

Open **this session's file** (the path you recorded, or the `session_key` match
from Step 2 — confirm the key matches first). Do NOT modify frontmatter or
earlier sections, and never touch another session's file. Append:

```markdown

## Update HH:MM

**Since last log:** <2-3 sentences naming actual files, commands, decisions>
**Current state:** <one line>
**Next:** <single concrete next action>
```

Use `$now_colon` for `HH:MM`.

### Step 5 — Confirm

Print one line: the file path, and whether this was a fresh write or an append.

```
Logged to <dir>/2026-06-09-1432-oauth-token-rotation-fix.md (new)
```

### Step 6 — Artifacts (optional, delegated)

This skill stays **text-only**. But if the session produced an HTML or visual
artifact (dashboard, report, diagram) and a vault projects dir is configured,
delegate the embed to the **embed-artifact** skill so the deliverable is
viewable in the vault — don't inline HTML here. Default to the LATEST version;
embed all versions only if the user said "log all artifacts." Then add to this
log: `artifact updated: [[<Slug>]] (rev N)`.

---

## Edge cases

- **Slug collision** (same HHmm exists): append seconds — `${today}-${now_hhmm}$(date '+%S')-<slug>.md`.
- **Sessions dir missing**: STOP, tell the user, don't write elsewhere.
- **Many slug files today (parallel sessions)**: normal — each session owns its file. Append ONLY to the one whose `session_key` matches this session's. Never pick by mtime; never merge across sessions; when unsure, write a new file.

---

## How this fits the loop

- **Write:** this skill → `vault/sessions/`
- **Read on load:** the SessionStart hook reads recent `summary:` lines and injects them
- **Read on demand:** `/recall` greps the vault and cites matches

See `obsidian-agent-brain/workflow-guide.md` in this repo for the full picture.
