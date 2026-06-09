# Never used Obsidian? Start here (5 minutes)

You do **not** need to learn Obsidian to use this. The whole system is just a
folder of plain-text Markdown files. Obsidian is one nice way to browse them —
but your AI agent reads and writes the files directly, with or without the app.

## What Obsidian actually is

A free app that opens a folder of `.md` (Markdown) files and lets you browse,
search, and link between them. The folder is called a **vault**. That's it.
No database, no cloud lock-in — your notes are files on disk you fully own.

- Download: https://obsidian.md (optional — the agent loop works on the files alone)
- `[[double brackets]]` make links between notes. Frontmatter (the `---` block
  at the top of a file) holds metadata like date and tags.

## The 5-folder starter vault

Create a folder anywhere (this is your vault) with these subfolders:

    my-vault/
    ├── AGENTS.md          ← the rulebook agents read first (copy the template)
    ├── sessions/          ← session logs your agent writes (the "what happened" trail)
    ├── Decisions/         ← distilled decisions + rationale
    ├── Projects/          ← one note per project
    └── Clippings/         ← raw sources you save (articles, transcripts)

That's the whole structure. Everything else is optional.

## Wire it up (3 steps)

1. **Copy the schema.** Put `AGENTS.template.md` at your vault root as `AGENTS.md`
   and edit the folder map to match. This tells every agent how to behave.

2. **Install the two skills.** Copy `skills/log-session` and `skills/recall` into
   your agent's skills folder (for Claude Code: `~/.claude/skills/`). Set
   `OBSIDIAN_SESSIONS_DIR` and `OBSIDIAN_VAULT_DIR` in each.

3. **Turn on auto-recall (optional but the magic part).** Wire
   `load-vault-context.py` to a SessionStart hook so every new session opens
   already knowing your recent work. See `workflow-guide.md` for the snippet.

## The loop you just built

- You work with your agent like normal.
- At the end (or mid-session), say "log this session" → a clean log lands in `sessions/`.
- Next time you start, the agent already knows where you left off (on-load hook).
- Anytime, ask "what did we decide about X?" → `/recall` searches the vault and answers with citations.

No more re-explaining context every session. Read `workflow-guide.md` for the
full picture and the upgrade paths (semantic search, multi-agent).
