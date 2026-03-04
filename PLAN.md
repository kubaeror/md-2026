# Millennium Dawn 2026 Rework - Plan Pracy

## Informacje o projekcie

- **Nazwa submoda:** Millennium Dawn 2026 Rework
- **Typ:** Dependency submod (wymaga oryginalnego Millennium Dawn: A Modern Day Mod)
- **Wersja HOI4:** 1.17.4.1
- **Wersja bazowego MD:** 1.12.3 (Workshop ID: 2777392649)
- **Cel:** Aktualizacja stanu swiata do roku 2026 z nowym bookmarkiem startowym `2026.1.1`
- **Zakres krajow:** Mocarstwa + kraje regionalne + wszystkie kraje NATO (~50-60 krajow)

## Architektura submoda

Submod dziala jako **dependency** - wymaga oryginalnego MD jako bazy. Nadpisuje tylko zmienione pliki.
Nowy bookmark `2026.1.1` wyswietla sie obok oryginalnego `2000.1.1`.

---

## Docelowa struktura plikow

```
md-2026/
|-- descriptor.mod
|-- PLAN.md
|-- common/
|   |-- bookmarks/
|   |   |-- blitzkrieg.txt              (kopia MD + nowy bookmark 2026)
|   |   +-- the_gathering_storm.txt     (placeholder)
|   |-- characters/                     (nadpisane pliki krajow)
|   |   |-- USA.txt
|   |   |-- SOV.txt
|   |   |-- UKR.txt
|   |   +-- ... (50-60 plikow)
|   |-- ideas/
|   |   +-- md2026_national_spirits.txt
|   |-- national_focus/
|   |   +-- md2026_*.txt                (nowe galezi focus tree)
|   |-- scripted_effects/
|   |   +-- md2026_startup_effects.txt
|   +-- scripted_triggers/
|       +-- md2026_triggers.txt
|-- events/
|   +-- md2026_*.txt
|-- history/
|   |-- countries/                      (nadpisane pliki krajow)
|   |   |-- USA - USA.txt
|   |   |-- SOV - Russia.txt
|   |   +-- ... (50-60 plikow)
|   |-- states/                         (tylko zmienione stany)
|   |   +-- ... (Krym, Donbas, Zaporoze, Cherson etc.)
|   +-- units/                          (OOB na 2026)
|       +-- ...
|-- localisation/
|   |-- english/
|   |   +-- md2026_l_english.yml
|   +-- polish/
|       +-- md2026_l_polish.yml
+-- gfx/
    +-- leaders/                        (portrety liderow - generic na start)
```

---

## FAZA 0: Infrastruktura submoda
**Priorytet:** KRYTYCZNY | **Zlozonosc:** Niska | **Pliki:** 3-4

### Zadania:
- [x] Utworzyc repozytorium git
- [x] Zapisac plan do pliku PLAN.md
- [ ] Zaktualizowac `descriptor.mod` - dodac `dependencies`, `replace_path` dla bookmarkow
- [ ] Zaktualizowac `md-2026.mod` (plik launchera)
- [ ] Skopiowac i zmodyfikowac `common/bookmarks/blitzkrieg.txt` - dodac bookmark 2026
- [ ] Skopiowac `common/bookmarks/the_gathering_storm.txt` (placeholder)

### Szczegoly techniczne:
- MD **nie ma** `replace_path` na `common/bookmarks`, wiec submod moze nadpisac plik bookmarkow
- Oryginalny bookmark 2000 zostanie zachowany 1:1 w naszym pliku
- `descriptor.mod` potrzebuje `dependencies = { "Millennium Dawn: A Modern Day Mod" }`
- Nowy bookmark:
  - Nazwa: `MD_2026`
  - Data: `2026.1.1.12`
  - Featured countries: USA, SOV, CHI, UKR, ISR, TUR, POL, JAP

---

## FAZA 1: Granice i stany
**Priorytet:** WYSOKI | **Zlozonosc:** Srednia | **Pliki:** 10-30 stanow

### Zmiany terytorialne 2000-2026:

