#!/usr/bin/env python3
"""Report which vanilla/MD OOB files combine units and air_wings (D-02 check)."""
import os
import re
import sys

VAN = r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
MD = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2777392649"

for label, root in (("vanilla", os.path.join(VAN, "history", "units")),
                    ("MD", os.path.join(MD, "history", "units"))):
    both, air_only, units_only = [], [], []
    for name in sorted(os.listdir(root)) if os.path.isdir(root) else []:
        if not name.endswith(".txt"):
            continue
        text = open(os.path.join(root, name), encoding="utf-8-sig", errors="replace").read()
        has_units = bool(re.search(r"(?m)^\s*units\s*=\s*\{", text))
        has_air = bool(re.search(r"(?m)^\s*air_wings\s*=\s*\{", text))
        if has_units and has_air:
            both.append(name)
        elif has_air:
            air_only.append(name)
        elif has_units:
            units_only.append(name)
    print(f"{label}: {len(both)} combined, {len(units_only)} units-only, {len(air_only)} air-only")
    print("  combined sample:", both[:8])
    print("  air-only sample:", air_only[:8])
