# Dovetail → persona-engine connector

Pipes curated **live Dovetail research** into the persona-analysis engine, so the clustering
runs on fresh interview data rather than static sample transcripts.

## Architecture (LLM/MCP fetch separated from deterministic transform)

```
 [1] FETCH (Claude, main process)        [2] INGEST (deterministic)       [3] BUILD (deterministic)       [4] ANALYZE
 Dovetail MCP get_data_content   ──▶   raw/<data_id>.json          ──▶   <stream>/*.txt transcripts ──▶  pipeline.run_pipeline
   (large → persisted to disk;          (one slim JSON per entry)        (cleaned, stream-routed)        (LLM extract → cluster)
    small → inline in session log)
```

Only step 1 touches MCP/network. Steps 2–4 are pure Python and re-runnable offline. That
split matters: you re-cluster as many times as you like without re-fetching, and the
deterministic half is testable without credentials.

## Streams (curation by intent)

Routing is by **explicit `data_id`** in your manifest (because `get_data_content` omits the
project field), falling back to project id when present.

Define one stream per *kind of voice*, and keep them apart:

- **A behavioral-interview stream** → the clustering engine. End-user interviews only.
- **A B2B / channel stream** → **NOT** clustered. Partner, OEM, and dealer interviews are
  about business and integration needs, not end-user behavior; mixing them into behavioral
  clustering pollutes it. Land them separately for their own analysis.

Copy `manifest.example.json` to `manifest.json` and fill in your own project/data ids. Tune
`skip_title_patterns` there (it drops photos, surveys, candidate/question lists, numbered
highlight clips) and set `min_transcript_chars`.

`manifest.json` and everything under `raw/`, `streams/`, and your transcript input directory
are **research data, not framework** — keep them out of any shared repo. See "Data handling."

## Run it

**Step 1 — fetch (Claude does this).** For each curated entry, call the Dovetail MCP
`get_data_content(data_id)`. Add the entry's `data_id` to the right stream in `manifest.json`.

**Step 2+3 — ingest + build.** Two paths, depending on how the fetches came back:

```bash
# Normal path: payloads persisted to the session tool-results dir
python dovetail_to_transcripts.py --ingest <session>/tool-results
```

```bash
# Inline fallback: smaller payloads are returned inline and live only in the session
# transcript. Mine BOTH the jsonl and tool-results, then build.
python ingest_from_session.py --jsonl "$CLAUDE_SESSION_JSONL" --tool-results "$CLAUDE_TOOL_RESULTS"
```

```bash
python dovetail_to_transcripts.py            # build transcripts + run_log.json
python dovetail_to_transcripts.py --report   # inspect what was kept/skipped and why
```

`$CLAUDE_SESSION_JSONL` and `$CLAUDE_TOOL_RESULTS` are under
`~/.claude/projects/<project-slug>/`.

**Step 4 — analyze.** Requires `ANTHROPIC_API_KEY` — your own key, never provisioned by the
connector. Deps come from `pipeline/requirements.txt`.

```bash
export ANTHROPIC_API_KEY=...
```

```bash
# Optional: propose fresh dimension options from the corpus before locking a config
python -m pipeline.run_pipeline --phase discover --transcripts <input-dir>
```

```bash
# Full run: extract → cluster → classify → validate → report
python -m pipeline.run_pipeline --phase full --config <project>_config.json --transcripts <input-dir> --output <output-dir>
```

## Data handling (read before running on real research)

- **Transcripts are participant data.** `raw/`, `streams/`, the transcript input dir, and
  `run_log.json` (which records participant names alongside file paths) all contain PII.
  Gitignore them; the source of record is Dovetail, where participants consented for the
  content to live.
- **Re-pull rather than copy.** If someone else needs this analysis, give them the config and
  the connector and let them pull with their own Dovetail seat. Loose transcript files on a
  shared drive are a second, unmanaged copy of consented research.
- **Only outputs travel.** Persona profiles and reports are derived and aggregated — those are
  the shareable artifact.

## Notes / caveats

- A config tuned for one study is a *starting point* for another, not a drop-in. If the new
  corpus has a different framing (e.g. a survey vs. a product-feedback session), run
  `--phase discover` first and check whether the existing dimension options are actually
  exercised before locking the config. Options with zero support produce fake separation.
- Watch for participants whose role is ambiguous (end-user vs. dealer/trade). The pipeline's
  tier-1 coverage check flags low-signal transcripts — believe it.
- **Small n is the main failure mode.** The engine forces k and warns on overfit at low
  sample counts. Below roughly 15 transcripts, treat output as directional and say so in the
  report; leave-one-out stability in the report tells you how much to trust it.