| Zmiana | Stany do modyfikacji | Opis |
|--------|---------------------|------|
| Krym -> Rosja (2014) | Stany Krymu | `owner = SOV`, `add_core_of = SOV/UKR` |
| Donbas - aneksja przez Rosje (2022) | Stany Doniecka, Luganska | `owner = SOV`, rdzenie SOV + UKR |
| Zaporoze/Cherson (czesciowa okupacja) | Stany Zaporoza, Chersonia | Czesc SOV, czesc UKR |
| Sudan Poludniowy (2011) | Stany Sudanu Pld. | Weryfikacja tagu SSD |
| Kosowo (status) | Stan Kosowa | `owner = KOS` |
| Syria post-Assad (2024) | Stany Syrii | HTS kontrola, Kurdowie polnoc-wschod |
| Golan (de facto Izrael) | Stan Golanu | Weryfikacja |

### Do zbadania:
- Dokladne ID stanow MD dla Krymu, Donbasu, Zaporoza, Chersonia
- Linie frontu wojny rosyjsko-ukrainskiej na styczen 2026
- Kontrola terytorialna w Syrii po upadku Assada (grudzien 2024)
- Status Sudanu Poludniowego w MD (czy tag SSD istnieje)

---

## FAZA 2: Historia krajow
**Priorytet:** WYSOKI | **Zlozonosc:** Wysoka | **Pliki:** 50-60 krajow

Dla kazdego kraju tworzymy blok `2026.1.1` w pliku `history/countries/TAG - Kraj.txt`.

### Mocarstwa (12 krajow):

| Kraj | Tag | Lider 2026 | Ideologia MD | GDP per capita |
|------|-----|------------|-------------|----------------|
| USA | USA | Donald Trump | nationalist/Nat_Populism | ~85.0 |
| Rosja | SOV | Wladimir Putin | communism/Autocracy | ~15.0 |
| Chiny | CHI | Xi Jinping | communism/Autocracy | ~17.0 |
| UK | ENG | Keir Starmer | democratic/socialism | ~48.0 |
| Francja | FRA | Emmanuel Macron | democratic/liberalism | ~44.0 |
| Niemcy | GER | Friedrich Merz | democratic/conservatism | ~52.0 |
| Indie | RAJ | Narendra Modi | communism/Conservative | ~3.5 |
| Japonia | JAP | Shigeru Ishiba | democratic/conservatism | ~34.0 |
| Turcja | TUR | Recep Erdogan | communism/Autocracy | ~13.0 |
| Iran | PER | M. Pezeshkian / Khamenei | communism/Vilayat_e_Faqih | ~7.0 |
| Brazylia | BRA | Lula da Silva | democratic/socialism | ~10.0 |
| Ukraina | UKR | Wolodymyr Zelenski | democratic/liberalism | ~5.0 |

### Kraje NATO (dodatkowe ~20):

| Kraj | Tag | Lider 2026 | Ideologia MD |
|------|-----|------------|-------------|
| Polska | POL | Donald Tusk | democratic/liberalism |
| Rumunia | ROM | Marcel Ciolacu | democratic/conservatism |
| Finlandia | FIN | Petteri Orpo | democratic/conservatism |
| Szwecja | SWE | Ulf Kristersson | democratic/conservatism |
| Hiszpania | SPR | Pedro Sanchez | democratic/socialism |
| Wlochy | ITA | Giorgia Meloni | nationalist/Nat_Populism |
| Holandia | HOL | Dick Schoof | democratic/conservatism |
| Kanada | CAN | Mark Carney | democratic/liberalism |
| Norwegia | NOR | Jonas Gahr Store | democratic/socialism |
| Dania | DEN | Mette Frederiksen | democratic/socialism |
| Grecja | GRE | Kyriakos Mitsotakis | democratic/conservatism |
| Czechy | CZE | Petr Fiala | democratic/conservatism |
| Bulgaria | BUL | Dimitar Glowczew | democratic/conservatism |
| Portugalia | POR | Luis Montenegro | democratic/conservatism |
| Belgia | BEL | Alexander De Croo | democratic/liberalism |
| Estonia | EST | Kristen Michal | democratic/liberalism |
| Lotwa | LAT | Evika Silina | democratic/conservatism |
| Litwa | LIT | Gintautas Paluckas | democratic/socialism |
| Chorwacja | CRO | Andrej Plenkovic | democratic/conservatism |
| Albania | ALB | Edi Rama | democratic/socialism |
| Wegry | HUN | Viktor Orban | nationalist/Nat_Populism |
| Slowacja | SLO | Robert Fico | nationalist/Nat_Populism |
| Slowenia | SLV | Robert Golob | democratic/liberalism |
| Czarnogora | MNT | Milojko Spajic | democratic/liberalism |
| Macedonia Pln. | FYR | Hristijan Mickoski | democratic/conservatism |
| Islandia | ICE | Bjarni Benediktsson | democratic/conservatism |
| Luksemburg | LUX | Luc Frieden | democratic/conservatism |

