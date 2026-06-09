#!/usr/bin/env python3
"""Analyze a project directory and emit structured facts for scaffold-claude-md.

Usage:
    python3 project_analyzer.py /path/to/project

Outputs JSON with detected stack, git remote, build commands, and layout.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def detect_stack(root: Path) -> dict:
    """Return a dict describing the detected stack (language, frameworks)."""
    markers = {
        "node": root / "package.json",
        "python_pyproject": root / "pyproject.toml",
        "python_requirements": root / "requirements.txt",
        "rust": root / "Cargo.toml",
        "swift_spm": root / "Package.swift",
        "xcode": next(root.glob("*.xcodeproj"), None),
        "go": root / "go.mod",
        "make": root / "Makefile",
    }
    detected = {}
    for name, path in markers.items():
        if path and path.exists():
            detected[name] = str(path.relative_to(root))

    # Frameworks from package.json
    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text())
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            detected["node_frameworks"] = sorted(
                fw for fw in ["react", "next", "vue", "svelte", "express", "fastify", "vite", "typescript"]
                if fw in deps
            )
            detected["node_scripts"] = list(data.get("scripts", {}).keys())
        except Exception:
            pass
    return detected


def git_remote(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            # Convert SSH to owner/repo short form
            m = re.search(r"[:/]([^/:]+/[^/.]+?)(?:\.git)?$", url)
            return m.group(1) if m else url
    except Exception:
        pass
    return None


def top_level_layout(root: Path, max_entries: int = 12) -> list[dict]:
    """Return top-level dirs and key files, ignoring noise."""
    ignore = {".git", "node_modules", "dist", "build", ".next", "__pycache__",
              ".pytest_cache", ".venv", "venv", ".DS_Store", ".cache"}
    entries = []
    for p in sorted(root.iterdir()):
        if p.name in ignore or p.name.startswith("."):
            continue
        entries.append({
            "name": p.name,
            "type": "dir" if p.is_dir() else "file",
        })
        if len(entries) >= max_entries:
            break
    return entries


def detect_commands(stack: dict, root: Path) -> dict:
    """Best-guess build / run / test commands."""
    cmds = {}
    if "node" in stack:
        scripts = stack.get("node_scripts", [])
        if "build" in scripts:
            cmds["build"] = "npm run build"
        if "dev" in scripts:
            cmds["run"] = "npm run dev"
        elif "start" in scripts:
            cmds["run"] = "npm start"
        if "test" in scripts:
            cmds["test"] = "npm test"
    if "python_pyproject" in stack or "python_requirements" in stack:
        if (root / "main.py").exists():
            cmds.setdefault("run", "python3 main.py")
        if (root / "tests").is_dir() or (root / "test").is_dir():
            cmds.setdefault("test", "pytest")
    if "rust" in stack:
        cmds["build"] = "cargo build"
        cmds["run"] = "cargo run"
        cmds["test"] = "cargo test"
    if "swift_spm" in stack:
        cmds["build"] = "swift build"
        cmds["test"] = "swift test"
    if "make" in stack:
        cmds.setdefault("build", "make")
    return cmds


def detect_hardware_signals(root: Path) -> list[str]:
    """Look for files that suggest physical hardware involvement."""
    signals = []
    for name in ["pins.md", "wiring.md", "BOM.md", "bom.md", "hardware.md", "schematic.pdf"]:
        if (root / name).exists():
            signals.append(name)
    for pattern in ["**/*.kicad_*", "**/*.fzz", "**/STL/*.stl"]:
        if any(root.glob(pattern)):
            signals.append(pattern)
    return signals


def detect_env_vars(root: Path) -> list[str]:
    """Find referenced env var names in code, capped to first 20 unique."""
    env_vars = set()
    extensions = [".py", ".ts", ".js", ".tsx", ".jsx", ".swift", ".rs", ".go"]
    for ext in extensions:
        for path in root.rglob(f"*{ext}"):
            if any(p in path.parts for p in ["node_modules", "dist", "build", ".git"]):
                continue
            try:
                content = path.read_text(errors="ignore")
            except Exception:
                continue
            env_vars.update(re.findall(r"(?:process\.env|os\.environ\.get|os\.getenv)\(?\.?['\"]?([A-Z_][A-Z0-9_]+)", content))
            if len(env_vars) >= 20:
                break
    return sorted(env_vars)[:20]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: project_analyzer.py <project-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).expanduser().resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 1

    stack = detect_stack(root)
    report = {
        "project_name": root.name,
        "local_path": str(root),
        "git_remote": git_remote(root),
        "stack": stack,
        "commands": detect_commands(stack, root),
        "layout": top_level_layout(root),
        "hardware_signals": detect_hardware_signals(root),
        "env_vars": detect_env_vars(root),
        "has_readme": (root / "README.md").exists(),
        "has_claude_md": (root / "CLAUDE.md").exists(),
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
