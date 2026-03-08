# Order of Battle (OOB)

The mod provides 65 Order of Battle files defining the military forces of each country at the start of the 2026 bookmark. OOB files are in `history/units/` and referenced from country history files via `oob = "TAG_2026_nsb"`.

Unlike the base Millennium Dawn mod (which uses separate files per DLC: `_nsb.txt` for ground, `_naval_mtg.txt` for navy, `_bba.txt` for air), this submod uses **single combined files** with ground forces, fleets, and air wings all in one `TAG_2026_nsb.txt` file.

---

## Design Philosophy

### Balanced for Gameplay

OOB files use **custom optimized templates** rather than exact real-world TO&Es. The goal is gameplay balance — every country should be playable and competitive within its tier, while still reflecting relative military power accurately.

### Real Unit Names

All deployed units use **real-world designations**:

- **Ground divisions** carry authentic brigade/division names (e.g. "Iron Wolf Brigada", "1. Panzergrenadierbrigade")
- **Ships** have real hull numbers and vessel names (e.g. "USS Gerald R. Ford (CVN-78)", "HMS Queen Elizabeth (R08)")
- **Air wings** use real squadron/wing names with accurate aircraft types and version names (e.g. "F-35A Lightning II", "Su-30SM Flanker-H")
- **Foreign-origin equipment** uses the `creator` tag to mark the producing country (e.g. Poland's F-16C has `creator = "USA"`, India's Rafale has `creator = "FRA"`)

### Template Approach

Instead of copying Millennium Dawn's default templates (which are designed for the 2000 start), the mod defines modern 2026-era unit templates:

- **Infantry**: Modernized with support companies (artillery, AT, AA, engineers, recon)
- **Mechanized/Motorized**: IFV/APC-equipped mobile divisions
- **Armor**: MBT-focused divisions with mechanized infantry support
- **Special Forces**: Marines, paratroopers, mountain, special operations
- **Naval**: Carrier groups, surface action groups, submarine squadrons
- **Air**: Fighter wings, multirole squadrons, CAS, transport, AWACS, maritime patrol, UAV

---

## OOB Tiers

### Tier 1 — Superpowers (3 countries)

**USA, Russia (SOV), China (CHI)**

Full-spectrum military forces including:
- Multiple army groups with armored, mechanized, and infantry divisions
- Blue-water navy with carrier battle groups and nuclear submarines
- Strategic and tactical air forces with 5th-gen fighters
- Nuclear forces (represented through techs/ideas, not OOB)
- Special operations forces

| Country | Army Divisions | Ships | Air Wings | Carriers |
|---------|---------------|-------|-----------|----------|
| USA | ~30+ | 76 (7 fleets) | 30+ | 5 (CVN) |
| SOV | ~40+ | ~56 (4 fleets) | 22+ | 0 |
| CHI | ~35+ | ~60 (3 fleets) | 16+ | 3 |

### Tier 2a — Major Powers (5 countries)

**Germany (GER), UK (ENG), France (FRA), Japan (JAP), India (RAJ)**

Professional military forces with:
- Corps-level ground forces
- Regional naval capabilities (some blue-water)
- Modern air force with 4th/5th gen aircraft
- Carrier-based aviation where applicable (ENG, FRA, RAJ)

| Country | Ships | Air Wings | Notable Assets |
|---------|-------|-----------|----------------|
| ENG | 36 | 8 | 2x QE-class carriers, F-35B, Typhoon |
| FRA | 33 | 10 | 1x CdG carrier, Rafale M/C/B, FREMM |
| JAP | 44 | 7 | F-35A, F-15J, F-2A, P-1, Izumo-class |
| GER | 24 | 6 | Typhoon, Tornado, F125/F124/F123, U212A |
| RAJ | ~40 | 16 | 2x carriers, Su-30MKI, Rafale, MiG-29K |

### Tier 2b — Regional Military Powers (4 countries)

**Turkey (TUR), Poland (POL), South Korea (KOR), Israel (ISR)**

Strong regional forces with:
- Division-level ground forces with modern equipment
- Coastal/regional navy
- Capable air force

| Country | Ships | Air Wings | Notable Assets |
|---------|-------|-----------|----------------|
| TUR | ~30 | 12 | 240x F-16C, Bayraktar TB2/TB3, Akinci |
| POL | 8 | 6 | F-16C, FA-50, 3. Flotylla |
| KOR | 30 | 9 | F-35A, F-15K, KF-16, Sejong Daewang |
| ISR | 13 | 9 | F-35I, F-16I, F-15I, Sa'ar 6 |

### Tier 3a — Secondary Powers (10 countries)