### Kraje regionalne (konflikty, ~10-15):

| Kraj | Tag | Lider 2026 | Kontekst |
|------|-----|------------|----------|
| Izrael | ISR | Benjamin Netanyahu | Post-Gaza, operacje Liban |
| Arabia Saudyjska | SAU | Mohammed bin Salman | Vision 2030, normalizacja |
| Korea Pln. | NKO | Kim Jong-un | Program nuklearny, drony dla Rosji |
| Korea Pld. | KOR | Han Duck-soo (p.o.) | Kryzys polityczny, impeachment Yoon |
| Tajwan | (tag MD) | Lai Ching-te | Napięcia z Chinami |
| Syria | SYR | Ahmad al-Sharaa (HTS) | Post-Assad, upadek reziimu XII.2024 |
| Egipt | EGY | Abdel Fattah el-Sisi | Kryzys gospodarczy |
| Mjanma | BRM | Min Aung Hlaing | Wojna domowa, junta |
| Australia | AST | Anthony Albanese | AUKUS |
| RPA | SAF | Cyril Ramaphosa | BRICS |
| Etiopia | ETH | Abiy Ahmed | BRICS+, post-wojna Tigraj |
| UAE | UAE | Mohammed bin Zayed | Abraham Accords, BRICS |
| Sudan | SUD | Abdel Fattah al-Burhan | Wojna domowa RSF vs SAF |
| Jemen | YEM | Houthi vs rzad | Podzielony kraj |

### Elementy do ustawienia per kraj:
- Lider (country_leader w characters + set_politics w history)
- Ideologia i sub-ideologia
- GDP per capita
- OOB (Order of Battle) - jednostki wojskowe
- Odblokowane technologie
- Prawa i ustawy (conscription, trade, economy)
- National spirits/ideas
- Zmienne (election timer, parliament support, etc.)
- Flagi krajowe (sanctions, alliances, etc.)
- Relacje dyplomatyczne i wplyw

---

## FAZA 3: Konflikty aktywne
**Priorytet:** WYSOKI | **Zlozonosc:** Srednia | **Pliki:** 5-10

### Wojny do ustawienia na 2026.1.1:

| Konflikt | Strona A | Strona B | Mechanika |
|----------|----------|----------|-----------|
| Wojna rosyjsko-ukrainska | SOV | UKR | `declare_war_on`, stany frontowe |
| Wojna domowa w Sudanie | SUD (SAF) | tag rebeliancki (RSF) | Podział stanow |
| Wojna domowa w Mjanmie | BRM (junta) | tag opozycji | Kontrola terytorialna |
| Jemen (Houthi) | YEM (Houthi) vs rzad | Podział polnoc/poludnie | Weryfikacja tagow |
| Somalia (Al-Shabaab) | SOM vs SHB | Insurgency | Kontrola terytorialna |
| Syria (fragmentacja) | SYR (HTS) | Kurdowie (autonomia) | Strefy kontroli |

### Linie frontu wojny rosyjsko-ukrainskiej (styczen 2026):
- Rosja kontroluje: Krym, wiekszosc obwodu lugańskiego, czesc donieckiego, polnocny Cherson, czesc Zaporoza
- Ukraina kontroluje: reszte Chersonia, wiekszosc Zaporoza, czesc Doniecka, cala reszte kraju
- Aktywne walki: glownie w obwodzie donieckim (Pokrowsk, Kurachowe, Wuhledar utracony)
- Kursk: ukrainska operacja na terenie Rosji (od VIII.2024, czesc terytorium nadal pod kontrola UKR)

---

## FAZA 4: Frakcje i sojusze
**Priorytet:** WYSOKI | **Zlozonosc:** Srednia | **Pliki:** 5-10

