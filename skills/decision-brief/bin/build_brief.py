#!/usr/bin/env python3
"""Build a self-contained decision-brief HTML file.

Injects a brief JSON (the block data model) into the shared runtime template.
No third-party dependencies; runs on stdlib only. Forked from visual-plan's
build_plan.py — same injection mechanism, memo-genre data model.

Usage (single line):
  python3 ~/.claude/skills/decision-brief/bin/build_brief.py --data /tmp/brief.json --out /tmp/brief.html

The JSON shape is documented in references/block-catalog.md. Minimal:
  {"meta": {"title": "...", "question": "...", "owner": "...", "date": "YYYY-MM-DD"},
   "blocks": [ {"id":"rec","type":"recommendation","brief":"...","detail":"..."}, ... ]}
"""
import argparse
import json
import os
import sys

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

# The fixed answer-first spine. Order is enforced only as a warning — the author
# may legitimately omit Options (no real decision) and may add evidence blocks.
SPINE = ["recommendation", "problem", "background", "options", "rationale", "open-questions"]


def read(name):
    with open(os.path.join(ASSETS, name), "r", encoding="utf-8") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser(description="Build a self-contained decision-brief HTML file.")
    ap.add_argument("--data", required=True, help="Path to the brief JSON file.")
    ap.add_argument("--out", required=True, help="Path to write the HTML file.")
    args = ap.parse_args()

    with open(args.data, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            sys.exit("ERROR: %s is not valid JSON: %s" % (args.data, e))

    data.setdefault("meta", {})
    data["meta"].setdefault("kind", "brief")
    data.setdefault("blocks", [])
    data.setdefault("state", {"edits": {}, "answers": {}, "comments": []})

    # Validate block ids are present and unique (cheap guard; the renderer needs them).
    seen = set()
    types = []
    for i, b in enumerate(data["blocks"]):
        if "type" not in b:
            sys.exit("ERROR: block #%d has no 'type'." % i)
        if "id" not in b:
            b["id"] = "b%d" % i
        if b["id"] in seen:
            sys.exit("ERROR: duplicate block id '%s'." % b["id"])
        seen.add(b["id"])
        types.append(b["type"])

    # Soft guardrails — the brief is a recommendation memo, so it must lead with an answer.
    if types and types[0] != "recommendation":
        sys.stderr.write("WARNING: first block is '%s', not 'recommendation'. A decision brief "
                         "should lead with the answer.\n" % types[0])
    if "recommendation" not in types:
        sys.stderr.write("WARNING: no 'recommendation' block. If the work doesn't support a single "
                         "conclusion, pause and ask the user rather than shipping a brief without one.\n")

    template = read("template.html")
    styles = read("styles.css")
    # Defensive: a literal closing-script sequence anywhere in the inlined JS would
    # terminate the <script> tag early. Neutralize it; the escaped form is identical JS.
    runtime = read("runtime.js").replace("</script", "<\\/script")
    # Embed JSON safely inside a <script> context.
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    title = data["meta"].get("title", "Decision Brief")

    html = (template
            .replace("__TITLE__", _esc(title))
            .replace("__STYLES__", styles)
            .replace("__PLAN_DATA__", payload)
            .replace("__RUNTIME__", runtime))

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print("Wrote %s (%d blocks, %.1f KB)" % (args.out, len(data["blocks"]), len(html) / 1024.0))


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


if __name__ == "__main__":
    main()
