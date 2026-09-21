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
            text = rebase.strip_comments(rebase.read(p))
            ids = set()
            for m in re.finditer(r"(?m)^\s*(?:focus|shared_focus|joint_focus)\s*=\s*\{", text):
                ob = text.index("{", m.end() - 1)
                end = rebase.find_block(text, ob)
                idm = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_\-\.]+)", text[ob:end][:400])
                if idm:
                    ids.add(idm.group(1))
            s["focus"] |= ids
            s["focus_by_file"][p] = ids

    s["equipment"] = set()
    for p in files(os.path.join(md, "common", "units", "equipment")) + \
             files(os.path.join(REPO, "common", "units", "equipment")) + \
             files(os.path.join(rebase.VANILLA, "common", "units", "equipment")):
        text = rebase.strip_comments(rebase.read(p))
        for name, _ in rebase.children(text):
            s["equipment"].add(name)
        # archetypes are usually nested one level down
        for root_name, body in rebase.children(text):
            for name, _ in rebase.children(body):
                s["equipment"].add(name)

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
    for root in (os.path.join(md, "common", "country_leader"),
                 os.path.join(REPO, "common", "country_leader"),
                 r"D:\SteamLibrary\steamapps\common\Hearts of Iron IV\common\country_leader"):
        for p in files(root):
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
    # every country entry needs a version key (frontend picks the entry by DLC version;
    # a missing version crashed the country selection screen in 1.19.3)
    for m in re.finditer(r'(?m)^\s*"([A-Z]{3})"\s*=\s*\{', text):
        tag = m.group(1)
        ob = text.index("{", m.end() - 1)
        end = rebase.find_block(text, ob)
        if "version" not in text[ob:end]:
            ERRORS["bookmark entry without version"].append(tag)


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


def check_sprites(md):
    """Focus icons, idea pictures and event/decision sprites must exist."""
    names = set()
    for root in (os.path.join(md, "interface"), os.path.join(REPO, "interface"),
                 os.path.join(r"D:\SteamLibrary\steamapps\common\Hearts of Iron IV", "interface")):
        for p in files(root, ".gfx"):
            text = rebase.read(p)
            names |= set(re.findall(r'name\s*=\s*"?([A-Za-z0-9_.\-]+)"?', text))

    def exists(ref):
        return any(x in names for x in (ref, "GFX_" + ref, "GFX_idea_" + ref,
                                        "GFX_focus_" + ref, "GFX_decision_" + ref, "GFX_goal_" + ref))

    for p in files(os.path.join(REPO, "common", "national_focus")) + files(os.path.join(REPO, "common", "ideas")) + \
             files(os.path.join(REPO, "common", "decisions")) + files(os.path.join(REPO, "events")):
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r"(?m)^\s*(?:icon|picture)\s*=\s*([A-Za-z0-9_.\-]+)", text):
            ref = m.group(1)
            if ref.lower() in ("yes", "no") or ref.startswith("GFX_report_event"):
                continue
            if not exists(ref):
                WARNINGS["missing sprite"].append(f"{ref}  ({rel(p)})")


def check_oob_locations(md):
    """Unit locations in our OOBs must exist in MD's states."""
    provinces = set()
    for p in files(os.path.join(md, "history", "states")):
        text = rebase.read(p)
        for m in re.finditer(r"provinces\s*=\s*\{([^}]*)\}", text):
            provinces |= set(m.group(1).split())
    for p in files(os.path.join(REPO, "history", "units")):
        text = rebase.read(p)
        for m in re.finditer(r"location\s*=\s*(\d+)", text):
            if m.group(1) not in provinces:
                WARNINGS["unknown province"].append(f"{m.group(1)}  ({rel(p)})")


SCOPE_KEYWORDS = {"ROOT", "PREV", "FROM", "THIS", "OWNER", "CONTROLLER", "CAPITAL", "OVERLORD", "yes", "no"}


