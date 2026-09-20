"""MD 2026 Rework - rebase tool.

Keeps every file that overrides Millennium Dawn generated from:
  * the currently installed MD (source of truth for 2000-01-01 state), and
  * the hand-maintained 2026 patches in patches/.

Usage:
    python tools/rebase.py extract     # one-time: split old copies into patches/
    python tools/rebase.py generate    # rebuild all MD overrides from MD + patches
    python tools/rebase.py focus       # rebuild focus tree overrides only
    python tools/rebase.py history     # rebuild history/countries + history/states

MD path can be overridden with --md <path> or the MD_PATH env var.
"""

import argparse
import csv
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


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # HoI4 script files must NOT have a UTF-8 BOM (the parser reports "Unexpected token: ?")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def strip_comments(text):
    return "\n".join(line.split("#")[0] for line in text.split("\n"))


def find_block(text, start):
    """Given index of an opening '{', return index just past its matching '}'."""
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


def extract_dated_block(text, date):
    """Return the 'YYYY.M.D = { ... }' block (with leading comments) or None."""
    pat = re.compile(r"^\s*" + re.escape(date) + r"\s*=\s*\{", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return None
    open_brace = text.index("{", m.start())
    end = find_block(text, open_brace)
    # include trailing comment lines directly above the date line
    start = m.start()
    lines = text[:start].split("\n")
    k = len(lines) - 1
    while k > 0 and lines[k - 1].strip().startswith("#"):
        k -= 1
    start = len("\n".join(lines[:k])) + (1 if k > 0 else 0)
    return text[start:end]


# --------------------------------------------------------------------------
# extract: old full copies -> patches (2026 delta only)
# --------------------------------------------------------------------------

def extract_history_countries():
    src_dir = os.path.join(REPO, "history", "countries")
    dst_dir = os.path.join(REPO, "patches", "history_countries")
    os.makedirs(dst_dir, exist_ok=True)
    n = 0
    for name in sorted(os.listdir(src_dir)):
        if not name.endswith(".txt"):
            continue
        tag = name.split(" ")[0]
        text = read(os.path.join(src_dir, name))
        block = extract_dated_block(text, "2026.1.1")
        if not block:
            print(f"  !! no 2026.1.1 block in {name}")
            continue
        write(os.path.join(dst_dir, tag + ".txt"), block.rstrip() + "\n")
        n += 1
    print(f"extracted {n} country patches -> patches/history_countries/")


def extract_history_states():
    src_dir = os.path.join(REPO, "history", "states")
    dst_dir = os.path.join(REPO, "patches", "history_states")
    os.makedirs(dst_dir, exist_ok=True)
    n = 0
    for name in sorted(os.listdir(src_dir)):
        if not name.endswith(".txt"):
            continue
        state_id = name.split("-")[0].strip()
        text = read(os.path.join(src_dir, name))
        block = extract_dated_block(text, "2026.1.1")
        if not block:
            print(f"  !! no 2026.1.1 block in {name}")
            continue
        write(os.path.join(dst_dir, state_id + ".txt"), block.rstrip() + "\n")
        n += 1
    print(f"extracted {n} state patches -> patches/history_states/")


# --------------------------------------------------------------------------
# focus trees
# --------------------------------------------------------------------------

def focus_inject_config():
    path = os.path.join(REPO, "patches", "focus_inject.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def md_focus_file_by_tree_id(md, tree_id):
    """Find the MD national_focus file that defines focus_tree with this id."""
    root = os.path.join(md, "common", "national_focus")
    for name in sorted(os.listdir(root)):
        if not name.endswith(".txt"):
            continue
        text = read(os.path.join(root, name))
        for m in re.finditer(r"focus_tree\s*=\s*\{", text):
            open_brace = text.index("{", m.start())
            end = find_block(text, open_brace)
            head = text[open_brace:end][:400]
            if re.search(r"(?m)^\s*id\s*=\s*" + re.escape(tree_id) + r"\s*$", head):
                return name
    return None


MINIMAL_BOOKMARK = """bookmarks = {
\tbookmark = {
\t\tname = "MD_2026"
\t\tdesc = "MD_2026_DESC"
\t\tdate = 2026.1.1.12
\t\tpicture = "GFX_select_date_2000"
\t\tdefault_country = "USA"
\t\tdefault = no

\t\t"USA" = {
\t\t\thistory = "USA_MILLENNIUM_DAWN_DESC"
\t\t\tideology = democratic
\t\t}

\t\t"---" = {
\t\t\tminor = yes
\t\t\thistory = "OTHER_MILLENNIUM_DAWN_DESC"
\t\t}

\t\teffect = {
\t\t\trandomize_weather = 22345
\t\t}
\t}
}
"""


def generate_bookmark():
    """Writes the bookmark file. debug.json minimal_bookmark switches to a stub."""
    dst = os.path.join(REPO, "common", "bookmarks", "md2026_bookmark.txt")
    if debug_flags().get("minimal_bookmark"):
        write(dst, "# BISECT: minimal bookmark (no country content)\n" + MINIMAL_BOOKMARK)
        print("  bookmark: minimal diagnostic bookmark written")
        return
    src = os.path.join(REPO, "patches", "bookmark_md2026.txt")
    if os.path.exists(src):
        write(dst, read(src))
        print("  bookmark: restored from patches/bookmark_md2026.txt")


def rebase_focus(md):
    """Rebuild focus tree overrides: copy the MD file and inject shared focuses
    into every tree the config assigns a branch to."""
    out_dir = os.path.join(REPO, "common", "national_focus")
    flags = debug_flags()
    skip_branches = flags.get("skip_focus_branches", False)
    # move branch definitions out of the way / restore them
    for name in os.listdir(out_dir):
        if skip_branches and name.startswith("md2026_") and name.endswith("_focus.txt"):
            os.rename(os.path.join(out_dir, name), os.path.join(out_dir, name + ".disabled"))
        elif not skip_branches and name.startswith("md2026_") and name.endswith("_focus.txt.disabled"):
            os.rename(os.path.join(out_dir, name), os.path.join(out_dir, name[:-len(".disabled")]))
    if skip_branches:
        print("  focus branches: DISABLED (diagnostic build)")
    cfg = {} if skip_branches else focus_inject_config()  # tree_id -> [shared focus ids]
    out_dir = os.path.join(REPO, "common", "national_focus")
    root = os.path.join(md, "common", "national_focus")
    generated = set()
    for name in sorted(os.listdir(root)):
        if not name.endswith(".txt"):
            continue
        text = read(os.path.join(root, name))
        text = apply_fixups(text, *md_reference_sets(md))
        text = fix_portraits_auto(text, md)
        blocks = []
        for m in re.finditer(r"focus_tree\s*=\s*\{", text):
            ob = text.index("{", m.start())
            end = find_block(text, ob)
            head = text[ob:end][:400]
            idm = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+)", head)
            if idm and idm.group(1) in cfg and cfg[idm.group(1)]:
                indent = re.search(r"(?m)^(\s*)id", text[ob:ob + 400]).group(1)
                blocks.append((ob + idm.start(), idm.group(1), indent))
        if not blocks:
            continue
        for abs_id, tree_id, ind in reversed(blocks):
            line_end = text.index("\n", abs_id)
            ins = "\n" + "\n".join(f"{ind}shared_focus = {sid}" for sid in cfg[tree_id])
            text = text[:line_end] + ins + text[line_end:]
        write(os.path.join(out_dir, name), text)
        generated.add(name)
        print(f"  generated {name} ({', '.join(t for _, t, _ in blocks)})")
    missing = [t for t in cfg if t not in sum((md_tree_ids_in_file(md, n) for n in os.listdir(root) if n.endswith('.txt')), [])]
    for t in missing:
        print(f"  !! tree id not found in MD: {t}")
    return generated


def md_tree_ids_in_file(md, fname):
    """All focus_tree ids defined in an MD national_focus file."""
    text = read(os.path.join(md, "common", "national_focus", fname))
    ids = []
    for m in re.finditer(r"focus_tree\s*=\s*\{", text):
        ob = text.index("{", m.start())
        end = find_block(text, ob)
        idm = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+)", text[ob:end][:400])
        if idm:
            ids.append(idm.group(1))
    return ids


