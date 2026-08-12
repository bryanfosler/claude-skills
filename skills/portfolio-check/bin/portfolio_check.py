#!/usr/bin/env python3
"""portfolio-check: read-only scan of a Smartsheet program bowler.
Builds a normalized snapshot, runs stall/drift detection, emits exception-only
findings. Every claim is tagged FACT / INFERENCE / HYPOTHESIS with a source row.
NEVER writes to Smartsheet. Token from Keychain.

Setup (once):
    security add-generic-password -a "$USER" -s smartsheet-api -w
    export BOWLER_SHEET_ID=<your sheet id>      # or pass it as argv[1]
    export PORTFOLIO_CHECK_VAULT_DIR=<path>     # where the brief is written

Usage: python3 portfolio_check.py [sheet_id]
"""
import json, subprocess, urllib.request, os, sys, re
from datetime import datetime, date, timezone

MONDAY_SHEET = os.environ.get("BOWLER_SHEET_ID", "")   # the program bowler to scan
KEYCHAIN_ITEM = os.environ.get("PORTFOLIO_CHECK_KEYCHAIN_ITEM", "smartsheet-api")
# admin/non-work sections to skip (OOO, travel, etc.) — not real milestones
EXCLUDE_PROGRAM = re.compile(r"OOO|Travel|Vacation|Holiday", re.I)
STALE_BIZ_DAYS = 10                # no change in >= N business days ...
NEAR_GATE_DAYS = 30                # ... while a gate is < N days out
TODAY = date.today()

# ---------- API (read-only) ----------
def token():
    return subprocess.run(
        ["security", "find-generic-password", "-a", os.environ["USER"],
         "-s", KEYCHAIN_ITEM, "-w"],
        capture_output=True, text=True, check=True).stdout.strip()

def get(path, tok):
    req = urllib.request.Request("https://api.smartsheet.com/2.0" + path,
                                 headers={"Authorization": "Bearer " + tok})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

# ---------- helpers ----------
def biz_days_between(d1, d2):
    """business days from d1 to d2 (d2 >= d1); negative if d2 < d1."""
    if d2 < d1:
        return -biz_days_between(d2, d1)
    days, cur = 0, d1
    while cur < d2:
        cur = date.fromordinal(cur.toordinal() + 1)
        if cur.weekday() < 5:
            days += 1
    return days

def parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None

def parse_end_date(v):
    dt = parse_dt(v)
    return dt.date() if dt else None

LINE_DATE = re.compile(r"\b(\d{1,2})/(\d{1,2})\b")
def last_update_date(progress_text):
    """latest M/D mentioned in the Progress Update log -> a date (year inferred)."""
    if not progress_text:
        return None
    best = None
    for m, d in LINE_DATE.findall(progress_text):
        m, d = int(m), int(d)
        if not (1 <= m <= 12 and 1 <= d <= 31):
            continue
        # infer year: assume current year, but if that date is in the future, use last year
        for yr in (TODAY.year, TODAY.year - 1):
            try:
                cand = date(yr, m, d)
            except ValueError:
                continue
            if cand <= TODAY:
                if best is None or cand > best:
                    best = cand
                break
    return best

# ---------- load + normalize ----------
def load(sheet_id):
    s = get(f"/sheets/{sheet_id}", token())
    by_id = {c["id"]: c["title"] for c in s["columns"]}
    rows = []
    for r in s["rows"]:
        cells = {}
        for c in r.get("cells", []):
            t = by_id.get(c["columnId"])
            v = c.get("displayValue", c.get("value"))
            cells[t] = v
        rows.append({
            "rowNumber": r["rowNumber"],
            "id": r["id"],
            "parentId": r.get("parentId"),
            "modifiedAt": parse_dt(r.get("modifiedAt")),
            "cells": cells,
        })
    return s["name"], rows

def is_program(row):
    c = row["cells"]
    return (c.get("Working Tasks") == "Exclude") or \
           (c.get("Report Tag") in ("Tier 1", "Tier 2") and not c.get("Owner"))

def find_program(row, rowmap):
    """nearest ancestor that looks like a program; else the top ancestor."""
    seen, cur = set(), row
    last_prog = None
    while cur is not None and cur["id"] not in seen:
        seen.add(cur["id"])
        if cur is not row and is_program(cur):
            last_prog = cur
        cur = rowmap.get(cur.get("parentId"))
    return last_prog

