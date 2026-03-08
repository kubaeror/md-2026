# Millennium Dawn 2026 Rework

A submod for **[Millennium Dawn: A Modern Day Mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2777392649)** that adds a new **January 1, 2026** start date bookmark to Hearts of Iron IV.

## Overview

This mod updates the world state to reflect geopolitical reality as of January 2026. It introduces a fully playable `2026.1.1` bookmark alongside Millennium Dawn's original `2000.1.1` start date, with updated borders, leaders, conflicts, alliances, technologies, national spirits, focus trees, events, and military orders of battle for approximately 70 countries.

## Features

- **New 2026 Bookmark** with 8 featured nations (USA, Russia, China, Ukraine, Israel, Turkey, Poland, Japan)
- **66 updated countries** with accurate 2026 leaders, ideologies, and political setups
- **Updated borders** reflecting Crimea annexation, Donbas occupation, post-Assad Syria, South Sudan, and Kosovo
- **Active conflicts** — Russo-Ukrainian War, Sudan Civil War, Myanmar Civil War, Yemen division
- **32-member NATO**, CSTO, EU (27), BRICS+, AUKUS, SCO, Abraham Accords, Quad
- **5-tier technology system** with DLC-aware gating (No Step Back, By Blood Alone, Gotterdammerung)
- **23 shared focus trees** — USA, Russia, Ukraine, China, Germany, India, Japan, Turkey, Brazil, Israel, South Korea, Saudi Arabia, Poland + France, UK, Iran, Italy, North Korea, Canada, Australia, Taiwan, Egypt, Syria
- **260 new focus nodes** across 10 expanded country trees (26 focuses each with 5 branches, mutually exclusive paths, and capstone focuses)
- **210 pre-completed focuses** across 23 countries reflecting real-world events already occurred by Jan 2026
- **~75 events** across 11 event chains — elections, NATO-Russia tensions, Taiwan crisis, BRICS expansion, Middle East, migration, climate, tech revolution, space race, demographics
- **45+ national spirits** (15 base + 22 expansion + 8 focus rewards) for major and regional powers
- **20 strategic decisions** across 5 categories (sanctions, NATO, military, geopolitics, economy)
- **65 OOB files** with real-world unit names, ~600 named ships across 40+ navies, 200+ air wings with accurate aircraft types and squadron designations, carrier air wings for 5 carrier nations, and `creator` tags for all imported equipment
- **~1,450 localisation keys** (English)

## Requirements

- Hearts of Iron IV v1.17.x
- [Millennium Dawn: A Modern Day Mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2777392649) (v1.12.3+)

### Recommended DLCs

The mod works without any DLC, but the technology system includes specialized branches for:
- **No Step Back** — tank designer, advanced armor/artillery modules
- **By Blood Alone** — aircraft designer, airframe/module technologies
- **Gotterdammerung** — missile systems (ICBMs, IRBMs, cruise missiles, SAMs)
- **La Resistance** — intelligence agency system

## Installation

### Steam Workshop
*(Coming soon)*

### Manual Installation
1. Download or clone this repository
2. Place the `md-2026` folder in your HoI4 mod directory:
   - Windows: `Documents\Paradox Interactive\Hearts of Iron IV\mod\`
   - Linux: `~/.local/share/Paradox Interactive/Hearts of Iron IV/mod/`
   - macOS: `~/Documents/Paradox Interactive/Hearts of Iron IV/mod/`
3. Create a `md-2026.mod` file in the `mod/` directory with the following content:
   ```
   path="mod/md-2026"
   ```
   Then copy the contents of `descriptor.mod` into this file (after the path line).
4. Enable both **Millennium Dawn** and **Millennium Dawn 2026 Rework** in the launcher
5. Make sure this submod loads **after** the base Millennium Dawn mod

## Countries

### Tier A — Major Powers (full update + focus trees)
USA, Russia, China, UK, France, Germany, India, Japan, Turkey, Iran, Brazil, Ukraine

### Tier B — NATO + Regional (full update, select countries with focus trees)
Poland, Italy, Canada, South Korea, Saudi Arabia, Israel, North Korea, Australia — with focus trees
Spain, Romania, Netherlands, Belgium, Norway, Denmark, Portugal, Czechia, Greece, Hungary, Iceland, Luxembourg, Bulgaria, Croatia, Albania, Lithuania, Latvia, Estonia, Slovakia, Slovenia, Montenegro, North Macedonia, Finland, Sweden

### Tier C — Conflict Zones (partial update, select countries with focus trees)
Taiwan, Egypt, Syria — with focus trees
Myanmar, Sudan, Yemen, UAE, Ethiopia, South Africa

### Tier D — Minimal Update (leader + ideology)
Belarus, Kazakhstan, Kyrgyzstan, Tajikistan, Uzbekistan, Armenia, Georgia, Moldova, Serbia, Bosnia, Kosovo, Pakistan, Afghanistan

## Project Structure

```
md-2026/
├── descriptor.mod
├── common/
│   ├── bookmarks/           # 2026 bookmark + placeholder
│   ├── characters/          # Leader definitions for 66 countries
│   ├── decisions/           # 20 strategic decisions + 5 categories
│   ├── ideas/               # National spirits + decision reward ideas
│   ├── national_focus/      # 23 shared focus trees + 22 base tree copies
│   ├── on_actions/          # Startup event triggers
│   ├── opinion_modifiers/   # Custom opinion modifiers
│   ├── scripted_effects/    # Startup effects + technology tier system
│   └── scripted_triggers/   # Helper triggers
├── events/                  # 11 event files (~75 events)
├── history/
│   ├── countries/           # 66 country history files
│   ├── states/              # 8 updated state files
│   └── units/               # 65 OOB files
└── localisation/
    └── english/             # ~1,450 localisation keys
```

## How It Works

This is a **dependency submod** — it requires the original Millennium Dawn mod and builds on top of it. The technical approach:

- Uses `dependencies` in `descriptor.mod` to require Millennium Dawn
- Uses `replace_path="common/bookmarks"` to override the bookmark file
- Country history files are **full copies** of MD originals with `2026.1.1 = { }` date blocks appended
- Focus trees use the **shared_focus** system — new branches are added to existing trees via `shared_focus = { }` blocks with `allow_branch` gating
- Events, decisions, ideas, and scripted effects use the `md2026_` prefix to avoid conflicts with base MD files
- Technologies use composable year-based scripted effects called at game start via `on_actions`

## Known Issues

- ~30 leader portraits use placeholder images (missing .dds files) — purely cosmetic
- Polish translation not yet implemented
- Some vanilla GFX sprites referenced in events may show as blank if base game files are missing

## License

This project is a fan-made modification for Hearts of Iron IV. All rights to the base game belong to Paradox Interactive. All rights to Millennium Dawn belong to its respective authors.

## Credits

- **Millennium Dawn: A Modern Day Mod** team — for the incredible base mod
- **Paradox Interactive** — for Hearts of Iron IV