def cleanup_old_focus_copies(expected):
    out_dir = os.path.join(REPO, "common", "national_focus")
    removed = 0
    for name in sorted(os.listdir(out_dir)):
        if name.startswith("md2026_") or not name.endswith(".txt"):
            continue
        if name not in expected:
            os.remove(os.path.join(out_dir, name))
            removed += 1
            print(f"  removed obsolete copy {name}")
    return removed


# --------------------------------------------------------------------------
# technology effects (generated from MD's own tech tree)
# --------------------------------------------------------------------------

def children(text):
    """Return (name, body) for top-level 'name = { ... }' blocks only."""
    out = []
    i = 0
    n = len(text)
    pat = re.compile(r"([A-Za-z0-9_\-\.]+)\s*=\s*\{")
    while i < n:
        c = text[i]
        if (i == 0 or text[i - 1] in " \t\r\n") and (c.isalnum() or c == "_"):
            m = pat.match(text, i)
            if m:
                ob = text.index("{", m.start())
                end = find_block(text, ob)
                out.append((m.group(1), text[ob + 1:end - 1]))
                i = end
                continue
        i += 1
    return out


def parse_techs(md):
    root = os.path.join(md, "common", "technologies")
    techs = {}
    for name in sorted(os.listdir(root)):
        if not name.endswith(".txt"):
            continue
        text = strip_comments(read(os.path.join(root, name)))
        for m in re.finditer(r"technologies\s*=\s*\{", text):
            ob = text.index("{", m.start())
            end = find_block(text, ob)
            for tname, body in children(text[ob + 1:end - 1]):
                if tname.startswith("@"):
                    continue
                if re.search(r"allow\s*=\s*\{\s*always\s*=\s*no", body):
                    continue  # hidden tech (special projects)
                ym = re.search(r"start_year\s*=\s*(\d+)", body)
                year = int(ym.group(1)) if ym else 1936
                conds = []
                ab = re.search(r"allow_branch\s*=\s*\{", body)
                if ab:
                    aob = body.index("{", ab.start())
                    aend = find_block(body, aob)
                    inner = body[aob + 1:aend - 1]
                    neg = re.findall(r"NOT\s*=\s*\{([^{}]*)\}", inner)
                    for n in neg:
                        for d in re.findall(r'has_dlc\s*=\s*"([^"]+)"', n):
                            conds.append(("not", d))
                    rest = re.sub(r"NOT\s*=\s*\{[^{}]*\}", "", inner)
                    for d in re.findall(r'has_dlc\s*=\s*"([^"]+)"', rest):
                        conds.append(("has", d))
                techs[tname] = (year, tuple(sorted(set(conds))))
    return techs


