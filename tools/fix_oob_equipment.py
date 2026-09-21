#!/usr/bin/env python3
"""Map obsolete MD 1.x equipment names in our OOB files to MD 2.0 names.

The 2026 order-of-battle files were carried over from the old submod, which
used MD 1.x equipment names (``infantry_weapons5``, ``small_plane_strike_airframe_2``,
``command_control_equipment2`` ...).  MD 2.0 renamed most of them, so the game
logs "invalid database object" / "Invalid equipment version" and silently drops
the stockpiles and air wings.

Mapping rules (all verified against MD 2.0 definitions):
  * ``infantry_weaponsN``             -> ``infantry_weapons_N``      (same tier)
  * ``command_control_equipmentN``    -> ``cnc_equipment_N``         (same tier)
  * ``util_vehicle_equipment``        -> newest util_vehicle_* with year <= 2026
  * ``X_airframe_N``                  -> concrete equipment of archetype X with
                                         the same trailing tier digit
  * ``cv_medium_plane_fighter_airframe_N`` -> ``CV_MR_FighterN``
  * ``cv_medium_plane_maritime_patrol_airframe_N`` -> the unnumbered concrete name

Usage:
    python tools/fix_oob_equipment.py [--apply] [--md PATH]
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rebase  # noqa: E402

REPO = rebase.REPO
OOB_DIR = os.path.join(REPO, "history", "units")


def equipment_definitions(md):
    """name -> (archetype, year) for every equipment defined in MD + vanilla."""
    defs = {}
    roots = [os.path.join(md, "common", "units", "equipment"),
             os.path.join(rebase.VANILLA, "common", "units", "equipment")]
    for root in roots:
        for dirpath, _, files in os.walk(root):
            for fn in files:
                if not fn.endswith(".txt"):
                    continue
                try:
                    text = rebase.strip_comments(rebase.read(os.path.join(dirpath, fn)))
                except Exception:
                    continue
                for m in re.finditer(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", text):
                    ob = text.index("{", m.end() - 1)
                    body = text[ob:rebase.find_block(text, ob)]
                    am = re.search(r"archetype\s*=\s*([A-Za-z0-9_]+)", body)
                    ym = re.search(r"year\s*=\s*(\d{4})", body)
                    defs[m.group(1)] = (am.group(1) if am else None,
                                        int(ym.group(1)) if ym else 0)
    return defs


def tier(name):
    m = re.search(r"(\d+)$", name)
    return int(m.group(1)) if m else None


def build_mapping(defs):
    """obsolete name -> MD 2.0 name."""
    by_arch = {}
    for name, (arch, year) in defs.items():
        if arch:
            by_arch.setdefault(arch, []).append((name, year))
    for arch in by_arch:
        by_arch[arch].sort(key=lambda nf: (tier(nf[0]) if tier(nf[0]) is not None else 999, nf[1]))

    def pick(arch, want_tier):
        """Concrete equipment of `arch` closest to the wanted tier digit."""
        if arch not in by_arch:
            return None
        exact = [n for n, _ in by_arch[arch] if tier(n) == want_tier]
        if exact:
            return exact[0]
        cands = sorted(by_arch[arch], key=lambda nf: (abs((tier(nf[0]) or 99) - want_tier), nf[1]))
        return cands[0][0] if cands else None

    newest_util = max((n for n in defs if n.startswith("util_vehicle_") and defs[n][1] <= 2026),
                      key=lambda n: (defs[n][1], tier(n) or 0), default=None)

    def map_one(name):
        if name in defs:
            return None  # already valid
        m = re.match(r"^(.*?)(\d+)$", name)
        base, want = (m.group(1), int(m.group(2))) if m else (name, None)
        if base:
            base = base.rstrip("_")
        if want is not None and base + "_" + str(want) in defs:
            return base + "_" + str(want)
        if base == "command_control_equipment" and want is not None:
            cand = f"cnc_equipment_{want}"
            return cand if cand in defs else None
        if name == "util_vehicle_equipment":
            return newest_util
        if base == "cv_medium_plane_fighter_airframe" and want is not None:
            return pick("cv_medium_plane_airframe", want)
        if base == "cv_medium_plane_maritime_patrol_airframe":
            return "cv_medium_plane_maritime_patrol_airframe" if "cv_medium_plane_maritime_patrol_airframe" in defs else None
        if want is not None:
            got = pick(base, want)
            if got:
                return got
        return None

    mapping = {}
    for name in sorted(defs) + sorted(collect_used_names()):
        if name in mapping or name in defs:
            continue
        got = map_one(name)
        if got:
            mapping[name] = got
    return mapping


def collect_used_names():
    """Every equipment name referenced by our OOB files."""
    used = set()
    for fn in os.listdir(OOB_DIR):
        if not fn.endswith(".txt"):
            continue
        text = rebase.strip_comments(rebase.read(os.path.join(OOB_DIR, fn)))
        for m in re.finditer(r"type\s*=\s*([A-Za-z0-9_]+)", text):
            used.add(m.group(1))
        for m in re.finditer(r"equipment\s*=\s*\{", text):
            ob = text.index("{", m.end() - 1)
            body = text[ob:rebase.find_block(text, ob)]
            for mm in re.finditer(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", body):
                used.add(mm.group(1))
        for m in re.finditer(r"air_wings\s*=\s*\{", text):
            ob = text.index("{", m.end() - 1)
            body = text[ob:rebase.find_block(text, ob)]
            for mm in re.finditer(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", body):
                if not mm.group(1).isdigit():
                    used.add(mm.group(1))
    return used


def rewrite(text, mapping):
    """Replace obsolete names in equipment positions only."""
    changes = []

    def sub_type(m):
        name = m.group(1)
        if name in mapping:
            changes.append((name, mapping[name]))
            return "type = " + mapping[name]
        return m.group(0)

    text = re.sub(r"type[ \t]*=[ \t]*([A-Za-z0-9_]+)", sub_type, text)

    spans = []
    for block_re in (r"equipment[ \t]*=[ \t]*\{", r"air_wings[ \t]*=[ \t]*\{"):
        for m in re.finditer(block_re, text):
            ob = text.index("{", m.end() - 1)
            end = rebase.find_block(text, ob)
            if any(s < ob and end <= e for s, e, _ in spans):
                continue  # nested in an already collected block
            body = text[ob:end]

            def sub_key(mm):
                name = mm.group(2)
                if name in mapping:
                    changes.append((name, mapping[name]))
                    return mm.group(1) + mapping[name] + " = {"
                return mm.group(0)

            body2 = re.sub(r"(?m)^([ \t]*)([A-Za-z_][A-Za-z0-9_]*)[ \t]*=[ \t]*\{", sub_key, body)
            if body2 != body:
                spans.append((ob, end, body2))
    for ob, end, body2 in sorted(spans, reverse=True):
        text = text[:ob] + body2 + text[end:]
    return text, changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--md", default=os.environ.get("MD_PATH", rebase.DEFAULT_MD))
    args = ap.parse_args()

    defs = equipment_definitions(args.md)
    mapping = build_mapping(defs)
    print(f"mapowanie: {len(mapping)} nazw")
    for old, new in sorted(mapping.items()):
        print(f"   {old:44} -> {new}")

    total = 0
    for fn in sorted(os.listdir(OOB_DIR)):
        if not fn.endswith(".txt"):
            continue
        path = os.path.join(OOB_DIR, fn)
        text = rebase.read(path)
        new_text, changes = rewrite(text, mapping)
        if not changes:
            continue
        total += len(changes)
        print(f"   {fn}: {len(changes)} zmian")
        if args.apply:
            rebase.write(path, new_text)
    print(f"razem zmian: {total}" + ("" if args.apply else "  (dry-run, uzyj --apply)"))


if __name__ == "__main__":
    main()
