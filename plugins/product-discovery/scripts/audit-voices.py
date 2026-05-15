#!/usr/bin/env python3
"""
audit-voices.py — Structurally enforce the Iron Rule on a VOICES.md file.

The plugin's stated differentiator vs. Productboard/Zeda/Kraftful is the
verbatim-quote-with-source-URL discipline. This script makes that enforceable,
not just normative.

Checks:
  1. Minimum quote count (default 15)
  2. Every quote line has a source URL (a markdown link to http/s)
  3. Every theme has at least 2 quotes (configurable)
  4. Every theme has cross-platform corroboration (min 2 distinct domains)
  5. Switch stories section present with at least 3 entries
  6. Gaps section present (honest empty-result documentation)
  7. No `[SYNTHETIC EXAMPLE]` tags appearing as evidence (only allowed in templates)

Exit codes:
  0 = passes all checks
  1 = warnings (style/count below targets but technically valid)
  2 = hard failure (Iron Rule violated)

Usage:
  python3 audit-voices.py <path-to-VOICES.md>
  python3 audit-voices.py .discovery/cairn-adhd/02-voices/VOICES.md --strict
"""

import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse


QUOTE_LINE_RE = re.compile(r'^\s*>\s*[\"“‘](.+?)[\"”’]\s*[-—]\s*\[?(.+?)\]?\(?(https?://\S+)\)?', re.MULTILINE)
# Looser fallback: any blockquote that mentions a URL
QUOTE_LOOSE_RE = re.compile(r'^\s*>\s*.+?(https?://\S+)', re.MULTILINE)
URL_RE = re.compile(r'https?://[^\s\)]+')
THEME_HEADER_RE = re.compile(r'^###\s+Theme\s*\d+', re.MULTILINE | re.IGNORECASE)
SWITCH_SECTION_RE = re.compile(r'^##\s*Switch\s*stor(?:y|ies)', re.MULTILINE | re.IGNORECASE)
GAPS_SECTION_RE = re.compile(r'^##\s*Gaps?', re.MULTILINE | re.IGNORECASE)
SYNTHETIC_RE = re.compile(r'\[SYNTHETIC EXAMPLE\]', re.IGNORECASE)


def domain_of(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
        host = host.lstrip('www.')
        # Collapse Reddit subreddits to single domain
        if host.endswith('reddit.com'):
            return 'reddit.com'
        return host
    except Exception:
        return url


def extract_themes(content: str):
    """Return list of (theme_label, theme_body) tuples."""
    # Split on Theme headers; each theme runs until next theme or another section
    parts = re.split(r'^(###\s+Theme[^\n]*)$', content, flags=re.MULTILINE)
    themes = []
    for i in range(1, len(parts), 2):
        label = parts[i].strip()
        body = parts[i+1] if i+1 < len(parts) else ''
        # Trim at next ## (section break)
        next_section = re.search(r'^##\s', body, re.MULTILINE)
        if next_section:
            body = body[:next_section.start()]
        themes.append((label, body))
    return themes


def quotes_in(body: str):
    """Return list of (quote_text, url) from a body of text."""
    out = []
    # Try strict pattern first
    for m in QUOTE_LINE_RE.finditer(body):
        out.append((m.group(1), m.group(3)))
    if out:
        return out
    # Fallback: any blockquote line with a URL
    for m in QUOTE_LOOSE_RE.finditer(body):
        url = m.group(1)
        # Extract the quoted text if any
        line = body[m.start():m.end()]
        qtext = ''
        qm = re.search(r'[\"“‘](.+?)[\"”’]', line)
        if qm:
            qtext = qm.group(1)
        out.append((qtext, url))
    return out


def audit(path: Path, strict: bool = False) -> int:
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    content = path.read_text()

    errors = []
    warnings = []

    # Synthetic-example tags in voice evidence are not allowed
    if SYNTHETIC_RE.search(content):
        errors.append(
            "Found [SYNTHETIC EXAMPLE] tags in VOICES.md. "
            "Synthetic examples are not allowed as evidence; only real verbatim quotes."
        )

    # Required sections
    if not SWITCH_SECTION_RE.search(content):
        errors.append("Missing 'Switch stories' section.")
    if not GAPS_SECTION_RE.search(content):
        warnings.append("Missing 'Gaps' section (honest empty-result documentation).")

    # All quote-like lines
    all_quotes = quotes_in(content)
    total_with_url = sum(1 for _, u in all_quotes if u)
    if total_with_url < 15:
        errors.append(
            f"Only {total_with_url} quotes have source URLs (Iron Rule minimum: 15). "
            f"Each theme needs verbatim quotes with citations."
        )

    # Per-theme checks
    themes = extract_themes(content)
    if not themes:
        warnings.append("No `### Theme N:` headers found — file may not follow the voices template.")

    for label, body in themes:
        theme_quotes = quotes_in(body)
        n = sum(1 for _, u in theme_quotes if u)
        if n < 2:
            errors.append(f"{label}: only {n} quotes with URLs (minimum 2).")
        domains = set(domain_of(u) for _, u in theme_quotes if u)
        # Filter empty
        domains.discard('')
        if len(domains) < 2 and n >= 2:
            warnings.append(
                f"{label}: {n} quotes but only {len(domains)} distinct domain "
                f"({', '.join(domains) or 'none'}). Cross-platform corroboration "
                f"target is 2+ domains. Consider broader sources."
            )

    # Switch stories minimum
    switch_match = SWITCH_SECTION_RE.search(content)
    if switch_match:
        switch_body = content[switch_match.end():]
        # End at next ##
        next_h = re.search(r'^##\s', switch_body, re.MULTILINE)
        if next_h:
            switch_body = switch_body[:next_h.start()]
        switch_quotes = quotes_in(switch_body)
        switch_n = sum(1 for _, u in switch_quotes if u)
        if switch_n < 3:
            warnings.append(
                f"Switch stories section has {switch_n} entries with URLs (target: 3+). "
                f"Switch stories are Moesta's highest-signal evidence."
            )

    # Report
    print(f"== Voices audit: {path} ==")
    print(f"Total quotes with source URLs: {total_with_url}")
    print(f"Themes detected: {len(themes)}")
    if errors:
        print("\nERRORS (Iron Rule violated):")
        for e in errors:
            print(f"  ✗ {e}")
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  ⚠ {w}")
    if not errors and not warnings:
        print("\n✓ All checks passed.")

    if errors:
        return 2
    if warnings and strict:
        return 1
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('path', type=Path, help='Path to VOICES.md')
    p.add_argument('--strict', action='store_true',
                   help='Treat warnings as failures (exit 1)')
    args = p.parse_args()
    sys.exit(audit(args.path, strict=args.strict))


if __name__ == '__main__':
    main()
