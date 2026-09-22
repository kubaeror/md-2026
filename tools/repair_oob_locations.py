#!/usr/bin/env python3
"""One-off repair: restore 'division = {' prefixes dropped by fix_oob_locations.py."""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import rebase  # noqa: E402

OOB = os.path.join(rebase.REPO, "history", "units")
fixed = 0
for fn in sorted(os.listdir(OOB)):
    if not fn.endswith("_2026_nsb.txt"):
        continue
    p = os.path.join(OOB, fn)
    text = rebase.read(p)
    lines = text.split("\n")
    hit = False
    for i, line in enumerate(lines):
        if line.strip() == "{" and i + 1 < len(lines) and re.match(r'^\t\tname\s*=\s*"', lines[i + 1]):
            lines[i] = "\tdivision = {"
            hit = True
            fixed += 1
    if hit:
        rebase.write(p, "\n".join(lines))
print(f"repaired {fixed} division blocks")
