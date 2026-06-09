---
name: memory-lint
description: Run a health check on an LLM memory wiki — an index file (MEMORY.md) plus one topic file per fact. Detects MEMORY.md overflow (200-line cap), bloated inline entries, orphan topic files, broken references, duplicate or empty headings, and missing/malformed frontmatter. Use when the user invokes /memory-lint, asks to "check memory", "audit memory", or "clean up memory" — also a good periodic maintenance pass.
---

# Memory Lint

Inspired by Karpathy's LLM Wiki pattern (Ingest / Query / **Lint**). If you keep
a persistent memory directory — an index file plus one topic file per fact —
this skill is the Lint operation: a deterministic health check that catches
degradation before it silently breaks recall.

## When to run

- The user asks to check, audit, or clean up memory
- After a session with heavy memory churn (many saves)
- Periodic maintenance pass
- Any time the index feels off

## How to run

```bash
# point it at your memory directory (one of these)
python3 lint.py ~/path/to/memory
MEMORY_DIR=~/path/to/memory python3 lint.py
```

The directory must contain a `MEMORY.md` index. Exit codes: 0 clean, 1 warnings, 2 errors.

## What it checks

| Check | Why it matters |
|---|---|
| **MEMORY.md line cap (200)** | Lines past the cap silently truncate — entries become invisible to context |
| **Bloated inline entries (>4 body lines)** | MEMORY.md is an index, not memory — bloat steals cap space from other entries |
| **Orphan files** | A topic file exists but isn't pointed to from MEMORY.md → never recalled |
| **Broken references** | MEMORY.md points to a file that doesn't exist → recall fails |
| **Duplicate / empty headings** | Stub or copy-paste leftovers that take up cap |
| **Frontmatter present + valid type** | Topic files need `type: user/feedback/project/reference` |
| **Naming convention** | `{type}_{topic}.md` is the convention; legacy bare names get flagged info-only |

## After running

1. Show the report to the user as-is.
2. If errors exist, propose specific fixes (extract bloated section X to file Y, delete duplicate heading Z).
3. **Do not auto-edit memory files without confirmation** — memory edits affect every future session.
4. After fixes are made, re-run lint to confirm clean.

See `README.md` in this folder for the full memory-wiki convention this lints against, and how to add new checks.