def check_decision_categories(md):
    cats = set()
    for root in (os.path.join(md, "common", "decisions", "categories"), os.path.join(REPO, "common", "decisions", "categories")):
        for p in files(root):
            text = rebase.strip_comments(rebase.read(p))
            cats |= {n for n, _ in rebase.children(text)}
    tech_cats = set()
    for p in files(os.path.join(md, "common", "technology_tags")) + files(os.path.join(REPO, "common", "technology_tags")):
        text = rebase.strip_comments(rebase.read(p))
        tech_cats |= set(re.findall(r"(?m)^\s*(CAT_[A-Za-z0-9_]+)", text))
    tech_cats_low = {c.lower() for c in tech_cats}
    cats_low = {c.lower() for c in cats}
    for p in files(os.path.join(REPO, "common", "decisions")) + files(os.path.join(REPO, "common", "national_focus")):
        if "categories" in p:
            continue
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r"(?m)^\s*category\s*=\s*([A-Za-z0-9_]+)", text):
            ref = m.group(1)
            if ref.lower() in tech_cats_low:
                continue
            if ref.lower() in cats_low:
                continue
            # MD sometimes uses the short doctrine form (land_doctrine)
            if ("cat_" + ref.lower()) in tech_cats_low:
                continue
            WARNINGS["unknown category"].append(f"{ref}  ({rel(p)})")


def check_focus_filters(md):
    defined = set()
    for root in (os.path.join(md, "common", "national_focus"), os.path.join(REPO, "common", "national_focus")):
        for p in files(root):
            text = rebase.read(p)
            defined |= set(re.findall(r"(?m)^\s*(FOCUS_FILTER_[A-Z_0-9]+)\s*=\s*\d+", text))
    md_defined = set()
    for p in files(os.path.join(md, "common", "national_focus")):
        md_defined |= set(re.findall(r"(?m)^\s*(FOCUS_FILTER_[A-Z_0-9]+)\s*=\s*\d+", rebase.read(p)))
    if md_defined:
        WARNINGS["MD defines focus filters"].append(
            f"MD defines {len(md_defined)} search_filter_prios - md2026_search_filters.txt is redundant")
    used = set()
    for p in files(os.path.join(REPO, "common", "national_focus")):
        text = rebase.read(p)
        for m in re.finditer(r"search_filters\s*=\s*\{([^}]*)\}", text):
            for f in m.group(1).split():
                if f.startswith("FOCUS_FILTER"):
                    used.add(f)
    missing = used - defined
    for f in sorted(missing):
        WARNINGS["undefined focus filter"].append(f)


def check_installation():
    """Sanity-check the local installation (launcher descriptor, playset, last run)."""
    mod_dir = os.path.join(os.path.expanduser("~"), "Documents", "Paradox Interactive",
                           "Hearts of Iron IV", "mod")
    mod_file = os.path.join(mod_dir, "md-2026.mod")
    if not os.path.exists(mod_file):
        WARNINGS["installation"].append("brak mod/md-2026.mod - uruchom tools/install_mod.ps1")
        return
    content = rebase.read(mod_file)
    if not re.search(r'(?m)^\s*path\s*=', content):
        ERRORS["installation"].append("mod/md-2026.mod nie ma linii path= (gra nie wczyta moda)")
    link = os.path.join(mod_dir, "md-2026")
    if not os.path.isdir(link):
        WARNINGS["installation"].append("brak katalogu mod/md-2026 (junction)")
    elif not os.path.exists(os.path.join(link, "descriptor.mod")):
        WARNINGS["installation"].append("mod/md-2026 nie wskazuje na repo (brak descriptor.mod)")
    playset = os.path.join(os.path.dirname(mod_dir), "dlc_load.json")
    if os.path.exists(playset):
        try:
            data = json.load(open(playset, encoding="utf-8"))
            if not any("md-2026" in m for m in data.get("enabled_mods", [])):
                WARNINGS["installation"].append("md-2026 nie jest wlaczony w playset (dlc_load.json)")
        except Exception:
            pass
    log = os.path.join(os.path.dirname(mod_dir), "logs", "system.log")
    if os.path.exists(log):
        text = rebase.read(log)
        for m in re.finditer(r"Active Mod Count: (\d+)", text):
            count = int(m.group(1))
            if count < 2:
                WARNINGS["installation"].append(
                    f"ostatnie uruchomienie gry: Active Mod Count = {count} (submod nie zostal wczytany)")


