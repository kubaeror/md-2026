#!/usr/bin/env python3
"""Fix the misplaced deployments found by the 2026 audit (one-off migration).

Edits only history/units/<TAG>_2026_nsb.txt; rebuild the non-NSB variants
afterwards with `python tools/make_nonnsb_oob.py --apply`.

Re-running is safe: entries whose location already matches are skipped.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import rebase  # noqa: E402

OOB = os.path.join(REPO, "history", "units")

# (tag, exact division name, new province, optional new name, why)
MOVES = [
    ("USA", "2nd Infantry Division (Korea)", "7221", None,
     "Camp Humphreys, Gyeonggi, South Korea (state 604)"),
    ("GER", "Panzerbrigade 45 (Lithuania)", "3320", None,
     "Rudninkai/Rukla, Lithuania (state 110); name corrected from the working '42'"),
    ("SOV", "5th Combined Arms Army", "3977", None, "Ussuriysk, Primorye (state 692)"),
    ("SOV", "35th Combined Arms Army", "12654", None, "Belogorsk, Amur (state 1069)"),
    ("SOV", "155th Naval Infantry Brigade (Pacific)", "957", None,
     "Vladivostok, Primorye (state 692)"),
    ("SOV", "29th Combined Arms Army", "12641", None, "Chita, Transbaikal (state 1070)"),
    ("SOV", "68th Army Corps", "12446", None, "Yuzhno-Sakhalinsk (state 691)"),
    ("SUD", "1. Firqa Miliishiya", "12881", None, "Khartoum (state 220)"),
    ("SUD", "7. Firqa Mushaat", "12768", None, "Khartoum (state 220)"),
    ("SUD", "5. Firqa Miliishiya", "4133", None, "North Kordofan (state 223)"),
    ("SUD", "2. Liwa' Motahirka", "2088", None, "Khartoum (state 220)"),
    ("SYR", "3. Firqa Mushaat", "4111", None, "Damascus (state 186)"),
    ("SYR", "1. Firqa Miliishiya", "6302", None, "Homs (state 188)"),
    ("SYR", "5. Firqa Miliishiya", "12473", None, "Aleppo (state 566)"),
    ("UKR", "93rd Mechanized Brigade 'Kholodny Yar'", "11437", None,
     "Dnipropetrovsk (state 1087)"),
    ("UKR", "54th Motorized Brigade", "9556", None, "Kharkiv (state 696)"),
    ("UKR", "35th Marine Brigade", "11683", None, "Mykolaiv (state 1086)"),
    ("UKR", "36th Marine Brigade", "6597", None, "Mykolaiv (state 1086)"),
    ("UKR", "118th TDF Brigade", "488", None, "Cherkasy (state 1091)"),
    ("UKR", "55th Artillery Brigade", "11405", None, "Zaporizhzhia (state 694)"),
]


def division_blocks(text):
    """(open_brace_index, block_end_index, body) for every division block."""
    out = []
    for m in re.finditer(r"(?m)^\tdivision\s*=\s*\{", text):
        ob = text.index("{", m.end() - 1)
        end = rebase.find_block(text, ob)
        out.append((ob, end, text[ob:end]))
    return out


def main():
    moved, skipped, failed = 0, 0, 0
    for tag, name, prov, newname, why in MOVES:
        path = os.path.join(OOB, f"{tag}_2026_nsb.txt")
        text = rebase.read(path)
        hits = [b for b in division_blocks(text)
                if re.search(r'(?m)^\t\tname\s*=\s*"' + re.escape(name) + r'"$', b[2])]
        if len(hits) != 1:
            print(f"!! {tag} {name!r}: {len(hits)} matching division blocks")
            failed += 1
            continue
        ob, end, body = hits[0]
        new_body = re.sub(r"(?m)^(\t\tlocation\s*=\s*)\d+", r"\g<1>" + prov, body, count=1)
        if newname:
            new_body = re.sub(r'(?m)^(\t\tname\s*=\s*")' + re.escape(name) + r'(")$',
                              r"\g<1>" + newname.replace("\\", "\\\\") + r"\g<2>", new_body, count=1)
        if new_body == body:
            skipped += 1
            continue
        rebase.write(path, text[:ob] + new_body + text[end:])
        moved += 1
        print(f"ok {tag}: {name} -> province {prov}  ({why})")
    print(f"{moved} moved, {skipped} already correct, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
