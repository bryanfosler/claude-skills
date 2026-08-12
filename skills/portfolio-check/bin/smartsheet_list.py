#!/usr/bin/env python3
"""List every Smartsheet the token can see: name, numeric id, permalink.
Read-only. Token pulled from macOS Keychain, never stored."""
import json, subprocess, urllib.request, os

def token():
    return subprocess.run(
        ["security", "find-generic-password", "-a", os.environ["USER"],
         "-s", "smartsheet-api", "-w"],
        capture_output=True, text=True, check=True).stdout.strip()

def get(path, tok):
    req = urllib.request.Request("https://api.smartsheet.com/2.0" + path,
                                 headers={"Authorization": "Bearer " + tok})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def main():
    tok = token()
    data = get("/sheets?includeAll=true", tok)
    rows = data.get("data", [])
    print(f"{len(rows)} sheets visible to this token:\n")
    for s in rows:
        print(f"  id={s['id']}  name={s.get('name','?')!r}")
        print(f"      {s.get('permalink','')}")

if __name__ == "__main__":
    main()