**Italy (ITA), Saudi Arabia (SAU), Egypt (EGY), Pakistan (PAK), Ukraine (UKR), North Korea (NKO), Iran (PER), Brazil (BRA), Taiwan (TAI), Australia (AST)**

Significant military capabilities:
- Brigade-to-division level forces
- Varying naval capabilities
- Mixed-generation air force

| Country | Ships | Air Wings | Notable Assets |
|---------|-------|-----------|----------------|
| ITA | 20 | 10 | Typhoon, F-35A/B, Cavour carrier |
| SAU | 11 | 11 | F-15SA, Typhoon, Tornado |
| EGY | 16 | 6 | Rafale, F-16C, MiG-29M, FREMM |
| PAK | 13 | 12 | JF-17, F-16, J-10CE, ZDK-03 |
| UKR | 6 | 7 | F-16AM (from NATO), Bayraktar TB2 |
| NKO | 26 | 6 | MiG-29, Su-25, aging Cold War fleet |
| PER | 11 | 10 | F-14A, MiG-29, Su-24MK, Mohajer-6 |
| BRA | 11 | 8 | Gripen, F-5EM, AMX, KC-390 |
| TAI | 25 | 9 | F-16V, Mirage 2000-5EI, F-CK-1 |
| AST | 21 | 8 | F-35A, F/A-18F, EA-18G, Hobart DDG |

### Tier 3b — NATO/Developed (10 countries)

**Canada (CAN), Spain (SPR), South Africa (SAF), Sweden (SWE), Finland (FIN), Greece (GRE), Romania (ROM), Hungary (HUN), Czechia (CZE), Myanmar (BRM)**

Professional but smaller forces focused on territorial defense or NATO commitments.

| Country | Ships | Air Wings | Notable Assets |
|---------|-------|-----------|----------------|
| CAN | 22 | 6 | CF-188, Halifax FFH, Victoria SSK |
| SPR | 18 | 7 | Typhoon, EF-18, F100 frigates |
| SAF | 10 | 3 | Gripen, Valour MEKO frigates |
| SWE | 9 | 6 | Gripen, Visby corvettes, Gotland SSK |
| FIN | 9 | 3 | F/A-18C, Hamina FAC |
| GRE | 15 | 8 | Rafale, F-16V, Hydra MEKO frigates |
| ROM | 6 | 5 | F-16AM, Type 22 frigates |
| HUN | 0 | 2 | Gripen (landlocked) |
| CZE | 0 | 3 | Gripen, L-159 (landlocked) |
| BRM | 7 | 3 | MiG-29, Yak-130 |

### Tier 3c — Conflict Zone Forces (8 countries)

**Syria (SYR), Yemen (YEM), Ethiopia (ETH), Afghanistan (AFG), Sudan (SUD), Belarus (BLR), Georgia (GEO), Armenia (ARM)**

Forces shaped by ongoing or recent conflicts, with:
- War-depleted or irregular formations
- Limited naval/air capabilities
- High manpower but lower equipment quality

| Country | Ships | Air Wings | Notable Assets |
|---------|-------|-----------|----------------|
| BLR | 0 | 5 | Su-30SM, MiG-29BM, Su-25SM |
| GEO | 0 | 2 | Su-25KM Scorpion, Bayraktar TB2 |
| ARM | 0 | 2 | 4x Su-30SM, Su-25 (post-Karabakh) |
| SYR | 2 | 2 | 6x MiG-29, 10x L-39ZA (remnants) |
| YEM | 0 | 1 | 20x Samad-3/Shahed-136 drones |
| ETH | 0 | 3 | Su-27/Su-30, Bayraktar TB2 |
| SUD | 0 | 3 | MiG-29SE, Su-25, Bayraktar TB2 |
| AFG | 0 | 0 | Taliban has no operational air force |

### Tier 3d — Small NATO/Other (25 countries)

**Norway, Denmark, Belgium, Netherlands, Portugal, Bulgaria, Croatia, Albania, Lithuania, Latvia, Estonia, Slovakia, Slovenia, Montenegro, North Macedonia, Iceland, Luxembourg, Serbia, Bosnia, Kosovo, Kazakhstan, Kyrgyzstan, Tajikistan, Uzbekistan, Moldova**

Small professional forces, primarily:
- Brigade-level ground forces
- Limited or no navy
- Small air force or none
- NATO interoperability (where applicable)

