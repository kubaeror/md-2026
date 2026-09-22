#!/usr/bin/env python3
"""Read-only lookup helper for OOB editing.

Resolves the mod's state map (from MD + the submod's own history/states) so an
editor can pick the right province for a division, fleet or air wing.

Usage:
    python tools/oob_lookup.py --province 10781
    python tools/oob_lookup.py --state 604
    python tools/oob_lookup.py --tag USA [--bases-only] [--provinces]
    python tools/oob_lookup.py --tag USA --unit "2nd Infantry"
    python tools/oob_lookup.py --search Gyeonggi
    python tools/oob_lookup.py --equipment f16_block_52
    python tools/oob_lookup.py --equipment-search f16

All lookups are read-only.
"""

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))

import oob_digest  # noqa: E402
import rebase  # noqa: E402

_EQ_CACHE = None


def provinces_of(ref, sid):
    return sorted((p for p, s in ref.prov2state.items() if s == str(sid)), key=int)


def state_line(ref, sid):
    info = ref.state.get(str(sid), {})
    naval = ", ".join(f"{p}:L{l}" for p, l in sorted(info.get("naval", {}).items())) or "-"
    return (f"state {sid} ({ref.name(sid)}) owner={info.get('owner')} "
            f"air={info.get('air', 0)} naval={naval} provinces={len(provinces_of(ref, sid))} "
            f"file={info.get('file')}")


def equipment_names(md):
    global _EQ_CACHE
    if _EQ_CACHE is None:
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
        _EQ_CACHE = names
    return _EQ_CACHE


def show_units(ref, tag, needle):
    path = os.path.join(REPO, "history", "units", f"{tag}_2026_nsb.txt")
    if not os.path.exists(path):
        print(f"no {os.path.relpath(path, REPO)}")
        return 1
    d = oob_digest.parse_oob(path, ref)
    needle = needle.lower()
    for u in d["divisions"]:
        if needle in u["name"].lower():
            print(f"DIV   {u['name']} [{u['template']}] province {u['province']} "
                  f"state {u['state']} ({u['state_name']}) owner {u['owner']}")
    for w in d["air_wings"]:
        if needle in (w["name"] or "").lower():
            print(f"AIR   {w['name']} state {w['state']} ({w['state_name']}) owner {w['owner']}")
    for f in d["fleets"]:
        if needle in f["name"].lower():
            print(f"FLEET {f['name']} base {f['naval_base']} "
                  f"state {f['base_state']} ({f['base_state_name']}) owner {f['base_owner']}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=None)
    ap.add_argument("--province")
    ap.add_argument("--state")
    ap.add_argument("--tag")
    ap.add_argument("--search")
    ap.add_argument("--equipment")
    ap.add_argument("--equipment-search")
    ap.add_argument("--unit")
    ap.add_argument("--bases-only", action="store_true",
                    help="with --tag: only states with an air/naval base")
    ap.add_argument("--provinces", action="store_true",
                    help="with --tag: list every province id")
    args = ap.parse_args()

    md = oob_digest.resolve(args.md, "MD_PATH", rebase.MD_REL, "descriptor.mod")
    ref = oob_digest.Ref(md)

    if args.province:
        sid, info = ref.prov(args.province)
        if not sid:
            print(f"province {args.province}: unknown")
            return 1
        print(state_line(ref, sid))
        return 0

    if args.state:
        print(state_line(ref, args.state))
        provs = provinces_of(ref, args.state)
        if provs:
            print("provinces:", " ".join(provs))
        return 0

    if args.tag and args.unit:
        return show_units(ref, args.tag.upper(), args.unit)

    if args.tag:
        tag = args.tag.upper()
        rows = []
        for sid, info in ref.state.items():
            if info.get("owner") != tag:
                continue
            naval = sum(1 for l in info.get("naval", {}).values() if l)
            air = info.get("air", 0)
            if args.bases_only and not (naval or air):
                continue
            rows.append((int(sid), sid, info, naval, air))
        for _, sid, info, naval, air in sorted(rows):
            provs = " ".join(provinces_of(ref, sid)) if args.provinces else ""
            print(f"{sid:>5}  {ref.name(sid):<32} air={air:<2} naval={naval:<2} "
                  f"file={info.get('file')}  {provs}")
        print(f"({len(rows)} states owned by {tag})")
        return 0

    if args.search:
        needle = args.search.lower()
        hits = 0
        for sid, info in sorted(ref.state.items(), key=lambda kv: int(kv[0])):
            if needle in ref.name(sid).lower():
                print(state_line(ref, sid))
                hits += 1
        if not hits:
            print(f"no state name contains {args.search!r}")
            return 1
        return 0

    if args.equipment or args.equipment_search:
        names = equipment_names(md)
        if args.equipment:
            ok = args.equipment in names
            print("yes" if ok else "NO - not defined by MD")
            return 0 if ok else 1
        needle = args.equipment_search.lower()
        hits = sorted(n for n in names if needle in n.lower())
        print("\n".join(hits) if hits else f"no equipment name contains {args.equipment_search!r}")
        return 0 if hits else 1

    ap.error("pass one of --province/--state/--tag/--search/--equipment")


if __name__ == "__main__":
    sys.exit(main())
