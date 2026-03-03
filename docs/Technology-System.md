# Technology System

The mod implements a comprehensive 5-tier technology system that grants countries appropriate 2026-era technologies at game start. The system is DLC-aware, with separate branches for No Step Back, By Blood Alone, Gotterdammerung, and La Resistance content.

---

## Architecture

Technologies are assigned via composable scripted effects in `common/scripted_effects/md2026_technology_effects.txt` (1258 lines).

### Year-Based Effects

Individual year effects grant technologies available up to that year:

| Effect | Technologies Covered |
|--------|---------------------|
| `md2026_techs_prereqs` | "Glue" prerequisite techs needed to unlock later tiers |
| `md2026_techs_2005` | Technologies through 2005 |
| `md2026_techs_2010` | Technologies through 2010 |
| `md2026_techs_2015` | Technologies through 2015 |
| `md2026_techs_2020` | Technologies through 2020 |
| `md2026_techs_2025` | Technologies through 2025 |
| `md2026_techs_2025_advanced` | Cutting-edge 2025 technologies |

### Tier Composition Effects

Each tier calls a specific combination of year effects:

| Tier Effect | Years Included | Description |
|-------------|---------------|-------------|
| `md2026_tier1_2026_techs` | All through 2025 + advanced | Superpowers with cutting-edge tech |
| `md2026_tier2_2026_techs` | All through 2025 | Major powers, full modern tech |
| `md2026_tier3_2026_techs` | All through 2020 | Developed nations |
| `md2026_tier4_2026_techs` | All through 2015 | Developing nations |
| `md2026_tier5_2026_techs` | All through 2010 | Basic modernization |

---

## Country Tier Assignments

### Tier 1 — Superpowers
USA, SOV (Russia), CHI (China)

*All technologies through 2025 + cutting-edge systems*

### Tier 2 — Major Powers
ENG (UK), FRA (France), GER (Germany), JAP (Japan), KOR (South Korea), ISR (Israel), ITA (Italy), RAJ (India), AST (Australia), TUR (Turkey), CAN (Canada)

*All technologies through 2025*

### Tier 3 — Developed Nations
POL, SPR, HOL, NOR, SWE, FIN, UKR, GRE, DEN, BEL, TAI, SAU, UAE, PAK, BRA, SAF, POR, EGY

*All technologies through 2020*

### Tier 4 — Developing Nations
ROM, NKO, PER, CZE, HUN, SER, BUL, CRO, BRM, KAZ, BLR, GEO, ARM, EST, LAT, LIT, SLO

*All technologies through 2015*

### Tier 5 — Basic Modernization
AFG, ALB, BOS, ETH, FYR, ICE, KOS, KYR, LUX, MLV, MNT, SLV, SUD, SYR, TAJ, UZB, YEM

*All technologies through 2010*

---

## Technology Categories

### Infantry & Small Arms
- Infantry weapons (infantry_weapons1 through infantry_weapons5)
- Motorized/mechanized infantry
- Night vision, C2 systems, body armor, camouflage
- Special forces, combat engineers
- Drones and UAS

### Armor (Non-NSB)
- Main Battle Tanks (MBT_1 through MBT_7)
- APCs, IFVs, Reconnaissance vehicles

### Armor (No Step Back DLC)
- Advanced tank chassis and modules
- ERA, APS, composite armor
- Modern FCS and stabilization

### Artillery
- Towed and self-propelled artillery
- MLRS systems
- Modern precision munitions

### Anti-Air
- Light and heavy AA systems
- Self-propelled AA
- Modern SHORAD/VSHORAD

### Aircraft (Non-BBA)
- Fighters, strike aircraft, CAS
- Bombers (tactical and strategic)
- Transport, naval aviation, AWACS
- UAVs

### Aircraft (By Blood Alone DLC)
- Airframes and modules
- Advanced avionics, stealth
- Precision guided munitions

### Helicopters
- Attack, transport, and utility helicopters
- Modern sensor and weapon systems

### Missiles (Gotterdammerung DLC)
- ICBMs, IRBMs
- Cruise missiles
- Surface-to-air missiles (SAM)

### Naval
- Surface combatants (destroyers through carriers)
- Submarines (conventional and nuclear)
- Naval weapons and sensor systems
- Landing craft

### Industry & Space
- Computing, AI, cybersecurity
- Nanotech, 3D printing, biotech
- Energy (solar, wind, fusion research)
- Nuclear power
- Space systems (GNSS, COMSAT, SPYSAT, KILLSAT, OLV)
- Construction, rail, agriculture

---

## DLC Gating

All DLC-specific technologies are wrapped in conditional blocks:

```
if = {
    limit = { has_dlc = "No Step Back" }
    # NSB-specific techs
}
else = {
    # Non-NSB fallback techs
}
```

This ensures:
- Players **with** the DLC get the full modern equipment
- Players **without** the DLC get equivalent non-DLC technologies
- No errors are generated regardless of DLC configuration

---

## Prerequisite System

The `md2026_techs_prereqs` effect grants "glue" technologies — intermediate techs that serve as prerequisites for later-tier technologies. This prevents the "missing prerequisite" issue where the game refuses to grant a tech because its parent wasn't unlocked.

Prerequisite chains are organized by category (13 batches total):
1. Artillery chains
2. Anti-tank & anti-air chains
3. Infantry chains
4. Engineering chains (AI, computing, encryption)
5. Non-NSB armor chains
6. NSB armor chains
7. BBA aircraft chains
8. Non-BBA fixed-wing chains
9. Non-BBA heavy aircraft chains
10. Helicopter chains
11. Missile chains
12. Naval chains
13. Industry & space chains
