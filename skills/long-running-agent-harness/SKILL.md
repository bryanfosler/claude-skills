---
name: long-running-agent-harness
description: >
  Design and operate long-running AI agent workflows that span multiple context windows,
  hours, or days. Use when building or orchestrating autonomous agents that lose continuity
  between sessions, redo completed work, declare victory too early, leave code in a broken
  or undocumented state between sessions, or regress multi-session progress. Apply this skill
  when work needs durable handoff artifacts, a strict per-session startup protocol, exhaustive
  feature tracking, and reliable incremental progress across repeated agent sessions.
---

# Long-Running Agent Harness

Treat long-running agent work like shift handoff engineering. Assume every new session starts with no memory. Make continuity a property of the harness and its artifacts, not a property of the model.

Use this skill together with `$harness-engineering` when the repo also needs agent-facing architecture docs, CI checks, or broader coding guardrails.

## Scope

Use this pattern when:
- Tasks span multiple context windows, hours, or days
- Agents forget prior progress and redo work
- Agents mark work done before end-to-end verification
- Sessions leave the repo in a broken or undocumented state
- You need reliable autonomous progress across repeated sessions

Do not use this pattern when:
- The task comfortably fits in one session
- You only need repo structure, AGENTS.md, and CI feedback loops without long-lived session handoff problems

## Use Two Roles

Split the work into two specialized roles instead of asking one agent to finish the whole project in a single pass.

### 1. Run an Initializer Agent Once

Have the initializer establish the working environment and produce the continuity artifacts:
- Create `init.sh`
- Create `claude-progress.txt`
- Create `feature_list.json`
- Make the initial baseline commit

Use this role only in the first session or when bootstrapping an existing repo that lacks these artifacts.

### 2. Run a Coding Agent for Every Later Session

Have each coding session follow the same startup sequence:
- Read the handoff artifacts
- Select the authoritative execution worktree
- Start the environment with `init.sh`
- Verify the current state before writing new code
- Pick one incomplete feature
- Implement, test, commit, and update the progress log

Do not let the coding agent "one-shot" the full roadmap. That is the main path to partial work, context exhaustion, and broken handoffs.

## Treat Worktrees as Disposable Execution Surfaces

If you use git worktrees, treat them as isolation mechanics, not as continuity artifacts.

Continuity must live in:
- `claude-progress.txt`
- `feature_list.json`
- descriptive commits

Continuity must not live in:
- a dirty root worktree
- abandoned `agent-*` worktrees
- uncommitted changes that exist only in one forgotten checkout

Rules:
- Keep exactly one authoritative coding worktree for the active long-running task
- If the root worktree is already dirty or used for unrelated work, create a dedicated isolated worktree for the task
- Use the same authoritative worktree across later sessions until its work is merged or intentionally abandoned
- Remove stale worktrees once they no longer carry unique value
- Delete stale worktree branches after removing their worktrees
- Never commit worktree directories such as `.claude/worktrees/*` into the repository
- Add local ignore or exclude rules when needed so worktree directories do not pollute `git status`

If multiple worktrees exist, a session must explicitly decide which one is authoritative before doing any implementation.

## Create Three Continuity Artifacts

### `feature_list.json`

Use JSON rather than Markdown. JSON is harder to casually rewrite in ways that erase testing intent or progress detail.

Keep the list exhaustive:
- For complex apps, expect hundreds of testable entries
- Write concrete user-observable behaviors, not vague milestones
- List verification steps that a later session can repeat
- Start every `passes` field as `false`
- Flip `passes` to `true` only after end-to-end verification
- Never delete or weaken items to make the project look closer to complete

If the roadmap is intentionally phase-gated rather than feature-gated, prefer a hierarchical ledger instead of a flat phase list. In that case:
- Create one `type: "phase"` gate entry per execution-plan phase
- Under each phase, create ordered child entries such as `P-03-01`, `P-03-02`, and a terminal `P-03-99`
- Link child entries with `parentId`
- Use `type: "subtask"` for bounded implementation items and `type: "verification"` for the phase closeout check
- Add enough detail inside each child entry that a fresh session can resume without guessing
- Include at least:
  - ordered `steps`
  - repeatable `verification`
  - optional `scopeGuardrails` when the phase boundary is easy to cross
  - optional `currentEvidence` or `statusBasis` explaining why the item is still open or already passed
