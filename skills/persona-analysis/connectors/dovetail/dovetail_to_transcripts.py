#!/usr/bin/env python3
"""
Dovetail -> persona-engine connector (deterministic, no MCP/network).

Two-step bridge that keeps the LLM/MCP fetch separate from code-based transform,
per the project's deterministic-pipeline preference:

  1. FETCH (done by Claude in the main process via the Dovetail MCP):
       get_data_content(data_id) for each curated entry. Large payloads are
       persisted by the harness to the session tool-results dir. Those raw
       payloads are the input to this script.

  2. BUILD (this script, deterministic):
       --ingest <dir>  : scan a dir for raw Dovetail get_data_content payloads,
                         copy matched ones into raw/<data_id>.json (durable).
       (default)        : read raw/, route each entry to a STREAM by project id
                         (per manifest.json), apply skip rules + a transcript
                         length floor, normalize content_markdown into a clean
                         transcript .txt, and write it to the stream's input_dir.

Run:
    python dovetail_to_transcripts.py --ingest /path/to/session/tool-results
    python dovetail_to_transcripts.py            # build transcripts from raw/
    python dovetail_to_transcripts.py --report   # show last run log

Output per build: <stream.input_dir>/*.txt  +  run_log.json
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW_DIR = HERE / "raw"
MANIFEST = HERE / "manifest.json"
RUN_LOG = HERE / "run_log.json"


def load_manifest() -> dict:
    with open(MANIFEST) as f:
        return json.load(f)


def parse_payload(obj) -> dict | None:
    """Normalize a get_data_content payload into the inner {id,title,content_markdown,...} dict.

    Handles: the MCP array form [{"type":"text","text":"<json>"}], a {"data":{...}} wrapper,
    or an already-unwrapped data dict. Returns None if it isn't a Dovetail data payload.
    """
    # Array form: find the text item and parse its JSON string.
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict) and "text" in item:
                try:
                    return parse_payload(json.loads(item["text"]))
                except (json.JSONDecodeError, TypeError):
                    continue
        return None
    if isinstance(obj, dict):
        if "data" in obj and isinstance(obj["data"], dict):
            obj = obj["data"]
        if "content_markdown" in obj and "id" in obj:
            return obj
    return None


def ingest(source: Path) -> int:
    """Copy any raw Dovetail data payloads found under `source` into raw/<id>.json."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    copied = 0
    for jf in sorted(source.glob("*.json")):
        try:
            with open(jf) as f:
                obj = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        data = parse_payload(obj)
        if data is None:
            continue
        dest = RAW_DIR / f"{data['id']}.json"
        with open(dest, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        copied += 1
        print(f"  ingested {data['id']}  {data.get('title','')[:60]}")
    print(f"Ingested {copied} Dovetail payload(s) into {RAW_DIR}")
    return copied


def slugify(title: str) -> str:
    s = re.sub(r"[^\w\s-]", "", title.lower()).strip()
    s = re.sub(r"[\s_-]+", "_", s)
    return s[:60] or "untitled"


def clean_transcript(md: str) -> str:
    """Strip the leading AudioVideo link / boilerplate, keep speaker-tagged transcript body."""
    lines = md.splitlines()
    kept = []
    for ln in lines:
        s = ln.strip()
        if s.startswith("[AudioVideo") or s == "#### Transcript":
            continue
        kept.append(ln)
    return "\n".join(kept).strip()


def stream_for_entry(manifest: dict, data: dict):
    """Route an entry to a stream by explicit data_id first (get_data_content omits the
    project field), then fall back to the entry's project id when present."""
    data_id = data.get("id")
    project_id = (data.get("project") or {}).get("id")
    for name, spec in manifest["streams"].items():
        if data_id and data_id in spec.get("data_ids", []):
            return name, spec
    for name, spec in manifest["streams"].items():
        for proj in spec.get("projects", []):
            if proj["id"] == project_id:
                return name, spec
    return None, None


def should_skip(manifest: dict, data: dict) -> str | None:
    if data["id"] in manifest.get("skip_data_ids", []):
        return "skip_data_ids"
    title = data.get("title", "")
    for pat in manifest.get("skip_title_patterns", []):
        if re.search(pat, title):
            return f"title~/{pat}/"
    return None


def build(manifest: dict) -> dict:
    floor = manifest.get("min_transcript_chars", 0)
    log = {"kept": [], "skipped": []}
    # Clean rider/oe input dirs at the start of a build so re-runs are idempotent.
    for spec in manifest["streams"].values():
        out = (HERE / spec["input_dir"]).resolve()
        out.mkdir(parents=True, exist_ok=True)
        for old in out.glob("dt_*.txt"):
            old.unlink()

    for jf in sorted(RAW_DIR.glob("*.json")):
        with open(jf) as f:
            data = json.load(f)
        title = data.get("title", "")
        project_id = (data.get("project") or {}).get("id")

        stream_name, spec = stream_for_entry(manifest, data)
        if spec is None:
            log["skipped"].append({"id": data["id"], "title": title, "reason": "no stream for entry"})
            continue

        skip_reason = should_skip(manifest, data)
        if skip_reason:
            log["skipped"].append({"id": data["id"], "title": title, "stream": stream_name, "reason": skip_reason})
            continue

        body = clean_transcript(data.get("content_markdown", "") or "")
        if len(body) < floor:
            log["skipped"].append({"id": data["id"], "title": title, "stream": stream_name,
                                    "reason": f"transcript too short ({len(body)}<{floor})"})
            continue

        out_dir = (HERE / spec["input_dir"]).resolve()
        fname = f"dt_{slugify(title)}.txt"
        header = f"# Source: Dovetail | {title} | id={data['id']} | project={project_id}\n\n"
        (out_dir / fname).write_text(header + body)
        log["kept"].append({"id": data["id"], "title": title, "stream": stream_name,
                             "chars": len(body), "file": str(out_dir / fname)})

    with open(RUN_LOG, "w") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    by_stream = {}
    for k in log["kept"]:
        by_stream.setdefault(k["stream"], 0)
        by_stream[k["stream"]] += 1
    print(f"\nBuilt transcripts: {len(log['kept'])} kept, {len(log['skipped'])} skipped")
    for s, n in sorted(by_stream.items()):
        print(f"  {s}: {n} transcripts -> {(HERE / manifest['streams'][s]['input_dir']).resolve()}")
    if log["skipped"]:
        print("  skipped:")
        for s in log["skipped"]:
            print(f"    - {s['title'][:50]:50s} [{s['reason']}]")
    return log


def main():
    ap = argparse.ArgumentParser(description="Dovetail -> persona-engine connector")
    ap.add_argument("--ingest", help="Dir to scan for raw Dovetail get_data_content payloads")
    ap.add_argument("--report", action="store_true", help="Print last run_log.json and exit")
    args = ap.parse_args()

    if args.report:
        if RUN_LOG.exists():
            print(RUN_LOG.read_text())
        else:
            print("No run_log.json yet.")
        return

    manifest = load_manifest()
    if args.ingest:
        ingest(Path(args.ingest).expanduser())
    build(manifest)


if __name__ == "__main__":
    main()
