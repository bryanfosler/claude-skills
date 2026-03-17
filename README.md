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
git clone https://github.com/bryanfosler/claude-skills.git ~/Documents/claude-skills
ln -s ~/Documents/claude-skills/skills/wrap-up ~/.claude/skills/wrap-up
```

## Skills

### `/wrap-up`

End-of-session checklist that runs automatically when you say "wrap up" or "close session".

**Four phases:**
1. **Ship It** — commit & push, file placement check, GitHub issue + time logging, session log entry, learnings log
2. **Remember It** — routes new knowledge to the right tier of Claude's memory hierarchy (auto memory, CLAUDE.md, project rules)
3. **Review & Apply** — scans the conversation for self-improvement findings and auto-applies them
4. **Publish It** — identifies content worth sharing publicly and drafts posts for your approval

**Customize it** by editing your local copy to add your own repo paths, project board numbers, and preferred logging tools.

→ [skills/wrap-up/SKILL.md](skills/wrap-up/SKILL.md)

---

## Contributing

PRs welcome. Each skill lives in its own directory: `skills/<name>/SKILL.md`.
Supporting files (templates, examples) can live alongside it in the same directory.
