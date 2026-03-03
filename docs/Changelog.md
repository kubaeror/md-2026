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
- **23 shared focus trees**: USA, Russia, Ukraine, China, Germany, India, Japan, Turkey, Brazil, Israel, South Korea, Saudi Arabia, Poland + France, UK, Iran, Italy, North Korea, Canada, Australia, Taiwan, Egypt, Syria
- **10 expanded trees** (FRA, ENG, PER, ITA, NKO, CAN, AST, TAI, EGY, SYR) with 26 focuses each — 5 branches, mutually exclusive paths, capstone focuses
- **260 new focus nodes** across the 10 expanded trees
- **9 base mod focus tree files** copied (france, uk, iran, italy, korea_north, canada, egypt, syria, generic) with `shared_focus` references
- **210 pre-completed focuses** across all 23 countries (root + T1 + non-ME T2 focuses auto-completed in history files)
- Branch gating via `allow_branch` + date check
- 22 total copied original MD focus tree files with `shared_focus` references

### Events (FAZA 9)
- **11 event files** with ~75 events total
- Event chains: Elections, NATO-Russia, Russia-Ukraine, Taiwan, Middle East, BRICS, Migration, Climate, Tech Revolution, Space, Demographics
- Cyclical election system with timed flags
- News events for major occurrences

### Decisions (FAZA 10 — part)
- 20 strategic decisions across 5 categories
- Sanctions, NATO, military modernization, geopolitics, economy

### Localisation (FAZA 10)
- ~1,450 English localisation keys
- Covers all events, focuses (including 10 expanded trees), spirits, decisions, bookmarks

### Order of Battle (FAZA 11 — part)
- **65 OOB files** with optimized unit templates
- Tiered deployment matching country military capabilities
- Custom templates for infantry, armor, mechanized, special forces, naval, air

### OOB Expansion — Fleets, Air Wings & Real Unit Names (30 commits on `dev`)

Complete overhaul of all 65 OOB files to add real-world military detail:

**Template cleanup:**
- Removed "2026" suffix from all division template names across 23 countries (e.g. `"Armored Brigade 2026"` -> `"Armored Brigade"`)

**Naval forces added (fleets with real ship names and hull numbers):**
- **Tier 1:** USA (76 ships / 7 fleets), Russia (56 ships / 4 fleets), China (60 ships / 3 fleets, 3 carriers)
- **Tier 2a:** UK (36 ships, 2 carriers), France (33 ships, 1 carrier), Japan (44 ships), Germany (24 ships), India (40 ships, 2 carriers)
- **Tier 2b:** Turkey (~30 ships), Poland (8 ships), South Korea (30 ships), Israel (13 ships)
- **Tier 3a:** Italy (20), SAU (11), EGY (16), PAK (13), UKR (6), NKO (26), PER (11, 2 fleets), BRA (11), TAI (25), AST (21)
- **Tier 3b:** CAN (22), SPR (18), SAF (10), SWE (9), FIN (9), GRE (15), ROM (6), BRM (7)
- **Tier 3c-d:** SYR (2), HOL (11), NOR (16), DEN (9), BEL (2), POR (9), BUL (4), CRO (5), UAE (8), LIT (4), LAT (5), EST (3), ALB (2)

**Air wings added (real squadron names, accurate aircraft types, correct creator tags):**
- 5th-gen fighters: F-35A/B/C (USA, ENG, ITA, NOR, DEN, BEL, HOL, AST, JAP, KOR, ISR), F-22A (USA), J-20A (CHI)
- 4th-gen fighters: Typhoon, Rafale, F-15, F-16, Su-30/35, MiG-29, Gripen, FA-50, JF-17, J-10CE, F-CK-1
- CAS/Strike: Su-25, Su-24, A-10C, Tornado IDS, Mirage 2000D, AMX, Su-34
- AWACS/AEW: E-3, E-7, E-767, E-2C/D, A-50U, KJ-500, G550 CAEW, E-99M, GlobalEye
- MPA: P-8A, P-1, P-3C, Atlantique 2
- Transport: C-17, C-130H/J, A400M, KC-390, C-2, C-27J, C-295M, Il-76
- Drones/UCAV: MQ-9A, Bayraktar TB2/TB3, Akinci, Heron TP, Hermes 900, Wing Loong II, Mohajer-6, Samad-3/Shahed-136
- Carrier air wings: USA (5x CVN), UK (2x QE), France (CdG), China (3x), India (2x)

**Countries with no air/naval additions (ground forces only):**
- Afghanistan (Taliban — no air force), Bosnia, Kosovo, Slovenia, Montenegro, North Macedonia — no significant air or naval assets to model

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
