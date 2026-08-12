# claude-skills

A collection of reusable [Claude Code](https://claude.ai/claude-code) skills (slash commands) for common development workflows.

## What is a skill?

A skill is a markdown file that becomes a `/slash-command` in Claude Code. Drop it in `~/.claude/skills/<name>/SKILL.md` and type `/name` in any session to run it. Claude can also trigger skills automatically based on the description in the frontmatter.

See the [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) for more on skills.

## Installation

Copy any skill directory into your global skills folder:

```bash
cp -r skills/wrap-up ~/.claude/skills/wrap-up
```

Or clone the whole repo and symlink:

```bash
git clone https://github.com/bryanfosler/claude-skills.git ~/claude-skills
ln -s ~/claude-skills/skills/wrap-up ~/.claude/skills/wrap-up
```

---

## Skills

### `/decision-brief`

Turns a body of work, a document, or a set of documents into a formal, **answer-first executive decision brief** — a recommendation memo, not a recap or a plan. One self-contained HTML file with a two-altitude toggle: an **Executive 1-pager** for leadership and a **Detailed ~3-pager** for the team that has to defend or build it.

**Format:** a solid-accent recommendation hero (the verdict, up top), a flexible strip of concrete date/fact stats, numbered scannable zones, and a ranked options table with the recommended row marked — modeled on a real decision-brief + executive-summary house style, not an essay.

**Built in:** prints to a clean one-page PDF from Chrome (⌘P), per-section clean-copy for pasting into Teams/email, an on-screen page-break boundary, inline edit + comments, and a **never-fabricate-a-conclusion** rule (it asks rather than inventing a recommendation the evidence doesn't support). Light/cream, single-accent, quiet. Composes with `/embed-artifact` for Obsidian.

→ [skills/decision-brief/SKILL.md](skills/decision-brief/SKILL.md)

---

### `/wrap-up`

End-of-session checklist that runs automatically when you say "wrap up" or "close session".

**Four phases:**
1. **Ship It** — commit & push, GitHub issue tracking, time + token logging, session log, Obsidian notes, learning log
2. **Remember It** — routes new knowledge to the right tier of Claude's memory hierarchy
3. **Review & Apply** — scans the conversation for self-improvement findings and auto-applies them
4. **Publish It** — identifies content worth sharing publicly and drafts posts for your approval

The skill is modular — each optional feature (Obsidian, Notion, token tracking) is clearly marked and can be skipped by leaving its config variable unset.

→ [skills/wrap-up/SKILL.md](skills/wrap-up/SKILL.md)

---

### `/long-running-agent-harness`

Harness for AI agent workflows that span multiple context windows, hours, or days. Prevents agents from losing continuity between sessions, redoing completed work, or declaring victory too early.

**Three continuity artifacts:**
- `feature_list.json` — exhaustive, testable feature ledger (flat or phase-gated hierarchy)
- `claude-progress.txt` — append-only session log (read first, write last)
- `init.sh` — reproducible startup script

**Two roles:** Initializer (once) creates artifacts + baseline commit. Coding agent (every session) reads artifacts, verifies baseline, implements one feature, commits.

**Best paired with** superpowers `executing-plans` (inline) as the within-session execution engine.

Based on [Anthropic's "Effective Harnesses for Long-Running Agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

→ [skills/long-running-agent-harness/SKILL.md](skills/long-running-agent-harness/SKILL.md)

---

### `/self-improving-loop`

Run a task as an autonomous self-checking loop that improves its own approach each pass until it clears a goal or exhausts a loop budget. For tasks Claude doesn't one-shot well, where a defined quality signal can tell good from bad and each failure teaches the next prompt.

**The loop:** produce → score → diagnose → amend → repeat. Keep-or-discard against best-so-far; stop on goal cleared, budget hit, or K passes with no gain.

**Hard gate:** no checker, no loop. Leads with defining the goal signal (rubric / assertion / verifier-agent) so "improve" isn't vibes.

**Cost-aware:** deterministic checker = free scoring; single judge by default, panel only for taste work; inline mode avoids subagent fan-out entirely. See the "Cost vs output" section.

**Two modes:** autonomous (Workflow-orchestrated, walk-away) with a drop-in script template, or inline single-pass. Sibling to `long-running-agent-harness` — that one is self-*continuing* across sessions; this one is self-*improving* within a task.

→ [skills/self-improving-loop/SKILL.md](skills/self-improving-loop/SKILL.md)

---

### `/qa`

A QA checkpoint to run before moving on or shipping. Reads the actual `git diff`, generates a **specific** test checklist tailored to the change type (UI control, API endpoint, bug fix, refactor…), waits for you to test, then records a clean pass or routes found issues back into build mode.

→ [skills/qa/SKILL.md](skills/qa/SKILL.md)

---

### `/handoff`

Generates a paste-ready handoff document so the next session can resume cold — no "what were we doing?" re-exploration. Enforces a six-question quality bar (goal, done, left, next action, prerequisite reads, scope guardrail) and ships a fill-in template.

→ [skills/handoff/SKILL.md](skills/handoff/SKILL.md)

---

### `/scaffold-sessions-md`

Creates a `sessions.md` session-log file at the project root in a consistent, reverse-chronological format — the file `/wrap-up` appends to at the end of every session.

→ [skills/scaffold-sessions-md/SKILL.md](skills/scaffold-sessions-md/SKILL.md)

---

### `/scaffold-claude-md`

Creates an opinionated project-level `CLAUDE.md` (not the generic `/init` output). A deterministic Python analyzer collects project facts — stack, git remote, layout, build/test commands, env vars, hardware signals — then the skill writes house-format prose around them for your review.

→ [skills/scaffold-claude-md/SKILL.md](skills/scaffold-claude-md/SKILL.md)

---

### `/memory-lint`

Health check for an LLM memory wiki (an index file plus one topic file per fact, à la Karpathy's LLM Wiki pattern). Catches the failure that silently breaks recall: index overflow past the 200-line cap, bloated inline entries, orphan files, broken references, duplicate/empty headings, and malformed frontmatter.

→ [skills/memory-lint/SKILL.md](skills/memory-lint/SKILL.md)

---

### `/sync-project-board`

Syncs open GitHub issues across multiple repos onto a single GitHub Projects (v2) board. Works around the v2 limitation that "Auto-add to project" only watches one repository per project. Idempotent — set your owner, project number, and repo list in `sync.sh`.

→ [skills/sync-project-board/SKILL.md](skills/sync-project-board/SKILL.md)

---

### `/log-session`

Writes a clean, retrieval-optimized session log to an Obsidian vault — the **write** half of the [Obsidian Agent-Brain Kit](obsidian-agent-brain/workflow-guide.md). Each log carries a one-line `summary` that the on-load hook and `/recall` read first. Text-only (no git/issues); appends an update on same-day re-runs.

→ [skills/log-session/SKILL.md](skills/log-session/SKILL.md)

---

### `/recall`

Searches an Obsidian vault (synthesis-first, then session logs) and answers **with citations** — the **on-demand read** half of the agent-brain loop. Pairs with `/log-session` and the on-load context hook.

→ [skills/recall/SKILL.md](skills/recall/SKILL.md)

### `/embed-artifact`

Makes a generated HTML (or visual) artifact viewable **inside** Obsidian: copies it into a vault project folder and scaffolds a `.md` wrapper with an absolute `file://` iframe **plus** the artifact's diagrams as native Mermaid (so the note renders even if the iframe is blocked). Default refreshes the latest version in place; "log all" keeps timestamped copies. The **artifact** half of the loop — composed by `/log-session` and `/wrap-up`.

→ [skills/embed-artifact/SKILL.md](skills/embed-artifact/SKILL.md)

### `/log-infra-change`

Appends a structured entry to an infrastructure changelog (`INFRA_LOG_FILE`) for tooling/environment changes — skill installs/edits, Claude Code config & hooks, launchd/cron jobs, plugin/marketplace changes, symlinks, MCP config. The gap that session logs and memory don't cover. Invocable directly, and composed by `/wrap-up` and `/log-session`.

→ [skills/log-infra-change/SKILL.md](skills/log-infra-change/SKILL.md)

---

## PM automation suite

Four skills that turn a calendar, a Teams tenant, and a Smartsheet program bowler into
written vault artifacts. All are **read-only on their sources** and write only to the vault.
Each has a `## Configure` block — set `OBSIDIAN_VAULT` (and for `/portfolio-check`, the
sheet id + a Keychain token) before first run. All four require an authorized Microsoft 365
connector except `/portfolio-check`, which needs a Smartsheet API token.

### `/morning-brief`

Pulls today's Microsoft 365 calendar, filters out cadence/template blocks, and writes a
prep-focused brief — today's meetings with enough context to walk in prepared — to
`Sessions/Briefings/`. Idempotent. Designed to run unattended before the workday.

→ [skills/morning-brief/SKILL.md](skills/morning-brief/SKILL.md)

### `/meeting-notes`

Three-phase transcript pipeline: pulls Teams transcripts for the past 10 business days,
lands VTTs on disk, then dispatches subagents that read local files only (no MCP, no auth
overhead) to produce paired summary notes. Idempotent — skips meetings already summarized.
Handles the recurring-URI multi-segment bug by scoring each segment against the target date.

→ [skills/meeting-notes/SKILL.md](skills/meeting-notes/SKILL.md)

### `/stream-transcript`

The fallback when Graph transcript access is closed off by tenant policy (403
`GraphAccessToTranscriptsDisabled`), the recording exceeds the connector's 100 MB fetch cap,
or the call was ad-hoc with no calendar event. Calls the SharePoint/Stream REST API from
inside the page via the user's own browser session and lifts the player's in-memory turn
data — producing a speaker-labeled `<v Name>` VTT with no manual export. Also the fallback
for `/meeting-notes` Phase 1.3.

→ [skills/stream-transcript/SKILL.md](skills/stream-transcript/SKILL.md)

### `/portfolio-check`

Read-only scan of a Smartsheet program bowler for programs drifting, stalled, blocked,
past-due, or marked Green-but-overdue. Exception-only — healthy programs get one summary
line. Every claim is tagged **FACT / INFERENCE / HYPOTHESIS** with its source row, and the
`contradiction` rule (Health=Green while showing trouble) is surfaced, never resolved. Stops
and reports rather than emitting a misleading brief if the sheet structure changed.

→ [skills/portfolio-check/SKILL.md](skills/portfolio-check/SKILL.md)

---

## Visual deliverables

### `/visual-plan`

Turns a text plan into a rich interactive visual plan — diagrams, file maps, annotated code,
open questions, UI wireframes — as a single self-contained HTML file you can edit, comment
on, and embed in Obsidian. No server, no sign-in, nothing leaves the machine.

→ [skills/visual-plan/SKILL.md](skills/visual-plan/SKILL.md)

### `/visual-recap`

Same output shape, pointed at a PR, branch, commit, or diff: diagrams, file maps, API/schema
summaries, annotated diffs, and review notes in one self-contained HTML file.

→ [skills/visual-recap/SKILL.md](skills/visual-recap/SKILL.md)

---

## Thinking tools

### `/grill-me`

Interviews you relentlessly about a plan or design, resolving each branch of the decision
tree until you reach shared understanding. Use it to stress-test before you build.

→ [skills/grill-me/SKILL.md](skills/grill-me/SKILL.md)

### `/grill-with-docs`

`/grill-me` plus a memory: challenges the plan against your existing domain model, sharpens
terminology, and updates `CONTEXT.md` / ADRs inline as decisions crystallize. Formats for
both are in the skill directory.

→ [skills/grill-with-docs/SKILL.md](skills/grill-with-docs/SKILL.md)

### `/clip`

Copies text to the macOS clipboard via `pbcopy` so it pastes cleanly, instead of being
selected out of the terminal where line-wrapping and timestamps get baked into the
selection. Useful right after producing a message draft or any multi-line block.

→ [skills/clip/SKILL.md](skills/clip/SKILL.md)

---

## Obsidian Agent-Brain Kit

A complete, adoptable loop for using an Obsidian vault as your AI agent's long-term
memory: the agent **logs what it does** and **pulls that context back** at session
start or on demand. Works with Claude Code, Codex, or any agent — the vault is just
a folder of Markdown.

**The loop:**
- **Write** — `/log-session` captures each session as a structured log
- **Read on load** — `load-vault-context.py` (a SessionStart hook) injects recent context so new sessions start warm
- **Read on demand** — `/recall` searches the vault and answers with citations
- **Embed deliverables** — `/embed-artifact` puts HTML/visual artifacts in the vault as notes you can view in Reading view
- **Log environment changes** — `/log-infra-change` records tooling/config/skill changes to an infra changelog
- **Schema** — `AGENTS.template.md` is the rulebook both sides obey

Never used Obsidian? → [obsidian-agent-brain/onboarding.md](obsidian-agent-brain/onboarding.md) (5-minute setup).
Full workflow, setup, and upgrade paths → [obsidian-agent-brain/workflow-guide.md](obsidian-agent-brain/workflow-guide.md).

---

## Optional Setup

### Token & Cost Tracking

Track how many tokens each session uses and the estimated API cost. Useful for understanding your usage patterns over time.

**How it works:**
Claude Code stores session transcripts as JSONL files in `~/.claude/projects/`. The script reads your current session, sums all token counts across assistant turns, and calculates cost using Anthropic's published rates.

**Setup:**
```bash
# Copy the script somewhere on your PATH or a known location
cp utils/session_tokens.py ~/utils/session_tokens.py

# Test it
python3 ~/utils/session_tokens.py
# Output: Tokens: 1234567  Cost: 4.56
```

Then set `SESSION_TOKENS_SCRIPT` in the skill's Configure section.

**Update pricing** in `session_tokens.py` if Anthropic changes rates — the `PRICING` dict is at the top of the file.

→ [utils/session_tokens.py](utils/session_tokens.py)

---

### Obsidian Session Log

Automatically writes a structured session summary to your Obsidian vault at the end of every session. Great for building a searchable history of your work.

**How it works:**
The skill writes a markdown file named `YYYY-MM-DD-HHmm-short-slug.md` to a `sessions/` folder in your vault. If your vault syncs via iCloud, Syncthing, or Obsidian Sync, it appears on all your devices automatically.

**Setup:**
1. Create a `sessions/` folder inside your Obsidian vault
2. Set `OBSIDIAN_SESSIONS_DIR` in the skill's Configure section:
   ```
   OBSIDIAN_SESSIONS_DIR: ~/path/to/vault/sessions
   ```

That's it — no plugins required. The output is plain markdown.

---

### Notion Sync via GitHub Actions

Automatically syncs your GitHub issues to a Notion database whenever you post a time/token comment. Great for tracking work across projects in one place.

**How it works:**
When the wrap-up skill posts a comment matching `Time: Xm` on a GitHub issue, a GitHub Actions workflow fires and creates or updates a row in your Notion database with the issue metadata, time spent, tokens, and cost.

**Setup:**

1. **Create a Notion integration**
   - Go to https://www.notion.so/my-integrations → New integration
   - Copy the "Internal Integration Secret" — this is your `NOTION_API_KEY`

2. **Create or reuse a Notion database**
   Add these properties (exact names and types matter):

   | Property | Type |
   |---|---|
   | Title | Title |
   | Status | Select |
   | Labels | Multi-select |
   | GitHub URL | URL |
   | Created | Date |
   | Project | Select |
   | Time Spent (min) | Number |
   | Tokens | Number |
   | API Equiv ($) | Number |
   | Week | Select |
   | Month | Select |

   Then share the database with your integration: open the database → ••• → Connections → add your integration.

3. **Get the database ID**
   From the database URL:
   `https://notion.so/your-workspace/DATABASE_ID?v=...`
   Copy the `DATABASE_ID` portion.

4. **Add the workflow to your repo**
   ```bash
   mkdir -p .github/workflows
   cp path/to/claude-skills/.github/workflows/notion-sync.yml .github/workflows/
   ```
   Edit the two placeholders at the top of the workflow:
   ```yaml
   NOTION_DB_ID: "YOUR_NOTION_DATABASE_ID"
   PROJECT_NAME: "Your Project Name"    # must match a Notion select option
   ```

5. **Add your Notion API key as a GitHub secret**
   ```bash
   gh secret set NOTION_API_KEY --body "secret_..."
   ```

6. Set `NOTION_SYNC: true` in the skill's Configure section.

The workflow runs on `issue_comment` events — no polling, no cron.

→ [.github/workflows/notion-sync.yml](.github/workflows/notion-sync.yml)

---

### GitHub Project Board Tracking

Automatically adds issues to a GitHub Project board so your board stays current without manual triage.

**Setup:**
1. Find your project number — it's in the URL when you open the board:
   `https://github.com/users/USERNAME/projects/PROJECT_NUMBER`
2. In the skill's Configure section, set your project number where prompted in step 6b.
3. The skill will run:
   ```bash
   gh project item-add PROJECT_NUMBER --owner GITHUB_USERNAME --url ISSUE_URL
   ```

Works best if you have one project board per repo (or a single unified board across repos).

---

### Learning Log

At the end of each session, the skill checks whether any meaningful technical concepts, debugging stories, or "aha moments" came up. If so, it appends a new section to `learnings.md` in your project.

**No setup required** — just make sure the skill can write to your project directory. The file is created automatically if it doesn't exist.

The goal is a readable, growing record of *why* things work the way they do — written like you're explaining to a curious friend, not a spec sheet.

---

## Contributing

PRs welcome. Each skill lives in its own directory: `skills/<name>/SKILL.md`.
Supporting files (templates, examples, scripts) can live alongside it in the same directory.
