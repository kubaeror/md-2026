# MD2026 Implementation Plan — Rozszerzenia

## Punkty do wdrożenia

### 1. on_actions — inicjalizacja i hooki [WYSOKI]
- Plik: `common/on_actions/md2026_on_actions.txt`
- on_startup: ustawienie global_flag md2026_initialized, intro news event
- on_monthly: war exhaustion tick (Rosja-Ukraina), sanctions degradation
- on_peace: efekty zakończenia wojny, zniesienie mobilizacji
- on_declare_war: NATO Article 5 check
- on_government_change: usuwanie/dodawanie spiritów zależnych od ideologii

### 2. scripted_triggers [WYSOKI]
- Plik: `common/scripted_triggers/md2026_triggers.txt`
- md2026_is_active, md2026_is_nato_member, md2026_is_brics_member
- md2026_is_western_democracy, md2026_is_authoritarian
- md2026_is_conflict_zone, md2026_is_nuclear_power

### 3. Nowe national spirits [WYSOKI]
- Plik: edycja `common/ideas/md2026_national_spirits.txt`
- JAP: md2026_jap_demographic_crisis
- KOR: md2026_kor_political_crisis (impeachment Yoon)
- SAU: md2026_sau_vision_2030
- SUD: md2026_sud_civil_war
- YEM: md2026_yem_houthi_division
- RAJ: md2026_raj_hindu_nationalism, md2026_raj_digital_india
- SOV: md2026_sov_shadow_economy
- War exhaustion: md2026_war_exhaustion_1 do _3 (timed, stackable)
- Nuclear deterrence: md2026_nuclear_deterrent (shared, per-country gating)
- NATO Article 5: md2026_nato_article5_active
- Sanctions tiers: md2026_additional_sanctions_effect (already exists), add tier system

### 4. Decyzje non-Western [WYSOKI]
- Plik: edycja `common/decisions/md2026_decisions.txt` + nowa kategoria
- Nowa kategoria: md2026_internal_politics_category
- SOV: war economy, information control, shadow fleet, partial mobilization
- CHI: Belt and Road, Taiwan military pressure, tech self-sufficiency
- RAJ: Make in India expansion, border standoff (CHI/PAK), space program
- NKO: nuclear test, missile provocation, diplomatic outreach
- PER: proxy warfare, nuclear acceleration
- SAU: Vision 2030 acceleration, normalization with Israel

### 5. Wzbogacenie focus tree rewards [WYSOKI]
- Pliki: edycja md2026_usa_focus.txt + inne focus trees
- Dodanie budowy fabryk, infrastruktury, research bonusów
- Dodanie triggerowania eventów z fokusów
- Dodanie national spirits jako reward
- USA capstone focus

### 6. Eventy wyborów z leader change [WYSOKI]
- Plik: edycja `events/md2026_elections.txt`
- GER 2029, UK 2029, JAP 2028, KOR 2027, BRA 2030, POL 2027, ITA 2027/2028
- Każdy event zmienia lidera (create_country_leader lub set_politics)
- Opcje z realnymi kandydatami

### 7. NATO Article 5 + sanctions system [ŚREDNI]
- Article 5: event chain triggerowany z on_declare_war gdy ktoś atakuje NATO member
- Sanctions: tiered system (mild → moderate → severe → total)
- Integration z existing MD sanctions scripted effects

### 8. Mechaniki systemowe [ŚREDNI]
- War exhaustion: monthly tick dodający timed ideas
- Nuclear deterrence: decision + national spirit system
- BRICS expansion: scripted effects + events

### 9. Random events / cykliczne kryzysy [ŚREDNI]
- Plik: `events/md2026_random_events.txt`
- Kryzysy regionalne (MTTH 12-24 mies.)
- Odkrycia technologiczne, katastrofy naturalne
- Ataki terrorystyczne, protesty, kryzysy ekonomiczne

### 10. Opinion modifiers [ŚREDNI]
- Dodanie trade = yes modyfikatorów
- Dodanie długoterminowych relacji

### 11. Fixy techniczne [NISKI]
- Poprawka fortify_borders decision
- Poprawka picture names w ideas
