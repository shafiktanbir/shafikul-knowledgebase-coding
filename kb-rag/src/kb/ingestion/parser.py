"""Markdown parser — reads a .md file and extracts structured sections.

Extracts:
- Front matter (YAML between --- delimiters) if present
- Section title hierarchy (# ## ### headings)
- Clean text content per section

Does NOT modify the source file.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Section:
    """A logical section of a Markdown document."""

    title: str           # The heading text (e.g. "PostgreSQL Indexing Strategies")
    level: int           # Heading level: 1=H1, 2=H2, 3=H3
    content: str         # Raw markdown text of this section
    heading_path: list[str] = field(default_factory=list)  # e.g. ["Overview", "Architecture"]


@dataclass
class ParsedDocument:
    """Fully parsed representation of a Markdown file."""

    source: str                          # relative path from KB root
    abs_path: Path                       # absolute path on disk
    file_hash: str                       # SHA-256 of raw file bytes
    front_matter: dict[str, Any]
    sections: list[Section]
    raw_text: str                        # full file content (source of truth)


_YAML_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def parse_document(abs_path: Path, kb_root: Path) -> ParsedDocument:
    """Parse a Markdown file into a ParsedDocument.

    Args:
        abs_path: Absolute path to the .md file.
        kb_root: KB root for computing the relative source path.

    Returns:
        ParsedDocument with sections and metadata extracted.
    """
    raw_bytes = abs_path.read_bytes()
    file_hash = hashlib.sha256(raw_bytes).hexdigest()
    raw_text = raw_bytes.decode("utf-8", errors="replace")

    source = str(abs_path.relative_to(kb_root)).replace("\\", "/")

    front_matter: dict[str, Any] = {}
    body = raw_text

    # Strip YAML front matter
    fm_match = _YAML_FRONT_MATTER_RE.match(raw_text)
    if fm_match:
        try:
            import yaml  # noqa: PLC0415
            front_matter = yaml.safe_load(fm_match.group(1)) or {}
        except Exception:  # noqa: BLE001
            pass
        body = raw_text[fm_match.end():]

    sections = _split_into_sections(body)

    return ParsedDocument(
        source=source,
        abs_path=abs_path,
        file_hash=file_hash,
        front_matter=front_matter,
        sections=sections,
        raw_text=raw_text,
    )


def _split_into_sections(body: str) -> list[Section]:
    """Split markdown body into logical sections at heading boundaries."""
    # Find all headings and their positions
    heading_positions: list[tuple[int, int, str]] = []  # (start, level, title)
    for m in _HEADING_RE.finditer(body):
        level = len(m.group(1))
        title = m.group(2).strip()
        heading_positions.append((m.start(), level, title))

    if not heading_positions:
        # No headings — treat entire document as one section
        content = body.strip()
        if content:
            return [Section(title="Document", level=1, content=content)]
        return []

    sections: list[Section] = []

    # Content before the first heading
    pre_content = body[: heading_positions[0][0]].strip()
    if pre_content:
        sections.append(Section(title="Introduction", level=1, content=pre_content))

    heading_stack: list[str] = []  # tracks heading hierarchy

    for i, (start, level, title) in enumerate(heading_positions):
        # Determine content end (next heading or end of document)
        if i + 1 < len(heading_positions):
            end = heading_positions[i + 1][0]
        else:
            end = len(body)

        # Get the raw block (includes the heading line itself)
        raw_block = body[start:end]
        # Content below the heading line
        heading_line_end = raw_block.index("\n") + 1 if "\n" in raw_block else len(raw_block)
        content = raw_block[heading_line_end:].strip()

        # Maintain heading stack for hierarchy context
        heading_stack = heading_stack[: level - 1]
        heading_stack.append(title)

        if content or True:  # Always include, even empty sections
            sections.append(
                Section(
                    title=title,
                    level=level,
                    content=content,
                    heading_path=list(heading_stack[:-1]),
                )
            )

    return sections