# ---------- detection ----------
def analyze(rows):
    rowmap = {r["id"]: r for r in rows}
    snapshot = {}   # program name -> {milestones:[...]}
    findings = []

    for r in rows:
        c = r["cells"]
        task = (c.get("Task") or "").strip()
        if not task or is_program(r):
            continue
        status = c.get("Status")
        if status == "Complete":
            continue   # only open milestones

        prog_row = find_program(r, rowmap)
        prog = (prog_row["cells"].get("Task") if prog_row else None) or "(ungrouped)"
        prog = prog.strip().rstrip(":")
        if EXCLUDE_PROGRAM.search(prog):
            continue   # skip OOO/travel/admin sections

        end = parse_end_date(c.get("End Date"))
        is_gate = bool(re.search(r"\bMS\s*\d+\b", task, re.I))
        owner = c.get("Owner")
        health = c.get("Health")
        modified = r["modifiedAt"].date() if r["modifiedAt"] else None
        last_note = last_update_date(c.get("Progress Update"))
        # staleness: the dated Progress Update note is the real signal — the sheet's
        # cell-modified date resets every Monday (bulk review), so it's useless here.
        # Fall back to modifiedAt only when there's no dated note.
        stale_basis = last_note or modified
        days_to_end = (end - TODAY).days if end else None
        stale_biz = biz_days_between(stale_basis, TODAY) if stale_basis else None
        on_fire = c.get("Priority Level") == "On Fire!"

        flags = []
        def flag(kind, conf, msg, evidence):
            flags.append({"kind": kind, "confidence": conf, "msg": msg, "evidence": evidence})

        src = f"row {r['rowNumber']}"

        # --- rules ---
        if status == "Blocked":
            flag("blocked", "FACT", "Status = Blocked", f"{src}: Status")
        if not owner:
            # only flag missing owner when it actually matters soon, or it's hot
            near = days_to_end is not None and days_to_end <= 60
            if near or on_fire or health == "Red":
                why = ("due in %dd" % days_to_end) if near else \
                      ("On Fire" if on_fire else "Health=Red")
                flag("no_owner", "FACT",
                     f"No owner assigned on an open item ({why})", f"{src}: Owner empty")
        if end and days_to_end is not None and days_to_end < 0:
            flag("past_due", "FACT",
                 f"End Date {end} is {-days_to_end}d in the past, still open",
                 f"{src}: End Date / Status")
        later = c.get("Later than LC")
        if later and str(later).strip() not in ("0", "", "0d", "—"):
            flag("slipped_vs_baseline", "INFERENCE",
                 f"Later than baseline (LC): {later}", f"{src}: Later than LC")
        if (stale_biz is not None and stale_biz >= STALE_BIZ_DAYS
                and days_to_end is not None and 0 <= days_to_end < NEAR_GATE_DAYS):
            flag("stale_near_gate", "INFERENCE",
                 f"No update in ~{stale_biz} business days, gate due in {days_to_end}d",
                 f"{src}: last note {stale_basis}")
        # contradiction: Green but evidence of trouble
        trouble = [f for f in flags if f["kind"] in
                   ("blocked", "past_due", "stale_near_gate", "slipped_vs_baseline")]
        if health == "Green" and trouble:
            why = ", ".join(sorted({f["kind"] for f in trouble}))
            flag("contradiction", "HYPOTHESIS",
                 f"Marked Health=Green but shows: {why}",
                 f"{src}: Health vs evidence")

        rec = {
            "program": prog, "task": task, "row": r["rowNumber"],
            "is_gate": is_gate, "status": status, "owner": owner,
            "health": health, "end_date": str(end) if end else None,
            "days_to_end": days_to_end, "last_note": str(stale_basis) if stale_basis else None,
            "stale_biz_days": stale_biz, "on_fire": on_fire,
            "flags": flags,
        }
        snapshot.setdefault(prog, []).append(rec)
        if flags:
            findings.append(rec)

    return snapshot, findings

# ---------- output ----------
SEV = {"On Fire!": 0}
def rank_key(rec):
    kinds = {f["kind"] for f in rec["flags"]}
    score = 0
    if rec["on_fire"]: score -= 100
    if "blocked" in kinds: score -= 50
    if "past_due" in kinds: score -= 40
    if "contradiction" in kinds: score -= 30
    if "stale_near_gate" in kinds: score -= 20
    if rec["is_gate"]: score -= 10
    return (score, rec["days_to_end"] if rec["days_to_end"] is not None else 9999)

