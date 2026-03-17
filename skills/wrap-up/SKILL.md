---
name: wrap-up
description: Use when user says "wrap up", "close session", "end session",
  "wrap things up", "close out this task", or invokes /wrap-up — runs
  end-of-session checklist for shipping, memory, and self-improvement
---

# Session Wrap-Up

Run four phases in order. All phases auto-apply without asking; present a
consolidated report at the end.

---

## Phase 1: Ship It

**Commit & push:**
1. Run `git status` in each project repo that was touched this session
2. If uncommitted changes exist, stage relevant source files (never `git add -A`
   — avoid accidentally staging `.env`, build artifacts, or binary files) and
   commit with a descriptive message ending with:
   `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
3. Push to `origin main`

**File placement check:**
4. If any files were created this session, verify they are in the right location:
   - Skills (Skill tool) belong in `~/.claude/skills/<skill-name>/SKILL.md`
   - Native CC slash commands belong in `~/.claude/commands/<name>.md`
   - Doc/reference files belong at the project root, not buried in source folders
5. Auto-fix any misplaced files — no need to ask

**GitHub issue pipeline:**
6. For each repo that had work done, run all of these steps in order:

   **a) Find or create the issue:**
   - Check for an open issue covering this session's work
   - If none exists, create one:
     ```
     gh issue create --repo YOUR_USERNAME/REPO --title "..." --body "..."
     ```

   **b) Add issue to the GitHub Project board (if you use one):**
   ```
   gh project item-add PROJECT_NUMBER --owner YOUR_USERNAME --url ISSUE_URL
   ```

   **c) Log time on the issue:**
   - Post a comment with how long the session took:
     ```
     gh issue comment ISSUE_NUMBER --repo YOUR_USERNAME/REPO --body "Time: Xm"
     ```
   - Round to nearest 5 minutes; formats: `45m`, `1h`, `1h30m`, `2h`

   **d) Close the issue if work is complete:**
   ```
   gh issue close ISSUE_NUMBER --repo YOUR_USERNAME/REPO
   ```

**Session log:**
7. Append a new entry to the project's `sessions.md` file (create it if it
   doesn't exist) using this format:

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

**Learning log:**
8. If the session produced meaningful new technical concepts, debugging stories,
   or "aha moments", add a new section to the project's `learnings.md` (create
   if it doesn't exist).
   Write it engagingly — like explaining to a curious friend, not a spec sheet.
   Use analogies, reference what we actually tried, explain the *why*.
   Skip this step if the session was minor changes with nothing worth teaching.

**Task cleanup:**
9. Check the task list for in-progress or stale items
10. Mark completed tasks as done, flag orphaned ones

---

## Phase 2: Remember It

Review what was learned this session. Place each piece of knowledge in the
right spot in the memory hierarchy:

**Memory placement guide:**
- **Auto memory** — Debugging patterns, project quirks, one-off discoveries
- **Global `CLAUDE.md`** — Rules and conventions that apply across all projects
  (working style, decision framework, session process)
- **Project `CLAUDE.md`** — Permanent project rules: architecture decisions,
  build commands, key file locations
- **`.claude/rules/`** — Topic-scoped rules with `paths:` frontmatter
- **`CLAUDE.local.md`** — Private per-project context (current blockers, local
  URLs, sandbox creds) — not committed

**Decision framework:**
- Global working style / session process → global `CLAUDE.md`
- Project-specific architecture or conventions → project `CLAUDE.md`
- Scoped to specific file types → `.claude/rules/` with `paths:`
- Pattern Claude discovered → auto memory
- Personal ephemeral context → `CLAUDE.local.md`

---

## Phase 3: Review & Apply

Analyze the conversation for self-improvement findings. If the session was
short or routine with nothing notable, say "Nothing to improve" and move on.

**Auto-apply all actionable findings immediately** — do not ask for approval.
Apply the change, commit if it's a file edit, then summarize.

**Finding categories:**
- **Skill gap** — Things Claude got wrong, needed multiple attempts at, or
  misunderstood about the project setup
- **Friction** — Steps the user had to ask for explicitly that should have been
  automatic
- **Knowledge** — Facts about the project or preferences Claude didn't know but
  should (add to appropriate CLAUDE.md)
- **Automation** — Repetitive patterns that could become a skill, hook, or script

**Action types:**
- **Global CLAUDE.md** → your workspace root CLAUDE.md
- **Project CLAUDE.md** → the project's CLAUDE.md
- **Rules** → `.claude/rules/` file
- **Auto memory** → save for future sessions
- **New skill spec** → draft `~/.claude/skills/<name>/SKILL.md`

Present findings in two sections:

Findings (applied):

1. ✅ Friction: [description]
   → [Where it was applied] [What was changed]

---
No action needed:

2. Knowledge: [description]
   Already documented in [location]

---

## Phase 4: Publish It

After all other phases are complete, review the full conversation for content
worth sharing. Good material includes:

- Interesting bugs and how they were solved
- Technical decisions with non-obvious reasoning
- Learning moments that other developers would recognize
- Project milestones or shipped features

**If publishable material exists**, draft the post and save it to a `Drafts/`
folder, then present it for approval. Suggest a platform (Reddit, blog, etc.)
and wait for the user to respond before posting.

**Scheduling:**
- Don't post multiple items from the same session at once
- Space posts at least a few hours apart on the same platform

**If nothing publishable:** Say "Nothing worth publishing from this session."
