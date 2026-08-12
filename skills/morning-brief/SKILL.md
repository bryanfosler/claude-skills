---
name: morning-brief
description: Generate a daily morning brief — pull today's Microsoft 365 calendar, filter to real meetings, and write a prep-focused brief to the Obsidian vault (Sessions/Briefings/latest-morning-brief.md + a dated archive). Runs unattended via launchd before the workday; also runnable manually with /morning-brief. Idempotent — a fresh brief for today is left alone.
---

# Morning Brief

You are generating the user's daily morning brief, unattended via launchd (early AM, weekdays) or on demand. Be efficient and quiet — terse final report. All MCP calls happen in the main process; this skill is small enough that no subagents are needed.

Purpose: when the user opens `Dashboard - Focus` in the morning, the brief gives them today's meetings with enough context to walk in prepared. Tasks already live on the dashboard — the brief's unique value is **today's calendar + per-meeting prep**.

## Configure

```
OBSIDIAN_VAULT: ~/Documents/ObsidianVault    # vault ROOT (absolute path; may contain spaces — always quote)
```

Requires an authorized Microsoft 365 connector for calendar access. If `OBSIDIAN_VAULT` is unset or doesn't exist, STOP and tell the user — never write elsewhere.

## Output files

- Canonical (embedded by the dashboard): `$OBSIDIAN_VAULT/Sessions/Briefings/latest-morning-brief.md` — overwrite each run.
- Dated archive: `$OBSIDIAN_VAULT/Sessions/Briefings/{YYYY-MM-DD}-morning.md` — one per day.

Both share identical content. The dashboard embeds the canonical file's `## 🗓️ Today's calendar` heading, so **that heading text must be exact** (emoji included) or the embed renders empty.

## Idempotency

If the dated archive for today already exists AND its `date:` matches today, **skip entirely** (a brief was already generated). This makes the morning + any re-runs cheap. Manual `/morning-brief force` regenerates anyway.

## Phase 1: Pull today's calendar (main process, MCP)

1. Compute today's local date (Central — Madison, WI).
2. `outlook_calendar_search` for events with start within today (local 00:00–23:59).
3. Filter out, same rules as `/meeting-notes`:
   - `isCancelled: true`
   - Subject contains `[In-person]`, or `Focus time`, `Pub run`, `check in`, `Save the date`, `OOO`, `Out of Office`
   - All-day marker events (`isAllDay: true`) that aren't real meetings
   - **Cadence/template blocks**: `attendees: null` AND `location: null` (the user's own recurring cadence placeholders) — skip without fetching details.
4. For surviving events, `read_resource` the event URI (batch up to 8) to get start/end, attendees, location, and body/preview.

## Phase 2: Write the brief

For each surviving meeting, write a block: time range, title, attendees, location, and a **one-line prep note**. Keep prep light and grounded — derive it from the meeting subject, body, and any obvious context you already hold (recent meeting notes, known projects). **Do not** launch deep research per meeting; this runs daily and must stay cheap. If a meeting clearly maps to a known project/person, a single pointed sentence ("pull your LRPM COGS file — Athul's framing is GP gaps") beats a paragraph.

Sort meetings chronologically. If there are no real meetings today, say so in one line (still write the file, still with the exact calendar heading).

### File template

```markdown
---
date: {YYYY-MM-DD}
type: morning-brief
generated: {YYYY-MM-DD HH:MM} CT
---

# Morning Brief — {Weekday, Month D, YYYY}

## 🗓️ Today's calendar

{for each meeting:}
**{H:MM}–{H:MM} {AM/PM}** · {title}
- Attendees: {comma list}
- Location: {location}
- prep: {one grounded line}

{if none:}
No scheduled Teams/calendar meetings today. Clear runway — protect a deep-work block.
```

(Keep the brief to today's calendar for v1. Weather / overnight-context sections can be added later; don't invent data you can't source.)

## Phase 3: Bookkeeping

Write both files (overwrite canonical, create/overwrite dated archive), then commit:

```bash
cd $OBSIDIAN_VAULT
git add Sessions/Briefings/
git commit -m "morning-brief: $(date +%Y-%m-%d)" || true
```

Don't push — the 22:00 `obsidian-git-backup` job handles that.

## Final report

Terse: `brief written — {N} meetings` or `brief written — no meetings today` or `skipped — today's brief already exists`.

## Cost discipline

- Skip the whole run if today's brief already exists (Phase 1 idempotency, before any MCP call beyond the existence check).
- One `read_resource` per surviving meeting; batch in 8s; no retries within a run.
- No per-meeting deep research. The brief is a launch pad, not a dossier.
- Empty-calendar days must be cheap.
