# Millennium Dawn 2026 Rework - Roadmap rozbudowy

## Stan obecny

Submod dodaje bookmark 2026.1.1 do base modu Millennium Dawn. Aktualna zawartosc:
- 57 focus trees (~451k linii), 23 krajow z pelnym custom contentem
- 191 eventow w 28 plikach, 11 lancuchow tematycznych (Ukraina, Tajwan, Bliski Wschod, BRICS, NATO, wybory, tech, cyber, proxy, demografia, klimat)
- 56 decyzji w 7 kategoriach (sankcje, NATO, geopolityka, modernizacja wojskowa, ekonomia, nuklearne, cyber)
- 60+ national spirits, 72 country history files, 5-tierowy system technologii
- 23 pliki characters z liderami 2026, 72 pliki OOB
- 18 plikow lokalizacji (angielski)

Znane problemy:
- 9 bledow skladni (SYN001) w focus trees - array syntax do weryfikacji
- Duplikat klucza md2026_sov_war_economy
- Brak custom doktryn, GUI, technologii - bazuje na base modzie
- Brak polskiej lokalizacji

---

## FAZA 1: Naprawy krytyczne

Priorytet: KRYTYCZNY
Status: UKONCZONA (2026-03-17)

Wyniki weryfikacji:
- Bledy SYN001 (^ array syntax) - FALSE POSITIVES. Operator ^ jest poprawnym syntax HoI4 1.17,
  uzywany setki razy w base modzie (np. Belarus.txt, Czech decisions).
- Duplikat md2026_sov_war_economy - FALSE POSITIVE. Klucze sa rozne:
  md2026_sov_war_economy (spirit) vs md2026_sov_war_economy_decision (decyzja).
- OOB files - OK. history/units/ nie ma replace_path, HoI4 laduje z obu lokalizacji.
  Base mod dostarcza USA_2000_nsb i pochodne.

Zrealizowane (sesje 2026-03-12 i 2026-03-17):
- Usunieto 15 blednych replace_path z descriptor.mod (zostaly tylko bookmarks i history/states)
- Naprawiono cudzyslow w usa.txt:40032
- Dodano lokalizacje 56 decyzji i 8 kategorii (md2026_decisions_l_english.yml)

---

## FAZA 2: Rozszerzenie eventow

Priorytet: WYSOKI
Cel: Dodac nowe lancuchy eventow pokrywajace kluczowe scenariusze geopolityczne 2026-2030

### 2.1 Eskalacja tajwanska (5-7 eventow)

Lancuch eventow modelujacy potencjalny kryzys wokol Tajwanu.

Eventy:
1. md2026_taiwan_esc.1 - "Prowokacje militarne na Ciesninie" - CHI prowadzi cwiczenia wojskowe, TAI podnosi alert
2. md2026_taiwan_esc.2 - "Blokada morska Tajwanu" - CHI ogłasza strefę wykluczenia, handel morski sparalizowany
3. md2026_taiwan_esc.3 - "Kryzys międzynarodowy" - USA/JAP reaguja, UNSC zwoluje sesje nadzwyczajna
4. md2026_taiwan_esc.4 - "Ultimatum Pekinu" - CHI zadajo reinkorporacji, TAI musi odpowiedziec
5. md2026_taiwan_esc.5a - "Inwazja na Tajwan" - jesli TAI odrzuci ultimatum i USA nie interweniuje
6. md2026_taiwan_esc.5b - "Dyplomatyczne rozwiazanie" - jesli mediacja sie powiedzie
7. md2026_taiwan_esc.6 - "Nowy status quo" - konsekwencje dlugoterminowe

Triggery: Odpalaja sie po 2027 jesli CHI zakonczy odpowiednie focusy i TAI nie jest w fakcji z USA.
Mechaniki: Country flags kontrolujace sciezke, war goals, opinion modifiers, national spirits.
Plik: events/md2026_taiwan_escalation.txt
Lokalizacja: localisation/english/md2026_taiwan_esc_l_english.yml

### 2.2 Scenariusz upadku Rosji (5-7 eventow)

Lancuch eventow modelujacy potencjalny rozpad Rosji po przedluzajacej sie wojnie.

