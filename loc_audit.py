import os, re, glob

base = r"C:\Users\kuba\Documents\md\md\md-2026"

# Step 1: Extract all localization keys from ALL yml files
loc_dir = os.path.join(base, "localisation", "english")
loc_files = glob.glob(os.path.join(loc_dir, "md2026_*l_english.yml"))

loc_keys = set()
for loc_file in loc_files:
    with open(loc_file, "r", encoding="utf-8-sig") as f:
        loc_content = f.read()
    for m in re.finditer(r"^\s+(\S+):0\s", loc_content, re.MULTILINE):
        loc_keys.add(m.group(1))

print(f"Total localization keys found: {len(loc_keys)} (from {len(loc_files)} files)")

# Step 2a: Extract all focus IDs from md2026_*_focus.txt files
focus_files = glob.glob(
    os.path.join(base, "common", "national_focus", "md2026_*_focus.txt")
)
focus_ids = set()
for fp in focus_files:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    for m in re.finditer(r"^\s+id\s*=\s*(MD2026_\S+)", content, re.MULTILINE):
        focus_ids.add(m.group(1))

print(f"Total focus IDs found: {len(focus_ids)}")

# Step 2b: Extract all national spirit / idea IDs from ALL idea files
idea_files = glob.glob(os.path.join(base, "common", "ideas", "md2026_*.txt"))
ns_ids = set()
for ns_file in idea_files:
    with open(ns_file, "r", encoding="utf-8") as f:
        ns_content = f.read()
    for m in re.finditer(r"^\s+(md2026_\w+)\s*=\s*\{", ns_content, re.MULTILINE):
        ns_ids.add(m.group(1))

print(
    f"Total national spirit/idea IDs found: {len(ns_ids)} (from {len(idea_files)} files)"
)

# Step 2c: Extract decision IDs from ALL decision files
dec_files = glob.glob(os.path.join(base, "common", "decisions", "md2026_*.txt"))
dec_ids = set()
for dec_file in dec_files:
    with open(dec_file, "r", encoding="utf-8") as f:
        dec_content = f.read()
    for m in re.finditer(r"^\t(md2026_\w+)\s*=\s*\{", dec_content, re.MULTILINE):
        dec_ids.add(m.group(1))

print(f"Total decision IDs found: {len(dec_ids)} (from {len(dec_files)} files)")

# Step 2d: Decision category IDs
cat_file = os.path.join(
    base, "common", "decisions", "categories", "md2026_decision_categories.txt"
)
with open(cat_file, "r", encoding="utf-8") as f:
    cat_content = f.read()
cat_ids = set()
for m in re.finditer(r"^(md2026_\w+)\s*=\s*\{", cat_content, re.MULTILINE):
    cat_ids.add(m.group(1))

print(f"Total decision category IDs found: {len(cat_ids)}")

# Step 2e: (Merged into step 2b — all idea files scanned together)

# Step 2f: Extract event IDs, explicit title/desc keys, and option keys
event_files = glob.glob(os.path.join(base, "events", "md2026_*.txt"))
event_ids = []
# Track explicit title= and desc= keys per event ID
event_explicit_title = {}  # event_id -> explicit title key
event_explicit_desc = {}  # event_id -> explicit desc key
current_event_id = None
for fp in event_files:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    for m in re.finditer(r"^\s+id\s*=\s*(md2026_\w+\.\d+)", content, re.MULTILINE):
        event_ids.append(m.group(1))
    # Parse explicit title and desc assignments per event
    for line in content.splitlines():
        id_m = re.match(r"\s+id\s*=\s*(md2026_\w+\.\d+)", line)
        if id_m:
            current_event_id = id_m.group(1)
        title_m = re.match(r"\s+title\s*=\s*(md2026_[\w.]+)", line)
        if title_m and current_event_id:
            event_explicit_title[current_event_id] = title_m.group(1)
        desc_m = re.match(r"\s+desc\s*=\s*(md2026_[\w.]+)", line)
        if desc_m and current_event_id:
            event_explicit_desc[current_event_id] = desc_m.group(1)

event_ids = sorted(set(event_ids))
print(f"Total event IDs found: {len(event_ids)}")

# Extract event option keys from event files
event_option_keys = set()
for fp in event_files:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    for m in re.finditer(r"name\s*=\s*(md2026_[\w.]+)", content, re.MULTILINE):
        event_option_keys.add(m.group(1))

print(f"Total event option keys found in code: {len(event_option_keys)}")

# Step 2g: Bookmark entries
bookmark_files = glob.glob(os.path.join(base, "common", "bookmarks", "*.txt"))
bookmark_keys = set()
for fp in bookmark_files:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    for m in re.finditer(r'name\s*=\s*"?(\w*MD[_]?2026\w*)"?', content, re.MULTILINE):
        bookmark_keys.add(m.group(1))
    for m in re.finditer(r'desc\s*=\s*"?(\w*MD[_]?2026\w*)"?', content, re.MULTILINE):
        bookmark_keys.add(m.group(1))

