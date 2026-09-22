# Millennium Dawn 2026 Rework

A submod for **[Millennium Dawn: A Modern Day Mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2777392649)**
that adds a **January 1, 2026** start date bookmark to Hearts of Iron IV.

* **Hearts of Iron IV 1.19.x**
* **Millennium Dawn 2.0.0** (Workshop ID 2777392649)

> This repository was rebased onto Millennium Dawn 2.0.0 / HoI4 1.19 in September 2026.
> See [docs/Architecture.md](docs/Architecture.md) for how the submod is built and how to
> regenerate it after a Millennium Dawn update.

## Features

- **2026 bookmark** (`2026.1.1`) next to Millennium Dawn's original 2000 start.
- **68 updated countries** with 2026 leaders, parties, national spirits, GDP and politics.
- **Updated borders** - Crimea, Donbas, Zaporizhzhia, Kherson, post-Assad Syria.
- **NATO 2026** - post-2000 members receive Millennium Dawn's `NATO_member` idea and are
  registered in MD's `global.nato_members` array.
- **Focus tree branches**: **32** (`MD2026_*` shared focuses) injected into the current
  MD 2.0 trees; every 2026 bookmark country now has one.
- **67 orders of battle** for 2026, each with a No Step Back **and** a non-No-Step-Back variant.
- **5-tier technology system**, generated from Millennium Dawn's own technology tree
  (all techs up to a year, with MD's DLC gating).
- **Events, decisions, national spirits, opinion modifiers** with the `md2026_` prefix.
- **English and Polish localisation** (1720 keys each).

## Coverage

| | Count |
|---|---|
| Countries with a 2026 history patch | 68 |
| 2026 bookmark entries | 30 |
| Focus branches (`MD2026_*`) | 30 |
| 2026 orders of battle (NSB / non-NSB) | 67 / 67 |
| Pre-completed focuses | 2108 |
| Localisation keys (EN / PL) | 1720 / 1720 |
| Validator | 0 errors |

`python tools/audit_2026.py --write` regenerates the full report in
[docs/Coverage.md](docs/Coverage.md).

## Installation (local / development)

```powershell
pwsh -File tools/install_mod.ps1
```

The script creates a directory junction in your HoI4 mod folder and writes the launcher
descriptor `md-2026.mod`. Then enable **Millennium Dawn** and **Millennium Dawn 2026 Rework**
in the launcher (the submod must load after Millennium Dawn - the `dependencies` field handles it).

## Regenerating after a Millennium Dawn update

Everything that overrides a Millennium Dawn file is generated from the installed MD plus the
hand-maintained 2026 data in `patches/`:

```bash
python tools/rebase.py generate    # bookmark-independent: focus trees, histories, states, tech effects
python tools/validate.py           # checks every reference against MD 2.0
```

If Millennium Dawn renames or removes something the patches reference, `validate.py` reports it
and `patches/mappings/*.csv` holds the rename tables used to fix it.

## Repository layout

```
descriptor.mod / md-2026.mod       launcher metadata
patches/                           hand-maintained 2026 data (never copied from MD)
  history_countries/<TAG>.txt        only the 2026.1.1 block
  history_states/<id>.txt            only the 2026 ownership/core block
  focus_inject.json                  tree id -> MD2026 shared focus roots
  focus_overrides.json               per-focus 2026 reward adaptations
  unsafe_focuses.json                manual pre-completion exclusions
  mappings/*.csv                     MD 1.12 -> MD 2.0 renames (techs, ideas, focuses)
tools/                             rebase generator, validator, audits, install script
common/, history/, events/         mod content (generated parts + md2026_* content)
localisation/english|polish/       localisation (md2026_l_*.yml)
docs/                              architecture, coverage, known issues, testing
```

## Testing

`docs/Testing.md` lists the start-up checks (2026 and 2000, with and without
No Step Back). The short version: run the game, start the 2026 bookmark, play three
days and look at `logs/error.log` - the only expected entries are the MD-side ones
listed in `docs/Known-Issues.md`.

## Known issues

See [docs/Known-Issues.md](docs/Known-Issues.md). The validator currently reports
**0 errors**; a single warning is an issue inside Millennium Dawn's own content.

## License

Fan-made modification for Hearts of Iron IV. All rights to the base game belong to Paradox
Interactive; all rights to Millennium Dawn belong to its authors.
