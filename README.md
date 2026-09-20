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
- **66 updated countries** with 2026 leaders, parties, national spirits, GDP and politics.
- **Updated borders** - Crimea, Donbas, Zaporizhzhia, Kherson, post-Assad Syria.
- **NATO 2026** - post-2000 members receive Millennium Dawn's `NATO_member` idea and are
  registered in MD's `global.nato_members` array.
- **23 focus tree branches** (`MD2026_*` shared focuses) injected into the current MD 2.0 trees.
- **5-tier technology system**, generated from Millennium Dawn's own technology tree
  (all techs up to a year, with MD's DLC gating).
- **Events, decisions, national spirits, opinion modifiers** with the `md2026_` prefix.

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
  mappings/*.csv                     MD 1.12 -> MD 2.0 renames (techs, ideas, focuses)
tools/                             rebase generator, validator, install script
common/, history/, events/, localisation/   mod content (generated parts + md2026_* content)
docs/                              architecture, compatibility, known issues, testing
```

## Known issues

See [docs/Known-Issues.md](docs/Known-Issues.md). The validator currently reports
**0 errors**; a single warning is an issue inside Millennium Dawn's own content.

## License

Fan-made modification for Hearts of Iron IV. All rights to the base game belong to Paradox
Interactive; all rights to Millennium Dawn belong to its authors.
