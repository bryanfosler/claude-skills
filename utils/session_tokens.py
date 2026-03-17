#!/usr/bin/env python3
"""
session_tokens.py — Claude Code session token + cost tracker

Reads the current session from ~/.claude/history.jsonl, finds the matching
JSONL transcript, and sums token usage across all assistant turns.

Usage:
    python3 session_tokens.py

Output:
    Tokens: 1234567  Cost: 4.56

Pricing (update if Anthropic changes rates):
    https://www.anthropic.com/pricing
"""

import json
import os
import glob
from pathlib import Path

# ── Pricing (USD per million tokens) ─────────────────────────────────────────
# Update these if Anthropic changes rates. Current: claude-sonnet-4-6
PRICING = {
    "input":         3.00,   # per 1M input tokens
    "output":       15.00,   # per 1M output tokens
    "cache_write":   3.75,   # per 1M cache creation tokens
    "cache_read":    0.30,   # per 1M cache read tokens
}

CLAUDE_DIR = Path.home() / ".claude"
HISTORY_FILE = CLAUDE_DIR / "history.jsonl"
PROJECTS_DIR = CLAUDE_DIR / "projects"


def get_current_session_id():
    """Read the most recent sessionId from history.jsonl."""
    if not HISTORY_FILE.exists():
        raise FileNotFoundError(f"No history file found at {HISTORY_FILE}")

    last_session = None
    with open(HISTORY_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if "sessionId" in entry:
                    last_session = entry["sessionId"]
            except json.JSONDecodeError:
                continue

    if not last_session:
        raise ValueError("No sessionId found in history.jsonl")
    return last_session


def find_session_file(session_id):
    """Find the JSONL transcript file for the given session ID."""
    pattern = str(PROJECTS_DIR / "**" / "*.jsonl")
    candidates = glob.glob(pattern, recursive=True)

    for path in candidates:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get("sessionId") == session_id:
                        return path
                except json.JSONDecodeError:
                    continue
    return None


def sum_tokens(session_file):
    """Sum all token counts from assistant turns in the session file."""
    totals = {
        "input": 0,
        "output": 0,
        "cache_write": 0,
        "cache_read": 0,
    }

    with open(session_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            if entry.get("type") != "assistant":
                continue

            usage = entry.get("message", {}).get("usage", {})
            totals["input"]       += usage.get("input_tokens", 0)
            totals["output"]      += usage.get("output_tokens", 0)
            totals["cache_write"] += usage.get("cache_creation_input_tokens", 0)
            totals["cache_read"]  += usage.get("cache_read_input_tokens", 0)

    return totals


def calculate_cost(totals):
    """Calculate USD cost from token totals using PRICING table."""
    cost = 0.0
    for key, price_per_million in PRICING.items():
        cost += totals[key] * price_per_million / 1_000_000
    return cost


def main():
    session_id = get_current_session_id()
    session_file = find_session_file(session_id)

    if not session_file:
        print(f"Session file not found for session: {session_id}")
        return

    totals = sum_tokens(session_file)
    total_tokens = sum(totals.values())
    cost = calculate_cost(totals)

    print(f"Tokens: {total_tokens}  Cost: {cost:.2f}")


if __name__ == "__main__":
    main()
