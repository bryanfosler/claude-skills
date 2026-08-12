---
name: meeting-notes
description: Pull Microsoft Teams meeting transcripts from the past 10 business days, write VTT files to the Obsidian Meetings/Transcripts folder, and produce paired summary notes in Meetings/Notes. Idempotent — skips meetings already summarized. For recurring-URI bug (multiple segments), scores each segment against the target date and summarizes only the matching segment. Use `/meeting-notes` (default 10-business-day catchup) or `/meeting-notes today` (today only) or `/meeting-notes since 2026-05-01`.
---

# Meeting Notes Automation

You are running an automated transcript + summary pipeline for the user's Obsidian vault. Be efficient and quiet — this runs unattended via launchd. Final report should be terse.

The pipeline has three phases. **Phase 1** does all MCP calls in the main process and lands every transcript on local disk. **Phase 2** dispatches subagents that read local files — no MCP, no ToolSearch, no auth overhead. **Phase 3** commits and reports.

## Configure

```
OBSIDIAN_VAULT: ~/Documents/ObsidianVault    # vault ROOT (absolute path; may contain spaces — always quote)
```

Requires an authorized Microsoft 365 connector for calendar + transcript access. If `OBSIDIAN_VAULT` is unset or doesn't exist, STOP and tell the user — never write elsewhere.

## Vault paths

- Transcripts → `$OBSIDIAN_VAULT/Meetings/Transcripts/{YYYY-MM-DD}-{Slug}-Transcript.md`
- Notes → `$OBSIDIAN_VAULT/Meetings/Notes/{YYYY-MM-DD}-{Slug}.md`

The two files share `{YYYY-MM-DD}-{Slug}` so they cross-link cleanly.

## Slug rules

From the meeting subject:
1. Strip leading `<EXT>`, `Canceled:`, `Following:` prefixes.
2. Strip trailing `[In-person]` if present.
3. Replace non-alphanumeric chars with `-`.
4. Collapse runs of `-` into single `-`.
5. Trim leading/trailing `-`.
6. Date prefix from the event's UTC `start` field.

## Date window

- `/meeting-notes` with no args → last 10 business days.
- `/meeting-notes today` → today only.
- `/meeting-notes since YYYY-MM-DD` → from that date through now.

## Interactive mode: a single meeting (e.g. a pasted Teams recap link)

When invoked with a Teams recap/meeting URL or a single named meeting instead of a date window, this is an interactive one-off, not the unattended catchup — produce just that one note. Two gotchas, both seen with ad-hoc 1:1 ("OneOnOneChat") calls:

- **No calendar event.** Ad-hoc calls placed directly (not scheduled) have no Outlook event, so there's no `meetingTranscriptUrl` to read. `outlook_calendar_search` will come up empty — don't burn many tries on it.
- **The recap link's `driveItemId` points at the recording MP4, not the transcript.** Reading that file fails with `file_size_exceeded` (recordings routinely exceed the 100 MB connector cap). Teams does **not** store an ad-hoc call's transcript as a sibling `.vtt` you can fetch.

So the reliable path for a recap link is: resolve the `driveId`/`driveItemId` (or `sharepoint_folder_search` for the `Recordings` folder) just far enough to confirm which meeting it is, then **invoke the `stream-transcript` skill** — it pulls a speaker-labeled VTT out of the SharePoint/Stream player in Chrome via in-page `fetch()`, no manual export and no size limit. Only fall back to asking the user to export from the Teams recap (Transcript tab → ⋯ → Download .vtt/.docx) if that skill can't reach the recording. Once you have the VTT on disk, summarize from it directly (it's a single segment — no recurring-URI scoring needed) and write the paired transcript + note with the normal templates. Note in the transcript file's blockquote where the VTT came from and whether speakers are labeled.

## Idempotency

For each candidate meeting, build the target Notes/ path first. If it already exists, **skip entirely** — don't re-fetch the transcript, don't overwrite. This makes daily runs cheap on the gap-fill side.

## Filtering — skip these

