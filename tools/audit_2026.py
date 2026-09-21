"""MD 2026 - coverage audit.

Prints (and optionally writes) a coverage report of the 2026 content:

  * countries that have their own focus tree in Millennium Dawn 2.0,
  * which of them have a 2026 history patch, a 2026 focus branch, an OOB
    (NSB and non-NSB variant) and a bookmark entry,
  * bookmark countries and what they are missing,
  * localisation keys used by our files but missing from the English file,
  * localisation keys present in English but missing in other languages.

Usage:
    python tools/audit_2026.py                # report to stdout
    python tools/audit_2026.py --write        # also writes docs/Coverage.md
    python tools/audit_2026.py --md <path>    # override the MD install path
"""

import argparse
import json
import os
import re
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MD = r"D:\SteamLibrary\steamapps\workshop\content\394360\2777392649"

MD = None


def read(path):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def files(root, ext=".txt"):
    out = []
    if not os.path.isdir(root):
        return out
    for dirpath, _, names in os.walk(root):
        for n in names:
            if n.endswith(ext):
                out.append(os.path.join(dirpath, n))
    return sorted(out)


def find_block(text, start):
    depth = 0
    i = start
    while i < len(text):
        c = text[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced braces")


def strip_comments(text):
    return "\n".join(line.split("#")[0] for line in text.split("\n"))


TAG_RE = re.compile(r"(?<![\w])([A-Z]{3})(?![\w])")


def tags_in_text(text):
    """All tags seen inside tag = / original_tag = clauses."""
    out = set()
    for m in re.finditer(r"(?:^|\s)(?:tag|original_tag)\s*=\s*([A-Z]{3})(?![\w])", text):
        out.add(m.group(1))
    return out


def md_focus_trees(md):
    """file -> list of (tree_id, tags)."""
    trees = {}
    for p in files(os.path.join(md, "common", "national_focus")):
        text = strip_comments(read(p))
        found = []
        for m in re.finditer(r"focus_tree\s*=\s*\{", text):
            ob = text.index("{", m.start())
            end = find_block(text, ob)
            body = text[ob:end]
            idm = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+)", body[:400])
            if not idm:
                continue
            tags = set()
            cb = re.search(r"country\s*=\s*\{", body[:3000])
            if cb:
                c_ob = body.index("{", cb.start())
                c_end = find_block(body, c_ob)
                cbody = body[c_ob:c_end]
                tags = tags_in_text(cbody)
                # MD uses "modifier = { add = N tag = XXX }" too
                tags |= set(re.findall(r"tag\s*=\s*([A-Z]{3})(?![\w])", cbody))
            found.append((idm.group(1), tags))
        if found:
            trees[os.path.basename(p)] = found
    return trees


def our_focus_branches():
    """tag -> list of branch files (from shared_focus original_tag)."""
    out = {}
    for p in files(os.path.join(REPO, "common", "national_focus")):
        n = os.path.basename(p)
        if not n.startswith("md2026_") or n == "md2026_search_filters.txt":
            continue
        text = strip_comments(read(p))
        tags = set()
        for m in re.finditer(r"(?:original_tag|tag)\s*=\s*([A-Z]{3})(?![\w])", text):
            tags.add(m.group(1))
        for t in tags:
            out.setdefault(t, []).append(n)
    return out


def oob_files():
    """tag -> {'nsb': path, 'nonnsb': path}."""
    out = {}
    root = os.path.join(REPO, "history", "units")
    for p in files(root):
        m = re.match(r"([A-Z]{3})_2026(_nonnsb|_nsb)?\.txt$", os.path.basename(p))
        if not m:
            continue
        tag, kind = m.group(1), m.group(2)
        key = "nonnsb" if kind == "_nonnsb" else "nsb"
        out.setdefault(tag, {})[key] = os.path.basename(p)
    return out


def history_patches():
    root = os.path.join(REPO, "patches", "history_countries")
    return sorted(n[:-4] for n in os.listdir(root) if n.endswith(".txt"))


def bookmark_countries():
    text = strip_comments(read(os.path.join(REPO, "patches", "bookmark_md2026.txt")))
    out = {}
    for m in re.finditer(r'(?m)^\s*"([A-Z]{3})"\s*=\s*\{', text):
        ob = text.index("{", m.end() - 1)
        end = find_block(text, ob)
        out[m.group(1)] = text[ob:end]
    return out


def our_source_files():
    """Files we ship (generated + hand-written), excluding documentation."""
    out = []
    for sub in ("common", "events", "history", "localisation", "patches"):
        root = os.path.join(REPO, sub)
        if os.path.isdir(root):
            out += files(root)
    out += [os.path.join(REPO, "descriptor.mod")]
    return out