def check_file_hygiene():
    """HoI4 script files must not carry a UTF-8 BOM; localisation must."""
    for root in ("common", "events", "history", "patches"):
        for p in files(os.path.join(REPO, root)):
            with open(p, "rb") as f:
                if f.read(3) == b"\xef\xbb\xbf":
                    ERRORS["BOM in script file"].append(rel(p))
    for p in files(os.path.join(REPO, "localisation"), ".yml"):
        with open(p, "rb") as f:
            if f.read(3) != b"\xef\xbb\xbf":
                WARNINGS["missing BOM in localisation"].append(rel(p))


def check_shared_focus_injection(md):
    """shared_focus = MD2026_* references must sit inside a focus_tree block."""
    for p in files(os.path.join(REPO, "common", "national_focus")):
        if os.path.basename(p).startswith("md2026_"):
            continue
        text = rebase.read(p)
        trees = []
        for m in re.finditer(r"focus_tree\s*=\s*\{", text):
            ob = text.index("{", m.start())
            trees.append((ob, rebase.find_block(text, ob)))
        for m in re.finditer(r"(?m)^\s*shared_focus = (MD2026[A-Za-z0-9_]+)", text):
            if not any(ob < m.start() < end for ob, end in trees):
                ERRORS["shared_focus outside focus tree"].append(f"{m.group(1)}  ({rel(p)})")


def check_portraits(md):
    """Leader portraits referenced by the submod must resolve (bare names resolve
    against gfx/leaders/<TAG>/). Only checks our own files/patches - Millennium
    Dawn's own files are its responsibility."""
    van = r"D:\SteamLibrary\steamapps\common\Hearts of Iron IV"
    md_basenames = set()
    for sub in ("common", "events", "history"):
        root = os.path.join(md, sub)
        for dirpath, _, names in os.walk(root):
            for n in names:
                md_basenames.add(n)

    targets = list(files(os.path.join(REPO, "patches"))) + \
        list(files(os.path.join(REPO, "events"))) + \
        list(files(os.path.join(REPO, "common", "ideas"))) + \
        list(files(os.path.join(REPO, "common", "decisions"))) + \
        [p for p in files(os.path.join(REPO, "common", "national_focus")) if os.path.basename(p).startswith("md2026_")]
    for p in targets:
        name = os.path.basename(p)
        tag = name[:3] if name[:3].isupper() else (name.split("_")[1].upper() if name.startswith("md2026_") else "")
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r'(?m)^\s*picture\s*=\s*"([^"]+\.dds)"', text):
            ref = m.group(1)
            if "/" in ref:
                ok = any(os.path.exists(os.path.join(b, ref)) for b in (md, van)) or \
                     any(os.path.exists(os.path.join(b, "portraits", ref)) for b in (md, van))
            elif tag:
                ok = any(os.path.exists(os.path.join(b, "gfx", "leaders", tag, ref)) for b in (md, van))
            else:
                ok = True
            if not ok:
                ERRORS["missing portrait"].append(f"{ref}  ({rel(p)})")


def check_equipment_refs(sets):
    targets = list(files(os.path.join(REPO, "common", "decisions"))) + \
        [p for p in files(os.path.join(REPO, "common", "national_focus")) if os.path.basename(p).startswith("md2026_")] + \
        list(files(os.path.join(REPO, "events"))) + list(files(os.path.join(REPO, "patches")))
    for p in targets:
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r"(?:add_equipment_to_stockpile|add_equipment_to_stockpile_from_stockpile)\s*=\s*\{", text):
            ob = text.index("{", m.end() - 1)
            end = rebase.find_block(text, ob)
            body = text[ob:end]
            for tm in re.finditer(r"(?m)^\s*type\s*=\s*([A-Za-z0-9_]+)", body):
                if tm.group(1) not in sets["equipment"]:
                    ERRORS["unknown equipment type"].append(f"{tm.group(1)}  ({rel(p)})")


