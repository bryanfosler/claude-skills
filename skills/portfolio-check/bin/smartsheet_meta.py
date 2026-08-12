#!/usr/bin/env python3
"""Print provenance + shape of a sheet. Read-only."""
import sys, os, json, subprocess, urllib.request

def token():
    return subprocess.run(["security","find-generic-password","-a",os.environ["USER"],
        "-s","smartsheet-api","-w"], capture_output=True, text=True, check=True).stdout.strip()

def get(path, tok):
    req = urllib.request.Request("https://api.smartsheet.com/2.0"+path,
        headers={"Authorization":"Bearer "+tok})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

sid = sys.argv[1]
s = get(f"/sheets/{sid}?include=ownerInfo", token())
print("name:        ", s.get("name"))
print("owner:       ", s.get("owner"), "(ownerId", s.get("ownerId"), ")")
print("createdAt:   ", s.get("createdAt"))
print("modifiedAt:  ", s.get("modifiedAt"))
print("totalRows:   ", s.get("totalRowCount"))
print("columns:     ", [c["title"] for c in s["columns"]])
print("\nfirst rows (primary col):")
prim = next((c["id"] for c in s["columns"] if c.get("primary")), None)
for r in s["rows"][:14]:
    cell = next((c for c in r.get("cells",[]) if c["columnId"]==prim), {})
    print(f"  row {r['rowNumber']}: {cell.get('displayValue', cell.get('value',''))}")