BANDS = [(2005, 0, 2005), (2010, 2005, 2010), (2015, 2010, 2015),
         (2020, 2015, 2020), (2025, 2020, 2025), (2026, 2025, 2026)]


def _cond_limit(conds):
    parts = []
    for kind, dlc in conds:
        if kind == "has":
            parts.append(f'has_dlc = "{dlc}"')
        else:
            parts.append(f'NOT = {{ has_dlc = "{dlc}" }}')
    return " ".join(parts)


def generate_tech_effects(md):
    techs = parse_techs(md)
    lines = [
        "# MD2026 Technology Scripted Effects",
        "# GENERATED FILE - do not edit by hand.",
        "# Rebuild with: python tools/rebase.py tech",
        "#",
        "# Grants every Millennium Dawn technology up to a given year,",
        "# mirroring MD's own DLC gating. Tiers are compositions of the bands.",
        "",
    ]
    for band, lo, hi in BANDS:
        sel = {t: c for t, (y, c) in techs.items() if lo < y <= hi}
        lines.append(f"md2026_techs_{band} = {{")
        groups = {}
        for t, c in sel.items():
            groups.setdefault(c, []).append(t)
        # ungated first, then gated
        for conds in sorted(groups, key=lambda c: (len(c), c)):
            names = sorted(groups[conds])
            body = "\n".join(f"\t\t{t} = 1" for t in names)
            if not conds:
                lines.append("\tset_technology = {")
                lines.append(body)
                lines.append("\t}")
            else:
                lines.append(f"\tif = {{ limit = {{ {_cond_limit(conds)} }}")
                lines.append("\t\tset_technology = {")
                lines.append(body)
                lines.append("\t\t}")
                lines.append("\t}")
        lines.append("}")
        lines.append("")

    tiers = {
        "tier1_2026": ["2005", "2010", "2015", "2020", "2025", "2026"],
        "tier2_2026": ["2005", "2010", "2015", "2020", "2025"],
        "tier3_2026": ["2005", "2010", "2015", "2020"],
        "tier4_2026": ["2005", "2010", "2015"],
        "tier5_2026": ["2005", "2010"],
    }
    for tier, bands in tiers.items():
        lines.append(f"md2026_{tier}_techs = {{")
        for b in bands:
            lines.append(f"\tmd2026_techs_{b} = yes")
        lines.append("}")
        lines.append("")

    write(os.path.join(REPO, "common", "scripted_effects", "md2026_technology_effects.txt"),
          "\n".join(lines))
    print(f"  generated technology effects: {len(techs)} techs, bands {[b for b, _, _ in BANDS]}")


