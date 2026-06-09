# AI Agent + Obsidian: a logging & context-recall workflow

A complete, adoptable loop for using an Obsidian vault as your AI agent's
long-term memory — so Claude Code, Codex, or any agent **logs what it does** and
**pulls that context back** at the start of the next session or on demand.

This guide ties together the pieces in this repo:

- `skills/log-session/` — **write**: capture a session as a clean log
- `skills/recall/` — **read on demand**: search the vault and answer with citations
- `obsidian-agent-brain/load-vault-context.py` — **read on load**: inject recent context at session start
- `obsidian-agent-brain/AGENTS.template.md` — **the schema** both sides obey
- `obsidian-agent-brain/onboarding.md` — 5-minute setup for Obsidian newcomers

---

## The problem it solves

Every agent session starts cold. You re-explain the project, the decisions, what
broke last time. The agent re-derives context you already paid for. The job to be
done is simple: **stop re-explaining context every session.**

That job has three parts:

1. **Capture** — every session leaves a durable, structured trace.
2. **Recall on load** — a new session starts already knowing where things stand.
3. **Recall on demand** — mid-task, the agent can search prior decisions and sessions.

Most "second brain for AI" tools nail capture and on-demand search. The
underserved part — and the point of this kit — is **#2 plus the bidirectional
loop**: logs written in a shape specifically optimized to be retrieved and
injected, governed by one schema both the writer and reader obey.

---

## The loop

```
        ┌──────────────  AGENTS.md  (the schema both sides obey)  ──────────────┐
        │   folder roles · frontmatter (type/source/date/summary/tags) · rules   │
        └────────────────────────────────────────────────────────────────────────┘

   WRITE (capture)            READ — on load                READ — on demand
   ┌──────────────┐           ┌─────────────────────┐       ┌─────────────────────┐
   │ /log-session │ ─writes─▶ │ SessionStart hook   │       │ /recall  (skill)    │
   │              │  dated,   │ load-vault-context  │       │  rg over vault,     │
   │              │  tagged,  │ injects recent      │       │  synthesis-first,   │
   │              │  summary  │ summaries on start  │       │  answers w/ citation│
   └──────────────┘           └─────────────────────┘       └─────────────────────┘
           │                            ▲                              ▲
           └──────────── vault/sessions/  +  Decisions/ + Projects/ ───┴──────────┘
```

The `summary:` line each log carries is the connective tissue: cheap for the
on-load hook to grab, and the highest-signal field for `/recall` to rank on.

---

## The four components

### 1. The schema — `AGENTS.md`

One file at the vault root that tells every agent: which folders are raw vs.
synthesis, what frontmatter to write, and the three operations (ingest, query,
lint). Without it, agents either refuse to touch the vault or churn it
inconsistently. Copy `AGENTS.template.md`, edit the folder map, done.

This follows the **LLM Wiki pattern**: raw sources stay immutable; agents
maintain a distilled synthesis layer; you read the synthesis, not the raw text.

### 2. Write — `/log-session`

At the end of a session (or mid-session for a checkpoint), the agent writes a
structured log to `sessions/`: a one-line summary, what was done, decisions,
current state, open questions, next steps. Re-running the same day appends an
update rather than duplicating. Text-only — it doesn't commit code or touch
issues; that's a separate concern.

### 3. Read on load — `load-vault-context.py`

A SessionStart hook reads the `summary:` line from the N most recent session
logs and prints a compact briefing, which the agent harness injects as context.
Every new session opens already knowing the last few things that happened.

Claude Code wiring (`~/.claude/settings.json`):

    {
      "hooks": {
        "SessionStart": [
          { "hooks": [
              { "type": "command",
                "command": "OBSIDIAN_SESSIONS_DIR=~/vault/sessions python3 /path/to/load-vault-context.py" }
          ] }
        ]
      }
    }

Other agents: run the same script from your startup convention and feed its
stdout into the model's context. The script is agent-agnostic — it just prints
Markdown.

### 4. Read on demand — `/recall`

When you ask "what did we decide about X?" or "have we done Y before?", `/recall`
searches the vault synthesis-first (decisions and concepts before raw sessions),
reads the top matches, and answers **with citations** to the notes it used. If
the vault doesn't have it, it says so and offers to capture the answer.

---

## Setup in five steps

1. Make a vault folder with `sessions/`, `Decisions/`, `Projects/`, `Clippings/`.
2. Copy `AGENTS.template.md` → vault root as `AGENTS.md`; edit the folder map.
3. Install `skills/log-session` and `skills/recall`; set `OBSIDIAN_SESSIONS_DIR`
   and `OBSIDIAN_VAULT_DIR`.
4. Wire `load-vault-context.py` to a SessionStart hook.
5. Work normally. Say "log this session" when you finish. Watch the next session
   start with context.

New to Obsidian? Read `onboarding.md` first — it's a folder of Markdown, nothing more.

---

## The one tradeoff to understand

This kit is a **write-time synthesis** system: the thinking happens when you log
and curate, and you read the distilled result. The opposite approach is
**query-time retrieval** (a vector database that captures raw thoughts fast and
re-derives meaning per query). They fail in opposite ways:

- A neglected wiki **lies confidently** — a stale synthesis note still reads as
  true. Mitigate by checking `date:` on what you cite and running periodic lint.
- A neglected vector store **retrieves noise** — it returns the closest match
  even when the closest match is garbage.

This is why `/recall` searches synthesis-first but always respects recency, and
why the schema includes a lint operation. Curate, or the brain rots.

---

## Upgrade paths (only when you feel the pain)

- **Semantic search.** Plain `rg` (what `/recall` uses) is keyword-based. When
  keyword search stops finding things you know are there, add an Obsidian MCP
  server or a small vector index *alongside* the vault — not replacing it. The
  vault stays the browsable source of truth; the index is a retrieval accelerant.

- **Multiple agents.** If several agents share the vault, the schema's cross-agent
  rules (author your own files, cite peers', resolve conflicts by appending not
  overwriting) keep them from clobbering each other. Add a per-agent `source:`
  value and let each own its `sessions/` subfolder.

- **Passive capture.** If you want thoughts captured outside agent sessions
  (e.g. from chat), a continuous-capture memory layer can feed the vault. Add it
  when "I told one agent something the others don't know" becomes a real, repeated
  problem — not before.

Start with the four components. Add an upgrade only when a concrete pain point
names itself.
