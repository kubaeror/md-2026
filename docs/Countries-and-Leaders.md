# Countries & Leaders

This mod updates 66 countries with accurate January 2026 leaders, ideologies, and political configurations.

---

## Ideology System

Millennium Dawn uses a custom ideology system mapped onto HoI4's five base ideology groups:

| HoI4 Group | MD Label | Sub-ideologies |
|------------|----------|----------------|
| `democratic` | Western | conservatism, liberalism, socialism, Western_Autocracy |
| `communism` | Emerging/Authoritarian | Communist-State, Conservative, Autocracy, Vilayat_e_Faqih |
| `fascism` | Salafism | Kingdom, Caliphate |
| `neutrality` | Non-aligned | Various regional variants |
| `nationalist` | Nationalism | Nat_Autocracy, Nat_Fascism, Nat_Populism, Monarchist |

---

## Tier A — Major Powers

Full update with focus trees, national spirits, events, and detailed OOB. All 12 countries have shared focus tree branches.

| Country | Tag | Leader (2026) | Ideology | Notes |
|---------|-----|---------------|----------|-------|
| **United States** | USA | Donald Trump | nationalist / Nat_Populism | Second term, America First agenda |
| **Russia** | SOV | Vladimir Putin | communism / Autocracy | War in Ukraine, Western sanctions |
| **China** | CHI | Xi Jinping | communism / Autocracy | Taiwan tensions, economic slowdown |
| **United Kingdom** | ENG | Keir Starmer | democratic / socialism | Post-Brexit governance |
| **France** | FRA | Emmanuel Macron | democratic / liberalism | Final presidential term |
| **Germany** | GER | Friedrich Merz | democratic / conservatism | New chancellor, Zeitenwende |
| **India** | RAJ | Narendra Modi | communism / Conservative | Third term, rising power |
| **Japan** | JAP | Shigeru Ishiba | democratic / conservatism | Security normalization |
| **Turkey** | TUR | Recep Tayyip Erdogan | communism / Autocracy | Regional power projection |
| **Iran** | PER | M. Pezeshkian / Khamenei | communism / Vilayat_e_Faqih | Nuclear program, sanctions |
| **Brazil** | BRA | Lula da Silva | democratic / socialism | BRICS presidency, Amazon |
| **Ukraine** | UKR | Volodymyr Zelensky | democratic / liberalism | Wartime president, NATO aspirant |

---

## Tier B — NATO & Regional Powers

Full update with leaders, politics, military, alliances. Countries marked with * have shared focus tree branches.

| Country | Tag | Leader (2026) | Ideology |
|---------|-----|---------------|----------|
| Poland* | POL | Donald Tusk | democratic / liberalism |
| Italy* | ITA | Giorgia Meloni | nationalist / Nat_Populism |
| Spain | SPR | Pedro Sanchez | democratic / socialism |
| Canada* | CAN | Mark Carney | democratic / liberalism |
| Romania | ROM | Marcel Ciolacu | democratic / conservatism |
| Netherlands | HOL | Dick Schoof | democratic / conservatism |
| Belgium | BEL | Alexander De Croo | democratic / liberalism |
| Norway | NOR | Jonas Gahr Store | democratic / socialism |
| Denmark | DEN | Mette Frederiksen | democratic / socialism |
| Portugal | POR | Luis Montenegro | democratic / conservatism |
| Czechia | CZE | Petr Fiala | democratic / conservatism |
| Greece | GRE | Kyriakos Mitsotakis | democratic / conservatism |
| Hungary | HUN | Viktor Orban | nationalist / Nat_Populism |
| Iceland | ICE | Bjarni Benediktsson | democratic / conservatism |
| Luxembourg | LUX | Luc Frieden | democratic / conservatism |
| Bulgaria | BUL | Dimitar Glavchev | democratic / conservatism |
| Croatia | CRO | Andrej Plenkovic | democratic / conservatism |
| Albania | ALB | Edi Rama | democratic / socialism |
| Lithuania | LIT | Gintautas Paluckas | democratic / socialism |
| Latvia | LAT | Evika Silina | democratic / conservatism |
| Estonia | EST | Kristen Michal | democratic / liberalism |
| Slovakia | SLO | Robert Fico | nationalist / Nat_Populism |
| Slovenia | SLV | Robert Golob | democratic / liberalism |
| Montenegro | MNT | Milojko Spajic | democratic / liberalism |
| North Macedonia | FYR | Hristijan Mickoski | democratic / conservatism |
| Finland | FIN | Petteri Orpo | democratic / conservatism |
| Sweden | SWE | Ulf Kristersson | democratic / conservatism |
| Israel* | ISR | Benjamin Netanyahu | democratic / conservatism |
| Saudi Arabia* | SAU | Mohammed bin Salman | fascism / Kingdom |
| North Korea* | NKO | Kim Jong-un | communism / Communist-State |
| South Korea* | KOR | Han Duck-soo (acting) | democratic / conservatism |
| Australia* | AST | Anthony Albanese | democratic / socialism |

