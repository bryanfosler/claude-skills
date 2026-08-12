#!/usr/bin/env python3
"""Dump a sheet's structure: columns (title/type) + sample rows. Read-only.
Usage: python3 smartsheet_dump.py <sheet_id> [n_rows]"""
import json, subprocess, urllib.request, os, sys

def token():
    return subprocess.run(
        ["security", "find-generic-password", "-a", os.environ["USER"],
         "-s", "smartsheet-api", "-w"],
        capture_output=True, text=True, check=True).stdout.strip()

def get(path, tok):
    req = urllib.request.Request("https://api.smartsheet.com/2.0" + path,
                                 headers={"Authorization": "Bearer " + tok})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def main():
    sid = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    s = get(f"/sheets/{sid}", token())
    cols = s["columns"]
    by_id = {c["id"]: c["title"] for c in cols}
    print(f"SHEET: {s['name']}   rows={s['totalRowCount']}\n")
    print("COLUMNS:")
    for c in cols:
        extra = ""
        if c.get("options"):
            extra = "  options=" + json.dumps(c["options"])[:120]
        prim = " [PRIMARY]" if c.get("primary") else ""
        print(f"  - {c['title']!r}  ({c['type']}){prim}{extra}")
    print(f"\nFIRST {n} ROWS (indent = hierarchy depth):")
    # build depth map from parentId chain
    depth = {}
    def d(rid):
        return depth.get(rid, 0)
    for row in s["rows"][:n]:
        pid = row.get("parentId")
        depth[row["id"]] = (depth.get(pid, 0) + 1) if pid in depth else 0
        pad = "  " * depth[row["id"]]
        vals = {}
        for cell in row.get("cells", []):
            t = by_id.get(cell["columnId"], "?")
            v = cell.get("displayValue", cell.get("value"))
            if v not in (None, ""):
                vals[t] = v
        print(f"{pad}row {row['rowNumber']}: {json.dumps(vals, default=str)[:400]}")

if __name__ == "__main__":
    main()
