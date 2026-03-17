# Millennium Dawn 2026 Rework — Expansion Roadmap v2

## Stan wyjściowy (po fazie 1–6)

| Region | Kraj | Focusy | Eventy | AI |
|--------|------|--------|--------|----|
| **Europa** | ENG, GER, FRA, ITA, SPR, POL, TUR, UKR | 20–41 | ✓ | ✓ |
| **Europa** | ROM | 11 | ✓ | ✓ |
| **Europa** | Baltic (EST/LAT/LIT) | 10 | — | — |
| **Europa** | HUN, SWE, FIN, GRE, CZE, SRB, NET, NOR, DEN, BUL, POR, BEL | **0** | — | — |
| **Ameryka Płn.** | USA | 22 | ✓ | ✓ |
| **Ameryka Płn.** | CAN | 26 | ✓ | ✓ |
| **Ameryka Płn.** | MEX | 28 | — | ✓ |
| **Azja** | CHI, JAP, KOR, NKO, TAI, RAJ, PAK, IDN, VIN, AUS | 20–26 | ✓ | ✓ |
| **Azja** | PHI, THA, MAL | **0** | — | — |

Fazy 1–6 zakończone: naprawy crashu, lokalizacja, eventy (12 łańcuchów), decyzje (56),
focus trees dla PAK/ARG/MEX/SAF/VIN/IDN, systemy gameplay (proxy/cyber/ekonomia),
plany AI dla 6 krajów, newspaper events, alternatywne bookmarki.

---

## FAZA A: Rozbudowa drzewek głównych mocarstw

**Priorytet: KRYTYCZNY** — USA (22), CHI (20), SOV (20), UKR (20) mają za mało focusów dla krajów tej rangi.

### A.1 USA (22 → 42 focusów)

Istniejące gałęzie: Trump 2. kadencja, DOGE, tarify, energia, NATO, Ukraina, terytoria.

**Nowe gałęzie:**

| Gałąź | Nowe focusy | Tematyka |
|-------|------------|----------|
| Domestic Economy | `usa_reindustrialize`, `usa_chips_act_2`, `usa_ai_frontier`, `usa_infrastructure_2` | reindustrializacja, AI |
| Military Buildup | `usa_reagan_buildup_2`, `usa_sixth_gen_fighter`, `usa_navy_600_ships`, `usa_space_force_ops` | F-47, flota, Space Force |
| Americas Hegemony | `usa_greenland_annexation`, `usa_canada_pressure`, `usa_panama_reclaim`, `usa_monroe_2` | Grenlandia, Panama, Kanada |
| Democracy Crisis | `usa_restore_institutions`, `usa_supreme_court_reform`, `usa_digital_authoritarianism` (XOR) | polaryzacja |

**Plik:** `common/national_focus/md2026_usa_focus.txt` (rozszerzenie)

---

### A.2 CHI (20 → 38 focusów)

Istniejące: wielkie odrodzenie, kwestia tajwańska, dominacja tech, ekspansja morska.

**Nowe gałęzie:**

| Gałąź | Nowe focusy | Tematyka |
|-------|------------|----------|
| Internal Control | `chi_common_prosperity_2`, `chi_ai_surveillance`, `chi_social_credit_2`, `chi_xinjiang_final` | kontrola wewnętrzna |
| Economic Decoupling | `chi_yuan_internationalization`, `chi_rare_earth_weapon`, `chi_domestic_consumption`, `chi_bri_2` | oderwanie od Zachodu |
| Military Modernization | `chi_j20_expansion`, `chi_hypersonic_2`, `chi_carrier_fleet_2`, `chi_pla_reform` | zbrojenia |
| Global South | `chi_brics_chair`, `chi_africa_pivot_2`, `chi_global_south_leader`, `chi_russia_alignment` | dyplomacja |

**Plik:** `common/national_focus/md2026_chi_focus.txt` (rozszerzenie)

---

### A.3 SOV (20 → 38 focusów)

Istniejące: punkt zwrotny w wojnie, wschodnia oś, autarkia ekonomiczna.

