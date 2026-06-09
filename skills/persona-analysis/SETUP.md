# Persona Analysis — Setup

A self-contained, deterministic pipeline that turns customer interview transcripts into
behavioral personas (structured LLM extraction → pure-Python clustering → validation → JTBD bridge).

Everything needed to run is in this folder. Nothing external is required beyond the Python
dependencies and an Anthropic API key.

## 1. Install

```bash
cd persona-analysis-for-evan          # the package root (where this file lives)
python3 -m venv .venv && source .venv/bin/activate
pip install -r pipeline/requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
```

Requires Python 3.10+.

## 2. Configure your domain (once)

Scan your transcripts to get proposed dimension options:

```bash
python3 -m pipeline.run_pipeline --phase discover --transcripts path/to/transcripts/
```

Then copy `schemas/project_config.json`, fill in every `REPLACE_WITH_YOUR_...` value with
your own product's contexts / triggers / pain points / ecosystem, and save it as
`project_config.json` in the package root.

> Transcripts = one `.txt` or `.md` file per interviewee. 7+ recommended; the pipeline will
> honestly report "no natural clusters" below the statistical threshold rather than invent personas.

## 3. Run

```bash
# full pipeline (extract → cluster → validate → report)
python3 -m pipeline.run_pipeline --transcripts path/to/transcripts/

# already have extractions.json? skip straight to clustering
python3 -m pipeline.run_pipeline --phase cluster
```

See `python3 -m pipeline.run_pipeline --help` for all phases and flags.

## 4. Output

```
output/
├── PERSONA_REPORT.md      # profiles + validation metrics (read this first)
├── PERSONA_PROFILES.json  # machine-readable, feeds JTBD
└── extractions.json       # per-interview structured data + verbatim evidence (audit trail)
```

## How it works (short version)

- **Extraction** runs 3 passes per transcript with different framings (behavior- / motivation- /
  frustration-first) and merges by consensus — that variance-then-consensus is what makes it
  reproducible. Every extracted value carries a verbatim quote.
- **Clustering** is pure Python (k-means + silhouette, fixed seed). NaN-aware distances, categorical
  normalization, auto-PCA for small samples, and a minimum silhouette gate so it won't fabricate
  segments.
- **Validation** flags overfit, fragility (leave-one-out), decorative dimensions, and borderline
  customers before any of it reaches your conclusions.

`README.md` and `SKILL.md` go deeper on the methodology and the "no clusters" handling.

---
*Bundled as a standalone package — paths in the docs refer to files inside this folder.*
