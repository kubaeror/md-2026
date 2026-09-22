# Audit 2026 — resolution log

This document tracks what was done about every finding in
[docs/Audit-2026.md](Audit-2026.md) and the two machine-readable finding lists
(`docs/audit_findings.csv`, `docs/audit_findings_oob.csv`). The audit itself is
kept unchanged as the record of what was found; this file is the record of what
changed.

Method: static findings were fixed in the patches/tooling and verified with
`tools/validate.py` and `tools/audit_deep.py`; the 67-country order-of-battle
reality findings were applied per country against the installed MD 2.0 data
(state ownership, equipment archetypes) with web-checked 1 January 2026
sources, then re-verified with `tools/oob_check.py`, `tools/validate.py` and a
full `tools/make_nonnsb_oob.py --apply` regeneration.

## 1. Tooling (section 2)

| ID | Status | Fix |
|---|---|---|
| T-01 | fixed | All hardcoded `D:\SteamLibrary` paths removed. `tools/rebase.py` now resolves MD/vanilla from `MD_PATH`/`HOI4_PATH`, the Windows Steam registry and `libraryfolders.vdf`, then the usual library locations (`rebase.resolve_install`); `validate.py`, `audit_2026.py`, `build_focus_config.py`, `audit_deep.py` and `oob_digest.py` use it. |
| T-02 | expected | The launcher descriptor only exists after `tools/install_mod.ps1`; unchanged. |

## 2. Static findings (section 3)

