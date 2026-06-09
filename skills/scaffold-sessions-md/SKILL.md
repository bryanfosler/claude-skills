---
name: scaffold-sessions-md
description: Use when starting a new project, adding session tracking to an existing repo, or whenever the user asks to "create a sessions.md" or "set up session logging" — produces a standard session-log file
---

# Scaffold sessions.md

## What this does

Creates a `sessions.md` file at the project root using a standard session-log format. This is the file `/wrap-up` appends to at the end of every session.

## When to use

- New project bootstrap
- Existing repo missing session tracking
- The user says "create a sessions.md", "add session logging", "set up the session log file"

## How to use

1. Detect the project name from the directory or `package.json` / `Cargo.toml` / `pyproject.toml` (or ask if ambiguous).
2. Write `sessions.md` at the project root using `template.md` in this skill folder.
3. Replace `{{PROJECT_NAME}}` with the detected name.
4. If `sessions.md` already exists, STOP and tell the user — never overwrite.

## Format

The template produces a header and a Session 1 placeholder. Subsequent sessions are appended in **reverse-chronological order** (newest at top), which keeps the most relevant entry visible without scrolling.

Each session block uses:

```markdown
## Session N — [Title]

**Date:** MM.DD.YYYY
**Time spent:** ~Xh Xm

### What We Built
-

### What Shipped
-

### Bugs Fixed
-

### Decisions Made
-
```

## Output

Confirm with: `Created sessions.md for <project-name>. Ready for first session entry via /wrap-up.`

## Common mistakes

- **Overwriting existing file** — always check first; if present, ask before clobbering
- **Inconsistent date format** — pick one (`MM.DD.YYYY` here) and stay consistent so the log is scannable
- **Forgetting the project name in the header** — keeps cross-project search useful
