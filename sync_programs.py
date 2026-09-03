#!/usr/bin/env python3
"""Rewrite docs/programs/backup_ver*.{py,txt} from the chapter's code blocks.

The chapter and the standalone copies in docs/programs/ are the same programs
and the same expected output, so they have to agree. This regenerates the
standalone files from problem_solving.md, which is the version learners
actually read.

Only the backup examples are handled; the other programs in that directory have
not diverged.

Run from the repo root:  uv run sync_programs.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
CHAPTER = ROOT / "docs" / "problem_solving.md"
PROGRAMS = ROOT / "docs" / "programs"
CODE_BLOCK = re.compile(r"```python\n(.*?)```", re.S)
TEXT_BLOCK = re.compile(r"```text\n(.*?)```", re.S)


def write_if_changed(target, content):
    """Write the file only when it differs, and report what happened."""
    if not target.exists():
        print(f"{target.name}: missing, skipping")
        return
    if target.read_text(encoding="utf-8") == content:
        print(f"{target.name}: already up to date")
        return
    target.write_text(content, encoding="utf-8")
    print(f"{target.name}: updated from the chapter")


def main():
    chapter = CHAPTER.read_text(encoding="utf-8")

    code = [
        b for b in CODE_BLOCK.findall(chapter)
        if "zipfile.ZipFile" in b or "os.system" in b
    ]
    output = [
        b for b in TEXT_BLOCK.findall(chapter)
        if re.search(r"^\$ python backup_ver", b, re.M)
    ]

    if len(code) != 4 or len(output) != 4:
        print(
            f"Expected 4 programs and 4 outputs in the chapter, "
            f"found {len(code)} and {len(output)}."
        )
        return 1

    for index, (program, expected) in enumerate(zip(code, output), start=1):
        write_if_changed(PROGRAMS / f"backup_ver{index}.py", program)
        write_if_changed(PROGRAMS / f"backup_ver{index}.txt", expected)

    return 0


if __name__ == "__main__":
    sys.exit(main())
