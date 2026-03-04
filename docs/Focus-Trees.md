# Focus Trees

The mod adds 23 new focus tree branches for major and regional countries. These are implemented as **shared focuses** that attach to existing Millennium Dawn focus trees, appearing only when playing the 2026 bookmark.

The 7 compact trees (USA, Russia, Ukraine, China, Brazil, Saudi Arabia, Poland) have branches of ~8-12 focuses. The **16 expanded trees** (France, UK, Iran, Italy, North Korea, Canada, Australia, Taiwan, Egypt, Syria, Germany, Japan, South Korea, Israel, India, Turkey) each have **26 focuses** across 5 branches with mutually exclusive paths and capstone focuses.

---

## Architecture

### Shared Focus Approach

Instead of replacing entire focus trees (which would break MD compatibility), the mod uses HoI4's shared focus system:

1. **New focus branches** are defined as `shared_focus = { }` blocks in `md2026_*_focus.txt` files
2. **Original MD focus tree files** are copied into the submod with a `shared_focus = MD2026_XXX_root` reference added inside the `focus_tree = { }` block
3. **Branch gating** ensures 2026 branches only appear for the correct country in the 2026 bookmark:

```
allow_branch = {
    original_tag = TAG
    date > 2025.12.31
}
```

### File Structure

Each country has two files:
- `common/national_focus/md2026_TAG_focus.txt` — New shared focus definitions
- `common/national_focus/TAG_NF.txt` (or similar) — Copied MD original with `shared_focus` reference

---

## Focus Trees by Country

### USA — America in 2026

**Root**: `MD2026_USA_root` | **File**: `md2026_usa_focus.txt`

```
MD2026_USA_root
├── MD2026_USA_trump_agenda (Trump 2.0 / MAGA Agenda)
│   ├── MD2026_USA_mass_deportations → stability/manpower effects
│   ├── MD2026_USA_tariff_war → trade war with China/EU
│   ├── MD2026_USA_nato_pressure → NATO spending demands
│   └── MD2026_USA_energy_dominance → energy independence bonuses
├── MD2026_USA_deal_with_russia → diplomatic path to end Ukraine war
└── MD2026_USA_space_force → space technology bonuses
```

### Russia (SOV) — Crossroads

**Root**: `MD2026_SOV_root` | **File**: `md2026_sov_focus.txt`

```
MD2026_SOV_root
├── MD2026_SOV_war_path (Escalation)
│   ├── MD2026_SOV_total_mobilization → manpower + conscription
│   ├── MD2026_SOV_nuclear_brinkmanship → ultimatum events
│   └── MD2026_SOV_fortress_russia → defensive bonuses
├── MD2026_SOV_frozen_conflict (Negotiation)
│   ├── MD2026_SOV_ceasefire → war ends, partial sanctions relief
│   └── MD2026_SOV_autarky → self-sufficient economy
└── MD2026_SOV_eastern_pivot → BRICS+, SCO, China trade
```

### Ukraine (UKR) — Fight or Negotiate

**Root**: `MD2026_UKR_root` | **File**: `md2026_ukr_focus.txt`

```
MD2026_UKR_root
├── MD2026_UKR_war_path (Military)
│   ├── MD2026_UKR_counteroffensive → requires Western aid
│   └── MD2026_UKR_nato_membership → long-term NATO accession
├── MD2026_UKR_diplomatic_path (Diplomacy)
│   ├── MD2026_UKR_ceasefire → negotiated settlement
│   └── MD2026_UKR_eu_integration → EU accession path
└── MD2026_UKR_reconstruction → rebuilding bonuses
```

### China (CHI) — Century of China

**Root**: `MD2026_CHI_root` | **File**: `md2026_chi_focus.txt`

```
MD2026_CHI_root
├── MD2026_CHI_taiwan (Taiwan Question)
│   ├── MD2026_CHI_taiwan_escalation → military pressure
│   └── MD2026_CHI_taiwan_diplomacy → reunification talks
├── MD2026_CHI_bri2 (Belt & Road 2.0) → global influence
├── MD2026_CHI_tech_dominance → tech race with USA
└── MD2026_CHI_naval_expansion → South China Sea
```

### Germany (GER) — Zeitenwende 2026

**Root**: `MD2026_GER_zeitenwende_2026` | **File**: `md2026_ger_focus.txt`

```
MD2026_GER_zeitenwende_2026 (root)
├── MD2026_GER_european_army → EU defense integration
├── MD2026_GER_energy_independence → renewable energy transition
└── MD2026_GER_eu_expansion → Ukraine/Moldova/Balkans accession
```

