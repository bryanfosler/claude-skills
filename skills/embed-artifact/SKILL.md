---
name: embed-artifact
description: Use when the user wants an HTML (or other rendered) artifact viewable INSIDE Obsidian — "embed in obsidian", "save this html to the vault", "put the dashboard in obsidian", "make it viewable in obsidian", "view this in obsidian", or invokes /embed-artifact. Copies the artifact into a vault project folder and scaffolds a .md wrapper (absolute file:// iframe + native-Mermaid fallback) so it renders in Reading view. Default: refresh the LATEST version in place; "log all" keeps timestamped copies. Composes with /log-session and /wrap-up.
---

# Embed Artifact in Obsidian

Make a generated artifact (usually a self-contained `.html` dashboard) viewable
**inside** Obsidian — not just "open in browser." The artifact is copied into a
vault project folder and paired with a `.md` wrapper that embeds it via an
**absolute `file://` iframe**, with the artifact's diagrams also dropped in as
**native Mermaid** so the note is never blank even if the iframe is blocked.

This is the **artifact** half of the Obsidian loop; `log-session` handles the
text log, this handles rendered deliverables. It is designed to be **composed**
(see "How this fits the loop") — `/log-session` and `/wrap-up` can invoke it.

---

## Configure

```
OBSIDIAN_VAULT: ~/Documents/ObsidianSRAM     # vault ROOT — must resolve to an absolute path for file://
OBSIDIAN_PROJECTS_SUBDIR: Projects           # where per-project folders live
```

If `OBSIDIAN_VAULT` is unset or doesn't exist, STOP and tell the user — never
write elsewhere. Quote all paths in shell (vault paths contain spaces).

---

## Inputs

- **artifact** — path to the file to embed. If this session just generated one,
  use that path. If several exist and the user didn't say which, ask (or treat
  "log all" as "embed each").
- **project** — target folder name under `Projects/` (e.g. `PD-Milestones`).
  Default to a slug of the artifact name; confirm if ambiguous.
- **mode** — `latest` (default) or `all`. Use `all` only when the user says
  "log all artifacts" / "keep versions."

---

## Procedure

### Step 1 — Resolve the absolute vault path

`file://` iframes only resolve with an **absolute** path in Obsidian's Electron
renderer (relative paths silently fail — this is the #1 cause of a blank embed).

```bash
VAULT_ABS=$(cd "${OBSIDIAN_VAULT/#\~/$HOME}" 2>/dev/null && pwd) || { echo "Vault not found"; exit 1; }
DEST="$VAULT_ABS/${OBSIDIAN_PROJECTS_SUBDIR:-Projects}/<Project>"
mkdir -p "$DEST"
```

### Step 2 — Place the artifact (versioning)

Pick a stable Pascal/kebab `<Slug>` (e.g. `PD-Milestones-Map`).

- **latest (default):** canonical name `<Slug>.html` — copy/overwrite in place.
  This is the right behavior when iterating on revisions: one living file, no
  clutter. If a wrapper `.md` already exists, you'll refresh it (Step 4) and
  bump `rev:` rather than create a new note.
- **all:** `<Slug>-$(date +%Y-%m-%d).html` — keep prior copies; list them in a
  "Versions" section of the wrapper note (newest first).

For **non-HTML** artifacts (PNG/PDF/SVG): skip the iframe — copy into the folder
and embed natively with `![[<file>]]` (Obsidian renders these directly).

### Step 3 — Build the file:// URL

```bash
# URL-encode spaces only; keep slashes
FILE_URL="file://$(python3 -c "import sys,urllib.parse as u; print(u.quote(sys.argv[1]))" "$DEST/<Slug>.html")"
```

### Step 4 — Write/refresh the `.md` wrapper

Path: `$DEST/<Slug>.md`. Use this skeleton. **Always include the three layers**
(embed → native Mermaid fallback → browser fallback link) so the note renders
regardless of the reader's iframe settings.

````markdown
---
type: dashboard
project: <Project>
date: <YYYY-MM-DD>
rev: <n>            # bump on each latest-mode refresh
source: <where the data came from>
---

# <Title>

> [!info] What this is
> <1–2 line description>

## Interactive dashboard (embedded)

<iframe
  src="<FILE_URL>"
  style="width:100%; height:1400px; border:1px solid #2a3340; border-radius:12px; background:#0f1216;"
  sandbox="allow-same-origin allow-scripts allow-popups allow-popups-to-escape-sandbox">
</iframe>

> [!tip] If the embed is blank
> Obsidian renders iframes in **Reading view** only, and only with an
> **absolute `file://` path** (the src above is absolute). If your install still
> blocks it, open directly: [Open in browser](<FILE_URL>). The native diagrams
> below always render.

## Diagrams (native Mermaid)

```mermaid
<paste the artifact's flow/gantt as Mermaid — author from the artifact's content
so the note is useful even with no iframe. Omit this section only if the
artifact genuinely has no diagram.>
```

## Source / links
- <markdown links to the underlying docs, if any>

## Related
- <[[Projects/.../index]] cross-links — VERIFY each target exists before linking>
````

Rules:
- **Reading view only** — note in the tip; the iframe/Mermaid don't render in
  source/live-preview reliably.
- **Verify cross-link targets exist** (`ls`/glob) before writing `[[ ]]` links —
  don't create broken links (mirror `reference_obsidian_sram` conventions:
  frontmatter, MOC contents for long notes).
- **Refresh, don't clobber** — in latest mode, if the wrapper exists, update the
  iframe + Mermaid + bump `rev:`, but preserve any human-added prose sections.

### Step 5 — Confirm

Print: html path, md path, mode, and rev. Remind to open in **Reading view**.

```
Embedded → Projects/PD-Milestones/PD-Milestones-Map.{html,md} (latest, rev 2). Open in Reading view.
```

---

## Edge cases

- **Vault/dir missing** → STOP; don't write elsewhere.
- **Blank embed** → Reading view? absolute `file://`? Both covered above; Mermaid
  fallback guarantees content.
- **Multiple artifacts this session** → embed the latest unless user said "log
  all"; then embed each (timestamped).
- **Artifact lives outside the vault** (e.g. `~/foo.html`) → copy into the vault;
  the canonical copy lives in the project folder, not the original location.

---

## How this fits the loop

- **Write text:** `/log-session` → `vault/Sessions/`
- **Embed deliverables:** this skill → `vault/Projects/<Project>/`
- **Read back:** `/recall`, on-load hook

`/log-session` and `/wrap-up` call this skill when a session produced an HTML or
visual artifact (latest version by default; all versions if the user said "log
all"). The session log then records `artifact updated: [[<Slug>]] (rev N)`.
