---
name: portfolio-check
description: Scan a Smartsheet program bowler (read-only) for programs that are drifting, stalling, blocked, past-due, or marked Green-but-overdue. Writes an exception-only brief to the Obsidian vault (Sessions/Portfolio-Check/) and a machine-readable snapshot. Runnable on demand with /portfolio-check or unattended via launchd on a weekly schedule. Read-only on Smartsheet — never edits a sheet, sends a message, or changes a plan.
---

# Portfolio Check

Answers one question on a weekly cadence: **which of my programs need attention this week, and why?** Exception-only — healthy programs produce one summary line, not a report.

It is **read-only** on Smartsheet and writes **only** to the vault. It never edits a sheet, sends a message, creates a ticket, or changes a plan. Owner-nudges and escalations are drafted in the brief for the user to send manually.

---

## Configure

Everything is driven by environment variables — nothing is hardcoded:

```
BOWLER_SHEET_ID                   # the Smartsheet program bowler to scan (required)
PORTFOLIO_CHECK_VAULT_DIR         # where the brief is written
                                  #   default ~/Documents/ObsidianVault/Sessions/Portfolio-Check
PORTFOLIO_CHECK_KEYCHAIN_ITEM     # Keychain item holding the API token (default: smartsheet-api)
```

**First-time setup** — store your own Smartsheet API token in the Keychain. The skill never reads a token from code, the vault, or chat:

```bash
security add-generic-password -a "$USER" -s smartsheet-api -w
```

Generate the token in Smartsheet under *Account → Personal Settings → API Access*.

Don't know the sheet id? List everything the token can see:

```bash
python3 bin/smartsheet_list.py
```

If the Keychain item is missing, the script fails on the `security` call — STOP and tell the user to run the `add-generic-password` command above. Never prompt for a token in chat or write one to disk.

---

## How it works

Self-contained: all logic lives in `bin/` inside this skill directory (pure Python, stdlib only — no venv, no pip install). This skill is a thin wrapper: run it, commit the vault output, report terse.

```
bin/portfolio_check.py    the scan (the one you run)
bin/smartsheet_list.py    list sheets the token can see — use this to find BOWLER_SHEET_ID
bin/smartsheet_meta.py    dump a sheet's column metadata (for adapting the detection rules)
bin/smartsheet_dump.py    dump raw rows (for debugging a parse that looks wrong)
```

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
python3 bin/portfolio_check.py
```

Then commit the vault output, if the vault is a git repo:

```bash
git -C "$OBSIDIAN_VAULT" add Sessions/Portfolio-Check/ && git -C "$OBSIDIAN_VAULT" commit -m "portfolio-check: $(date +%Y-%m-%d)" || true
```

**Adapting it to a different bowler.** The detection rules read specific column names (Status, Health, End Date, Owner, Progress Update, "Later than LC"). If your sheet names them differently, run `bin/smartsheet_meta.py <sheet_id>` to see the real columns and adjust the parser. Do this before trusting the first run — a rule that silently matches nothing looks identical to a healthy portfolio.

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
