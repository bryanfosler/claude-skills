---
name: scaffold-claude-md
description: Use when starting a new project, when a project is missing CLAUDE.md, or when the user asks to "analyze this project and create a CLAUDE.md" — produces an opinionated project-level CLAUDE.md (not the generic /init output)
---

# Scaffold project CLAUDE.md

## What this does

Creates a `CLAUDE.md` at the project root using an opinionated house format — specific about sections, tone, and what belongs vs. doesn't. Different from Claude Code's built-in `/init` (which is generic).

## When to use

- New project where CLAUDE.md doesn't exist
- Existing project where CLAUDE.md is too thin or doesn't match the house format
- The user says: "analyze this project and create a CLAUDE.md", "make a CLAUDE.md for this repo", "scaffold project context"

## How to use

**Step 1 — Gather facts (deterministic):**
Run the analyzer script to collect project facts:

```bash
python3 project_analyzer.py <project-path>
```

This outputs a JSON report with: project name, detected stack, git remote, top-level layout, build/run/test commands (if standard), and detected hardware/config files.

**Step 2 — Write prose (judgment):**
Use `template.md` as the skeleton. Fill in the prose sections using:
- Facts from the analyzer
- README content if present
- Existing code structure inspection
- What you observe vs. what the user told you

Replace `{{PLACEHOLDERS}}` in the template.

**Step 3 — Show the user the draft, do not commit.**
Read the draft, surface any sections you couldn't confidently fill in (mark them `TODO`), and ask the user to review before writing the final file.

## House format rules

- **Title:** `# <project-name> — Project Context` (em-dash, exactly this format)
- **Required sections (in order):** What It Is, What It Does, Project Layout, Build & Deploy
- **Optional sections (only if relevant):** Hardware, Key API Routes, Environment Variables, Known Issues, Important Files
- **Tone:** factual, declarative — not marketing speak. Write like a senior engineer documenting for the next engineer.
- **Code blocks:** real commands, not placeholders. If the setup deviates from defaults (e.g. a non-standard service user or ownership model), capture the deviation explicitly.
- **What to OMIT:** roadmap items, TODOs that belong in issue tracking, anything ephemeral.

## What CLAUDE.md is NOT

- Not a README (READMEs are for humans browsing GitHub; CLAUDE.md is for AI agents)
- Not a changelog (that lives in CHANGELOG.md or git)
- Not project plans (those live in a planning folder or issue tracker)

## Output

Confirm with: `Drafted CLAUDE.md for <project-name>. Sections I marked TODO: [list]. Ready for review.`

## Common mistakes

- Generic boilerplate that could apply to any project — kill it
- Listing every file in the tree — the layout section is for orientation, not exhaustive
- Hard-coded paths that aren't actually current — verify with `ls` before writing
- Forgetting the em-dash in the title