Eventy:
1. md2026_sov_collapse.1 - "Wyczerpanie wojenne" - SOV traci stabilnosc ponizej 20%, bunty w armii
2. md2026_sov_collapse.2 - "Protesty w Moskwie" - masowe demonstracje, siły bezpieczenstwa wahaja sie
3. md2026_sov_collapse.3 - "Zamach stanu" - generałowie probuja obalic rzad, 50/50 sukces/porazka
4. md2026_sov_collapse.4a - "Nowy rezim wojskowy" - junta przejmuje wladze, zawieszenie broni z UKR
5. md2026_sov_collapse.4b - "Chaos i secesja" - zamach sie nie udal, regiony ogłaszaja niepodleglosc
6. md2026_sov_collapse.5 - "Kaukaz w ogniu" - Czeczenia, Dagestan, Gruzja reaguja
7. md2026_sov_collapse.6 - "Nowy porzadek" - konsekwencje miedzynarodowe, BRICS w kryzysie

Triggery: SOV w wojnie > 3 lata, stabilnosc < 20%, war support < 15%.
Mechaniki: Release nations, civil war, faction dissolution.
Plik: events/md2026_russia_collapse.txt

### 2.3 Arabska Wiosna 2.0 (4-6 eventow)

Fala protestow w krajach arabskich inspirowana zmianami w Syrii.

Eventy:
1. md2026_arab2.1 - "Iskra w Kairze" - protesty w Egipcie po wzroscie cen zywnosci
2. md2026_arab2.2 - "Fala protestow" - rozszerza sie na Algerie, Tunezje, Jordanie
3. md2026_arab2.3a - "Represje" - rzad tlumi protesty silą - stabilnosc -, war support +
4. md2026_arab2.3b - "Ustepstwa" - rzad idzie na kompromis - stabilnosc +, PP -
5. md2026_arab2.4 - "Zmiana rezimu" - jesli stabilnosc spadnie ponizej progu
6. md2026_arab2.5 - "Reakcja regionalna" - SAU/UAE interweniuja, Turcja wspiera opozycje

Triggery: Po 2027, SYR zmienila rzad, EGY stabilnosc < 40%.
Plik: events/md2026_arab_spring2.txt

### 2.4 Kryzys migracyjny EU (4-5 eventow)

Presja migracyjna na granicach EU i jej polityczne konsekwencje.

Eventy:
1. md2026_eu_migr.1 - "Fala migracyjna" - wojna/niestabilnosc w Afryce/Bliskim Wschodzie generuje fale
2. md2026_eu_migr.2 - "Polaryzacja polityczna" - partie antyimigranckie zyskuja poparcie w EU
3. md2026_eu_migr.3a - "Reforma Schengen" - EU zaciesnia kontrole graniczne, zachowuje wolny ruch
4. md2026_eu_migr.3b - "Zawieszenie Schengen" - kraje zamykaja granice jednostronnie
5. md2026_eu_migr.4 - "Nowa polityka azylowa" - dlugoterminowe konsekwencje dla EU

Triggery: Aktywny konflikt w Afryce/Bliskim Wschodzie, > 2 kraje EU z niestabilnoscia.
Plik: events/md2026_eu_migration.txt

### 2.5 Kryzys Indo-Pakistanski (5-6 eventow)

Eskalacja napiec miedzy Indiami a Pakistanem.

Eventy:
1. md2026_indopak.1 - "Incydent w Kaszmirze" - atak terrorystyczny lub starcie graniczne
2. md2026_indopak.2 - "Mobilizacja" - obie strony mobilizuja sily na granicy
3. md2026_indopak.3 - "Grozba nuklearna" - PAK podnosi alert nuklearny
4. md2026_indopak.4a - "Ograniczony konflikt" - starcia na linii kontroli, bez eskalacji nuklearnej
5. md2026_indopak.4b - "Mediacja miedzynarodowa" - USA/CHI wymuszaja zawieszenie broni
6. md2026_indopak.5 - "Nowy status quo" - napiety pokoj lub dalsze zmiany graniczne

Triggery: Po 2027, RAJ zakonczyla focusy militarne, PAK niestabilny.
Plik: events/md2026_indo_pak.txt

### 2.6 Dodatkowe wybory (8-10 eventow)

Cykle wyborcze dla krajow ktorych brak w obecnym systemie.

