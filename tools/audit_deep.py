#!/usr/bin/env python3
"""Deep read-only audit of the Millennium Dawn 2026 Rework submod.

Groups:
  S  file integrity                 O  OOB structure
  H  history / politics             F  focus trees
  E  events / decisions / scripts   L  localisation
  B  bookmark                       G  generated-override reproducibility
  C  cross-mod ordering (arrays, membership, legacy state)

Usage:
    python tools/audit_deep.py [--md PATH] [--vanilla PATH] [--json OUT]
                               [--no-repro] [--quiet]

Never writes to the repo (the reproducibility check captures generator output
in memory instead of letting it write).
"""

import argparse
import contextlib
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import rebase  # noqa: E402

MD_REL = rebase.MD_REL
VANILLA_REL = rebase.VANILLA_REL


def resolve_path(arg, env, rel, marker):
    found = rebase.resolve_install(rel, marker, override=arg, env=env)
    if not found or not os.path.exists(os.path.join(found, marker)):
        raise SystemExit(f"could not locate {rel}; pass --md/--vanilla or set {env}")
    return found


# ----------------------------------------------------------------- helpers

def read(p):
    with open(p, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def strip_comments(text):
    return "\n".join(line.split("#")[0] for line in text.split("\n"))


def find_block(text, start):
    """Index just past the '}' matching the '{' at start, or None."""
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
    return None


def body_at(text, open_idx):
    end = find_block(text, open_idx)
    if end is None:
        return text[open_idx:]
    return text[open_idx:end]


def line_at(text, idx):
    return text.count("\n", 0, idx) + 1


def walk(root, ext=".txt"):
    out = []
    if not os.path.isdir(root):
        return out
    for dirpath, _, names in os.walk(root):
        for n in names:
            if n.endswith(ext):
                out.append(os.path.join(dirpath, n))
    return sorted(out)


def our(relpath, ext=".txt"):
    return walk(os.path.join(REPO, relpath), ext)


def relpath(p):
    try:
        return os.path.relpath(p, REPO)
    except ValueError:
        return p


class Report:
    def __init__(self):
        self.items = []

    def add(self, fid, sev, cat, title, file=None, line=None, tag=None,
            detail="", rec="", confidence="high"):
        self.items.append({
            "id": fid, "severity": sev, "category": cat, "title": title,
            "file": relpath(file) if file else "", "line": line or "",
            "tag": tag or "", "detail": detail, "recommendation": rec,
            "confidence": confidence,
        })

    def count(self, sev=None):
        return sum(1 for i in self.items if sev is None or i["severity"] == sev)

    def json(self, path):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)


# ----------------------------------------------------------------- reference data