---

## Tier C — Conflict Zones

Partial update — leaders, borders, active wars. Countries marked with * have shared focus tree branches.

| Country | Tag | Leader (2026) | Context |
|---------|-----|---------------|---------|
| Syria* | SYR | Ahmad al-Sharaa (HTS) | Post-Assad, Dec 2024 regime change |
| Egypt* | EGY | Abdel Fattah el-Sisi | Economic crisis, BRICS member |
| Myanmar | BRM | Min Aung Hlaing | Military junta, civil war |
| Sudan | SUD | Abdel Fattah al-Burhan | Civil war (SAF vs RSF) |
| Yemen | YEM | Houthi control | Divided country |
| UAE | UAE | Mohammed bin Zayed | Abraham Accords, BRICS |
| Ethiopia | ETH | Abiy Ahmed | Post-Tigray, BRICS+ |
| South Africa | SAF | Cyril Ramaphosa | BRICS host |
| Taiwan* | TAI | Lai Ching-te | Cross-strait tensions |

---

## Tier D — Minimal Update

Leader and ideology only, using generic OOB and basic setup.

| Country | Tag | Leader (2026) |
|---------|-----|---------------|
| Belarus | BLR | Alexander Lukashenko |
| Kazakhstan | KAZ | Kassym-Jomart Tokayev |
| Kyrgyzstan | KYR | Sadyr Japarov |
| Tajikistan | TAJ | Emomali Rahmon |
| Uzbekistan | UZB | Shavkat Mirziyoyev |
| Armenia | ARM | Nikol Pashinyan |
| Georgia | GEO | Bidzina Ivanishvili (de facto) |
| Moldova | MLV | Maia Sandu |
| Serbia | SER | Aleksandar Vucic |
| Bosnia | BOS | Rotating presidency |
| Kosovo | KOS | Albin Kurti |
| Pakistan | PAK | Shehbaz Sharif |
| Afghanistan | AFG | Taliban (Hibatullah Akhundzada) |

---

## Country History File Format

Each country's `history/countries/TAG - Name.txt` file contains the original MD `2000.1.1` block followed by a new `2026.1.1` block:

```
capital = STATE_ID

2000.1.1 = {
    # ... original MD content (unchanged) ...
}

2026.1.1 = {
    set_politics = {
        ruling_party = ideology
        last_election = "2024.11.5"
        election_frequency = 48
        elections_allowed = yes
    }
    set_popularities = {
        democratic = 45
        communism = 5
        fascism = 0
        neutrality = 10
        nationalist = 40
    }
    create_country_leader = { ... }
    oob = "TAG_2026"
    set_technology = { ... }
    add_ideas = { ... }
}
```

The `2026.1.1` block only contains what **changes** from the 2000 start. The game engine applies it as an overlay when the 2026 bookmark is selected.