| Country | Ships | Air Wings | Notable Assets |
|---------|-------|-----------|----------------|
| HOL | 11 | 4 | F-35A, De Zeven Provincien LCF |
| NOR | 16 | 4 | F-35A, Fridtjof Nansen FFG |
| DEN | 9 | 2 | F-35A, Iver Huitfeldt FFG |
| BEL | 2 | 3 | F-35A, F-16AM, A400M |
| POR | 9 | 3 | F-16AM, Tridente SSK |
| BUL | 4 | 3 | F-16V (new), MiG-29 |
| CRO | 5 | 1 | 12x Rafale (new) |
| SER | 0 | 2 | MiG-29, J-22 Orao |
| SLO | 0 | 2 | 14x F-16V Block 70 (new) |
| UAE | 8 | 5 | F-16E/F, Mirage 2000-9 |
| KAZ | 0 | 5 | Su-30SM, MiG-29, MiG-31BS |
| UZB | 0 | 6 | Su-30SM, MiG-29, Su-25, TB2 |
| LIT | 4 | 1 | C-27J (NATO air policing) |
| LAT | 5 | 0 | MCM only (NATO air policing) |
| EST | 3 | 0 | MCM only (NATO air policing) |
| ALB | 2 | 0 | Patrol vessels only |
| MLV | 0 | 2 | 6x MiG-29, An-26 |
| LUX | 0 | 1 | 1x A400M |
| KYR | 0 | 1 | L-39 trainers |
| TAJ | 0 | 1 | L-39 trainers |

Note: Iceland has no military forces (no OOB file). Slovenia, Kosovo, North Macedonia, Montenegro, and Bosnia have ground forces only (no significant air or naval assets to model).

---

## Naval Forces

### Ship Types

Ships use the Man the Guns (MTG) hull system with real-world class names:

| Hull Type | Real-World Examples |
|-----------|-------------------|
| `carrier_hull_2` | Nimitz, Gerald R. Ford, Queen Elizabeth, Charles de Gaulle, Liaoning, Shandong, Fujian |
| `battle_cruiser_hull_1` | Kirov-class (Pyotr Velikiy, Admiral Nakhimov) |
| `cruiser_hull_2` | Ticonderoga CG, Slava-class |
| `destroyer_hull_3` | Arleigh Burke DDG, Daring T45, Horizon, Kolkata, Sejong Daewang |
| `destroyer_hull_2` | Udaloy, Sovremennyy |
| `frigate_hull_3` | FREMM, F125, Mogami, Type 054A |
| `frigate_hull_2` | Oliver Hazard Perry, Halifax, Anzac, Fridtjof Nansen |
| `corvette_hull_2` | Visby, Buyan-M, Baynunah, Skjold |
| `corvette_hull_1` | Patrol vessels, mine countermeasures, small combatants |
| `helicopter_operator_hull_2` | Mistral LHD, Juan Carlos I, Dokdo |
| `attack_submarine_hull_3` | Virginia SSN, Astute SSN, Suffren SSN |
| `attack_submarine_hull_2` | Los Angeles SSN, Akula SSN, Trafalgar SSN |
| `attack_submarine_hull_1` | Kilo SSK, Gotland SSK, Soryu SSK, Type 039A |
| `missile_submarine_hull_3` | Ohio SSBN, Columbia SSBN, Vanguard SSBN |
| `missile_submarine_hull_2` | Borei SSBN, Triomphant SSBN |

### Fleet Organization

Navies are organized into fleets with task forces reflecting real-world fleet structures:

- **USA:** 7 fleets (2nd, 3rd, 4th, 5th, 6th, 7th Fleet + Pacific Submarine Force), 76 ships total
- **Russia:** 4 fleets (Northern, Baltic, Black Sea, Pacific), ~56 ships total
- **China:** 3 fleets (Northern, Eastern, Southern Theater Navy), ~60 ships total with 3 carriers
- Smaller navies use 1-2 fleets as appropriate

### Carrier Air Wings

Carrier-based air wings use the carrier's name string as the "state ID":

```
"USS Gerald R. Ford (CVN-78)" = {
    cv_small_plane_strike_airframe_2 = { owner = "USA" amount = 44 version_name = "F-35C Lightning II" }
    name = "Carrier Air Wing 8 (CVW-8)"
    start_experience_factor = 0.7
}
```

---

## Air Forces

### Aircraft Types (By Blood Alone Airframes)