class Ctx:
    def __init__(self, md, vanilla):
        self.md = md
        self.vanilla = vanilla
        self.equipment = set()
        self.equipment_md = set()
        self.archetypes = set()
        self.subunits = set()
        self.traits = set()
        self.tags = set()
        self.ideas = set()
        self.sprites = set()
        self.focus_ids = set()
        self.events = set()
        self.tech_dlc = defaultdict(set)
        self.ideology_family = {}
        self.prov2state = {}
        self.state = {}          # state id -> dict(owner, cores, air, naval{prov:lvl}, file)
        self.md_on_action_hooks = set()
        self._load()

    # ---- loading helpers
    def _load(self):
        md, van = self.md, self.vanilla

        def add_eq(name, body, md_side):
            self.equipment.add(name)
            if md_side:
                self.equipment_md.add(name)
            if re.search(r"(?m)^\s*is_archetype\s*=\s*yes", body):
                self.archetypes.add(name)

        for root in (os.path.join(md, "common", "units", "equipment"),
                     os.path.join(REPO, "common", "units", "equipment")):
            md_side = root.startswith(md)
            for n in sorted(os.listdir(root)) if os.path.isdir(root) else []:
                p = os.path.join(root, n)
                if not n.endswith(".txt") or not os.path.isfile(p):
                    continue
                text = strip_comments(read(p))
                for name, body in self._top_children(text):
                    if name in ("equipments", "equipment"):
                        for sub, sbody in self._top_children(body):
                            add_eq(sub, sbody, md_side)
                            for var, vbody in self._top_children(sbody):
                                add_eq(var, vbody, md_side)
                    else:
                        add_eq(name, body, md_side)
        for p in walk(os.path.join(md, "common", "units")) + walk(os.path.join(REPO, "common", "units")):
            text = strip_comments(read(p))
            for m in re.finditer(r"(?m)^\s*sub_units\s*=\s*\{", text):
                ob = text.index("{", m.end() - 1)
                for name, _ in self._top_children(body_at(text, ob)):
                    self.subunits.add(name)
        for p in walk(os.path.join(md, "common", "country_leader")) + \
                 walk(os.path.join(van, "common", "country_leader")):
            text = strip_comments(read(p))
            for m in re.finditer(r"leader_traits\s*=\s*\{", text):
                ob = text.index("{", m.end() - 1)
                for name, _ in self._top_children(body_at(text, ob)):
                    self.traits.add(name)
        for p in walk(os.path.join(md, "common", "country_tags")) + \
                 walk(os.path.join(REPO, "common", "country_tags")) + \
                 walk(os.path.join(md, "common", "country_tag_aliases")) + \
                 walk(os.path.join(REPO, "common", "country_tag_aliases")):
            self.tags |= set(re.findall(r"(?m)^\s*([A-Z0-9]{3})\s*=", read(p)))
        for p in walk(os.path.join(md, "common", "ideas")) + walk(os.path.join(REPO, "common", "ideas")):
            text = strip_comments(read(p))
            for m in re.finditer(r"ideas\s*=\s*\{", text):
                ob = text.index("{", m.start())
                for _, cbody in self._top_children(body_at(text, ob)):
                    for idea, _ in self._top_children(cbody):
                        self.ideas.add(idea)
        for p in walk(os.path.join(md, "interface"), ".gfx") + \
                 walk(os.path.join(REPO, "interface"), ".gfx") + \
                 walk(os.path.join(van, "interface"), ".gfx"):
            self.sprites |= set(re.findall(r'name\s*=\s*"?([A-Za-z0-9_.\-]+)"?', read(p)))
        for root in (os.path.join(md, "common", "national_focus"), os.path.join(REPO, "common", "national_focus")):
            for p in walk(root):
                text = strip_comments(read(p))
                for m in re.finditer(r"(?m)^\s*(?:focus|shared_focus|joint_focus)\s*=\s*\{", text):
                    ob = text.index("{", m.end() - 1)
                    idm = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_\-\.]+)", body_at(text, ob)[:400])
                    if idm:
                        self.focus_ids.add(idm.group(1))
        for root in (os.path.join(md, "events"), os.path.join(REPO, "events")):
            for p in walk(root):
                self.events |= set(re.findall(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+\.[0-9]+)",
                                              strip_comments(read(p))))
        self._load_tech_dlc()
        self._load_ideologies()
        self._load_states()
        for p in walk(os.path.join(md, "common", "on_actions")):
            self.md_on_action_hooks |= set(re.findall(r"(?m)^\s*([a-z_][a-z0-9_]*)\s*=\s*\{",
                                                      strip_comments(read(p))))

    @staticmethod
    def _top_children(text):
        """Direct children of a block body (skips nested blocks)."""
        out = []
        pat = re.compile(r"([A-Za-z_@][A-Za-z0-9_@\.\-]*)\s*=\s*\{")
        i = 0
        n = len(text)
        while i < n - 1:
            m = pat.match(text, i)
            if m:
                c_ob = m.end() - 1
                c_end = find_block(text, c_ob)
                if c_end is None:
                    break
                out.append((m.group(1), text[c_ob:c_end]))
                i = c_end
                continue
            i += 1
        return out

    def _load_tech_dlc(self):
        root = os.path.join(self.md, "common", "technologies")
        for p in walk(root):
            text = strip_comments(read(p))
            for m in re.finditer(r"(?m)^\s*([A-Za-z0-9_]+)\s*=\s*\{", text):
                ob = text.index("{", m.end() - 1)
                body = body_at(text, ob)
                if "enable_equipment" not in body:
                    continue
                names = set()
                for g in re.findall(r"enable_equipments?\s*=\s*\{([^}]*)\}", body):
                    names |= set(g.split())
                if re.search(r"NOT\s*=\s*\{[^}]*has_dlc\s*=\s*\"No Step Back\"", body):
                    kind = "nonsb"
                elif 'has_dlc = "No Step Back"' in body or os.path.basename(p).startswith("NSB_"):
                    kind = "nsb"
                else:
                    kind = "both"
                for n in names:
                    self.tech_dlc[n].add(kind)

    def _load_ideologies(self):
        for root in (os.path.join(self.md, "common", "ideologies"),
                     os.path.join(self.vanilla, "common", "ideologies")):
            for p in walk(root):
                text = strip_comments(read(p))
                for m in re.finditer(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", text):
                    ob = text.index("{", m.end() - 1)
                    body = body_at(text, ob)
                    tm = re.search(r"types\s*=\s*\{", body)
                    if not tm:
                        continue
                    tb = body.index("{", tm.end() - 1)
                    for name, _ in self._top_children(body_at(body, tb)):
                        if not name.startswith("@"):
                            self.ideology_family[name] = m.group(1)

    def _load_states(self):
        for root, is_ours in ((os.path.join(self.md, "history", "states"), False),
                              (os.path.join(REPO, "history", "states"), True)):
            for p in walk(root):
                text = strip_comments(read(p))
                sid_m = re.search(r"(?m)^\s*id\s*=\s*(\d+)", text)
                if not sid_m:
                    continue
                sid = sid_m.group(1)
                hb = re.search(r"history\s*=\s*\{", text)
                hist = body_at(text, text.index("{", hb.end() - 1)) if hb else text
                info = self.state.setdefault(sid, {"owner": None, "cores": set(),
                                                   "air": 0, "naval": {}, "file": os.path.basename(p)})
                info["file"] = os.path.basename(p)
                for cm in re.finditer(r"add_core_of\s*=\s*([A-Z]{3})", hist):
                    info["cores"].add(cm.group(1))
                for am in re.finditer(r"(?m)^\s*air_base\s*=\s*(\d+)", hist):
                    info["air"] = max(info["air"], int(am.group(1)))
                for bm in re.finditer(r"(?m)^\s*(\d+)\s*=\s*\{", hist):
                    bbody = body_at(hist, hist.index("{", bm.end() - 1))
                    nm = re.search(r"naval_base\s*=\s*(\d+)", bbody)
                    if nm:
                        info["naval"][bm.group(1)] = int(nm.group(1))
                # date override (2026) wins
                dm = re.search(r"(?m)^\s*2026\.1\.1\s*=\s*\{", hist)
                scope = hist
                if dm:
                    scope = body_at(hist, hist.index("{", dm.end() - 1))
                    info["cores"] = set(re.findall(r"add_core_of\s*=\s*([A-Z]{3})", scope))
                own = re.search(r"(?m)^\s*owner\s*=\s*([A-Z]{3})", scope)
                if own:
                    info["owner"] = own.group(1)
                for m in re.finditer(r"provinces\s*=\s*\{([^}]*)\}", text):
                    for pv in m.group(1).split():
                        self.prov2state[pv] = sid

    def owner_of_province(self, prov):
        sid = self.prov2state.get(str(prov))
        if not sid:
            return None, None
        return self.state.get(sid, {}).get("owner"), sid

    def owner_of_state(self, sid):
        return self.state.get(str(sid), {}).get("owner")


# ----------------------------------------------------------------- checks: S

def check_file_integrity(ctx, rep):
    for sub in ("common", "events", "history", "patches"):
        for p in our(sub):
            raw = open(p, "rb").read()
            if raw[:3] == b"\xef\xbb\xbf":
                rep.add("S-02", "BUG", "file", "UTF-8 BOM in script file", p, 1,
                        rec="Strip the BOM (the HoI4 parser logs 'Unexpected token: ?').")
            text = raw.decode("utf-8-sig", errors="replace")
            if "\ufffd" in text:
                rep.add("S-03", "BUG", "file", "Corrupted (U+FFFD) characters", p,
                        line_at(text, text.index("\ufffd")),
                        rec="Re-save the file as UTF-8 without BOM.")
            clean = strip_comments(text)
            depth = 0
            bad = None
            for i, c in enumerate(clean):
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth < 0:
                        bad = i
                        break
            if bad is not None or depth != 0:
                rep.add("S-01", "BUG", "file", "Unbalanced braces", p,
                        line_at(clean, bad if bad is not None else len(clean) - 1),
                        detail=f"final depth {depth}",
                        rec="Fix the block structure before the game loads the file.")


def check_duplicates(ctx, rep):
    # focus ids across our files (override copies may legitimately repeat MD ids)
    seen = defaultdict(list)
    for p in our("common/national_focus"):
        text = strip_comments(read(p))
        for m in re.finditer(r"(?m)^\s*(?:focus|shared_focus|joint_focus)\s*=\s*\{", text):
            ob = text.index("{", m.end() - 1)
            idm = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_\-\.]+)", body_at(text, ob)[:400])
            if idm:
                seen[idm.group(1)].append((p, line_at(text, m.start())))
    for fid, places in sorted(seen.items()):
        files = {relpath(p) for p, _ in places}
        if len(places) > 1 and len(files) > 1:
            rep.add("S-04", "BUG", "duplicate", f"Focus id '{fid}' defined in several files",
                    places[0][0], places[0][1], detail=", ".join(sorted(files)),
                    rec="Keep one definition (or make the file an intentional MD override).")

    def dup_simple(fid, paths, regex, label):
        seen = defaultdict(list)
        for p in paths:
            text = strip_comments(read(p))
            for m in re.finditer(regex, text):
                seen[m.group(1)].append((p, line_at(text, m.start())))
        for name, places in sorted(seen.items()):
            files = {relpath(p) for p, _ in places}
            if len(places) > 1 and len(files) > 1:
                rep.add(fid, "BUG", "duplicate", f"{label} '{name}' defined more than once",
                        places[0][0], places[0][1], detail=", ".join(sorted(files)))

    dup_simple("S-04", our("events"), r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+\.[0-9]+)\s*$", "Event id")
    dup_simple("S-04", our("common/scripted_effects"),
               r"(?m)^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", "Scripted effect")
    dup_simple("S-04", our("common/scripted_triggers"),
               r"(?m)^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", "Scripted trigger")
    dup_simple("S-04", our("common/opinion_modifiers"),
               r"(?m)^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", "Opinion modifier")
    # on_action hooks repeated inside one file
    for p in our("common/on_actions"):
        text = strip_comments(read(p))
        for m in re.finditer(r"(?m)^\s*on_actions\s*=\s*\{", text):
            ob = text.index("{", m.end() - 1)
            names = [n for n, _ in ctx._top_children(body_at(text, ob))]
            for name, n in Counter(names).items():
                if n > 1:
                    rep.add("S-04", "BUG", "duplicate", f"on_action hook '{name}' repeated",
                            p, line_at(text, m.start()), detail=f"{n} times in one block",
                            rec="Merge the duplicate hook blocks.")
    # duplicate idea ids inside our idea files
    for p in our("common/ideas"):
        text = strip_comments(read(p))
        names = []
        for m in re.finditer(r"ideas\s*=\s*\{", text):
            ob = text.index("{", m.start())
            for _, cbody in ctx._top_children(body_at(text, ob)):
                names += [n for n, _ in ctx._top_children(cbody)]
        for name, n in Counter(names).items():
            if n > 1:
                rep.add("S-04", "BUG", "duplicate", f"Idea '{name}' defined {n} times", p,
                        rec="Keep one definition.")


