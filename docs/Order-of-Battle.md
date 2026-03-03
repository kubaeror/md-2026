# Order of Battle (OOB)

The mod provides 65 Order of Battle files defining the military forces of each country at the start of the 2026 bookmark. OOB files are in `history/units/` and referenced from country history files via `oob = "TAG_2026"`.

---

## Design Philosophy

### Balanced for Gameplay

OOB files use **custom optimized templates** rather than exact real-world TO&Es. The goal is gameplay balance — every country should be playable and competitive within its tier, while still reflecting relative military power accurately.

### Template Approach

Instead of copying Millennium Dawn's default templates (which are designed for the 2000 start), the mod defines modern 2026-era unit templates:

- **Infantry**: Modernized with support companies (artillery, AT, AA, engineers, recon)
- **Mechanized/Motorized**: IFV/APC-equipped mobile divisions
- **Armor**: MBT-focused divisions with mechanized infantry support
- **Special Forces**: Marines, paratroopers, mountain, special operations
- **Naval**: Carrier groups, surface action groups, submarine squadrons
- **Air**: Fighter wings, multirole squadrons, CAS, transport, helicopter units

---

## OOB Tiers

### Tier 1 — Superpowers (3 countries)

**USA, Russia (SOV), China (CHI)**

Full-spectrum military forces including:
- Multiple army groups with armored, mechanized, and infantry divisions
- Blue-water navy with carrier battle groups
- Strategic and tactical air forces
- Nuclear forces (represented through techs/ideas, not OOB)
- Special operations forces

| Country | Army Divisions | Naval Groups | Air Wings |
|---------|---------------|--------------|-----------|
| USA | ~30+ | 6+ carrier groups | 15+ |
| SOV | ~40+ | 4+ fleets | 12+ |
| CHI | ~35+ | 3+ fleets | 10+ |

### Tier 2a — Major Powers (5 countries)

**Germany (GER), UK (ENG), France (FRA), Japan (JAP), India (RAJ)**

Professional military forces with:
- Corps-level ground forces
- Regional naval capabilities (some blue-water)
- Modern air force with 4th/5th gen aircraft

### Tier 2b — Regional Military Powers (4 countries)

**Turkey (TUR), Poland (POL), South Korea (KOR), Israel (ISR)**

Strong regional forces with:
- Division-level ground forces with modern equipment
- Coastal/regional navy
- Capable air force

### Tier 3a — Secondary Powers (10 countries)

**Italy (ITA), Saudi Arabia (SAU), Egypt (EGY), Pakistan (PAK), Ukraine (UKR), North Korea (NKO), Iran (PER), Brazil (BRA), Taiwan (TAI), Australia (AST)**

Significant military capabilities:
- Brigade-to-division level forces
- Varying naval capabilities
- Mixed-generation air force

### Tier 3b — NATO/Developed (10 countries)

**Canada (CAN), Spain (SPR), South Africa (SAF), Sweden (SWE), Finland (FIN), Greece (GRE), Romania (ROM), Hungary (HUN), Czechia (CZE), Myanmar (BRM)**

Professional but smaller forces focused on territorial defense or NATO commitments.

### Tier 3c — Conflict Zone Forces (8 countries)

**Syria (SYR), Yemen (YEM), Ethiopia (ETH), Afghanistan (AFG), Sudan (SUD), Belarus (BLR), Georgia (GEO), Armenia (ARM)**

Forces shaped by ongoing or recent conflicts, with:
- War-depleted or irregular formations
- Limited naval/air capabilities
- High manpower but lower equipment quality

### Tier 3d — Small NATO/Other (25 countries)

**Norway, Denmark, Belgium, Netherlands, Portugal, Bulgaria, Croatia, Albania, Lithuania, Latvia, Estonia, Slovakia, Slovenia, Montenegro, North Macedonia, Iceland, Luxembourg, Serbia, Bosnia, Kosovo, Kazakhstan, Kyrgyzstan, Tajikistan, Uzbekistan, Moldova**

Small professional forces, primarily:
- Brigade-level ground forces
- Limited or no navy
- Small air force
- NATO interoperability (where applicable)

Note: Iceland has no military forces (no OOB file).

---

## OOB File Format

Each OOB file follows HoI4's standard format:

```
division_template = {
    name = "Template Name"
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
        # ...
    }
    support = {
        artillery = { x = 0 y = 0 }
        engineer = { x = 0 y = 1 }
        # ...
    }
}

units = {
    division = {
        name = "1st Division"
        location = STATE_ID
        division_template = "Template Name"
        start_experience_factor = 0.3
    }
    # ...
}

# Naval units
fleet = {
    name = "Fleet Name"
    naval_base = STATE_ID
    task_force = {
        name = "Task Force"
        ship = { ... }
    }
}

# Air units
air_wings = {
    STATE_ID = {
        fighter_equipment = {
            owner = TAG
            amount = 100
        }
    }
}
```

---

## Unit Equipment

Units use equipment defined by the technology tier assigned to each country. For example:
- Tier 1 countries deploy the latest MBTs, 5th-gen fighters, modern ships
- Tier 3 countries have a mix of modern and older generation equipment
- Tier 5 countries rely primarily on basic infantry with limited heavy equipment

Equipment type is determined automatically by HoI4 based on researched technologies — the OOB only specifies template composition and unit counts.

---

## Special Considerations

### Ukraine
Ukraine's OOB reflects wartime mobilization with large infantry forces, Western-supplied equipment bonuses (via national spirits), and depleted armor/air forces consistent with the ongoing conflict.

### Russia
Russia's OOB reflects partial mobilization with large ground forces but equipment losses from the Ukraine war, partially offset by wartime production bonuses.

### North Korea
Large ground forces (reflecting one of the world's largest armies by personnel) but outdated equipment, consistent with Tier 4 technology assignment.

### Syria
Post-civil-war forces under new HTS government — small, irregular, with limited heavy equipment.
