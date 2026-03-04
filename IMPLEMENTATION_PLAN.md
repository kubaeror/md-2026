# MD2026 — Millennium Dawn 2026 Rework

Submod do Millennium Dawn (Steam Workshop ID: 2777392649) dodający bookmark startowy 1 stycznia 2026.

---

## Spis treści

1. [Struktura plików](#struktura-plików)
2. [on_actions — inicjalizacja i hooki](#1-on_actions--inicjalizacja-i-hooki)
3. [Scripted triggers](#2-scripted-triggers)
4. [National spirits](#3-national-spirits)
5. [Decision categories i decyzje](#4-decision-categories-i-decyzje)
6. [Decision reward ideas](#5-decision-reward-ideas)
7. [Opinion modifiers](#6-opinion-modifiers)
8. [Focus trees (23 kraje)](#7-focus-trees-23-kraje)
9. [Eventy — system](#8-eventy--system)
10. [Eventy — NATO Article 5](#9-eventy--nato-article-5)
11. [Eventy — wybory](#10-eventy--wybory)
12. [Eventy — random](#11-eventy--random)
13. [Lokalizacja](#12-lokalizacja)
14. [Konwencje nazewnicze](#konwencje-nazewnicze)
15. [Znane ograniczenia i TODO](#znane-ograniczenia-i-todo)

---

## Struktura plików

```
md-2026/
├── descriptor.mod
├── thumbnail.png
├── IMPLEMENTATION_PLAN.md              # ten plik
├── loc_audit.py                        # skrypt do audytu lokalizacji
│
├── common/
│   ├── bookmarks/
│   │   └── md2026_bookmark.txt         # bookmark 2026.1.1
│   ├── countries/                      # kolory i tagi
│   ├── country_tags/
│   ├── decisions/
│   │   ├── categories/
│   │   │   └── md2026_decision_categories.txt   # 7 kategorii (141 linii)
│   │   └── md2026_decisions.txt                 # ~45 decyzji (2123 linii)
│   ├── ideas/
│   │   ├── md2026_national_spirits.txt          # ~58 spiritów (1098 linii)
│   │   └── md2026_decision_ideas.txt            # ~31 idea rewardów (342 linii)
│   ├── national_focus/
│   │   ├── md2026_usa_focus.txt
│   │   ├── md2026_sov_focus.txt
│   │   ├── md2026_ukr_focus.txt
│   │   ├── md2026_chi_focus.txt
│   │   ├── md2026_ger_focus.txt
│   │   ├── md2026_eng_focus.txt
│   │   ├── md2026_fra_focus.txt
│   │   ├── md2026_jap_focus.txt
│   │   ├── md2026_kor_focus.txt
│   │   ├── md2026_raj_focus.txt
│   │   ├── md2026_tur_focus.txt
│   │   ├── md2026_isr_focus.txt
│   │   ├── md2026_pol_focus.txt
│   │   ├── md2026_bra_focus.txt
│   │   ├── md2026_sau_focus.txt
│   │   ├── md2026_tai_focus.txt
│   │   ├── md2026_per_focus.txt
│   │   ├── md2026_nko_focus.txt
│   │   ├── md2026_ita_focus.txt
│   │   ├── md2026_ast_focus.txt
│   │   ├── md2026_can_focus.txt
│   │   ├── md2026_syr_focus.txt
│   │   └── md2026_egy_focus.txt        # 23 drzewek fokusów
│   ├── on_actions/
│   │   └── md2026_on_actions.txt                # hooki (267 linii)
│   ├── opinion_modifiers/
│   │   └── md2026_opinion_modifiers.txt         # ~36 modyfikatorów (202 linii)
│   └── scripted_triggers/
│       └── md2026_triggers.txt                  # 6 triggerów (150 linii)
│
├── events/
│   ├── md2026_ru_ukr.txt               # eventy Rosja-Ukraina
│   ├── md2026_taiwan.txt               # eventy Tajwan
│   ├── md2026_mideast.txt              # eventy Bliski Wschód
│   ├── md2026_brics.txt                # eventy BRICS
│   ├── md2026_nato_russia.txt          # eventy NATO-Rosja
│   ├── md2026_migration.txt            # eventy migracyjne
│   ├── md2026_climate.txt              # eventy klimatyczne
│   ├── md2026_tech.txt                 # eventy technologiczne
│   ├── md2026_demographics.txt         # eventy demograficzne
│   ├── md2026_space.txt                # eventy kosmiczne
│   ├── md2026_elections.txt            # 10 eventów wyborczych (1024 linii)
│   ├── md2026_system.txt               # 3 eventy systemowe (142 linii)
│   ├── md2026_nato_article5.txt        # 3 eventy Art.5 (209 linii)
│   └── md2026_random_events.txt        # 8 eventów losowych (398 linii)
│
├── history/
│   ├── countries/                      # historia 66+ krajów (liderzy, spirity, polityka, PP, stab)
│   ├── states/                         # stany (budynki, zasoby, VP)
│   └── units/                          # OOB
│
└── localisation/
    └── english/
        └── md2026_l_english.yml        # pełna lokalizacja EN (1918 linii)
```

---

## 1. on_actions — inicjalizacja i hooki

**Plik:** `common/on_actions/md2026_on_actions.txt` (267 linii)

| Hook | Funkcja |
|---|---|
| `on_startup` | Ustawienie `md2026_initialized`, flagowanie NATO/BRICS/nuclear members, intro news event (`md2026_system.1`) |
| `on_monthly` | War exhaustion tick (SOV/UKR w stanie wojny >12 mies.), sprawdzanie eskalacji sankcji |
| `on_peace` | Usuwanie war exhaustion, dodawanie `md2026_reconstruction_effort`, resetowanie flag Article 5 |
| `on_declare_war` | NATO Article 5 check — jeśli cel ma `md2026_nato_member`, fire event do USA |
| `on_government_change` | Usuwanie/dodawanie spiritów zależnych od ideologii (np. `md2026_hun_illiberal_democracy`) |

---

## 2. Scripted triggers

**Plik:** `common/scripted_triggers/md2026_triggers.txt` (150 linii)

| Trigger | Opis |
|---|---|
| `md2026_is_active` | `has_global_flag = md2026_initialized` |
| `md2026_is_nato_member` | Lista krajów NATO (USA, ENG, FRA, GER, POL, ITA, CAN, TUR, ...) |
| `md2026_is_brics_member` | SOV, CHI, RAJ, BRA, SAU, UAE, EGY, ETH, PER |
| `md2026_is_western_democracy` | `has_government = democratic` + faction z USA |
| `md2026_is_authoritarian` | `has_government = communism/nationalist/fascism` |
| `md2026_is_nuclear_power` | USA, SOV, CHI, FRA, ENG, RAJ, PAK, ISR, NKO + flag `md2026_nuclear_power` |

---

## 3. National spirits

**Plik:** `common/ideas/md2026_national_spirits.txt` (1098 linii, ~58 spiritów)

### Spirity krajowe (przypisywane w history/on_startup)

| Spirit | Kraj | Opis |
|---|---|---|
| `md2026_usa_polarization` | USA | Polaryzacja polityczna |
| `md2026_sov_western_sanctions` | SOV | Zachodnie sankcje |
| `md2026_sov_war_mobilization` | SOV | Mobilizacja wojenna |
| `md2026_sov_shadow_economy` | SOV | Szara strefa gospodarcza |
| `md2026_ukr_russian_invasion` | UKR | Rosyjska inwazja |
| `md2026_chi_common_prosperity` | CHI | Wspólny dobrobyt |
| `md2026_ger_zeitenwende` | GER | Zwrot w polityce obronnej |
| `md2026_eng_post_brexit` | ENG | Post-Brexit |
| `md2026_fra_social_unrest` | FRA | Niepokoje społeczne |
| `md2026_jap_demographic_crisis` | JAP | Kryzys demograficzny |
| `md2026_kor_political_crisis` | KOR | Kryzys polityczny (stan wojenny 2024) |
| `md2026_raj_hindu_nationalism` | RAJ | Nacjonalizm hinduistyczny |
| `md2026_raj_digital_india` | RAJ | Cyfrowa India |
| `md2026_tur_regional_power` | TUR | Turecka potęga regionalna |
| `md2026_isr_security_state` | ISR | Państwo bezpieczeństwa |
| `md2026_pol_frontline_state` | POL | Państwo frontowe NATO |
| `md2026_bra_lula_return` | BRA | Powrót Luli |
| `md2026_sau_vision_2030` | SAU | Wizja 2030 |
| `md2026_tai_silicon_shield` | TAI | Tarcza krzemowa |
| `md2026_per_axis_of_resistance` | PER | Oś oporu |
| `md2026_nko_juche_ideology` | NKO | Ideologia Juche |
| `md2026_ita_right_wing_government` | ITA | Prawicowy rząd |
| `md2026_ast_aukus_member` | AST | Członek AUKUS |
| `md2026_can_nato_commitment` | CAN | Zobowiązania NATO |
| `md2026_syr_post_civil_war` | SYR | Po wojnie domowej |
| `md2026_egy_military_government` | EGY | Rząd wojskowy |
| `md2026_sud_civil_war` | SUD | Wojna domowa |
| `md2026_yem_houthi_division` | YEM | Podział Houthi |
| `md2026_eth_post_tigray` | ETH | Po wojnie w Tigraju |
| `md2026_uae_economic_diversification` | UAE | Dywersyfikacja gospodarcza |
| `md2026_hun_illiberal_democracy` | HUN | Nieliberalna demokracja |
| `md2026_geo_eu_candidate` | GEO | Kandydat do UE |

### Spirity z enrichmentu drzewek fokusów

| Spirit | Kraj | Opis |
|---|---|---|
| `md2026_usa_labor_shortage` | USA | Niedobór siły roboczej |
| `md2026_usa_trade_war_tariffs` | USA | Taryfy celne |
| `md2026_sov_war_economy` | SOV | Gospodarka wojenna |
| `md2026_sov_sanctions_evasion` | SOV | Obchodzenie sankcji |
| `md2026_ukr_resistance` | UKR | Opór narodowy |
| `md2026_ukr_nato_candidate` | UKR | Kandydatura NATO |
| `md2026_chi_national_rejuvenation` | CHI | Odrodzenie narodowe |
| `md2026_chi_tech_self_reliance` | CHI | Samowystarczalność technologiczna |

### Spirity systemowe

| Spirit | Opis |
|---|---|
| `md2026_war_exhaustion_1` | Zmęczenie wojną (lekkie) |
| `md2026_war_exhaustion_2` | Zmęczenie wojną (poważne) |
| `md2026_war_exhaustion_3` | Zmęczenie wojną (krytyczne) |
| `md2026_nuclear_deterrent` | Odstraszanie jądrowe |
| `md2026_nato_article5_active` | Artykuł 5 NATO aktywny |
| `md2026_sanctions_tier_mild` | Sankcje łagodne |
| `md2026_sanctions_tier_moderate` | Sankcje umiarkowane |
| `md2026_sanctions_tier_severe` | Sankcje poważne |
| `md2026_sanctions_tier_total` | Sankcje totalne |
| `md2026_reconstruction_effort` | Odbudowa powojenno |
| `md2026_brics_development_bank` | Bank Rozwoju BRICS |

---

## 4. Decision categories i decyzje

### Kategorie

**Plik:** `common/decisions/categories/md2026_decision_categories.txt` (141 linii, 7 kategorii)

| Kategoria | Widoczność | Opis |
|---|---|---|
| `md2026_sanctions_category` | Zachodnie demokracje | Sankcje i restrykcje handlowe |
| `md2026_nato_category` | Członkowie NATO | Decyzje sojusznicze |
| `md2026_geopolitics_category` | Wszyscy | Ogólne geopolityczne |
| `md2026_military_modernization_category` | Wszyscy | Modernizacja wojskowa |
| `md2026_economic_category` | Wszyscy | Gospodarka |
| `md2026_internal_politics_category` | Wszyscy | Polityka wewnętrzna |
| `md2026_nuclear_category` | Mocarstwa jądrowe | Programy nuklearne |

### Decyzje

**Plik:** `common/decisions/md2026_decisions.txt` (2123 linii, ~45 decyzji)

#### Sankcje i NATO (oryginalne, linie 1-1219)
- Sankcje wobec Rosji, sankcje wobec Iranu, liftowanie sankcji
- Dostawy broni dla Ukrainy, szkolenia NATO, ćwiczenia
- Fortyfikacja granic, obrona cyberprzestrzeni
- Modernizacja armii, lotnictwa, marynarki
- Programy ekonomiczne

#### Polityka wewnętrzna (linie 1220-1966)

| Decyzja | Kraj | Efekt |
|---|---|---|
| `md2026_sov_war_economy` | SOV | Timed idea: gospodarka wojenna (+15% prod. fabryk zbrojeniowych, -10% consumer goods) |
| `md2026_sov_information_control` | SOV | Permanent idea: kontrola informacji (+5% stab, +10% war support) |
| `md2026_sov_shadow_fleet_sales` | SOV | Timed idea: shadow fleet (+5% industrial capacity, -10% trade opinion) |
| `md2026_sov_partial_mobilization` | SOV | Permanent idea: mobilizacja (+2% conscription, +300k manpower, -8% stab) |
| `md2026_chi_belt_road_expansion` | CHI | Timed idea: BRI (+10% trade opinion, +5% build speed) |
| `md2026_chi_taiwan_pressure` | CHI | Timed idea: presja na Tajwan (+5% attack, +10% war support, opinion z TAI/USA/JAP) |
| `md2026_chi_tech_self_sufficiency` | CHI | Permanent idea: tech (+5% research, +5% efficiency) + tech bonus computing |
| `md2026_raj_make_in_india` | RAJ | Timed idea: Make in India (+10% prod. civ, +5% mil) + 1 fabryka |
| `md2026_raj_border_standoff` | RAJ | Timed idea: standoff (+10% defence, +5% war support) |
| `md2026_raj_space_program` | RAJ | Permanent idea: ISRO (+5% research, +5% PP) + tech bonus |
| `md2026_nko_nuclear_test` | NKO | Timed idea: test (+15% war support, -20% trade) + opinion kary |
| `md2026_nko_missile_provocation` | NKO | Timed idea: prowokacja (+5% attack, +10% war support) |
| `md2026_nko_diplomatic_outreach` | NKO | Poprawa opinii z KOR/USA/CHI |
| `md2026_per_proxy_warfare` | PER | Timed idea: proxy (+5% attack, -5% stab) + opinion z ISR/SAU/USA |
| `md2026_per_nuclear_acceleration` | PER | Permanent idea: program nuklearny + flag `md2026_nuclear_power` |
| `md2026_sau_vision_acceleration` | SAU | Permanent idea: przyspieszenie Vision 2030 (+15% build speed) + 2 fabryki |
| `md2026_sau_normalize_israel` | SAU | Normalizacja stosunków z Izraelem — opinion bonusy ISR/USA, kara PER |

#### Decyzje nuklearne (linie 1968-2123)

| Decyzja | Warunek | Efekt |
|---|---|---|
| `md2026_nuclear_modernization` | Flag `md2026_nuclear_power` | Permanent idea: modernizacja (+5% war support, +5% defence) + tech bonus rocketry |
| `md2026_nuclear_posturing` | Flag `md2026_nuclear_power` + wojna | Timed idea: posturing (+15% war support, -5% stab, +10% defence) |
| `md2026_develop_nuclear_weapons` | PER/SAU/TUR/KOR/JAP/EGY, brak flagi | Flag `md2026_nuclear_power` + idea `md2026_nuclear_deterrent` + masowa kara opinion |

---

## 5. Decision reward ideas

**Plik:** `common/ideas/md2026_decision_ideas.txt` (342 linii, 31 idea)

### Oryginalne (12 idea, linie 1-142)
- `md2026_improved_military`, `md2026_modernized_air_force`, `md2026_expanded_navy`
- `md2026_economic_growth_effect`, `md2026_infrastructure_boost`
- `md2026_additional_sanctions_effect`, `md2026_arms_delivery_effect`
- `md2026_nato_training_effect`, `md2026_cyber_capability`
- `md2026_military_exercises_effect`, `md2026_military_aid_effect`
- `md2026_economic_cooperation_effect`

### Nowe (19 idea, linie 143-342)

| Idea | Picture | Kluczowe modyfikatory |
|---|---|---|
| `md2026_sov_war_economy` | `national_mobilization` | -10% consumer, +15% arms prod, -5% stab |
| `md2026_sov_information_control` | `political_censorship` | +5% stab, +10% war support, +15% drift defence |
| `md2026_sov_shadow_fleet` | `entrepot_trade` | -10% trade opinion, -5% consumer, +5% industrial |
| `md2026_sov_partial_mobilization` | `national_mobilization` | +2% conscription, +5% attack, -8% stab |
| `md2026_chi_belt_road` | `economic_road_idea` | +10% trade opinion, +5% build speed |
| `md2026_chi_taiwan_pressure` | `threat` | +5% attack, +10% war support |
| `md2026_chi_tech_self_sufficiency` | `electronic_warfare` | +5% research, +5% efficiency |
| `md2026_raj_make_in_india_decision` | `generic_goods` | +10% civ prod, +5% mil prod, -3% consumer |
| `md2026_raj_border_standoff` | `fortification2` | +10% defence, +5% war support |
| `md2026_raj_space_program` | `rocket` | +5% research, +5% PP, +3% stab |
| `md2026_nko_nuclear_test_effect` | `rocket` | +15% war support, +5% defence, -20% trade |
| `md2026_nko_missile_provocation_effect` | `rocket` | +5% attack, +10% war support |
| `md2026_per_proxy_warfare` | `political_violence` | +5% attack, +10% war support, -5% stab |
| `md2026_per_nuclear_program` | `rocket` | +3% research, -5% stab, -15% trade |
| `md2026_sau_vision_2030_acceleration` | `economic_boom` | +15% build speed, -5% consumer, +3% research |
| `md2026_nuclear_modernization_effect` | `rocket` | +5% war support, +5% defence, +2% research |
| `md2026_nuclear_posturing_effect` | `rocket` | +15% war support, -5% stab, +10% defence |

Wszystkie picture names zweryfikowane z `interface/MD_ideas.gfx` bazy MD (12045 linii). Resolucja: `picture = foo` → `GFX_idea_foo`.

---

## 6. Opinion modifiers

**Plik:** `common/opinion_modifiers/md2026_opinion_modifiers.txt` (202 linii, ~36 modyfikatorów)

### Kluczowe modyfikatory

| Modifier | Wartość | Decay | Trade | Opis |
|---|---|---|---|---|
| `md2026_improved_relations` | +25 | -1/rok | tak | Poprawa stosunków |
| `md2026_diplomatic_disapproval` | -30 | -0.5/rok | tak | Dyplomatyczne potępienie |
| `md2026_diplomatic_outreach` | +15 | -1/rok | tak | Inicjatywa dyplomatyczna |
| `md2026_arms_delivery_opinion` | +30 | -1/rok | tak | Dostawa broni |
| `md2026_sanctions_opinion` | -40 | -0.5/rok | tak | Nałożenie sankcji |
| `md2026_article5_solidarity` | +50 | -1/rok | tak | Solidarność NATO Art.5 |
| `md2026_article5_betrayal` | -75 | -0.5/rok | tak | Zdrada Art.5 |
| `md2026_article5_reluctance` | -25 | -1/rok | tak | Niechęć do Art.5 |
| `md2026_nuclear_test_condemnation` | -50 | -0.5/rok | tak | Potępienie testu jądrowego |
| `md2026_nuclear_test_approval` | +10 | -1/rok | nie | Aprobata testu |
| `md2026_military_pressure_anger` | -30 | -0.5/rok | tak | Gniew z presji militarnej |
| `md2026_belt_road_opinion` | +20 | -1/rok | tak | BRI opinia |
| `md2026_proxy_war_anger` | -40 | -0.5/rok | tak | Gniew z proxy warfare |
| `md2026_normalization_opinion` | +40 | -0.5/rok | tak | Normalizacja stosunków |
| `md2026_shadow_fleet_anger` | -20 | -1/rok | tak | Shadow fleet |
| `md2026_missile_provocation_anger` | -35 | -0.5/rok | tak | Prowokacja rakietowa |
| `md2026_space_program_rivalry` | -15 | -1/rok | nie | Rywalizacja kosmiczna |

---

## 7. Focus trees (23 kraje)

Każdy kraj ma dedykowane drzewko fokusów z 10-15 fokusami odzwierciedlającymi realne priorytety polityczne, gospodarcze i militarne na 2026 rok.

### Drzewka wzbogacone (enriched) — z pełnymi mechanikami

Te 4 drzewka zostały dodatkowo wzbogacone o fabryki, tech bonusy, research sloty, national spirits i opinion modifiers:

| Kraj | Plik | Liczba fokusów | Kluczowe mechaniki |
|---|---|---|---|
| **USA** | `md2026_usa_focus.txt` | 15 | Fabryki, tech bonusy, `md2026_usa_labor_shortage`, `md2026_usa_trade_war_tariffs`, research slot |
| **SOV** | `md2026_sov_focus.txt` | ~14 | Fabryki (mil+civ), tech bonusy, `md2026_sov_war_economy`, `md2026_sov_sanctions_evasion`, aluminium/chromium |
| **UKR** | `md2026_ukr_focus.txt` | ~10 | Fabryki, tech bonusy, `md2026_ukr_resistance`, `md2026_ukr_nato_candidate`, research slot, lend-lease |
| **CHI** | `md2026_chi_focus.txt` | ~14 | Fabryki (civ+mil+dockyard), tech bonusy, `md2026_chi_national_rejuvenation`, `md2026_chi_tech_self_reliance`, research slot |

### Drzewka standardowe — już bogate od początku

Pozostałe 19 drzewek miało już pełne mechaniki (fabryki, tech bonusy, opinion modifiers, national spirits) od czasu pierwszej implementacji:

| Kraj | Plik | Tematyka |
|---|---|---|
| GER | `md2026_ger_focus.txt` | Zeitenwende, Bundeswehra, EU leadership |
| ENG | `md2026_eng_focus.txt` | Global Britain, AUKUS, post-Brexit |
| FRA | `md2026_fra_focus.txt` | Autonomia strategiczna, reforma armii, Afryka |
| JAP | `md2026_jap_focus.txt` | Remilitaryzacja, współpraca z USA, demografia |
| KOR | `md2026_kor_focus.txt` | Kryzys polityczny, obrona, K-gospodarka |
| RAJ | `md2026_raj_focus.txt` | Make in India, BRICS, program kosmiczny |
| TUR | `md2026_tur_focus.txt` | Neo-osmańska polityka, S-400, mediacja |
| ISR | `md2026_isr_focus.txt` | Bezpieczeństwo, Iron Dome, normalizacja |
| POL | `md2026_pol_focus.txt` | NATO, modernizacja, Tarcza Wschodu |
| BRA | `md2026_bra_focus.txt` | Amazonia, BRICS, reindustrializacja |
| SAU | `md2026_sau_focus.txt` | Vision 2030, NEOM, normalizacja z Izraelem |
| TAI | `md2026_tai_focus.txt` | Półprzewodniki, obrona, asymetryczna strategia |
| PER | `md2026_per_focus.txt` | Program jądrowy, proxy warfare, oś oporu |
| NKO | `md2026_nko_focus.txt` | Broń nuklearna, rakiety, reżim |
| ITA | `md2026_ita_focus.txt` | Meloni, obronność, migracja |
| AST | `md2026_ast_focus.txt` | AUKUS, łodzie podwodne, Indo-Pacyfik |
| CAN | `md2026_can_focus.txt` | NATO, Arktyka, NORAD |
| SYR | `md2026_syr_focus.txt` | Odbudowa, reintegracja, rosyjskie bazy |
| EGY | `md2026_egy_focus.txt` | Kanał Sueski, armia, stabilizacja |

---

## 8. Eventy — system

**Plik:** `events/md2026_system.txt` (142 linii, 3 eventy)

| Event | Typ | Trigger | Opis |
|---|---|---|---|
| `md2026_system.1` | news_event | on_startup (triggered) | "The World in 2026" — intro event z 3 opcjami (Zachód/Wschód/reszta) |
| `md2026_system.2` | news_event | MTTH, date > 2026.12.31 | "2027: A Year in Review" — rocznica, fire_once |
| `md2026_system.3` | country_event | MTTH 36 mies., is_major | "Global Economic Turbulence" — opcje: austerity vs stimulus |

---

## 9. Eventy — NATO Article 5

**Plik:** `events/md2026_nato_article5.txt` (209 linii, 3 eventy)

Event chain triggerowany z `on_declare_war` gdy ktoś atakuje członka NATO.

| Event | Odbiorca | Opcje |
|---|---|---|
| `md2026_nato_article5.1` | USA | Invoke Art.5 (+15 war support, -75 PP, triggeruje .2 do NATO) **lub** Condemn only (-5 stab, opinion penalty) |
| `md2026_nato_article5.2` | Każdy NATO member | Full commitment (idea `md2026_nato_article5_active`, +10 war support) **lub** Limited support (+5 war support) **lub** Refuse (-5 stab, opinion penalties) |
| `md2026_nato_article5.3` | Posiadacze Art.5 idea | Stand down (remove idea, +5 stab, +25 PP) — fires po zakończeniu wojny |

---

## 10. Eventy — wybory

**Plik:** `events/md2026_elections.txt` (1024 linii, 10 eventów)

### Oryginalne (3 eventy)

| Event | Kraj | Rok | Kandydaci |
|---|---|---|---|
| `md2026_elections.1` | Generyczny | — | Incumbent / Opposition / Populist |
| `md2026_elections.10` | USA | 2026 midterms | Democratic sweep / Republican sweep / Split |
| `md2026_elections.20` | FRA | 2027 | Macron successor / Le Pen / Mélenchon |

### Nowe (7 eventów)

| Event | Kraj | Rok | Kandydaci |
|---|---|---|---|
| `md2026_elections.30` | GER | 2029 | Merz (CDU) / Pistorius (SPD) / Weidel (AfD) / Habeck (Zieloni) |
| `md2026_elections.40` | ENG | 2029 | Starmer (Labour) / Badenoch (Conservative) / Farage (Reform UK) |
| `md2026_elections.50` | JAP | 2028 | Ishiba (LDP) / Noda (opozycja) / Kobayashi (LDP-hawks) |
| `md2026_elections.60` | KOR | 2027 | Lee Jae-myung (liberal) / Han Dong-hoon (konserwatysta) / deadlock |
| `md2026_elections.70` | BRA | 2030 | Haddad (PT) / de Freitas (bolsonaryzm) / Tebet (centrum) |
| `md2026_elections.80` | POL | 2027 | Tusk (KO) / Morawiecki (PiS) / Trzaskowski (nowa centroprawica) |
| `md2026_elections.90` | ITA | 2028 | Meloni (FdI) / Schlein (PD) / Conte (M5S) |

Każdy event używa `create_country_leader` z odpowiednimi cechami ideologicznymi MD (`conservatism`, `socialism`, `liberalism`, `Nat_Populism`) i traitami (`western_conservatism`, `career_politician`, `anti_establishment`, `media_personality`, `lawyer`, `captain_of_industry`).

---

## 11. Eventy — random

**Plik:** `events/md2026_random_events.txt` (398 linii, 8 eventów)

Eventy losowe oparte na MTTH, dodające nieprzewidywalność do rozgrywki.

| Event | MTTH | Warunki | Opcje |
|---|---|---|---|
| `md2026_random.1` — Border Incident | 48 mies. | Sąsiad w wojnie | Dyplomacja (+3 stab) / Wojsko (+5 WS) |
| `md2026_random.2` — Natural Disaster | 72 mies. | Wszyscy | Pomoc domowa (-50 PP) / Pomoc międzynarodowa (+opinion) |
| `md2026_random.3` — Tech Breakthrough | 60 mies. | is_major, >30 civ | Komercjalizacja (tech computing) / Militaryzacja (tech doctrine) |
| `md2026_random.4` — Terrorism | 96 mies. | is_major lub NATO | Crackdown (-8 stab, +10 WS) / Jedność (-5 stab, +25 PP) |
| `md2026_random.5` — Pandemic Scare | 120 mies. | Global (once) | Lockdown (-10 stab, -50 PP) / Otwarta gospodarka (-5 stab) |
| `md2026_random.6` — Market Crash | 84 mies. | is_major | Bailout (-75 PP) / Free market (-10 stab) |
| `md2026_random.7` — Cyber Attack | 60 mies. | is_major lub NATO | Obrona cyber (-50 PP) / Odwet (+3 WS) |
| `md2026_random.8` — Mass Protests | 24 mies. | stab < 40% | Ustępstwa (+5 stab, -50 PP) / Represje (-5 stab, +25 PP) |

---

## 12. Lokalizacja

**Plik:** `localisation/english/md2026_l_english.yml` (1918 linii)

Format HOI4 YAML z BOM: `﻿l_english:` w pierwszej linii, klucze z spacją na początku: ` key:0 "value"`.

### Zawartość lokalizacji

| Sekcja | Zakres linii | Liczba kluczy |
|---|---|---|
| Bookmark i opisy krajów | 1-37 | ~35 |
| National spirits (oryginalne) | 38-70 | ~30 |
| Focus trees (23 kraje) | 71-390 | ~300 |
| Eventy — Rosja/Ukraina | 391-500 | ~50 |
| Eventy — Tajwan | 500-600 | ~50 |
| Eventy — Bliski Wschód | 600-750 | ~70 |
| Eventy — BRICS | 750-850 | ~50 |
| Eventy — NATO-Rosja | 850-950 | ~50 |
| Eventy — migracja | 950-1050 | ~50 |
| Eventy — klimat | 1050-1150 | ~50 |
| Eventy — technologia | 1150-1250 | ~50 |
| Eventy — demografia | 1250-1350 | ~50 |
| Eventy — wybory (oryginalne) | 1350-1410 | ~20 |
| Decyzje i kategorie (oryginalne) | 1410-1500 | ~60 |
| Eventy — kosmos | 1636-1663 | ~30 |
| Kategorie decyzji (nowe) | 1665-1669 | 4 |
| Eventy systemowe | 1671-1683 | 13 |
| Eventy NATO Article 5 | 1685-1697 | 11 |
| Eventy wyborcze (7 nowych krajów) | 1699-1757 | 28 |
| Eventy random (8 eventów) | 1759-1801 | 24 |
| National spirits — krajowe | 1803-1835 | 22 |
| National spirits — systemowe | 1837-1867 | 24 |
| National spirits — focus enrichment | 1869-1881 | 16 |
| Decision reward ideas (nowe) | 1883-1917 | 34 |
| Decyzje — internal politics | 1879-1910 | ~30 |
| Decyzje — nuclear | 1912-1918 | 6 |

---

## Konwencje nazewnicze

### Prefiksy

Wszystkie nowe elementy submoda używają prefiksu `md2026_` aby uniknąć kolizji z bazowym MD.

```
md2026_[tag]_[nazwa]          → spirit/decyzja dla konkretnego kraju
md2026_[system]               → element systemowy (war_exhaustion, sanctions_tier)
md2026_[event_namespace].[n]  → eventy
```

### Ideologie MD

| HOI4 ideology | MD subtype | Użycie |
|---|---|---|
| `democratic` | `conservatism`, `socialism`, `liberalism` | Zachód, demokratyczne kraje |
| `communism` | — | Autokracje (Rosja, Chiny) |
| `fascism` | — | Salafizm |
| `nationalist` | `Nat_Populism`, `Nat_Fascism` | Populizm narodowy |
| `neutrality` | — | Niezaangażowani |

### Leader traits

```
western_conservatism, western_socialism, western_liberalism    → ideologiczne
nationalist_Nat_Populism                                       → nacjonalistyczne
career_politician, captain_of_industry, lawyer                 → zawodowe
anti_establishment, media_personality                          → osobowościowe
```

### Grafiki ideas

Nazwy `picture = ` w ideas odwołują się do sprite'ów z `interface/MD_ideas.gfx` bazy MD:
- `picture = foo` → resolver: `GFX_idea_foo`
- Zweryfikowane nazwy: `NATO_member`, `CSTO_member`, `bricks`, `embargo`, `volunteer_defenders`, `political_violence`, `political_censorship`, `political_establishment`, `economic_increase`, `economic_boom`, `economic_road_idea`, `army_problems`, `electronic_warfare`, `national_mobilization`, `GENERIC_protectionism`, `population`, `rocket`, `bricks_bank`, `central_management`, `generic_goods`, `fortification2`, `strike`, `entrepot_trade`, `threat`

---

## Znane ograniczenia i TODO

### Poza zakresem (celowo pominięte)

- [ ] **Polska lokalizacja** (`md2026_l_polish.yml`) — do zrobienia ręcznie
- [ ] **GFX/portrety liderów** — portrety `.dds` z eventów wyborczych wymagają grafik
- [ ] **thumbnail.png** — placeholder, wymaga zaprojektowania grafiki

### Potencjalne problemy

- **Duplikat klucza `md2026_sov_war_economy`** — ten sam klucz jest zdefiniowany zarówno w `md2026_national_spirits.txt` (spirit z fokusu, linia 1023) jak i w `md2026_decision_ideas.txt` (idea z decyzji, linia 145). HOI4 użyje jednej z definicji (prawdopodobnie ostatniej załadowanej). Obie mają podobne modyfikatory, więc w praktyce nie powinno powodować problemów, ale dla czystości kodu warto rozdzielić nazwy.
- **Portrety liderów z wyborów** — eventy wyborów tworzą liderów z `picture = "gfx/leaders/XXX/Name.dds"`. Jeśli bazowy MD nie ma danego portretu, wyświetli się domyślny. Nie jest to błąd krytyczny.
- **Brak `md2026_cyber_capability` idea** — event `md2026_random.7` sprawdza `has_idea = md2026_cyber_capability` w modyfikatorze MTTH. Ta idea jest zdefiniowana w `md2026_decision_ideas.txt` (oryginalne 12 idea), więc jest dostępna tylko po decyzji cyber warfare.

### Statystyki

| Element | Liczba |
|---|---|
| Focus trees | 23 |
| National spirits | ~58 |
| Decision categories | 7 |
| Decisions | ~45 |
| Decision reward ideas | 31 |
| Opinion modifiers | ~36 |
| Election events | 10 |
| System events | 3 |
| NATO Article 5 events | 3 |
| Random events | 8 |
| Thematic event chains | 10 (RU-UKR, Taiwan, Mideast, BRICS, NATO-Russia, Migration, Climate, Tech, Demographics, Space) |
| Scripted triggers | 6 |
| Localisation keys | ~1900 |
| Country histories | 66+ |
