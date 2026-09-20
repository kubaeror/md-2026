"""Builds patches/focus_inject.json from the old tree copies.

Maps every MD 2.0 focus tree belonging to a country (tag) to the 2026 shared
focus root(s) that should be injected into it. Run once, before the old copies
are deleted; afterwards the JSON is the hand-maintained source of truth.
"""

import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MD = r"D:\SteamLibrary\steamapps\workshop\content\394360\2777392649"
sys.path.insert(0, os.path.join(REPO, "tools"))
import rebase  # noqa: E402

md = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MD

# root shared focus -> country tag (from allow_branch in md2026_*_focus.txt)
roots = {}
for name in sorted(os.listdir(os.path.join(REPO, "common", "national_focus"))):
    if not name.startswith("md2026_") or not name.endswith(".txt"):
        continue
    text = rebase.read(os.path.join(REPO, "common", "national_focus", name))
    for m in re.finditer(r"(?s)shared_focus\s*=\s*\{\s*id\s*=\s*(MD2026_[A-Za-z0-9_]+).*?allow_branch\s*=\s*\{([^}]*)\}", text):
        root = m.group(1)
        tags = re.findall(r"(?:original_tag|tag)\s*=\s*([A-Z]{3})", m.group(2))
        for t in tags:
            roots.setdefault(t, []).append(root)
print("rooty 2026 per tag:", {k: v for k, v in sorted(roots.items())})

root_dir = os.path.join(md, "common", "national_focus")
out = {}
for name in sorted(os.listdir(root_dir)):
    if not name.endswith(".txt"):
        continue
    text = rebase.read(os.path.join(root_dir, name))
    for m in re.finditer(r"focus_tree\s*=\s*\{", text):
        ob = text.index("{", m.start())
        end = rebase.find_block(text, ob)
        head = text[ob:end][:1500]
        idm = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+)", head)
        if not idm:
            continue
        tree_id = idm.group(1)
        tags = set(re.findall(r"(?:original_tag|tag)\s*=\s*([A-Z]{3})", head))
        for t in tags:
            if t in roots:
                out.setdefault(tree_id, [])
                for r in roots[t]:
                    if r not in out[tree_id]:
                        out[tree_id].append(r)

# countries without a dedicated tree use the generic tree
for t, rs in roots.items():
    if not any(rs == v for v in out.values()) and not any(r in sum(out.values(), []) for r in rs):
        for r in rs:
            out.setdefault("generic_focus", [])
            if r not in out["generic_focus"]:
                out["generic_focus"].append(r)
        print(f"  {t}: brak dedykowanego drzewa -> generic_focus ({rs})")

dst = os.path.join(REPO, "patches", "focus_inject.json")
with open(dst, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=2, sort_keys=True)
    f.write("\n")
print("wrote", dst, "with", len(out), "trees")
