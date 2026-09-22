#!/usr/bin/env python3
"""Generate the non-No-Step-Back variants of the 2026 orders of battle.

Without the *No Step Back* DLC the 2026 bookmark must not load a file that
references equipment only unlocked by NSB-gated technologies.  This tool

  * reads MD's technology tree and collects which equipment is unlocked only
    through NSB technologies (``NSB_*.txt`` / ``has_dlc = "No Step Back"``),
  * checks every equipment reference in ``history/units/<TAG>_2026_nsb.txt``,
  * replaces NSB-only references using ``NSB_EQUIVALENT`` (all current 2026
    files are DLC-neutral, so in practice the variants are identical),
  * writes ``history/units/<TAG>_2026_nonnsb.txt``.

Sub-units are deliberately not filtered: MD defines every sub-unit in its own
``common/units/*.txt`` (MD replaces that folder), and MD's own ``*_2000_nonnsb``
order-of-battle files use the same sub-units as the NSB ones.

Usage:
    python tools/make_nonnsb_oob.py [--apply] [--md PATH]
"""

import argparse
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rebase  # noqa: E402

REPO = rebase.REPO
OOB_DIR = os.path.join(REPO, "history", "units")

# NSB-only equipment -> non-NSB replacement.  Empty today; kept so future
# OOB edits have one obvious place for the mapping.
NSB_EQUIVALENT = {
    # "example_nsb_only": "example_nonnsb",
}

GENERATED_HEADER = (
    "# GENERATED FILE - do not edit by hand.\n"
    "# Non-No-Step-Back variant of {tag}_2026_nsb.txt.\n"
    "# Rebuild with: python tools/make_nonnsb_oob.py --apply\n"
)


def dlc_availability(md):
    """equipment -> set of DLC paths ('nsb', 'nonsb', 'both') that unlock it."""
    out = defaultdict(set)
    root = os.path.join(md, "common", "technologies")
    for name in sorted(os.listdir(root)):
        if not name.endswith(".txt"):
            continue
        text = rebase.strip_comments(rebase.read(os.path.join(root, name)))
        for m in re.finditer(r"(?m)^\s*([A-Za-z0-9_]+)\s*=\s*\{", text):
            ob = text.index("{", m.end() - 1)
            body = text[ob:rebase.find_block(text, ob)]
            if "enable_equipment" not in body:
                continue
            names = set()
            for g in re.findall(r"enable_equipments\s*=\s*\{([^}]*)\}", body):
                names |= set(g.split())
            if not names:
                continue
            if re.search(r"NOT\s*=\s*\{[^}]*has_dlc\s*=\s*\"No Step Back\"", body):
                kind = "nonsb"
            elif 'has_dlc = "No Step Back"' in body or name.startswith("NSB_"):
                kind = "nsb"
            else:
                kind = "both"
            for n in names:
                out[n].add(kind)
    return out


def equipment_refs(text):
    """Every equipment name referenced by an OOB file."""
    used = set()
    for m in re.finditer(r"type[ \t]*=[ \t]*([A-Za-z0-9_]+)", text):
        used.add(m.group(1))
    for block_re in (r"equipment[ \t]*=[ \t]*\{", r"air_wings[ \t]*=[ \t]*\{",
                     r"fleet[ \t]*=[ \t]*\{"):
        for m in re.finditer(block_re, text):
            ob = text.index("{", m.end() - 1)
            body = text[ob:rebase.find_block(text, ob)]
            for mm in re.finditer(r"(?m)^[ \t]*([A-Za-z_][A-Za-z0-9_]*)[ \t]*=[ \t]*\{", body):
                name = mm.group(1)
                if not name.isdigit():
                    used.add(name)
    return used


def make_nonnsb(text, tag, avail):
    """Return (new_text, replacements, unportable)."""
    replacements, unportable = [], []

    def replace(name):
        if name in NSB_EQUIVALENT:
            replacements.append((name, NSB_EQUIVALENT[name]))
            return NSB_EQUIVALENT[name]
        unportable.append(name)
        return name

    def check(name):
        paths = avail.get(name)
        if paths is None:
            return name  # not tech-gated at all (module, archetype, ...): assume ok
        if "nsb" in paths and "nonsb" not in paths and "both" not in paths:
            return replace(name)
        return name

    def sub_type(m):
        return "type = " + check(m.group(1))

    text = re.sub(r"type[ \t]*=[ \t]*([A-Za-z0-9_]+)", sub_type, text)

    spans = []
    for block_re in (r"equipment[ \t]*=[ \t]*\{", r"air_wings[ \t]*=[ \t]*\{",
                     r"fleet[ \t]*=[ \t]*\{", r"add_equipment_to_stockpile\s*=\s*\{"):
        for m in re.finditer(block_re, text):
            ob = text.index("{", m.end() - 1)
            end = rebase.find_block(text, ob)
            if any(s < ob and end <= e for s, e, _ in spans):
                continue
            body = text[ob:end]

            def sub_key(mm):
                name = mm.group(2)
                if name.isdigit():
                    return mm.group(0)
                return mm.group(1) + check(name) + " = {"

            body2 = re.sub(r"(?m)^([ \t]*)([A-Za-z_][A-Za-z0-9_]*)[ \t]*=[ \t]*\{",
                           sub_key, body)
            if body2 != body:
                spans.append((ob, end, body2))
    for ob, end, body2 in sorted(spans, reverse=True):
        text = text[:ob] + body2 + text[end:]
    return text, replacements, sorted(set(unportable))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="verify the on-disk non-NSB files match a fresh generation")
    ap.add_argument("--md", default=os.environ.get("MD_PATH", rebase.DEFAULT_MD))
    args = ap.parse_args()

    avail = dlc_availability(args.md)
    nsb_only = sorted(n for n, p in avail.items()
                      if "nsb" in p and "nonsb" not in p and "both" not in p)
    print(f"NSB-only equipment in MD: {len(nsb_only)}")

    total, problems, stale = 0, 0, 0
    for fn in sorted(os.listdir(OOB_DIR)):
        m = re.match(r"^([A-Z]{3})_2026_nsb\.txt$", fn)
        if not m:
            continue
        tag = m.group(1)
        path = os.path.join(OOB_DIR, fn)
        text = rebase.read(path)
        new_text, replacements, unportable = make_nonnsb(text, tag, avail)
        if unportable:
            problems += 1
            print(f"  !! {tag}: no non-NSB equivalent for {unportable}")
        header = GENERATED_HEADER.format(tag=tag)
        body = new_text
        if body.startswith(header):
            pass
        else:
            new_text = header + body
        out = os.path.join(OOB_DIR, f"{tag}_2026_nonnsb.txt")
        total += 1
        if args.check:
            on_disk = rebase.read(out) if os.path.exists(out) else None
            if on_disk != new_text:
                stale += 1
                print(f"  !! {tag}: non-NSB variant is stale (regenerate with --apply)")
        else:
            print(f"  {tag}: {len(replacements)} replacements -> {os.path.basename(out)}")
        if args.apply:
            rebase.write(out, new_text)
    if args.check:
        print(f"{total} variants checked, {stale} stale")
        if stale:
            sys.exit(1)
    else:
        print(f"{total} variants" + ("" if args.apply else "  (dry-run, use --apply)"))
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
