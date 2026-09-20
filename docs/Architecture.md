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
| `common/national_focus/<md file>` | MD file + `shared_focus = MD2026_*` lines | `rebase.py focus` |
| `history/countries/<md file>` | MD file + `patches/history_countries/<TAG>.txt` | `rebase.py history` |
| `history/states/<md file>` | MD file + `patches/history_states/<id>.txt` (inside `history = {}`) | `rebase.py history` |
| `common/scripted_effects/md2026_technology_effects.txt` | MD's technology tree (`start_year` + `allow_branch` DLC gating) | `rebase.py tech` |
| `thumbnail.png` | - | `tools/make_thumbnail.py` |

`python tools/rebase.py generate` runs all three steps. `tools/rebase.py extract` is a one-time
helper that split the original full copies into patches (kept for reference).

## Fixups

While generating, `rebase.py` repairs known Millennium Dawn 2.0 bugs inside the files it copies:

- technology/character references with wrong case (`early_APC` → `Early_APC`,
  `UKR_dmytro_kiva` → `UKR_Dmytro_Kiva`),
- references to ids that no longer exist in MD 2.0 (commented out with a `MD2026:` note),
- `original_tag = NOR` leftovers (MD renamed Norway's tag to `NRY`),
- `CAT_computing_tech` → `CAT_computer_systems`, short doctrine categories → `CAT_*_doctrine`.

The fixes are applied to *our* copies only and disappear automatically once MD fixes them.

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