def check_leader_traits(sets):
    for p in files(os.path.join(REPO, "patches")) + list(files(os.path.join(REPO, "events"))) + \
             [p for p in files(os.path.join(REPO, "common", "national_focus")) if os.path.basename(p).startswith("md2026_")]:
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r"traits\s*=\s*\{([^}]*)\}", text):
            for tr in m.group(1).split():
                if tr not in sets["trait"]:
                    ERRORS["unknown leader trait"].append(f"{tr}  ({rel(p)})")


def check_oob_equipment(sets):
    """Equipment referenced by our OOB files must exist in MD 2.0 (the old
    submod used MD 1.x names, which silently dropped stockpiles and air wings)."""
    oob = os.path.join(REPO, "history", "units")
    for p in files(oob):
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r"type[ \t]*=[ \t]*([A-Za-z0-9_]+)", text):
            if m.group(1) not in sets["equipment"]:
                ERRORS["unknown OOB equipment"].append(f"{m.group(1)}  ({rel(p)})")
        for block_re in (r"equipment[ \t]*=[ \t]*\{", r"air_wings[ \t]*=[ \t]*\{"):
            for m in re.finditer(block_re, text):
                ob = text.index("{", m.end() - 1)
                body = text[ob:rebase.find_block(text, ob)]
                for mm in re.finditer(r"(?m)^[ \t]*([A-Za-z_][A-Za-z0-9_]*)[ \t]*=[ \t]*\{", body):
                    name = mm.group(1)
                    if name.isdigit():
                        continue
                    if name not in sets["equipment"]:
                        ERRORS["unknown OOB equipment"].append(f"{name}  ({rel(p)})")


def check_history_syntax():
    """Catch scalar/array mix-ups in our history blocks (MD sets the ruling
    party index with set_variable = { ruling_party = N }, not add_to_array)."""
    scalars = ("ruling_party", "party_pop_array", "party_pop_elect_array")
    targets = list(files(os.path.join(REPO, "patches", "history_countries"))) + \
        list(files(os.path.join(REPO, "history", "countries")))
    for p in targets:
        text = rebase.strip_comments(rebase.read(p))
        for m in re.finditer(r"add_to_array\s*=\s*\{\s*([A-Za-z_][A-Za-z0-9_]*)", text):
            if m.group(1) in scalars:
                ERRORS["array syntax for scalar"].append(f"{m.group(1)}  ({rel(p)})")


