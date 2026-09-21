#!/usr/bin/env python3
"""Align air-wing equipment tiers in our OOB files with the aircraft they name.

The equipment names in ``history/units/*`` are valid MD 2.0 names, but the tier
digits were carried over from MD 1.x: an air wing labelled "F-35A Lightning II"
could still field a 1995-tier airframe.  This tool reads the ``version_name`` of
every air wing, classifies it by generation and re-points the equipment to the
concrete MD 2.0 equipment of the same archetype whose ``year`` is closest to the
target year (2025 for 5th gen, 2015 for 4th gen, 1975 for older types).

Usage:
    python tools/fix_oob_tiers.py [--apply] [--md PATH]
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rebase  # noqa: E402
from fix_oob_equipment import equipment_definitions  # noqa: E402

OOB_DIR = os.path.join(rebase.REPO, "history", "units")

MODERN = ("F-35", "F-22", "Su-57", "Su-75", "J-20", "J-35", "KF-21", "F-15EX")
FOURTH = ("F-16", "F-15", "F-18", "Rafale", "Typhoon", "Gripen", "MiG-29", "Su-27", "Su-30",
          "Su-34", "Su-35", "Mirage 2000", "F-2", "J-10", "J-11", "J-15", "J-16", "FA-50",
          "Tejas", "Kfir", "F-20", "JF-17", "LCA")
OLD = ("MiG-21", "MiG-23", "MiG-27", "MiG-19", "MiG-17", "F-4 ", "F-4D", "F-4E", "F-5",
       "Su-22", "Su-24", "Su-25", "Mirage III", "Mirage 5", "J-7", "J-6", "A-4", "F-104",
       "Hunter", "Lightning", "Canberra", "MiG-15")

TARGET_YEAR = {"modern": 2025, "fourth": 2015, "old": 1975}


def classify(label):
    for k in MODERN:
        if k.lower() in label.lower():
            return "modern"
    for k in FOURTH:
        if k.lower() in label.lower():
            return "fourth"
    for k in OLD:
        if k.lower() in label.lower():
            return "old"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--md", default=os.environ.get("MD_PATH", rebase.DEFAULT_MD))
    args = ap.parse_args()

    defs = equipment_definitions(args.md)
    by_arch = {}
    for name, (arch, year) in defs.items():
        if arch:
            by_arch.setdefault(arch, []).append((name, year))
    for arch in by_arch:
        by_arch[arch].sort(key=lambda nf: nf[1])

    def pick(arch, target):
        if arch not in by_arch:
            return None
        return min(by_arch[arch], key=lambda nf: abs(nf[1] - target))[0]

    def pick_newest(arch, max_year=2026):
        if arch not in by_arch:
            return None
        cands = [nf for nf in by_arch[arch] if nf[1] <= max_year]
        return max(cands, key=lambda nf: nf[1])[0] if cands else None

    total = 0
    for fn in sorted(os.listdir(OOB_DIR)):
        if not fn.endswith(".txt"):
            continue
        path = os.path.join(OOB_DIR, fn)
        text = rebase.read(path)
        changed = []

        def sub(m):
            name, body = m.group(1), m.group(0)
            vm = re.search(r'version_name\s*=\s*"([^"]+)"', body)
            if not vm:
                return body
            kind = classify(vm.group(1))
            if kind != "modern":
                return body  # only upgrade clearly 5th-generation airframes
            arch = defs.get(name, (None, 0))[0]
            new = pick_newest(arch) if arch else None
            if not new or new == name:
                return body
            changed.append((vm.group(1), name, new))
            return body.replace(name + " = {", new + " = {", 1)

        text2 = re.sub(r"(?m)^[ \t]*([A-Za-z_][A-Za-z0-9_]*)[ \t]*=[ \t]*\{[^\n]*version_name[^\n]*\}", sub, text)
        if changed:
            total += len(changed)
            print(f"  {fn}: {len(changed)} zmian")
            for label, old, new in changed[:3]:
                print(f"      {label[:34]:36} {old:34} -> {new}")
            if args.apply:
                rebase.write(path, text2)
    print(f"razem: {total}" + ("" if args.apply else "  (dry-run, uzyj --apply)"))


if __name__ == "__main__":
    main()
