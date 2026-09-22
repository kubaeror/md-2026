# Architecture

The submod is a **dependency submod**: it requires Millennium Dawn and builds on top of it.
Since HoI4 has no "append to another mod's file" mechanism, files that need to *extend* MD
content have to be overridden by a full copy. To keep those copies from going stale (which is
what broke the previous MD 1.12-era version), **every overriding file is generated** from the
currently installed Millennium Dawn plus small, hand-maintained patches.

## Data flow

```
Millennium Dawn 2.0 (workshop)          patches/ (this repo)              common/, history/ (generated)
┌───────────────────────────┐    ┌──────────────────────────────┐    ┌──────────────────────────────┐
│ common/national_focus/05_* │──▶ │ patches/focus_inject.json    │──▶ │ common/national_focus/05_*   │
│ history/countries/*.txt    │──▶ │ patches/history_countries/*  │──▶ │ history/countries/*.txt      │
│ history/states/*.txt       │──▶ │ patches/history_states/*     │──▶ │ history/states/*.txt         │
│ common/technologies/*      │──▶ │ (generated directly)         │──▶ │ common/scripted_effects/...  │
└───────────────────────────┘    └──────────────────────────────┘    └──────────────────────────────┘
```

Files that do **not** override MD (`common/bookmarks/md2026_bookmark.txt`,
`common/ideas/md2026_*`, `common/decisions/md2026_*`, `common/on_actions/md2026_*`,
`events/md2026_*`, `localisation/english/md2026_l_english.yml`, `history/units/*_2026_*.txt`)
are written by hand and use the `md2026_` prefix to avoid collisions.

## Generated artifacts

| Artifact | Source | Tool |
|---|---|---|
| `common/national_focus/<md file>` | MD file + `shared_focus = MD2026_*` lines + `patches/focus_overrides.json` | `rebase.py focus` |
| `history/countries/<md file>` | MD file + `patches/history_countries/<TAG>.txt` | `rebase.py history` |
| `history/states/<md file>` | MD file + `patches/history_states/<id>.txt` (inside `history = {}`) | `rebase.py history` |
| `history/units/<TAG>_2026_nonnsb.txt` | `<TAG>_2026_nsb.txt` (DLC-neutral 2026 OOB) | `tools/make_nonnsb_oob.py` |
| `common/units/MD_regimental_support.txt` | MD file + `support` added to the hidden `Light_*` sub-units | `rebase.py units` |
| `common/scripted_effects/md2026_technology_effects.txt` | MD's technology tree (`start_year` + `allow_branch` DLC gating) | `rebase.py tech` |
| `thumbnail.png` | - | `tools/make_thumbnail.py` |

`python tools/rebase.py generate` runs all steps. `tools/rebase.py extract` is a one-time
helper that split the original full copies into patches (kept for reference).

## Focus overrides

`patches/focus_overrides.json` adapts single Millennium Dawn focuses for 2026:

* `"allow": true` keeps MD's reward but lets the 2026 history pre-complete the
  focus (for rewards that are verified to be correct in 2026),
* `"reward": "..."` replaces the whole `completion_reward` body (for rewards
  that touch 2000-era leaders, parties or events).

The generator applies the override to our copy of the focus file before the
pre-completion safety filter runs, so an overridden focus is no longer skipped.
Focuses that are skipped on purpose are listed in `docs/Known-Issues.md`.

## Fixups

While generating, `rebase.py` repairs known Millennium Dawn 2.0 bugs inside the files it copies:

- technology/character references with wrong case (`early_APC` → `Early_APC`,
  `UKR_dmytro_kiva` → `UKR_Dmytro_Kiva`),
