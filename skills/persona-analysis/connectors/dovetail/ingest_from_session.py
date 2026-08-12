#!/usr/bin/env python3
"""
Session-ingest fallback for the Dovetail connector.

When Claude fetches entries via the Dovetail MCP, large payloads are persisted to the
session tool-results dir, but smaller ones are returned inline and only exist in the
session transcript (.jsonl). This helper mines BOTH sources for Dovetail data payloads
(anything carrying `content_markdown`) and writes each to raw/<id>.json so the
deterministic adapter (dovetail_to_transcripts.py) can build transcripts from them.

No MCP/network. Pure disk read.

Usage:
    python ingest_from_session.py \
        --jsonl /path/to/<session>.jsonl \
        --tool-results /path/to/<session>/tool-results
    # then:
    python dovetail_to_transcripts.py        # build transcripts + run_log.json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from dovetail_to_transcripts import parse_payload, RAW_DIR


def deep_find_payloads(obj, found: list):
    """Recursively walk a parsed object tree collecting any dict that is a Dovetail data
    payload (has content_markdown + id). Tool-result bodies are JSON strings nested inside
    the message JSON, so we also attempt to json.loads any string and recurse into it."""
    if isinstance(obj, dict):
        if "content_markdown" in obj and "id" in obj:
            found.append(obj)
        for v in obj.values():
            deep_find_payloads(v, found)
    elif isinstance(obj, list):
        for v in obj:
            deep_find_payloads(v, found)
    elif isinstance(obj, str):
        if "content_markdown" in obj:
            s = obj.strip()
            if s and s[0] in "[{":
                try:
                    deep_find_payloads(json.loads(s), found)
                except json.JSONDecodeError:
                    pass


def ingest_jsonl(path: Path) -> list[dict]:
    out = []
    with open(path, errors="ignore") as f:
        for line in f:
            if "content_markdown" not in line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            deep_find_payloads(obj, out)
    return out


def ingest_tool_results(d: Path) -> list[dict]:
    out = []
    for jf in sorted(d.glob("*.json")):
        try:
            obj = json.load(open(jf))
        except (json.JSONDecodeError, OSError):
            continue
        payload = parse_payload(obj)
        if payload:
            out.append(payload)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", help="Path to the Claude session .jsonl transcript")
    ap.add_argument("--tool-results", help="Path to the session tool-results dir")
    args = ap.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    payloads = {}
    if args.jsonl:
        for p in ingest_jsonl(Path(args.jsonl).expanduser()):
            payloads[p["id"]] = p  # dedupe by id; last wins
    if args.tool_results:
        for p in ingest_tool_results(Path(args.tool_results).expanduser()):
            payloads[p["id"]] = p

    for pid, p in payloads.items():
        slim = {"id": p["id"], "title": p.get("title", ""),
                "content_markdown": p.get("content_markdown", "")}
        if p.get("project"):
            slim["project"] = p["project"]
        (RAW_DIR / f"{pid}.json").write_text(json.dumps(slim, indent=2, ensure_ascii=False))

    print(f"Wrote {len(payloads)} raw payload(s) -> {RAW_DIR}")
    for pid, p in payloads.items():
        print(f"  {pid}  {p.get('title','')[:55]}  ({len(p.get('content_markdown',''))} chars)")


if __name__ == "__main__":
    main()
