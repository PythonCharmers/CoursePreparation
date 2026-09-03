#!/usr/bin/env python3
"""Check external URLs in the course notes for dead links.

Sends a HEAD request (falling back to GET, since some hosts reject HEAD) to every
http(s) URL in the markdown, and reports anything that does not come back OK.
Results are grouped by status so redirects and hard failures are easy to tell apart.

Run from the repo root:  uv run check_urls.py
"""
import concurrent.futures
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
URL = re.compile(r"https?://[^\s)\]\"'>]+")
TIMEOUT = 20
USER_AGENT = "Mozilla/5.0 (compatible; link-checker/1.0)"


def collect():
    """Map each URL to the 'file:line' locations that reference it."""
    found = defaultdict(list)
    for path in sorted(ROOT.glob("*.md")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for url in URL.findall(line):
                found[url.rstrip(".,;")].append(f"{path.name}:{lineno}")
    return found


def check(url):
    """Return (url, status) where status is an HTTP code or an error string."""
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(
            url, method=method, headers={"User-Agent": USER_AGENT}
        )
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                return url, response.status
        except urllib.error.HTTPError as exc:
            if method == "GET" or exc.code not in (403, 405, 501):
                return url, exc.code
        except Exception as exc:  # DNS failure, timeout, bad TLS, ...
            if method == "GET":
                return url, type(exc).__name__
    return url, "unknown"


def main():
    locations = collect()
    print(f"Checking {len(locations)} unique URLs...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        results = dict(pool.map(check, locations))

    broken = {u: s for u, s in results.items() if s != 200}
    for url, status in sorted(broken.items(), key=lambda kv: str(kv[1])):
        print(f"[{status}] {url}")
        for location in locations[url]:
            print(f"    {location}")

    print(f"\n{len(broken)} of {len(locations)} URLs did not return 200.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
