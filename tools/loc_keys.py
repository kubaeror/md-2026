#!/usr/bin/env python3
"""Localisation coverage for the submod's own content.

Extracts the localisation keys our files actually need (event titles/descs,
option names, focus/idea/decision ids + _desc, tooltips, ...) and compares
them with the keys defined in localisation/<language>/*.yml and with the keys
Millennium Dawn / the base game already define.

Usage:
    python tools/loc_keys.py                 # report
    python tools/loc_keys.py --lang polish   # report + keys missing in PL
    python tools/loc_keys.py --write-missing # append empty EN keys for missing ones
"""

import argparse
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rebase  # noqa: E402

REPO = rebase.REPO
LOC_DIR = os.path.join(REPO, "localisation")
VANILLA = rebase.VANILLA
_external_cache = None

CONTENT_DIRS = ("common", "events", "patches")

# loc positions: every one of these takes a localisation key
EXPLICIT_RE = re.compile(
    r"(?m)^[ \t]*(?:title|desc|text|tooltip|custom_effect_tooltip|custom_trigger_tooltip|"
    r"effect_tooltip|trigger_tooltip|remove_effect_tooltip|select_effect|localization_key|"
    r"special_project_tooltip|mission_description|button_text|complete_effect_tooltip|"
    r"remove_effect_tooltip|target_array_tooltip)[ \t]*=[ \t]*"
    r"(?:\"([A-Za-z0-9_\.\-]+)\"|([A-Za-z0-9_\.\-]+))"
)

# bookmark fields that take loc keys
BOOKMARK_RE = re.compile(r"(?m)^[ \t]*(?:name|desc|history)[ \t]*=[ \t]*\"?([A-Za-z0-9_\.\-]+)\"?")

NOT_KEYS = re.compile(r"^(GFX_|gfx/|SPRITE|sprite)")


def is_our_file(relpath):
    """True when a file is content of this submod (not an MD override)."""
    base = os.path.basename(relpath)
    if base.startswith("md2026_"):
        return True
    if relpath.startswith("events" + os.sep) or relpath.startswith("patches"):
        return True
    if relpath.startswith("history" + os.sep):
        return True
    return False

# fields that make a block look like a decision (a category has none of these)
DECISION_MARKERS = ("complete_effect", "remove_effect", "fire_only_once", "days_remove",
                    "days_re_enable", "decision_category", "is_available", "targets",
                    "activation", "custom_cost_text", "select_effect", "complete_effect_tooltip")


def content_files():
    out = []
    for sub in CONTENT_DIRS:
        root = os.path.join(REPO, sub)
        for dirpath, _, names in os.walk(root):
            for n in names:
                if n.endswith(".txt"):
                    out.append(os.path.join(dirpath, n))
    return sorted(out)


def block_children(text):
    """(name, indent, start, end) for every 'name = { ... }' block."""
    out = []
    for m in re.finditer(r"(?m)^([ \t]*)([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", text):
        ob = text.index("{", m.end() - 1)
        try:
            end = rebase.find_block(text, ob)
        except ValueError:
            continue
        out.append((m.group(2), len(m.group(1)), m.start(), end))
    return out


def direct_children(blocks, parent_start, parent_end):
    """Blocks nested exactly one level below the parent."""
    inner = [b for b in blocks if parent_start < b[2] and b[3] <= parent_end]
    if not inner:
        return []
    child_indent = min(b[1] for b in inner)
    return [b for b in inner if b[1] == child_indent]


def is_decision(body):
    return any(re.search(r"(?m)^[ \t]*" + k + r"\s*=", body) for k in DECISION_MARKERS)