**Nowe gałęzie:**

| Gałąź | Nowe focusy | Tematyka |
|-------|------------|----------|
| War Escalation | `sov_total_mobilization`, `sov_nuclear_posturing_2`, `sov_missile_campaign`, `sov_belarusian_integration` | eskalacja |
| Frozen Conflict | `sov_ceasefire_terms`, `sov_new_minsk`, `sov_rebuild_army` | zamrożenie |
| Domestic Power | `sov_siloviki_purge`, `sov_succession_crisis`, `sov_patriotic_mobilization` (XOR) | polityka wewnętrzna |
| War Economy | `sov_war_economy_2`, `sov_china_energy_deal_2`, `sov_arctic_resources`, `sov_import_substitution` | gospodarka wojenna |

**Plik:** `common/national_focus/md2026_sov_focus.txt` (rozszerzenie)

---

### A.4 UKR (20 → 36 focusów)

Istniejące: ścieżka wojenna, zachodnia broń, przemysł obronny.

**Nowe gałęzie:**

| Gałąź | Nowe focusy | Tematyka |
|-------|------------|----------|
| NATO/EU Path | `ukr_nato_membership`, `ukr_article5_bid`, `ukr_eu_accession`, `ukr_security_guarantee` | integracja zachodnia |
| Military Doctrine | `ukr_drone_army`, `ukr_territorial_defense_2`, `ukr_counteroffensive`, `ukr_crimea_operation` | doktryna wojskowa |
| Reconstruction | `ukr_marshall_plan`, `ukr_diaspora_return`, `ukr_digital_gov_2`, `ukr_energy_rebuild` | odbudowa |
| Peace Scenarios | `ukr_ceasefire_terms`, `ukr_frozen_peace`, `ukr_territorial_concession` (XOR) | pokój |

**Plik:** `common/national_focus/md2026_ukr_focus.txt` (rozszerzenie)

---

## FAZA B: Nowe drzewka europejskie — Tier 1 (priorytetowe)

### B.1 Węgry (HUN) — 28 focusów [NOWY]

**Kontekst 2026:** Orbán balansuje między UE a Moskwą/Pekinem. Weto sankcji, PAKS2, Fudan, spór o praworządność, art. 7.

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `hun_orban_mandate` | 5. kadencja Orbána |
| EU Conflict | `hun_eu_confrontation`, `hun_article7_crisis`, `hun_exit_threat` XOR `hun_eu_reform` | konfrontacja z UE |
| Russia-Energy | `hun_energy_dependency`, `hun_paks2_nuclear`, `hun_russia_appeasement`, `hun_strategic_neutrality` | gaz rosyjski, Paks2 |
| China Pivot | `hun_bri_hub`, `hun_fudan_university`, `hun_chinese_ev_factory`, `hun_eastern_opening` | chiński pivot |
| Domestic | `hun_illiberal_democracy`, `hun_media_control`, `hun_migration_fence`, `hun_constitution_reform` | polityka wewnętrzna |
| Military | `hun_nato_obligation`, `hun_gripen_upgrade`, `hun_home_defense` | armia |
| Capstone | `hun_sovereignist_model` XOR `hun_european_return` | |

**Plik:** `common/national_focus/md2026_hun_focus.txt`

---

### B.2 Szwecja (SWE) — 26 focusów [NOWY]

**Kontekst 2026:** Nowy członek NATO (2024), remilitaryzacja, kryzys gangów, Gripen E, Saab.

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `swe_nato_integration` | integracja z NATO |
| Defense | `swe_gripen_e_expand`, `swe_total_defense`, `swe_conscription_return`, `swe_nordic_brigade` | obrona |
| Economy | `swe_innovation_hub`, `swe_green_steel`, `swe_fintech`, `swe_saab_defense_contracts` | gospodarka |
| Society | `swe_gang_crisis`, `swe_integration_policy`, `swe_welfare_reform`, `swe_center_right_govt` | społeczeństwo |
| Foreign | `swe_nordic_defense_pact`, `swe_baltic_sea_command`, `swe_eu_solidarity`, `swe_atlanticism` | zagraniczna |
| Capstone | `swe_northern_pillar` | |

