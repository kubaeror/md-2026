# Changelog

All notable changes to the Millennium Dawn 2026 Rework submod.

---

## v1.0.0 — Initial Release

### Infrastructure (FAZA 0)
- Created `descriptor.mod` with dependency on Millennium Dawn
- Added `replace_path="common/bookmarks"` for bookmark override
- Created 2026 bookmark (`the_gathering_storm.txt`) alongside original 2000 bookmark

### Borders & States (FAZA 1)
- **8 state history files** modified:
  - Crimea → Russian ownership (2014 annexation)
  - Donetsk Oblast → Russian control (2022)
  - Luhansk Oblast → Russian control (2022)
  - Zaporizhzhia Oblast → Partial Russian occupation
  - Kherson Oblast → Partial, western part Ukrainian
  - Syria → Post-Assad HTS control
  - Golan Heights → Israeli control
  - Kosovo → Independent state

### Countries & Leaders (FAZA 2)
- **66 country history files** with `2026.1.1` date blocks
- Updated leaders, ideologies, and political setups for all countries
- 12 major powers + 32 NATO members + 9 conflict zones + 13 regional states

### Conflicts (FAZA 3)
- Active wars configured via startup scripted effects
- Russo-Ukrainian War with front-line unit deployments
- Sudan, Myanmar civil wars
- Yemen division

### Alliances & Factions (FAZA 4)
- NATO (32 members including Finland & Sweden)
- CSTO (without Armenia — frozen membership)
- EU (27 members)
- BRICS+ (10 members after 2024 expansion)
- AUKUS, SCO, Quad, Abraham Accords

### Characters (FAZA 5)
- Leaders defined via `create_country_leader` in country history
- ~66 country leaders with appropriate traits

### Technologies (FAZA 6)
- 5-tier technology system (1258 lines of scripted effects)
- DLC-aware gating for NSB, BBA, Gotterdammerung, La Resistance
- 13 prerequisite chain batches ensuring clean tech tree progression
- Year-based composable effects (2005 → 2010 → 2015 → 2020 → 2025 → advanced)

### National Spirits (FAZA 7)
- 15 base national spirits for major powers
- 22 expansion spirits for additional countries
- 8 focus tree reward spirits
- 11 decision reward ideas

### Focus Trees (FAZA 8)
- **13 shared focus trees**: USA, Russia, Ukraine, China, Germany, India, Japan, Turkey, Brazil, Israel, South Korea, Saudi Arabia, Poland
- Branch gating via `allow_branch` + date check
- 13 copied original MD focus tree files with `shared_focus` references

### Events (FAZA 9)
- **11 event files** with ~75 events total
- Event chains: Elections, NATO-Russia, Russia-Ukraine, Taiwan, Middle East, BRICS, Migration, Climate, Tech Revolution, Space, Demographics
- Cyclical election system with timed flags
- News events for major occurrences

### Decisions (FAZA 10 — part)
- 20 strategic decisions across 5 categories
- Sanctions, NATO, military modernization, geopolitics, economy

### Localisation (FAZA 10)
- 927 English localisation keys
- Covers all events, focuses, spirits, decisions, bookmarks

### Order of Battle (FAZA 11 — part)
- **65 OOB files** with optimized unit templates
- Tiered deployment matching country military capabilities
- Custom templates for infantry, armor, mechanized, special forces, naval, air

---

### Bug Fix Rounds

#### Bug Fix Round 1 (`ee633e6`)
- Removed broken `md2026_setup_alliances` call from on_actions

#### Bug Fix Round 2 (`bda8d47`)
- Fixed state history date blocks (must be inside `history = { }`)
- Corrected invalid triggers (`is_border_state` → `any_neighbor_state`)
- Fixed invalid modifiers (`stability > X` → `has_stability > X`)
- Corrected invalid ideas (`full_draft_army`, `moderate_growth`, `nuclear_power_on`)
- Fixed technology categories to use `CAT_` prefix
- Added missing opinion modifier definitions

#### Bug Fix Round 3 (`c337fae`)
- Renamed opinion modifiers to avoid MD conflicts (`improved_relations` → `md2026_improved_relations`, `border_conflict` → `md2026_border_conflict`)
- Added 3 new context-specific opinion modifiers (`md2026_diplomatic_disapproval`, `md2026_tech_rivalry`, `md2026_migration_tensions`)
- Replaced `embargo` overuse in events with appropriate context-specific modifiers
- Wired up orphan `md2026_demographics_news.1` event (now triggers from aging crisis event)
- Fixed election cycling — changed permanent `set_country_flag` to timed flag (730 days auto-expiry)

#### Tech Prerequisite Batches (13 commits)
- Batch 1: Artillery prerequisite chains
- Batch 2: Anti-tank & anti-air chains
- Batch 3: Infantry chains (weapons, vehicles, NV, C2, drones, armor, camo, support, SF, engineers)
- Batch 4: Engineering chains (AI, computing, encryption, internet, wifi)
- Batch 5: Non-NSB armor chains (MBT, APC, IFV, Rec tank)
- Batch 6: NSB armor chains
- Batch 7: BBA aircraft chains
- Batch 8: Non-BBA fixed-wing chains (fighters, strike, UAV)
- Batch 9: Non-BBA heavy aircraft (bombers, transport, naval, CAS, AWACS)
- Batch 10: Helicopter chains (NSB + non-NSB)
- Batch 11: Missile chains (Gotterdammerung + non-got)
- Batch 12: Naval chains (hulls, weapons, systems, landing craft)
- Batch 13: Industry & space chains (nanotech, 3D printing, biotech, energy, nuclear, construction, rail, agriculture, GNSS, COMSAT, SPYSAT, KILLSAT, OLV)