Eventy:
- md2026_elect_ext.1 - Argentyna 2027 (post-Milei: kontynuacja reform vs powrot peronizmu)
- md2026_elect_ext.2 - Turcja 2028 (Erdogan vs opozycja CHP)
- md2026_elect_ext.3 - Australia 2028 (Labor vs Coalition)
- md2026_elect_ext.4 - Kanada 2029 (Liberals vs Conservatives vs NDP)
- md2026_elect_ext.5 - Indie 2029 (BJP vs INDIA alliance)
- md2026_elect_ext.6 - Indonezja 2029 (post-Prabowo)
- md2026_elect_ext.7 - RPA 2029 (ANC vs DA vs MK vs EFF)
- md2026_elect_ext.8 - Meksyk 2030 (MORENA vs opozycja)

Kazdy event: 2-3 opcje z roznymi konsekwencjami politycznymi (zmiana ideologii, modyfikatory, liderzy).
Plik: events/md2026_elections_extended.txt

---

## FAZA 3: Nowe focus trees

Priorytet: WYSOKI
Cel: Dodac pelne focus trees dla 6 kolejnych krajow, pokrywajac kluczowe regiony swiata

Kazdy focus tree ma strukture:
- 5 galezi: polityka wewnetrzna, wojskowosc, ekonomia, dyplomacja, technologia/spoleczenstwo
- ~25-30 focusow na galez, ~130-150 focusow lacznie
- Mutually exclusive paths w kazdej galezi
- Pre-completed focusy odzwierciedlajace stan na 2026.1.1
- Integracja z istniejacymi eventami i decyzjami

### 3.1 Pakistan (PAK)

Kontekst: Potega nuklearna, rywalizacja z Indiami, sojusz z Chinami, niestabilnosc wewnetrzna.

Galaz polityczna:
- Sciezka wojskowa: przewrot wojskowy, junta, stabilizacja sila
- Sciezka demokratyczna: reformy, wolne media, walka z korupcja
- Wspólne: Kaszmir (eskalacja vs dialog), relacje z Afganistanem

Galaz wojskowa:
- Modernizacja armii (czolgi Al-Khalid 2, JF-17 Block 3)
- Program nuklearny (miniaturyzacja glowic, rakiety Shaheen-III)
- Wspolpraca z Chinami (wspolna produkcja, bazy)
- Antyterroryzm (operacje w FATA/Beludzystan)

Galaz ekonomiczna:
- Program MFW vs odrzucenie pomocy
- CPEC 2.0 (rozszerzenie korytarza chinskiego)
- Eksport tekstylny i IT
- Reforma podatkowa

Galaz dyplomatyczna:
- Sojusz z Chinami (SCO, BRI)
- Normalizacja z Indiami (handel, woda)
- Relacje z USA (balansowanie)
- Swiat islamski (OIC, Turcja, SAU)

Plik: common/national_focus/pakistan.txt
Characters: common/characters/PAK.txt (nowy)
History: history/countries/PAK - Pakistan.txt (aktualizacja)
AI plan: common/ai_strategy_plans/md2026_ai_plans.txt (rozszerzenie)

### 3.2 Indonezja (INS)

Kontekst: Najwiekszy kraj muzulmanski, ASEAN leader, nowa stolica Nusantara, zasoby niklu.

Galaz polityczna:
- Demokratyczna konsolidacja vs autorytarny drift (Prabowo)
- Wolnosc mediow vs kontrola informacji
- Relacje centrum-regiony (Papua, Aceh)

Galaz wojskowa:
- Modernizacja marynarki (okrety podwodne, fregaty)
- Obrona Morza Poludniowochinskiego (spor z CHI o Natuna)
- Sily specjalne (Kopassus)
- Przemysl obronny (PT Pindad, PT PAL)

Galaz ekonomiczna:
- Nusantara (budowa nowej stolicy - ogromny projekt infrastrukturalny)
- Downstreaming niklu (zakaz eksportu rudy, budowa hutnictwa)
- Gospodarka cyfrowa (Gojek, Tokopedia, unicorny)
- Turystyka (Bali, Labuan Bajo)

Galaz dyplomatyczna:
- Przywodztwo ASEAN (centralna rola w regionie)
- Balansowanie USA-Chiny (wolnosc zeglugi vs inwestycje chinskie)
- G20 i Global South voice
- Wspólpraca z Australia (Timor Leste, stabilnosc)

Plik: common/national_focus/indonesia.txt (rozszerzenie istniejacego)
Characters: common/characters/INS.txt (nowy)

### 3.3 Meksyk (MEX)

Kontekst: Sasiad USA, kartele narkotykowe, nearshoring, USMCA, migracja.

