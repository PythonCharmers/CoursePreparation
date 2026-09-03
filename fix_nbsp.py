#!/usr/bin/env python3
"""Replace non-breaking spaces (U+00A0) with ordinary spaces in the markdown.

Non-breaking spaces are invisible in most editors but break literal text
searches and can render oddly. They creep in when text is pasted from word
processors or web pages.

Run from the repo root:  uv run fix_nbsp.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent / "docs"
NBSP = " "


def main():
    changed = 0
    for path in sorted(ROOT.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if NBSP not in text:
            continue
        count = text.count(NBSP)
        path.write_text(text.replace(NBSP, " "), encoding="utf-8")
        print(f"{path.name}: replaced {count} non-breaking space(s)")
        changed += 1

    print(f"\n{changed} file(s) updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