def check_duplicate_air_wings(ctx, rep):
    for p in our("history/units"):
        text = strip_comments(read(p))
        m = re.search(r"air_wings\s*=\s*\{", text)
        if not m:
            continue
        body = body_at(text, text.index("{", m.end() - 1))
        ids = [x.group(1) for x in re.finditer(r"(?m)^\s*(\d+)\s*=\s*\{", body)]
        dups = sorted({x for x in ids if ids.count(x) > 1})
        if dups:
            rep.add("S-05", "INFO", "structure",
                    "Several air wings share one state id", p,
                    detail=f"states {dups}",
                    rec="Informational: MD's own OOBs do the same (wings coexist in a state).",
                    confidence="high")


# ----------------------------------------------------------------- checks: O

SHIP_FAMILY = {
    "carrier": "carrier_hull_",
    "battle_cruiser": "battle_cruiser_hull_",
    "cruiser": "cruiser_hull_",
    "destroyer": "destroyer_hull_",
    "frigate": "frigate_hull_",
    "corvette": "corvette_hull_",
    "helicopter_operator": "helicopter_operator_hull_",
    "attack_submarine": "attack_submarine_hull_",
    "missile_submarine": "missile_submarine_hull_",
    "submarine": ("attack_submarine_hull_", "missile_submarine_hull_"),
}