DEBUG_FLAGS_FILE = os.path.join(REPO, "patches", "debug.json")


def debug_flags():
    if os.path.exists(DEBUG_FLAGS_FILE):
        try:
            with open(DEBUG_FLAGS_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def apply_debug_flags(patch, flags, tag=None):
    """Temporarily disable parts of the 2026 setup for crash bisection."""
    if flags.get("skip_tech_tiers"):
        patch = re.sub(r"(?m)^(\s*)(md2026_tier[0-9]_2026_techs\s*=\s*yes)",
                       r"\1# BISECT: tech tiers disabled\n\1# \2", patch)
    if flags.get("skip_precompleted_focuses"):
        patch = re.sub(r"(?m)^(\s*)(complete_national_focus\s*=.*)$",
                       r"\1# BISECT: pre-completed focuses disabled\n\1# \2", patch)
    if flags.get("skip_oob"):
        patch = re.sub(r"(?m)^(\s*)(set_(?:oob|air_oob|naval_oob)\s*=.*)$",
                       r"\1# BISECT: OOB disabled\n\1# \2", patch)
    if flags.get("skip_wars"):
        patch = re.sub(r"(?ms)^(\s*)declare_war_on\s*=\s*\{.*?\n\1\}", r"\1# BISECT: war disabled", patch)
    skip_tags = flags.get("skip_leaders_tags") or []
    if flags.get("skip_leaders") or (tag and tag in skip_tags):
        patch = re.sub(r"(?ms)^(\s*)create_country_leader\s*=\s*\{.*?\n\1\}", r"\1# BISECT: leader disabled", patch)
    return patch


# --------------------------------------------------------------------------
# fixups for known MD 2.0 bugs, applied to generated (overriding) files
# --------------------------------------------------------------------------

def md_reference_sets(md):
    techs, chars = set(), set()
    for p in [os.path.join(md, "common", "technologies", n) for n in os.listdir(os.path.join(md, "common", "technologies"))] \
            if os.path.isdir(os.path.join(md, "common", "technologies")) else []:
        text = strip_comments(read(p))
        for m in re.finditer(r"technologies\s*=\s*\{", text):
            ob = text.index("{", m.start())
            end = find_block(text, ob)
            for name, _ in children(text[ob + 1:end - 1]):
                if not name.startswith("@"):
                    techs.add(name)
    cdir = os.path.join(md, "common", "characters")
    for n in os.listdir(cdir) if os.path.isdir(cdir) else []:
        if not n.endswith(".txt"):
            continue
        text = strip_comments(read(os.path.join(cdir, n)))
        for m in re.finditer(r"characters\s*=\s*\{", text):
            ob = text.index("{", m.start())
            end = find_block(text, ob)
            for name, _ in children(text[ob + 1:end - 1]):
                chars.add(name)
    return techs, chars


def _portrait_replacement(ref, md, tag):
    """Return a resolvable portrait path for ref, or '' when nothing matches."""
    van = r"D:\SteamLibrary\steamapps\common\Hearts of Iron IV"
    root = os.path.join(md, "gfx", "leaders", tag) if tag else ""
    files_ = os.listdir(root) if root and os.path.isdir(root) else []

    def norm(s):
        return re.sub(r"[^a-z0-9]", "", s.lower())

    if "/" in ref:
        if any(os.path.exists(os.path.join(b, ref)) for b in (md, van)):
            return ""
    elif tag and any(os.path.exists(os.path.join(b, "gfx", "leaders", tag, ref)) for b in (md, van)):
        return ""
    base = norm(os.path.splitext(os.path.basename(ref))[0])
    for fn in files_:
        if base and base in norm(os.path.splitext(fn)[0]):
            return fn
    if "_" in base:
        surname = base.split("_")[-1]
        if len(surname) > 3:
            for fn in files_:
                if surname in norm(fn):
                    return fn
    return "gfx/leaders/generic_politicians/white_001.dds"


def fix_portraits(text, md, tag):
    """Replace leader portraits that cannot be resolved (a known crash source)."""
    def repl(m):
        new = _portrait_replacement(m.group(2), md, tag)
        if not new:
            return m.group(0)
        if new.startswith("gfx/leaders/generic_politicians"):
            return (f"{m.group(1)}# MD2026: portrait '{m.group(2)}' missing in MD 2.0\n"
                    f'{m.group(1)}picture = "{new}"')
        return f'{m.group(1)}picture = "{new}"'
    return re.sub(r'(?m)^(\s*)picture\s*=\s*"([^"]+\.dds)"', repl, text)


def fix_portraits_auto(text, md):
    """Same as fix_portraits but derives the country tag from the nearest focus id."""
    def repl(m):
        prev = text[:m.start()]
        ids = re.findall(r"id\s*=\s*([A-Z]{3})[A-Za-z0-9_]*", prev)
        tag = ids[-1] if ids else ""
        new = _portrait_replacement(m.group(2), md, tag)
        if not new:
            return m.group(0)
        if new.startswith("gfx/leaders/generic_politicians"):
            return (f"{m.group(1)}# MD2026: portrait '{m.group(2)}' missing in MD 2.0\n"
                    f'{m.group(1)}picture = "{new}"')
        return f'{m.group(1)}picture = "{new}"'
    return re.sub(r'(?m)^(\s*)picture\s*=\s*"([^"]+\.dds)"', repl, text)


def apply_fixups(text, techs, chars, md=None, tag=None):
    low_t = {t.lower(): t for t in techs}
    low_c = {c.lower(): c for c in chars}

    # character references: fix case, drop broken ones
    def char_line(m):
        ind, kind, name = m.group(1), m.group(2), m.group(3)
        if name in chars:
            return m.group(0)
        if name.lower() in low_c:
            return f"{ind}{kind} = {low_c[name.lower()]}"
        return f"{ind}# MD2026: dropped broken MD reference ({kind} = {name})"

    text = re.sub(r"(?m)^(\s*)(recruit_character|promote_character|retire_character|has_character)\s*=\s*([^\s#]+)[ \t]*$",
                  char_line, text)

    # technologies inside set_technology blocks
    out = []
    pos = 0
    for m in re.finditer(r"set_technology\s*=\s*\{", text):
        ob = text.index("{", m.start())
        end = find_block(text, ob)
        body = text[ob + 1:end - 1]
        new_lines = []
        for line in body.split("\n"):
            tm = re.match(r"^(\s*)([A-Za-z0-9_]+)(\s*=\s*[0-9]+.*)$", line)
            if tm:
                ind, name, rest = tm.groups()
                if name not in techs and name.lower() in low_t:
                    line = f"{ind}{low_t[name.lower()]}{rest}"
                elif name not in techs:
                    line = f"{ind}# MD2026: dropped broken MD tech reference ({name})"
            new_lines.append(line)
        text = text[:ob + 1] + "\n".join(new_lines) + text[end - 1:]

    # has_tech references
    def has_tech(m):
        name = m.group(2)
        if name in techs:
            return m.group(0)
        if name.lower() in low_t:
            return f"{m.group(1)}{low_t[name.lower()]}"
        return f"# MD2026: dropped broken MD tech reference (has_tech = {name})"

    text = re.sub(r"(?m)^(\s*has_tech\s*=\s*)([A-Za-z0-9_]+)", has_tech, text)

    # Norway tag rename leftovers in MD's own content
    text = re.sub(r"(?<![\w])(original_tag|tag)\s*=\s*NOR(?![\w])", r"\1 = NRY", text)

    if md and tag:
        text = fix_portraits(text, md, tag)

    # MD 2.0 renamed the computing tech category
    text = text.replace("CAT_computing_tech", "CAT_computer_systems")
    # MD uses the short doctrine category names; normalise to the canonical form
    text = re.sub(r"(?m)^(\s*category\s*=\s*)(land|naval|air)_doctrine\s*$", r"\1CAT_\2_doctrine", text)
    return text


def generate_search_filters(md):
    """MD 2.0 replaced vanilla's common/national_focus/generic.txt (which defined
    search_filter_prios) without providing a replacement, so every focus search filter
    is undefined. Restore the priorities for the filters MD and this submod use."""
    vanilla = {
        "FOCUS_FILTER_POLITICAL": 1010,
        "FOCUS_FILTER_RESEARCH": 522,
        "FOCUS_FILTER_INDUSTRY": 509,
        "FOCUS_FILTER_BALANCE_OF_POWER": 200,
        "FOCUS_FILTER_SOV_POLITICAL_PARANOIA": 111,
        "FOCUS_FILTER_PROPAGANDA": 110,
        "FOCUS_FILTER_MISSIOLINI": 110,
        "FOCUS_FILTER_ARMY_XP": 103,
        "FOCUS_FILTER_NAVY_XP": 102,
        "FOCUS_FILTER_AIR_XP": 101,
    }
    # if MD defines any priority itself, leave it alone
    defined = set()
    for name in os.listdir(os.path.join(md, "common", "national_focus")):
        if not name.endswith(".txt"):
            continue
        text = read(os.path.join(md, "common", "national_focus", name))
        defined |= set(re.findall(r"(?m)^\s*(FOCUS_FILTER_[A-Z_0-9]+)\s*=\s*\d+", text))
    if defined:
        print(f"  search filters: MD defines {len(defined)} priorities, skipping generation")
        return

    used = Counter()
    for root in (os.path.join(md, "common", "national_focus"), os.path.join(REPO, "common", "national_focus")):
        for name in os.listdir(root):
            if not name.endswith(".txt"):
                continue
            text = read(os.path.join(root, name))
            for m in re.finditer(r"search_filters\s*=\s*\{([^}]*)\}", text):
                for f in m.group(1).split():
                    if f.startswith("FOCUS_FILTER"):
                        used[f] += 1
    lines = [
        "# GENERATED FILE - do not edit by hand.",
        "# Rebuild with: python tools/rebase.py filters",
        "#",
        "# Millennium Dawn 2.0 replaces common/national_focus (and with it vanilla's",
        "# generic.txt that defined search_filter_prios) without providing a replacement,",
        "# which leaves every focus search filter undefined. This file restores them",
        "# (vanilla priorities where known, otherwise ordered by how often MD uses them).",
        "",
        "search_filter_prios = {",
    ]
    extra = [f for f in used if f not in vanilla]
    extra.sort(key=lambda f: (-used[f], f))
    prio = 900
    values = dict(vanilla)
    for f in extra:
        values[f] = prio
        prio -= 5
    for f in sorted(used):
        lines.append(f"\t{f} = {values[f]}")
    lines.append("}")
    lines.append("")
    write(os.path.join(REPO, "common", "national_focus", "md2026_search_filters.txt"), "\n".join(lines))
    print(f"  generated search filter priorities: {len(used)} filters")


# --------------------------------------------------------------------------
# history generation
# --------------------------------------------------------------------------

def md_history_country_file(md, tag):
    root = os.path.join(md, "history", "countries")
    for name in sorted(os.listdir(root)):
        if name.startswith(tag + " ") and name.endswith(".txt"):
            return name
    # tag might have been renamed in MD (e.g. NOR -> NRY)
    return None


def md_state_file(md, state_id):
    root = os.path.join(md, "history", "states")
    for name in sorted(os.listdir(root)):
        if name.endswith(".txt") and name.split("-")[0].strip() == str(state_id):
            return name
    return None


def write_deferred_focuses(focuses_by_tag):
    """Pre-completed focuses run after game start, never during history.

    Focus rewards call ingame-only systems (ingame_update_setup and friends)
    that are not initialised while history is still being processed - MD itself
    never completes a focus from a history file.  They are completed in
    on_startup once MD's own startup pass has run (marker: global.update_monie_ui),
    with the first daily tick as a fallback for anything still pending.
    """
    eff = [
        "### Millennium Dawn 2026 - pre-completed focuses ###",
        "# Called from common/on_actions/md2026_precompleted_focuses.txt after game",
        "# start.  Focus rewards touch ingame-only economy systems, so they must not",
        "# run while history is still being processed.",
        "",
        "md2026_complete_precompleted_focuses = {",
    ]
    for tag in sorted(focuses_by_tag):
        focuses = focuses_by_tag[tag]
        if not focuses:
            continue
        eff.append("\tif = {")
        eff.append(f"\t\tlimit = {{ tag = {tag} }}")
        for f in focuses:
            eff.append(f"\t\tcomplete_national_focus = {f}")
        eff.append("\t}")
    eff += ["}", ""]
    write(os.path.join(REPO, "common", "scripted_effects", "md2026_precompleted_focuses.txt"),
          "\n".join(eff))

    act = [
        "### Millennium Dawn 2026 - pre-completed focuses (driver) ###",
        "# on_startup: MD's startup pass (00_on_actions.txt) loads first and sets",
        "# global.update_monie_ui, so by the time this runs the economy is ready.",
        "# on_daily: fallback for countries still pending (e.g. after loading a save).",
        "",
        "on_actions = {",
        "\ton_startup = {",
        "\t\teffect = {",
        "\t\t\tif = {",
        "\t\t\t\tlimit = {",
        "\t\t\t\t\tdate > 2025.12.31",
        "\t\t\t\t\tcheck_variable = { global.update_monie_ui > 0 }",
        "\t\t\t\t}",
        "\t\t\t\tevery_country = {",
        "\t\t\t\t\tlimit = { has_country_flag = md2026_focuses_pending }",
        "\t\t\t\t\tclr_country_flag = md2026_focuses_pending",
        "\t\t\t\t\tmd2026_complete_precompleted_focuses = yes",
        "\t\t\t\t}",
        "\t\t\t}",
        "\t\t}",
        "\t}",
        "\ton_daily = {",
        "\t\teffect = {",
        "\t\t\tevery_country = {",
        "\t\t\t\tlimit = { has_country_flag = md2026_focuses_pending }",
        "\t\t\t\tclr_country_flag = md2026_focuses_pending",
        "\t\t\t\tmd2026_complete_precompleted_focuses = yes",
        "\t\t\t}",
        "\t\t}",
        "\t}",
        "}",
        "",
    ]
    write(os.path.join(REPO, "common", "on_actions", "md2026_precompleted_focuses.txt"),
          "\n".join(act))
    n = sum(len(v) for v in focuses_by_tag.values())
    print(f"  generated deferred focuses: {n} focuses for {len(focuses_by_tag)} countries")


def rebase_history(md, rename_map):
    out_dir = os.path.join(REPO, "history", "countries")
    patch_dir = os.path.join(REPO, "patches", "history_countries")
    techs, chars = md_reference_sets(md)
    used = set()
    focuses_by_tag = {}
    for pf in sorted(os.listdir(patch_dir)):
        if not pf.endswith(".txt"):
            continue
        tag = pf[:-4]
        md_tag = rename_map.get(tag, tag)
        fname = md_history_country_file(md, md_tag)
        if not fname:
            print(f"  !! no MD history file for {md_tag}")
            continue
        used.add(fname)
        base = read(os.path.join(md, "history", "countries", fname))
        patch = read(os.path.join(patch_dir, pf))
        if tag != md_tag:
            patch = re.sub(r"(?<![\w])" + re.escape(tag) + r"(?![A-Za-z])", md_tag, patch)
        patch = apply_debug_flags(patch, debug_flags(), md_tag)
        if debug_flags().get("skip_2026_blocks"):
            patch = "# BISECT: entire 2026 block disabled\n"
        # Pre-completed focuses are deferred to the first daily tick: their
        # rewards are ingame-only code (see write_deferred_focuses).
        focuses = re.findall(r"(?m)^[ \t]*complete_national_focus\s*=\s*([A-Za-z0-9_]+)\s*$", patch)
        if focuses:
            patch = re.sub(r"(?m)^[ \t]*complete_national_focus\s*=.*\n?", "", patch)
            patch = patch.rstrip() + "\n\n\t### Pre-completed focuses (run on the first daily tick) ###\n" \
                                    "\tset_country_flag = md2026_focuses_pending\n"
            focuses_by_tag[md_tag] = focuses
        out = apply_fixups(base.rstrip() + "\n\n" + patch, techs, chars, md, md_tag)
        write(os.path.join(out_dir, fname), out)
    write_deferred_focuses(focuses_by_tag)
    print(f"  generated {len(used)} country history files")

    s_out = os.path.join(REPO, "history", "states")
    s_patch = os.path.join(REPO, "patches", "history_states")
    n = 0
    used_states = set()
    for pf in sorted(os.listdir(s_patch)):
        if not pf.endswith(".txt"):
            continue
        sid = pf[:-4]
        fname = md_state_file(md, sid)
        if not fname:
            print(f"  !! no MD state file for {sid}")
            continue
        base = read(os.path.join(md, "history", "states", fname))
        patch = read(os.path.join(s_patch, pf)).strip("\n")
        # state date blocks live inside the state's history = { } block
        hm = re.search(r"history\s*=\s*\{", base)
        if not hm:
            print(f"  !! no history block in {fname}")
            continue
        ob = base.index("{", hm.start())
        end = find_block(base, ob)
        patch_ind = patch
        base = apply_fixups(base[:end - 1].rstrip() + "\n\n" + patch_ind + "\n" + base[end - 1:], techs, chars)
        write(os.path.join(s_out, fname), base)
        used_states.add(fname)
        n += 1
    print(f"  generated {n} state history files")

    # drop leftovers from the old copy-based approach
    for name in sorted(os.listdir(out_dir)):
        if name.endswith(".txt") and name not in used:
            os.remove(os.path.join(out_dir, name))
            print(f"  removed obsolete history copy {name}")
    for name in sorted(os.listdir(s_out)):
        if name.endswith(".txt") and name not in used_states:
            os.remove(os.path.join(s_out, name))
            print(f"  removed obsolete state copy {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["extract", "generate", "focus", "history", "tech", "filters"])
    ap.add_argument("--md", default=os.environ.get("MD_PATH", DEFAULT_MD))
    args = ap.parse_args()

    global MD
    MD = args.md
    if not os.path.isdir(MD):
        sys.exit(f"MD not found: {MD}")

    if args.mode in ("extract",):
        extract_history_countries()
        extract_history_states()
    if args.mode in ("generate", "focus"):
        exp = rebase_focus(MD)
        cleanup_old_focus_copies(exp)
        generate_bookmark()
    if args.mode in ("generate", "history"):
        rename = {"NOR": "NRY"}
        rebase_history(MD, rename)
    if args.mode in ("generate", "tech"):
        generate_tech_effects(MD)
    if args.mode in ("generate", "filters"):
        generate_search_filters(MD)


if __name__ == "__main__":
    main()