**Plik:** `common/national_focus/md2026_swe_focus.txt`

---

### B.3 Finlandia (FIN) — 26 focusów [NOWY]

**Kontekst 2026:** 1340 km granicy z Rosją w NATO, fortyfikacje, F-35, artyleria rezerwowa, kwestia Karelii.

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `fin_nato_eastern_pillar` | wschodnia flanka NATO |
| Defense | `fin_fortress_finland`, `fin_artillery_reserve`, `fin_f35_fleet`, `fin_border_fortification` | obrona |
| Russia Policy | `fin_karelia_question`, `fin_border_militarization`, `fin_russia_sanctions`, `fin_historical_reckoning` | relacje z Rosją |
| Economy | `fin_tech_renaissance`, `fin_nokia_revival`, `fin_green_mining`, `fin_gaming_industry` | gospodarka |
| Nordic Coop | `fin_nordic_defense_coord`, `fin_swe_joint_command`, `fin_baltic_security` | nordycka |
| Capstone | `fin_northern_sentinel` | |

**Plik:** `common/national_focus/md2026_fin_focus.txt`

---

### B.4 Grecja (GRE) — 26 focusów [NOWY]

**Kontekst 2026:** Napięcia z Turcją (Morze Egejskie, Cypr), zakup F-35, LNG hub, rola NATO na Wschodzie.

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `gre_eastern_nato_anchor` | kotwica wschodnia NATO |
| Turkey Rivalry | `gre_aegean_sovereignty`, `gre_f35_response`, `gre_cyprus_reunification`, `gre_aegean_incident` | Grecja-Turcja |
| Military | `gre_f35_acquisition`, `gre_navy_expansion`, `gre_aegean_fortification`, `gre_special_forces` | wojsko |
| Economy | `gre_tourism_dominance`, `gre_lng_hub`, `gre_shipping_power`, `gre_digital_revival` | gospodarka |
| Diplomacy | `gre_israel_partnership`, `gre_egypt_alignment`, `gre_eu_solidarity`, `gre_balkan_stability` | dyplomacja |
| Capstone | `gre_aegean_hegemon` | |

**Plik:** `common/national_focus/md2026_gre_focus.txt`

---

### B.5 Serbia (SRB) — 24 focusy [NOWY]

**Kontekst 2026:** Vučić balansuje Wschód-Zachód, Kosowo (odmowa uznania), kandydat UE bez postępów, rosyjski gaz, chiskie inwestycje.

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `srb_vucic_mandate` | |
| Kosovo | `srb_kosovo_pressure`, `srb_northern_kosovo`, `srb_recognition_no` XOR `srb_recognition_yes` | Kosowo |
| EU Path | `srb_eu_accession_push`, `srb_rule_of_law`, `srb_sanctions_compliance` XOR `srb_eu_rejection` | UE |
| Eastern Vector | `srb_russia_energy`, `srb_chinese_investment`, `srb_bri_corridors`, `srb_eastern_pivot` | Rosja-Chiny |
| Military | `srb_armed_neutrality`, `srb_army_modernization`, `srb_chinese_weapons` | wojsko |
| Capstone | `srb_regional_broker` XOR `srb_eu_member` | |

**Plik:** `common/national_focus/md2026_srb_focus.txt`

---

### B.6 Czechy (CZE) — 24 focusy [NOWY]

**Kontekst 2026:** Centrum produkcji broni dla Ukrainy, Fiala, NATO hub Europy Środkowej, F-35, przemysł zbrojeniowy.

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `cze_central_europe_anchor` | |
| Defense Industry | `cze_arms_exports`, `cze_ukraine_arsenal`, `cze_nato_production_hub`, `cze_ammunition_surge` | zbrojenia |
| Economy | `cze_automotive_transition`, `cze_ev_manufacturing`, `cze_tech_corridor`, `cze_energy_independence` | gospodarka |
| Military | `cze_f35_acquisition`, `cze_army_modernization`, `cze_v4_defense` | wojsko |
| Diplomacy | `cze_transatlantic_bridge`, `cze_v4_leadership`, `cze_ukraine_solidarity` | dyplomacja |
| Capstone | `cze_arsenal_of_europe` | |