### NATO na 2026 (32 czlonkow):
Pelna lista w startup_effects: USA, ENG, FRA, GER, ITA, CAN, TUR, SPR, POL, HOL,
BEL, NOR, DEN, POR, CZE, GRE, HUN, ICE, LUX, ROM, BUL, CRO, ALB, LIT, LAT,
EST, SLO, SLV, MNT, FYR, FIN, SWE

### CSTO na 2026:
SOV (Rosja), BLR (Bialorus), KAZ (Kazachstan), KYR (Kirgistan), TAJ (Tadzykistan)
UWAGA: Armenia (ARM) oficjalnie zamrozila czlonkostwo w 2024

### EU na 2026 (27 czlonkow):
GER, FRA, ITA, SPR, HOL, BEL, LUX, POR, GRE, AUS, FIN, SWE, DEN, POL, CZE,
HUN, ROM, BUL, CRO, SLO, SLV, EST, LAT, LIT, IRL, CYP, MLT

### Inne sojusze/grupy:
- **AUKUS:** USA, ENG, AST (Australia) - pakt bezpieczenstwa
- **BRICS+ (2024):** CHI, SOV, RAJ, BRA, SAF, EGY, ETH, PER, UAE, SAU
- **SCO:** CHI, SOV, RAJ, KAZ, KYR, TAJ, UZB, PER, BLR (2024)
- **Abraham Accords:** ISR + UAE, BHR, MAR, SUD (normalizacja)
- **Quad:** USA, JAP, RAJ, AST

---

## FAZA 5: Postaci (characters)
**Priorytet:** WYSOKI | **Zlozonosc:** Wysoka | **Pliki:** 50-60

### Per kraj (characters/TAG.txt):
- **Lider kraju** (prezydent/premier/monarcha)
  - Portret: generic na start, custom GFX pozniej
  - Traits: odpowiednie cechy przywodcze
- **Glownodowodzacy sil zbrojnych** (1-3 generałow/admirałow)
- **Doradcy polityczni** (2-4)

### Kluczowi nowi liderzy do dodania:
- Donald Trump (USA) - juz moze istniec w MD jako postac
- Friedrich Merz (GER) - nowy kanclerz 2025
- Keir Starmer (ENG) - premier od 2024
- Mark Carney (CAN) - premier od 2025
- Ahmad al-Sharaa (SYR) - lider HTS, de facto wladca Syrii
- Lai Ching-te (Tajwan) - prezydent od 2024
- Giorgia Meloni (ITA) - premier od 2022
- Wielu nowych generalow i dowodcow wojskowych

### Format portretu (generic):
Uzycie istniejacych generycznych portretow z MD dopoki custom GFX nie bedzie gotowe.
Sciezka: `gfx/leaders/TAG/leader_name.dds`

---

## FAZA 6: Technologie
**Priorytet:** SREDNI | **Zlozonosc:** Srednia | **Wbudowane w Faze 2**

Bloki technologiczne w `history/countries/` z odblokowanymi tech na 2026.

### Glowne kategorie:

| Kategoria | Przyklady | Kraje wiodace |
|-----------|-----------|--------------|
| Czolgi nowoczesne | Leopard 2A7+, M1A2 SEPv3, T-90M, T-14 Armata (proto) | GER, USA, SOV |
| Mysliwce 5. gen | F-35A/B/C, Su-57, J-20, KF-21 (proto) | USA, SOV, CHI, KOR |
| Drony bojowe | Bayraktar TB2, Shahed-136, MQ-9, Wing Loong | TUR, PER, USA, CHI |
| Obrona przeciwrakietowa | Iron Dome, THAAD, S-400, S-500, Patriot PAC-3 | ISR, USA, SOV |
| Marynarka | Type 055, Gerald Ford, Yasen-M | CHI, USA, SOV |
| Technologie kosmiczne | Starlink, BeiDou, GLONASS | USA, CHI, SOV |
| Cyber | Zaawansowane cyber zdolnosci | USA, CHI, SOV, ISR |
| Nuklearne | Arsenaly na 2026 | USA, SOV, CHI, FRA, ENG, ISR, RAJ, NKO, PAK |

### Poziomy tech per tier krajow:
- **Tier 1 (supermocarstwa):** USA, CHI, SOV - prawie wszystkie tech odblokowane
- **Tier 2 (mocarstwa regionalne):** ENG, FRA, GER, JAP, KOR, ISR, RAJ, TUR - wiekszosc tech
- **Tier 3 (NATO rozwinięte):** POL, ITA, SPR, CAN, AST, HOL, NOR, SWE, FIN - solidna baza
- **Tier 4 (rozwijajace sie):** BRA, EGY, SAU, UAE, PER - wybrane nowoczesne systemy
- **Tier 5 (pozostale):** reszta - bazowe technologie

