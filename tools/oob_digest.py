#!/usr/bin/env python3
"""Read-only OOB digest for the 2026 reality audit.

Prints a per-country fact sheet (divisions, ships, air wings, stockpiles,
wiring) that can be pasted into a subagent prompt or saved as JSON.

Usage:
    python tools/oob_digest.py --tag USA
    python tools/oob_digest.py --all --json docs/oob_digest.json
    python tools/oob_digest.py --all --outdir C:/temp/digests
"""

import argparse
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


def resolve(arg, env, rel, marker):
    """Locate an install: explicit arg, env var, then Steam's own libraries."""
    found = rebase.resolve_install(rel, marker, override=arg, env=env)
    if not found or not os.path.exists(os.path.join(found, marker)):
        raise SystemExit(f"could not locate {rel}; set {env}")
    return found


def read(p):
    with open(p, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def strip_comments(text):
    return "\n".join(line.split("#")[0] for line in text.split("\n"))


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
    return len(text)


def block(text, start):
    return text[start:find_block(text, start)]


def children(text):
    out = []
    pat = re.compile(r"([A-Za-z_@][A-Za-z0-9_@\.\-]*)\s*=\s*\{")
    i = 0
    while i < len(text) - 1:
        m = pat.match(text, i)
        if m:
            ob = m.end() - 1
            ce = find_block(text, ob)
            out.append((m.group(1), text[ob:ce]))
            i = ce
            continue
        i += 1
    return out


# --------------------------------------------------------------- reference

class Ref:
    def __init__(self, md):
        self.prov2state = {}
        self.state = {}
        self.state_names = {}
        for root in (os.path.join(md, "history", "states"), os.path.join(REPO, "history", "states")):
            for dp, _, ns in os.walk(root):
                for n in ns:
                    if not n.endswith(".txt"):
                        continue
                    t = strip_comments(read(os.path.join(dp, n)))
                    sid = re.search(r"(?m)^\s*id\s*=\s*(\d+)", t)
                    if not sid:
                        continue
                    sid = sid.group(1)
                    info = self.state.setdefault(sid, {"owner": None, "air": 0, "naval": {}, "file": n})
                    info["file"] = n
                    hb = re.search(r"history\s*=\s*\{", t)
                    hist = block(t, hb.end() - 1) if hb else t
                    for am in re.finditer(r"(?m)^\s*air_base\s*=\s*(\d+)", hist):
                        info["air"] = max(info["air"], int(am.group(1)))
                    for bm in re.finditer(r"(?m)^\s*(\d+)\s*=\s*\{", hist):
                        bb = block(hist, hist.index("{", bm.end() - 1))
                        nm = re.search(r"naval_base\s*=\s*(\d+)", bb)
                        if nm:
                            info["naval"][bm.group(1)] = int(nm.group(1))
                    dm = re.search(r"(?m)^\s*2026\.1\.1\s*=\s*\{", hist)
                    scope = hist
                    if dm:
                        scope = block(hist, hist.index("{", dm.end() - 1))
                    own = re.search(r"(?m)^\s*owner\s*=\s*([A-Z]{3})", scope)
                    if own:
                        info["owner"] = own.group(1)
                    for m in re.finditer(r"provinces\s*=\s*\{([^}]*)\}", t):
                        for pv in m.group(1).split():
                            self.prov2state[pv] = sid
        # real state names from MD localisation
        for dp, _, ns in os.walk(os.path.join(md, "localisation", "english")):
            for n in ns:
                if not n.endswith(".yml"):
                    continue
                for m in re.finditer(r'(?m)^\s*STATE_(\d+):\d*\s*"([^"]+)"', read(os.path.join(dp, n))):
                    self.state_names[m.group(1)] = m.group(2)

    def prov(self, pv):
        sid = self.prov2state.get(str(pv))
        if not sid:
            return None, None
        return sid, self.state.get(sid, {})

    def name(self, sid):
        return self.state_names.get(str(sid), f"STATE_{sid}")


# --------------------------------------------------------------- digest

def parse_oob(path, ref):
    text = strip_comments(read(path))
    tag = os.path.basename(path)[:3]
    out = {"tag": tag, "file": os.path.relpath(path, REPO).replace("\\", "/"),
           "templates": [], "divisions": [], "fleets": [], "air_wings": [],
           "stockpiles": [], "totals": {}}

    for m in re.finditer(r"division_template\s*=\s*\{", text):
        b = block(text, text.index("{", m.end() - 1))
        name = re.search(r'name\s*=\s*"([^"]+)"', b)
        tmpl = {"name": name.group(1) if name else "?", "regiments": {}, "support": {}}
        for kind, re_key in (("regiments", r"regiments\s*=\s*\{"), ("support", r"support\s*=\s*\{")):
            bm = re.search(re_key, b)
            if not bm:
                continue
            bb = block(b, b.index("{", bm.end() - 1))
            tmpl[kind] = dict(Counter(x.group(1) for x in
                                      re.finditer(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", bb)))
        out["templates"].append(tmpl)

    for m in re.finditer(r"division\s*=\s*\{", text):
        b = block(text, text.index("{", m.end() - 1))
        nm = re.search(r'name\s*=\s*"([^"]+)"', b)
        loc = re.search(r"location\s*=\s*(\d+)", b)
        tmpl = re.search(r'division_template\s*=\s*"([^"]+)"', b)
        exp = re.search(r"start_experience_factor\s*=\s*([0-9.]+)", b)
        eq = re.search(r"start_equipment_factor\s*=\s*([0-9.]+)", b)
        sid, info = ref.prov(loc.group(1)) if loc else (None, {})
        out["divisions"].append({
            "name": nm.group(1) if nm else "?",
            "template": tmpl.group(1) if tmpl else "?",
            "province": loc.group(1) if loc else None,
            "state": sid,
            "state_name": ref.name(sid) if sid else None,
            "owner": info.get("owner") if info else None,
            "exp": exp.group(1) if exp else None,
            "equip": eq.group(1) if eq else None,
        })

    for m in re.finditer(r"fleet\s*=\s*\{", text):
        b = block(text, text.index("{", m.end() - 1))
        nm = re.search(r'name\s*=\s*"([^"]+)"', b)
        nb = re.search(r"naval_base\s*=\s*(\d+)", b)
        sid, info = ref.prov(nb.group(1)) if nb else (None, {})
        fleet = {"name": nm.group(1) if nm else "?", "naval_base": nb.group(1) if nb else None,
                 "base_state": sid, "base_state_name": ref.name(sid) if sid else None,
                 "base_owner": info.get("owner") if info else None,
                 "base_level": info.get("naval", {}).get(nb.group(1)) if info and nb else None,
                 "task_forces": []}
        for tm in re.finditer(r"task_force\s*=\s*\{", b):
            tb = block(b, b.index("{", tm.end() - 1))
            tname = re.search(r'name\s*=\s*"([^"]+)"', tb)
            tf = {"name": tname.group(1) if tname else "?", "ships": []}
            for sm in re.finditer(r"ship\s*=\s*\{", tb):
                sb = block(tb, tb.index("{", sm.end() - 1))
                sn = re.search(r'name\s*=\s*"([^"]+)"', sb)
                df = re.search(r"definition\s*=\s*([A-Za-z_][A-Za-z0-9_]*)", sb)
                hull = re.search(r"([a-z_]+_hull_[0-9]+)\s*=\s*\{", sb)
                hb = block(sb, sb.index("{", hull.start()) ) if hull else ""
                ver = re.search(r'version_name\s*=\s*"([^"]+)"', hb)
                own = re.search(r"owner\s*=\s*([A-Z]{3})", hb)
                cre = re.search(r"creator\s*=\s*([A-Z]{3})", hb)
                tf["ships"].append({
                    "name": sn.group(1) if sn else "?",
                    "definition": df.group(1) if df else "?",
                    "hull": hull.group(1) if hull else "?",
                    "class": ver.group(1) if ver else None,
                    "owner": own.group(1) if own else None,
                    "creator": cre.group(1) if cre else None,
                })
            fleet["task_forces"].append(tf)
        out["fleets"].append(fleet)

    m = re.search(r"air_wings\s*=\s*\{", text)
    if m:
        b = block(text, text.index("{", m.end() - 1))
        for sm in re.finditer(r"(?m)^\s*(\d+)\s*=\s*\{", b):
            sb = block(b, b.index("{", sm.end() - 1))
            wing = {"state": sm.group(1), "state_name": ref.name(sm.group(1)),
                    "owner": ref.state.get(sm.group(1), {}).get("owner"),
                    "air_base": ref.state.get(sm.group(1), {}).get("air"),
                    "name": None, "aircraft": []}
            nm = re.search(r'name\s*=\s*"([^"]+)"', sb)
            wing["name"] = nm.group(1) if nm else None
            for am in re.finditer(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{", sb):
                ab = block(sb, sb.index("{", am.end() - 1))
                amount = re.search(r"amount\s*=\s*(\d+)", ab)
                if not amount:
                    continue
                ver = re.search(r'version_name\s*=\s*"([^"]+)"', ab)
                own = re.search(r"owner\s*=\s*([A-Z]{3})", ab)
                cre = re.search(r"creator\s*=\s*([A-Z]{3})", ab)
                wing["aircraft"].append({"airframe": am.group(1), "amount": int(amount.group(1)),
                                         "version": ver.group(1) if ver else None,
                                         "owner": own.group(1) if own else None,
                                         "creator": cre.group(1) if cre else None})
            out["air_wings"].append(wing)

    for m in re.finditer(r"add_equipment_to_stockpile\s*=\s*\{", text):
        b = block(text, text.index("{", m.end() - 1))
        ty = re.search(r"type\s*=\s*([A-Za-z0-9_]+)", b)
        am = re.search(r"amount\s*=\s*(\d+)", b)
        pr = re.search(r"producer\s*=\s*([A-Z]{3})", b)
        if ty:
            out["stockpiles"].append({"type": ty.group(1),
                                      "amount": int(am.group(1)) if am else None,
                                      "producer": pr.group(1) if pr else None})

    ships = [s for f in out["fleets"] for tf in f["task_forces"] for s in tf["ships"]]
    planes = [a for w in out["air_wings"] for a in w["aircraft"]]
    out["totals"] = {
        "divisions": len(out["divisions"]),
        "templates": len(out["templates"]),
        "ships": len(ships),
        "carriers": sum(1 for s in ships if s["definition"] == "carrier"),
        "submarines": sum(1 for s in ships if "submarine" in s["definition"]),
        "air_wings": len(out["air_wings"]),
        "aircraft": sum(a["amount"] for a in planes),
        "aircraft_types": dict(Counter(a["airframe"] for a in planes)),
        "stockpile_lines": len(out["stockpiles"]),
    }
    return out


def history_info(tag):
    patch_tag = {"NRY": "NOR"}.get(tag, tag)
    p = os.path.join(REPO, "patches", "history_countries", patch_tag + ".txt")
    if not os.path.exists(p):
        return {}
    t = strip_comments(read(p))
    return {
        "patch": os.path.relpath(p, REPO).replace("\\", "/"),
        "set_oob": re.findall(r'set_oob\s*=\s*"([^"]+)"', t),
        "tech_tier": re.findall(r"(?m)^\s*(md2026_tier\d_2026_techs)\s*=", t),
        "gdp_per_capita": (re.search(r"gdp_per_capita\s*=\s*([0-9.]+)", t) or [None, None])[1],
        "debt": (re.search(r"var\s*=\s*debt\s+value\s*=\s*([0-9.]+)", t) or [None, None])[1],
        "ruling_party": (re.search(r"set_politics\s*=\s*\{[^}]*ruling_party\s*=\s*([A-Za-z_]+)", t) or [None, None])[1],
        "leader": (re.search(r'create_country_leader\s*=\s*\{[^}]*name\s*=\s*"([^"]+)"', t) or [None, None])[1],
    }


def render(d):
    tag = d["tag"]
    L = []
    L.append(f"# {tag} - 2026 OOB digest")
    h = d["history"]
    L.append("")
    L.append(f"- patch: `{h.get('patch', '?')}`")
    L.append(f"- set_oob: {h.get('set_oob', '?')}  |  tech tier: {h.get('tech_tier', '?')}")
    L.append(f"- gdp_per_capita: {h.get('gdp_per_capita')} (thousand USD)  |  debt: {h.get('debt')} (bn USD)")
    L.append(f"- ruling party: {h.get('ruling_party')}  |  leader: {h.get('leader')}")
    t = d["totals"]
    L.append(f"- totals: {t['divisions']} divisions, {t['ships']} ships "
             f"({t['carriers']} carriers, {t['submarines']} submarines), "
             f"{t['air_wings']} air wings / {t['aircraft']} aircraft")
    L.append("")
    L.append("## Division templates")
    for tm in d["templates"]:
        reg = ", ".join(f"{k} x{v}" for k, v in tm["regiments"].items())
        sup = ", ".join(f"{k} x{v}" for k, v in tm["support"].items())
        L.append(f"- **{tm['name']}**: {reg}" + (f"  |  support: {sup}" if sup else ""))
    L.append("")
    L.append(f"## Ground deployments ({len(d['divisions'])})")
    for u in d["divisions"]:
        flag = ""
        if u["owner"] and u["owner"] != tag:
            flag = f"  <-- FOREIGN ({u['owner']})"
        L.append(f"- {u['name']} [{u['template']}] @ {u['state_name']} ({u['owner']})"
                 f" exp {u['exp']} eq {u['equip']}{flag}")
    L.append("")
    L.append(f"## Navy ({t['ships']} ships)")
    for f in d["fleets"]:
        n = sum(len(tf["ships"]) for tf in f["task_forces"])
        L.append(f"- **{f['name']}** ({n} ships) - base {f['base_state_name']} "
                 f"({f['base_owner']}, level {f['base_level']})")
        for tf in f["task_forces"]:
            L.append(f"  - {tf['name']}: " + "; ".join(
                f"{s['name']} [{s['class']} / {s['hull']}]" for s in tf["ships"]))
    L.append("")
    L.append(f"## Air wings ({t['aircraft']} aircraft)")
    for w in d["air_wings"]:
        ac = "; ".join(f"{a['version']} ({a['airframe']}) x{a['amount']}" for a in w["aircraft"])
        flag = ""
        if w["owner"] and w["owner"] != tag:
            flag = f"  <-- FOREIGN ({w['owner']})"
        L.append(f"- {w['name']} @ {w['state_name']} (air base {w['air_base']}): {ac}{flag}")
    L.append("")
    L.append("## Stockpiles")
    for s in d["stockpiles"]:
        L.append(f"- {s['type']} x{s['amount']} (producer {s['producer']})")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=None)
    ap.add_argument("--tag")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", default=None)
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--text", action="store_true", help="print digests to stdout")
    args = ap.parse_args()

    md = resolve(args.md, "MD_PATH", MD_REL, "descriptor.mod")
    ref = Ref(md)

    if args.tag:
        tags = [args.tag.upper()]
    elif args.all:
        tags = sorted({n[:3] for n in os.listdir(os.path.join(REPO, "history", "units"))
                       if re.match(r"[A-Z]{3}_2026_nsb\.txt$", n)})
    else:
        sys.exit("pass --tag TAG or --all")

    digests = {}
    for tag in tags:
        nsb = os.path.join(REPO, "history", "units", f"{tag}_2026_nsb.txt")
        nonnsb = os.path.join(REPO, "history", "units", f"{tag}_2026_nonnsb.txt")
        d = parse_oob(nsb, ref) if os.path.exists(nsb) else parse_oob(nonnsb, ref)
        d["history"] = history_info(tag)
        d["nonnsb_file"] = os.path.relpath(nonnsb, REPO).replace("\\", "/") \
            if os.path.exists(nonnsb) else None
        digests[tag] = d

    if args.outdir:
        os.makedirs(args.outdir, exist_ok=True)
        for tag, d in digests.items():
            with open(os.path.join(args.outdir, f"{tag}.md"), "w", encoding="utf-8", newline="\n") as f:
                f.write(render(d) + "\n")
        print(f"wrote {len(digests)} digests to {args.outdir}")
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as f:
            json.dump(digests, f, ensure_ascii=False, indent=1)
        print(f"wrote {args.json}")
    if args.text or (not args.json and not args.outdir):
        for tag in tags:
            print(render(digests[tag]))
            print("\n" + "=" * 80 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