Galaz polityczna:
- MORENA kontynuacja vs opozycja
- Reforma sadownictwa (kontrowersyjna reforma 2024)
- Walka z korupcja vs patronat

Galaz wojskowa:
- Wojna z kartelami (Sinaloa, CJNG, Los Zetas)
- Gwardia Narodowa (militaryzacja bezpieczenstwa)
- Wspolpraca z USA (DEA, extradycje) vs suwerennosc
- Kontrola granic poludniowych

Galaz ekonomiczna:
- Nearshoring boom (przenoszenie fabryk z Chin do Meksyku)
- USMCA renegocjacja 2026
- Pemex i reforma energetyczna
- Turystyka i remittance

Galaz dyplomatyczna:
- Relacje z USA (Trump tariffs, mur, migracja)
- Ameryka Lacinska (CELAC, regionalne przywodztwo)
- Dywersyfikacja (EU, Azja)
- Kryzys migracyjny (tranzyty z Ameryki Srodkowej)

Plik: common/national_focus/mexico.txt (rozszerzenie istniejacego)

### 3.4 RPA (SAF)

Kontekst: Potega regionalna Afryki, kryzys energetyczny, BRICS, nierównosci.

Galaz polityczna:
- Koalicja rzadowa (ANC-DA GNU vs rozpad koalicji)
- Populizm (EFF, MK Party)
- Walka z korupcja (state capture, komisja Zondo)
- Reforma gruntow

Galaz wojskowa:
- Operacje pokojowe AU (Mozambik, Kongo)
- Modernizacja SANDF (przestarzaly sprzet)
- Przemysl obronny (Denel)
- Bezpieczenstwo wewnetrzne (przestepczosc)

Galaz ekonomiczna:
- Load shedding (kryzys Eskom, energetyka)
- Gornictwo (platyna, zloto, mangan, lit)
- Infrastruktura (Transnet, porty)
- Nierównosci (BEE, reforma rynku pracy)

Galaz dyplomatyczna:
- BRICS+ (gospodarz, most miedzy Global South a Zachodem)
- Afryka (AU, SADC, mediacje)
- Neutralnosc (Rosja-Ukraina - kontrowersyjna pozycja)
- Handel (AGOA z USA, EPA z EU)

Plik: common/national_focus/south_africa.txt (nowy)
Characters: common/characters/SAF.txt (aktualizacja)

### 3.5 Argentyna (ARG)

Kontekst: Reformy Milei, hiperinflacja, Falklandy, Mercosur.

Galaz polityczna:
- Kontynuacja reform Milei (deregulacja, ciecla budzetowe)
- Opozycja peronistowska (powrot populizmu)
- Reforma konstytucyjna
- Protesty spoleczne

Galaz wojskowa:
- Modernizacja sil zbrojnych (od lat zaniedbywanych)
- Falklandy/Malwiny (dyplomatyczna presja vs eskalacja)
- Antarktyka (roszczenia, bazy)
- Wspolpraca NATO+ (sojusz z Zachodem)

Galaz ekonomiczna:
- Dollaryzacja (przejscie na dolara vs peso)
- Vaca Muerta (shale oil/gas - ogromne zloze)
- Lit (trojkat litowy z Chile i Boliwia)
- Eksport rolny (soja, wolowina, pszenica)

Galaz dyplomatyczna:
- Zwrot prozachodni (Milei: USA, Izrael)
- Mercosur (renegocjacja vs wyjscie)
- EU-Mercosur FTA
- Rywalizacja z Brazylia

Plik: common/national_focus/argentina.txt (rozszerzenie istniejacego lub nowy)

### 3.6 Wietnam (VIN)

Kontekst: Bamboo diplomacy, boom produkcyjny, Morze Poludniowochińskie, balansowanie mocarstw.

Galaz polityczna:
- Reforma partii komunistycznej (antykorupcja "piec rozpalony")
- Liberalizacja gospodarcza vs kontrola polityczna
- Sukcesja przywodztwa

Galaz wojskowa:
- Morze Poludniowochinskie (spor z CHI, wyspy Spratly/Paracele)
- Modernizacja marynarki (okrety podwodne Kilo, fregaty Gepard)
- Obrona cyberprzestrzeni
- Przemysl obronny (Viettel)

Galaz ekonomiczna:
- Manufacturing hub (Samsung, Intel, Apple - przenoszenie z Chin)
- Semiconductors (fabryki chipow)
- Infrastruktura (kolej szybka polnoc-poludnie)
- Turystyka i eksport