def ideology_families(md):
    """sub-ideology -> top-level ideology (from types = { } blocks)."""
    fam = {}
    for root in (os.path.join(md, "common", "ideologies"),
                 os.path.join(rebase.VANILLA, "common", "ideologies")):
        for p in files(root):
            text = rebase.strip_comments(rebase.read(p))
            for m in re.finditer(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", text):
                ob = text.index("{", m.end() - 1)
                body = text[ob:rebase.find_block(text, ob)]
                tm = re.search(r"types\s*=\s*\{", body)
                if not tm:
                    continue
                tb = body.index("{", tm.end() - 1)
                te = rebase.find_block(body, tb)
                for name, _ in rebase.children(body[tb + 1:te - 1]):
                    if not name.startswith("@"):
                        fam[name] = m.group(1)
    return fam


def check_leader_ideology(md):
    """Our 2026 leaders must belong to the ruling party's ideology family,
    otherwise the game will not show them as the current leader."""
    fam = ideology_families(md)
    for p in files(os.path.join(REPO, "patches", "history_countries")):
        text = rebase.strip_comments(rebase.read(p))
        sp = re.search(r"set_politics\s*=\s*\{([^}]*)\}", text)
        if not sp:
            continue
        ruling = re.search(r"ruling_party\s*=\s*([A-Za-z_]+)", sp.group(1))
        if not ruling:
            continue
        rf = fam.get(ruling.group(1), ruling.group(1))
        for m in re.finditer(r"create_country_leader\s*=\s*\{", text):
            ob = text.index("{", m.end() - 1)
            body = text[ob:rebase.find_block(text, ob)]
            ide = re.search(r"ideology\s*=\s*([A-Za-z_\-]+)", body)
            if not ide:
                continue
            lf = fam.get(ide.group(1), ide.group(1))
            if lf != rf:
                ERRORS["leader ideology outside ruling family"].append(
                    f"{os.path.basename(p)[:3]}: {ide.group(1)} ({lf}) vs {ruling.group(1)} ({rf})")


def check_membership_lists():
    """BRICS 2026 has 11 members; NATO has 32 (MD's 19 + our 13 joiners)."""
    on_actions = rebase.read(os.path.join(REPO, "common", "on_actions", "md2026_on_actions.txt"))
    m = re.search(r"OR\s*=\s*\{([^}]*)\}\s*\}\s*set_country_flag = md2026_brics_member", on_actions)
    if not m:
        ERRORS["BRICS list not found"].append("md2026_on_actions.txt")
    else:
        got = set(re.findall(r"tag = ([A-Z]{3})", m.group(1)))
        want = {"BRA", "CHI", "EGY", "ETH", "IND", "PER", "RAJ", "SAU", "SAF", "SOV", "UAE"}
        if got != want:
            ERRORS["BRICS list mismatch"].append(f"brakuje {sorted(want - got)}, zbedne {sorted(got - want)}")
    joiners = set()
    for p in files(os.path.join(REPO, "patches", "history_countries")):
        text = rebase.strip_comments(rebase.read(p))
        if re.search(r"add_ideas\s*=\s*\{\s*NATO_member", text):
            joiners.add(os.path.basename(p)[:3])
    want_joiners = {"ALB", "BUL", "CRO", "EST", "FIN", "FYR", "LAT", "LIT", "MNT", "ROM", "SLO", "SLV", "SWE"}
    if joiners != want_joiners:
        ERRORS["NATO joiner list mismatch"].append(
            f"brakuje {sorted(want_joiners - joiners)}, zbedne {sorted(joiners - want_joiners)}")


def check_unsafe_focuses(sets):
    """Manual pre-completion exclusions must reference real focuses."""
    for fid in rebase.manual_unsafe_focuses():
        if fid not in sets["focus"]:
            ERRORS["unknown manually excluded focus"].append(fid)


def check_precompleted_focuses(md):
    """A focus completed in a country history file must not belong to another
    country's focus tree (SAU completing Gulf-tree focuses crashed the game)."""
    tree_tags = {}
    focus_tree = {}
    for root in (os.path.join(md, "common", "national_focus"), os.path.join(REPO, "common", "national_focus")):
        for p in files(root):
            text = rebase.strip_comments(rebase.read(p))
            for m in re.finditer(r"focus_tree\s*=\s*\{", text):
                ob = text.index("{", m.start())
                end = rebase.find_block(text, ob)
                body = text[ob:end]
                idm = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+)", body[:400])
                if not idm:
                    continue
                tid = idm.group(1)
                tags = set()
                cb = re.search(r"country\s*=\s*\{", body[:2000])
                if cb:
                    cb_ob = body.index("{", cb.start())
                    cb_end = rebase.find_block(body, cb_ob)
                    tags = set(re.findall(r"(?:tag|original_tag)\s*=\s*([A-Z]{3})", body[cb_ob:cb_end]))
                tree_tags[tid] = tags
                for fm in re.finditer(r"(?m)^\s*(?:focus|shared_focus|joint_focus)\s*=\s*\{", body):
                    fob = body.index("{", fm.end() - 1)
                    fend = rebase.find_block(body, fob)
                    fid = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+)", body[fob:fend][:300])
                    if fid:
                        focus_tree[fid.group(1)] = tid
    rename = {"NOR": "NRY"}
    for p in files(os.path.join(REPO, "patches", "history_countries")):
        tag = rename.get(os.path.basename(p)[:3], os.path.basename(p)[:3])
        text = rebase.read(p)
        for m in re.finditer(r"complete_national_focus\s*=\s*([A-Za-z0-9_]+)", text):
            f = m.group(1)
            tid = focus_tree.get(f)
            if not tid:
                continue  # shared/joint focus, pulled in by its branch root
            tags = tree_tags.get(tid, set())
            if tags and tag not in tags:
                ERRORS["focus from another country's tree"].append(
                    f"{tag}: {f} (tree {tid} -> {sorted(tags)[:3]})")


