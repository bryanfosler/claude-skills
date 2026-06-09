# Memory Wiki — System Reference

A persistent, LLM-maintained knowledge base for Claude Code, and the lint.py
health check that keeps it trustworthy.

Inspired by Andrej Karpathy's LLM Wiki pattern:
https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

(Saved as .txt rather than .md so it won't be picked up as the skill's primary doc.)

## What it is

A memory wiki is a directory of markdown files: an index (MEMORY.md) plus one
topic file per fact Claude has learned. It persists across conversations — every
session starts with MEMORY.md loaded into context, and Claude reads a linked
topic file on demand when an entry is relevant.

It has three layers (per Karpathy's pattern):

| Layer | Where | Editable by |
|---|---|---|
| Schema | the "memory" section of the system prompt | the platform |
| Wiki | <memory-dir>/*.md | Claude (writes during conversations) |
| Index | <memory-dir>/MEMORY.md | Claude (kept under a 200-line cap) |

## Three operations

| Op | Trigger | What happens |
|---|---|---|
| Ingest | During a conversation when something worth remembering is said | Claude writes a new topic file + adds an index entry |
| Query | Any future conversation | Claude recalls from the loaded index, optionally reads a topic file |
| Lint | Manually with /memory-lint, or on a schedule | Health check — overflow, bloat, orphans, broken refs, frontmatter |

## File naming convention

{type}_{topic}.md where type is one of:

- user_*      — facts about the user (role, preferences, knowledge)
- feedback_*  — guidance on how to work (corrections + validated approaches)
- project_*   — ongoing initiatives, status, decisions
- reference_* — pointers to external systems, infra, schemas

Each topic file has YAML frontmatter:

    ---
    name: short title
    description: one-line hook used to decide relevance
    type: user | feedback | project | reference
    ---

## MEMORY.md format

It is an INDEX, not memory. Each line is one of:

    - [Title](file.md) — short hook describing what's inside

Hard cap: 200 lines. Beyond that, the system silently truncates and entries
become invisible to context. Lint catches this.

## How to invoke lint

    # slash command (preferred)
    /memory-lint

    # or directly — point at your memory directory
    python3 lint.py ~/path/to/memory
    MEMORY_DIR=~/path/to/memory python3 lint.py

Exit codes: 0 clean, 1 warnings, 2 errors.

## Checks performed

| Check | Why |
|---|---|
| MEMORY.md <= 200 lines | Past 200 = silent truncation |
| Bloated inline entries (> 4 non-pointer lines) | MEMORY.md is index, not detail |
| Orphan files (on disk, not in index) | Never recalled, dead weight |
| Broken markdown link / "See" references | Recall target missing |
| Duplicate or empty headings | Stub leftovers waste cap |
| Frontmatter present, type valid | Without frontmatter, type-based filtering breaks |
| Naming convention | {type}_{slug}.md (legacy bare names flagged INFO-only) |

## How to extend

Adding a new check is straightforward:

1. Open lint.py
2. Add a new "# CHECK N:" block in main()
3. Append to errors (exit 2), warnings (exit 1), or info (exit 0)
4. Re-run on a memory dir to confirm the signal/noise tradeoff

If a check produces too many false positives, tighten the regex (see
referenced_files() for an example of placeholder/external-pointer filtering).

## Background — why this pattern

Karpathy's gist argues that LLM-maintained wikis beat raw-document RAG because the
wiki COMPOUNDS: cross-references and synthesis accumulate, so future queries don't
need to re-derive context. Most memory systems implement Ingest (auto-save) and
Query (recall) but skip Lint — the maintenance pass that catches drift before the
index silently exceeds its cap and starts losing entries to truncation.