def render(sheet_name, snapshot, findings):
    out = []
    n_prog = len(snapshot)
    n_open = sum(len(v) for v in snapshot.values())
    flagged_progs = sorted({f["program"] for f in findings})
    out.append(f"# portfolio-check — {sheet_name}")
    out.append(f"_scanned {TODAY} · {n_open} open items across {n_prog} programs · "
               f"{len(findings)} items flagged in {len(flagged_progs)} programs_\n")

    # headline (the future push-notification line)
    out.append("## Headline")
    if findings:
        bits = []
        for p in flagged_progs:
            recs = [f for f in findings if f["program"] == p]
            kinds = {k for r in recs for k in (f["kind"] for f in r["flags"])}
            tag = "blocked" if "blocked" in kinds else \
                  "past-due" if "past_due" in kinds else \
                  "stale" if "stale_near_gate" in kinds else "drift"
            bits.append(f"{p} ({tag})")
        out.append(f"**{len(findings)} items need attention** — " + "; ".join(bits) + "\n")
    else:
        out.append("**All clear** — no open items tripped a rule.\n")

    CONF_MARK = {"FACT": "🟥 FACT", "INFERENCE": "🟧 INFERENCE", "HYPOTHESIS": "🟨 HYPOTHESIS"}
    for p in flagged_progs:
        out.append(f"## {p}")
        recs = sorted([f for f in findings if f["program"] == p], key=rank_key)
        for rec in recs:
            gate = " · GATE" if rec["is_gate"] else ""
            fire = " · 🔥ON FIRE" if rec["on_fire"] else ""
            out.append(f"### {rec['task']}{gate}{fire}")
            meta = [f"row {rec['row']}", f"status: {rec['status']}",
                    f"owner: {rec['owner'] or '—'}",
                    f"health: {rec['health'] or '—'}",
                    f"end: {rec['end_date'] or '—'}"]
            if rec["days_to_end"] is not None:
                meta.append(f"due in {rec['days_to_end']}d")
            out.append("> " + " · ".join(meta))
            for f in rec["flags"]:
                out.append(f"- {CONF_MARK[f['confidence']]} — {f['msg']}  _({f['evidence']})_")
            out.append("")
    return "\n".join(out)

VAULT_DIR = os.environ.get(
    "PORTFOLIO_CHECK_VAULT_DIR",
    os.path.expanduser("~/Documents/ObsidianVault/Sessions/Portfolio-Check"))

def frontmatter(name, n_flagged, n_open, n_prog):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return ("---\n"
            f"date: {TODAY}\n"
            "type: portfolio-check\n"
            f"generated: {now} CT\n"
            f"sheet: {name}\n"
            f"flagged: {n_flagged}\n"
            f"open_items: {n_open}\n"
            f"programs: {n_prog}\n"
            "---\n\n")

def main():
    sheet_id = sys.argv[1] if len(sys.argv) > 1 else MONDAY_SHEET
    if not sheet_id:
        sys.exit("No sheet id. Set BOWLER_SHEET_ID or pass it as the first argument.\n"
                 "List the sheets your token can see:  python3 smartsheet_list.py")
    name, rows = load(sheet_id)
    snapshot, findings = analyze(rows)
    n_open = sum(len(v) for v in snapshot.values())
    n_prog = len(snapshot)

    os.makedirs("out", exist_ok=True)
    with open("out/project-snapshot.json", "w") as fh:
        json.dump({"sheet": name, "scanned": str(TODAY), "programs": snapshot},
                  fh, indent=2, default=str)

    report = render(name, snapshot, findings)
    doc = frontmatter(name, len(findings), n_open, n_prog) + report
    with open("out/portfolio-check.md", "w") as fh:
        fh.write(doc)

    # write to the Obsidian vault: latest (overwrite) + dated archive
    os.makedirs(VAULT_DIR, exist_ok=True)
    for fn in ("latest-portfolio-check.md", f"{TODAY}-portfolio-check.md"):
        with open(os.path.join(VAULT_DIR, fn), "w") as fh:
            fh.write(doc)

    print(f"portfolio-check written — {len(findings)} flagged across "
          f"{len({f['program'] for f in findings})} programs "
          f"({n_open} open items, {n_prog} programs scanned)")
    print(f"vault: {VAULT_DIR}/latest-portfolio-check.md")

if __name__ == "__main__":
    main()
