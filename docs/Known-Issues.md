# Known Issues & Troubleshooting

---

## Known Issues

### Leader Portraits (Cosmetic)

Approximately 30 country leaders reference `.dds` portrait files that do not exist in the mod. The game handles this gracefully by displaying a generic placeholder portrait. This is purely cosmetic and does not affect gameplay.

**Affected**: Various Tier B-D countries where custom portraits were not created.

**Workaround**: The game's generic leader portraits are used automatically.

### Polish Translation Not Implemented

The `localisation/polish/` directory was planned but not yet created. All text is in English only.

### GFX Sprite References

Some events reference GFX sprite names (e.g., `GFX_report_event_generic_protests`, `GFX_report_event_generic_industry`) that exist in the vanilla HoI4 base game but may not be explicitly defined in the Millennium Dawn mod. These should work correctly as long as the base game files are intact.

### YML Localisation LSP Errors

If your editor shows YAML errors on `md2026_l_english.yml`, these are **false positives**. HoI4 uses a non-standard YAML format for localisation files that is not compatible with standard YAML parsers. The files work correctly in-game.

---

## Troubleshooting

### Mod doesn't appear in launcher

**Cause**: Missing or incorrect `.mod` file.

**Fix**:
1. Ensure `md-2026.mod` exists in your `mod/` directory (alongside the `md-2026/` folder)
2. Verify the `path=` line points to the correct location
3. Restart the launcher

### 2026 bookmark doesn't appear

**Cause**: Millennium Dawn is not loaded, or load order is wrong.

**Fix**:
1. Ensure Millennium Dawn is enabled in the launcher
2. Ensure both mods are in the same playset
3. The 2026 Rework should load after MD (the `dependencies` declaration handles this)

### Game crashes on startup

**Cause**: Usually a file syntax error or incompatible mod version.

**Fix**:
1. Check `Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log`
2. Look for lines mentioning `md2026` files
3. Verify you're running HoI4 v1.17.x
4. Verify Millennium Dawn is up to date (v1.12.3+)
5. Try disabling all other mods except MD + this submod

### Countries have wrong leaders/settings in 2026

**Cause**: Country history file may not be loading correctly.

**Fix**:
1. In-game, open console with `~` key
2. Type `tdebug` to enable debug mode
3. Hover over the country to see its tag
4. Check that `history/countries/TAG - Name.txt` exists in the submod
5. Verify the `2026.1.1` date block is correctly placed after the `2000.1.1` block

### Technologies not applied

**Cause**: Scripted effect not executing, or prerequisite chain broken.

**Fix**:
1. Check that the country history file calls the correct tier effect:
   - `md2026_tier1_2026_techs = yes` (or tier 2-5)
2. Check `error.log` for technology-related errors
3. In console, use `research all` to verify the tech tree works

### Focus tree 2026 branches not visible

**Cause**: `allow_branch` condition not met, or `shared_focus` reference missing.

**Fix**:
1. Verify you selected the 2026 bookmark (not the 2000 one)
2. Check that the country's original focus tree file has `shared_focus = MD2026_TAG_root`
3. Verify `allow_branch = { original_tag = TAG date > 2025.12.31 }` is correct

### Events not firing

**Cause**: Trigger conditions not met.

**Fix**:
1. Check event trigger conditions (date, country tag, flags)
2. Use console command `event md2026_namespace.number` to force-fire
3. Check if required flags are set/unset
4. Verify `on_actions` file is loading (check `error.log`)

### NATO/alliances not set up correctly

**Cause**: Startup scripted effects not executing.

**Fix**:
1. Check that `common/on_actions/md2026_on_actions.txt` exists
2. Verify `common/scripted_effects/md2026_startup_effects.txt` exists
3. Check `error.log` for scripted effect errors
4. In console, try `set_country_flag md2026_setup_complete` to check if setup ran

### Compatibility issues with other submods

**Cause**: File conflicts with another mod modifying the same MD files.

**Fix**:
1. Identify which files conflict (same filename in both mods)
2. Load this mod after the conflicting mod (or before, depending on which should take priority)
3. For country history files, manual merging may be required
4. See [Compatibility](Compatibility.md) for details on which directories are affected

---

## Reporting Bugs

When reporting issues, please include:
1. HoI4 version number
2. Millennium Dawn version number
3. List of other active mods
4. Contents of `error.log` (relevant lines)
5. Steps to reproduce the issue
6. Screenshot if applicable

File issues at: [https://github.com/kubaeror/md-2026/issues](https://github.com/kubaeror/md-2026/issues)