- `isCancelled: true`
- Subject contains `[In-person]` (no Teams transcript will exist — unless the user later drops a VTT in manually)
- Subject equals or contains: `Focus time`, `Pub run`, `Crowne Plaza`, `check in`, `Save the date`, `OOO`, `Out of Office`
- All-day events (`isAllDay: true`) that look like markers rather than real meetings
- **Calendar-template / cadence blocks**: events with `attendees: null` AND `location: null` (e.g. the user's own "PM Cadence"-categorized recurring blocks like "Product Team Sync", "Cross-functional Stakeholder Sync", "HW/ID CAD Review", "1:1s with key leads"). These are planning placeholders, not real Teams meetings — they never have a transcript. Skip in Step 1.1 without fetching event details (saves token-heavy `read_resource` calls).

---

## Phase 1: Fetch (main process — all MCP calls)

All MCP interaction happens here. No subagents. Every transcript lands on local disk before Phase 2 begins.

### Step 1.1: Calendar query

1. Compute the date window from args.
2. Call `outlook_calendar_search` for all events in the window.
3. Apply filtering rules. Compute slugs for surviving meetings.
4. Check idempotency: if `Meetings/Notes/{YYYY-MM-DD}-{Slug}.md` exists, skip.
5. Result: a candidate list with subject, date, slug, and event URI.

### Step 1.2: Fetch event details (batches of 8)

1. For each candidate, call `read_resource` with the calendar event URI.
2. Extract `meetingTranscriptUrl`, `start`, `end`, attendees.
3. If `meetingTranscriptUrl` is null/missing → mark `skip:no-transcript`.
4. If error (403, etc.) → mark `skip:{reason}`.
5. Batch size: **8 parallel calls** (event detail responses are small).

### Availability gate (after Step 1.2, before Step 1.3)

Report transcript availability up front, then decide whether to continue:

1. Print one line, first thing in the final-report buffer:
   `AVAILABILITY: {A} of {C} candidates have transcripts ({K} no-transcript, {E} error, {X} already-exist)`
2. **If A == 0, stop here.** Skip Step 1.3 and Phase 2 entirely. Emit the per-meeting skip lines and the availability line as the final report. This is the most common outcome of a scheduled run — empty runs must be cheap and must read as "nothing available," not as failure.
3. If A > 0, continue to Step 1.3 with only the A available meetings.

### Step 1.3: Fetch transcripts (batches of 8)

1. For all meetings with transcript URLs, call `read_resource` with the transcript URL.
2. Large responses auto-save to tool-results files. **Record each file path** — this is the handoff to subagents.
3. If error (NOT_FOUND, 403, etc.) → mark `skip:{reason}`. Don't retry **within the run**.
   - **403 `GraphAccessToTranscriptsDisabled` (tenant-wide since ~2026-07-30):** this is not a per-meeting failure and not a dead end. Probe with **one** fetch; if it 403s, stop calling Graph for transcripts this run and use the **`stream-transcript` skill** instead — it pulls a speaker-labeled VTT from the SharePoint/Stream player in Chrome. That path needs a `stream.aspx` URL per meeting and drives a browser, so it does not batch: use it for interactive single-meeting runs, and for unattended catchup runs report the 403 and stop rather than trying to browse N recordings.
   - **Finalization lag (same-day runs):** a `transcripts_empty` (or suspiciously short) result for a meeting that **ended within the last hour or so** usually means Teams hasn't finished finalizing the transcript yet — not that none exists. Report it as `skip:not-finalized-yet (retry later)`, not a permanent no-transcript, and surface it so the user knows to re-run or hand over a manual VTT export. (Seen 2026-06-17: a post-meeting pull returned ~half the content vs the manual export. See `reference_transcript_finalization_lag`.)
4. Batch size: **8 parallel calls**.
5. After each batch, note the status: `{meeting}: {file_path}, {N} segments, {size}`.

**Critical**: After the MCP call, when Claude Code reports `Full output saved to: /path/to/file`, record that path. If the response is inline (small transcript), record "inline" and hold the content in context.

### Phase 1 output

A manifest of meetings ready for Phase 2, each with:
- Subject, date, start/end, slug, attendees
- Transcript source: file path or "inline" with content
- Number of segments (count `transcripts[]` entries from the JSON)
- Skip reason (if applicable)

---

## Phase 2: Analyze + Write

### Dispatch strategy

- **Inline processing** (main process): single-segment transcripts where the VTT content is <25K chars. Write both files directly — no subagent needed.
- **Subagent processing**: everything else (multi-segment, or single-segment ≥25K). Launch up to **8 subagents in parallel**.

### Subagent briefing

Each subagent receives (via its prompt):

1. Meeting metadata: subject, date, start/end time, slug, attendees
2. Transcript source path (tool-results file) or inline content
3. Number of segments
4. Output file paths for transcript and notes
5. The segment analysis algorithm (below)
6. The file templates (below)

**Subagent tools needed**: Read, Write, Bash. **NOT needed**: MCP tools, ToolSearch. All transcript data is already on disk.

### Segment analysis algorithm

The MCP response JSON contains `meeting.startDateTime` (often wrong for recurring meetings) and a `transcripts[]` array. Each entry has an `id` and `content` (a complete WEBVTT block from one meeting instance).

**Single segment** (`transcripts` has 1 entry):
- Compare `meeting.startDateTime` with the calendar event date.
- If within 7 days: `target-segment: 0`, no warning.
- If >7 days off: `target-segment: 0`, `date_warning = true`. Scan first ~30 cues for content clues to describe the mismatch.

**Multi-segment** (`transcripts` has >1 entry):
This is the recurring-URI bug — Graph returned content from multiple series instances.

1. For each segment, extract the first ~40 VTT cues (speaker text only — strip timing and `<v>` tags).
2. Search for temporal indicators:
   - **Explicit dates**: "May 20th", "the 14th", "5/20", "twentieth"
   - **Day-of-week references**: "last Monday", "yesterday", "this Friday"
   - **Relative time**: "last week", "two weeks ago", "next Friday"
   - **Event anchors**: "summit last week", "Giro in progress", "after the holiday", "spring classics"
   - **Project milestones**: specific decisions, deadlines, or deliverable names that can be cross-referenced
3. For each indicator, compute what date it implies relative to the segment's context.
4. Score each segment against the **target calendar date**:
   - `match` — at least one indicator directly confirms the target date (within 3 days)
   - `likely` — indicators are consistent but not conclusive
   - `mismatch` — at least one indicator contradicts the target date by >7 days
   - `unknown` — no temporal indicators found in first 40 cues
5. Select the target segment:
   - Priority: `match` > `likely` > `unknown` > `mismatch`
   - Tie-break: prefer the segment with more VTT cues (longer = more likely the complete instance)
   - If all segments score `unknown`: use segment 0 as default
6. Always set `date_warning = true` for multi-segment transcripts.
7. Record: `target_segment` index, `total_segments` count, scores list, and a brief `date_observation` describing the evidence.

### Transcript file template

```markdown
---
date: YYYY-MM-DD
meeting: {original subject}
summary: "[[YYYY-MM-DD-Slug]]"
type: transcript
total-segments: {N}
target-segment: {X}
{if N > 1:} segment-scores: [{score0}, {score1}, ...]
{if date_warning:} content-date-warning: "{observation}. See [[reference_mcp_recurring_transcript_bug]]."
---

# {original subject} — Raw Transcript

> Auto-pulled from Teams via Microsoft Graph API (`/meeting-notes` skill run).
{if N > 1:}
> Recurring-series URI returned {N} segments. **Segment {X}** identified as the {YYYY-MM-DD} instance ({brief evidence}).

```vtt
{if N == 1:}
{full VTT content}
{if N > 1:}
=== Segment 0 (of {N}){if X == 0: ← TARGET} ===
{VTT content for segment 0}

=== Segment 1 (of {N}){if X == 1: ← TARGET} ===
{VTT content for segment 1}

... (continue for all segments)
```
```

### Notes file template

```markdown
---
date: YYYY-MM-DD
meeting: {original subject}
transcript: "[[YYYY-MM-DD-Slug-Transcript]]"
attendees: [list of names from speakers + calendar attendees]
type: meeting-note
{if N > 1:} target-segment: {X}
{if N > 1:} total-segments: {N}
{if date_warning:} content-date-warning: true
---

# YYYY-MM-DD — {original subject}

**Date:** YYYY-MM-DD HH:MM–HH:MM {timezone}
**Attendees:** [comma list]
**Transcript:** [[YYYY-MM-DD-Slug-Transcript]]

## Summary

{if date_warning:}
> ⚠️ **Date warning:** {description of mismatch — e.g., "The Microsoft Graph API returned startDateTime of 2024-04-23 for this recurring meeting. Segment {X} of {N} was identified as the {date} instance based on {evidence}. Summary is based on segment {X} only."}

{2–4 paragraph summary — based on TARGET SEGMENT ONLY, never mix content from other segments}

## Decisions
- {decision 1}
- {decision 2}

## Action items
- [ ] **{owner}** — {action} (by {date if mentioned})

## Open questions
- {question raised but not resolved}
```

**Important**: When a target segment has been identified in a multi-segment transcript, summarize ONLY that segment. Content from other segments is from different meeting instances and would produce inaccurate notes.

---

## Phase 3: Bookkeeping

### Git commit

After all writes are done:
```bash
cd $OBSIDIAN_VAULT
git add Meetings/Transcripts/ Meetings/Notes/
git commit -m "meeting-notes: auto-pull $(date +%Y-%m-%d-%H%M)" || true
```

(Don't push — the daily 22:00 `obsidian-git-backup` job handles that.)

### Final report

Terse single-line per meeting:
```
[✓ saved | ⚠ saved+warning | ✗ skip:reason | ⊘ already-exists] {date} — {subject}
```
For ⚠ lines, append: `(segment {X}/{N}, {score})`

Plus a one-line summary count: `N new, M with warnings, K skipped, J already existed`.

Lead the report with the `AVAILABILITY:` line from Phase 1 so empty runs read as "nothing available" rather than failure.

---

## Parallelism summary

| Phase | What | Batch size | Who |
|-------|------|-----------|-----|
| 1.2 | Event details (MCP) | 8 | Main process |
| 1.3 | Transcript fetch (MCP) | 8 | Main process |
| 2 | Analyze + write | 8 subagents | Subagents (local I/O only) |

Don't dump VTT bodies into status updates — they're huge and the launchd log will fill up.

## Cost discipline

- Skip meetings already in Notes/ before doing any MCP calls (Phase 1 idempotency).
- Don't summarize transcripts that returned an error or were skipped.
- One pass per meeting — no retries in the same run.
- **Subagents must never call MCP tools.** All transcript data is on disk from Phase 1.
- For inline processing (small single-segment), summarize directly from the fetched content — don't re-read.