Galaz dyplomatyczna:
- Bamboo diplomacy (balansowanie USA-Chiny-Rosja)
- ASEAN (wspolpraca z Indonezja)
- Comprehensive Strategic Partnership z USA (2023+)
- Historyczne wiezi z Rosja (bron, energia)

Plik: common/national_focus/vietnam.txt (nowy)
Characters: common/characters/VIN.txt (nowy)

---

## FAZA 4: Systemy gameplay

Priorytet: SREDNI
Cel: Dodac nowe mechaniki rozgrywki pogłebiajace strategie geopolityczna

### 4.1 Rozszerzony system proxy wars

Obecny system (3 decyzje: proxy_support_sov/usa/per) jest minimalny.
Rozszerzenie o pelny system wojen zaslepionych.

Nowe decyzje (15-20):
- Wsparcie Hezbollahu (PER/SYR) - wplywa na konflikt z ISR
- Wsparcie Houthis (PER) - blokada Morza Czerwonego, wplywa na handel
- Wsparcie Wagnera/Africa Corps (SOV) - wplyw w Sahelu, Mali, Burkina Faso, Niger
- Wsparcie opozycji syryjskiej (TUR/USA) - wplyw na SYR
- Wsparcie kurdow (USA) - antagonizuje TUR
- Szkolenie sil ukrainskich (USA/ENG/FRA) - wzmacnia UKR
- Dostawy broni do Tajwanu (USA/JAP) - antagonizuje CHI
- Operacje w Birmie (CHI) - wsparcie jednej ze stron
- Cyber proxy (CHI/SOV/USA) - ataki przez trzecie kraje

Kazda decyzja:
- Koszt: 50-100 PP
- Czas: 90-180 dni
- Efekt: bonus do ataku/obrony proxy, opinion modifier, event chain
- Ryzyko: 10-30% szans na ujawnienie, kryzys dyplomatyczny

Nowe ideas (10-15):
- md2026_proxy_hezbollah_support, md2026_proxy_wagner_africa, etc.
- Kazda daje bonusy do wpływu w regionie + kary do opinii miedzynarodowej

Pliki:
- common/decisions/md2026_proxy_expanded.txt
- common/ideas/md2026_proxy_ideas.txt (rozszerzenie)
- events/md2026_proxy_events.txt
- localisation/english/md2026_proxy_expanded_l_english.yml

### 4.2 Rozszerzony system cyber warfare

Obecny system (3 decyzje) jest podstawowy. Rozszerzenie o pelny system cyberoperacji.

Nowe decyzje (10-12):
- Ofensywne:
  - Atak na infrastrukture energetyczna (damage fabryki)
  - Atak na system finansowy (damage ekonomii)
  - Kradziez technologii wojskowej (bonus research)
  - Dezinformacja/wplyw na wybory (destabilizacja polityczna)
  - Atak na systemy C2 (obnizenie org armii wroga)

- Defensywne:
  - Cyber shield (redukcja damage z atakow)
  - Cyber counterintelligence (wykrywanie atakow)
  - Szkolenie kadr cyber (staly bonus)
  - Miedzynarodowa wspolpraca cyber (NATO Cyber Defence)

- Specjalne:
  - Stuxnet 2.0 (atak na program nuklearny - specyficznie PER/NKO)
  - False flag cyber (atak wyglada jakby pochodzil z innego kraju)

Mechaniki:
- Nowy modifier: cyber_capability (0-100, wplywa na skutecznosc ataków)
- Tier system: basic -> intermediate -> advanced -> elite
- Cooldowny miedzy operacjami
- Risk/reward: im wiekszy atak, tym wieksza szansa wykrycia

Pliki:
- common/decisions/md2026_cyber_expanded.txt
- common/ideas/md2026_cyber_ideas.txt (rozszerzenie)
- events/md2026_cyber_events.txt (rozszerzenie)
- common/scripted_effects/md2026_cyber_effects.txt
- localisation/english/md2026_cyber_expanded_l_english.yml

### 4.3 System cyklu ekonomicznego

Nowy system modelujacy globalne cykle koniunkturalne.

4 stany ekonomii:
1. BOOM - +10% factory output, +5% construction speed, -10% consumer goods
2. STABILNY - brak modyfikatorow (stan domyslny)
3. RECESJA - -10% factory output, -5% construction speed, +5% consumer goods, -5% stability
4. KRYZYS - -20% factory output, -10% construction speed, +15% consumer goods, -15% stability, -10% PP