**Plik:** `common/national_focus/md2026_cze_focus.txt`

---

## FAZA C: Nowe drzewka europejskie — Tier 2

### C.1 Rumunia (ROM) — rozszerzenie 11 → 28 focusów

**Kontekst 2026:** NATO wschodnia flanka (bazy USA, Aegis Ashore), granica z Ukrainą, tranzyt broni, gaz offshore, aspiracje Mołdawii.

| Nowe gałęzie | Focusy | Tematyka |
|--------------|--------|----------|
| NATO Frontline | `rom_nato_hub`, `rom_us_forces`, `rom_aegis_ashore_2`, `rom_black_sea_command` | NATO |
| Moldova | `rom_moldova_integration`, `rom_moldova_eu_bridge`, `rom_reunification_debate` | Mołdawia |
| Economy | `rom_offshore_gas`, `rom_ev_hub`, `rom_it_sector`, `rom_energy_independence` | gospodarka |
| Military | `rom_f16_fleet`, `rom_army_expansion`, `rom_patriot_2` | wojsko |
| Capstone | `rom_black_sea_guardian` | |

**Plik:** `common/national_focus/md2026_rom_focus.txt` (rozszerzenie)

---

### C.2 Holandia (NET) — 26 focusów [NOWY]

**Kontekst 2026:** ASML (monopol na EUV, kluczowy dla chipy), rząd Wildersa, presja USA/CHI o eksport technologii, Rotterdam hub.

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `net_wilders_coalition` | prawicowy rząd |
| Tech Sovereignty | `net_asml_strategy`, `net_chip_export_china`, `net_silicon_sovereignty`, `net_us_tech_alliance` | ASML i chipy |
| Migration | `net_border_control`, `net_asylum_reform`, `net_eu_migration_pact`, `net_integration_crisis` | migracja |
| Economy | `net_port_rotterdam`, `net_fintech_hub`, `net_eu_budget_hawk`, `net_green_port` | gospodarka |
| Military | `net_nato_commitment`, `net_f35_expansion`, `net_navy_modernization` | wojsko |
| Capstone | `net_silicon_republic` XOR `net_atlantic_hub` | |

**Plik:** `common/national_focus/md2026_net_focus.txt`

---

### C.3 Norwegia (NOR) — 22 focusy [NOWY]

**Kontekst 2026:** Największy eksporter gazu do Europy po sankcjach na Rosję, SWF $1.7 bln, NATO arktyka, Svalbard.

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `nor_energy_hegemon` | |
| Energy | `nor_gas_europe`, `nor_sovereign_fund`, `nor_oil_production`, `nor_renewable_transition` | energia |
| Arctic | `nor_svalbard_sovereignty`, `nor_arctic_nato`, `nor_russia_border`, `nor_northern_command` | arktyka |
| Military | `nor_f35_fleet`, `nor_naval_modernization`, `nor_special_forces` | wojsko |
| Diplomacy | `nor_nordic_solidarity`, `nor_mediator_role`, `nor_ukraine_fund` | dyplomacja |
| Capstone | `nor_arctic_guardian` | |

**Plik:** `common/national_focus/md2026_nor_focus.txt`

---

### C.4 Dania (DEN) — 22 focusy [NOWY]

**Kontekst 2026:** Trump żąda Grenlandii (styczeń 2025), Dania odmawia, wzrost wydatków wojskowych, obrona Bałtyku.

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `den_greenland_crisis` | kryzys grenlandzki |
| Greenland | `den_greenland_sovereignty`, `den_greenland_autonomy_expand`, `den_us_concession` (XOR) | Grenlandia |
| Defense | `den_defense_buildup`, `den_f35_fleet`, `den_baltic_command`, `den_nato_commitment` | obrona |
| Economy | `den_green_energy_export`, `den_maersk_logistics`, `den_tech_hub`, `den_arctic_resources` | gospodarka |
| Diplomacy | `den_nordic_anchor`, `den_us_relations`, `den_eu_solidarity` | dyplomacja |
| Capstone | `den_northern_guardian` | |

