#!/usr/bin/env python3
"""Remove GitBook's backslash escaping from the markdown.

GitBook's exporter escaped parentheses, brackets and similar characters in
prose - `\\(like this\\)`. Standard markdown parsers such as the one MkDocs
uses do not need the escaping and render the backslash literally, so it has to
come out before the notes are built with anything else.

Only prose is touched. Fenced code blocks and inline code spans are left
exactly as they are, because a backslash inside them is real content - the line
continuations and `'\\n'` escapes in the examples depend on it.

Run from the repo root:  uv run unescape_gitbook.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent / "docs"

# The characters GitBook escaped that plain markdown is happy to see bare.
ESCAPED = re.compile(r"\\([()\[\]#_>|+.!-])")
FENCE = re.compile(r"^(\s*)(```|~~~)")
INLINE_CODE = re.compile(r"(`+)(.*?)\1", re.S)


def unescape_prose(text):
    """Strip escaping outside inline code spans."""
    pieces = []
    last = 0
    for match in INLINE_CODE.finditer(text):
        pieces.append(ESCAPED.sub(r"\1", text[last:match.start()]))
        pieces.append(match.group(0))  # leave code spans untouched
        last = match.end()
    pieces.append(ESCAPED.sub(r"\1", text[last:]))
    return "".join(pieces)


def process(text):
    """Unescape prose lines, skipping fenced code blocks entirely."""
    out = []
    in_fence = False
    fence_marker = None

    for line in text.splitlines(keepends=True):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(2)
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker == fence_marker:
                in_fence, fence_marker = False, None
            out.append(line)
            continue

        out.append(line if in_fence else unescape_prose(line))

    return "".join(out)


def main():
    changed = 0
    for path in sorted(ROOT.glob("*.md")):
        original = path.read_text(encoding="utf-8")
        updated = process(original)
        if updated == original:
            continue
        removed = len(ESCAPED.findall(original)) - len(ESCAPED.findall(updated))
        path.write_text(updated, encoding="utf-8")
        print(f"{path.name}: removed {removed} escape(s)")
        changed += 1

    print(f"\n{changed} file(s) updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
