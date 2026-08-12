#!/usr/bin/env python3
"""Build a self-contained visual-plan / visual-recap HTML file.

Injects a plan JSON (the block data model) into the shared runtime template.
No third-party dependencies; runs on stdlib only.

Usage (single line):
  python3 ~/.claude/skills/visual-plan/bin/build_plan.py --data /tmp/plan.json --out /tmp/plan.html

The JSON shape is documented in references/block-catalog.md. Minimal:
  {"meta": {"title": "...", "kind": "plan"|"recap"}, "blocks": [ ... ]}
"""
import argparse
import json
import os
import sys

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


def read(name):
    with open(os.path.join(ASSETS, name), "r", encoding="utf-8") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser(description="Build a self-contained visual plan/recap HTML file.")
    ap.add_argument("--data", required=True, help="Path to the plan JSON file.")
    ap.add_argument("--out", required=True, help="Path to write the HTML file.")
    ap.add_argument("--kind", choices=["plan", "recap"], help="Override meta.kind.")
    args = ap.parse_args()

    with open(args.data, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            sys.exit("ERROR: %s is not valid JSON: %s" % (args.data, e))

    data.setdefault("meta", {})
    if args.kind:
        data["meta"]["kind"] = args.kind
    data["meta"].setdefault("kind", "plan")
    data.setdefault("blocks", [])
    data.setdefault("state", {"edits": {}, "checks": {}, "answers": {}, "comments": []})

    # Validate block ids are present and unique (cheap guard; the renderer needs them).
    seen = set()
    for i, b in enumerate(data["blocks"]):
        if "type" not in b:
            sys.exit("ERROR: block #%d has no 'type'." % i)
        if "id" not in b:
            b["id"] = "b%d" % i
        if b["id"] in seen:
            sys.exit("ERROR: duplicate block id '%s'." % b["id"])
        seen.add(b["id"])

    template = read("template.html")
    styles = read("styles.css")
    # Defensive: a literal closing-script sequence anywhere in the inlined JS would
    # terminate the <script> tag early. Neutralize it; the escaped form is identical JS.
    runtime = read("runtime.js").replace("</script", "<\\/script")
    # Embed JSON safely inside a <script> context.
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    title = data["meta"].get("title", "Visual Plan")

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
