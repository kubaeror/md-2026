# Compatibility

## Mod Compatibility

### Required
- **Millennium Dawn: A Modern Day Mod** (Steam Workshop ID: 2777392649, v1.12.3+)

### Architecture
This submod is designed as a **dependency mod**. It:
- Requires Millennium Dawn as a base
- Overrides specific files from MD where needed
- Adds new files with the `md2026_` prefix to avoid conflicts
- Uses `replace_path="common/bookmarks"` to inject the 2026 bookmark

### Compatibility with Other Submods

This mod **may conflict** with other Millennium Dawn submods that modify:
- `common/bookmarks/` — any mod using `replace_path` for bookmarks
- `common/national_focus/` — 45 files (23 `md2026_*` shared focus definitions + 22 base tree copies); other submods modifying the same base tree files will conflict
- `history/countries/` — files are full copies of MD originals; other submods modifying the same country files will conflict
- `history/states/` — only 8 state files are modified (Crimea, Donbas, Zaporizhzhia, Kherson, Syria, Golan, Kosovo, South Sudan)
- `common/characters/` — full copies of character files for ~66 countries
- `history/units/` — 65 OOB files

This mod **should be compatible** with submods that only add:
- New events (different namespaces)
- New decisions (different filenames)
- New focus trees (different filenames)
- GFX/portrait mods
- Music/sound mods

### Load Order
The mod must load **after** Millennium Dawn. The `dependencies` declaration in `descriptor.mod` should handle this automatically. If you experience issues, manually adjust load order in the launcher.

---

## Game Version Compatibility

| HoI4 Version | Status |
|---------------|--------|
| 1.17.x | Supported |
| 1.16.x | Untested, may work |
| < 1.16 | Not supported |

---

## DLC Compatibility Matrix

The technology system dynamically adapts to installed DLCs:

| DLC | Effect When Present | Effect When Absent |
|-----|--------------------|--------------------|
| **No Step Back** | NSB armor, artillery, AA, helicopter module techs granted | Fallback to non-NSB equivalents via `else` blocks |
| **By Blood Alone** | BBA airframe and module techs granted | Fallback to non-BBA fixed-wing aircraft techs |
| **Gotterdammerung** | Missile system techs (ICBM, IRBM, CM, SAM) granted | Missile techs skipped entirely |
| **La Resistance** | Intelligence agency techs replace encryption/decryption | Standard encryption/decryption techs granted |
| **Arms Against Tyranny** | No specific handling | No impact |
| **Man the Guns** | No specific handling | No impact |

All DLC gating uses `if = { limit = { has_dlc = "DLC Name" } }` with proper `else = { }` fallbacks.