Przejscia (monthly check):
- BOOM -> STABILNY: 5% base chance + modifiers (wojna, sankcje, deficyt)
- STABILNY -> RECESJA: 3% base + modifiers
- RECESJA -> KRYZYS: 5% base, jesli recesja trwa > 12 miesiecy
- KRYZYS -> RECESJA: 3% base + modifiers (stymulacja, reformy)
- RECESJA -> STABILNY: 3% base + modifiers
- STABILNY -> BOOM: 2% base (niskie szanse, wymaga dobrych warunkow)

Decyzje gracza:
- "Pakiet stymulacyjny" - 100 PP, +20% szans na wyjscie z recesji, -50 PP/miesiac przez 6 miesiecy
- "Program oszczednosciowy" - 0 PP, +10% szans na wyjscie z recesji, -5% stability na 12 miesiecy
- "Luzowanie ilosciowe" - 75 PP, natychmiast +5% factory output, ryzyko inflacji
- "Reforma podatkowa" - 150 PP, trwaly +3% factory output, -2% stability
- "Nacjonalizacja przemyslu" - 100 PP, +15% factory output, -30% trade opinion, -10% stability

Eventy:
- "Globalny crash gieldowy" - triggeruje recesje w wielu krajach naraz
- "Banka spekulacyjna" - boom zakonczony nagla recesja
- "Inflacja" - konsekwencja nadmiernej stymulacji
- "Bankructwo panstwowe" - jesli kryzys trwa > 24 miesiace

Pliki:
- common/scripted_effects/md2026_economy_cycle.txt
- common/scripted_triggers/md2026_economy_triggers.txt (rozszerzenie)
- common/decisions/md2026_economy_cycle.txt
- common/ideas/md2026_economy_cycle_ideas.txt
- events/md2026_economy_cycle.txt
- localisation/english/md2026_economy_cycle_l_english.yml

---

## FAZA 5: AI i balans

Priorytet: WYSOKI
Cel: Zapewnic ze AI sensownie korzysta z nowego contentu i gra jest zbalansowana

### 5.1 AI strategy plans

Kazdy kraj z custom focus tree potrzebuje AI planu ktory mowi AI w jakiej kolejnosci
realizowac focusy. Bez tego AI losowo wybiera focusy co prowadzi do nierealistycznych
scenariuszy.

Plany do dodania/rozszerzenia:
- PAK: priorytet - stabilnosc wewnetrzna, potem wojskowosc, potem Kaszmir
- INS: priorytet - Nusantara, potem ekonomia, potem morze
- MEX: priorytet - kartele, potem nearshoring, potem dyplomacja
- SAF: priorytet - load shedding, potem BRICS, potem AU
- ARG: priorytet - inflacja, potem Vaca Muerta, potem dyplomacja
- VIN: priorytet - manufacturing, potem morze, potem balansowanie

Aktualizacja istniejacych planow:
- Wszystkie 23 kraje z focus trees - review i tuning

Plik: common/ai_strategy_plans/md2026_ai_plans.txt (rozszerzenie)

### 5.2 AI strategy (dyplomacja i wojskowosc)

Nowe strategie AI dla nowych krajow:
- PAK: antagonize RAJ (200), befriend CHI (150), befriend TUR (100), cautious USA
- INS: neutral wobec CHI/USA, befriend AST (100), protect Natuna
- MEX: befriend USA (100 ale warunkowe), neutral LATAM
- SAF: neutral, befriend BRICS (100), protect Southern Africa
- ARG: befriend USA (100, jesli Milei), antagonize ENG (Falklandy, warunkowe)
- VIN: cautious CHI (befriend 50 ale antagonize 50), befriend USA (75)

Plik: common/ai_strategy/md2026_ai_strategies.txt (rozszerzenie)

### 5.3 Balans modyfikatorow

Systematyczny przeglad:
- Wszystkie national spirits: czy bonusy/kary sa proporcjonalne?
- Decyzje: czy koszty PP sa sensowne? Czy AI moze sobie na nie pozwolic?
- Events: czy MTTH (mean time to happen) jest realistyczne? (nie za czesto, nie za rzadko)
- Focus trees: czy 70 dni na focus jest ok? Czy reward focusow jest zbalansowany?

