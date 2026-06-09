#!/usr/bin/env python3
"""load-vault-context.py — on-load context injector for the Obsidian agent-brain loop.

Reads the most recent session logs from an Obsidian vault and prints a compact
"recent context" block. Wire it to a SessionStart hook so every new agent session
starts already knowing where things stand — without re-explaining.

How it works:
  - SessionStart hooks inject a command's stdout into the session as context.
  - This script reads the `summary:` frontmatter (and date) from the N most
    recent session logs and prints them as a short briefing.

Configuration (environment variables):
  OBSIDIAN_SESSIONS_DIR   path to the vault's session-log folder (required)
  RECENT_SESSIONS_COUNT   how many recent logs to include (default 5)
  RECENT_SESSIONS_PROJECT optional: only include logs whose `project:` matches

Usage:
  OBSIDIAN_SESSIONS_DIR=~/vault/sessions python3 load-vault-context.py

Wire into Claude Code (~/.claude/settings.json):
  {
    "hooks": {
      "SessionStart": [
        { "hooks": [
            { "type": "command",
              "command": "OBSIDIAN_SESSIONS_DIR=~/vault/sessions python3 /path/to/load-vault-context.py" }
        ] }
      ]
    }
  }

Other agents (Codex, etc.): run the same script from your startup convention and
feed its stdout into the model's context.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}-.*\.md$")


def read_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def main() -> int:
    raw = os.environ.get("OBSIDIAN_SESSIONS_DIR")
    if not raw:
        # Silent no-op: a missing config shouldn't break session startup.
        return 0
    sessions = Path(raw).expanduser()
    if not sessions.is_dir():
        return 0

    count = int(os.environ.get("RECENT_SESSIONS_COUNT", "5"))
    project = os.environ.get("RECENT_SESSIONS_PROJECT")

    files = sorted(
        (p for p in sessions.glob("*.md") if SLUG_RE.match(p.name)),
        key=lambda p: p.name,
        reverse=True,
    )

    rows = []
    for p in files:
        try:
            fm = read_frontmatter(p.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue
        if project and fm.get("project") not in (project, None):
            if fm.get("project") != project:
                continue
        summary = fm.get("summary", "").strip()
        date = fm.get("date", p.name[:10])
        if summary:
            rows.append((date, fm.get("project", ""), summary))
        if len(rows) >= count:
            break

    if not rows:
        return 0

    print("## Recent session context (from Obsidian vault)\n")
    print("Most recent work, newest first. Use `/recall <topic>` to search deeper.\n")
    for date, proj, summary in rows:
        tag = f" `{proj}`" if proj else ""
        print(f"- **{date}**{tag} — {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