- references to ids that no longer exist in MD 2.0 (commented out with a `MD2026:` note),
- `original_tag = NOR` leftovers (MD renamed Norway's tag to `NRY`),
- `CAT_computing_tech` → `CAT_computer_systems`, short doctrine categories → `CAT_*_doctrine`,
- ideologies written with the wrong case (`Democratic`, `Nat_populism`,
  `has_government = Democratic`) - the game is case sensitive, so those rewards
  silently did nothing.

The fixes are applied to *our* copies only and disappear automatically once MD fixes them.

## Validation and audits

| Tool | Purpose |
|---|---|
| `tools/validate.py` | reference/consistency checker (technologies, ideas, focuses, characters, OOB equipment and sub-units, tags, ideologies, events, sprites, loc keys, duplicates, phantom platforms); the goal is 0 errors |
| `tools/audit_2026.py` | coverage report -> `docs/Coverage.md` (patch/branch/OOB/loc coverage) |
| `tools/audit_deep.py` | deep static audit (file integrity, OOB structure/basing, history, focus, events, loc, bookmark, cross-mod arrays, generator reproducibility); findings feed `docs/Audit-2026.md` |
| `tools/oob_digest.py` | per-country OOB fact sheet (divisions, fleets, air wings, stockpiles) for review and audits |
| `tools/oob_lookup.py` | province/state/equipment lookup for OOB editing (state owner, air/naval base, provinces) |
| `tools/oob_check.py` | fast structural check of the 2026 OOBs (basing, naval/air bases, equipment, templates, ship names) |
| `tools/oob_diff_summary.py` | before/after diff of the OOBs (HEAD vs working tree) used to review the audit fixes |
| `tools/loc_keys.py` | localisation key extraction, missing/unused/translation report |
| `tools/check_leaders.py` | leader data in `patches/leaders_2026.json` vs generated histories |
| `tools/economy_report.py` | GDP/debt table for review -> `docs/Economy-2026.md` (includes a debt/treasury sanity check) |
| `tools/make_nonnsb_oob.py` | non-NSB OOB variants |
| `tools/fix_oob_equipment.py` | equipment name mapping for the OOB files |
| `tools/fix_oob_tiers.py` | air wing generation tiers |
| `tools/check_pl_part.py` / `assemble_pl.py` | Polish translation parts |

`patches/phantom_platforms.json` lists ships, aircraft and formations that did
not exist on 1 January 2026; `validate.py` fails when one reappears in a 2026
OOB. `tools/foreign_basing.json` holds the intentional foreign-basing pairs used
by the OOB checks.

## Focus branches

2026 focus branches are `shared_focus` definitions in `common/national_focus/md2026_*_focus.txt`.
The root of each branch is injected into the corresponding MD 2.0 tree by `rebase.py`, driven by
`patches/focus_inject.json` (tree id → root focus ids). The branch nodes themselves use
`relative_position_id`/`prerequisite`, so only the root needs to be listed in the tree.

`allow_branch = { original_tag = TAG date > 2025.12.31 }` keeps the branches hidden in the 2000 start.

## Technology tiers

`md2026_tierN_2026_techs` grants every MD technology up to a year:

| Tier | Countries | Tech level |
|---|---|---|
| 1 | USA, SOV, CHI | up to 2026 |
| 2 | major powers | up to 2025 |
| 3 | modern mid-tier | up to 2020 |
| 4 | regional | up to 2015 |
| 5 | basic | up to 2010 |

The lists are generated from MD's `start_year` fields, so they follow MD's tech tree automatically.
DLC-gated branches are mirrored with `if = { limit = { has_dlc = "..." } }`.

## Validation

`tools/validate.py` checks, against the installed MD:

- technologies, ideas, focuses, characters, tags, ideologies, events, scripted effects,
  decision/technology categories, GFX sprites, OOB province ids, localisation keys
  (existence and duplicates),
- duplicate focus ids between our files and MD's (files that do not override an MD file by name),
- references that live exclusively in files we override are reported as `MD-side reference`
  (MD's own bug, harmless for us).

Run it before every commit; the goal is 0 errors.
