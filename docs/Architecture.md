# Architecture & Mod Structure

Technical documentation of how the Millennium Dawn 2026 Rework submod is built and how it interacts with the base Millennium Dawn mod.

---

## Dependency Architecture

This mod is a **dependency submod** — it cannot run standalone and requires Millennium Dawn as its base. This is declared in `descriptor.mod`:

```
dependencies={
    "Millennium Dawn: A Modern Day Mod"
}
```

The HoI4 launcher enforces load order: MD loads first, then this submod overrides specific files.

---

## File Override Strategy

HoI4 has two mechanisms for mod file interaction:

### 1. `replace_path` — Full Directory Replacement

When a mod declares `replace_path="some/directory"`, it tells the engine to **ignore all other mods' files** in that directory and only use this mod's files.

**MD's replace_path entries** (72 total) include:
- `common/scripted_effects`, `common/scripted_triggers`
- `common/ideas`, `common/decisions`, `common/decisions/categories`
- `common/national_focus`, `common/characters`, `common/technologies`
- `history/countries`, `history/states`, `history/units`
- `events`
- And many more...

**Our submod's replace_path:**
- `common/bookmarks` — to override the bookmark file (MD does NOT use replace_path for bookmarks)

### 2. Same-Name Override

For directories covered by MD's `replace_path`, our submod must provide **complete copies** of any files we want to modify. A file with the same name and path as an MD file will override it.

### 3. New Files (Additive)

For directories covered by MD's `replace_path`, new files with unique names are **added alongside** MD's files. We use the `md2026_` prefix for all new files.

---

## File Categories

### Full Copies (override MD files)

These files are complete copies of MD originals with our `2026.1.1` blocks appended:

| Directory | Files | Purpose |
|-----------|-------|---------|
| `history/countries/` | 66 files | Country history with 2026 date blocks |
| `history/states/` | 8 files | State ownership changes |
| `common/characters/` | 66 files | Leader definitions |
| `common/national_focus/` | 22 files | Original trees + `shared_focus` refs |

### New Files (additive, md2026_ prefix)

| Directory | Files | Purpose |
|-----------|-------|---------|
| `common/national_focus/` | 23 `md2026_*` files | Shared focus definitions |
| `common/scripted_effects/` | 2 files | Startup + technology effects |
| `common/ideas/` | 2 files | National spirits + decision ideas |
| `common/decisions/` | 1 file | Strategic decisions |
| `common/decisions/categories/` | 1 file | Decision categories |
| `common/on_actions/` | 1 file | Startup triggers |
| `common/opinion_modifiers/` | 1 file | Custom opinion modifiers |
| `common/scripted_triggers/` | 1 file | Helper triggers |
| `events/` | 11 files | Event chains |
| `history/units/` | 65 files | 2026 OOB files |
| `localisation/english/` | 1 file | All text strings |

### Bookmarks (replace_path)

| Directory | Files | Purpose |
|-----------|-------|---------|
| `common/bookmarks/` | 2 files | Both bookmarks (2000 + 2026) |

Since we use `replace_path` for bookmarks, we must include the original MD bookmark (`blitzkrieg.txt`) alongside our new one (`the_gathering_storm.txt`).

---

## Startup Flow

When a game starts with the 2026 bookmark:

```
Game Start (2026.1.1)
├── 1. Country history files apply 2026.1.1 date blocks
│   ├── Set politics (leader, ideology, popularities)
│   ├── Set OOB reference (TAG_2026)
│   ├── Add national spirits
│   └── Set technologies (via scripted effect call)
├── 2. State history files apply 2026.1.1 date blocks
│   └── Change ownership, add cores
├── 3. on_actions fires md2026_on_startup
│   ├── Check date > 2025.12.31
│   ├── Call md2026_setup_factions (NATO, CSTO, EU, BRICS, etc.)
│   ├── Call md2026_setup_wars (declare ongoing wars)
│   └── Call md2026_setup_diplomacy (opinion modifiers)
├── 4. OOB files deploy units
│   └── Divisions, fleets, air wings placed
└── 5. Focus trees show 2026 branches
    └── allow_branch checks date > 2025.12.31
```

---

## Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Scripted effects | `md2026_effect_name` | `md2026_setup_factions` |
| Scripted triggers | `md2026_trigger_name` | `md2026_is_nato_member` |
| Ideas/spirits | `md2026_spirit_name` | `md2026_western_sanctions` |
| Events | `md2026_namespace.number` | `md2026_elections.1` |
| Decisions | `md2026_decision_name` | `md2026_impose_sanctions` |
| Decision categories | `md2026_category_name` | `md2026_sanctions_decisions` |
| Focus IDs | `MD2026_TAG_focus_name` | `MD2026_USA_trump_agenda` |
| Opinion modifiers | `md2026_modifier_name` | `md2026_improved_relations` |
| Country flags | `md2026_flag_name` | `md2026_election_held` |
| Global flags | `md2026_flag_name` | `md2026_asat_incident` |
| OOB files | `TAG_2026` | `USA_2026` |
| Localisation keys | `md2026_key_name` | `md2026_elections.1.t` |

---

## Technology System Architecture

Technologies use a composable effect system:

```
md2026_tier1_2026_techs
├── md2026_techs_prereqs      (glue techs for all tiers)
├── md2026_techs_2005          (2001-2005 techs)
├── md2026_techs_2010          (2006-2010 techs)
├── md2026_techs_2015          (2011-2015 techs)
├── md2026_techs_2020          (2016-2020 techs)
├── md2026_techs_2025          (2021-2025 techs)
└── md2026_techs_2025_advanced (cutting-edge techs)
```

Each year effect contains `if/else` blocks for DLC gating:
```
if = { limit = { has_dlc = "No Step Back" } }
    # NSB techs
else = {
    # Non-NSB fallback
}
```

---

## Key Technical Constraints

### HoI4 Clausewitz Engine Quirks

1. **`else` syntax**: Goes INSIDE the `if` block, before its closing `}`
2. **State date blocks**: Must be inside `history = { }`, not after it
3. **YML format**: UTF-8 with BOM, non-standard YAML (LSP errors are false positives)
4. **Localisation**: Leading space, `:0` version suffix: ` KEY:0 "Value"`
5. **`set_country_flag` timed**: `set_country_flag = { flag = name days = X value = 1 }`

### MD-Specific Constraints

1. **No `full_draft_army`** — Use `drafted_women` for maximum conscription
2. **No `moderate_growth`** — Economic cycle: boom/fast_growth/stable_growth/stagnation/recession/depression
3. **No `nuclear_power_on`** — Use `nuclear_energy`/`nuclear_power_def`/`nuclear_power_off`
4. **No `is_border_state`** trigger — Use `any_neighbor_state` workaround
5. **No `stability > X`** — Use `has_stability > X`
6. **Technology tags use `CAT_` prefix** — e.g., `CAT_armor`, `CAT_fighter`, `CAT_missile`
7. **Modifier `Military_Spending_cost_factor`** is valid (651+ uses in MD)