Benchmarki:
- Observe mode 10 lat (2026-2036) - czy swiat wyglada realistycznie?
- Czy USA/CHI/SOV sa nadal mocarstwami po 10 latach?
- Czy mali gracze (TAI, UKR, ISR) przetrwaja?
- Czy AI korzysta z decyzji i eventow?

---

## FAZA 6: Polish i prezentacja

Priorytet: NISKI
Cel: Poprawa jakosci zycia gracza i dostosowalnosci moda

### 6.1 Newspaper events (global news)

Duze, klimatyczne eventy typu "breaking news" ze specjalnym formatowaniem.

Eventy (10-15):
- "Test nuklearny wstrzasa swiatem" - kraj uzyskal bron nuklearna
- "Historyczne porozumienie pokojowe" - zakonczenie duzego konfliktu
- "Sojusz sie rozpadl" - kraj opuscil fakcje
- "Zamach stanu!" - przewrot w waznym kraju
- "Globalny crash gieldowy" - poczatek kryzysu ekonomicznego
- "Wynaleziono sztuczna inteligencje ogolna" - przelom technologiczny
- "Czlowiek na Marsie" - osiagniecie kosmiczne
- "Pandemia" - nowa choroba zakazna
- "Katastrofa klimatyczna" - ekstremalny event pogodowy
- "Cyberatak sparalizowal kraj" - masowy atak na infrastrukture

Plik: events/md2026_newspaper.txt

### 6.3 Custom loading screen tips

Porady i ciekawostki wyswietlane podczas ladowania.

Przykladowe tipy (30):
- "W 2026 roku NATO liczy 32 czlonkow, wliczajac Finlandie i Szwecje."
- "BRICS+ rozszerzyl sie o Egipt, Etiopie, Iran, UAE i Arabie Saudyjska w 2024."
- "Pamiętaj o decyzjach sankcyjnych - moga znaczaco oslabic gospodarke wroga."
- "Fokus na cyberwojna moze dac Ci przewage technologiczna bez wypowiadania wojny."
- "AI bedzie podazac za historycznymi sciezkami focusow jesli nie zmienisz ustawien gry."

Plik: common/loading_screen_tips/md2026_tips.txt
Lokalizacja: localisation/english/md2026_tips_l_english.yml

### 6.4 Alternatywne bookmarki

Dodatkowe scenariusze startowe obok glownego 2026.1.1.

Bookmark 1: "Taiwan Crisis 2027" (2027.6.1)
- CHI przygotowuje inwazje, flota zmobilizowana
- TAI w pelnej gotowosci, USA deployed w regionie
- JAP i KOR w alertach
- Polecane kraje: CHI, TAI, USA, JAP

Bookmark 2: "Russian Collapse 2028" (2028.1.1)
- SOV z krytycznym wyczerpaniem wojennym, stability < 15%
- Regiony na skraju secesji
- UKR odzyskuje terytoria
- Polecane kraje: SOV, UKR, USA, CHI

Bookmark 3: "Middle East Inferno 2026" (2026.6.1)
- PER uzyskal bron nuklearna
- ISR w wojnie wielofrontowej
- SAU interweniuje
- Polecane kraje: ISR, PER, SAU, USA

Pliki:
- common/bookmarks/md2026_taiwan_crisis.txt
- common/bookmarks/md2026_russian_collapse.txt
- common/bookmarks/md2026_mideast_inferno.txt
- history/countries/* (warianty dla kazdego bookmarku - date blocks)
- localisation/english/md2026_bookmarks_l_english.yml

---

## Podsumowanie

| Faza | Priorytet | Nowe pliki | Zmodyfikowane pliki | Nowe eventy | Nowe focusy | Nowe decyzje |
|------|-----------|-----------|-------------------|------------|------------|-------------|
| 1 | KRYTYCZNY | 0 | ~12 | 0 | 0 | 0 |
| 2 | WYSOKI | 6-8 | 2-3 loc | ~40 | 0 | 0 |
| 3 | WYSOKI | 5-8 | 3-5 | 0 | ~800 | 0 |
| 4 | SREDNI | 8-12 | 3-5 | ~20 | 0 | ~35 |
| 5 | WYSOKI | 0 | 2-3 | 0 | 0 | 0 |
| 6 | NISKI | 10-15 | 5-8 | ~25 | 0 | 0 |
| **LACZNIE** | | **~35-50** | **~20-30** | **~85** | **~800** | **~35** |
