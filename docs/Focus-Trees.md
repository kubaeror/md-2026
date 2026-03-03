# Focus Trees

The mod adds 13 new focus tree branches for major countries. These are implemented as **shared focuses** that attach to existing Millennium Dawn focus trees, appearing only when playing the 2026 bookmark.

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

### Germany (GER) — Zeitenwende

**Root**: `MD2026_GER_root` | **File**: `md2026_ger_focus.txt`

```
MD2026_GER_root
├── MD2026_GER_european_army → EU defense integration
├── MD2026_GER_energy_independence → renewable energy transition
└── MD2026_GER_eu_expansion → Ukraine/Moldova/Balkans accession
```

### India (RAJ) — Rising Power

**Root**: `MD2026_RAJ_root` | **File**: `md2026_raj_focus.txt`

```
MD2026_RAJ_root
├── MD2026_RAJ_make_in_india → industrial self-reliance
├── MD2026_RAJ_border_security → China/Pakistan border
├── MD2026_RAJ_space_program → ISRO expansion
└── MD2026_RAJ_strategic_autonomy → multi-alignment diplomacy
```

### Japan (JAP) — Normal Nation

**Root**: `MD2026_JAP_root` | **File**: `md2026_jap_focus.txt`

```
MD2026_JAP_root
├── MD2026_JAP_constitutional_reform → Article 9 revision
├── MD2026_JAP_indo_pacific → QUAD, regional security
├── MD2026_JAP_tech_leadership → semiconductor, robotics
└── MD2026_JAP_demographic_crisis → aging society solutions
```

### Turkey (TUR) — Regional Ambitions

**Root**: `MD2026_TUR_root` | **File**: `md2026_tur_focus.txt`

```
MD2026_TUR_root
├── MD2026_TUR_defense_industry → domestic arms production
├── MD2026_TUR_regional_influence → Syria, Libya, Caucasus
├── MD2026_TUR_energy_hub → gas transit, nuclear power
└── MD2026_TUR_bridge_role → NATO-Russia mediation
```

### Brazil (BRA) — Green Superpower

**Root**: `MD2026_BRA_root` | **File**: `md2026_bra_focus.txt`

```
MD2026_BRA_root
├── MD2026_BRA_amazon_guardian → environmental protection
├── MD2026_BRA_brics_leadership → BRICS presidency
├── MD2026_BRA_south_atlantic → naval presence
└── MD2026_BRA_industrial_policy → reindustrialization
```

### Israel (ISR) — Security First

**Root**: `MD2026_ISR_root` | **File**: `md2026_isr_focus.txt`

```
MD2026_ISR_root
├── MD2026_ISR_iron_wall → defense systems expansion
├── MD2026_ISR_normalization → Abraham Accords expansion
├── MD2026_ISR_tech_nation → cyber, AI, startup ecosystem
└── MD2026_ISR_iran_threat → counter-proliferation
```

### South Korea (KOR) — Democratic Resilience

**Root**: `MD2026_KOR_root` | **File**: `md2026_kor_focus.txt`

```
MD2026_KOR_root
├── MD2026_KOR_political_recovery → post-impeachment stability
├── MD2026_KOR_nk_policy → North Korea engagement/deterrence
├── MD2026_KOR_defense_buildup → KF-21, submarines
└── MD2026_KOR_tech_powerhouse → semiconductors, batteries
```

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
