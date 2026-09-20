"""Builds rename mappings (MD 1.12 -> MD 2.0) for technologies and ideas.

Scans the submod for identifiers that do not exist in the installed MD and
suggests the closest MD 2.0 identifier (exact-insensitive, then fuzzy).
Writes patches/mappings/techs.csv and patches/mappings/ideas.csv for review.

Usage: python tools/build_mappings.py [--md PATH] [--write]
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
DEFAULT_MD = rebase.DEFAULT_MD


def collect_techs(md):
    ids = set()
    root = os.path.join(md, "common", "technologies")
    for name in os.listdir(root):
        if not name.endswith(".txt"):
            continue
        text = rebase.strip_comments(rebase.read(os.path.join(root, name)))
        depth = 0
        for line in text.split("\n"):
            if depth == 1:
                m = re.match(r"\s*([A-Za-z0-9_]+)\s*=", line)
                if m:
                    ids.add(m.group(1))
            depth += line.count("{") - line.count("}")
    return ids


def collect_ideas(md):
    ids = set()
    for root_dir in (os.path.join(md, "common", "ideas"), os.path.join(REPO, "common", "ideas")):
        for name in os.listdir(root_dir):
            if not name.endswith(".txt"):
                continue
            text = rebase.strip_comments(rebase.read(os.path.join(root_dir, name)))
            for m in re.finditer(r"ideas\s*=\s*\{", text):
                ob = text.index("{", m.start())
                end = rebase.find_block(text, ob)
                for cat, cbody in rebase.children(text[ob + 1:end - 1]):
                    for idea, _ in rebase.children(cbody):
                        ids.add(idea)
    return ids


def scan_techs(md):
    """Techs referenced by the submod via set_technology."""
    used = {}
    for dirpath, _, files in os.walk(REPO):
        if ".git" in dirpath:
            continue
        for fn in files:
            if not fn.endswith(".txt"):
                continue
            p = os.path.join(dirpath, fn)
            text = rebase.read(p)
            for m in re.finditer(r"set_technology\s*=\s*\{", text):
                ob = text.index("{", m.start())
                end = rebase.find_block(text, ob)
                for tm in re.finditer(r"(?m)^\s*([A-Za-z0-9_]+)\s*=", text[ob:end]):
                    used.setdefault(tm.group(1), set()).add(os.path.relpath(p, REPO))
    return used


def scan_ideas(md):
    used = {}
    pat = re.compile(r"(?:add_ideas|has_idea|remove_ideas|add_idea|remove_idea)\s*=\s*\{([^}]*)\}|(?:add_ideas|has_idea|remove_ideas|add_idea|remove_idea)\s*=\s*([A-Za-z0-9_]+)")
    for dirpath, _, files in os.walk(REPO):
        if ".git" in dirpath:
            continue
        for fn in files:
            if not fn.endswith(".txt"):
                continue
            p = os.path.join(dirpath, fn)
            text = rebase.strip_comments(rebase.read(p))
            for m in pat.finditer(text):
                names = m.group(1).split() if m.group(1) else [m.group(2)]
                for nm in names:
                    if nm and nm[0].isalpha():
                        used.setdefault(nm, set()).add(os.path.relpath(p, REPO))
    return used


def suggest(name, pool, cutoff=0.75):
    low = {p.lower(): p for p in pool}
    if name.lower() in low:
        return low[name.lower()]
    cands = difflib.get_close_matches(name.lower(), list(low), n=1, cutoff=cutoff)
    return low[cands[0]] if cands else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=os.environ.get("MD_PATH", DEFAULT_MD))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    md = args.md
    techs = collect_techs(md)
    ideas = collect_ideas(md)
    print(f"MD: {len(techs)} technologii, {len(ideas)} idei")

    for kind, pool, used, out_name in (
        ("tech", techs, scan_techs(md), "techs.csv"),
        ("idea", ideas, scan_ideas(md), "ideas.csv"),
    ):
        bad = {k: v for k, v in used.items() if k not in pool}
        print(f"\n=== {kind}: {len(bad)} nieznanych (z {len(used)} uzywanych) ===")
        rows = []
        for k in sorted(bad):
            s = suggest(k, pool)
            rows.append((k, s, len(bad[k]), sorted(bad[k])[0] if bad[k] else ""))
        for k, s, n, f in rows:
            flag = "OK " if s else "?? "
            print(f"  {flag}{k:44} -> {s or '(brak)':44} {n}x  {f}")
        if args.write:
            dst = os.path.join(REPO, "patches", "mappings", out_name)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w", encoding="utf-8", newline="\n") as f:
                w = csv.writer(f)
                w.writerow(["old", "new", "refs", "example_file"])
                w.writerows(rows)
            print("  wrote", dst)


if __name__ == "__main__":
    main()
