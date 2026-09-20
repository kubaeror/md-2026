"""Validates the submod against the installed Millennium Dawn version.

Checks every reference the submod makes (technologies, ideas, focuses,
characters, tags, events, localisation keys) against MD 2.0 + the submod's own
definitions, and looks for duplicate ids/keys.

Usage:
    python tools/validate.py [--md PATH] [--quiet]
Exit code 1 when errors are found.
"""

import argparse
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rebase  # noqa: E402

REPO = rebase.REPO
ERRORS = defaultdict(list)
WARNINGS = defaultdict(list)


def files(root, ext=".txt"):
    if not os.path.isdir(root):
        return []
    out = []
    for dirpath, _, names in os.walk(root):
        for n in names:
            if n.endswith(ext):
                out.append(os.path.join(dirpath, n))
    return sorted(out)


def rel(p):
    return os.path.relpath(p, REPO)


# ---------------------------------------------------------------- data sets

def load_sets(md):
    s = {}
    s["tech"] = set()
    for p in files(os.path.join(md, "common", "technologies")) + files(os.path.join(REPO, "common", "technologies")):
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r"technologies\s*=\s*\{", text):
            ob = text.index("{", m.start())
            end = rebase.find_block(text, ob)
            for name, _ in rebase.children(text[ob + 1:end - 1]):
                if not name.startswith("@"):
                    s["tech"].add(name)

    s["idea"] = set()
    for p in files(os.path.join(md, "common", "ideas")) + files(os.path.join(REPO, "common", "ideas")):
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r"ideas\s*=\s*\{", text):
            ob = text.index("{", m.start())
            end = rebase.find_block(text, ob)
            for _, cbody in rebase.children(text[ob + 1:end - 1]):
                for idea, _ in rebase.children(cbody):
                    s["idea"].add(idea)

    s["focus"] = set()
    s["focus_by_file"] = {}
    for root in (os.path.join(md, "common", "national_focus"), os.path.join(REPO, "common", "national_focus")):
        for p in files(root):
            text = rebase.read(p)
            ids = set(re.findall(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_\-\.]+)", text))
            s["focus"] |= ids
            s["focus_by_file"][p] = ids

    s["tag"] = set()
    for p in files(os.path.join(md, "common", "country_tags")) + files(os.path.join(REPO, "common", "country_tags")) + \
             files(os.path.join(md, "common", "country_tag_aliases")) + files(os.path.join(REPO, "common", "country_tag_aliases")):
        s["tag"] |= set(re.findall(r"(?m)^\s*([A-Z0-9]{3})\s*=", rebase.read(p)))

    s["char"] = set()
    for p in files(os.path.join(md, "common", "characters")) + files(os.path.join(REPO, "common", "characters")):
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r"characters\s*=\s*\{", text):
            ob = text.index("{", m.start())
            end = rebase.find_block(text, ob)
            for name, _ in rebase.children(text[ob + 1:end - 1]):
                s["char"].add(name)

    s["trait"] = set()
    for p in files(os.path.join(md, "common", "country_leader")) + files(os.path.join(REPO, "common", "country_leader")):
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r"leader_traits\s*=\s*\{", text):
            ob = text.index("{", m.start())
            end = rebase.find_block(text, ob)
            for name, _ in rebase.children(text[ob + 1:end - 1]):
                s["trait"].add(name)

    s["ideology"] = set()
    for p in files(os.path.join(md, "common", "ideologies")) + files(os.path.join(REPO, "common", "ideologies")):
        text = rebase.strip_comments(rebase.read(p))
        for name, body in rebase.children(text):
            s["ideology"].add(name)
            for sub, subbody in rebase.children(body):
                s["ideology"].add(sub)
                for subsub, subsubbody in rebase.children(subbody):
                    s["ideology"].add(subsub)
                    for leaf, _ in rebase.children(subsubbody):
                        s["ideology"].add(leaf)

    s["effect"] = set()
    s["trigger"] = set()
    for kind, sub in (("effect", "scripted_effects"), ("trigger", "scripted_triggers")):
        for root in (os.path.join(md, "common", sub), os.path.join(REPO, "common", sub)):
            for p in files(root):
                text = rebase.strip_comments(rebase.read(p))
                s[kind] |= {n for n, _ in rebase.children(text)}

    s["event"] = set()
    for root in (os.path.join(md, "events"), os.path.join(REPO, "events")):
        for p in files(root):
            text = rebase.strip_comments(rebase.read(p))
            s["event"] |= set(re.findall(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+\.[0-9]+)", text))

    s["loc"] = set()
    for root in (os.path.join(md, "localisation", "english"), os.path.join(REPO, "localisation")):
        for p in files(root, ".yml"):
            text = rebase.read(p)
            s["loc"] |= set(re.findall(r"(?m)^\s*([A-Za-z0-9_.\-]+):\d*\s", text))
    return s


# ---------------------------------------------------------------- scanning

def scan_submod():
    """Collect all references made by the submod."""
    ref = defaultdict(lambda: defaultdict(set))  # kind -> name -> files

    def add(kind, name, path):
        ref[kind][name].add(rel(path))

    for p in files(os.path.join(REPO, "common")) + files(os.path.join(REPO, "events")) + \
             files(os.path.join(REPO, "history")) + files(os.path.join(REPO, "patches")):
        text = rebase.read(p)
        clean = rebase.strip_comments(text)

        for m in re.finditer(r"set_technology\s*=\s*\{", clean):
            ob = clean.index("{", m.start())
            end = rebase.find_block(clean, ob)
            for tm in re.finditer(r"(?m)^\s*([A-Za-z0-9_]+)\s*=", clean[ob:end]):
                add("tech", tm.group(1), p)
        for m in re.finditer(r"has_tech\s*=\s*([A-Za-z0-9_]+)", clean):
            add("tech", m.group(1), p)

        pat = re.compile(r"(?:add_ideas|has_idea|remove_ideas|add_idea|remove_idea)\s*=\s*\{([^}]*)\}|"
                         r"(?:add_ideas|has_idea|remove_ideas|add_idea|remove_idea)\s*=\s*([A-Za-z0-9_]+)")
        for m in pat.finditer(clean):
            names = m.group(1).split() if m.group(1) else [m.group(2)]
            for n in names:
                if n and n[0].isalpha():
                    add("idea", n, p)

        for m in re.finditer(r"complete_national_focus\s*=\s*([A-Za-z0-9_\-\.]+)", clean):
            add("focus", m.group(1), p)
        for m in re.finditer(r"(?:recruit_character|promote_character|retire_character|has_character)\s*=\s*([^\s#]+)", clean):
            add("char", m.group(1), p)
        for m in re.finditer(r"(?<![\w])(?:original_tag|tag)\s*=\s*([A-Z]{3})\b", clean):
            add("tag", m.group(1), p)
        for m in re.finditer(r"add_to_faction\s*=\s*([A-Z]{3})\b", clean):
            add("tag", m.group(1), p)
        for m in re.finditer(r"(?m)^\s*has_government\s*=\s*([A-Za-z_\-]+)", clean):
            add("ideology", m.group(1), p)
        for m in re.finditer(r"(?m)^\s*ideology\s*=\s*([A-Za-z_\-]+)", clean):
            add("ideology", m.group(1), p)
        for m in re.finditer(r"(?:country_event|news_event)\s*=\s*\{\s*id\s*=\s*([A-Za-z0-9_.]+)", clean):
            add("event", m.group(1), p)
        for m in re.finditer(r"(?:country_event|news_event)\s*=\s*([A-Za-z0-9_]+\.[0-9]+)", clean):
            add("event", m.group(1), p)
        for m in re.finditer(r"(?m)^\s*(md2026_[a-z0-9_]+)\s*=\s*yes", clean):
            add("effect", m.group(1), p)
    return ref


def check_bookmark(sets):
    path = os.path.join(REPO, "common", "bookmarks", "md2026_bookmark.txt")
    if not os.path.exists(path):
        return
    text = rebase.strip_comments(rebase.read(path))
    for tag in re.findall(r'(?m)^\s*"([A-Z]{3})"\s*=', text):
        if tag not in sets["tag"]:
            ERRORS["bookmark tag"].append(f"{tag} (nie ma w MD)")
    for m in re.finditer(r"(?s)ideas\s*=\s*\{(.*?)\}", text):
        for idea in m.group(1).split():
            if idea not in sets["idea"]:
                ERRORS["bookmark idea"].append(idea)
    for m in re.finditer(r"(?s)focuses\s*=\s*\{(.*?)\}", text):
        for f in m.group(1).split():
            if f not in sets["focus"]:
                ERRORS["bookmark focus"].append(f)


def check_duplicate_focus_ids(md, sets):
    """Submod focus files that are not overriding an MD file must not redefine MD ids."""
    md_ids = set()
    for p in files(os.path.join(md, "common", "national_focus")):
        md_ids |= set(re.findall(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_\-\.]+)", rebase.read(p)))
    for p in files(os.path.join(REPO, "common", "national_focus")):
        if os.path.exists(os.path.join(md, "common", "national_focus", os.path.basename(p))):
            continue  # intentional override
        dup = set(re.findall(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_\-\.]+)", rebase.read(p))) & md_ids
        if dup:
            WARNINGS["duplicate focus id"].append(f"{rel(p)}: {len(dup)} (np. {sorted(dup)[0]})")


def check_loc_duplicates():
    for p in files(os.path.join(REPO, "localisation"), ".yml"):
        text = rebase.read(p)
        keys = re.findall(r"(?m)^\s*([A-Za-z0-9_.\-]+):\d*\s", text)
        for k, n in Counter(keys).items():
            if n > 1:
                WARNINGS["duplicate loc key"].append(f"{rel(p)}: {k} ({n}x)")
        if "\ufffd" in text:
            WARNINGS["loc encoding"].append(f"{rel(p)}: zawiera uszkodzone znaki (U+FFFD)")


SCOPE_KEYWORDS = {"ROOT", "PREV", "FROM", "THIS", "OWNER", "CONTROLLER", "CAPITAL", "OVERLORD", "yes", "no"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=os.environ.get("MD_PATH", rebase.DEFAULT_MD))
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    md = args.md
    sets = load_sets(md)
    print(f"MD: {len(sets['tech'])} tech | {len(sets['idea'])} idei | {len(sets['focus'])} focusow | "
          f"{len(sets['char'])} postaci | {len(sets['tag'])} tagow | {len(sets['event'])} eventow | "
          f"{len(sets['loc'])} kluczy loc")

    ref = scan_submod()
    md_override_basenames = set()
    for sub in ("common", "events", "history"):
        md_root = os.path.join(md, sub)
        for dirpath, _, names in os.walk(md_root):
            for n in names:
                md_override_basenames.add(os.path.relpath(os.path.join(dirpath, n), md_root))

    def is_md_side(where):
        """True when every file reporting this reference is an MD override."""
        for f in where:
            relpath = f.split(os.sep, 1)[1] if os.sep in f else f
            if relpath not in md_override_basenames:
                return False
        return True

    kinds = {
        "tech": "technologie", "idea": "idee", "focus": "focusy", "char": "postacie",
        "tag": "tagi", "ideology": "ideologie", "event": "eventy",
        "effect": "scripted effects",
    }
    for kind, label in kinds.items():
        pool = sets.get(kind, set())
        if kind == "effect":
            pool = sets["effect"] | sets["trigger"]
        unknown = {k: v for k, v in ref[kind].items() if k not in pool and k not in SCOPE_KEYWORDS}
        total = len(ref[kind])
        status = "OK" if not unknown else f"{len(unknown)} NIEZNANYCH"
        print(f"  {label:22} {total:5} referencji | {status}")
        for name, where in sorted(unknown.items()):
            # case-only mismatch of an existing id (MD's own bug, fixed in our overrides)
            lower = {x.lower(): x for x in pool}
            if name.lower() in lower:
                WARNINGS["case mismatch (MD)"].append(f"{name} -> {lower[name.lower()]}  ({sorted(where)[0]})")
            elif is_md_side(where):
                WARNINGS["MD-side reference"].append(f"{name}  ({sorted(where)[0]})")
            else:
                ERRORS[label].append(f"{name}  ({sorted(where)[0]})")

    check_bookmark(sets)
    check_duplicate_focus_ids(md, sets)
    check_loc_duplicates()

    print()
    if ERRORS:
        print("=== BLEDY ===")
        for kind, items in ERRORS.items():
            print(f"  [{kind}] {len(items)}")
            if not args.quiet:
                for it in items[:20]:
                    print(f"     {it}")
    if WARNINGS:
        print("=== OSTRZEZENIA ===")
        for kind, items in WARNINGS.items():
            print(f"  [{kind}] {len(items)}")
            if not args.quiet:
                for it in items[:20]:
                    print(f"     {it}")
    if not ERRORS and not WARNINGS:
        print("Brak bledow i ostrzezen.")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
