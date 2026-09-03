#!/usr/bin/env python3
"""Run the backup examples from problem_solving.md against a throwaway directory.

Extracts each ```python block from the chapter, rewrites the `source` and
`target_dir` paths to point at a temporary tree, and executes it. Version 3 is
expected to fail with a SyntaxError - that is the chapter's debugging lesson -
so it is checked for exactly that.

Run from the repo root:  uv run check_examples.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
CHAPTER = ROOT / "problem_solving.md"
BLOCK = re.compile(r"```python\n(.*?)```", re.S)
# Version 3 in the chapter is deliberately broken.
EXPECT_SYNTAX_ERROR = {3}


def build_tree(work):
    """Create the notes/ tree the examples pretend to back up."""
    notes = work / "notes"
    notes.mkdir()
    for name in ("blah1.txt", "blah2.txt", "blah3.txt"):
        (notes / name).write_text("some notes\n")
    return notes


def main():
    blocks = BLOCK.findall(CHAPTER.read_text(encoding="utf-8"))
    backups = [b for b in blocks if "zipfile.ZipFile" in b or "os.system" in b]
    if not backups:
        print("No backup examples found - has the chapter changed?")
        return 1

    failures = 0
    for index, code in enumerate(backups, start=1):
        work = Path(tempfile.mkdtemp(prefix=f"backup_ver{index}_"))
        notes = build_tree(work)

        # Point the example at our temporary tree instead of /Users/swa.
        code = code.replace("['/Users/swa/notes']", f"[{str(notes)!r}]")
        code = code.replace("'/Users/swa/backup'", repr(str(work / "backup")))

        script = work / f"backup_ver{index}.py"
        script.write_text(code, encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(script)],
            input="added new examples\n",
            capture_output=True,
            text=True,
            timeout=60,
        )

        expect_failure = index in EXPECT_SYNTAX_ERROR
        broke = result.returncode != 0
        syntax = "SyntaxError" in result.stderr

        if expect_failure and broke and syntax:
            status = "OK (fails with SyntaxError, as the chapter intends)"
        elif expect_failure:
            status = "WRONG - this version is supposed to raise a SyntaxError"
            failures += 1
        elif broke:
            status = f"FAILED\n{result.stderr.strip()}"
            failures += 1
        else:
            archives = list((work / "backup").rglob("*.zip"))
            if archives:
                status = f"OK (wrote {archives[0].name})"
            else:
                status = "FAILED - ran cleanly but produced no archive"
                failures += 1

        print(f"version {index}: {status}")
        shutil.rmtree(work)

    print(f"\n{len(backups)} example(s) checked, {failures} problem(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
