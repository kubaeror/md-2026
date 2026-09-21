#!/usr/bin/env python3
"""Verify a Polish translation part against the English source range.

Usage:
    python tools/check_pl_part.py <start-line> <end-line> <part-file>

The part file must contain exactly the keys of the English range (same order),
translated, with no localisation header.
"""

import re
import sys

EN = r"C:\Users\kubak\md-2026\localisation\english\md2026_l_english.yml"
KEY_RE = re.compile(r"^\s*([A-Za-z0-9_\.]+):(\d*)\s")


def keys_in(lines):
    out = []
    for line in lines:
        m = KEY_RE.match(line)
        if m:
            out.append(m.group(1))
    return out


def main():
    start, end, part = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    with open(EN, encoding="utf-8-sig") as f:
        en_lines = f.read().split("\n")[start - 1:end]
    try:
        with open(part, encoding="utf-8-sig") as f:
            pl_lines = f.read().split("\n")
    except FileNotFoundError:
        print(f"BRAK PLIKU: {part}")
        return 1

    en_keys = keys_in(en_lines)
    pl_keys = keys_in(pl_lines)
    missing = [k for k in en_keys if k not in set(pl_keys)]
    extra = [k for k in pl_keys if k not in set(en_keys)]
    print(f"EN keys: {len(en_keys)}  PL keys: {len(pl_keys)}")
    for k in missing:
        print(f"  BRAK:    {k}")
    for k in extra:
        print(f"  ZBEDNY:  {k}")
    if pl_keys != en_keys:
        for i, (a, b) in enumerate(zip(en_keys, pl_keys)):
            if a != b:
                print(f"  KOLEJNOSC: pozycja {i + 1}: EN {a} <> PL {b}")
                break
    untranslated = [l for l in pl_lines
                    if KEY_RE.match(l) and l.strip().endswith('"') is False]
    if untranslated:
        print(f"  UWAGA: {len(untranslated)} linii bez domkniecia cudzyslowu")
    ok = not missing and not extra
    print("OK" if ok else "BLAD")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
