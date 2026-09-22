#!/usr/bin/env python3
"""Fast per-tag structural check for the 2026 orders of battle.

Runs the OOB-related checks of tools/audit_deep.py for one or more tags (or all
tags) and prints the findings. Unlike the full audit it does not scan histories,
focus trees, events or localisation, so it is quick enough to run after every
edit.

Usage:
    python tools/oob_check.py --tag USA [--tag GER ...]
    python tools/oob_check.py --all
    python tools/oob_check.py --tag USA --verbose     # also print the units

Exit code 1 when any finding is reported.
"""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import oob_digest  # noqa: E402
import rebase  # noqa: E402

SHIP_FAMILY = {
    "carrier": "carrier_hull_", "battleship": "battleship_hull_",
    "cruiser": "cruiser_hull_", "destroyer": "destroyer_hull_",
    "frigate": "frigate_hull_", "corvette": "corvette_hull_",
    "helicopter_operator": "helicopter_operator_hull_",
    "attack_submarine": "attack_submarine_hull_",
    "missile_submarine": "missile_submarine_hull_",
    "submarine": ("attack_submarine_hull_", "missile_submarine_hull_"),
}

FOREIGN_BASING_OK = {
    ("ENG", "GER"), ("FRA", "GER"), ("USA", "GER"), ("USA", "JAP"),
    ("USA", "SPR"), ("USA", "ITA"), ("USA", "KOR"), ("USA", "ENG"),
    ("TUR", "NCY"), ("GER", "LIT"), ("USA", "POL"), ("USA", "ROM"),
    ("CHI", "HKG"),
} | {tuple(p) for p in rebase.foreign_basing_pairs()}


def block(text, start):
    return text[start:oob_digest.find_block(text, start)]


def equipment_names(md):
    names = set()
    for root in (os.path.join(md, "common", "units", "equipment"),
                 os.path.join(REPO, "common", "units", "equipment")):
        for dp, _, ns in os.walk(root):
            for n in ns:
                if not n.endswith(".txt"):
                    continue
                text = rebase.strip_comments(rebase.read(os.path.join(dp, n)))
                for m in re.finditer(r"(?m)^\s*([A-Za-z0-9_]+)\s*=\s*\{", text):
                    names.add(m.group(1))
    return names


def subunit_names(md):
    names = set()
    for root in (os.path.join(md, "common", "units"), os.path.join(REPO, "common", "units")):
        for dp, _, ns in os.walk(root):
            for n in ns:
                if not n.endswith(".txt"):
                    continue
                text = rebase.strip_comments(rebase.read(os.path.join(dp, n)))
                for m in re.finditer(r"(?m)^\s*sub_units\s*=\s*\{", text):
                    ob = text.index("{", m.end() - 1)
                    for name, _ in rebase.children(text[ob:rebase.find_block(text, ob)]):
                        names.add(name)
    return names