def defined_keys():
    """language -> {key: line}."""
    out = defaultdict(dict)
    for dirpath, _, names in os.walk(LOC_DIR):
        lang = os.path.basename(dirpath)
        for n in names:
            if not n.endswith(".yml"):
                continue
            with open(os.path.join(dirpath, n), encoding="utf-8-sig", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    m = re.match(r"^\s*([A-Za-z0-9_\.\-]+):\d*\s", line)
                    if m:
                        out[lang][m.group(1)] = i
    return out


def external_keys(md):
    """Keys defined by Millennium Dawn or the base game."""
    global _external_cache
    if _external_cache is not None:
        return _external_cache
    keys = set()
    for root in (os.path.join(md, "localisation"), os.path.join(VANILLA, "localisation")):
        for dirpath, _, names in os.walk(root):
            for n in names:
                if not n.endswith(".yml"):
                    continue
                with open(os.path.join(dirpath, n), encoding="utf-8-sig", errors="replace") as f:
                    for line in f:
                        m = re.match(r"^\s*([A-Za-z0-9_\.\-]+):\d*\s", line)
                        if m:
                            keys.add(m.group(1))
    _external_cache = keys
    return keys


def expected_keys():
    """key -> set of files that need it."""
    need = defaultdict(set)

    def add(key, path):
        if not key or NOT_KEYS.match(key):
            return
        need[key].add(os.path.relpath(path, REPO))

    for p in content_files():
        text = rebase.read(p)
        stripped = rebase.strip_comments(text)
        for m in EXPLICIT_RE.finditer(stripped):
            add(m.group(1) or m.group(2), p)
        if os.sep + "bookmarks" + os.sep in p:
            for m in BOOKMARK_RE.finditer(stripped):
                add(m.group(1), p)
        # focus ids need <id> and <id>_desc
        for m in re.finditer(r"(?m)^\s*(?:focus|shared_focus|joint_focus)\s*=\s*\{", stripped):
            ob = stripped.index("{", m.end() - 1)
            body = stripped[ob:rebase.find_block(stripped, ob)]
            idm = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_\-\.]+)", body[:400])
            if idm:
                add(idm.group(1), p)
                add(idm.group(1) + "_desc", p)
        # idea ids need <id> and <id>_desc (ideas files only) - see idea_keys()
        # event options: name = KEY only inside option = { }
        if os.sep + "events" + os.sep in p:
            for cat, _, cstart, cend in block_children(stripped):
                if cat != "option":
                    continue
                body = stripped[cstart:cend]
                nm = re.search(r"(?m)^\s*name\s*=\s*\"?([A-Za-z0-9_\.\-]+)\"?", body)
                if nm:
                    add(nm.group(1), p)
            for m in re.finditer(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+\.[0-9]+)\s*$", stripped):
                add(m.group(1) + ".t", p)
                add(m.group(1) + ".d", p)
    return need


def idea_keys():
    """Ideas are localised by their id (+ _desc)."""
    need = defaultdict(set)
    for p in content_files():
        if os.sep + "ideas" + os.sep not in p:
            continue
        rel = os.path.relpath(p, REPO)
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r"(?m)^\s*ideas\s*=\s*\{", text):
            ob = text.index("{", m.end() - 1)
            end = rebase.find_block(text, ob)
            blocks = block_children(text[ob + 1:end])
            for cat, _, cstart, cend in direct_children(blocks, 0, end - ob - 1):
                for idea, _, _, _ in direct_children(blocks, cstart, cend):
                    need[idea].add(rel)
                    need[idea + "_desc"].add(rel)
    return need


def decision_block(name, start, end, text):
    """True when the block's direct fields mark it as a decision."""
    body = text[start:end]
    kids = direct_children(block_children(body), 0, len(body))
    return any(k[0] in DECISION_MARKERS for k in kids)


def decision_keys():
    """Decisions need <id>/<id>_desc, categories need <id>/<id>_desc."""
    need = defaultdict(set)
    root = os.path.join(REPO, "common", "decisions")
    for dirpath, _, names in os.walk(root):
        for n in names:
            if not n.endswith(".txt"):
                continue
            p = os.path.join(dirpath, n)
            rel = os.path.relpath(p, REPO)
            text = rebase.strip_comments(rebase.read(p))
            top = [b for b in block_children(text) if b[1] == 0]
            for name, _, start, end in top:
                if decision_block(name, start, end, text):
                    need[name].add(rel)
                    need[name + "_desc"].add(rel)
                    continue
                # a category: <id>/<id>_desc plus its decision children
                need[name].add(rel)
                need[name + "_desc"].add(rel)
                body = text[start:end]
                for cname, _, cstart, cend in direct_children(block_children(body), 0, len(body)):
                    if decision_block(cname, cstart, cend, body):
                        need[cname].add(rel)
                        need[cname + "_desc"].add(rel)
    return need