# (oob tag, state owner) pairs where foreign basing is intentional
FOREIGN_BASING_OK = {
    ("ENG", "GER"), ("FRA", "GER"), ("USA", "GER"), ("USA", "JAP"),
    ("USA", "SPR"), ("USA", "ITA"), ("USA", "KOR"), ("USA", "ENG"),
    ("TUR", "NCY"), ("GER", "LIT"), ("USA", "POL"), ("USA", "ROM"),
    ("CHI", "HKG"),
}


def oob_files():
    return [p for p in our("history/units")
            if re.match(r"[A-Z]{3}_2026_(nsb|nonnsb)\.txt$", os.path.basename(p))]


def check_oob(ctx, rep):
    # O-01 set_oob wiring (NOR is renamed to NRY in the generated history)
    rename = {"NOR": "NRY"}
    for p in our("patches/history_countries"):
        text = strip_comments(read(p))
        tag = os.path.basename(p)[:3]
        for m in re.finditer(r'set_oob\s*=\s*"([^"]+)"', text):
            target = m.group(1)
            target = rename.get(target[:3], target[:3]) + target[3:]
            if not os.path.exists(os.path.join(REPO, "history", "units", target + ".txt")) and \
               not os.path.exists(os.path.join(ctx.md, "history", "units", target + ".txt")):
                rep.add("O-01", "BUG", "oob", f"set_oob points at missing file '{target}'",
                        p, line_at(text, m.start()), tag=tag)
    ship_names = defaultdict(list)
    for p in oob_files():
        tag = os.path.basename(p)[:3]
        text = strip_comments(read(p))
        defined = set()
        for m in re.finditer(r"division_template\s*=\s*\{", text):
            body = body_at(text, text.index("{", m.end() - 1))
            nm = re.search(r'name\s*=\s*"([^"]+)"', body)
            if nm:
                defined.add(nm.group(1))
            for block_re in (r"regiments\s*=\s*\{", r"support\s*=\s*\{"):
                bm = re.search(block_re, body)
                if not bm:
                    continue
                bbody = body_at(body, body.index("{", bm.end() - 1))
                batts = re.findall(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", bbody)
                if block_re.startswith("regiments") and len(batts) > 25:
                    rep.add("O-15", "BUG", "oob", "Template has more than 25 battalions",
                            p, line_at(text, m.start()), tag=tag,
                            detail=f"{nm.group(1) if nm else '?'}: {len(batts)}")
                if block_re.startswith("support") and len(batts) > 5:
                    rep.add("O-15", "BUG", "oob", "Template has more than 5 support companies",
                            p, line_at(text, m.start()), tag=tag,
                            detail=f"{nm.group(1) if nm else '?'}: {len(batts)}")
                coords = re.findall(r"x\s*=\s*(\d+)\s*y\s*=\s*(\d+)", bbody)
                dup = {c for c in coords if coords.count(c) > 1}
                if dup:
                    rep.add("O-15", "BUG", "oob", "Duplicate battalion coordinates in template",
                            p, line_at(text, m.start()), tag=tag,
                            detail=f"{nm.group(1) if nm else '?'}: {sorted(dup)}")
        for m in re.finditer(r'division_template\s*=\s*"([^"]+)"', text):
            if m.group(1) not in defined:
                rep.add("O-05", "BUG", "oob", f"Template '{m.group(1)}' used but not defined here",
                        p, line_at(text, m.start()), tag=tag)
        # divisions
        for m in re.finditer(r"division\s*=\s*\{", text):
            body = body_at(text, text.index("{", m.end() - 1))
            loc = re.search(r"location\s*=\s*(\d+)", body)
            nm = re.search(r'name\s*=\s*"([^"]+)"', body)
            if not loc:
                continue
            owner, sid = ctx.owner_of_province(loc.group(1))
            if owner is None:
                rep.add("O-02", "BUG", "oob", f"Division '{nm.group(1) if nm else '?'}' in unknown province {loc.group(1)}",
                        p, line_at(text, m.start()), tag=tag)
            elif owner != tag and (tag, owner) not in FOREIGN_BASING_OK:
                rep.add("O-02", "ACCURACY", "oob",
                        f"Division '{nm.group(1) if nm else '?'}' stationed in {owner} (state {sid})",
                        p, line_at(text, m.start()), tag=tag,
                        detail=f"state file {ctx.state.get(sid, {}).get('file', '?')}",
                        rec="Move the unit to a home (or intentionally allied) state.")
        # naval bases
        for m in re.finditer(r"naval_base\s*=\s*(\d+)", text):
            prov = m.group(1)
            owner, sid = ctx.owner_of_province(prov)
            lvl = ctx.state.get(sid, {}).get("naval", {}).get(prov, 0) if sid else 0
            if owner is None:
                rep.add("O-03", "BUG", "oob", f"naval_base province {prov} unknown", p,
                        line_at(text, m.start()), tag=tag)
            elif owner != tag and (tag, owner) not in FOREIGN_BASING_OK:
                rep.add("O-03", "ACCURACY", "oob",
                        f"naval_base {prov} is in {owner} (state {sid})", p,
                        line_at(text, m.start()), tag=tag)
            elif lvl == 0:
                rep.add("O-03", "ACCURACY", "oob",
                        f"naval_base {prov} has no naval base building in the state file",
                        p, line_at(text, m.start()), tag=tag)
        # air wings
        m = re.search(r"air_wings\s*=\s*\{", text)
        if m:
            body = body_at(text, text.index("{", m.end() - 1))
            for mm in re.finditer(r"(?m)^\s*(\d+)\s*=\s*\{", body):
                sid = mm.group(1)
                owner = ctx.owner_of_state(sid)
                air = ctx.state.get(sid, {}).get("air", 0)
                if owner is None:
                    rep.add("O-04", "BUG", "oob", f"air wing in unknown state {sid}", p,
                            line_at(text, m.start()), tag=tag)
                elif owner != tag and (tag, owner) not in FOREIGN_BASING_OK:
                    rep.add("O-04", "ACCURACY", "oob",
                            f"air wing in {owner} (state {sid})", p,
                            line_at(text, m.start()), tag=tag)
                elif air == 0:
                    rep.add("O-04", "BUG", "oob",
                            f"air wing in state {sid} without an air base", p,
                            line_at(text, m.start()), tag=tag)
        # equipment types
        for m in re.finditer(r"(?m)^\s*type\s*=\s*([A-Za-z0-9_]+)", text):
            name = m.group(1)
            if name not in ctx.equipment_md and name not in ctx.equipment:
                rep.add("O-06", "BUG", "oob", f"Unknown equipment type '{name}'", p,
                        line_at(text, m.start()), tag=tag)
            elif name not in ctx.equipment_md:
                rep.add("O-06", "BUG", "oob", f"Equipment '{name}' is vanilla-only (MD replace_path)",
                        p, line_at(text, m.start()), tag=tag)
        # stockpiles
        for m in re.finditer(r"add_equipment_to_stockpile\s*=\s*\{", text):
            body = body_at(text, text.index("{", m.end() - 1))
            tm = re.search(r"type\s*=\s*([A-Za-z0-9_]+)", body)
            am = re.search(r"amount\s*=\s*(\d+)", body)
            pr = re.search(r"producer\s*=\s*([A-Z]{3})", body)
            if tm and tm.group(1) in ctx.archetypes:
                rep.add("O-07", "BUG", "oob", f"Stockpile of an archetype '{tm.group(1)}'", p,
                        line_at(text, m.start()), tag=tag)
            if am and int(am.group(1)) <= 0:
                rep.add("O-13", "BUG", "oob", "Stockpile amount <= 0", p,
                        line_at(text, m.start()), tag=tag)
            if pr and pr.group(1) not in ctx.tags:
                rep.add("O-13", "BUG", "oob", f"Stockpile producer '{pr.group(1)}' is not a tag", p,
                        line_at(text, m.start()), tag=tag)
        # ships
        for m in re.finditer(r"ship\s*=\s*\{", text):
            body = body_at(text, text.index("{", m.end() - 1))
            nm = re.search(r'name\s*=\s*"([^"]+)"', body)
            df = re.search(r"definition\s*=\s*([A-Za-z_][A-Za-z0-9_]*)", body)
            hull = re.search(r"([a-z_]+_hull_[0-9]+)\s*=\s*\{", body)
            if nm:
                ship_names[p].append((nm.group(1), p, line_at(text, m.start())))
            if df and hull:
                fam = SHIP_FAMILY.get(df.group(1))
                if fam:
                    fams = (fam,) if isinstance(fam, str) else fam
                    if not any(hull.group(1).startswith(f) for f in fams):
                        rep.add("O-11", "ACCURACY", "oob",
                                f"Ship '{nm.group(1) if nm else '?'}' definition={df.group(1)} but hull {hull.group(1)}",
                                p, line_at(text, m.start()), tag=tag)
    for p, ships in ship_names.items():
        tag = os.path.basename(p)[:3]
        for name, n in Counter(s for s, _, _ in ships).items():
            if n > 1:
                first = next(x for x in ships if x[0] == name)
                rep.add("O-10", "BUG", "oob", f"Duplicate ship name '{name}' ({n}x)", first[1],
                        first[2], tag=tag)

def check_nsb_variants(ctx, rep):
    for p in our("history/units"):
        if not p.endswith("_2026_nonnsb.txt"):
            continue
        tag = os.path.basename(p)[:3]
        text = strip_comments(read(p))
        for m in re.finditer(r"(?m)^\s*type\s*=\s*([A-Za-z0-9_]+)", text):
            name = m.group(1)
            kinds = ctx.tech_dlc.get(name)
            if kinds and "nsb" in kinds and "nonsb" not in kinds and "both" not in kinds:
                rep.add("O-08", "BUG", "oob", f"NSB-only equipment '{name}' in non-NSB OOB",
                        p, line_at(text, m.start()), tag=tag,
                        rec="Swap for a non-NSB equivalent.")


# ----------------------------------------------------------------- checks: H

def check_history(ctx, rep):
    for p in our("patches/history_countries"):
        tag = os.path.basename(p)[:3]
        text = strip_comments(read(p))
        ruling = re.search(r"ruling_party\s*=\s*([A-Za-z_]+)", text)
        if ruling:
            rf = ctx.ideology_family.get(ruling.group(1), ruling.group(1))
            for m in re.finditer(r"create_country_leader\s*=\s*\{", text):
                body = body_at(text, text.index("{", m.end() - 1))
                ide = re.search(r"ideology\s*=\s*([A-Za-z_\-]+)", body)
                if ide:
                    lf = ctx.ideology_family.get(ide.group(1), ide.group(1))
                    if lf != rf:
                        rep.add("H-01", "BUG", "history",
                                f"Leader ideology '{ide.group(1)}' ({lf}) outside ruling family '{ruling.group(1)}' ({rf})",
                                p, line_at(text, m.start()), tag=tag,
                                rec="The game will not show this leader as head of state.")
        for m in re.finditer(r"traits\s*=\s*\{([^}]*)\}", text):
            for tr in m.group(1).split():
                if tr not in ctx.traits:
                    rep.add("H-02", "BUG", "history", f"Unknown leader trait '{tr}'", p,
                            line_at(text, m.start()), tag=tag)
        for m in re.finditer(r'picture\s*=\s*"([^"]+\.dds)"', text):
            ref = m.group(1)
            ok = False
            if "/" in ref:
                ok = any(os.path.exists(os.path.join(b, ref)) for b in (ctx.md, ctx.vanilla)) or \
                     any(os.path.exists(os.path.join(b, "portraits", ref)) for b in (ctx.md, ctx.vanilla))
            else:
                ok = any(os.path.exists(os.path.join(b, "gfx", "leaders", tag, ref))
                         for b in (ctx.md, ctx.vanilla))
            if not ok:
                rep.add("H-03", "BUG", "history", f"Missing portrait '{ref}'", p,
                        line_at(text, m.start()), tag=tag)
        # party popularity sums
        vals = {}
        for m in re.finditer(r"party_pop_array\^(\d+)\s*=\s*([0-9.]+)", text):
            vals[int(m.group(1))] = float(m.group(2))
        if vals:
            total = sum(vals.values())
            if abs(total - 1.0) > 0.02:
                rep.add("H-04", "ACCURACY", "history",
                        f"party_pop_array sums to {total:.3f}, not 1.0", p,
                        line_at(text, text.index("party_pop_array")), tag=tag)
        rp = re.search(r"set_variable\s*=\s*\{\s*ruling_party\s*=\s*(\d+)", text)
        if rp and vals:
            idx = int(rp.group(1))
            if idx not in vals:
                rep.add("H-05", "BUG", "history",
                        f"ruling_party index {idx} has no party_pop_array value", p,
                        line_at(text, rp.start()), tag=tag)
            elif vals[idx] <= 0:
                rep.add("H-05", "BUG", "history",
                        f"ruling_party index {idx} has zero popularity", p,
                        line_at(text, rp.start()), tag=tag)
        # elections
        em = re.search(r"elections_allowed\s*=\s*(yes|no)", text)
        fm = re.search(r"election_frequency\s*=\s*(\d+)", text)
        if em and em.group(1) == "no" and fm and int(fm.group(1)) < 900:
            rep.add("H-06", "NOTE", "history",
                    "elections_allowed = no with a real election_frequency", p,
                    line_at(text, em.start()), tag=tag)
        # GDP / debt sanity
        gm = re.search(r"gdp_per_capita\s*=\s*([0-9.]+)", text)
        if gm and not (0.05 <= float(gm.group(1)) <= 150):
            rep.add("H-07", "ACCURACY", "history",
                    f"gdp_per_capita = {gm.group(1)} outside plausible range (thousands USD)",
                    p, line_at(text, gm.start()), tag=tag)
        dm = re.search(r"var\s*=\s*debt\s+value\s*=\s*([0-9.]+)", text)
        if dm and float(dm.group(1)) > 200000:
            rep.add("H-07", "BUG", "history", f"debt = {dm.group(1)} (billions) is not plausible", p,
                    line_at(text, dm.start()), tag=tag, confidence="medium")
        # wars
        for m in re.finditer(r"declare_war_on\s*=\s*\{", text):
            body = body_at(text, text.index("{", m.end() - 1))
            tgt = re.search(r"target\s*=\s*([A-Z]{3})", body)
            if tgt and tgt.group(1) not in ctx.tags:
                rep.add("H-10", "BUG", "history", f"declare_war_on unknown target {tgt.group(1)}",
                        p, line_at(text, m.start()), tag=tag)
            if tgt and tgt.group(1) == tag:
                rep.add("H-10", "BUG", "history", "declare_war_on itself", p,
                        line_at(text, m.start()), tag=tag)


# ----------------------------------------------------------------- checks: F

def check_focus(ctx, rep):
    for p in our("common/national_focus"):
        name = os.path.basename(p)
        if not name.startswith("md2026_"):
            continue
        text = strip_comments(read(p))
        ids, coords, icons = [], [], []
        for m in re.finditer(r"(?m)^\s*(?:focus|shared_focus|joint_focus)\s*=\s*\{", text):
            ob = text.index("{", m.end() - 1)
            body = body_at(text, ob)
            idm = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_\-\.]+)", body[:300])
            if idm:
                ids.append((idm.group(1), line_at(text, m.start())))
            xy = re.search(r"(?m)^\s*x\s*=\s*(-?\d+)\s*\n\s*y\s*=\s*(-?\d+)", body)
            if xy and "relative_position_id" not in body:
                coords.append((xy.group(1), xy.group(2), line_at(text, m.start())))
            ic = re.search(r"(?m)^\s*icon\s*=\s*([A-Za-z0-9_.\-]+)", body)
            if ic:
                icons.append((ic.group(1), line_at(text, m.start())))
        for fid, ln in ids:
            if fid not in ctx.focus_ids:
                rep.add("F-01", "BUG", "focus", f"Focus '{fid}' not found anywhere", p, ln)
        seen = {}
        for x, y, ln in coords:
            if (x, y) in seen:
                rep.add("F-01", "ACCURACY", "focus", f"Focus grid position ({x},{y}) used twice",
                        p, ln, detail=f"first at line {seen[(x, y)]}")
            seen[(x, y)] = ln
        for icon, ln in icons:
            if icon.lower() in ("yes", "no"):
                continue
            cands = (icon, "GFX_" + icon, "GFX_focus_" + icon, "GFX_idea_" + icon,
                     "GFX_decision_" + icon, "GFX_goal_" + icon,
                     icon.replace("GFX_", ""))
            if not any(c in ctx.sprites for c in cands):
                rep.add("F-01", "NOTE", "focus", f"Focus icon '{icon}' not found in interface .gfx",
                        p, ln, confidence="medium")
        # prerequisites must exist
        for m in re.finditer(r"prerequisite\s*=\s*\{\s*focus\s*=\s*([A-Za-z0-9_]+)", text):
            if m.group(1) not in ctx.focus_ids:
                rep.add("F-01", "BUG", "focus", f"Prerequisite focus '{m.group(1)}' missing", p,
                        line_at(text, m.start()))