def check_deferred_focuses(md):
    """Pre-completed focuses must run after game start, never in history, and
    must not wreck the 2026 setup (civil wars, releases, government changes)."""
    rename = {"NOR": "NRY"}
    unsafe = rebase.unsafe_precompleted_focuses(md)
    groups = rebase.exclusive_focus_groups(md)
    patch_focuses = {}
    for p in files(os.path.join(REPO, "patches", "history_countries")):
        tag = rename.get(os.path.basename(p)[:3], os.path.basename(p)[:3])
        found = re.findall(r"complete_national_focus\s*=\s*([A-Za-z0-9_]+)", rebase.read(p))
        if not found:
            continue
        kept = [f for f in found if f not in unsafe]
        conflict = {f for f in kept if any(o in kept for o in groups.get(f, ()))}
        kept = [f for f in kept if f not in conflict]
        if kept:
            patch_focuses[tag] = kept

    hist_dir = os.path.join(REPO, "history", "countries")
    for p in files(hist_dir):
        if "complete_national_focus" in rebase.strip_comments(rebase.read(p)):
            ERRORS["focus completed in history"].append(rel(p))

    for tag in sorted(patch_focuses):
        cand = [p for p in files(hist_dir) if os.path.basename(p).startswith(tag + " -")]
        if not cand:
            ERRORS["deferred focuses: no history file"].append(tag)
        elif "md2026_focuses_pending" not in rebase.read(cand[0]):
            ERRORS["deferred focuses: missing pending flag"].append(f"{tag} ({os.path.basename(cand[0])})")

    eff_path = os.path.join(REPO, "common", "scripted_effects", "md2026_precompleted_focuses.txt")
    act_path = os.path.join(REPO, "common", "on_actions", "md2026_precompleted_focuses.txt")
    if not os.path.exists(eff_path) or not os.path.exists(act_path):
        ERRORS["deferred focuses: missing generated file"].append("md2026_precompleted_focuses")
        return
    eff = rebase.strip_comments(rebase.read(eff_path))
    blocks = {}
    for m in re.finditer(r"tag\s*=\s*([A-Z]{3})\s*\}\s*((?:\s*complete_national_focus\s*=\s*[A-Za-z0-9_]+\s*)+)",
                         eff):
        blocks[m.group(1)] = re.findall(r"complete_national_focus\s*=\s*([A-Za-z0-9_]+)", m.group(2))
    for tag, fs in sorted(patch_focuses.items()):
        got = blocks.get(tag)
        if got is None:
            ERRORS["deferred focuses: tag missing"].append(tag)
        elif sorted(got) != sorted(fs):
            ERRORS["deferred focuses: list mismatch"].append(
                f"{tag}: {len(fs)} w patchu, {len(got)} w scripted effect")
    act = rebase.strip_comments(rebase.read(act_path))
    for needle, why in (("on_startup", "brak on_startup"), ("on_daily", "brak on_daily"),
                        ("md2026_complete_precompleted_focuses = yes", "brak wywolania efektu"),
                        ("global.update_monie_ui", "brak znacznika startu MD")):
        if needle not in act:
            ERRORS["deferred focuses: driver"].append(why)


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
    check_sprites(md)
    check_oob_locations(md)
    check_decision_categories(md)
    check_focus_filters(md)
    check_file_hygiene()
    check_shared_focus_injection(md)
    check_portraits(md)
    check_equipment_refs(sets)
    check_oob_equipment(sets)
    check_history_syntax()
    check_leader_traits(sets)
    check_precompleted_focuses(md)
    check_deferred_focuses(md)
    check_leader_ideology(md)
    check_membership_lists()
    check_unsafe_focuses(sets)
    check_installation()

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
