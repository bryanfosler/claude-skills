---
name: log-infra-change
description: Use when the user wants to record a tooling/infrastructure change to an infra changelog — "log this to the infra-log", "log this infra change", "record this tooling change", "add to the infra changelog", or invokes /log-infra-change. Appends a structured entry (skill installs/edits, Claude Code config/settings, hooks, launchd/cron jobs, plugin/marketplace changes, symlinks, MCP config). Composes with /wrap-up (auto-fires when a session made infra changes) and /log-session.
---

# Log Infra Change

Append a structured entry to an **infrastructure changelog** so tooling changes
are durably recorded — the gap that session logs and memory don't cover. Session
logs capture *work*; this captures *changes to the agent's own environment*:
skill installs/edits, Claude Code `settings.json`/hooks, launchd/cron jobs,
plugin/marketplace installs, symlinks into `~/.claude`, MCP server config,
permission-mode changes, new automation scripts.

It is **composable**: `/wrap-up` calls it at close-out when the session made an
infra change; `/log-session` delegates to it. It's also invocable directly
mid-session ("log this to the infra-log").

---

## Configure

```
INFRA_LOG_FILE: $OBSIDIAN_VAULT/Infra-Log/infra-changelog.md
```

- Invoked **directly** and `INFRA_LOG_FILE` is unset or missing → STOP, tell the
  user; never create the log somewhere else.
- Invoked **via wrap-up/log-session** and it's unset → skip silently.
- Quote paths in shell (vault paths contain spaces).

---

## What counts (scope gate)

Log it if the session changed the **agent environment / tooling**:
- Skills created, installed, edited, removed (incl. symlinks into `~/.claude/skills`)
- Claude Code config: `settings.json`, permissions, hooks, env vars, status line
- Plugins / marketplaces installed or updated
- launchd / cron jobs, automation scripts, headless wrappers
- MCP server config; new integrations

Do NOT log normal product/project work, research, or doc edits — those belong in
session logs and memory. When unsure, ask: "infra change worth logging, or just
session work?"

---

## Procedure

### Step 1 — Gate

Did the session make an in-scope infra change? If not, do nothing (no entry).

### Step 2 — Resolve the log

```bash
LOG="${INFRA_LOG_FILE/#\~/$HOME}"
[ -f "$LOG" ] || { echo "Infra log not found at $LOG"; exit 1; }   # STOP if invoked directly
```

### Step 3 — Build the entry

Newest-on-top, structured (match the file's existing convention):

```markdown
## YYYY-MM-DD — Short title

**What:** 1–3 sentences. Name the file/setting/path/command. Note state if
incomplete (e.g. "plist not yet launchctl-loaded").
**Why:** Motivation — the incident, decision, or ask behind it.
**File changed:** `path`, `path`
**Session:** [[Sessions/YYYY-MM-DD-HHMM-slug]]   ← or "not yet logged" if no session log exists
```

- One coherent change = one entry. Combine related sub-changes into one `What`.
- Bump/extend rather than duplicate: if an entry for the same change already
  exists today, update it instead of adding a second.

### Step 4 — Insert at the top of the list

Insert directly **after the file's intro `---`** (above the newest existing
`## YYYY-MM-DD` entry), with a `---` separator below your entry. Do not modify
existing entries (except the de-dupe case in Step 3).

### Step 5 — Confirm

Print the heading and file path:

```
Infra-logged → Infra-Log/infra-changelog.md: "2026-06-09 — Added embed-artifact skill"
```

---

## Edge cases

- **Log file missing** → STOP (direct) / skip (delegated). Never write elsewhere.
- **Multiple unrelated infra changes** in one session → one entry each, newest first.
- **No session log yet** → use `Session: not yet logged`; if `/log-session` runs
  later, it can backfill the link.
- **Duplicate changelog files** (a stray copy elsewhere) → flag it; don't write
  to two files.

---

## How this fits the loop

- **Work narrative:** `/log-session` → `vault/Sessions/`
- **Deliverables:** `/embed-artifact` → `vault/Projects/`
- **Environment/tooling changes:** this skill → the infra changelog
- **Close-out:** `/wrap-up` invokes all three as applicable
