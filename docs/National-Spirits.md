# National Spirits

The mod adds 45 national spirits (ideas) that reflect the geopolitical and domestic situations of major countries in January 2026.

---

## Base National Spirits (15)

Defined in `common/ideas/md2026_national_spirits.txt` and assigned in country history files.

| Spirit | Country | Effects | Description |
|--------|---------|---------|-------------|
| `md2026_western_sanctions` | SOV | -15% factory output, -30% trade, +10% war support | Western economic sanctions over Ukraine |
| `md2026_war_mobilization` | SOV | +5% conscription, -10% consumer goods, +15% army attack | Full wartime mobilization |
| `md2026_western_military_aid` | UKR | +20% lend-lease equipment, +10% org | NATO military assistance packages |
| `md2026_defensive_mobilization` | UKR | +3% conscription, +15% defense, -20% GDP growth | Total defensive mobilization |
| `md2026_political_polarization` | USA | -5% stability, -10% political power, +5% war support | Deep political divisions |
| `md2026_america_first` | USA | +10% consumer goods, -15% diplomatic influence | Isolationist economic policy |
| `md2026_economic_slowdown` | CHI | -5% GDP growth, -10% construction speed | Property crisis and demographic decline |
| `md2026_military_modernization` | CHI | +10% army/navy/air experience gain | PLA modernization program |
| `md2026_zeitenwende` | GER | +15% military spending effectiveness, -5% stability | Historic defense spending increase |
| `md2026_post_brexit` | ENG | -5% trade, +5% sovereignty | Post-Brexit trade reality |
| `md2026_wartime_governance` | ISR | +20% army defense, +10% war support, -15% stability | Post-Gaza security posture |
| `md2026_erdogan_autocracy` | TUR | +10% political power, -5% democratic drift, -10% stability | Consolidated executive power |
| `md2026_international_sanctions_per` | PER | -20% trade, -10% factory output | Nuclear-related sanctions |
| `md2026_total_isolation` | NKO | -50% trade, +5% conscription, +20% army attack | Hermit kingdom status |
| `md2026_eastern_shield` | POL | +15% fort construction, +10% army defense | NATO eastern flank buildup |

---

## Expansion National Spirits (22)

Added for additional countries in later implementation phases.

| Spirit | Country | Key Effects |
|--------|---------|-------------|
| `md2026_fra_strategic_autonomy` | FRA | +10% military factory construction, -5% consumer goods |
| `md2026_ita_coalition_politics` | ITA | -10% political power, +5% stability |
| `md2026_egy_economic_crisis` | EGY | -15% GDP growth, -10% stability, +5% war support |
| `md2026_pak_security_challenges` | PAK | +10% army defense, -10% stability, +5% conscription |
| `md2026_tai_silicon_shield` | TAI | +20% electronics, +15% computing tech bonus |
| `md2026_ast_aukus_partnership` | AST | +10% naval doctrine, +15% submarine research |
| `md2026_can_arctic_sovereignty` | CAN | +10% army defense (cold), +5% naval range |
| `md2026_spr_regional_tensions` | SPR | -5% stability, -5% political power |
| `md2026_fin_nato_integration` | FIN | +15% army org, +10% fort construction |
| `md2026_swe_nato_transition` | SWE | +10% military factory construction, +10% army org |
| `md2026_gre_eastern_med` | GRE | +10% naval attack, +5% war support |
| `md2026_rom_black_sea_security` | ROM | +10% army defense, +10% air detection |
| `md2026_brm_civil_war` | BRM | -30% stability, -20% factory output, +10% army attack |
| `md2026_syr_post_assad` | SYR | -25% stability, -30% factory output, +20% reconstruction |
| `md2026_saf_brics_host` | SAF | +10% political power, +5% trade |
| `md2026_kaz_multi_vector` | KAZ | +5% trade, +10% political power, -5% stability |
| `md2026_blr_russian_integration` | BLR | +10% army org, -15% sovereignty, +5% factory output |
| `md2026_geo_european_path` | GEO | -10% stability, +5% democratic drift |

---

## Focus Reward Spirits (8)

Granted by completing focus tree branches. Defined in `common/ideas/md2026_national_spirits.txt`.

| Spirit | Granted By | Effects |
|--------|-----------|---------|
| `md2026_usa_energy_dominance` | USA focus tree | +15% fuel, +10% resource gain |
| `md2026_sov_eastern_pivot` | Russia focus tree | +10% trade with Asia |
| `md2026_ukr_eu_integration` | Ukraine focus tree | +10% factory output, +5% stability |
| `md2026_chi_tech_supremacy` | China focus tree | +15% research speed |
| `md2026_ger_european_army` | Germany focus tree | +10% army org for allies |
| `md2026_raj_self_reliance` | India focus tree | +10% consumer goods efficiency |
| `md2026_jap_normal_nation` | Japan focus tree | +15% military factory construction |
| `md2026_tur_regional_power` | Turkey focus tree | +10% political power, +5% war support |

---

## Decision Reward Ideas (11)

Granted by completing decisions. Defined in `common/ideas/md2026_decision_ideas.txt`.

These provide temporary or permanent bonuses as rewards for completing strategic decisions (sanctions, military modernization, economic reforms, etc.). See the [Decisions](Decisions.md) page for details.

---

## Implementation Notes

- All spirit IDs use the `md2026_` prefix to avoid conflicts with base MD ideas
- Spirits are assigned in country history files via `add_ideas = { md2026_spirit_name }`
- Focus reward spirits use `add_ideas` in the focus completion effect
- Decision reward ideas are added/removed via decision complete effects
- Localisation for all spirits is in `localisation/english/md2026_l_english.yml`