def duplicate_keys():
    """(key, file, line) for keys defined twice in the same localisation file."""
    out = []
    for dirpath, _, names in os.walk(LOC_DIR):
        for n in names:
            if not n.endswith(".yml"):
                continue
            path = os.path.join(dirpath, n)
            seen = {}
            with open(path, encoding="utf-8-sig", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    m = re.match(r"^\s*([A-Za-z0-9_\.\-]+):\d*\s", line)
                    if not m:
                        continue
                    key = m.group(1)
                    if key in seen:
                        out.append((key, os.path.relpath(path, REPO), i))
                    seen[key] = i
    return out


def prune_unused(unused):
    """Delete loc lines whose key appears nowhere outside localisation/."""
    corpus = []
    for sub in ("common", "events", "history", "patches", "docs", "tools"):
        root = os.path.join(REPO, sub)
        for dirpath, _, names in os.walk(root):
            for n in names:
                if n.endswith((".txt", ".json", ".csv", ".md", ".py", ".mod")):
                    corpus.append(os.path.join(dirpath, n))
    corpus_text = "\n".join(rebase.read(p) for p in corpus)
    dead = {k for k in unused if k not in corpus_text and not k.startswith("l_")}
    if not dead:
        return 0
    removed = 0
    for dirpath, _, names in os.walk(LOC_DIR):
        for n in names:
            if not n.endswith(".yml"):
                continue
            path = os.path.join(dirpath, n)
            with open(path, encoding="utf-8-sig", errors="replace") as f:
                lines = f.readlines()
            keep = [l for l in lines
                    if not (re.match(r"^\s*([A-Za-z0-9_\.\-]+):\d*\s", l)
                            and re.match(r"^\s*([A-Za-z0-9_\.\-]+):\d*\s", l).group(1) in dead)]
            if len(keep) != len(lines):
                removed += len(lines) - len(keep)
                with open(path, "w", encoding="utf-8-sig", newline="\n") as f:
                    f.writelines(keep)
    return removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="polish")
    ap.add_argument("--md", default=os.environ.get("MD_PATH", rebase.DEFAULT_MD))
    ap.add_argument("--write-missing", action="store_true")
    ap.add_argument("--prune-unused", action="store_true",
                    help="remove keys that appear only in localisation files")
    ap.add_argument("--limit", type=int, default=60)
    args = ap.parse_args()

    langs = defined_keys()
    if "english" not in langs:
        sys.exit("no english localisation found")
    en = langs["english"]

    need = expected_keys()
    need.update(idea_keys())
    need.update(decision_keys())
    external = external_keys(args.md)

    missing = {}
    md_side_missing = {}
    for k, v in need.items():
        if k in en or k in external:
            continue
        if any(is_our_file(f) for f in v):
            missing[k] = v
        else:
            md_side_missing[k] = v
    unused = {k: v for k, v in en.items() if k not in need}

    print(f"potrzebne klucze: {len(need)}")
    print(f"zdefiniowane (EN): {len(en)}")
    print(f"zdefiniowane w MD/vanilla: {len(external & set(need))}")
    print(f"brakujace w EN: {len(missing)}")
    for k in sorted(missing)[:args.limit]:
        print(f"   {k:52} {sorted(missing[k])[:2]}")
    if len(missing) > args.limit:
        print(f"   ... i {len(missing) - args.limit} wiecej")
    if md_side_missing:
        print(f"brakujace w EN, uzywane tylko przez pliki MD (nie nasze): {len(md_side_missing)}")
        for k in sorted(md_side_missing)[:6]:
            print(f"   {k:52} {sorted(md_side_missing[k])[:2]}")
    print(f"nieuzywane w EN: {len(unused)}")
    for k in sorted(unused)[:30]:
        print(f"   {k}")
    if len(unused) > 30:
        print(f"   ... i {len(unused) - 30} wiecej")

    if args.lang in langs:
        missing_lang = sorted(k for k in need if k in en and k not in langs[args.lang])
        print(f"\nbrakujace w {args.lang}: {len(missing_lang)} / {len(need)}")
        for k in missing_lang[:args.limit]:
            print(f"   {k}")
    else:
        print(f"\nbrak katalogu localisation/{args.lang}")

    if args.write_missing and missing:
        path = os.path.join(LOC_DIR, "english", "md2026_l_english.yml")
        with open(path, "a", encoding="utf-8-sig", newline="\n") as f:
            f.write("\n ### MISSING KEYS (generated stub) ###\n")
            for k in sorted(missing):
                f.write(f' {k}:0 ""\n')
        print(f"\ndopisano {len(missing)} pustych kluczy do {os.path.relpath(path, REPO)}")

    if args.prune_unused:
        dead = prune_unused(unused)
        print(f"\nusunieto {dead} nieuzywanych kluczy z {os.path.relpath(LOC_DIR, REPO)}")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