**Plik:** `common/national_focus/md2026_den_focus.txt`

---

## FAZA D: Nowe drzewka azjatyckie

### D.1 Filipiny (PHI) — 26 focusów [NOWY]

**Kontekst 2026:** Marcos Jr., Scarborough Shoal, BrahMos z Indii, bazy USA (EDCA rozszerzenie), gospodarka BPO.

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `phi_marcos_mandate` | |
| South China Sea | `phi_scarborough_defiance`, `phi_scs_arbitration`, `phi_us_alliance_deepen`, `phi_brahmos_deploy` | SCS |
| Military | `phi_modernization_program`, `phi_us_basing_expand`, `phi_coast_guard_2`, `phi_navy_buildup` | wojsko |
| Economy | `phi_bpo_expansion`, `phi_ofw_remittances`, `phi_semiconductor_assembly`, `phi_tourism_revival` | gospodarka |
| Diplomacy | `phi_us_strategic_partner` XOR `phi_asean_balancer`, `phi_japan_partnership`, `phi_china_econ_ties` | dyplomacja |
| Capstone | `phi_pearl_of_orient` | |

**Plik:** `common/national_focus/md2026_phi_focus.txt`

---

### D.2 Tajlandia (THA) — 22 focusy [NOWY]

**Kontekst 2026:** Pierwszy cywilny rząd od lat (Paetongtarn Shinawatra), napięcia armia-cywile, hub EV (Tesla, BYD), ASEAN.

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `tha_democratic_transition` | |
| Civil-Military | `tha_civilian_supremacy`, `tha_army_reform` XOR `tha_military_coup` | napięcia |
| Economy | `tha_ev_hub`, `tha_tourism_revival`, `tha_digital_economy`, `tha_supply_chain_hub` | gospodarka |
| Diplomacy | `tha_bamboo_diplomacy`, `tha_asean_hub`, `tha_us_treaty_ally`, `tha_china_balance` | dyplomacja |
| Military | `tha_modernization`, `tha_regional_security` | wojsko |
| Capstone | `tha_asean_power` | |

**Plik:** `common/national_focus/md2026_tha_focus.txt`

---

### D.3 Malezja (MAL) — 22 focusy [NOWY]

**Kontekst 2026:** Anwar Ibrahim reformy, ASEAN chair 2025, duże LNG, SCS roszczenia, chip packaging hub (back-end semiconductor).

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Root | `mal_anwar_reform` | |
| Economy | `mal_semiconductor_packaging`, `mal_lng_expansion`, `mal_digital_economy`, `mal_halal_hub` | gospodarka |
| South China Sea | `mal_scs_joint_dev`, `mal_china_negotiation`, `mal_asean_solidarity` | SCS |
| Diplomacy | `mal_asean_leadership`, `mal_neutrality_policy`, `mal_ummah_diplomacy`, `mal_global_south` | dyplomacja |
| Military | `mal_maritime_defense`, `mal_modernization`, `mal_five_powers_pact` | wojsko |
| Capstone | `mal_emerging_tiger` | |

**Plik:** `common/national_focus/md2026_mal_focus.txt`

---

## FAZA E: Rozszerzenie Ameryki Północnej

### E.1 USA — patrz Faza A.1

### E.2 Kanada (CAN) — uzupełnienie gałęzi

**Nowe focusy** do istniejącego drzewka 26-focusowego:

| Gałąź | Focusy | Tematyka |
|-------|--------|----------|
| Trump Crisis | `can_trump_tariffs_response`, `can_51st_state_rejection`, `can_economic_diversification`, `can_tpp_pivot` | kryzys z USA |
| Arctic Sovereignty | `can_arctic_sovereignty`, `can_norad_upgrade`, `can_northern_gateway`, `can_greenland_diplomacy` | arktyka |

**Plik:** `common/national_focus/md2026_can_focus.txt` (uzupełnienie)

---