- Preserve the one-phase-at-a-time discipline in the session prompt:
  - select the earliest incomplete `phase`
  - then select the earliest incomplete child under that phase
  - mark the parent `phase` as passed only after all of its child entries are passed
- Do not use bare phase titles like "Phase 3: Slim UI" with only 2-3 generic steps; that is too coarse for handoff

Example:

```json
[
  {
    "category": "functional",
    "description": "New chat button creates a fresh conversation",
    "steps": [
      "Navigate to the main interface",
      "Click the New Chat button",
      "Verify a new conversation is created",
      "Check that the chat area shows the welcome state",
      "Verify the conversation appears in the sidebar"
    ],
    "passes": false
  }
]
```

Phase-gated example:

```json
[
  {
    "id": "P-03",
    "type": "phase",
    "category": "phase",
    "description": "Phase 3: Slim components and commands while preserving the reduced shell surface",
    "goal": "Finish the shell command/component reduction without drifting into service cleanup.",
    "completionRule": "Mark this phase passed only after every child item with parentId=P-03 is passed.",
    "passes": false
  },
  {
    "id": "P-03-01",
    "type": "subtask",
    "parentId": "P-03",
    "description": "Delete cut command directories and shrink the kept command surface",
    "steps": [
      "Delete cut command directories",
      "Shrink the command registry to the kept commands"
    ],
    "verification": [
      "List the remaining commands and confirm only the keep list remains"
    ],
    "passes": false
  },
  {
    "id": "P-03-02",
    "type": "subtask",
    "parentId": "P-03",
    "description": "Delete cut component files and repair shell-local imports",
    "steps": [
      "Delete cut component files and directories",
      "Repair remaining shell imports caused by those deletions"
    ],
    "verification": [
      "Run typecheck and confirm the remaining shell errors are not still caused by deleted Phase 3 surface"
    ],
    "scopeGuardrails": [
      "Do not start deleting services or hooks in this phase"
    ],
    "passes": false
  },
  {
    "id": "P-03-99",
    "type": "verification",
    "parentId": "P-03",
    "description": "Phase 3 closeout verification",
    "steps": [
      "Smoke test the kept slash commands",
      "Confirm removed command surfaces are absent or fail gracefully"
    ],
    "verification": [
      "Mark P-03 passed only after the earlier P-03 children are already passed"
    ],
    "passes": false
  }
]
```

### `claude-progress.txt`

Use an append-only running log. Read it first at session start. Write to it last at session end.

Record:
- What changed in the session
- What was verified
- What remains next
- Known issues, blind spots, or blockers
- Anything a new session must know before touching the code

Example:

```text
## Session 2025-11-25T14:30
- Implemented user authentication login and logout
- Fixed sidebar rendering bug
- Verified login flow in the browser
- Next priority: chat message persistence
- Known issue: browser-native alert modals are not detectable via current automation

## Session 2025-11-25T10:00
- Set up project scaffolding
- Created init.sh for dev server startup
- Generated feature list with 215 entries
- Created baseline commit before iterative feature work
```

### `init.sh`

Use a single reproducible startup script for every later session. Make it idempotent when possible.

The script should:
- Change into the correct working directory
- Install dependencies when needed
- Start the required services
- Print the expected local URL or endpoint

Example:

```bash
#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
npm install
npm run dev &
echo "Dev server started on http://localhost:3000"
```

## Follow This Session Protocol

Run this sequence at the start of every coding session before attempting new work:

1. `pwd` to confirm the working directory
2. Run `git worktree list --porcelain` and identify the single authoritative worktree for the task
3. Read `claude-progress.txt` to understand the recent history
4. Read `feature_list.json` to identify incomplete features
5. Run `git log --oneline -20` to inspect recent commits
6. Run `init.sh` to start the environment
7. Verify basic functionality to ensure the baseline is not already broken
8. Select the highest-priority incomplete feature
   If the ledger is phase-gated, select the earliest incomplete child under the earliest incomplete phase