# ----------------------------------------------------------------- checks: E

def check_events_decisions(ctx, rep):
    for p in our("events"):
        text = strip_comments(read(p))
        for m in re.finditer(r"(?:country_event|news_event)\s*=\s*\{\s*id\s*=\s*([A-Za-z0-9_.]+)", text):
            if m.group(1) not in ctx.events:
                rep.add("E-01", "BUG", "events", f"Event reference '{m.group(1)}' not defined",
                        p, line_at(text, m.start()))
        for m in re.finditer(r"(?m)^\s*option\s*=\s*\{\s*\}", text):
            rep.add("E-01", "NOTE", "events", "Empty event option", p, line_at(text, m.start()))
    tech_cats = set()
    for p in our("common/technology_tags") + walk(os.path.join(ctx.md, "common", "technology_tags")):
        tech_cats |= set(re.findall(r"(?m)^\s*(CAT_[A-Za-z0-9_]+)", read(p)))
    cats = set()
    for p in our("common/decisions/categories") + walk(os.path.join(ctx.md, "common", "decisions", "categories")):
        cats |= {n for n, _ in ctx._top_children(strip_comments(read(p)))}
    allowed = {c.lower() for c in cats} | {c.lower() for c in tech_cats} | \
              {"cat_" + c.lower() for c in cats}
    for p in our("common/decisions"):
        if "categories" in p:
            continue
        text = strip_comments(read(p))
        for m in re.finditer(r"(?m)^\s*category\s*=\s*([A-Za-z0-9_]+)", text):
            cat = m.group(1)
            if cat.lower() not in allowed:
                rep.add("E-02", "BUG", "decisions", f"Unknown decision category '{cat}'", p,
                        line_at(text, m.start()))
    for p in our("common/on_actions"):
        text = strip_comments(read(p))
        for m in re.finditer(r"(?m)^\s*(on_[a-z_]+)\s*=\s*\{", text):
            if ctx.md_on_action_hooks and m.group(1) not in ctx.md_on_action_hooks:
                rep.add("E-03", "BUG", "on_actions", f"on_action hook '{m.group(1)}' not in MD",
                        p, line_at(text, m.start()), confidence="medium")