print(f"Total bookmark keys found: {len(bookmark_keys)}")

# ============================================================
# STEP 3: Cross-reference
# ============================================================

needed_keys = set()
missing_keys = []

# Focus IDs need both name and desc
for fid in sorted(focus_ids):
    needed_keys.add(fid)
    needed_keys.add(fid + "_desc")
    if fid not in loc_keys:
        missing_keys.append(("FOCUS NAME", fid))
    if (fid + "_desc") not in loc_keys:
        missing_keys.append(("FOCUS DESC", fid + "_desc"))

# National spirit IDs need both name and desc
for nsid in sorted(ns_ids):
    needed_keys.add(nsid)
    needed_keys.add(nsid + "_desc")
    if nsid not in loc_keys:
        missing_keys.append(("SPIRIT NAME", nsid))
    if (nsid + "_desc") not in loc_keys:
        missing_keys.append(("SPIRIT DESC", nsid + "_desc"))

# Decision IDs need both name and desc
for did in sorted(dec_ids):
    needed_keys.add(did)
    needed_keys.add(did + "_desc")
    if did not in loc_keys:
        missing_keys.append(("DECISION NAME", did))
    if (did + "_desc") not in loc_keys:
        missing_keys.append(("DECISION DESC", did + "_desc"))

# Decision category IDs need both name and desc
for cid in sorted(cat_ids):
    needed_keys.add(cid)
    needed_keys.add(cid + "_desc")
    if cid not in loc_keys:
        missing_keys.append(("DEC CATEGORY NAME", cid))
    if (cid + "_desc") not in loc_keys:
        missing_keys.append(("DEC CATEGORY DESC", cid + "_desc"))

# Event IDs need title and desc keys (use explicit keys if set, else default .t/.d)
for eid in sorted(event_ids):
    t_key = event_explicit_title.get(eid, eid + ".t")
    d_key = event_explicit_desc.get(eid, eid + ".d")
    needed_keys.add(t_key)
    needed_keys.add(d_key)
    if t_key not in loc_keys:
        missing_keys.append(("EVENT TITLE", t_key))
    if d_key not in loc_keys:
        missing_keys.append(("EVENT DESC", d_key))

# Event option keys
for ok in sorted(event_option_keys):
    needed_keys.add(ok)
    if ok not in loc_keys:
        missing_keys.append(("EVENT OPTION", ok))

# Bookmark keys
for bk in sorted(bookmark_keys):
    needed_keys.add(bk)
    if bk not in loc_keys:
        missing_keys.append(("BOOKMARK", bk))

# Tooltip key
needed_keys.add("md2026_ukr_western_aid_tt")
if "md2026_ukr_western_aid_tt" not in loc_keys:
    missing_keys.append(("TOOLTIP", "md2026_ukr_western_aid_tt"))

# ============================================================
# ORPHANED KEYS
# ============================================================
orphaned_keys = sorted(loc_keys - needed_keys)

# ============================================================
# PRINT RESULTS
# ============================================================
print()
print("=" * 70)
print("MISSING LOCALIZATION KEYS (ID in code, not in loc file)")
print("=" * 70)
if missing_keys:
    by_cat = {}
    for cat, key in missing_keys:
        by_cat.setdefault(cat, []).append(key)
    for cat in sorted(by_cat.keys()):
        print(f"\n  --- {cat} ({len(by_cat[cat])}) ---")
        for key in sorted(by_cat[cat]):
            print(f"    {key}")
else:
    print("  NONE - All IDs have localization!")

print()
print("=" * 70)
print("ORPHANED LOCALIZATION KEYS (key in loc file, not referenced in code)")
print("=" * 70)
if orphaned_keys:
    for key in orphaned_keys:
        print(f"  {key}")
else:
    print("  NONE - All loc keys are referenced!")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(
    f"  Focus IDs:              {len(focus_ids)} (need {len(focus_ids) * 2} loc keys)"
)
print(f"  National Spirit/Idea IDs: {len(ns_ids)} (need {len(ns_ids) * 2} loc keys)")
print(f"  Decision IDs:           {len(dec_ids)} (need {len(dec_ids) * 2} loc keys)")
print(f"  Decision Category IDs:  {len(cat_ids)} (need {len(cat_ids) * 2} loc keys)")
print(
    f"  Event IDs:              {len(event_ids)} (need {len(event_ids) * 2} title+desc keys)"
)
print(f"  Event Option Keys:      {len(event_option_keys)}")
print(f"  Bookmark Keys:          {len(bookmark_keys)}")
print(f"  Total needed loc keys:  {len(needed_keys)}")
print(f"  Total defined loc keys: {len(loc_keys)}")
print(f"  Missing loc keys:       {len(missing_keys)}")
print(f"  Orphaned loc keys:      {len(orphaned_keys)}")
