#!/usr/bin/env python3
"""Memory lint - health check for an LLM memory wiki.

Inspired by Karpathy's LLM Wiki pattern (Ingest / Query / Lint).
Runs deterministic checks on a memory directory that holds an index file
(MEMORY.md) plus one topic file per fact.

Usage:
    python3 lint.py [memory-dir]

The memory directory is resolved in this order:
    1. the first CLI argument, if given
    2. the MEMORY_DIR environment variable
    3. ~/.claude/memory  (fallback default)

Exit code 0 = clean, 1 = warnings, 2 = errors.
"""

from __future__ import annotations

import os
import re
import sys
from collections import Counter
from pathlib import Path


def resolve_mem_dir() -> Path:
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = os.environ.get("MEMORY_DIR", "~/.claude/memory")
    return Path(raw).expanduser()


MEM_DIR = resolve_mem_dir()
INDEX = MEM_DIR / "MEMORY.md"
LINE_CAP = 200
INLINE_BLOAT_THRESHOLD = 4  # body lines under a heading before it should be its own file
VALID_TYPES = {"user", "feedback", "project", "reference"}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def parse_index(text: str) -> list[tuple[str, list[str]]]:
    """Return [(heading, body_lines), ...] for each ## section in MEMORY.md."""
    sections: list[tuple[str, list[str]]] = []
    current_heading: str | None = None
    current_body: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current_heading is not None:
                sections.append((current_heading, current_body))
            current_heading = line[3:].strip()
            current_body = []
        elif current_heading is not None:
            current_body.append(line)
    if current_heading is not None:
        sections.append((current_heading, current_body))
    return sections


POINTER_PATTERNS = [
    re.compile(r"^\s*[-*]\s+\[[^\]]+\]\(([a-zA-Z0-9_\-]+\.md)\)", re.MULTILINE),  # - [Title](file.md)
    re.compile(r"→\s*See\s+([a-zA-Z0-9_\-]+\.md)"),                                # → See file.md
]


def is_pointer_line(line: str) -> bool:
    """A line that is purely a pointer to a topic file or external reference."""
    s = line.strip()
    if not s:
        return False
    for pat in POINTER_PATTERNS:
        if pat.search(line):
            return True
    # External pointer style: "- Foo → `~/path/to/file.md` (external) — note"
    if s.startswith("-") and "→" in s and "(external)" in s.lower():
        return True
    return False