---

## FAZA 7: Ideas / National Spirits
**Priorytet:** SREDNI | **Zlozonosc:** Srednia | **Pliki:** 5-10

### Nowe National Spirits (ideas) per kraj:

| Kraj | Spirit | Efekt |
|------|--------|-------|
| SOV | Sankcje zachodnie | -15% factory output, -30% trade, +10% war support |
| SOV | Mobilizacja wojenna | +5% conscription, -10% consumer goods, +15% army attack |
| UKR | Zachodnia pomoc wojskowa | +20% equipment from lend-lease, +10% org |
| UKR | Mobilizacja obronna | +3% conscription, +15% defense, -20% GDP growth |
| USA | Polaryzacja polityczna | -5% stability, -10% political power, +5% war support |
| USA | America First | +10% consumer goods, -15% diplomatic influence |
| CHI | Spowolnienie gospodarcze | -5% GDP growth, -10% construction speed |
| CHI | Modernizacja armii | +10% army/navy/air experience |
| GER | Zeitenwende | +15% military spending effectiveness, -5% stability |
| ENG | Post-Brexit reality | -5% trade, +5% sovereignty modifiers |
| ISR | Stan wojenny | +20% army defense, +10% war support, -15% stability |
| TUR | Autokracja Erdogana | +10% political power, -5% democratic drift, -10% stability |
| PER | Sankcje miedzynarodowe | -20% trade, -10% factory output |
| NKO | Izolacja totalitarna | -50% trade, +5% conscription, +20% army attack |
| POL | Tarcza Wschodu | +15% fort construction, +10% army defense |

### Modyfikatory systemowe:
- Aktualizacja corruption levels per kraj
- Aktualizacja economic cycle (recession/growth/stagnation)
- Aktualizacja internal factions (oligarchs, military, reformists, etc.)

---

## FAZA 8: Focus Trees
**Priorytet:** SREDNI | **Zlozonosc:** BARDZO WYSOKA | **Pliki:** 45 (23 shared + 22 base copies)
**Status:** UKONCZONY

### Podejscie: Nowe galezi drzew dodawane do istniejacych (NIE zastepujemy calych drzew)

### 23 drzewa fokusowe:
- [x] **Oryginalne 7 (kompaktowe, ~8-12 fokusow):** USA, SOV, UKR, CHI, BRA, SAU, POL
- [x] **Rozszerzone 16 (26 fokusow, 5 galezi, ME, capstone):** GER, RAJ, JAP, TUR, ISR, KOR, FRA, ENG, PER, ITA, NKO, CAN, AST, TAI, EGY, SYR

### Struktura rozszerzonych drzew (26 fokusow):
- 4 galeze non-ME: T1 → T2a + T2b → T3a + T3b (5 fokusow per galaz)
- 1 galaz ME: T1 → T2a ⊕ T2b → T3 (4 fokusy)
- 1 capstone: wymaga root + kilku T3
- Pozycje galezi wzgledem root: x = -6, -3, 0, +3, +6

### Pre-completion md2026_ fokusow (336 fokusow):
- [x] Oryginalne 7: ~70 fokusow pre-completed
- [x] Rozszerzone 16: 14 fokusow per kraj (root + 5 T1 + 8 non-ME T2) = 224
- [x] Dodatkowe 22 kraje (generic tree): bez md2026_ fokusow

### Pre-completion bazowych MD fokusow (root + T1, 2000-2026):
- [x] **44 kraje z dedykowanymi drzewami** (Batch 1-5): indywidualnie dobrane fokusy z uwzglednieniem ME par i sciezek politycznych
- [x] **15 krajow coastal (generic tree)**: 38 fokusow GENERIC (10 root + 28 T1)
- [x] **7 krajow landlocked (generic tree)**: 33 fokusy GENERIC (9 root + 24 T1, bez naval)
- Razem: ~2105 linii complete_national_focus w 66 plikach historii

