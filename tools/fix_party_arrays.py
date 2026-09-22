#!/usr/bin/env python3
"""Normalise party_pop_array values in patches/history_countries to sum to 1.0.

The audit (H-04) found 13 countries whose party shares summed to 0.85-0.97.
The fix keeps the relative shares and reapportions the missing/double share
proportionally, then lands the rounding remainder on the largest party.

Usage:
    python tools/fix_party_arrays.py [--apply] [--tolerance 0.02]
"""
import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import rebase  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--tolerance", type=float, default=0.02)
    args = ap.parse_args()

    root = os.path.join(REPO, "patches", "history_countries")
    fixed = 0
    for fn in sorted(os.listdir(root)):
        if not fn.endswith(".txt"):
            continue
        path = os.path.join(root, fn)
        text = rebase.read(path)
        matches = list(re.finditer(r"(?m)^(\s*)set_variable = \{ party_pop_array\^(\d+) = ([0-9.]+) \}", text))
        if not matches:
            continue
        vals = {int(m.group(2)): float(m.group(3)) for m in matches}
        total = sum(vals.values())
        if abs(total - 1.0) <= args.tolerance:
            continue
        scale = 1.0 / total
        new = {k: round(v * scale, 3) for k, v in vals.items()}
        # put the rounding remainder on the largest party
        biggest = max(new, key=lambda k: new[k])
        new[biggest] = round(new[biggest] + (1.0 - sum(new.values())), 3)
        out = text
        for m in reversed(matches):
            idx = int(m.group(2))
            if new[idx] != float(m.group(3)):
                out = out[:m.start(3)] + f"{new[idx]:.3f}" + out[m.end(3):]
        if out != text:
            print(f"{fn[:3]}: {total:.3f} -> {sum(new.values()):.3f} "
                  f"({len(matches)} parties, largest = index {biggest})")
            if args.apply:
                rebase.write(path, out)
            fixed += 1
    print(f"{fixed} files" + ("" if args.apply else "  (dry-run, use --apply)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