# ----------------------------------------------------------------- checks: L

def check_loc(ctx, rep):
    langs = {}
    for p in our("localisation", ".yml"):
        lang = os.path.basename(os.path.dirname(p))
        text = read(p)
        for m in re.finditer(r"(?m)^\s*([A-Za-z0-9_.\-]+):\d*\s", text):
            langs.setdefault(lang, {})[m.group(1)] = p
    en = langs.get("english", {})
    for lang, keys in sorted(langs.items()):
        if lang == "english":
            continue
        for k in sorted(en):
            if re.fullmatch(r"l_[a-z]{3,12}", k):
                continue  # language header (l_english:, l_polish:)
            if k not in keys:
                rep.add("L-01", "BUG", "loc", f"Key '{k}' missing in {lang}", en[k])

    def placeholders(v):
        return Counter(re.findall(r"\$([A-Za-z0-9_]+)\$", v))

    for k in sorted(set(en)):
        base = None
        for p in our("localisation", ".yml"):
            text = read(p)
            m = re.search(r'(?m)^\s*' + re.escape(k) + r':\d*\s*"(.*)"\s*$', text)
            if not m:
                continue
            if base is None:
                base = (p, m.group(1))
            elif placeholders(base[1]) != placeholders(m.group(1)):
                rep.add("L-02", "ACCURACY", "loc", f"Placeholder mismatch for '{k}'", p,
                        rec="Keep $variables$ identical across languages.")