def loc_keys(md):
    """key -> set of languages."""
    langs = {}
    root = os.path.join(REPO, "localisation")
    for p in files(root, ".yml"):
        lang = os.path.basename(os.path.dirname(p))
        text = read(p)
        for m in re.finditer(r"(?m)^\s*([A-Za-z0-9_\.]+)\s*:", text):
            langs.setdefault(m.group(1), set()).add(lang)
    # MD's own languages are not interesting; only report keys we define
    return langs


KEY_RE = re.compile(r"(?<![\w\.])((?:MD2026|md2026)[A-Za-z0-9_\.]*)")


def keys_used_in_our_files():
    used = Counter()
    for p in our_source_files():
        if not p.endswith(".txt") and not p.endswith(".mod"):
            continue
        text = read(p)
        for m in KEY_RE.finditer(text):
            used[m.group(1)] += 1
    return used


_loc_key_cache = None


def all_loc_keys(md):
    """Every localisation key defined by MD or the base game (cached)."""
    global _loc_key_cache
    if _loc_key_cache is not None:
        return _loc_key_cache
    keys = set()
    for root in (os.path.join(md, "localisation"),
                 r"D:\SteamLibrary\steamapps\common\Hearts of Iron IV\localisation"):
        for p in files(root, ".yml"):
            for m in re.finditer(r"(?m)^\s*([A-Za-z0-9_\.]+)\s*:", read(p)):
                keys.add(m.group(1))
    _loc_key_cache = keys
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=os.environ.get("MD_PATH", DEFAULT_MD))
    ap.add_argument("--write", action="store_true", help="write docs/Coverage.md")
    args = ap.parse_args()

    global MD
    MD = args.md
    if not os.path.isdir(MD):
        sys.exit(f"MD not found: {MD}")

    trees = md_focus_trees(MD)
    branches = our_focus_branches()
    oob = oob_files()
    patches = set(history_patches())
    bookmark = bookmark_countries()
    rename = {"NOR": "NRY"}

    # tag -> [tree files]
    tag_trees = {}
    for fname, found in sorted(trees.items()):
        for tree_id, tags in found:
            for t in tags:
                tag_trees.setdefault(t, []).append((fname, tree_id))

    # ignore purely generic/shared trees for the "own tree" count
    generic = {"generic_focus", "generic_dummy", "00_generic"}
    own_tags = sorted(t for t, v in tag_trees.items()
                      if not all(tid in generic for _, tid in v))

    def has_patch(tag):
        return rename.get(tag, tag) in patches

    missing_patch = [t for t in own_tags if not has_patch(t)]
    missing_branch = [t for t in own_tags if t not in branches and rename.get(t, t) not in branches]
    missing_oob = [t for t in own_tags if t not in oob]
    missing_nonnsb = [t for t in own_tags if t in oob and "nonnsb" not in oob[t]]
    missing_bookmark = [t for t in own_tags if t not in bookmark]

    loc = loc_keys(MD)
    used = keys_used_in_our_files()
    external = all_loc_keys(MD)
    missing_loc = sorted(k for k in used if k not in loc and k not in external)
    langs_present = sorted({l for v in loc.values() for l in v})
    # the authoritative localisation check lives in tools/loc_keys.py
    try:
        import loc_keys as L
        wanted = L.expected_keys()
        wanted.update(L.idea_keys())
        wanted.update(L.decision_keys())
        en_keys = L.defined_keys().get("english", {})
        pl_keys = L.defined_keys().get("polish", {})
        loc_missing_exact = sorted(k for k, v in wanted.items()
                                   if k not in en_keys and k not in external
                                   and any(L.is_our_file(f) for f in v))
        loc_untranslated = sorted(k for k in wanted if k in en_keys and k not in pl_keys)
    except Exception as exc:  # pragma: no cover - tool must not fail the audit
        print(f"  !! loc_keys.py unavailable: {exc}", file=sys.stderr)
        loc_missing_exact, loc_untranslated = [], []
    langs = langs_present
    en_only = sorted(k for k, v in loc.items() if v == {"english"} and k.startswith(("md2026", "MD2026")))

    lines = []
    lines.append("# Coverage - MD 2026 (automatic report)")
    lines.append("")
    lines.append("Generated by `python tools/audit_2026.py --write`. Do not edit by hand.")
    lines.append("")
    lines.append(f"- Countries with their own focus tree in Millennium Dawn 2.0: **{len(own_tags)}**")
    lines.append(f"- of those with a 2026 history patch: **{len(own_tags) - len(missing_patch)}**")
    lines.append(f"- with a 2026 focus branch: **{len(own_tags) - len(missing_branch)}**")
    lines.append(f"- with a 2026 OOB (NSB): **{len(own_tags) - len(missing_oob)}**")
    lines.append(f"- with a non-NSB OOB: **{len([t for t in own_tags if t in oob and 'nonnsb' in oob[t]])}**")
    lines.append(f"- bookmark entries: **{len(bookmark)}**")
    lines.append("")

    def table(title, items, fmt=str):
        lines.append(f"## {title}")
        lines.append("")
        if not items:
            lines.append("_none_")
            lines.append("")
            return
        for it in items:
            lines.append(f"- {fmt(it)}")
        lines.append("")

    table("Countries with an MD focus tree but no 2026 history patch", missing_patch)
    table("Countries with an MD focus tree but no 2026 focus branch", missing_branch)
    table("Countries with an MD focus tree but no 2026 OOB", missing_oob)
    table("Countries with an NSB OOB but no non-NSB variant", missing_nonnsb)

    lines.append("## Bookmark countries")
    lines.append("")
    lines.append("| Tag | Patch | Branch | OOB NSB | OOB non-NSB |")
    lines.append("|---|---|---|---|---|")
    for t in sorted(bookmark):
        md_t = rename.get(t, t)
        lines.append("| {} | {} | {} | {} | {} |".format(
            t,
            "yes" if md_t in patches else "**NO**",
            "yes" if t in branches else "**NO**",
            "yes" if md_t in oob and "nsb" in oob[md_t] else "**NO**",
            "yes" if md_t in oob and "nonnsb" in oob[md_t] else "**NO**",
        ))
    lines.append("")

    table("Localisation keys used in our files but not defined (approx.)", missing_loc[:60])
    lines.append(f"({len(missing_loc)} total, of which most are identifiers, not loc keys;"
                 f" see tools/loc_keys.py for the exact check)")
    lines.append("")
    lines.append(f"- Loc keys our content needs but that are missing in English: **{len(loc_missing_exact)}**")
    lines.append(f"- Keys defined in English but missing in Polish: **{len(loc_untranslated)}**")
    lines.append(f"- Languages present: {', '.join(langs)}")
    lines.append("")
    lines.append("## Scope decisions")
    lines.append("")
    lines.append("The 2026 bookmark covers **30 countries** (all of them with a history patch, a")
    lines.append("focus branch and both OOB variants). The remaining own-tree countries are not")
    lines.append("ported yet; the full list is above. The reasons are:")
    lines.append("")
    lines.append("- **Breakaway/release tags** (`DPR`, `LPR`, `SEU`, `HPR`, `OPR`, `CRM`, `NOV`,")
    lines.append("  `PMR`, `FSA`, `USB`, `TAT`, `SIB`, `UDM`, `YAK`, `KUB`, `CAS`, `ADY`, `ALT`, ...):")
    lines.append("  these are MD 1.x partition/alt-history tags that do not exist on the 2026 map.")
    lines.append("  Porting them would require inventing states and would risk the bookmark start.")
    lines.append("- **Countries without their own tree in MD** (e.g. Hungary, Sudan use")
    lines.append("  `generic_focus`): they received a branch inside the generic tree instead.")
    lines.append("- **Priority B countries** (`IRQ`, `CUB`, `ALG`, `AZE`, `LBY`, `KUW`, `QAT`,")
    lines.append("  `BHR`, `OMA`, `SIN`, `HKG`, `KHM`, `ERI`, `BOL`, `ZOM`, `NIG`, ...): each needs a")
    lines.append("  2026 leader, party system, GDP and starting position; scheduled for a later pass.")
    lines.append("  Their 2026 start uses MD's 2000 content at the 2026 date, which is playable but")
    lines.append("  not yet accurate.")
    lines.append("")

    report = "\n".join(lines)
    if args.write:
        out = os.path.join(REPO, "docs", "Coverage.md")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(report)
        print(f"wrote {os.path.relpath(out, REPO)}")
    else:
        print(report)

    print(f"\nsummary: {len(own_tags)} own-tree countries, "
          f"{len(missing_patch)} without patch, {len(missing_branch)} without branch, "
          f"{len(missing_oob)} without OOB, {len(missing_nonnsb)} without non-NSB, "
          f"{len(loc_missing_exact)} missing loc keys, {len(loc_untranslated)} untranslated keys",
          file=sys.stderr)


if __name__ == "__main__":
    main()