### Pary ME per kraj (rozszerzone 16):
| Kraj | Opcja A | Opcja B |
|------|---------|---------|
| GER | atlantic_solidarity | european_defense_pillar |
| RAJ | quad_deepening | brics_balance |
| JAP | taiwan_contingency | korea_reconciliation |
| TUR | nato_loyalty | eurasian_pivot |
| ISR | preemptive_strike | covert_ops |
| KOR | diplomatic_opening | maximum_pressure |
| FRA | sahel_withdrawal | sahel_reengage |
| ENG | cptpp | eu_rapprochement |
| PER | nuclear_accelerate | nuclear_negotiate |
| ITA | south_development | northern_industry |
| NKO | south_korea_threat | diplomatic_leverage |
| CAN | trade_diversification | us_accommodation |
| AST | china_decouple | china_engage |
| TAI | us_arms_sales | japan_cooperation |
| EGY | us_weapons | diversify_suppliers |
| SYR | secular_state | islamic_governance |

---

## FAZA 9: Eventy
**Priorytet:** SREDNI | **Zlozonosc:** BARDZO WYSOKA | **Pliki:** 10-20

### Lancuchy eventow:

#### 1. Negocjacje pokojowe Rosja-Ukraina
- Event: Propozycja zawieszenia broni (triggered by focus lub decision)
- Opcje: akceptacja/odrzucenie przez obie strony
- Outcomes: zamrozony konflikt, pelny pokoj, eskalacja
- Efekty: zmiany granic, zniesienie/utrzymanie sankcji, NATO membership

#### 2. Kryzys tajwanski
- Event: Chiny zblizaja sie do inwazji (triggered by focus)
- Reakcja USA/Japonii/AUKUS
- Opcje: blokada morska, inwazja, dyplomacja
- Efekty: globalna recesja, wojna, status quo

#### 3. Bliski Wschod post-2024
- Syria: odbudowa pod HTS, wybory, fragmentacja
- Izrael-Palestyna: rozejm, eskalacja, normalizacja
- Iran: program nuklearny, rewolucja?, otwarcie
- Jemen: zjednoczenie lub podzial

#### 4. Wybory cykliczne
- Aktualizacja election_var dla krajow demokratycznych
- Nowe kandydaci na 2026-2030
- Efekty wyborow na polityki

#### 5. BRICS+ ekspansja
- Nowe kraje dolaczaja do BRICS
- Alternatywny system finansowy
- De-dolaryzacja

#### 6. NATO-Rosja eskalacja
- Incydenty graniczne (Baltyk, Arktyka)
- Cyber ataki
- Artykul 5 scenario

#### 7. Kryzys migracyjny 2.0
- Migracja z Afryki/Bliskiego Wschodu do Europy
- Efekty na stability, populizm
- Reakcje polityczne

---

## FAZA 10: Lokalizacja
**Priorytet:** NISKI | **Zlozonosc:** Niska | **Pliki:** 2-4

### Pliki do stworzenia:
- `localisation/english/md2026_l_english.yml` - glowna lokalizacja
- `localisation/polish/md2026_l_polish.yml` - polskie tlumaczenie

### Zawartosc:
- Nazwa bookmarku i jego opis
- Opisy krajow w bookmarku
- Nazwy nowych national spirits
- Opisy nowych focusow
- Teksty eventow
- Nazwy nowych decyzji
- Tooltipy i opisy efektow

---

## FAZA 11: Testowanie i balans
**Priorytet:** NISKI | **Zlozonosc:** Srednia

### Checklist testowy:
- [ ] Gra nie crashuje przy ladowaniu submoda
- [ ] Bookmark 2026 wyswietla sie poprawnie
- [ ] Kazdy featured country mozna wybrac i zagrac
- [ ] Granice sa poprawne na 2026
- [ ] Liderzy krajow sa prawidlowi
- [ ] Wojny sa aktywne od startu
- [ ] NATO ma 32 czlonkow
- [ ] Technologie sa odpowiednie per kraj
- [ ] National spirits dzialaja
- [ ] Focus trees sie wyswietlaja i dzialaja
- [ ] Eventy sie triggeruja poprawnie
- [ ] AI zachowuje sie sensownie
- [ ] Brak errorrow w error.log
- [ ] Balans ekonomiczny (GDP, manpower, fabryki)
- [ ] Balans militarny (armie, floty, lotnictwo)