def referenced_files(text: str) -> set[str]:
    """Return file basenames that look like memory-wiki references.

    Matches:
      - `[Title](file.md)` markdown links
      - `→ See file.md` (legacy pointer style)
      - backticked `file.md` where the basename plausibly belongs to memory

    Skips obvious non-references: placeholder patterns (YYYY-MM-DD...),
    generic names like README.md, and any path with slashes.
    """
    refs: set[str] = set()
    for pat in POINTER_PATTERNS:
        refs |= set(pat.findall(text))
    for m in re.findall(r"`([a-zA-Z0-9_\-]+\.md)`", text):
        if m.upper() == "README.md".upper():
            continue
        if "YYYY" in m or "HHmm" in m or "MM-DD" in m:
            continue
        if re.match(r"^\d{4}-\d{2}-\d{2}", m):
            continue
        refs.add(m)
    return refs


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def main() -> int:
    if not INDEX.exists():
        print(f"ERROR: {INDEX} does not exist", file=sys.stderr)
        print("Set MEMORY_DIR or pass the memory directory as the first argument.", file=sys.stderr)
        return 2

    index_text = read(INDEX)
    index_lines = index_text.splitlines()
    sections = parse_index(index_text)
    refs = referenced_files(index_text)

    all_files = {p.name for p in MEM_DIR.glob("*.md") if p.name != "MEMORY.md"}

    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    # CHECK 1: line cap
    n_lines = len(index_lines)
    if n_lines > LINE_CAP:
        errors.append(
            f"MEMORY.md is {n_lines} lines (cap {LINE_CAP}). "
            f"Lines {LINE_CAP + 1}-{n_lines} truncate in context — "
            f"those entries are invisible unless mentioned by name."
        )
    elif n_lines > LINE_CAP * 0.9:
        warnings.append(f"MEMORY.md is {n_lines}/{LINE_CAP} lines ({n_lines/LINE_CAP:.0%}) — approaching cap.")
    else:
        info.append(f"MEMORY.md size OK: {n_lines}/{LINE_CAP} lines.")

    # CHECK 2: orphan files (in dir but not referenced from index)
    orphans = sorted(all_files - refs)
    if orphans:
        warnings.append(
            "Orphan files (exist on disk but not referenced in MEMORY.md):\n  - "
            + "\n  - ".join(orphans)
        )

    # CHECK 3: broken refs (referenced from index but don't exist on disk)
    broken = sorted(refs - all_files - {"MEMORY.md"})
    if broken:
        errors.append(
            "Broken references (mentioned in MEMORY.md but file missing):\n  - "
            + "\n  - ".join(broken)
        )

    # CHECK 4: bloated inline entries (sections with too many NON-pointer content lines)
    # An index section that holds N pointer bullets is fine; only flag actual content.
    bloated = []
    for heading, body in sections:
        non_pointer = [
            ln for ln in body
            if ln.strip() and not is_pointer_line(ln)
        ]
        if len(non_pointer) > INLINE_BLOAT_THRESHOLD:
            bloated.append((heading, len(non_pointer)))
    if bloated:
        warnings.append(
            f"Bloated inline entries (>{INLINE_BLOAT_THRESHOLD} body lines — should be extracted to topic files):\n  - "
            + "\n  - ".join(f"{h}  ({n} lines)" for h, n in bloated)
        )

    # CHECK 5: duplicate headings
    headings = [h for h, _ in sections]
    dupes = [h for h, c in Counter(headings).items() if c > 1]
    if dupes:
        errors.append("Duplicate headings in MEMORY.md:\n  - " + "\n  - ".join(dupes))

    # CHECK 6: empty headings (heading immediately followed by another heading or EOF)
    empty = [h for h, body in sections if not any(ln.strip() for ln in body)]
    if empty:
        warnings.append("Empty section headings:\n  - " + "\n  - ".join(empty))

    # CHECK 7: topic files missing or malformed frontmatter
    bad_fm = []
    bad_type = []
    for fname in sorted(all_files):
        text = read(MEM_DIR / fname)
        fm = parse_frontmatter(text)
        if fm is None:
            bad_fm.append(fname)
        else:
            t = fm.get("type", "")
            if t and t not in VALID_TYPES:
                bad_type.append(f"{fname}  (type={t!r})")
    if bad_fm:
        warnings.append(
            "Topic files missing YAML frontmatter:\n  - " + "\n  - ".join(bad_fm)
        )
    if bad_type:
        warnings.append(
            f"Topic files with non-standard type (expected {sorted(VALID_TYPES)}):\n  - "
            + "\n  - ".join(bad_type)
        )

    # CHECK 8: naming convention (legacy bare names vs. {type}_{topic}.md)
    legacy = [
        f for f in all_files
        if not any(f.startswith(f"{t}_") for t in VALID_TYPES)
    ]
    if legacy:
        info.append(
            "Files using legacy bare names (cosmetic — fine if indexed):\n  - "
            + "\n  - ".join(sorted(legacy))
        )

    # ── REPORT ──────────────────────────────────────────────────────
    print("=" * 60)
    print(f"MEMORY LINT — {MEM_DIR}")
    print("=" * 60)
    print(f"Index: {n_lines}/{LINE_CAP} lines, {len(sections)} sections")
    print(f"Topic files: {len(all_files)} on disk, {len(refs)} referenced")
    print()

    if errors:
        print(f"❌ ERRORS ({len(errors)}):")
        for e in errors:
            print(f"\n  • {e}")
        print()
    if warnings:
        print(f"⚠️  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"\n  • {w}")
        print()
    if info:
        print(f"ℹ️  INFO ({len(info)}):")
        for i in info:
            print(f"\n  • {i}")
        print()

    if not errors and not warnings:
        print("✅ Memory wiki is clean.")
        return 0
    if errors:
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
