---
name: portfolio-check
description: Scan a Smartsheet program bowler (read-only) for programs that are drifting, stalling, blocked, past-due, or marked Green-but-overdue. Writes an exception-only brief to the Obsidian vault (Sessions/Portfolio-Check/) and a machine-readable snapshot. Runnable on demand with /portfolio-check or unattended via launchd on a weekly schedule. Read-only on Smartsheet — never edits a sheet, sends a message, or changes a plan.
---

# Portfolio Check

Answers one question on a weekly cadence: **which of my programs need attention this week, and why?** Exception-only — healthy programs produce one summary line, not a report.

It is **read-only** on Smartsheet and writes **only** to the vault. It never edits a sheet, sends a message, creates a ticket, or changes a plan. Owner-nudges and escalations are drafted in the brief for the user to send manually.

---

## Configure

```
OBSIDIAN_VAULT: ~/Documents/ObsidianVault        # vault ROOT (absolute path; may contain spaces — always quote)
PORTFOLIO_CHECK_DIR: ~/Projects/portfolio-check  # where portfolio_check.py lives
BOWLER_SHEET_ID: <smartsheet-sheet-id>           # the program bowler to scan
KEYCHAIN_ITEM: smartsheet-api                    # macOS Keychain generic-password item holding the API token
```

**First-time setup** — store your own Smartsheet API token in the Keychain (the skill never reads a token from code or the vault):

```bash
security add-generic-password -a "$USER" -s smartsheet-api -w
```

Generate the token in Smartsheet under *Account → Personal Settings → API Access*. If `KEYCHAIN_ITEM` is missing, STOP and tell the user to run the command above — never prompt for a token in chat or write one to disk.

---

## How it works

All logic lives in `$PORTFOLIO_CHECK_DIR/portfolio_check.py` (pure Python, stdlib only). This skill is a thin wrapper: run it, commit the vault output, report terse.

The script:
1. Reads `$BOWLER_SHEET_ID` via the Smartsheet API. Token comes from macOS Keychain (`$KEYCHAIN_ITEM`) — never stored in code or the vault.
2. Normalizes rows into programs → open milestones, skipping completed items and OOO/Travel admin sections.
3. Runs detection rules, tagging every claim **FACT / INFERENCE / HYPOTHESIS** with a source row:
   - **past_due** (FACT) — End Date in the past, still open
   - **blocked** (FACT) — Status = Blocked
   - **no_owner** (FACT) — no owner, but only when due ≤60d, On Fire, or Health=Red
   - **stale_near_gate** (INFERENCE) — no dated Progress Update note in ≥10 business days while a gate is <30d out (uses the Progress Update log date, NOT the cell-modified date, which resets every week)
   - **slipped_vs_baseline** (INFERENCE) — "Later than LC" non-zero
   - **contradiction** (HYPOTHESIS) — Health=Green but shows trouble above; surfaced, never resolved
4. Writes:
   - `Sessions/Portfolio-Check/latest-portfolio-check.md` (overwrite) + `{date}-portfolio-check.md` (archive)
   - `out/project-snapshot.json` (feeds downstream Weekly Brief / Gate Radar pilots)

## Run

```bash
cd $PORTFOLIO_CHECK_DIR && python3 portfolio_check.py
```

Then commit the vault output (local only — never push; the nightly backup job pushes):

```bash
cd $OBSIDIAN_VAULT && git add Sessions/Portfolio-Check/ && git commit -m "portfolio-check: $(date +%Y-%m-%d)" || true
```

## Final report

Terse. Echo the script's summary line and the headline (the programs flagged + why), then point to the vault file. Example:

`4 flagged across 2 programs — Program A (past-due), Program B (on-fire/no-owner). Brief: Sessions/Portfolio-Check/latest-portfolio-check.md`

Do not paste the whole brief into chat unless asked — it's in the vault.

## Boundaries (hard)

- Read-only on Smartsheet and any other source. No writes back to any sheet.
- Writes only to the vault and `out/`. No messages sent, no tickets created, no plans changed.
- If the sheet structure has changed and parsing looks wrong (e.g. 0 programs, or every item flagged), STOP and report the anomaly rather than emitting a misleading brief.

## Notes / future

- Source is a single cross-program bowler sheet (breadth over depth). A per-program gantt with Baseline/Variance columns is a better source for a Gate Readiness Radar — keep that as a separate skill rather than widening this one.
- Notification channel (native push vs. Teams/email to self) is deliberately deferred until output quality is trusted. v1 = vault brief, on demand or scheduled.
- Tuning constants at the top of the script: `STALE_BIZ_DAYS`, `NEAR_GATE_DAYS`, `EXCLUDE_PROGRAM`.
