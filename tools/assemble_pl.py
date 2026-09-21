#!/usr/bin/env python3
"""Assemble the Polish translation from its parts.

Reads the part files in order, checks that together they contain exactly the
keys of the English file (in the same order) and writes
localisation/polish/md2026_l_polish.yml with the l_polish: header and a BOM.

Usage:
    python tools/assemble_pl.py <part1> <part2> ...
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN = os.path.join(REPO, "localisation", "english", "md2026_l_english.yml")
OUT = os.path.join(REPO, "localisation", "polish", "md2026_l_polish.yml")
KEY_RE = re.compile(r"^\s*([A-Za-z0-9_\.]+):(\d*)\s")


def keys_in(lines):
    return [m.group(1) for m in (KEY_RE.match(l) for l in lines) if m]


def main():
    parts = sys.argv[1:]
    if not parts:
        sys.exit("usage: python tools/assemble_pl.py <part1> <part2> ...")

    with open(EN, encoding="utf-8-sig") as f:
        en_lines = f.read().split("\n")
    en_keys = keys_in(en_lines)

    body, pl_keys = [], []
    for p in parts:
        with open(p, encoding="utf-8-sig") as f:
            lines = [l.rstrip("\r") for l in f.read().split("\n")]
        # drop an accidental language header
        if lines and lines[0].strip().startswith("l_"):
            lines = lines[1:]
        body.extend(lines)
        pl_keys.extend(keys_in(lines))

    missing = [k for k in en_keys if k not in set(pl_keys)]
    extra = [k for k in pl_keys if k not in set(en_keys)]
    if missing or extra:
        print(f"BRAKUJACE: {len(missing)}")
        for k in missing[:20]:
            print(f"  {k}")
        print(f"ZBEDNE: {len(extra)}")
        for k in extra[:20]:
            print(f"  {k}")
        return 1

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    text = "l_polish:\n\n" + "\n".join(body).rstrip("\n") + "\n"
    with open(OUT, "w", encoding="utf-8-sig", newline="\n") as f:
        f.write(text)
    print(f"zapisano {os.path.relpath(OUT, REPO)} ({len(pl_keys)} kluczy)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
