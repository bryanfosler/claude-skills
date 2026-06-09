---
name: qa
description: Use when you want to verify what was just built before moving on or
  shipping. Invoke mid-session, at feature completion, or before wrap-up.
---

# QA Checkpoint

Run through these phases in order. Present a consolidated report at the end.

---

## Phase 1: What Changed

Run in every repo touched this session (or since the last `/qa` run):

```bash
git diff HEAD
git status
```

Summarize in plain language:
- Files modified and what they do
- What behavior was added, changed, or removed
- Anything that touches user-facing output, data, or controls

---

## Phase 2: Generate Test Checklist

Based on the actual diff — not boilerplate — generate a **specific** checklist
for what was just built. Tailor items to the change type:

**New UI control:** Does it appear correctly? Does it respond to input? Does state
save/restore?

**New integration / external call:** Does the correct message/output fire? Does it
handle edge or out-of-range values?

**Config or service change:** Did the service reload? Does the new config take
effect? Any silent failures?

**New endpoint or API call:** Does it return the expected shape? What happens
with missing or malformed params?

**Bug fix:** Is the exact bug scenario now fixed? Did the fix break adjacent
behavior?

**Refactor / rename:** Does everything that called the old thing still work?
Any broken imports or references?

Present as a numbered checklist the user can run through:

```
Test Checklist — [feature or change name]

1. [ ] <specific thing to verify>
2. [ ] <specific thing to verify>
3. [ ] <specific thing to verify>
```

Keep it to 3–6 items. If the change is tiny, 1–2 is fine.

---

## Phase 3: User Tests

Pause and wait for the user to run through the checklist and report back.

---

## Phase 4: Results

**All passing:**
Note what was verified and mark this as a clean QA pass. The user can move on or
invoke `/wrap-up`.

**Issues found:**
1. List the specific issues the user reported
2. Ask: "Want to work through these now?"
   - **Yes** → pivot back into build mode, fix the issues, then re-run from
     Phase 1
   - **No / defer** → note the known issues, flag them at wrap-up so they don't
     get silently committed
