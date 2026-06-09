---
name: handoff
description: Use when the user asks to "write a handoff", "close and write a handoff", "pause this work", "save state and clear", or wants a paste-ready next-session prompt before context fills — produces a structured handoff document so the next session can resume cold
---

# Session Handoff Generator

## What this does

Generates a paste-ready handoff document so the next Claude session can resume cold without 15 minutes of "what are we working on?" exploration. Uses `template.md` as the structure.

## When to use

- The user says: "write a handoff", "close and write a handoff", "pause this work", "save state and clear"
- Context is approaching limits and meaningful state needs to survive a `/clear` or new session
- A long-running task is being paused mid-way for the day

## When NOT to use

- For full session close-out — use `/wrap-up` (handoff is a subset of that)
- For trivial sessions with nothing in flight to hand off

## How to use

1. **Pick the destination:**
   - Project with a `STATE.md`? → update `STATE.md` instead
   - Using a planning-doc convention (e.g. a `.planning/` folder)? → `.planning/next-session-prompt.md`
   - Otherwise → project root as `HANDOFF-YYYY-MM-DD.md`

2. **Fill in the template** at `template.md` in this skill folder. Each section is required unless explicitly marked optional.

3. **Be ruthlessly specific.** Bad: "continue Phase 3 work." Good: "Phase 3 SwiftUI refactor — `ContentView.swift:42-95` needs the `@State` → `@Binding` swap; tests in `ContentViewTests.swift` are red on lines 18, 22, 31."

4. **Include exact paths, branch names, commit SHAs, and test command lines.** The next session won't have your context.

5. **Show the user the draft before writing** — handoffs are high-leverage; mistakes cost an hour next session.

## Quality bar — the handoff must answer

A cold-start agent must be able to answer these six questions using ONLY the handoff:

1. What were we trying to do?
2. What's done?
3. What's left?
4. What is the very next concrete action?
5. What are the prerequisite files to read first?
6. What is the scope guardrail — what is OUT of scope?

If any are missing, fix the handoff before considering it done.

## Common mistakes

- Vague verbs ("continue", "finish") instead of named tasks
- Missing the "scope guardrail" — leads to next session sprawling
- Forgetting uncommitted state — note any dirty files explicitly
- Not naming the branch — next session might `git checkout` the wrong thing