9. Implement and test that single feature or child item
10. Commit the result and append the session summary to `claude-progress.txt`

Do not skip steps 1 through 7. Verification happens before new work, not after the repo has already drifted further.

If the root worktree is dirty and that dirt is unrelated to the active task, do not use it for baseline verification. Switch to or create the authoritative isolated worktree first.

## Prevent Premature Completion

The most common failure mode is early, incorrect completion. Prevent it structurally instead of hoping the agent self-corrects.

| Cause | Structural prevention |
|---|---|
| Agent tries to build everything at once | Keep an exhaustive ledger and enforce one bounded item per session |
| Agent marks work done without testing | Flip `passes` only after end-to-end verification |
| Later sessions assume partial work is complete | Record known issues and unverified areas in `claude-progress.txt` |
| Tests get edited or removed to avoid failures | Enforce an explicit rule to never remove or weaken existing tests |
| Context window ends mid-feature | Keep the work scope narrow and commit cleanly at session end |
| Sessions fight over different worktrees | Enforce a single authoritative worktree and record it in the progress log |

## Use Git as a Recovery Mechanism

Treat git as both version control and session recovery infrastructure.

- End every session with a descriptive commit
- Update `claude-progress.txt` in the same session
- Create an initial baseline commit before iterative feature work starts
- Prefer one dedicated task worktree over repeated edits in a dirty shared root checkout
- Remove stale worktrees and their branches once they are superseded
- Use `git revert` when a feature breaks existing behavior and fast repair is riskier than backing out
- Do not stack new work on top of a broken baseline just to maintain momentum

Commit history gives later sessions a second source of truth when the progress log is incomplete.

## Prefer End-to-End Verification

Unit tests and HTTP checks are useful, but they do not prove that a user-facing flow works from start to finish.

Prefer verification that matches the product surface:
- For web apps, use browser automation
- For CLI tools, run the real command-line flows
- For APIs, drive realistic integration paths instead of isolated handlers
- For UI features, verify observable outcomes, not only internal state

Handle blind spots explicitly:
- Record any behavior that current automation cannot observe
- Leave reproduction steps for manual verification when needed
- Do not claim completion for behavior that was never actually exercised

Never remove or edit existing tests to make progress appear green. Fix the code or document the blocker.

## Diagnose Common Failures

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent redoes completed work | Progress file missing or unread at session start | Read and maintain `claude-progress.txt` as a mandatory first artifact |
| Agent declares the project done too early | Feature list is too short or too vague | Expand `feature_list.json` into concrete, testable behaviors |
| Features regress between sessions | New work starts before baseline verification | Enforce startup steps 5 and 6 every session |
| Agent edits or deletes tests | No explicit prohibition on test modification | Add and repeat the rule: never remove or weaken existing tests |
| Code is left broken between sessions | No clean commit or no shutdown ritual | Require commit plus progress-file update at session end |
| Setup consumes most of the session | No reproducible startup script | Create and maintain `init.sh` |

## Keep the Handoff Clean

Aim for the same session exit state every time:
- Code committed or intentionally reverted
- `claude-progress.txt` appended with what changed, what passed, and what remains
- `feature_list.json` updated only for features actually verified
- The authoritative worktree clearly identified, with stale worktrees removed or explicitly marked non-authoritative
- Clear next priority recorded for the next session

If the session ends in a broken state, document that state explicitly and explain the fastest safe recovery path.

## Quick Reference

Initializer agent:
- Create `init.sh`
- Create `claude-progress.txt`
- Create `feature_list.json`
- Create the baseline commit

Coding agent:
- Read progress file
- Read feature list
- Read recent git history
- Inspect worktrees and select one authority
- Run `init.sh`
- Verify baseline behavior
- Pick one incomplete feature, or the earliest incomplete child under the earliest incomplete phase
- Implement and test it
- Commit and update progress

Hard rules:
- Treat continuity as a harness problem
- Work on one feature per session
- Use one authoritative worktree per active task
- Never let worktree directories become tracked repo content
- Never remove or weaken existing tests
- Mark features passed only after end-to-end verification

## References

- Anthropic Engineering, "Effective Harnesses for Long-Running Agents": https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Complementary skill: `$harness-engineering`
