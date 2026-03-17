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