# ----------------------------------------------------------------- checks: B

def check_bookmark(ctx, rep):
    p = os.path.join(REPO, "common", "bookmarks", "md2026_bookmark.txt")
    if not os.path.exists(p):
        rep.add("B-01", "BUG", "bookmark", "Bookmark file missing", p)
        return
    text = strip_comments(read(p))
    for m in re.finditer(r'(?m)^\s*"([A-Z]{3})"\s*=\s*\{', text):
        tag = m.group(1)
        ob = text.index("{", m.end() - 1)
        body = body_at(text, ob)
        if "version" not in body:
            rep.add("B-01", "BUG", "bookmark", f"Bookmark entry {tag} has no version key", p,
                    line_at(text, m.start()), tag=tag)
        if tag not in ctx.tags:
            rep.add("B-01", "BUG", "bookmark", f"Bookmark tag {tag} does not exist", p,
                    line_at(text, m.start()), tag=tag)


# ----------------------------------------------------------------- checks: C

NATO_MD_STARTUP = {
    "ALB", "BEL", "BUL", "CAN", "CRO", "CZE", "DEN", "EST", "FRA", "GER", "GRE",
    "HOL", "HUN", "ICE", "ITA", "LAT", "LIT", "LUX", "NRY", "POL", "POR", "ROM",
    "SLO", "SLV", "SPR", "TUR", "ENG", "USA",
}


