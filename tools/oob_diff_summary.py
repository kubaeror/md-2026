#!/usr/bin/env python3
"""Before/after summary of the 2026 OOBs (HEAD vs working tree).

Used to review the country-by-country audit fixes: prints per-tag division,
ship and aircraft counts and the added/removed unit names.

Usage:
    python tools/oob_diff_summary.py                 # all changed tags
    python tools/oob_diff_summary.py --tag USA SOV   # specific tags
    python tools/oob_diff_summary.py --full --tag USA
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import oob_digest  # noqa: E402
import rebase  # noqa: E402


def git_show(rev, path, out_path):
    with open(out_path, "wb") as f:
        rc = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=REPO, stdout=f,
                            stderr=subprocess.DEVNULL)
    return rc.returncode == 0


def names(d):
    divs = {u["name"] for u in d["divisions"]}
    ships = {s["name"] for f in d["fleets"] for tf in f["task_forces"] for s in tf["ships"]}
    planes = Counter()
    for w in d["air_wings"]:
        for a in w["aircraft"]:
            planes[(a["version"] or a["airframe"])] += a["amount"]
    return divs, ships, planes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--rev", default="HEAD")
    args = ap.parse_args()

    md = oob_digest.resolve(None, "MD_PATH", rebase.MD_REL, "descriptor.mod")
    ref = oob_digest.Ref(md)

    tags = [t.upper() for t in args.tag]
    if not tags:
        out = subprocess.run(["git", "status", "--short", "history/units"],
                             cwd=REPO, capture_output=True, text=True).stdout
        tags = sorted({line.split()[-1][:3] for line in out.splitlines()})
    tmp = tempfile.mkdtemp(prefix="oobdiff_")
    for tag in tags:
        rel = f"history/units/{tag}_2026_nsb.txt"
        old_path = os.path.join(tmp, f"{tag}_old.txt")
        if not os.path.exists(os.path.join(REPO, rel)) or not git_show(args.rev, rel, old_path):
            print(f"{tag}: no {args.rev} version")
            continue
        old = oob_digest.parse_oob(old_path, ref)
        new = oob_digest.parse_oob(os.path.join(REPO, rel), ref)
        od, os_, op = names(old)
        nd, ns, np_ = names(new)
        print(f"== {tag}: divisions {len(old['divisions'])} -> {len(new['divisions'])} | "
              f"ships {len(os_)} -> {len(ns)} | aircraft {sum(op.values())} -> {sum(np_.values())}")
        for label, removed, added in (("div -", od - nd, nd - od),
                                      ("ship -", os_ - ns, ns - os_)):
            for x in sorted(removed):
                print(f"   {label} {x}")
            for x in sorted(added):
                print(f"   {label.replace('-', '+')} {x}")
        for k in sorted(set(op) | set(np_)):
            if op.get(k, 0) != np_.get(k, 0):
                print(f"   air  {k}: {op.get(k, 0)} -> {np_.get(k, 0)}")
        if args.full:
            for u in new["divisions"]:
                print(f"   div  {u['name']} @ {u['state_name']} ({u['owner']})")
            for f in new["fleets"]:
                print(f"   fleet {f['name']} @ {f['base_state_name']} ({f['base_owner']})")
            for w in new["air_wings"]:
                ac = ", ".join(f"{a['version'] or a['airframe']} x{a['amount']}" for a in w["aircraft"])
                print(f"   air  {w['name']} @ {w['state_name']} ({w['owner']}): {ac}")
    print(f"\ntmp files: {tmp}")


if __name__ == "__main__":
    sys.exit(main())
