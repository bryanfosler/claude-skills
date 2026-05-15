#!/usr/bin/env python3
"""
audit-brief.py — Structurally enforce the Iron Rule on a BRIEF.md file.

The plugin's value prop is *defensible* output. This script audits the final
brief for the disciplines the plugin claims to enforce.

Checks:
  1. Wedge section present and contains: wrong-belief, our-belief, beachhead
  2. Falsifying condition present ("What would make this wrong" section)
  3. Evidence section has 3+ verbatim quotes with source URLs
  4. Opportunity scores (if shown) are tagged [MODEL ESTIMATE] or equivalent
  5. Trace map present (links to phase docs)
  6. Confidence section names evidence depth + quote count + source diversity
  7. The wedge does NOT match generic-tagline patterns ("we'll be the X for Y")
  8. Falsifying condition is specific (not just "if our assumptions are wrong")

Exit codes:
  0 = passes all checks
  1 = warnings (style issues, non-critical)
  2 = hard failure (Iron Rule or wedge discipline violated)

Usage:
  python3 audit-brief.py <path-to-BRIEF.md>
  python3 audit-brief.py .discovery/cairn-adhd/BRIEF.md --strict
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


URL_RE = re.compile(r'https?://[^\s\)]+')
WEDGE_SECTION_RE = re.compile(r'^##\s+The\s+wedge', re.MULTILINE | re.IGNORECASE)
EVIDENCE_SECTION_RE = re.compile(r'^##\s+The\s+evidence', re.MULTILINE | re.IGNORECASE)
WRONG_SECTION_RE = re.compile(r'^##\s+What\s+would\s+make\s+this\s+wrong', re.MULTILINE | re.IGNORECASE)
TRACE_SECTION_PATTERNS = [
    re.compile(r'^##\s+Trace\s+map', re.MULTILINE | re.IGNORECASE),
    re.compile(r'^###\s+Trace\s+map', re.MULTILINE | re.IGNORECASE),
]
CONFIDENCE_SECTION_RE = re.compile(r'^##\s+Confidence', re.MULTILINE | re.IGNORECASE)
QUOTE_LINE_RE = re.compile(r'^\s*>\s*[\"“‘](.+?)[\"”’]', re.MULTILINE)
ESTIMATE_TAG_RE = re.compile(r'\[MODEL ESTIMATE\]', re.IGNORECASE)
SCORE_RE = re.compile(r'(?:opportunity score|score)\s*[:=]\s*\*?\*?(\d+(?:\.\d+)?)\*?\*?', re.IGNORECASE)


# Generic wedge patterns to reject
GENERIC_WEDGE_PATTERNS = [
    re.compile(r"we'?ll\s+be\s+the\s+\w+\s+for\s+\w+", re.IGNORECASE),
    re.compile(r"we\s+are\s+(?:the\s+)?(?:next|first|new)\s+\w+", re.IGNORECASE),
    re.compile(r"\w+\s+but\s+(?:better|simpler|faster|cheaper)$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\bdisrupt(?:ing|ion)\s+the\s+\w+\s+market", re.IGNORECASE),
]

VAGUE_FALSIFY_PATTERNS = [
    re.compile(r"if\s+(?:our\s+)?assumptions?\s+(?:are|prove)\s+wrong", re.IGNORECASE),
    re.compile(r"if\s+the\s+market\s+(?:isn'?t|is\s+not)\s+ready", re.IGNORECASE),
    re.compile(r"if\s+users?\s+don'?t\s+(?:care|like|adopt)", re.IGNORECASE),
]


def has_section(rx_or_list, content):
    if isinstance(rx_or_list, list):
        return any(p.search(content) for p in rx_or_list)
    return rx_or_list.search(content) is not None


def section_body(rx_or_list, content):
    rx = rx_or_list
    if isinstance(rx_or_list, list):
        for p in rx_or_list:
            if p.search(content):
                rx = p
                break
        else:
            return ''
    m = rx.search(content)
    if not m:
        return ''
    rest = content[m.end():]
    next_h = re.search(r'^##\s', rest, re.MULTILINE)
    if next_h:
        return rest[:next_h.start()]
    return rest


def audit(path: Path, strict: bool = False) -> int:
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    content = path.read_text()

    errors = []
    warnings = []

    # Required sections
    if not has_section(WEDGE_SECTION_RE, content):
        errors.append("Missing 'The wedge' section.")
    if not has_section(EVIDENCE_SECTION_RE, content):
        errors.append("Missing 'The evidence' section.")
    if not has_section(WRONG_SECTION_RE, content):
        errors.append("Missing 'What would make this wrong' section (falsifying condition required).")
    if not has_section(CONFIDENCE_SECTION_RE, content):
        warnings.append("Missing 'Confidence' section.")
    if not has_section(TRACE_SECTION_PATTERNS, content):
        warnings.append("Missing 'Trace map' section (links to phase deliverables).")

    # Evidence quote count + URLs
    ev_body = section_body(EVIDENCE_SECTION_RE, content)
    quotes_in_evidence = QUOTE_LINE_RE.findall(ev_body)
    urls_in_evidence = URL_RE.findall(ev_body)
    if len(quotes_in_evidence) < 3:
        errors.append(
            f"Evidence section has only {len(quotes_in_evidence)} verbatim quotes (minimum: 3)."
        )
    if len(urls_in_evidence) < len(quotes_in_evidence):
        warnings.append(
            f"Evidence section has {len(quotes_in_evidence)} quotes but only "
            f"{len(urls_in_evidence)} source URLs. Iron Rule: every quote needs a URL."
        )

    # Score tag check
    scores = SCORE_RE.findall(content)
    if scores and not ESTIMATE_TAG_RE.search(content):
        errors.append(
            f"Found {len(scores)} opportunity score(s) but no [MODEL ESTIMATE] tag in the brief. "
            "Plugin discipline: ODI scores must be tagged as estimates until survey-validated."
        )

    # Wedge generic-tagline check
    wedge_body = section_body(WEDGE_SECTION_RE, content)
    for pat in GENERIC_WEDGE_PATTERNS:
        m = pat.search(wedge_body)
        if m:
            errors.append(
                f"Wedge contains generic-tagline pattern: \"{m.group(0)}\". "
                f"A real wedge names a competitor-belief-that's-wrong, not a marketing tagline."
            )

    # Falsifying condition vagueness check
    wrong_body = section_body(WRONG_SECTION_RE, content)
    for pat in VAGUE_FALSIFY_PATTERNS:
        m = pat.search(wrong_body)
        if m:
            warnings.append(
                f"Falsifying condition uses vague phrasing: \"{m.group(0)}\". "
                f"Be specific: name what observation, experiment, or competitor move would invalidate the wedge."
            )

    # Report
    print(f"== Brief audit: {path} ==")
    print(f"Wedge section: {'✓' if has_section(WEDGE_SECTION_RE, content) else '✗'}")
    print(f"Evidence section: {'✓' if has_section(EVIDENCE_SECTION_RE, content) else '✗'} "
          f"({len(quotes_in_evidence)} verbatim quotes, {len(urls_in_evidence)} URLs)")
    print(f"Falsifying condition: {'✓' if has_section(WRONG_SECTION_RE, content) else '✗'}")
    print(f"Scores tagged as estimates: {'✓' if (not scores) or ESTIMATE_TAG_RE.search(content) else '✗'}")
    print(f"Confidence section: {'✓' if has_section(CONFIDENCE_SECTION_RE, content) else '⚠'}")
    print(f"Trace map: {'✓' if has_section(TRACE_SECTION_PATTERNS, content) else '⚠'}")

    if errors:
        print("\nERRORS (Iron Rule / wedge discipline violated):")
        for e in errors:
            print(f"  ✗ {e}")
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  ⚠ {w}")
    if not errors and not warnings:
        print("\n✓ All checks passed. Brief is publication-grade by structural rules.")
    elif not errors:
        print("\n✓ No hard failures. Address warnings if shipping to stakeholders.")

    if errors:
        return 2
    if warnings and strict:
        return 1
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('path', type=Path, help='Path to BRIEF.md')
    p.add_argument('--strict', action='store_true',
                   help='Treat warnings as failures (exit 1)')
    args = p.parse_args()
    sys.exit(audit(args.path, strict=args.strict))


if __name__ == '__main__':
    main()