def check_cross_mod(ctx, rep):
    usa = os.path.join(REPO, "patches", "history_countries", "USA.txt")
    if os.path.exists(usa):
        text = strip_comments(read(usa))
        added = set(re.findall(r"add_to_array\s*=\s*\{\s*global\.nato_members\s*=\s*([A-Z]{3})", text))
        dups = sorted(added & NATO_MD_STARTUP)
        if dups:
            rep.add("C-01", "ACCURACY", "cross-mod",
                    "NATO array entries duplicated by MD's startup pass", usa,
                    detail=f"our patch adds {dups}; MD's setup_global_arrays adds them too "
                           f"(no clear_array) -> duplicates in global.nato_members",
                    rec="Only add the tags MD's 2026 branch misses (MNT, FYR, FIN, SWE) or guard with is_in_array.")
    sov = os.path.join(REPO, "patches", "history_countries", "SOV.txt")
    if os.path.exists(sov):
        text = strip_comments(read(sov))
        if re.search(r"remove_from_array\s*=\s*\{\s*global\.CSTO_member\s*=\s*ARM", text):
            rep.add("C-02", "BUG", "cross-mod",
                    "CSTO removal runs before MD re-adds Armenia at on_startup", sov,
                    detail="history (2026.1.1) runs before on_startup; MD's setup_global_arrays "
                           "does add_to_array = { global.CSTO_member = ARM } with no clear_array, "
                           "so the removal is undone.",
                    rec="Move the removal into our on_startup effect (which runs after MD's) or a decision.")


# ----------------------------------------------------------------- checks: G

def check_repro(ctx, rep, quiet=False):
    import rebase
    captured = {}
    removals = []

    class OsShim:
        def __getattr__(self, name):
            return getattr(os, name)

        @staticmethod
        def remove(path):
            removals.append(path)

    real_write = rebase.write
    real_os = rebase.os

    def cap_write(path, text):
        captured[os.path.normcase(os.path.abspath(path))] = text

    rebase.write = cap_write
    rebase.os = OsShim()
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exp = rebase.rebase_focus(ctx.md)
            rebase.cleanup_old_focus_copies(exp)
            rebase.generate_bookmark()
            rebase.rebase_history(ctx.md, {"NOR": "NRY"})
            rebase.generate_tech_effects(ctx.md)
            rebase.generate_search_filters(ctx.md)
            rebase.generate_unit_fixes(ctx.md)
    finally:
        rebase.write = real_write
        rebase.os = real_os

    for path, text in sorted(captured.items()):
        if not os.path.exists(path):
            rep.add("G-01", "BUG", "repro", "Generator would create a file that is missing on disk",
                    path, rec="Run python tools/rebase.py generate.")
            continue
        disk = read(path).replace("\r\n", "\n")
        if disk != text.replace("\r\n", "\n"):
            dlines = disk.split("\n")
            glines = text.replace("\r\n", "\n").split("\n")
            first = next((i for i, (a, b) in enumerate(zip(dlines, glines)) if a != b), 0)
            rep.add("G-01", "BUG", "repro", "Generated file differs from a fresh regeneration",
                    path, first + 1,
                    detail=f"{len(dlines)} vs {len(glines)} lines; first difference at line {first + 1}",
                    rec="Run python tools/rebase.py generate and review the diff (stale MD override).")
    expected = {os.path.normcase(os.path.abspath(x)) for x in captured}
    for sub in ("common/national_focus", "history/countries", "history/states"):
        for p in our(sub):
            ap = os.path.normcase(os.path.abspath(p))
            if ap in expected:
                continue
            base = os.path.basename(p)
            if sub == "common/national_focus" and base.startswith("md2026_"):
                continue
            rep.add("G-02", "NOTE", "repro", "File not produced by the generator (leftover copy?)",
                    p, confidence="medium",
                    rec="Confirm it is hand-maintained or remove it.")
    if removals and not quiet:
        rep.add("G-03", "NOTE", "repro", "Generator would delete obsolete copies",
                detail=", ".join(sorted(relpath(x) for x in removals)[:10]),
                confidence="medium")


# ----------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=None)
    ap.add_argument("--vanilla", default=None)
    ap.add_argument("--json", default=None)
    ap.add_argument("--no-repro", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    md = resolve_path(args.md, "MD_PATH", MD_REL, "descriptor.mod")
    vanilla = resolve_path(args.vanilla, "HOI4_PATH", VANILLA_REL, "launcher-settings.json")

    import rebase
    rebase.VANILLA = vanilla
    rebase.DEFAULT_MD = md

    print(f"MD:      {md}")
    print(f"Vanilla: {vanilla}")
    ctx = Ctx(md, vanilla)
    print(f"loaded: {len(ctx.equipment_md)} MD equipment | {len(ctx.traits)} traits | "
          f"{len(ctx.ideas)} ideas | {len(ctx.focus_ids)} focuses | {len(ctx.state)} states")

    rep = Report()
    check_file_integrity(ctx, rep)
    check_duplicates(ctx, rep)
    check_duplicate_air_wings(ctx, rep)
    check_oob(ctx, rep)
    check_nsb_variants(ctx, rep)
    check_history(ctx, rep)
    check_focus(ctx, rep)
    check_events_decisions(ctx, rep)
    check_loc(ctx, rep)
    check_bookmark(ctx, rep)
    check_cross_mod(ctx, rep)
    if not args.no_repro:
        check_repro(ctx, rep, args.quiet)

    print()
    by_cat = defaultdict(int)
    for it in rep.items:
        by_cat[it["category"]] += 1
    for cat, n in sorted(by_cat.items()):
        print(f"  {cat:12} {n:4} findings")
    print()
    for sev in ("BLOCKER", "BUG", "ACCURACY", "NOTE", "INFO"):
        items = [i for i in rep.items if i["severity"] == sev]
        if not items:
            continue
        print(f"=== {sev} ({len(items)}) ===")
        if args.quiet:
            continue
        for i in items:
            loc = f"  [{i['file']}:{i['line']}]" if i["file"] else ""
            tag = f" {i['tag']}" if i["tag"] else ""
            print(f"  {i['id']}{tag} {i['title']}{loc}")
            if i["detail"]:
                print(f"      {i['detail']}")
    if args.json:
        rep.json(args.json)
        print(f"\nwrote {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
