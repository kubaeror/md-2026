"""Fixes complete_national_focus references in the 2026 patches.

References to focuses that no longer exist in MD 2.0 are mapped to the closest
MD 2.0 focus of the same country (fuzzy match) or dropped.

Usage:
    python tools/fix_focus_refs.py            # dry run, writes patches/mappings/focuses.csv
    python tools/fix_focus_refs.py --apply    # rewrite the patch files
"""

import argparse
import csv
import difflib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rebase  # noqa: E402

REPO = rebase.REPO
PATCH_DIR = os.path.join(REPO, "patches", "history_countries")
MAP_FILE = os.path.join(REPO, "patches", "mappings", "focuses.csv")
TAG_RENAME = {"NOR": "NRY"}

# Reviewed replacements for references whose fuzzy match was not meaningful.
OVERRIDES = {
    "JAP_ocean_campaigns": "JAP_blue_water_navy",
    "JAP_invest_in_toyota": "JAP_automotive_industry",
    "JAP_air_force_focus": "JAP_air_self_defence_force",
    "JAP_southern_expressways": "JAP_infrastructure_investments",
    "JAP_develop_honshu": "JAP_kanto_infrastructure",
    "JAP_new_trade_policy": "JAP_economic_partnership_agreements",
    "JAP_national_renewal": "JAP_a_nation_reborn",
    "CHI_One_China_Policy": "CHI_SAR_one_china_framework",
    "CHI_Two_Systems": "CHI_SAR_two_systems_commitment",
    "CHI_Internet_Crackdown": "CHI_three_red_lines_crackdown",
    "CHI_Global_Influence": "CHI_Leverage_Influence",
    "CHI_Chairman_Jiang_Reign": "CHI_hu_jintao_reign",
    "ENG_economic_stimulus": "ENG_a_more_balanced_economy",
    "ENG_focus_on_the_navy": "ENG_multi_ocean_navy",
    "ENG_focus_on_the_army": "ENG_field_army_expansion",
    "ENG_the_future_of_britain": "ENG_ambitions_for_britain",
    "FRA_the_fifth_power": "FRA_state_power",
    "MD2026_GER_energy_independence": "MD2026_GER_energy_transition",
    "MD2026_GER_eu_expansion": "MD2026_GER_eu_enlargement",
    "MD2026_GER_european_army": "MD2026_GER_european_army_corps",
    "MD2026_GER_nato_2_percent": "MD2026_GER_nato_commitment",
    "MD2026_KOR_kf21": "MD2026_KOR_kf21_boramae",
}

# References with no sensible MD 2.0 equivalent - dropped (commented out).
DROP = {
    "JAP_finish_nishiseto",
    "JAP_bushido",
    "JAP_continental_campaigns",
    "CHI_Proper_State_Atheism",
    "CHI_Preserve_the_Revolution",
    "CHI_Favor_Multipolarity",
    "CHI_The_Untapped_Market",
    "CHI_Smash_the_Iron_Rice_Bowl",
    "CHI_End_PLA_Business_Ventures",
    "CHI_The_Korean_Peninsula",
    "CHI_Future_of_the_CPC",
    "CHI_The_Northern_Shield",
    "HOL_NAM",
    "GEO_whyareyouhere",
    "RAJ_land_of_salad",
    "USSR_Legacy",
}


def load_focus_ids(md):
    ids = set()
    for root in (os.path.join(md, "common", "national_focus"),
                 os.path.join(REPO, "common", "national_focus")):
        for name in os.listdir(root):
            if name.endswith(".txt"):
                ids |= set(re.findall(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_\-\.]+)",
                                      rebase.read(os.path.join(root, name))))
    return ids


def suggest(fid, pool):
    # try the same tag first, then the renamed tag, then everything
    tag = fid.split("_")[0]
    prefixes = [tag]
    if tag in TAG_RENAME:
        prefixes.append(TAG_RENAME[tag])
    for pref in prefixes:
        cands = [p for p in pool if p.startswith(pref + "_")]
        hit = difflib.get_close_matches(fid, cands, n=1, cutoff=0.55)
        if hit:
            return hit[0]
    hit = difflib.get_close_matches(fid, list(pool), n=1, cutoff=0.75)
    return hit[0] if hit else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--md", default=os.environ.get("MD_PATH", rebase.DEFAULT_MD))
    args = ap.parse_args()

    focus = load_focus_ids(args.md)
    rows = []
    for name in sorted(os.listdir(PATCH_DIR)):
        if not name.endswith(".txt"):
            continue
        text = rebase.read(os.path.join(PATCH_DIR, name))
        new_text = text
        for m in re.finditer(r"(?m)^(\s*)complete_national_focus\s*=\s*([A-Za-z0-9_\-\.]+)\s*$", text):
            fid = m.group(2)
            if fid in focus:
                continue
            if fid in OVERRIDES:
                repl = OVERRIDES[fid]
            elif fid in DROP:
                repl = ""
            else:
                repl = suggest(fid, focus)
            rows.append([fid, repl, name])
            if args.apply:
                if repl:
                    new_text = new_text.replace(m.group(0),
                                                f"{m.group(1)}complete_national_focus = {repl}")
                else:
                    new_text = new_text.replace(m.group(0),
                                                f"{m.group(1)}# MD2026: dropped (no MD 2.0 equivalent): {fid}")
        if args.apply and new_text != text:
            rebase.write(os.path.join(PATCH_DIR, name), new_text)

    mapped = sum(1 for r in rows if r[1])
    print(f"nieistniejacych referencji: {len(rows)} | zmapowanych: {mapped} | do usuniecia: {len(rows) - mapped}")
    os.makedirs(os.path.dirname(MAP_FILE), exist_ok=True)
    with open(MAP_FILE, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f)
        w.writerow(["old", "new", "patch_file"])
        w.writerows(rows)
    print("wrote", MAP_FILE)
    for r in rows:
        if not r[1]:
            print(f"  ?? {r[0]:52} ({r[2]})")


if __name__ == "__main__":
    main()