### Narzedzia testowe:
- Konsola HOI4: `tdebug`, `tag [TAG]`, `observe`
- `error.log` w Documents/Paradox Interactive/Hearts of Iron IV/logs/
- Scenario tests (jesli dotyczy)

---

## Lista krajow objetych submodem (pelna)

### Tier A - Pelna aktualizacja (mocarstwa):
USA, SOV, CHI, ENG, FRA, GER, RAJ, JAP, TUR, PER, BRA, UKR

### Tier B - Pelna aktualizacja (NATO + regionalne):
POL, ITA, SPR, CAN, ROM, HOL, BEL, NOR, DEN, POR, CZE, GRE,
HUN, ICE, LUX, BUL, CRO, ALB, LIT, LAT, EST, SLO, SLV, MNT,
FYR, FIN, SWE, ISR, SAU, NKO, KOR, AST

### Tier C - Czesciowa aktualizacja (konflikty):
SYR, EGY, BRM, SUD, YEM, UAE, ETH, SAF, TAI (Tajwan)

### Tier D - Minimalna aktualizacja (lider + ideologia):
Pozostale kraje NATO juz wyzej, plus BLR, KAZ, KYR, TAJ, UZB (CSTO),
ARM, GEO, MLV (Moldawia), SER, BOS, KOS, PAK, AFG

### Suma: ~70 krajow

---

## Harmonogram (szacunkowy)

| Faza | Czas pracy | Kamien milowy |
|------|------------|---------------|
| Faza 0 | 1-2h | Submod laduje sie w grze |
| Faza 1 | 4-8h | Poprawne granice na 2026 |
| Faza 2 | 10-20h | Kraje maja wlasciwych liderow i ustawienia |
| Faza 3 | 2-4h | Wojny sa aktywne |
| Faza 4 | 2-4h | Sojusze dzialaja |
| Faza 5 | 8-16h | Postaci sa kompletne |
| Faza 6 | 4-8h | Technologie ustawione |
| Faza 7 | 4-8h | National spirits dzialaja |
| Faza 8 | 20-40h | Focus trees gotowe |
| Faza 9 | 15-30h | Eventy dzialaja |
| Faza 10 | 4-8h | Lokalizacja gotowa |
| Faza 11 | 8-16h | Gra przetestowana |
| **SUMA** | **~80-165h** | **Pelna wersja** |

---

## Zasady commitow git

- Commit po kazdej zakonczocznej fazie
- Format: `[FAZA X] Krotki opis zmian`
- Przyklady:
  - `[FAZA 0] Infrastruktura submoda - descriptor, bookmark 2026`
  - `[FAZA 1] Granice i stany - Krym, Donbas, Syria`
  - `[FAZA 2] Historia krajow - mocarstwa (USA, SOV, CHI, UKR)`
  - `[FAZA 2] Historia krajow - kraje NATO`
  - `[FAZA 3] Konflikty aktywne - wojna rosyjsko-ukrainska`

---

## Notatki techniczne

### Jak dziala nadpisywanie plikow w HOI4:
1. Submod laduje sie PO glownym modzie (MD)
2. Pliki o identycznej sciezce nadpisuja oryginalne
3. `replace_path` w descriptor calkowicie zastepuje folder
4. Bez `replace_path` - pliki sie laczą (merge) lub nadpisuja po nazwie

### Wazne sciezki w MD:
- Ideologie: `common/ideologies/00_ideologies.txt` (5 grup: democratic, communism, fascism, neutrality, nationalist)
- Tagi krajow: `common/country_tags/00_countries.txt` (405 tagow)
- Startup effects: `common/scripted_effects/00_startup_effects.txt` (NATO array, etc.)
- Factions: `common/factions/templates/` (NATO, CSTO, EU, etc.)
- Bookmarks: `common/bookmarks/blitzkrieg.txt` (glowny bookmark)

### System ideologii MD (mapowanie):
- `democratic` = Zachod (conservatism, liberalism, socialism, Western_Autocracy)
- `communism` = Emerging/Autorytarny (Communist-State, Conservative, Autocracy, Vilayat_e_Faqih)
- `fascism` = Salafizm (Kingdom, Caliphate)
- `neutrality` = Non-aligned (rozne warianty)
- `nationalist` = Nacjonalizm (Nat_Autocracy, Nat_Fascism, Nat_Populism, Monarchist)
