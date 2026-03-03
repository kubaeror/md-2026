# Alliances & Factions

The 2026 bookmark sets up all major real-world alliances and international organizations as HoI4 factions. These are configured via scripted effects in `common/scripted_effects/md2026_startup_effects.txt`, triggered on game start through `common/on_actions/md2026_on_actions.txt`.

---

## NATO (32 members)

The North Atlantic Treaty Organization with its 2026 membership, including Finland (2023) and Sweden (2024):

| Region | Members |
|--------|---------|
| **North America** | USA, CAN |
| **Western Europe** | ENG, FRA, GER, ITA, SPR, HOL, BEL, LUX, POR, ICE, NOR, DEN |
| **Southern Europe** | GRE, TUR, ALB, MNT, FYR, CRO, SLV |
| **Central Europe** | POL, CZE, HUN, ROM, BUL, SLO |
| **Baltic** | EST, LAT, LIT |
| **Nordic** | FIN, SWE |

**Implementation**: Uses MD's existing NATO faction system. The startup effect adds all members to the faction and sets up the alliance structure.

---

## CSTO (Collective Security Treaty Organization)

| Members | Notes |
|---------|-------|
| SOV (Russia) | Leader |
| BLR (Belarus) | |
| KAZ (Kazakhstan) | |
| KYR (Kyrgyzstan) | |
| TAJ (Tajikistan) | |

**Note**: Armenia (ARM) officially froze its CSTO membership in 2024 and is **not** included.

---

## European Union (27 members)

| Region | Members |
|--------|---------|
| **Founders** | GER, FRA, ITA, HOL, BEL, LUX |
| **Western** | SPR, POR, IRL |
| **Nordic** | FIN, SWE, DEN |
| **Central** | POL, CZE, HUN, SLO, AUS |
| **Southeast** | ROM, BUL, CRO, SLV, GRE, CYP |
| **Baltic** | EST, LAT, LIT |
| **Other** | MLT |

---

## BRICS+ (2024 Expansion)

The expanded BRICS bloc as of January 2024:

| Member | Region |
|--------|--------|
| CHI (China) | East Asia |
| SOV (Russia) | Eurasia |
| RAJ (India) | South Asia |
| BRA (Brazil) | South America |
| SAF (South Africa) | Africa |
| EGY (Egypt) | Middle East/Africa |
| ETH (Ethiopia) | Africa |
| PER (Iran) | Middle East |
| UAE | Middle East |
| SAU (Saudi Arabia) | Middle East |

---

## AUKUS

Security pact focused on Indo-Pacific:

| Member | Role |
|--------|------|
| USA | Nuclear submarine technology provider |
| ENG (UK) | Nuclear submarine technology provider |
| AST (Australia) | Recipient, regional presence |

---

## Shanghai Cooperation Organisation (SCO)

| Member | Notes |
|--------|-------|
| CHI (China) | Co-founder |
| SOV (Russia) | Co-founder |
| RAJ (India) | Full member since 2017 |
| KAZ (Kazakhstan) | Founding member |
| KYR (Kyrgyzstan) | Founding member |
| TAJ (Tajikistan) | Founding member |
| UZB (Uzbekistan) | Founding member |
| PER (Iran) | Full member since 2023 |
| BLR (Belarus) | Full member since 2024 |

---

## Quad (Quadrilateral Security Dialogue)

| Member | Role |
|--------|------|
| USA | Indo-Pacific strategy |
| JAP (Japan) | Regional security |
| RAJ (India) | Regional power |
| AST (Australia) | Regional presence |

---

## Abraham Accords

Normalization agreements between Israel and Arab states:

| Parties | Year Signed |
|---------|------------|
| ISR + UAE | 2020 |
| ISR + BHR (Bahrain) | 2020 |
| ISR + MAR (Morocco) | 2020 |
| ISR + SUD (Sudan) | 2020 |

---

## Active Wars (January 2026)

Wars are declared via scripted effects at game start:

| Conflict | Attacker | Defender | Type |
|----------|----------|----------|------|
| Russo-Ukrainian War | SOV | UKR | `declare_war_on` |
| Sudan Civil War | SUD internal | — | Civil war mechanics |
| Myanmar Civil War | BRM internal | — | Civil war mechanics |
| Yemen (Houthi control) | — | — | Represented through ownership |

---

## Diplomatic Relations

Country history files set initial opinion modifiers to reflect 2026 diplomatic realities:

- **Western sanctions on Russia** — Negative opinion modifiers between NATO countries and SOV
- **US-Cuba sanctions** — Negative opinion between USA and CUB
- **Iran sanctions** — Negative opinion between Western countries and PER
- **China-Taiwan tensions** — Negative opinion between CHI and TAI
- **Abraham Accords** — Positive opinion between ISR and signatory states