def check_tag(path, ref, equipment, subunits=None, verbose=False):
    tag = os.path.basename(path)[:3]
    text = rebase.strip_comments(rebase.read(path))
    out = []

    def add(code, msg, line=None):
        out.append((code, msg, line))

    templates = set()
    for m in re.finditer(r"division_template\s*=\s*\{", text):
        b = block(text, text.index("{", m.end() - 1))
        nm = re.search(r'name\s*=\s*"([^"]+)"', b)
        if nm:
            templates.add(nm.group(1))
        for re_key, what in ((r"regiments\s*=\s*\{", "battalions"),
                             (r"support\s*=\s*\{", "support companies")):
            bm = re.search(re_key, b)
            if not bm:
                continue
            bb = block(b, b.index("{", bm.end() - 1))
            batts = re.findall(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", bb)
            limit = 25 if what == "battalions" else 5
            if len(batts) > limit:
                add("O-15", f"template {nm.group(1) if nm else '?'}: {len(batts)} {what}")
            if subunits:
                for bname in batts:
                    if bname not in subunits and not bname.isdigit():
                        add("O-16", f"template {nm.group(1) if nm else '?'}: "
                                    f"unknown sub-unit '{bname}'")
            coords = re.findall(r"x\s*=\s*(\d+)\s*y\s*=\s*(\d+)", bb)
            dup = {c for c in coords if coords.count(c) > 1}
            if dup:
                add("O-15", f"template {nm.group(1) if nm else '?'}: duplicate coords {sorted(dup)}")

    for m in re.finditer(r'division_template\s*=\s*"([^"]+)"', text):
        if m.group(1) not in templates:
            add("O-05", f"template '{m.group(1)}' used but not defined in this file")

    if verbose:
        d = oob_digest.parse_oob(path, ref)
        for u in d["divisions"]:
            print(f"DIV   {u['name']} [{u['template']}] state {u['state']} "
                  f"({u['state_name']}) owner {u['owner']}")
        for w in d["air_wings"]:
            print(f"AIR   {w['name']} state {w['state']} ({w['state_name']}) owner {w['owner']}")
        for f in d["fleets"]:
            print(f"FLEET {f['name']} state {f['base_state']} ({f['base_state_name']}) "
                  f"owner {f['base_owner']}")

    for m in re.finditer(r"division\s*=\s*\{", text):
        b = block(text, text.index("{", m.end() - 1))
        loc = re.search(r"location\s*=\s*(\d+)", b)
        nm = re.search(r'name\s*=\s*"([^"]+)"', b)
        if not loc:
            continue
        sid, info = ref.prov(loc.group(1))
        owner = info.get("owner") if info else None
        if not sid:
            add("O-02", f"division '{nm.group(1) if nm else '?'}' in unknown province {loc.group(1)}")
        elif owner != tag and (tag, owner) not in FOREIGN_BASING_OK:
            add("O-02", f"division '{nm.group(1) if nm else '?'}' stationed in {owner} (state {sid})")

    for m in re.finditer(r"naval_base\s*=\s*(\d+)", text):
        prov = m.group(1)
        sid = ref.prov2state.get(prov)
        if not sid:
            add("O-03", f"naval_base province {prov} unknown")
            continue
        info = ref.state.get(sid, {})
        if info.get("owner") != tag and (tag, info.get("owner")) not in FOREIGN_BASING_OK:
            add("O-03", f"naval_base {prov} is in {info.get('owner')} (state {sid})")
        elif not info.get("naval", {}).get(prov):
            add("O-03", f"naval_base {prov} has no naval base building (state {sid})")

    m = re.search(r"air_wings\s*=\s*\{", text)
    if m:
        b = block(text, text.index("{", m.end() - 1))
        for mm in re.finditer(r"(?m)^\s*(\d+)\s*=\s*\{", b):
            sid = mm.group(1)
            info = ref.state.get(sid, {})
            owner = info.get("owner")
            if not info:
                add("O-04", f"air wing in unknown state {sid}")
            elif owner != tag and (tag, owner) not in FOREIGN_BASING_OK:
                add("O-04", f"air wing in {owner} (state {sid})")
            elif not info.get("air"):
                add("O-04", f"air wing in state {sid} without an air base")

    for m in re.finditer(r"(?m)^\s*type\s*=\s*([A-Za-z0-9_]+)", text):
        if m.group(1) not in equipment:
            add("O-06", f"unknown equipment type '{m.group(1)}'")

    for m in re.finditer(r"add_equipment_to_stockpile\s*=\s*\{", text):
        b = block(text, text.index("{", m.end() - 1))
        tm = re.search(r"type\s*=\s*([A-Za-z0-9_]+)", b)
        am = re.search(r"amount\s*=\s*(\d+)", b)
        pr = re.search(r"producer\s*=\s*([A-Z]{3})", b)
        if tm and tm.group(1) not in equipment:
            add("O-07", f"stockpile type '{tm.group(1)}' unknown")
        if am and int(am.group(1)) <= 0:
            add("O-13", "stockpile amount <= 0")
        if pr and not re.match(r"^[A-Z]{3}$", pr.group(1)):
            add("O-13", f"stockpile producer '{pr.group(1)}' is not a tag")

    ships = []
    for m in re.finditer(r"ship\s*=\s*\{", text):
        b = block(text, text.index("{", m.end() - 1))
        nm = re.search(r'name\s*=\s*"([^"]+)"', b)
        df = re.search(r"definition\s*=\s*([A-Za-z_][A-Za-z0-9_]*)", b)
        hull = re.search(r"([a-z_]+_hull_[0-9]+)\s*=\s*\{", b)
        if nm:
            ships.append(nm.group(1))
        if df and hull:
            fam = SHIP_FAMILY.get(df.group(1))
            if fam:
                fams = (fam,) if isinstance(fam, str) else fam
                if not any(hull.group(1).startswith(f) for f in fams):
                    add("O-11", f"ship '{nm.group(1) if nm else '?'}' definition={df.group(1)} "
                                f"but hull {hull.group(1)}")
    for name, n in Counter(ships).items():
        if n > 1:
            add("O-10", f"duplicate ship name '{name}' ({n}x)")
    return tag, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--md", default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    md = oob_digest.resolve(args.md, "MD_PATH", rebase.MD_REL, "descriptor.mod")
    ref = oob_digest.Ref(md)
    equipment = equipment_names(md)
    subunits = subunit_names(md)

    if args.all:
        tags = sorted({n[:3] for n in os.listdir(os.path.join(REPO, "history", "units"))
                       if re.match(r"[A-Z]{3}_2026_nsb\.txt$", n)})
    else:
        tags = [t.upper() for t in args.tag]
    if not tags:
        ap.error("pass --tag or --all")

    problems = 0
    for tag in tags:
        path = os.path.join(REPO, "history", "units", f"{tag}_2026_nsb.txt")
        if not os.path.exists(path):
            print(f"{tag}: no OOB")
            problems += 1
            continue
        tag, findings = check_tag(path, ref, equipment, subunits, args.verbose)
        if not findings:
            print(f"{tag}: ok")
        for code, msg, line in findings:
            print(f"{tag}: {code} {msg}")
            problems += 1
    print(f"{len(tags)} file(s) checked, {problems} finding(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