*See [Expanded Focus Trees](#expanded-focus-trees-26-focuses-each) section for full 26-focus tree diagram.*

### India (RAJ) — India's Century

**Root**: `MD2026_RAJ_indias_century` | **File**: `md2026_raj_focus.txt`

```
MD2026_RAJ_indias_century (root)
├── MD2026_RAJ_make_in_india → industrial self-reliance
├── MD2026_RAJ_china_border → China/Pakistan border security
├── MD2026_RAJ_space_power → ISRO expansion
└── MD2026_RAJ_strategic_autonomy → multi-alignment diplomacy
```

*See [Expanded Focus Trees](#expanded-focus-trees-26-focuses-each) section for full 26-focus tree diagram.*

### Japan (JAP) — Active Defense Era

**Root**: `MD2026_JAP_active_defense` | **File**: `md2026_jap_focus.txt`

```
MD2026_JAP_active_defense (root)
├── MD2026_JAP_constitutional_reform → Article 9 revision
├── MD2026_JAP_indo_pacific → QUAD, regional security
├── MD2026_JAP_maritime_supremacy → carrier fleet, submarine force
└── MD2026_JAP_economic_revitalization → semiconductor, robotics
```

*See [Expanded Focus Trees](#expanded-focus-trees-26-focuses-each) section for full 26-focus tree diagram.*

### Turkey (TUR) — Turkiye's New Era

**Root**: `MD2026_TUR_new_era` | **File**: `md2026_tur_focus.txt`

```
MD2026_TUR_new_era (root)
├── MD2026_TUR_defense_industry → domestic arms production
├── MD2026_TUR_mediation_power → regional strategy, NATO/Eurasia
├── MD2026_TUR_dual_seas → Black Sea & Mediterranean
└── MD2026_TUR_syria_influence → safe zone, refugee return
```

*See [Expanded Focus Trees](#expanded-focus-trees-26-focuses-each) section for full 26-focus tree diagram.*

### Brazil (BRA) — Green Superpower

**Root**: `MD2026_BRA_root` | **File**: `md2026_bra_focus.txt`

```
MD2026_BRA_root
├── MD2026_BRA_amazon_guardian → environmental protection
├── MD2026_BRA_brics_leadership → BRICS presidency
├── MD2026_BRA_south_atlantic → naval presence
└── MD2026_BRA_industrial_policy → reindustrialization
```

### Israel (ISR) — Iron Wall 2026

**Root**: `MD2026_ISR_iron_wall` | **File**: `md2026_isr_focus.txt`

```
MD2026_ISR_iron_wall (root)
├── MD2026_ISR_gaza_aftermath → post-Oct 7 security operations
├── MD2026_ISR_iran_threat → counter-proliferation
├── MD2026_ISR_mossad_shin_bet → intelligence & special ops
└── MD2026_ISR_abraham_accords → normalization expansion
```

*See [Expanded Focus Trees](#expanded-focus-trees-26-focuses-each) section for full 26-focus tree diagram.*

### South Korea (KOR) — Shield of Freedom

**Root**: `MD2026_KOR_shield_freedom` | **File**: `md2026_kor_focus.txt`

```
MD2026_KOR_shield_freedom (root)
├── MD2026_KOR_nk_deterrence → NK deterrence & kill chain
├── MD2026_KOR_peninsular_strategy → North Korea engagement/pressure
├── MD2026_KOR_k_defense → KF-21, K2 Panther, defense exports
└── MD2026_KOR_k_economy → semiconductors, cultural export
```

*See [Expanded Focus Trees](#expanded-focus-trees-26-focuses-each) section for full 26-focus tree diagram.*

### Saudi Arabia (SAU) — Vision 2030

**Root**: `MD2026_SAU_root` | **File**: `md2026_sau_focus.txt`

```
MD2026_SAU_root
├── MD2026_SAU_vision_2030 → economic diversification
├── MD2026_SAU_regional_security → Yemen, Iran balance
├── MD2026_SAU_normalization → Israel relations
└── MD2026_SAU_energy_transition → post-oil economy
```

### Poland (POL) — Shield of the East

**Root**: `MD2026_POL_root` | **File**: `md2026_pol_focus.txt`

```
MD2026_POL_root
├── MD2026_POL_fortress_poland → eastern border fortification
├── MD2026_POL_military_modernization → K2 tanks, FA-50, Patriot
├── MD2026_POL_eu_leadership → Weimar Triangle, EU influence
└── MD2026_POL_ukraine_support → aid and reconstruction
```

---

## Expanded Focus Trees (26 focuses each)

The following 16 countries have expanded trees with 5 branches each: 4 non-mutually-exclusive branches (T1→T2a+T2b→T3a+T3b) and 1 mutually exclusive branch (T1→T2a⊕T2b→T3). Each tree also has a capstone focus requiring completion of multiple T3 focuses. Root + T1 + non-ME T2 focuses (14 total) are pre-completed in history files.

### France (FRA) — European Power

**Root**: `MD2026_FRA_european_power` | **File**: `md2026_fra_focus.txt`

```
MD2026_FRA_european_power (root)
├── Branch 1: European Defense (x=-6)
│   ├── MD2026_FRA_european_defense (T1)
│   │   ├── MD2026_FRA_nuclear_deterrent (T2) → MD2026_FRA_strategic_autonomy (T3)
│   │   └── MD2026_FRA_arms_exports (T2) → MD2026_FRA_indo_pacific_presence (T3)
├── Branch 2: African Policy (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_FRA_african_policy (T1)
│   │   ├── MD2026_FRA_sahel_withdrawal (T2, ME) ⊕ MD2026_FRA_sahel_reengage (T2, ME)
│   │   └── MD2026_FRA_eu_defense_fund (T3, requires either T2)
├── Branch 3: Domestic Reform (x=0)
│   ├── MD2026_FRA_domestic_reform (T1)
│   │   ├── MD2026_FRA_2027_elections (T2) → MD2026_FRA_energy_transition (T3)
│   │   └── MD2026_FRA_economic_competitiveness (T2) → MD2026_FRA_nuclear_energy (T3)
├── Branch 4: European Integration (x=3)
│   ├── MD2026_FRA_european_integration (T1)
│   │   ├── MD2026_FRA_eu_reform (T2) → MD2026_FRA_eu_army (T3)
│   │   └── MD2026_FRA_franco_german_engine (T2) → MD2026_FRA_european_sovereignty (T3)
├── Branch 5: Technology (x=6)
│   ├── MD2026_FRA_technology_investment (T1)
│   │   ├── MD2026_FRA_ai_strategy (T2) → MD2026_FRA_digital_sovereignty (T3)
│   │   └── MD2026_FRA_green_industry (T2) → MD2026_FRA_hydrogen_economy (T3)
└── MD2026_FRA_capstone (y=5) → requires root + T3 focuses

ME pair: sahel_withdrawal ⊕ sahel_reengage
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### United Kingdom (ENG) — Global Britain

**Root**: `MD2026_ENG_global_britain` | **File**: `md2026_eng_focus.txt`

```
MD2026_ENG_global_britain (root)
├── Branch 1: Nuclear & AUKUS (x=-6)
│   ├── MD2026_ENG_nuclear_deterrent (T1)
│   │   ├── MD2026_ENG_aukus (T2) → MD2026_ENG_cyber_warfare (T3)
│   │   └── MD2026_ENG_carrier_strike (T2) → MD2026_ENG_army_modernization (T3)
├── Branch 2: Post-Brexit Trade (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_ENG_post_brexit_trade (T1)
│   │   ├── MD2026_ENG_cptpp (T2, ME) ⊕ MD2026_ENG_eu_rapprochement (T2, ME)
│   │   └── MD2026_ENG_science_innovation (T3, requires either T2)
├── Branch 3: Special Relationship (x=0)
│   ├── MD2026_ENG_special_relationship (T1)
│   │   ├── MD2026_ENG_five_eyes (T2) → MD2026_ENG_ai_strategy (T3)
│   │   └── MD2026_ENG_ukraine_support (T2) → MD2026_ENG_biotech_hub (T3)
├── Branch 4: Armed Forces (x=3)
│   ├── MD2026_ENG_armed_forces (T1)
│   │   ├── MD2026_ENG_tempest_fighter (T2) → MD2026_ENG_defense_innovation (T3)
│   │   └── MD2026_ENG_royal_navy (T2) → MD2026_ENG_arctic_presence (T3)
├── Branch 5: Commonwealth (x=6)
│   ├── MD2026_ENG_commonwealth_renewal (T1)
│   │   ├── MD2026_ENG_pacific_tilt (T2) → MD2026_ENG_indo_pacific_hub (T3)
│   │   └── MD2026_ENG_african_trade (T2) → MD2026_ENG_development_finance (T3)
└── MD2026_ENG_capstone (y=5) → requires root + T3 focuses

ME pair: cptpp ⊕ eu_rapprochement
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### Iran (PER) — Regime Survival

**Root**: `MD2026_PER_regime_survival` | **File**: `md2026_per_focus.txt`

```
MD2026_PER_regime_survival (root)
├── Branch 1: Nuclear Program (x=-6) — MUTUALLY EXCLUSIVE
│   ├── MD2026_PER_nuclear_program (T1)
│   │   ├── MD2026_PER_nuclear_accelerate (T2, ME) ⊕ MD2026_PER_nuclear_negotiate (T2, ME)
│   │   └── MD2026_PER_air_defense (T3, requires either T2)
├── Branch 2: Regional Proxies (x=-3)
│   ├── MD2026_PER_regional_proxies (T1)
│   │   ├── MD2026_PER_axis_resistance (T2) → MD2026_PER_hezbollah_rebuild (T3)
│   │   └── MD2026_PER_proxy_rebuild (T2) → MD2026_PER_iraq_influence (T3)
├── Branch 3: Sanctions Economy (x=0)
│   ├── MD2026_PER_sanctions_economy (T1)
│   │   ├── MD2026_PER_oil_barter (T2) → MD2026_PER_economic_resistance (T3)
│   │   └── MD2026_PER_russia_alliance (T2) → MD2026_PER_caspian_corridor (T3)
├── Branch 4: Domestic Control (x=3)
│   ├── MD2026_PER_domestic_control (T1)
│   │   ├── MD2026_PER_irgc_power (T2) → MD2026_PER_basij_expansion (T3)
│   │   └── MD2026_PER_succession_planning (T2) → MD2026_PER_velayat_consolidation (T3)
├── Branch 5: Military Industry (x=6)
│   ├── MD2026_PER_military_industry (T1)
│   │   ├── MD2026_PER_drone_program (T2) → MD2026_PER_missile_arsenal (T3)
│   │   └── MD2026_PER_information_warfare (T2) → MD2026_PER_cyber_army (T3)
└── MD2026_PER_capstone (y=5) → requires root + T3 focuses

ME pair: nuclear_accelerate ⊕ nuclear_negotiate
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### Italy (ITA) — Mediterranean Crossroads

**Root**: `MD2026_ITA_mediterranean_crossroads` | **File**: `md2026_ita_focus.txt`

```
MD2026_ITA_mediterranean_crossroads (root)
├── Branch 1: NATO Southern Flank (x=-6)
│   ├── MD2026_ITA_nato_southern_flank (T1)
│   │   ├── MD2026_ITA_naval_power (T2) → MD2026_ITA_mediterranean_security (T3)
│   │   └── MD2026_ITA_tempest_fighter (T2) → MD2026_ITA_defense_industry (T3)
├── Branch 2: Economic Reform (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_ITA_economic_reform (T1)
│   │   ├── MD2026_ITA_south_development (T2, ME) ⊕ MD2026_ITA_northern_industry (T2, ME)
│   │   └── MD2026_ITA_eurozone_reform (T3, requires either T2)
├── Branch 3: Migration Crisis (x=0)
│   ├── MD2026_ITA_migration_crisis (T1)
│   │   ├── MD2026_ITA_fortress_europe (T2) → MD2026_ITA_demographic_recovery (T3)
│   │   └── MD2026_ITA_integration_plan (T2) → MD2026_ITA_labor_market (T3)
├── Branch 4: Piano Mattei (x=3)
│   ├── MD2026_ITA_piano_mattei (T1)
│   │   ├── MD2026_ITA_energy_corridors (T2) → MD2026_ITA_african_partnership (T3)
│   │   └── MD2026_ITA_libya_stabilization (T2) → MD2026_ITA_gas_hub (T3)
├── Branch 5: EU Leadership (x=6)
│   ├── MD2026_ITA_eu_leadership (T1)
│   │   ├── MD2026_ITA_cultural_heritage (T2) → MD2026_ITA_soft_power (T3)
│   │   └── MD2026_ITA_vatican_diplomacy (T2) → MD2026_ITA_g7_presidency (T3)
└── MD2026_ITA_capstone (y=5) → requires root + T3 focuses

ME pair: south_development ⊕ northern_industry
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### North Korea (NKO) — Nuclear Shield

**Root**: `MD2026_NKO_nuclear_shield` | **File**: `md2026_nko_focus.txt`

```
MD2026_NKO_nuclear_shield (root)
├── Branch 1: Nuclear Expansion (x=-6)
│   ├── MD2026_NKO_nuclear_expansion (T1)
│   │   ├── MD2026_NKO_icbm_program (T2) → MD2026_NKO_thermonuclear (T3)
│   │   └── MD2026_NKO_tactical_nukes (T2) → MD2026_NKO_nuclear_doctrine (T3)
├── Branch 2: Russia Alliance (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_NKO_russia_alliance (T1)
│   │   ├── MD2026_NKO_south_korea_threat (T2, ME) ⊕ MD2026_NKO_diplomatic_leverage (T2, ME)
│   │   └── MD2026_NKO_satellite_program (T3, requires either T2)
├── Branch 3: Provocations (x=0)
│   ├── MD2026_NKO_provocations (T1)
│   │   ├── MD2026_NKO_arms_for_russia (T2) → MD2026_NKO_conventional_buildup (T3)
│   │   └── MD2026_NKO_russian_tech (T2) → MD2026_NKO_modern_equipment (T3)
├── Branch 4: Regime Maintenance (x=3)
│   ├── MD2026_NKO_regime_maintenance (T1)
│   │   ├── MD2026_NKO_cult_personality (T2) → MD2026_NKO_songbun_system (T3)
│   │   └── MD2026_NKO_juche_economy (T2) → MD2026_NKO_special_economic_zones (T3)
├── Branch 5: Cyber Warfare (x=6)
│   ├── MD2026_NKO_cyber_warfare (T1)
│   │   ├── MD2026_NKO_crypto_theft (T2) → MD2026_NKO_cyber_army (T3)
│   │   └── MD2026_NKO_information_warfare (T2) → MD2026_NKO_propaganda_machine (T3)
└── MD2026_NKO_capstone (y=5) → requires root + T3 focuses

ME pair: south_korea_threat ⊕ diplomatic_leverage
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### Canada (CAN) — Northern Shield

**Root**: `MD2026_CAN_northern_shield` | **File**: `md2026_can_focus.txt`

```
MD2026_CAN_northern_shield (root)
├── Branch 1: Arctic Sovereignty (x=-6)
│   ├── MD2026_CAN_arctic_sovereignty (T1)
│   │   ├── MD2026_CAN_northwest_passage (T2) → MD2026_CAN_arctic_military (T3)
│   │   └── MD2026_CAN_arctic_resources (T2) → MD2026_CAN_northern_development (T3)
├── Branch 2: US Trade Tensions (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_CAN_us_trade_tensions (T1)
│   │   ├── MD2026_CAN_trade_diversification (T2, ME) ⊕ MD2026_CAN_us_accommodation (T2, ME)
│   │   └── MD2026_CAN_cptpp_engagement (T3, requires either T2)
├── Branch 3: Defense Modernization (x=0)
│   ├── MD2026_CAN_defense_modernization (T1)
│   │   ├── MD2026_CAN_norad_renewal (T2) → MD2026_CAN_cyber_defense (T3)
│   │   └── MD2026_CAN_navy_expansion (T2) → MD2026_CAN_shipbuilding (T3)
├── Branch 4: Indo-Pacific (x=3)
│   ├── MD2026_CAN_indo_pacific (T1)
│   │   ├── MD2026_CAN_pacific_security (T2) → MD2026_CAN_asean_engagement (T3)
│   │   └── MD2026_CAN_critical_minerals (T2) → MD2026_CAN_supply_chain (T3)
├── Branch 5: Domestic Agenda (x=6)
│   ├── MD2026_CAN_domestic_agenda (T1)
│   │   ├── MD2026_CAN_reconciliation (T2) → MD2026_CAN_social_housing (T3)
│   │   └── MD2026_CAN_immigration_reform (T2) → MD2026_CAN_tech_sector (T3)
└── MD2026_CAN_capstone (y=5) → requires root + T3 focuses

ME pair: trade_diversification ⊕ us_accommodation
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### Australia (AST) — Pacific Partner

**Root**: `MD2026_AST_pacific_partner` | **File**: `md2026_ast_focus.txt`

```
MD2026_AST_pacific_partner (root)
├── Branch 1: AUKUS Commitment (x=-6)
│   ├── MD2026_AST_aukus_commitment (T1)
│   │   ├── MD2026_AST_nuclear_submarines (T2) → MD2026_AST_submarine_base (T3)
│   │   └── MD2026_AST_missile_capability (T2) → MD2026_AST_long_range_strike (T3)
├── Branch 2: China Balancing (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_AST_china_balancing (T1)
│   │   ├── MD2026_AST_china_decouple (T2, ME) ⊕ MD2026_AST_china_engage (T2, ME)
│   │   └── MD2026_AST_pacific_security (T3, requires either T2)
├── Branch 3: Pacific Islands (x=0)
│   ├── MD2026_AST_pacific_islands (T1)
│   │   ├── MD2026_AST_pacific_aid (T2) → MD2026_AST_climate_diplomacy (T3)
│   │   └── MD2026_AST_northern_bases (T2) → MD2026_AST_force_posture (T3)
├── Branch 4: Defense Expansion (x=3)
│   ├── MD2026_AST_defense_expansion (T1)
│   │   ├── MD2026_AST_cyber_defense (T2) → MD2026_AST_space_command (T3)
│   │   └── MD2026_AST_army_expansion (T2) → MD2026_AST_integrated_force (T3)
├── Branch 5: Economic Resilience (x=6)
│   ├── MD2026_AST_economic_resilience (T1)
│   │   ├── MD2026_AST_green_energy (T2) → MD2026_AST_hydrogen_export (T3)
│   │   └── MD2026_AST_innovation_economy (T2) → MD2026_AST_tech_sovereignty (T3)
└── MD2026_AST_capstone (y=5) → requires root + T3 focuses

ME pair: china_decouple ⊕ china_engage
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### Taiwan (TAI) — Porcupine Defense

**Root**: `MD2026_TAI_porcupine_defense` | **File**: `md2026_tai_focus.txt`

```
MD2026_TAI_porcupine_defense (root)
├── Branch 1: Asymmetric Defense (x=-6)
│   ├── MD2026_TAI_asymmetric_defense (T1)
│   │   ├── MD2026_TAI_anti_ship_missiles (T2) → MD2026_TAI_fortress_taiwan (T3)
│   │   └── MD2026_TAI_reserve_mobilization (T2) → MD2026_TAI_civil_defense_force (T3)
├── Branch 2: Silicon Shield (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_TAI_silicon_shield (T1)
│   │   ├── MD2026_TAI_us_arms_sales (T2, ME) ⊕ MD2026_TAI_japan_cooperation (T2, ME)
│   │   └── MD2026_TAI_international_space (T3, requires either T2)
├── Branch 3: TSMC & Tech (x=0)
│   ├── MD2026_TAI_tsmc_dominance (T1)
│   │   ├── MD2026_TAI_tech_sovereignty (T2) → MD2026_TAI_quantum_computing (T3)
│   │   └── MD2026_TAI_semiconductor_expansion (T2) → MD2026_TAI_ai_development (T3)
├── Branch 4: Civil Defense (x=3)
│   ├── MD2026_TAI_civil_defense (T1)
│   │   ├── MD2026_TAI_shelter_program (T2) → MD2026_TAI_resilient_infrastructure (T3)
│   │   └── MD2026_TAI_information_warfare (T2) → MD2026_TAI_media_resilience (T3)
├── Branch 5: Economic Diversification (x=6)
│   ├── MD2026_TAI_economic_diversification (T1)
│   │   ├── MD2026_TAI_green_energy (T2) → MD2026_TAI_energy_independence (T3)
│   │   └── MD2026_TAI_southbound_policy (T2) → MD2026_TAI_asean_integration (T3)
└── MD2026_TAI_capstone (y=5) → requires root + T3 focuses

ME pair: us_arms_sales ⊕ japan_cooperation
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### Egypt (EGY) — Nile Power

**Root**: `MD2026_EGY_nile_power` | **File**: `md2026_egy_focus.txt`

```
MD2026_EGY_nile_power (root)
├── Branch 1: Military Modernization (x=-6)
│   ├── MD2026_EGY_military_modernization (T1)
│   │   ├── MD2026_EGY_economic_crisis (T2) → MD2026_EGY_defense_industry (T3)
│   │   └── MD2026_EGY_imf_program (T2) → MD2026_EGY_economic_reform (T3)
├── Branch 2: Arms Procurement (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_EGY_gulf_investment (T1)
│   │   ├── MD2026_EGY_us_weapons (T2, ME) ⊕ MD2026_EGY_diversify_suppliers (T2, ME)
│   │   └── MD2026_EGY_infrastructure_expansion (T3, requires either T2)
├── Branch 3: Regional Role (x=0)
│   ├── MD2026_EGY_regional_role (T1)
│   │   ├── MD2026_EGY_gaza_mediator (T2) → MD2026_EGY_arab_leadership (T3)
│   │   └── MD2026_EGY_nile_dispute (T2) → MD2026_EGY_water_security (T3)
├── Branch 4: Mega Projects (x=3)
│   ├── MD2026_EGY_mega_projects (T1)
│   │   ├── MD2026_EGY_new_capital (T2) → MD2026_EGY_suez_expansion (T3)
│   │   └── MD2026_EGY_tourism_revival (T2) → MD2026_EGY_cultural_power (T3)
├── Branch 5: Energy Future (x=6)
│   ├── MD2026_EGY_energy_future (T1)
│   │   ├── MD2026_EGY_nuclear_power (T2) → MD2026_EGY_energy_hub (T3)
│   │   └── MD2026_EGY_solar_farms (T2) → MD2026_EGY_green_hydrogen (T3)
└── MD2026_EGY_capstone (y=5) → requires root + T3 focuses

ME pair: us_weapons ⊕ diversify_suppliers
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### Syria (SYR) — New Syria

**Root**: `MD2026_SYR_new_syria` | **File**: `md2026_syr_focus.txt`

```
MD2026_SYR_new_syria (root)
├── Branch 1: National Governance (x=-6) — MUTUALLY EXCLUSIVE
│   ├── MD2026_SYR_national_governance (T1)
│   │   ├── MD2026_SYR_secular_state (T2, ME) ⊕ MD2026_SYR_islamic_governance (T2, ME)
│   │   └── MD2026_SYR_refugee_return (T3, requires either T2)
├── Branch 2: Reconstruction (x=-3)
│   ├── MD2026_SYR_reconstruction (T1)
│   │   ├── MD2026_SYR_infrastructure_rebuild (T2) → MD2026_SYR_housing_program (T3)
│   │   └── MD2026_SYR_healthcare_system (T2) → MD2026_SYR_education_reform (T3)
├── Branch 3: Security Consolidation (x=0)
│   ├── MD2026_SYR_security_consolidation (T1)
│   │   ├── MD2026_SYR_new_army (T2) → MD2026_SYR_border_control (T3)
│   │   └── MD2026_SYR_kurdish_question (T2) → MD2026_SYR_national_reconciliation (T3)
├── Branch 4: International Recognition (x=3)
│   ├── MD2026_SYR_international_recognition (T1)
│   │   ├── MD2026_SYR_western_engagement (T2) → MD2026_SYR_sanctions_relief (T3)
│   │   └── MD2026_SYR_arab_reintegration (T2) → MD2026_SYR_arab_league (T3)
├── Branch 5: Economic Recovery (x=6)
│   ├── MD2026_SYR_economic_recovery (T1)
│   │   ├── MD2026_SYR_foreign_investment (T2) → MD2026_SYR_oil_reconstruction (T3)
│   │   └── MD2026_SYR_agriculture_revival (T2) → MD2026_SYR_food_security (T3)
└── MD2026_SYR_capstone (y=5) → requires root + T3 focuses

ME pair: secular_state ⊕ islamic_governance
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### Germany (GER) — Zeitenwende 2026

**Root**: `MD2026_GER_zeitenwende_2026` | **File**: `md2026_ger_focus.txt`

```
MD2026_GER_zeitenwende_2026 (root)
├── Branch 1: Bundeswehr Modernization (x=-6)
│   ├── MD2026_GER_bundeswehr_reform (T1)
│   │   ├── MD2026_GER_leopard_program (T2) → MD2026_GER_european_army_corps (T3)
│   │   └── MD2026_GER_eurofighter_upgrade (T2) → MD2026_GER_air_defense_shield (T3)
├── Branch 2: NATO Commitment (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_GER_nato_commitment (T1)
│   │   ├── MD2026_GER_atlantic_solidarity (T2, ME) ⊕ MD2026_GER_european_defense_pillar (T2, ME)
│   │   └── MD2026_GER_defense_spending (T3, requires either T2)
├── Branch 3: Energy Transition (x=0)
│   ├── MD2026_GER_energy_transition (T1)
│   │   ├── MD2026_GER_renewables_expansion (T2) → MD2026_GER_hydrogen_economy (T3)
│   │   └── MD2026_GER_lng_terminals (T2) → MD2026_GER_industrial_resilience (T3)
├── Branch 4: EU Leadership (x=3)
│   ├── MD2026_GER_eu_leadership (T1)
│   │   ├── MD2026_GER_eu_enlargement (T2) → MD2026_GER_balkans_accession (T3)
│   │   └── MD2026_GER_franco_german_engine (T2) → MD2026_GER_eu_defense_fund (T3)
├── Branch 5: Economic & Technology (x=6)
│   ├── MD2026_GER_wirtschaftswunder (T1)
│   │   ├── MD2026_GER_ai_leadership (T2) → MD2026_GER_digital_sovereignty (T3)
│   │   └── MD2026_GER_mittelstand_innovation (T2) → MD2026_GER_green_technology (T3)
└── MD2026_GER_leading_europe (y=5) → requires root + T3 focuses

ME pair: atlantic_solidarity ⊕ european_defense_pillar
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### Japan (JAP) — Active Defense Era

**Root**: `MD2026_JAP_active_defense` | **File**: `md2026_jap_focus.txt`

```
MD2026_JAP_active_defense (root)
├── Branch 1: Constitutional Reform & Defense (x=-6)
│   ├── MD2026_JAP_constitutional_reform (T1)
│   │   ├── MD2026_JAP_counterattack_capability (T2) → MD2026_JAP_jsdf_expansion (T3)
│   │   └── MD2026_JAP_missile_defense (T2) → MD2026_JAP_integrated_air_defense (T3)
├── Branch 2: Indo-Pacific Strategy (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_JAP_indo_pacific (T1)
│   │   ├── MD2026_JAP_taiwan_contingency (T2, ME) ⊕ MD2026_JAP_korea_reconciliation (T2, ME)
│   │   └── MD2026_JAP_quad_plus (T3, requires either T2)
├── Branch 3: Maritime Power (x=0)
│   ├── MD2026_JAP_maritime_supremacy (T1)
│   │   ├── MD2026_JAP_carrier_fleet (T2) → MD2026_JAP_pacific_guardian (T3)
│   │   └── MD2026_JAP_submarine_force (T2) → MD2026_JAP_island_defense (T3)
├── Branch 4: Economic Revitalization (x=3)
│   ├── MD2026_JAP_economic_revitalization (T1)
│   │   ├── MD2026_JAP_tech_sovereignty (T2) → MD2026_JAP_ai_robotics (T3)
│   │   └── MD2026_JAP_semiconductor_strategy (T2) → MD2026_JAP_supply_chain_resilience (T3)
├── Branch 5: US Alliance & Security (x=6)
│   ├── MD2026_JAP_us_alliance (T1)
│   │   ├── MD2026_JAP_joint_operations (T2) → MD2026_JAP_cyber_defense (T3)
│   │   └── MD2026_JAP_intelligence_sharing (T2) → MD2026_JAP_okinawa_posture (T3)
└── MD2026_JAP_normal_nation (y=5) → requires root + T3 focuses

ME pair: taiwan_contingency ⊕ korea_reconciliation
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### South Korea (KOR) — Shield of Freedom

**Root**: `MD2026_KOR_shield_freedom` | **File**: `md2026_kor_focus.txt`

```
MD2026_KOR_shield_freedom (root)
├── Branch 1: NK Deterrence (x=-6)
│   ├── MD2026_KOR_nk_deterrence (T1)
│   │   ├── MD2026_KOR_kill_chain (T2) → MD2026_KOR_dmz_fortification (T3)
│   │   └── MD2026_KOR_missile_shield (T2) → MD2026_KOR_preemptive_capability (T3)
├── Branch 2: Peninsular Strategy (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_KOR_peninsular_strategy (T1)
│   │   ├── MD2026_KOR_diplomatic_opening (T2, ME) ⊕ MD2026_KOR_maximum_pressure (T2, ME)
│   │   └── MD2026_KOR_unification_preparation (T3, requires either T2)
├── Branch 3: Defense Industry (x=0)
│   ├── MD2026_KOR_k_defense (T1)
│   │   ├── MD2026_KOR_kf21_boramae (T2) → MD2026_KOR_defense_exports (T3)
│   │   └── MD2026_KOR_k2_panther (T2) → MD2026_KOR_naval_expansion (T3)
├── Branch 4: Economy & Tech (x=3)
│   ├── MD2026_KOR_k_economy (T1)
│   │   ├── MD2026_KOR_semiconductor_hub (T2) → MD2026_KOR_ai_innovation (T3)
│   │   └── MD2026_KOR_cultural_export (T2) → MD2026_KOR_green_economy (T3)
├── Branch 5: Alliance & Indo-Pacific (x=6)
│   ├── MD2026_KOR_us_alliance (T1)
│   │   ├── MD2026_KOR_combined_forces (T2) → MD2026_KOR_japan_cooperation (T3)
│   │   └── MD2026_KOR_indo_pacific_partner (T2) → MD2026_KOR_asean_engagement (T3)
└── MD2026_KOR_global_pivot_state (y=5) → requires root + T3 focuses

ME pair: diplomatic_opening ⊕ maximum_pressure
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### Israel (ISR) — Iron Wall 2026

**Root**: `MD2026_ISR_iron_wall` | **File**: `md2026_isr_focus.txt`

```
MD2026_ISR_iron_wall (root)
├── Branch 1: Security Operations (x=-6)
│   ├── MD2026_ISR_gaza_aftermath (T1)
│   │   ├── MD2026_ISR_northern_front (T2) → MD2026_ISR_iron_dome_upgrade (T3)
│   │   └── MD2026_ISR_border_defense (T2) → MD2026_ISR_idf_restructuring (T3)
├── Branch 2: Iran Threat (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_ISR_iran_threat (T1)
│   │   ├── MD2026_ISR_preemptive_strike (T2, ME) ⊕ MD2026_ISR_covert_ops (T2, ME)
│   │   └── MD2026_ISR_nuclear_deterrent (T3, requires either T2)
├── Branch 3: Intelligence & Special Ops (x=0)
│   ├── MD2026_ISR_mossad_shin_bet (T1)
│   │   ├── MD2026_ISR_regional_intelligence (T2) → MD2026_ISR_counter_terrorism (T3)
│   │   └── MD2026_ISR_signals_intelligence (T2) → MD2026_ISR_cyber_warfare (T3)
├── Branch 4: Normalization (x=3)
│   ├── MD2026_ISR_abraham_accords (T1)
│   │   ├── MD2026_ISR_saudi_deal (T2) → MD2026_ISR_regional_trade (T3)
│   │   └── MD2026_ISR_gulf_integration (T2) → MD2026_ISR_water_diplomacy (T3)
├── Branch 5: Defense Tech (x=6)
│   ├── MD2026_ISR_defense_tech (T1)
│   │   ├── MD2026_ISR_iron_beam (T2) → MD2026_ISR_ai_warfare (T3)
│   │   └── MD2026_ISR_uav_dominance (T2) → MD2026_ISR_space_program (T3)
└── MD2026_ISR_startup_nation (y=5) → requires root + T3 focuses

ME pair: preemptive_strike ⊕ covert_ops
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### India (RAJ) — India's Century

**Root**: `MD2026_RAJ_indias_century` | **File**: `md2026_raj_focus.txt`

```
MD2026_RAJ_indias_century (root)
├── Branch 1: Make in India (x=-6)
│   ├── MD2026_RAJ_make_in_india (T1)
│   │   ├── MD2026_RAJ_digital_india (T2) → MD2026_RAJ_defense_production (T3)
│   │   └── MD2026_RAJ_semiconductor_push (T2) → MD2026_RAJ_green_energy (T3)
├── Branch 2: Strategic Autonomy (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_RAJ_strategic_autonomy (T1)
│   │   ├── MD2026_RAJ_quad_deepening (T2, ME) ⊕ MD2026_RAJ_brics_balance (T2, ME)
│   │   └── MD2026_RAJ_multi_alignment (T3, requires either T2)
├── Branch 3: Border Security (x=0)
│   ├── MD2026_RAJ_china_border (T1)
│   │   ├── MD2026_RAJ_lac_fortification (T2) → MD2026_RAJ_agni_deterrent (T3)
│   │   └── MD2026_RAJ_mountain_strike (T2) → MD2026_RAJ_military_modernization (T3)
├── Branch 4: Naval Power (x=3)
│   ├── MD2026_RAJ_blue_water_navy (T1)
│   │   ├── MD2026_RAJ_carrier_program (T2) → MD2026_RAJ_indian_ocean_dominance (T3)
│   │   └── MD2026_RAJ_submarine_fleet (T2) → MD2026_RAJ_andaman_command (T3)
├── Branch 5: Space & Technology (x=6)
│   ├── MD2026_RAJ_space_power (T1)
│   │   ├── MD2026_RAJ_isro_expansion (T2) → MD2026_RAJ_moon_mission (T3)
│   │   └── MD2026_RAJ_ai_hub (T2) → MD2026_RAJ_quantum_computing (T3)
└── MD2026_RAJ_vishwaguru (y=5) → requires root + T3 focuses

ME pair: quad_deepening ⊕ brics_balance
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

### Turkey (TUR) — Turkiye's New Era

**Root**: `MD2026_TUR_new_era` | **File**: `md2026_tur_focus.txt`

```
MD2026_TUR_new_era (root)
├── Branch 1: Defense Industry (x=-6)
│   ├── MD2026_TUR_defense_industry (T1)
│   │   ├── MD2026_TUR_bayraktar (T2) → MD2026_TUR_defense_exports (T3)
│   │   └── MD2026_TUR_tfx_fighter (T2) → MD2026_TUR_naval_program (T3)
├── Branch 2: Regional Strategy (x=-3) — MUTUALLY EXCLUSIVE
│   ├── MD2026_TUR_mediation_power (T1)
│   │   ├── MD2026_TUR_nato_loyalty (T2, ME) ⊕ MD2026_TUR_eurasian_pivot (T2, ME)
│   │   └── MD2026_TUR_regional_hegemon (T3, requires either T2)
├── Branch 3: Black Sea & Mediterranean (x=0)
│   ├── MD2026_TUR_dual_seas (T1)
│   │   ├── MD2026_TUR_black_sea_control (T2) → MD2026_TUR_straits_leverage (T3)
│   │   └── MD2026_TUR_east_med (T2) → MD2026_TUR_libya_influence (T3)
├── Branch 4: Economy (x=3)
│   ├── MD2026_TUR_central_corridor (T1)
│   │   ├── MD2026_TUR_energy_hub (T2) → MD2026_TUR_middle_corridor (T3)
│   │   └── MD2026_TUR_turkic_council (T2) → MD2026_TUR_economic_stabilization (T3)
├── Branch 5: Syria & Influence (x=6)
│   ├── MD2026_TUR_syria_influence (T1)
│   │   ├── MD2026_TUR_safe_zone (T2) → MD2026_TUR_infrastructure_projects (T3)
│   │   └── MD2026_TUR_refugee_return (T2) → MD2026_TUR_cultural_influence (T3)
└── MD2026_TUR_century_of_turkiye (y=5) → requires root + T3 focuses

ME pair: nato_loyalty ⊕ eurasian_pivot
Pre-completed (14): root + 5 T1 + 8 non-ME T2
```

---

## Opinion Modifiers

Focus tree effects use custom opinion modifiers (prefixed with `md2026_`) to avoid conflicts with base MD:

| Modifier | Value | Decay | Used In |
|----------|-------|-------|---------|
| `md2026_improved_relations` | +25 | 1/year | Multiple focus trees |
| `md2026_border_conflict` | -30 | 1/year | RAJ, POL focus trees |
| `md2026_diplomatic_disapproval` | -20 | 1/year | Elections events |
| `md2026_tech_rivalry` | -15 | 1/year | Tech/space events |
| `md2026_migration_tensions` | -20 | 1/year | Migration events |

---

## Adding a New Focus Tree

To add a new 2026 focus branch for a country:

1. Create `common/national_focus/md2026_TAG_focus.txt` with `shared_focus = { }` blocks
2. Copy the original MD focus tree file into the submod
3. Add `shared_focus = MD2026_TAG_root` inside the `focus_tree = { }` header
4. Use `allow_branch = { original_tag = TAG date > 2025.12.31 }` to gate visibility
5. Add localisation keys for all focus names and descriptions
