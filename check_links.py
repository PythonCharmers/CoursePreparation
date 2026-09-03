#!/usr/bin/env python3
"""Check internal cross-references in the course notes.

Verifies that every `file.md#anchor` link points at a file that exists and at an
anchor actually defined in that file, either as an explicit `<a id="...">` tag
or as a heading GitBook would slugify to that name.

Run from the repo root:  uv run check_links.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
EXPLICIT_ANCHOR = re.compile(r'<a\s+id="([^"]+)"')
HEADING = re.compile(r"^#+\s+(.*)$", re.MULTILINE)
# Trailing {#custom-id} syntax, as used by the upstream book.
HEADING_ID = re.compile(r"\{#([^}]+)\}\s*$")


def slugify(heading):
    """Approximate GitBook/Honkit heading -> anchor conversion."""
    text = re.sub(r"<a\s+id=\"[^\"]+\"\s*>\s*</a>", "", heading)
    text = HEADING_ID.sub("", text)
    text = re.sub(r"[`*_\\]", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s]+", "-", text).strip("-")


def anchors_in(path):
    """All anchor names that a link into this file could legitimately target."""
    text = path.read_text(encoding="utf-8")
    found = set(EXPLICIT_ANCHOR.findall(text))
    for heading in HEADING.findall(text):
        match = HEADING_ID.search(heading)
        if match:
            found.add(match.group(1))
        found.add(slugify(heading))
    return found


def main():
    md_files = sorted(ROOT.glob("*.md"))
    anchor_cache = {p.name: anchors_in(p) for p in md_files}
    problems = []

    for path in md_files:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for target in LINK.findall(line):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                filename, _, anchor = target.partition("#")
                filename = filename or path.name
                if not filename.endswith(".md"):
                    continue  # images and other assets
                if filename not in anchor_cache:
                    problems.append(f"{path.name}:{lineno}: missing file {filename}")
                elif anchor and anchor not in anchor_cache[filename]:
                    problems.append(
                        f"{path.name}:{lineno}: no anchor #{anchor} in {filename}"
                    )

    for problem in problems:
        print(problem)
    print(f"\n{len(problems)} broken internal link(s) across {len(md_files)} files.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