## FAZA F: Eventy regionalne

### F.1 Europa (6 łańcuchów, ~35 eventów)

| Łańcuch | Plik | Treść |
|---------|------|-------|
| Kryzys praworządności UE | `events/md2026_eu_rule_of_law.txt` | HUN/POL vs UE, art. 7, sankcje, wyjście |
| Rozszerzenie NATO/UE | `events/md2026_nato_expansion.txt` | Serbia/Ukraina/Georgia aplikują, negocjacje |
| Europejska energetyka | `events/md2026_europe_energy.txt` | LNG kontrakt, atom, odnawialne, kryzys gazu |
| Kryzys egejski | `events/md2026_aegean_crisis.txt` | incydenty lotnicze GRE-TUR, Cypr, Morze Egejskie |
| Nordycka obronność | `events/md2026_nordic_defense.txt` | joint command, ćwiczenia, rosyjskie prowokacje |
| Wschodnia flanka | `events/md2026_eastern_flank.txt` | przesunięcia NATO, Kaliningrad, incydenty |

### F.2 Azja (4 łańcuchy, ~24 eventy)

| Łańcuch | Plik | Treść |
|---------|------|-------|
| ASEAN vs Chiny (SCS) | `events/md2026_asean_scs.txt` | SCS incydenty, mediacje ASEAN, arbitraż |
| Półwysep Koreański | `events/md2026_korea_crisis.txt` | NKO testy, szczyt inter-koreański, presja USA |
| Polityka USA w Azji | `events/md2026_asia_pivot.txt` | QUAD, AUKUS, bazy Filipiny |
| Wybory azjatyckie | rozszerzenie `events/md2026_elections_extended.txt` | PHI, THA, MAL |

### F.3 Ameryka Północna (3 łańcuchy, ~18 eventów)

| Łańcuch | Plik | Treść |
|---------|------|-------|
| Grenlandia | `events/md2026_greenland.txt` | USA-Dania, autonomia, referendum |
| Kryzys USMCA | `events/md2026_usmca_crisis.txt` | tarify, renegocjacja, Meksyk-Kanada vs USA |
| Granica USA-Meksyk | `events/md2026_border_crisis.txt` | migracja, kartele, militaryzacja |

---

## FAZA G: AI i balans dla nowych krajów

Dla każdego nowego drzewka (HUN, SWE, FIN, GRE, SRB, CZE, ROM, NET, NOR, DEN, PHI, THA, MAL + rozszerzone USA/CHI/SOV/UKR/CAN):
- 2 AI plany z focusami (ścieżka historyczna + alternatywa)
- Strategia dyplomatyczna (befriend/antagonize/area_priority)
- Strategia wojskowa (role_ratio + air_factory_balance)

**Plik:** rozszerzenie `md2026_ai_plans.txt` + `md2026_ai_strategies.txt`

---

## Kolejność implementacji

```
A (mocarstwa) → B (Europa tier-1) → C (Europa tier-2) → D (Azja) → E (Ameryka) → F (eventy) → G (AI)
```

| Faza | Nowe focusy | Nowe eventy | AI planów |
|------|------------|------------|----------|
| A | ~72 (4×18) | — | — |
| B | ~155 (6 drzewka) | — | — |
| C | ~96 (4 drzewka) | — | — |
| D | ~70 (3 drzewka) | — | — |
| E | ~22 (USA+CAN) | — | — |
| F | — | ~77 eventów | — |
| G | — | — | ~26 planów |
| **Razem** | **~415** | **~77** | **~26** |

---

## Weryfikacja po każdej fazie

1. Sprawdzić brace matching w nowych plikach (`{}` parowane)
2. Sprawdzić czy wszystkie nowe tokeny mają lokalizację w `localisation/english/`
3. Sprawdzić `allow_branch`: każdy shared_focus musi mieć `original_tag = XXX` + `has_global_flag = md2026_initialized`
4. Przetestować w grze: bookmark ładuje się, focusy widoczne, AI działa (observe 5 lat)
5. Sprawdzić konflikty x/y z istniejącymi focusami base modu