| ID | Status | Fix |
|---|---|---|
| O-02 misplaced divisions | fixed | USA 2nd ID → Gyeonggi (604); GER Panzerbrigade 45 → Vilnius (110) and renamed from the working "42"; SOV Far East formations → Primorye/Amur/Transbaikal/Sakhalin; SUD units → Khartoum/North Kordofan; SYR units → Damascus/Homs/Aleppo; UKR brigades out of Crimea → Dnipropetrovsk/Kharkiv/Mykolaiv/Cherkasy/Zaporizhzhia; AFG now owns the Afghan states at 2026.1.1 (see D-01). `tools/audit_deep.py` reports 0. |
| O-03 IND naval base | fixed | IND fleet `naval_base` 4306 (a VP province) → 4608 (the level-4 naval base in Eastern Java). |
| C-01 NATO array duplicates | fixed | `patches/history_countries/USA.txt` now only adds MNT, FYR, FIN, SWE to `global.nato_members` (the four tags MD's 2026 array misses) and keeps the `is_in_array` guards. |
| C-02 CSTO ARM removal | fixed | The array removal moved from SOV's history (which MD's `setup_global_arrays` undid) to our `on_startup` in `common/on_actions/md2026_on_actions.txt`, which runs after MD's. |
| H-04 party_pop_array sums | fixed | `tools/fix_party_arrays.py` reapportions the 13 countries (BEL, DEN, GRE, HOL, HUN, ICE, IND, LAT, LIT, NOR, SLO, TUR, VEN) to sum to 1.000. |
| H-06 elections_allowed = no | intentional | CHI keeps MD's own combination; UKR now has `elections_allowed = no` on purpose (martial law). The audit classified this as a cosmetic NOTE. |
| S-05 shared air-wing states | not a bug | Left as is (MD does the same; wings coexist in a state). |
| D-01 AFG/TAL design | fixed | TAL's eight states are transferred to AFG in `patches/history_states/409,410,412,414,415,1152,1207,1208.txt` at 2026.1.1; the TAL→AFG `annex_country` at `on_startup` stays as a fallback. AFG's OOB is now on home soil. |
| D-02 air wings via `set_oob` | documented | The combined layout is kept (vanilla's `PAK_1936` proves the OOB loader parses `air_wings`, and the 1.2.0 history shows the wings were created but empty before the equipment fix). The day-1 check is in `docs/Testing.md` and `docs/Known-Issues.md`; if the wings turn out to be missing they must move to `set_air_oob` files. `tools/check_oob_layout.py` documents the MD/vanilla layouts. |

## 3. Politics and economy (section 5)

| Finding | Status | Fix |
|---|---|---|
| UKR `elections_allowed = yes` | fixed | → `no` (martial law). |
| HOL 2023 snapshot | fixed | 2025.10.29 election date, post-election party shares, caretaker coalition (VVD + NSC + BBB, PVV out since June 2025), `set_popularities` aligned. |
| KOR last election 2024.4.10 | fixed | → 2025.6.3 (snap presidential). |
| KOS last election 2021.2.14 | fixed | → 2025.12.28 (snap election). |
| MLV last election 2023.7.11 | fixed | → 2025.9.28. |
| EGY last election 2024.12.10 | fixed | → 2025.11.10 (parliamentary election window). |
| NRY last election 2021.9.13 | fixed | → 2025.9.8. |
| ALB last election 2025.4.25 | fixed | → 2025.5.11. |
| POR last election 2024.3.10 | fixed | → 2025.5.18. |
| BRM no elections | fixed | `elections_allowed = yes`, `last_election = 2025.12.28` (first phase), frequency 60. |
| TAI debt 30 | fixed | → 210 bn USD (central-government debt); `treasury` 50 no longer exceeds it. |
| LUX treasury > debt | fixed | `treasury` 25 → 10 (found by the new debt check). |
| GDP outliers | fixed | TUR 13.0→18.6, MNT 12.0→7.5, UZB 2.5→4.0, KYR 1.7→3.1, ALB 8.0→12.7, POL 22.0→28.4, TAJ 1.1→1.7 (tenths of the audit's reference values). |
| SAF ANC ideology | fixed | ANC coded as `socialism` (democratic family), `ruling_party` 3, leader ideology and popularity breakdown aligned; no longer in the communist family. |
| SYR Ba'athist focuses | fixed | The ten listed focuses added to `patches/unsafe_focuses.json`, so they are no longer pre-completed for the post-Assad government. |
| ARM/GEO/ETH/BLR communism label | noted | MD's taxonomy maps conservative/autocratic parties into the communism family; the audit classified it as an artefact, no code change. |

## 4. Tooling added (recommendation 12)

| Tool / file | Purpose |
|---|---|
| `tools/oob_check.py` | fast per-tag structural check (basing, naval/air base existence, equipment, templates, phantoms) — the O-02/O-03/O-04 checks made repeatable per country |
| `tools/oob_lookup.py` | province/state/equipment lookup used while fixing the OOBs |
| `tools/economy_report.py` | now checks debt bounds, `treasury > debt` and collapsed debt; documents the central-government debt convention |
| `patches/phantom_platforms.json` + `tools/validate.py` | regression net: ships/aircraft/formations that did not exist on 1 Jan 2026 fail the validator when they reappear |
| `tools/foreign_basing.json` | intentional foreign-basing allowlist shared by `oob_check.py` and `audit_deep.py` |
| `tools/oob_diff_summary.py` | before/after summary of the OOB changes (HEAD vs working tree) used to review the country work |
| `tools/fix_oob_locations.py`, `tools/fix_politics_2026.py`, `tools/fix_party_arrays.py` | the migration scripts that applied the O-02 and politics fixes |
| `tools/check_oob_layout.py` | diagnostic for the D-02 combined-OOB layout |

## 5. OOB reality audit (section 4)

All 67 orders of battle were reworked against the section 4 findings and the
97 rows of `docs/audit_findings_oob.csv`, with web-checked 1 January 2026
sources. The table shows divisions / ships / aircraft before → after; the
per-country notes list the substance.

| Tag | Div | Ships | Aircraft | Tag | Div | Ships | Aircraft |
|---|---|---|---|---|---|---|---|
| AFG | 11→12 | 0→0 | 0→34 | NKO | 40→41 | 26→26 | 233→233 |
| ALB | 3→2 | 2→5 | 0→0 | NRY | 4→4 | 16→17 | 47→61 |
| ARM | 6→5 | 0→0 | 12→19 | PAK | 30→31 | 13→19 | 245→455 |
| AST | 10→10 | 21→21 | 124→146 | PER | 22→27 | 11→9 | 159→309 |
| BEL | 3→2 | 2→9 | 44→44 | POL | 14→14 | 8→11 | 117→119 |
| BLR | 7→9 | 0→0 | 90→90 | POR | 4→4 | 9→11 | 38→38 |
| BOS | 4→4 | 0→0 | 0→0 | RAJ | 44→53 | 42→66 | 558→580 |
| BRA | 17→17 | 11→12 | 115→67 | ROM | 9→9 | 6→6 | 47→43 |
| BRM | 18→18 | 7→8 | 36→135 | SAF | 6→6 | 10→10 | 43→43 |
| BUL | 5→5 | 4→11 | 23→23 | SAU | 22→22 | 11→16 | 273→388 |
| CAN | 10→11 | 20→21 | 87→124 | SER | 7→7 | 0→0 | 20→31 |
| CHI | 58→66 | 65→89 | 1083→1283 | SLO | 2→2 | 0→0 | 16→27 |
| CRO | 5→3 | 5→8 | 12→12 | SLV | 2→3 | 0→0 | 0→0 |
| CZE | 4→4 | 0→0 | 38→40 | SOV | 45→61 | 59→68 | 396→600 |
| DEN | 3→3 | 9→18 | 31→37 | SPR | 10→11 | 18→22 | 159→170 |
| EGY | 20→23 | 16→27 | 285→353 | SUD | 15→13 | 0→0 | 22→22 |
| ENG | 7→7 | 36→35 | 143→203 | SWE | 8→10 | 9→11 | 102→98 |
| EST | 3→3 | 3→7 | 0→0 | SYR | 12→14 | 2→0 | 16→6 |
| ETH | 14→11 | 0→0 | 32→36 | TAI | 17→24 | 25→39 | 329→352 |
| FIN | 9→9 | 9→8 | 65→65 | TAJ | 4→5 | 0→0 | 6→5 |
| FRA | 11→9 | 33→34 | 209→287 | TUR | 24→25 | 30→36 | 351→469 |
| FYR | 2→2 | 0→0 | 0→0 | UAE | 5→7 | 8→11 | 153→181 |
| GEO | 6→9 | 0→0 | 20→20 | UKR | 29→63 | 6→6 | 89→94 |
| GER | 8→8 | 24→23 | 176→286 | USA | 26→28 | 80→85 | 1055→1139 |
| GRE | 13→13 | 15→25 | 174→204 | UZB | 8→8 | 0→0 | 82→89 |
| HOL | 4→4 | 11→20 | 60→56 | VEN | 16→15 | 8→5 | 60→52 |
| HUN | 5→4 | 0→0 | 15→16 | YEM | 11→13 | 0→0 | 20→20 |
| IND | 17→17 | 17→17 | 123→126 | KAZ | 7→13 | 0→4 | 74→81 |
| ISR | 17→20 | 13→12 | 335→331 | KOR | 27→27 | 30→51 | 304→304 |
| ITA | 14→14 | 20→27 | 185→204 | KOS | 2→4 | 0→0 | 0→5 |
| JAP | 14→18 | 44→68 | 348→416 | KYR | 2→4 | 0→0 | 6→14 |
| LAT | 2→5 | 5→5 | 0→0 | LIT | 4→4 | 4→8 | 3→3 |
| LUX | 1→1 | 0→0 | 1→1 | MLV | 3→3 | 0→0 | 8→5 |
| MNT | 2→3 | 0→2 | 0→0 | | | | |

Substance per country (the audit row tags in brackets):

- **USA [USA]** - removed the three phantom ships (Anzio, Vella Gulf, Lyndon B. Johnson), rebuilt cruiser/DDG flotillas and homeports, fixed 3rd ACR, 25th ID and 11th Airborne added, divisions rebased to their real states, 3rd MarDiv to Okinawa, B-52H 76, F-15EX/tankers/helicopters added.
- **SOV/BLR [SOV, BLR]** - Far East formations kept at their fixed bases; duplicate divisions removed and Tamanskaya/Kantemirovskaya renamed; Borei/Yasen hull identities fixed, Kharlamov removed, new ships added; ground forces in occupied Donbas/Crimea, the Oreshnik brigade in Belarus, the 102nd/201st bases; Su-57, Tu-95MS, Tu-22M3 counts and Kinzhal/Geran units added. Belarus: garrisons fixed, airborne brigades unswapped, Iskander and Su-30SM basing corrected.
- **CHI [CHI]** - 76th Group Army out of Hong Kong, 73rd/80th added, every group army at its HQ, airborne brigades renumbered, ship name/hull mismatches fixed, Type 093/094 renumbered, the whole amphibious force added, J-20A 300.
- **TAI [TAI]** - Kinmen/Penghu commands on their islands, 8th Corps south, reserve brigades real, An Chiang/Wan Chiang pennants, 5 Knox + 2 Perrys + Tuo Chiangs added, Hai Kun removed, aircraft counts corrected.
- **JAP [JAP]** - divisions at their real garrisons, Mogami 8, Murasame 9, submarines 22, F-15J 199, F-2 85, F-35A 47, P-1 37.
- **KOR [KOR]** - 26th Mech removed, 2nd QR/23rd Security/30th Armoured corrected, hull numbers fixed (DDG-995, FFG-815/828, SS-085/086), the missing KDX-I/Incheon/Daegu frigates and KSS-I/II boats added.
- **NKO [NKO]** - the Kursk contingent (~11,000 troops) added, Pyongyang artillery division moved home. Choe Hyon/Hero Kim Kun Ok correctly absent.
- **ENG/FRA/GER/ITA/POL/ISR [ENG, FRA, GER, ITA, POL, ISR]** - all phantom ships removed (Lancaster, Northumberland, Albion, Bulwark, Chiddingfold, Penzance, Émeraude, Emden, Drakon), Agamemnon/St Albans/Hunt MCMVs/Améthyste/Tourville/Schergat/Bianchi added; BAOR "7th Light Mech (Germany)" and the phantom French/Legion brigades/Jägerbrigade 1 replaced with real formations; aircraft counts raised to real totals (Typhoon 111, F-35B 45, Rafale 108, Eurofighter 138, Tornado 84, F-15 66, F-16 173); Golan/Galilee/Negev and Gaza/Lebanon/Hermon deployments added (ISR).
- **HOL/BEL/DEN/NRY/CAN/SPR/POR [HOL, BEL, DEN, NRY, CAN, SPR, POR]** - non-existent brigades removed/renamed, Walrus/Odda/P-3M phantoms removed, missing M-frigates/LPDs/CSS Den Helder/Alkmaar MCMs/AOPVs/OPVs/F-100 subs/Knud Rasmussen/Diana/Skjold/Uthaug/Harry DeWolf added, F-35A basing (Florennes) and counts fixed, Canada's MNB Latvia and Spain's NATO Battlegroup Slovakia added, army regions corrected.
- **FIN/SWE/TUR/GRE/ROM/HUN/CZE [FIN, SWE, TUR, GRE, ROM, HUN, CZE]** - Pohjanmaa class and İzmir/Murat Reis removed, TCG/Yavuz/Atılay fleet made real, Swedish NATO battalions (Latvia, Finland) added, Gripen/Södermanland subs and army regions fixed, Elli class + Kimon + F-4E added (GRE), MQ-9 phantom squadrons removed (ROM), C-17 removed and KC-390 added (HUN), brigade regions and C-295 fixed (CZE).
- **BUL/CRO/ALB/LIT/EST/SLO/SAF/EGY [BUL, CRO, ALB, LIT, EST, SLO, SAF, EGY]** - Bulgarian identities/pennants fixed, Croatian phantom hulls replaced by the real missile boats and minehunter, Aitvaras brigade replaced by Aukštaitija, Estonian pennants/Wambola fixed, Slovak inventory corrected, SAF readiness lowered to reality, Egyptian armoured/mech divisions and the missing frigates/submarines/Mirage 2000s fixed.
- **MLV/BRA/VEN/AST/IND/BRM [MLV, BRA, VEN, AST, IND, BRM]** - Moldova's phantom MiG-29 squadron removed, Brazil's phantom ships/brigades removed and the jungle brigades moved to Amazonia, Venezuela's hulk/retired ships and F-5 flight removed, Australian Anzac/Pilbara removed with 1st/3rd Bdes unswapped and the Fires brigade added, Indonesian chains of command/basing and F-16 blocks fixed, Myanmar's air force rebuilt (~130 aircraft incl. Su-30SME) and the second submarine added.
- **RAJ/PAK/SAU/UAE/PER [RAJ, PAK, SAU, UAE, PER]** - India's ~10 invented formations replaced by the real corps/division/brigade structure, Chakra III/Triput removed and Surat/Tushil/Tamal/Himgiri added, Tejas 30/Mirage 2000 added; Pakistan's 054A/P names, Babur-class corvettes and Hangor removal, army rebased to real garrisons, F-16 75/Mirages 170; Saudi fleet homeports unswapped, Badr class fixed, Avante 2200 class added, MQ-9 phantom removed, Tornado 81; UAE P176 renamed, Gowind/Falaj/TB2 added; Iran's Artesh/IRGC order of battle rebased per ISW/CTP, IRGC Navy out of Lorestan, Damavand removed and Deylaman added, missing air types and the IRGC UAV force added.
- **KAZ/KYR/TAJ/UZB/SUD/ETH [KAZ, KYR, TAJ, UZB, SUD, ETH]** - Kazakh MiG-29/MiG-31 wings (retired 2023) removed, real brigades + Caspian flotilla added; Kyrgyz/Tajik Turkish drones and helicopters added; Uzbek C-130H phantom removed, MiG-29 38, wings spread over real bases; Sudanese units out of RSF-held Darfur into army-held commands; Fano divisions removed from the ENDF OOB and Amhara garrisoned; Ethiopian air inventory corrected.
- **UKR/SYR/YEM/AFG [UKR, SYR, YEM, AFG]** - Ukraine expanded to the 2025 corps structure (63 units), Mirage 2000-5F added, naval pennants fixed, no units in Russian-held territory; Syria's navy deleted, air reduced to 6 real airframes, ground rebuilt on the numbered divisions; Yemen's province IDs aligned, Houthi units confined to the highlands and PLC/IRG formations added; Afghanistan's divisions moved to the real corps HQs and its ~34 airframes modelled.
- **LAT/SLV/SER/BOS/KOS/FYR/MNT/LUX [report section 4.8]** - Latvian MCM class and brigade name fixed, National Guard regionalised; Slovenian 1st Brigade added and 72nd moved to Maribor; Serbian MiG-29/Orao counts, real army brigades and the 63rd Parachute Brigade; Bosnian Tactical Support Brigade to Sarajevo and helicopters added; Kosovo's three regiments + National Guard + TB2; FYR's 1st Mechanized Infantry Brigade; Montenegro shrunk to one active battalion with Durmitor and Jadran added; Luxembourg's A400M moved to Melsbroek and H145M added.

### Deliberately not changed

- **ETH TDF** is not modelled: the Tigray Defence Forces existed on 1 Jan 2026
  but were not fighting the ENDF (clashes resumed 26 January 2026) and there is
  no separate Tigray tag in MD to put them on.
- **SAF ANC ideology** was fixed in the politics pass (section 3), not the OOB.
- **MD-side abstractions kept**: the mod's generic division templates, the
  "12 mobilized brigades" in the Russian OOB (MD's stated 2022+ mobilisation
  abstraction) and MD's own naval hull families.
- **Greece's "III Infantry Division"** and Serbia's legacy "72nd Special
  Brigade" are flagged in the subagent work but were outside the audit rows.
- **MD-side anachronisms reachable in 2026**: MD's own focus trees still offer
  some 2000-era rewards (e.g. `ENG_albion_class_lpd` builds HMS Albion, retired
  in March 2025; it is not pre-completed and not overridden). These are MD's
  content, not the 2026 OOB, and adapting each one is separate follow-up work.

### Verification

```text
python tools/make_nonnsb_oob.py --apply     # 67 non-NSB variants rebuilt
python tools/oob_check.py --all             # 67 files, 0 findings
python tools/validate.py                    # 0 errors, 4 known warnings
python tools/audit_deep.py                  # 0 non-informational findings (incl. G-01 reproducibility)
```

## 6. What remains (runtime only)

The audit's section 6 and recommendation 13 list checks that need a running
game; they are documented in `docs/Testing.md` and `docs/Known-Issues.md`:

1. AFG/TAL: states transfer at 2026.1.1 with the annexation as fallback.
2. `global.nato_members` / `global.CSTO_member` contents in a save or console.
3. Air wings spawning from the combined `set_oob` files (D-02); the layout is
   kept on precedent, but if day 1 shows no wings they must move to
   `set_air_oob` files.
4. Pre-completed focus rewards in `error.log`.
5. Legacy-war settlement (Chechnya, Aceh, Tamil Eelam, Afghanistan, Eritrea,
   South Sudan, African rebels).

Everything else from the audit - tooling (T-01), static bugs (O-02, O-03,
C-01, C-02), the informational items (H-04, H-06, S-05), the design item
(D-01), politics/economy (section 5) and the 67-country OOB reality audit -
is fixed and verified statically.
