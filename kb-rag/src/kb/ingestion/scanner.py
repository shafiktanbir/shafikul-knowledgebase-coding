"""Markdown scanner — walks the knowledge base directory and finds .md files.

Respects the exclude_patterns from config.
Returns a list of relative paths (relative to the KB root).
"""

from __future__ import annotations

import fnmatch
from pathlib import Path


def scan_markdown_files(
    kb_root: Path,
    exclude_patterns: list[str] | None = None,
) -> list[Path]:
    """Walk kb_root recursively, return paths to all .md files.

    Args:
        kb_root: Absolute path to the knowledge base root directory.
        exclude_patterns: Glob patterns (relative to kb_root) to exclude.

    Returns:
        List of absolute Paths to .md files, sorted alphabetically.
    """
    exclude_patterns = exclude_patterns or []
    found: list[Path] = []

    for path in sorted(kb_root.rglob("*.md")):
        if not path.is_file():
            continue

        rel = path.relative_to(kb_root)
        rel_str = str(rel).replace("\\", "/")  # normalise on Windows too

        if _is_excluded(rel_str, exclude_patterns):
            continue

        found.append(path)

    return found


def _is_excluded(rel_path: str, patterns: list[str]) -> bool:
    """Return True if the relative path matches any exclude pattern."""
    for pattern in patterns:
        # Match against full path and filename
        if fnmatch.fnmatch(rel_path, pattern):
            return True
        # Also check if any path component matches a simple pattern
        if fnmatch.fnmatch(rel_path.split("/")[0] + "/", pattern.split("/")[0] + "/"):
            if "**" in pattern:
                return True
    return False