| Airframe | Role | Examples |
|----------|------|---------|
| `small_plane_airframe_2` | Light fighter | MiG-29, JF-17 |
| `small_plane_strike_airframe_2` | Multirole strike | F-35A/B/C, F-16C/V, Gripen, FA-50 |
| `medium_plane_fighter_airframe_2` | Air superiority | F-22A, Su-35S, F-15J, Typhoon, J-20A |
| `medium_plane_airframe_2` | Heavy multirole | Rafale, F-15E/I/K/SA, Su-30SM/MKI, F/A-18F |
| `small_plane_cas_airframe_2` | Close air support | Su-25, A-1M AMX |
| `medium_plane_cas_airframe_1` | Strike/interdiction | Su-24M, Mirage 2000D, Tornado IDS |
| `medium_plane_cas_airframe_2` | Heavy CAS/strike | Su-34, A-10C |
| `large_plane_airframe_2/3` | Strategic bomber | Tu-160, Tu-95MS, B-2, B-52H, H-6K/N |
| `large_plane_air_transport_airframe_1` | Tactical transport | C-130H/J, C-27J, An-26, C-295M |
| `large_plane_air_transport_airframe_2` | Strategic transport | C-17, A400M, C-2, KC-390, Il-76 |
| `large_plane_awacs_airframe_2` | AWACS | E-3, E-7, E-767, A-50U, KJ-500 |
| `large_plane_awacs_airframe_1` | AEW/recon | E-2C/D, RC-135, G550 CAEW, E-99M |
| `large_plane_maritime_patrol_airframe_1` | MPA/ASW | P-8A, P-1, P-3C, Atlantique 2 |
| `small_plane_suicide_airframe_2` | UCAV/drone | MQ-9A, Bayraktar TB2/TB3, Hermes 900, Heron TP, Akinci, Wing Loong II |
| `cv_small_plane_strike_airframe_2` | Carrier strike | F-35B/C |
| `cv_medium_plane_fighter_airframe_2` | Carrier fighter | Rafale M, J-15 |
| `cv_medium_plane_scout_airframe_2` | Carrier AEW | E-2C/D |

### Foreign Equipment

Countries that purchased (not produced) aircraft use `creator = "TAG"` to mark the manufacturer:

```
small_plane_strike_airframe_2 = { owner = "POL" creator = "USA" amount = 48 version_name = "F-16C Block 52+" }
```

This applies to all imported equipment — e.g. Poland's F-16C (creator=USA), Greece's Rafale (creator=FRA), India's Su-30MKI (creator=SOV).

---

## OOB File Structure

Each combined OOB file follows this structure:

```
##### Country - 2026 OOB #####

division_template = { ... }          # Template definitions

units = {
    division = { ... }               # Ground force deployments

    fleet = {                        # Fleet blocks INSIDE units = { }
        name = "Fleet Name"
        naval_base = PROVINCE_ID
        task_force = {
            name = "Task Force Name"
            location = PROVINCE_ID
            ship = { name = "Ship Name (HULL-XX)" definition = type
                     equipment = { hull_type = { amount = 1 owner = TAG
                     version_name = "Class Name" } } }
        }
    }
}

instant_effect = {                   # Starting equipment stockpile
    add_equipment_to_stockpile = { ... }
}

air_wings = {                        # Air wings AFTER instant_effect, at top level
    STATE_ID = {
        airframe_type = { owner = "TAG" creator = "TAG" amount = XX
                          version_name = "Aircraft Name" }
        name = "Wing/Squadron Name"
        start_experience_factor = 0.5
    }
}
```

---

## Special Considerations

### Ukraine
Ukraine's OOB reflects wartime mobilization with large infantry forces, Western-supplied equipment (F-16AM with `creator = "USA"`), and depleted armor/air forces consistent with the ongoing conflict.

### Russia
Russia's OOB reflects partial mobilization with large ground forces but equipment losses from the Ukraine war, partially offset by wartime production bonuses. The fleet reflects post-Moskva losses in the Black Sea.

### North Korea
Large ground forces (reflecting one of the world's largest armies by personnel) with 26 ships and 6 air wings, but outdated equipment. Two fleets (East Sea and West Sea) with aging Romeo/Sang-O submarines and Najin frigates.

### Syria
Post-civil-war forces under new HTS government — minimal remnant forces with just 2 ships and a handful of operational MiG-29s and L-39 trainers.

### Iran (PER)
Two separate fleets (Southern Fleet at Bandar Abbas and Caspian Flotilla at Bandar-e Anzali). Air force uses aging F-14A Tomcats, MiG-29s, and F-4E Phantoms — no modern imports due to sanctions.

### Baltic States (LIT, LAT, EST)
No combat aircraft of their own — rely on NATO Baltic Air Policing. Small mine countermeasures / patrol vessel navies. Lithuania has 3x C-27J Spartan transports as its only air asset.

### Carrier Nations
Five countries operate carriers with dedicated carrier air wings:
- **USA** — 5x CVN with F-35C and F/A-18E/F
- **UK** — 2x QE-class with F-35B
- **France** — 1x Charles de Gaulle with Rafale M
- **China** — 3x carriers (Liaoning, Shandong, Fujian) with J-15
- **India** — 2x carriers (Vikramaditya, Vikrant) with MiG-29K
