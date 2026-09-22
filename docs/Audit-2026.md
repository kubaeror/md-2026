# MD 2026 Rework — Full Audit

Date: 2026-09-22
Auditor: automated static analysis (`tools/audit_deep.py`, `tools/validate.py`,
`tools/oob_digest.py`) + web-verified reality checks by research subagents.
Scope: the whole submod, with a country-by-country OOB reality audit for all
**67** 2026 orders of battle. **Report only — no fixes applied.**

## 0. Executive summary

- **Static validation: clean.** `tools/validate.py` reports **0 errors**
  (after working around hardcoded paths); no BOM/encoding/brace problems, no
  unknown references, no broken `set_oob` wiring, and the generator reproduces
  every override byte-for-byte.
- **Real bugs found statically:** six groups of divisions stationed in the
  wrong country (USA in Pakistan, Germany in Kaliningrad, Russia in Yunnan,
  Ukraine in Crimea, Sudan in South Sudan, Syria in Lebanon), an Indonesian
  fleet homeport without a naval base, duplicate NATO-array entries, an
  ineffective CSTO removal, and the Afghanistan-on-the-wrong-tag design issue.
- **OOB reality audit (67 countries):** **24 countries need rework**, 43 have
  minor deviations, and **no country was fully clean**. The dominant problems
  are phantom platforms (ships/aircraft not in service on 1 Jan 2026),
  systematically scrambled ground basing, missing foreign deployments, and
  procurement timing that is 1–2 years ahead of reality.
- **Politics:** all 30 bookmark leaders are correct for 1 Jan 2026; 10+ stale
  election dates, Ukraine's `elections_allowed` is wrong, and Taiwan's debt is
  ~7× too low.
- **Tooling:** 9 hardcoded `D:\SteamLibrary` paths break validation on any
  other machine; `economy_report.py` never checks debt; the validator has no
  OOB-basing or phantom-platform checks (this audit adds them as
  `tools/audit_deep.py` + `tools/oob_digest.py`).

## 1. Environment and baseline

| Item | Value |
|---|---|
| Repo | `C:\Users\Kuba\Documents\md-2026` (commit `0c732af`) |
| Millennium Dawn | 2.0.0, `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2777392649` |
| Hearts of Iron IV | 1.19.3, `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV` |
| Game logs | none on this machine (`Documents\Paradox Interactive` absent) → **static audit only** |
| Validator | `tools/validate.py` → **0 errors**, 4 warnings (3 MD-side, 1 installation) |
| Coverage | 30 bookmark countries complete; 79 MD own-tree countries not ported (documented) |

`tools/validate.py` only produces its clean result after working around the
hardcoded paths (finding T-01). Without that workaround it reports 4 false
errors and 430 false warnings.

**How this audit was produced (all read-only):**

```bash
python tools/validate.py                      # baseline (needs the path fix / MD_PATH)
python tools/audit_deep.py --json findings.json   # static audit (new, read-only)
python tools/oob_digest.py --all --outdir digests --json digest.json  # OOB digests (new)
```

The reality checks were performed by nine country batches (one batch was split
in two after an upstream content filter, so ten OOB research runs) plus one
politics subagent, each with web access and the per-country digest as input;
their findings are reproduced in section 4 with sources.
`tools/audit_deep.py` never writes to the repo (its reproducibility check
captures generator output in memory).

## 2. Tooling findings

| ID | Severity | Finding |
|---|---|---|
| T-01 | BUG (tooling) | `D:\SteamLibrary\...` is hardcoded in 9 places: `tools/rebase.py:25,26,786`, `tools/validate.py:125,273,428`, `tools/audit_2026.py:26,198`, `tools/build_focus_config.py:14`. On any machine without that exact path the validator cannot see vanilla content, MD's default path breaks, and `rebase.py generate` fails. Recommendation: resolve paths from `MD_PATH` / `HOI4_PATH` env vars, then scan the usual Steam library locations. |
| T-02 | NOTE | `validate.py` reports the missing launcher descriptor (`mod/md-2026.mod`) because the Paradox user directory does not exist on this machine. Expected, not a content problem. |

## 3. Static audit results (`tools/audit_deep.py`)

Groups: S = file integrity, O = OOB structure, H = history/politics,
F = focus trees, E = events/decisions/scripts, L = localisation,
B = bookmark, C = cross-mod ordering, G = generated-file reproducibility.

### 3.1 Confirmed content bugs

**O-02 — divisions stationed in the wrong country** (both NSB and non-NSB files)

| Country | Unit(s) | Placed in | Real 2026 location | Recommendation |
|---|---|---|---|---|
| USA | `2nd Infantry Division (Korea)` | Sindh, **Pakistan** (state 426, province 1147) | Camp Humphreys, Gyeonggi, **South Korea** (state 604) | move to state 604 |
| GER | `Panzerbrigade 42 (Lithuania)` | **Kaliningrad**, Russia (state 642) | Rukla, **Lithuania** (states 109/110/1043/1044) | move to a Lithuanian state |
| SOV | `5th`, `29th`, `35th Combined Arms Army`, `68th Army Corps`, `155th Naval Infantry Brigade (Pacific)` | **Yunnan, China** (state 578) | Russian Far East: Primorye (692), Khabarovsk (687), Amur (1069), Sakhalin (691) | move to Far East states |
| SUD | `1./5. Firqa Miliishiya`, `7. Firqa Mushaat`, `2. Liwa' Motahirka` | **Jonglei, South Sudan** (state 924) | Sudan: Khartoum (220), Darfur (224/614), North Kordofan (223) | move to Sudanese states |
| SYR | `3. Firqa Mushaat`, `1./5. Firqa Miliishiya` | **Bekaa / North Lebanon** (states 553/203) | Syria: Damascus (186), Homs (188), Aleppo (566), Latakia (189) | move to Syrian states |
| UKR | `93rd Mechanized`, `54th Motorized`, `35th/36th Marine`, `118th TDF`, `55th Artillery` | **Crimea** (state 669) — Russian-owned in 2026, and Russia is at war with Ukraine at start | Ukrainian-controlled territory: Odesa (695), Mykolaiv (1086), Zaporizhzhia (694), Cherkasy (1091), East Donetsk (693) | move out of Crimea |

Impact: units on foreign soil without military access are teleported or
destroyed at start; the Ukrainian brigades in Russian-held Crimea are
especially severe because Russia and Ukraine start at war. Files:
`history/units/<TAG>_2026_nsb.txt` and `_nonnsb.txt` (each finding occurs in
both variants).

**O-03 — Indonesian fleet homeport has no naval base**
`history/units/IND_2026_nsb.txt:238` (and `_nonnsb.txt:241`) set
`naval_base = 4306` for the Surabaya fleet, but the level-4 naval base in
Eastern Java is province **4608** (`634-Eastern Java.txt`); 4306 is only a
victory point. Recommendation: change to 4608.

**C-01 — NATO member array gets duplicate entries**
`patches/history_countries/USA.txt` adds 13 post-2000 members to
`global.nato_members` during history. MD's `setup_global_arrays`
(`common/scripted_effects/00_startup_effects.txt`, on_startup) adds 9 of them
again and never clears the array, so ALB, BUL, CRO, EST, LAT, LIT, ROM, SLO,
SLV appear **twice**. MD's loop-based NATO tally code then double-counts those
countries. Recommendation: only add the four tags MD's 2026 branch misses
(MNT, FYR, FIN, SWE), or guard each addition with
`NOT = { is_in_array = { global.nato_members = TAG } }`.

**C-02 — CSTO Armenia removal is undone at startup**
`patches/history_countries/SOV.txt:63` does
`remove_from_array = { global.CSTO_member = ARM }` during history (2026.1.1),
but MD's `setup_global_arrays` re-adds ARM at on_startup with no clear_array,
so Armenia remains a CSTO member in the array. The faction removal
(`remove_from_faction = ARM`) does work. Recommendation: move the array
removal into our own `on_startup` effect (which runs after MD's) or a decision.

### 3.2 Design-level / fragile items

**D-01 — Afghanistan runs on the wrong tag (by design, but fragile)**
MD's land is owned by `TAL` (Afghan Taliban); `AFG` is MD's rebel tag with
`dynamic_rebel_flag`. The submod sets up 2026 Afghanistan on `AFG`
(`patches/history_countries/AFG.txt`) and `common/on_actions/md2026_on_actions.txt:87`
annexes TAL into AFG at on_startup. Consequences: (a) the AFG OOB places two
divisions inside TAL's Bactria state before the annexation; (b) if the
annexation fails (tag absent, event order), AFG has no home territory;
(c) AFG has no 2026 focus branch, unlike every bookmark country;
(d) the annexation happens after history, so AFG starts with foreign-soil
units for at least one tick. Recommendation: either move the 2026 setup to
`TAL` (the tag that owns the land and is the Taliban), or transfer the
Afghan states to AFG in `history/states` at 2026.1.1 and keep the annexation
as a fallback.

**D-02 — Combined OOB files rely on `set_oob` loading `air_wings`**
The submod puts ground, fleet and `air_wings` in one file loaded by
`set_oob`. Evidence: vanilla Pakistan's `oob = "PAK_1936"` uses the same
combined layout (`units` + `air_wings` in one file), and the submod's own
history showed empty air wings (rather than no wings) before the 1.2.0
equipment-name fix — both imply the default OOB loader parses `air_wings`.
However, **neither MD nor vanilla contains a `set_oob` target with an
`air_wings` block** (only the legacy `oob =` field does), so this rests on the
`oob =` precedent. Verify on day 1 in game: the air base screen should show
the 2026 wings. If it does not, each `air_wings` block must move to a
`set_air_oob` file.

### 3.3 Informational

| ID | Finding |
|---|---|
| S-05 | 46 OOB files repeat an `air_wings` state id (several wings in the same state). MD's own OOBs do the same in 12 files; wings coexist in a state. Not a bug. |
| H-04 | 13 countries have `party_pop_array` values summing to 0.85–0.97 instead of 1.0 (BEL, DEN, GRE, HOL, HUN, ICE, IND, LAT, LIT, NOR, SLO, TUR, VEN). MD's own 2000 data has 33 of 385 countries below 0.98, so this is a consistency nit, not a functional bug. |
| H-06 | China uses `elections_allowed = no` together with `election_frequency = 60`; MD uses the same combination elsewhere. Cosmetic. |

### 3.4 Checks that passed (positive results)

- **Equipment**: every equipment type in all 134 OOB files resolves against
  MD 2.0 (585 MD equipment definitions); no vanilla-only or archetype names.
- **File integrity**: no BOM, no corrupted characters, no unbalanced braces in
  any shipped script file.
- **Templates**: every `division_template` used in an OOB is defined; no
  template exceeds 25 battalions / 5 support companies; no overlapping
  battalion coordinates.
- **OOB wiring**: every `set_oob` target exists (after the NOR→NRY rename);
  every 2026 OOB has both NSB and non-NSB variants; non-NSB files contain no
  NSB-gated equipment.
- **Locations**: all naval bases except IND 4306 have a base building; all air
  wings are in states with an air base. The static allowlist marked US basing
  in Germany/Japan/Spain, France in Germany, Turkey in Northern Cyprus and
  China in Hong Kong as intentional; the reality audit later showed the
  **UK "7th Light Mech Brigade (Germany)" is an artifact** (7th Bde is at
  Cottesmore; British Army Germany is a small presence at Sennelager), so that
  entry needs review rather than acceptance.
- **History**: every 2026 leader's ideology matches the ruling party's
  ideology family; all traits and portraits resolve; `set_oob` runs after the
  tech tier grant in every patch.
- **Bookmark**: all 30 entries have a `version` key and valid tags.
- **Localisation**: EN and PL complete, no duplicate keys, no placeholder
  (`$var$`) mismatches between languages.
- **Generated files**: regeneration via `rebase.py` reproduces the on-disk
  files byte-for-byte (no stale MD overrides).
- **Validator**: 0 errors after path workaround; the remaining warnings are
  MD-side content (`ARM` reference in `05_france.txt`, 95 MD-side stockpile
  references, 56 MD-side `create_unit` templates).

## 4. OOB reality audit — 67 countries

> Web-verified by nine research batches against open 2026 sources (IISS
> Military Balance, FlightGlobal World Air Forces, official navies/MoDs,
> reputable press). Verdicts: **2026-accurate**, **minor deviations**,
> **wrong — needs rework**, **stale 2000-era**. The state names in the tables
> come from the mod's own MD map data (`tools/oob_digest.py`).

### 4.1 Summary of verdicts

| Verdict | Countries |
|---|---|
| Wrong — needs rework | USA, SOV, CHI, ENG, RAJ, SAU, PAK, UKR, FIN, BRM, KAZ, HOL, BUL, CRO, MLV (stale), PER, TAI, VEN, BRA, AST, SYR, YEM, ETH, SUD |
| Minor deviations | ITA, EGY, NKO, TUR, POL, KOR, ISR, GER, FRA, JAP, CAN, SPR, SAF, SWE, GRE, ROM, HUN, CZE, NRY, KYR, TAJ, UZB, UAE, DEN, BEL, POR, ALB, LIT, LAT, EST, SLO, SLV, SER, BOS, KOS, FYR, MNT, LUX, IND, AFG, BLR, GEO, ARM |
| 2026-accurate | none (no country came out fully clean) |
| Stale 2000-era | MLV (MiG-29 squadron that does not exist); BRM close (2000s-era air force) |

Common patterns across all batches: **naval lists are the weakest area**
(wrong/phantom hulls in 9 of 19 small-NATO countries and every major navy),
**ground basing is systematically scrambled** (units placed in the wrong
region even when the unit exists), **foreign deployments are missing**
(Canada/Spain/Sweden NATO brigades, US 3rd Marine Div in Okinawa, Russian
forces in occupied Ukraine, Israeli Gaza/Lebanon/Syria positions), and
**procurement timing is frequently 1–2 years early** (ships/aircraft not yet
commissioned on 1 Jan 2026).

**Were the OOBs actually changed for 2026?** Yes — every one of the 67 files
is a genuine rewrite, not a copied 2000-era order of battle. Against MD's own
2000 files the counts and names differ sharply: USA 26 divisions / 80 ships /
1055 aircraft vs 146 / 243 / 4386; SOV 45 / 59 / 396 vs 221 / 326 / 3648;
CHI 58 / 65 / 1083 vs 463 / 160 / 2131; ENG 7 / 36 / 143 vs 31 / 86 / 730.
Unit-name overlap with the 2000 files is near zero for almost every country
(the few exceptions, e.g. India's 12 shared names and Pakistan's 19, are
legacy unit designations that still exist). The 2026 equipment generations
(F-35, P-8A, Gripen E, Type 212A, Borei/Yasen, J-20) confirm the rewrite
targets the modern era. The remaining question is accuracy of the rewrite,
which sections 4.2–4.11 cover.

### 4.2 Superpowers (USA, SOV, CHI)

**USA — minor deviations, but 4 hard blockers.** Decommissioned ships still
listed: **USS Anzio (CG-68)** (out 2022) and **USS Vella Gulf (CG-72)** (out
2022) (BLOCKER); **USS Lyndon B. Johnson (DDG-1002)** is not commissioned
(planned 2027) (BLOCKER); **2nd Infantry Division (Korea) is in Sindh,
Pakistan** — the file's own comment says Korea (BLOCKER, already caught
statically). Also: USS Jackson is Independence-class, not Freedom; 3rd
Armored Cavalry Regiment was renamed in 2011; roughly a third of divisions are
in the wrong state (101st/10th Mtn/3rd ID/7th ID/2nd ID/2nd CR/75th Rangers);
25th ID (Hawaii) and 11th Airborne (Alaska) missing; 3rd Marine Division
should be FOREIGN (Okinawa); Navy homeports stale (Michael Murphy, Rafael
Peralta, Shiloh, Dewey, John Finn in the wrong fleets); SSGNs homeported at
Kings Bay instead of Bangor; no F-15EX, no tankers/helicopters; B-52H 48 vs
~76. Air types/generations otherwise correct. Sources: navy.mil,
Wikipedia (ship pages, US Army formations, USAF aircraft).

**SOV — wrong, needs rework.** The five Far East formations in Yunnan, China
are a province-ID bug (BLOCKER, already caught statically). **Admiral
Kharlamov (Udaloy) was decommissioned in 2020** but is listed in the Northern
Fleet (BLOCKER). Borei hull numbers/variants scrambled (K-553 = Generalissimus
Suvorov, K-554 = Imperator Aleksandr III, K-551 = Vladimir Monomakh not Knyaz
Oleg); B-187 is Komsomolsk-on-Amur, not Novosibirsk; Kronshtadt (Lada) is in
the Northern Fleet, not Baltic. Four duplicated divisions (2nd Gds MRD =
Tamanskaya; 4th Gds Tank = Kantemirovskaya; 3rd MRD twice; 144th MRD twice) —
the "45 divisions" headline is inflated. Ground HQs placed in North Krasnodar
instead of Moscow/Rostov/Vladikavkaz/Stavropol; **no Russian ground units
inside occupied Ukraine/Belarus** despite the war; Su-57 10 vs ~21; Tu-95MS
16 vs ~55–60; Tu-22M3 28 vs ~60; no Shahed/Geran drones, no MiG-31K Kinzhal,
no Il-78 tankers. Sources: ww2.dk, Wikipedia (armies, Borei/Kilo/Lada
classes, Tu-95/Tu-22M/Su-57), navalnews.com, tochnyi.info.

**CHI — wrong, needs rework.** Four 76th Group Army brigades are garrisoned in
**Hong Kong** (76th GA HQ is Xining; the HK garrison is separate) (BLOCKER);
the Taiwan-facing **73rd Group Army is entirely missing**; most group armies
are relocated to the wrong provinces (Hainan/Guangxi/Guangdong/Hubei);
Tibet MD placed in Guangdong and Xinjiang MD in Guangxi; airborne brigades use
pre-2017 division numbers (43rd/44th/45th/46th) that no longer exist (BUG);
ship register errors: "CNS Wuhu (539)" is a Type 054A not 054B, "Changzhou
(156)" is Zibo, "Zibo (157)" is Lishui, "Nantong (133)" is Baotou, "Tangshan
(164)" is Guilin; Type 093/094 numbering mismatched; **no amphibious shipping
at all** (Type 075 LHDs, Type 071 LPDs, LSTs) — the biggest structural gap for
a Taiwan scenario; J-20A 100 vs ~300; J-16/J-15 naming. Correct: 3 carriers
(Fujian commissioned 5 Nov 2025), all 8 Type 055s, marine brigades. Sources:
Wikipedia (PLAGF, HK Garrison, Type 054B/052D/093/094/075, J-20), navalnews.com,
news.usni.org.

### 4.3 Regional powers (TUR, POL, KOR, ISR)

**TUR — minor deviations.** **TCG İzmir (F-516) is still on trials** (not in
service on 1 Jan 2026) and **TCG Murat Reis (S-332) is not commissioned**
(ACCURACY); four still-serving Yavuz-class frigates and four Atılay-class
submarines are missing (sub fleet 11 vs ~14); the Cyprus garrison is misnamed
— 28th is a **Mechanized Infantry Division**, and the 39th Mech Inf Div is
missing (14th Armoured Bde correct); 1st Armoured Bde is at Hadımköy, not
Edirne; ~30 F-4E Terminators, KC-135Rs, CN-235s, Anka/Aksungur missing.
Correctly omits KAAN/Hürjet. Sources: navalnews.com, Wikipedia (Istanbul-class
frigate, Reis-class submarine, Turkish Navy/Land Forces/Air Force),
globalsecurity.org.

**POL — minor deviations.** **ORP Ślązak's pennant is 241, not 341** (BUG);
the two Oliver Hazard Perry frigates and the Kilo submarine are missing;
FA-50 20 vs 12 delivered; **8 F-35As in the stockpile is premature** (first
in-country delivery May 2026); WOT brigade numbering/locations swapped (1st is
Podlaska, 3rd Podkarpacka); 6th Airborne Bde is Kraków not Kielce; ~10
MiG-29s still in service. Correctly omits the 96 AH-64Es (from 2028).
Sources: Wikipedia (Polish Navy/Land Forces/Air Force, ORP Ślązak), defense.gov.

**KOR — minor deviations.** Ship register bugs: "Jeongjo the Great (DDG-993)"
should be DDG-995 (DDG-993 is Seoae Ryu Seong-ryong, missing); "Gangwon
(FFG-820)" should be FFG-815; "Chungnam (FFG-821)" is actually ROKS Seoul
(Chungnam is FFG-828); "Gyeongbuk (FFG-819)" is Gyeongnam; An Mu SS-084 →
SS-085; Shin Chae-ho SS-085 → SS-086; ~10 surface combatants and 7 submarines
missing (all KDX-I, 4 Incheon, 5 Daegu, KSS-I/II). **26th Mechanized Infantry
Division was disbanded in 2018** but is listed (BUG); 2nd ID is now 2nd Quick
Response Division; 23rd is a Security Brigade; 30th Mech is an Armored
Brigade. Air is clean (F-35A 40, F-15K 60, FA-50 60, E-737 4 all match).
Sources: Wikipedia (ROKN active ships, Sejong/Incheon/Daegu/Chungnam classes,
ROK Army/ROKAF).

**ISR — minor deviations.** **INS Drakon was still in Germany on 1 Jan 2026**
(delivery voyage Aug 2026) — not in service (ACCURACY); F-15 20 vs ~66
airframes; F-16 198 vs ~173; "Nitzhon" → *Nitzachon*; 7th and 188th armoured
brigades are Golan-based but placed in coastal Galilee; the Judea and Samaria
territorial brigade is placed in the Negev; no representation of the Gaza
ceasefire lines, southern-Lebanon outposts or the Syrian Hermon buffer.
Correct: Merkava-era brigades, Sa'ar 6/5 flotillas, F-35I, Eitam CAEW, Hermes
900. Sources: Wikipedia (INS Drakon, Sa'ar 6, Israeli Air Force, IDF brigades).

### 4.4 Majors (GER, ENG, FRA, JAP, RAJ)

**GER — minor deviations (2 hard bugs).** The Lithuania brigade is actually
**Panzerbrigade 45** (activated Apr 2025, Rūdninkai/Rukla) — "42" was a
working designation — and it sits in Kaliningrad (BLOCKER, already caught
statically). **P-3C Orions are retired** (replaced by the 5 P-8As) (BUG).
Ground names/locations: 9. Panzerbrigade → Panzerlehrbrigade 9 (Munster),
21. Panzergrenadierbrigade → Panzerbrigade 21, 12. Panzerbrigade is Cham/Amberg
not Baden-Württemberg, 37. PzGrenBrig is Frankenberg/Saxony, Luftlandebrigade 1
is Saarlouis, and **"Jägerbrigade 1" does not exist**. K130 *Emden* (F266) is
still in trials (only *Köln* F265 commissioned Sep 2025); Sachsen-class belongs
to 2. Fregattengeschwader (Wilhelmshaven). Eurofighter 96 vs 138, Tornado
30 vs ~90, A400M 36 vs ~45–50. Sources: Wikipedia (45th Panzer Brigade,
Structure of the German Army, German corvette Emden, Sachsen class),
bundeswehr.de, milmag.pl, flightglobal.com.

**ENG — wrong, needs rework (navy/ground).** Four phantom ships:
**HMS Lancaster (decommissioned 5 Dec 2025)**, **HMS Northumberland**
(decommissioned 2024/25), **HMS Albion and HMS Bulwark** (both retired March
2025 — the RN has no LPD in service) (BUG ×4); HMS Chiddingfold is laid up in
extended readiness; HMS Penzance is a retired Sandown; HMS St Albans and three
Hunt-class MCMVs (Middleton/Hurworth/Bangor) are missing. Ground: **"7th Light
Mech Brigade (Germany)" is a British Army of the Rhine-era artifact** — 7th
Light Mech BCT is at Cottesmore, and British Army Germany is a few hundred
troops at Sennelager, not a brigade (BUG — this corrects the static audit's
"by design" flag); 1st Armoured Infantry Bde no longer exists (12th/20th
Armoured Bdes now); 20th is at Bulford not the West Midlands. Air types all
correct, counts low: Typhoon 72 vs 111, F-35B 24 vs ~45. Sources: royalnavy.mod.uk,
forcesnews.com, navylookout.com, naval-technology.com, Wikipedia (Structure of
the British Army).

**FRA — minor deviations (2 phantom brigades).** **"1re Brigade Blindée" and
"Brigade de la Légion Étrangère" do not exist** (BUG ×2) — the armoured
brigades are 7e BB (Besançon) and 2e BB (Strasbourg); the Legion is a command,
its regiments belong to other brigades. **SSN Émeraude was decommissioned
12 Dec 2024** (BUG); Suffren class 2 vs 3 (*Tourville* commissioned Jul 2025);
*Améthyste* missing. 9e Brigade Interarmes → 9e BIMa; 2e BB placed in
Franche-Comté instead of Alsace. Rafale 75 vs 108; Mirage 2000 58 vs 99.
Navy surface fleet otherwise exemplary (every hull/class/base correct).
Sources: Wikipedia (Structure of the French Army, Rubis class), navalnews.com,
defense.gouv.fr, foreignlegion.info.

**JAP — minor deviations.** Ground deployments scrambled: 9th/6th Divisions
are Tohoku not Hokkaido; 1st Div is Nerima (Kanto); 1st Airborne Bde and SFGp
are Narashino (Kanto) not Chubu; ARDB/4th Div are Kyushu; 8th Div Kumamoto;
15th Bde Naha/Okinawa. Mogami 6 vs 8 (Niyodo/Yubetsu delivered 2025);
**submarines 12 vs ~22**; Murasame 3 vs 9; **P-1 70 vs ~35–38** (overcount);
F-15J 130 vs 199; F-2 60 vs 85; F-35A 40 vs 47–51. Ships/classes otherwise all
real and correctly based. Sources: Wikipedia (JGSDF, Mogami class, Soryu
class, JASDF), janes.com, nti.org, globalmilitary.net.

**RAJ (India) — wrong, needs rework.** ~10 invented formations ("Southern Army
Reserve", "Central Reserve Division", "RAPID Reserve Division", corps reserve
units) (BUG); "36th Corps (Ranchi)" does not exist (23 Inf Div is there);
"2nd Armoured Division (RAPID)" does not exist (armoured divisions are 1st,
31st, 33rd); XIV Corps is Leh, Nagrota is XVI Corps; strike corps are deployed
to Arunachal/Jharkhand instead of the Punjab/Rajasthan plains; XVII Corps is
Panagarh not Sikkim. Navy: **INS Chakra III never delivered** (BUG — India has
no SSN); **INS Triput not yet commissioned** (BUG); missing the newest
commissioned ships (INS Surat D69, Tushil F70, Tamal F71, Himgiri F34);
pennant errors (Nilgiri F33/F34/F35, Sindhukesari S60, Arihant S2/Arighaat S3);
Shishumar/Brahmaputra/corvette classes omitted. Air: Tejas 80 vs ~30 (2.7×
overcount); **Mirage 2000 fleet (36+) entirely missing**; Jaguar 50 vs 86.
Sources: Bharat Rakshak, globalsecurity.org, Wikipedia (Indian Navy ships,
Arihant/Sindhughosh/Talwar classes, HAL Tejas, active Indian aircraft).

### 4.5 Central Asia + Gulf (KAZ, KYR, TAJ, UZB, UAE)

**KAZ — wrong, needs rework.** Air OOB is a ~2018 snapshot: MiG-29 (28) and
MiG-31BS (14) wings are types **retired in 2023** (BLOCKER); Su-30SM 12 vs
~30 real; the 24 Su-27/UB still in service are missing; Wing Loong/Anka UAVs
missing. Ground: generic brigade names (real ones: 3rd/4th/8th Mech, 3rd/7th
MR, 11th Tank, 35th Gds/36th/37th/38th Air Assault, 390th Naval Infantry),
everything placed north/south-east with nothing in the west (Atyrau/Aktau) or
east (Semey/Ayaguz), navy missing. Sources: aerospaceglobalnews.com,
forecastinternational.com, Wikipedia (Kazakh Air Defense Forces, Kazakh Ground
Forces, Armed Forces of Kazakhstan).

**KYR — minor deviations.** Structure fine (2 brigades) but the 2021–2023
Turkish drone fleet (TB2, Akinci, Aksungur, Anka — Border Guard) is absent;
helicopters (Mi-8/17/24) and An-26 missing; L-39 6 vs 4; both brigades in the
north, Osh/Batken south missing. Sources: overtdefense.com, dailysabah.com,
Wikipedia (Kyrgyz Air Force, Armed Forces of the Kyrgyz Republic).

**TAJ — minor deviations.** Plausible size and placement; the ~20 Mi-8/Mi-24
helicopters that are the air force's real substance are missing; L-39 6 vs 4;
12th Artillery Bde (Dushanbe) and the Murghob unit not modelled; "border
brigades" are really a separate service. Russian 201st base (~7,000 troops)
not represented. Sources: Wikipedia (Tajik Air Force, Tajikistani Ground
Forces, Russian 201st Military Base).

**UZB — minor deviations.** Clear error: 4 × C-130H "in service" — Uzbekistan
**does not operate C-130s** (real transports: Il-76, An-12, An-26, C-295; the
count matches the Afghan C-130H fleet — likely a mix-up) (BUG). MiG-29 20 vs
38; Su-24M 20 probably retired; all six air wings stacked in one state instead
of Karshi-Khanabad/Chirchiq/Jizzakh/Fergana/Tashkent; ground garrisons
generalised. Correctly omits the J-10CE (arrived July 2026). Sources:
Wikipedia (Uzbekistan Air and Air Defence Forces, Uzbek Ground Forces,
Karshi-Khanabad AB), asianmilitaryreview.com.

**UAE — minor deviations.** Strongest of the batch. P176 is *Al Hili*, not
"Shahama" (BUG); the two new Bani Yas/Gowind corvettes (2023–24) and Falaj 3
OPV missing; GlobalEye 3 vs 5, C-17 6 vs 8, Mirage 2000-9 55 vs 59; the 20
TB2s delivered 2022 missing; brigade names invented (open sources give only
generic types); correctly omits the Rafale (deliveries from 2027). Sources:
Wikipedia (UAE Navy/Air Force/Army), saab.com, globalsecurity.org.

### 4.6 Secondary powers A (ITA, SAU, EGY, PAK, UKR, NKO)

**ITA — minor deviations.** Ships essentially correct (Cavour, Trieste, both
Horizons, 8 FREMMs, 4 Type 212A, 3 PPAs). Errors: Ariete in Veneto (real:
Friuli), Folgore and Col Moschin in Puglia (real: Tuscany), submarine command
at Taranto not Sicily; FREMM 8 vs 10 (F598/F599 delivered 2025), PPA 3 vs 4,
Sauro-class subs missing, Tornado 15 vs 35, F-35B 7 vs 15, C-130J 22 vs 13.
Sources: navalnews.com, fincantieri.com, marina.difesa.it, Wikipedia (Italian
Army/Navy/aircraft).

**SAU — wrong, needs rework (navy + drones).** The two fleets are based in
each other's ports — Western Fleet should be Jeddah, Eastern Fleet Jubail
(BUG); "Al Yamamah" is not a Badr-class ship (Badr class: Badr, Al Yarmook,
Hitteen, Tabuk) (BUG); the entire Al Jubail/Avante 2200 class (5 corvettes,
2022–25) missing; a 12-aircraft **MQ-9A Reaper wing does not exist** in Saudi
service (BUG — only negotiations for MQ-9B); Tornado 24 vs 81; F-15 family
counts low; SANG brigades are named, not numbered; Royal Saudi Marines are 2
brigades. Ground list broadly plausible. Sources: Wikipedia (Royal Saudi
Navy/Air Force/National Guard/Marine Forces), breakingdefense.com.

**EGY — minor deviations.** Phantom "23rd Armoured Division" (real armoured
divs: 4th, 6th, 9th, 21st); 6th is armoured, not mechanized; missing mech
divisions 16th/23rd/33rd/36th; navy omits the 4 MEKO A-200 frigates, the 3rd
FREMM (*Bernees*) and 2 of 4 OHPs; Gowind pennants wrong; 4 Romeo-class subs
still active; Rafale 36 vs 46, F-16 180 vs 220, Mirage 2000s missing. Named
ships that are present are all real. Sources: Wikipedia (Egyptian Army,
Egyptian Navy, Egyptian Air Force), navalnews.com.

**PAK — wrong, needs rework (navy).** Type 054A/P names wrong — 3rd is *Tippu
Sultan* (F-263), 4th *Shah Jahan* (F-264); "PNS Badr" is a Babur-class
corvette, "PNS Hunain" a Yarmook-class (BUG); **PNS Hangor was only
commissioned 30 Apr 2026** — not in service on 1 Jan 2026 (BUG); the two
newest in-service ships (PNS Babur F-280, PNS Khaibar F-282, commissioned
21 Dec 2025) are missing. Army: phantom "2nd Armoured Division"; extensive
basing errors (most divisions placed in Gilgit-Baltistan/Sindh/Balochistan
are actually Punjab/KP garrisons); 37th is mechanized, 35th infantry. Air
types right (J-10CE, JF-17, F-16, Mirage ROSE) but F-16 45 vs 75, Mirages
30 vs 170+. Sources: Wikipedia (Tughril class, Yarmook class, Hangor class,
Babur class, PAF), globalsecurity.org, defensenews.com, navalnews.com.

**UKR — wrong, needs rework (game-breaking).** Six brigades — 93rd Mech,
54th Mech, 35th/36th Marine, 118th TDF, 55th Artillery — are placed inside
**Russian-held Crimea** (Sevastopol, Simferopol, Kerch, Dzhankoi) while
Donetsk, Luhansk, Zaporizhzhia and Kherson have **zero** Ukrainian units, in a
mod whose start is the ongoing Russo-Ukrainian war (BLOCKER). Force size 29
manoeuvre units vs 60+ real brigades and no corps HQs; 38th Marine Brigade
and the Mirage 2000-5F (~4–5 in service) missing; naval pennants wrong
(Sandown-class are M310/M311). F-16AM count plausible; correctly omits the
Ada-class corvette (still on trials). Sources: militaryland.net,
en.wikipedia.org (Ukrainian Marine Corps, Ukrainian Navy), global.espreso.tv.

**NKO — minor deviations.** ~11,000 KPA troops were in Russia's Kursk oblast
at the start of 2026 — not represented (major omission). Correctly omits the
Choe Hyon-class destroyers (commissioned June 2026) and the Hero Kim Kun Ok
submarine (not operational); ship/division names are placeholders; Pyongyang
Defence Artillery Division placed in Hamgyong. Sources:
kyivindependent.com, Wikipedia (Korean People's Navy/Army), CSIS Beyond
Parallel.

### 4.7 NATO / developed (CAN, SPR, SAF, SWE, FIN, GRE, ROM, HUN, CZE, BRM, NRY)

**CAN — minor deviations.** CF-188 55 vs ~88; CP-140 10 vs 14; 5th Harry
DeWolf-class missing (commissioned 13 Jun 2025); four reserve/regular
formations in the wrong province (2 CMBG is Petawawa not Manitoba, 5 CMBG
Valcartier not BC, 34 CBG Montreal not Ontario, 38 CBG Winnipeg not Alberta);
Canada's brigade-sized NATO mission in Latvia absent. Correctly no F-35 yet.
Sources: Wikipedia (CF-18, CP-140, Harry DeWolf class, Canadian Army), NATO
eFP, canada.ca.

**SPR — minor deviations.** P-3M Orion still listed — **type retired** (BUG);
Santa María class 3 vs 6; submarines 1 vs 2 (Galerna still serving); half the
army brigades in the wrong region (Madrid/Galicia/Zaragoza/Almería/Cádiz
scrambled); Spain-led NATO brigade in Slovakia missing; MQ-9 and AV-8B+
absent. Air wings/bases otherwise correct. Sources: key.aero,
armada.defensa.gob.es, NATO SHAPE, Wikipedia (Spanish Army/Navy/Air Force).

**SAF — minor deviations.** ANC coded as `communism` / `anarcho-communism` —
factually wrong (BUG, player-visible); readiness modelled at 75–85% when the
real SANDF has ~27% deployable personnel and near-zero ship/aircraft
availability; 43 SA Bde is Bloemfontein not Western Cape; 46 SA Bde
Johannesburg not Limpopo; Rooivalk (11) missing; "9 SA Division" and "General
Support Brigade" unverified. Sources: pmg.org.za, Wikipedia (SANDF, SAAF, SAN).

**SWE — minor deviations.** Submarines 2 vs 5 (Halland back in service,
Södermanland class); four army units in the wrong region (Boden in Stockholm
county, Skövde in Västerbotten, Gotland on the mainland, marines inland);
Sweden's battalion in NATO Bde Latvia and the FLF Finland framework role
missing; "S 102B Korpen" is SIGINT, not AEW (S 100B/D Argus are). Corvette
list accurate (Gävle retained). Sources: nti.org, euro-sd.com, nato.int,
Wikipedia (Swedish Army/Air Force).

**FIN — wrong, needs rework (navy).** FNS *Pohjanmaa* and *Häme* are listed
in service — the class is **not commissioned until 2027** (BLOCKER); Karjalan
Prikaati and Jääkäriprikaati swapped between Lapland and Karelia; Rauma class
3 vs 4; correctly no F-35A yet (arrives 2026). Sources: Wikipedia (Pohjanmaa
class, Finnish Army), janes.com, navalnews.com.

**GRE — minor deviations.** Navy roughly half-modelled: Elli-class (up to 9
frigates) and HS *Kimon* (FDI, handed over 18 Dec 2025) missing; F-4E (~30)
missing; 1st "Armoured Division" is really I Infantry Div and the armoured
division is XX; XVI is mechanized, not armoured; several units in
Thessaly/Southern Macedonia instead of Thrace/Aegean. Sources: Wikipedia
(Hellenic Navy/Army), navalnews.com, key.aero.

**ROM — minor deviations.** A 4-aircraft **MQ-9A squadron that Romania does
not own** (Reapers at Câmpia Turzii are US/Dutch) (BUG); five of nine
brigades in the wrong region (Bucharest/Constanța/Iași/Buzău/Focșani
scrambled); F-16AM 32 plausible; navy correct. Sources: af.mil,
airforce-technology.com, Wikipedia (Romanian Land Forces/Navy).

**HUN — minor deviations.** A Hungarian-owned C-17 that does not exist
(Hungary is in NATO's pooled SAC) (ACCURACY); the two real KC-390s (2024–25)
missing; 86th Szolnok is a helicopter base, not an infantry brigade; 2nd
"Árpád" is the SOF brigade; Tata/Debrecen in swapped regions; Gripen 14
correct for Jan 2026. Sources: Wikipedia (SAC, Hungarian Ground Forces),
embraer.com, janes.com.

**CZE — minor deviations.** Cleanest of the batch. 7th Mech Bde is Moravia
not Bohemia and 4th Rapid Deployment Bde Bohemia not Moravia (swapped); 13th
Artillery Regiment Jince is Central Bohemia not Šumava; C-295 4 vs 6; Babiš
(Dec 2025) correctly modelled. Sources: Wikipedia (Czech Army), mo.gov.cz,
czdefence.com.

**BRM — wrong, needs rework.** Air force modelled as a 2000s-era MiG-29B
force: omits the Su-30SME (delivered 2023–25), JF-17 (largely grounded), F-7M,
A-5C, FTC-2000G and K-8 — ~90 aircraft including the regime's strike assets;
total combat air 36 vs ~130; navy 1 vs 2 submarines; class/hull designations
unverifiable; LID basing ignores NUG/PDF control of much of the countryside.
Ground LID numbers are real. Sources: Irrawaddy, RFA, Wikipedia (Myanmar Air
Force/Navy/Tatmadaw).

**NRY — minor deviations.** "KNM Odda (P966)" does not exist — Skjold class is
P960–P965, lead ship *Skjold* omitted (BUG); P-8A 3 vs 5; F-35A 40 vs 49–52;
Ula class 5 vs 6 (S304 *Uthaug* missing); "Oslo Garnisonsgruppe" sits in
Trøndelag. Brigade Nord/Finnmark/SOF correct; correctly omits the 2025 Type 26
decision. The NOR→NRY patch rename is handled by the generator (verified by
the reproducibility check) — not a bug. Sources: Wikipedia (Skjold class,
List of RNoN ships), seaforces.org, breakingdefense.com.

### 4.8 Small NATO / other (HOL, DEN, BEL, POR, BUL, CRO, ALB, LIT, LAT, EST, SLO, SLV, SER, BOS, KOS, FYR, MNT, LUX, MLV)

**HOL — wrong, needs rework.** "13e Luchtmobiele Brigade" should be **11
Luchtmobiele Brigade**; "1e Gemechaniseerde Brigade" **does not exist** (the
third brigade is 13 Gemechaniseerde/Lichte Bde, Oirschot) (BUG ×2); **HNLMS
Walrus (S802) was retired 12 Oct 2023** (BUG); the fleet is missing 2
M-frigates, both LPDs, the new CSS Den Helder (2025) and the Alkmaar MCMs;
F-35A 52 vs ~48. Sources: globalsecurity.org, marineschepen.nl, Wikipedia
(43rd Mechanized Brigade, Dutch navy).

**DEN — minor deviations.** F-35A 27 vs 21 delivered (16 more ordered); F-16s
were still in service on 1 Jan 2026 (retired 18 Jan); the Knud Rasmussen
Arctic patrol ships (3) and Diana class are missing; Absalon pennants are now
F341/F342; the C-130J wing is at Aalborg not Sjælland. Sources: fmn.dk,
defensenews.com, aerotime.aero, Wikipedia (Danish navy).

**BEL — minor deviations.** First Belgian F-35As arrived at **Florennes** (2
Wing), not Kleine Brogel (BUG); "Paracommando Brigade" is a legacy name (the
Land Component has a Motorised Brigade + SOF Regiment); the navy is missing
the Castor patrol boats, 4 Tripartite MCMs and the new City-class BNS Oostende
(commissioned 3 Nov 2025); the A400M unit is at Melsbroek. Sources:
theaviationist.com, prnewswire.com, Wikipedia (Belgian Army/Navy).

**POR — minor deviations.** Viana do Castelo OPVs 2 vs 4 (P362 Sines, P363
Setúbal missing); "Brigada Ligeira de Intervenção" does not exist (it is
Brigada de Intervenção); Comando Norte is not on Madeira; the Mechanized
Brigade is at Santa Margarida not Lisbon. Core fleet (5 frigates, 2 subs)
correct. Sources: Wikipedia (Portuguese Navy, Brigada de Intervenção),
exercito.pt.

**BUL — wrong, needs rework.** BGS Gordi is **F43** (F42 is Verni); BGS
Reshitelni is a **Pauk-class ASW corvette (13)**, not a Wielingen frigate;
Bodri is a Pauk at Varna, not a Poti at Atia; the Wielingen trio is based at
Burgas (Atia), not Varna; missing Koni *Smeli*, Tarantul *Malniya*, the MCM
flotilla and the new **MMPV Hrabri (12), commissioned 8 Dec 2025**. F-16V 8
correct. Sources: Wikipedia (Bulgarian Navy/Air Force), sofiaglobe.com.

**CRO — wrong, needs rework.** "OB-51 Omiš / OB-52 Šibenik / OB-53 Cavtat" are
phantom hulls — only **OOB-31 Omiš and OOB-32 Umag** exist (Šibenik is
RTOP-21) (BUG); the class is Omiš, not Kralj; missing the 5 missile boats and
the Korčula minehunter; the Rafales (12, F3-R, national QRA from 1 Jan 2026 —
correct count) are at **Zagreb/Pleso**, not Slavonia; the army has one
armoured-mechanized and one mechanized guards brigade, not three numbered
ones. Sources: Wikipedia (Croatian Navy/Air Force), ac.nato.int, morh.gov.hr.

**ALB — minor deviations.** P131/P132 are **Iliria-class (Damen Stan 4207)**,
not Diciotti (BUG); P133/P134 and the 2025 ex-Italian corvette are missing;
the land force is one infantry brigade, not two. Sources: Wikipedia
(Albanian Naval Force).

**LIT — minor deviations.** "Aitvaras Brigada" is the **SOF squadron name**;
the third brigade is Aukštaitija (reserve) (BUG); naval pennants wrong
(P12 = Dzūkas, Aukštaitis = P14, Kuršis = M54, Sūduvis = M55) (BUG); Jotvingis
(N42) missing; **Leopard 2A8 deliveries start ~2027** — no MBTs in service on
1 Jan 2026. Sources: Wikipedia (Lithuanian Land Forces/Navy).

**LAT — minor deviations.** Minehunter class is **Tripartite** (Alkmaar is the
Dutch designation); "Mehanizeta Kaujinieku Brigade" is a spelling error for
Mehanizētā kājnieku brigāde; National Guard is regional, not one brigade.
Cleanest Baltic file; no combat aircraft is correct. Sources: Wikipedia
(Latvian Naval Forces), NATO Baltic Air Policing.

**EST — minor deviations.** **M313 is Admiral Cowan, Ugandi is M315** (BUG);
**Wambola is a Lindormen-class minelayer (A433)**, not a Sandown (BUG); after
the 2023 merger the navy also operates Kindral Kurvits (P101), Raju and Valve;
1st Brigade is at Tapa, not Tartu. Sources: Wikipedia (Estonian Navy).

**SLO — minor deviations.** F-16V 14 vs **10 in-country** (9 C + 1 D as of
30 Dec 2025; last 4 in the US until 2027); manoeuvre units are 1st/2nd
Mechanized Brigades; L-39s, UH-60Ms, Mi-17s and L-410s missing. Sources:
Wikipedia (Slovak Air Force), spravy.pravda.sk.

**SLV — minor deviations.** The **1st Brigade (western Slovenia) is missing**;
72nd Brigade is in Maribor (eastern Slovenia), not Carniola; the Special
Operations Unit is at Kočevska Reka. No fighters is correct for Jan 2026.
Sources: Wikipedia (Slovenian Armed Forces/Air Force).

**SER — minor deviations.** MiG-29 10 vs **14 (11 SM + 3 UB)**; J-22 Orao 10
vs 17; brigades are the 1st–4th Army Brigades (Novi Sad, Kraljevo, Niš,
Vranje); 63rd Parachute Bde missing; correctly no Rafales (deliveries ~2028).
Sources: Wikipedia (Serbian Air Force), vs.rs.

**BOS — minor deviations (most accurate small file).** Tactical Support Brigade
HQ is Sarajevo (armour in Tuzla), not Unsko-sanski; the three infantry
brigades and no-combat-aircraft are correct; helicopters (Huey II, Mi-8/17)
not modelled. Sources: Wikipedia (Armed Forces of BiH).

**KOS — minor deviations.** The KSF fields **three infantry regiments**
(Gjilan, Istog, Mitrovica) plus National Guard Command, not two brigades;
TB2 UCAVs and UH-60 procurement not modelled; two brigade-equivalents
overstates the ~4–5,000-strong force. Sources: Wikipedia (Kosovo Security
Force).

**FYR — minor deviations.** The manoeuvre formation is the **1st Mechanized
Infantry Brigade**, not a light infantry brigade; Special Operations Regiment
correct; no combat aircraft correct. Sources: Wikipedia (Army of North
Macedonia).

**MNT — minor deviations.** The army is **one active infantry battalion**
(Danilovgrad) plus reserve, not two brigades (roughly doubles the real force);
the navy is missing patrol boat P-105 Durmitor and the training ship Jadran.
Sources: Wikipedia (Armed Forces of Montenegro).

**LUX — minor deviations.** The A400M (CT-01) is operated from **Melsbroek,
Belgium** in the bi-national unit, not from Luxembourg; the H145M is missing;
one infantry battalion is correct. Sources: Wikipedia (Luxembourg Armed
Forces).

**MLV — stale 2000-era (BLOCKER).** A **6-aircraft MiG-29 squadron that does
not exist** — Moldova sold its MiG-29s in 1997 and the last non-airworthy
hulks were auctioned in 2010; the air force is transports and helicopters only
(1 An-26, An-2s, Mi-8/Mi-2). Two infantry brigades + "Fulger" SOF battalion is
otherwise a fair representation. Sources: Wikipedia (Moldovan Air Force).

### 4.9 West Asia (PER, TAI, VEN)

**PER (Iran) — wrong, needs rework.** Almost every named ground formation is in
the wrong province (16th Armd → Qazvin, 81st → Kermanshah, 88th → Zahedan,
92nd → Ahvaz, 21st → Tabriz, 58th is a Takavar div at Shahroud, 55th Airborne
→ Shiraz, etc. per ISW/CTP's 2025 ORBAT); "1st Sarallah IRGC Division" does
not exist (Sarallah is the Tehran HQ; the 41st is in Kerman) (BUG); **the IRGC
Navy is placed in landlocked Lorestan** (BUG); the IRGC division sites are
likewise shuffled. Navy: **IRIS Damavand (77) has been out of service since
Jan 2018** (BUG) — the Caspian flagship is *Deylaman* (78), which is missing;
only *Tareq* of the three Kilos was operational; IRIS Fateh is 920, not S-1.
Air: ~100–150 aircraft missing (Mirage F1, F-7, Kowsar, Su-22, Yak-130) plus
the entire IRGC missile/UAV force that is Iran's real strike power; F-4E 30 vs
~63. Sources: ISW/CTP Artesh OOB, Wikipedia (Iranian Army, IRGC Ground
Forces/Navy, IRIS Damavand, IRIN ships), aerocorner.com.

**TAI (Taiwan) — wrong, needs rework.** Ground data is the worst: **Kinmen
Defense Command placed in Tainan and Penghu Defense Command in Hualien** (wrong
islands) (BUG ×2); 8th Army is the *southern* corps but placed in Hsinchu;
10th Army has no infantry division; the two marine brigades are moved from
Zuoying onto offshore islands; reserve "divisions" should be ~12 brigades.
Navy: **ROCS An Chiang is PGG-625 (not 620) and Wan Chiang is PGG-626 (not
621)** (BUG ×2); only 3 of 7 Tuo Chiangs present; the Knox (Chi Yang) class
and two ex-US Perrys are missing; **ROCS Hai Kun was still in sea trials on
1 Jan 2026** (delivery target June) (BUG). Air: F-16V 150 vs ~138 upgraded
Block 20s (zero Block 70 in-country until Aug 2026); F-16 wings placed at
Hsinchu/Kaohsiung instead of Chiayi/Hualien; Mirage 2000-5 45 vs 52; F-CK-1
100 vs 129; E-2K 6 vs 5. Sources: Wikipedia (ROC Army, ROCN ships, Tuo Chiang
class, Hai Kun class, ROCAF), USNI News.

**VEN (Venezuela) — wrong, needs rework.** Navy: **F-21 Mariscal Sucre is a
partially sunk hulk at Puerto Cabello** and **PC-22 Warao has been out of
service since 2012** (interned in Brazil) (BUG ×2); only *Almirante Brión* is
operational, one Type 209 usable; the navy is based at Puerto Cabello/La
Guaira/Punto Fijo, not "Miranda". Air: **the F-5A/B flight is a ghost — the
type was retired in 2010** (BUG); Su-30MK2 21 (≈13 serviceable) correct; F-16
home base is Maracay (Aragua), not Miranda; C-130H 6 vs 3–4. Ground: 41st
Armd Bde is Carabobo, 42nd Airborne is Aragua, "1st Armored Brigade" should be
the 11th, 32nd is a Ranger brigade and 33rd a Signals brigade, jungle brigades
are 51st/52nd/53rd; the army has 6 divisions, not 16. Baseline (pre-3 Jan
2026) is otherwise valid. Sources: Wikipedia (Lupo class, Bolivarian
Navy/Army/Aviation), armyrecognition.com.

### 4.10 Asia-Pacific (BRA, AST, IND)

**BRA (Brazil) — wrong, needs rework.** **Tamandaré (F200) was not
commissioned until 24 Apr 2026** (BUG); **Niterói (F40) was decommissioned in
2019** and **Tamoio (S31) in Sep 2023** (Tikuna S34 is the missing active boat)
(BUG ×2); **1ª and 2ª Brigada de Cavalaria Blindada do not exist** (BUG ×2);
all five jungle brigades are placed in the south-east/south instead of
Amazonia (1ª Boa Vista, 2ª São Gabriel, 16ª Tefé, 17ª Porto Velho, 23ª
Marabá); 4ª/9ª/10ª motorised brigades are Juiz de Fora/Rio/Recife, not the
north; 6ª is armoured (Santa Maria), not light; the parachute brigade is Rio,
not São Paulo. Air: **40 AMX modelled vs fewer than 6 airworthy**, and at
bases the type left years ago (BUG); Gripen 24 vs 11 delivered (no F-variant
existed in 2026); P-3AM squadron moved to Rio. Correct: NAM Atlântico,
Defensora, Constituição, Barroso, Riachuelo/Humaitá/Tonelero, Tupi, KC-390
count. Sources: Brazilian Navy/TKMS, defesaaereanaval.com.br, pt.wikipedia
(Army brigades), tecnodefesa.com.br, airdatanews.com.

**AST (Australia) — wrong, needs rework.** **HMAS Anzac (FFH-150) was
decommissioned 18 May 2024** and **HMAS Pilbara was launched Oct 2025 but not
commissioned** (pennant will be OPV 205, not 302) (BUG ×2); Arafura is OPV 203,
not 301; Supply/Stalwart missing. Army: **1st and 3rd Brigades are swapped**
(1st is light/Darwin, 3rd is armoured/Townsville); three of six reserve
brigades in the wrong state (5th NSW, 9th SA, 11th Qld); 8th is a training
formation, not manoeuvre; 10th (Fires/HIMARS) missing. Air: F-35A 50 vs 72
(all delivered by Dec 2024); F/A-18F and EA-18G are at Amberley (Qld), C-130J
at Richmond (NSW), P-8A at Edinburgh (SA). Correctly omits Hunters and AUKUS
SSNs. Sources: defence.gov.au, navalnews.com, psnews.com.au, Wikipedia
(Australian Army brigades, RAAF squadrons).

**IND (Indonesia) — minor deviations (navy strong).** Every one of the 17
named ships and hull numbers checks out for 1 Jan 2026, including the
submarines and KRI Bung Karno (369); aircraft types largely match (Su-27 5,
Su-30 11, Hawk 209 21, Super Tucano 13, CN-295 9, CH-4B 6); Rafale correctly
absent (first 3 arrived 23–26 Jan 2026). Ground: five brigades and both raider
battalions are in the wrong province or under the wrong command (Brigif 9/18
under Kostrad, 16 under Kodam V, 21 Kupang, 22 Gorontalo, Yonif 300 Cianjur,
400 Semarang); F-16A/B are Block 15 OCU/eMLU, not "ADF"; F-16C/D 20 vs 23.
Sources: Wikipedia (Indonesian Navy/Air Force equipment), id.wikipedia unit
pages, thejakartapost.com.

### 4.11 Conflict zones (SYR, YEM, ETH, AFG, SUD, BLR, GEO, ARM)

**SYR (Syria) — wrong, needs rework.** The three divisions in Lebanon are a
province-ID error (BLOCKER, already caught statically). **The navy is
fictional**: the two ships (Tishreen, Al Assad) were destroyed or retired —
Israel sank the Syrian fleet at Latakia on 9–10 Dec 2024, and both Petya
frigates were derelict/retired by 2018 (BLOCKER). **The air force is
fictional**: the 6 MiG-29A + 10 L-39ZA at Damascus were destroyed in the Dec
2024 strikes; by 2026 only a handful of refurbished L-39/Su-22 fly (BLOCKER).
Ground names are generic; real numbered divisions (50th Coastal, 56th, 60th,
76th/80th, 44th SF) and the five-corps structure exist. **Content bug:** the
2026 setup pre-completes Ba'athist path focuses for the post-Assad government
— `SYR_iranian_sponsorship` (grants the *iranian_aid* idea!),
`SYR_support_hezbollah`, `SYR_expand_tartus_base`, `SYR_reaffirm_claims_on_hatay`,
`SYR_affirm_presence_in_lebanon`, `SYR_concentrate_on_lebanon`,
`SYR_invest_in_lebanon`, `SYR_relocate_lebanese_industry`,
`SYR_harbor_extremists`, `SYR_reduced_political_liberty` (10 of the 39 deferred
focuses) — these should be added to `unsafe_focuses.json` or given 2026
rewards. Sources: navalnews.com, nytimes.com, Wikipedia (Syrian Navy/Air
Force/Army), militarnyi.com.

**YEM (Yemen) — wrong, needs rework (faction mash-up).** The tag installs the
PLC's chairman (al-Alimi) as leader but fills the army with Houthi divisions
("Ansar Allah"), and **four of eleven divisions sit in STC-held territory**
(Aden, Hadramaut, Al Mahrah, Socotra) on 1 Jan 2026 (BUG ×4). Province IDs
contradict the file's own comments throughout ("Saada" in an Aden province,
"Hodeidah coast" in Al Bayda, "Marib front" in Al Mahrah). No IRG/PLC
formations at all. The Houthi drone wing is a good abstraction. Fix: either
split the Houthis onto MD's `HOU` tag or rename the divisions to PLC
formations and move the Houthi-named ones north of the front. Sources:
congress.gov CRS R48942, Wikipedia (Fall of Aden 2026, southern Yemen
campaign), commonslibrary.parliament.uk.

**ETH (Ethiopia) — wrong, needs rework.** **Four divisions named "Ye Fano
Hayl" are the Amhara insurgent militia at war with the ENDF** (BUG), and they
are deployed in Ogaden, Southern Ethiopia, Afar and Tigray — not Amhara —
while there is **no ENDF unit in Amhara**, the actual active front. Air:
16 "Su-27SK/Su-30MK" vs ~20 Su-27SK + 2 Su-30K (no Su-30MK in service);
C-130 4 vs 2. TDF forces not modelled (clashes resumed 26 Jan 2026).
Sources: Wikipedia (Ethiopian Air Force, Fano insurgency), dw.com,
conflictzone.io, acleddata.com.

**AFG (Afghanistan) — minor deviations.** Nine of eleven divisions are stacked
in Badakhshan/Nuristan/Kunar instead of the corps locations their comments
describe (Kabul 313 Central, 201 Khalid Ibn Walid, 205 Al-Badr, 207 Al-Farooq,
209 Al-Fatah, 215 Azam, 217 Omari); "Badri 313" is a battalion, not a
division; **no air element at all** although the Islamic Emirate Air Force
flies ~34 airframes (A-29, MD530F, Mi-17/25, UH-60, C-208). The Bactria
placement resolves at startup via the TAL annexation (confirmed not a bug).
Sources: Wikipedia (Afghan Armed Forces/Air Force).

**SUD (Sudan) — wrong, needs rework.** Four divisions are inside **South
Sudan** (BLOCKER, already caught statically — and the mod's own on_actions
white-peaces SUD–SSU). Five divisions are in **Darfur**, which the RSF
controlled by Jan 2026 after El Fasher fell on 27 Oct 2025 (BLOCKER). Province
IDs contradict the comments (Khartoum/Port Sudan garrisons are misplaced).
Names are generic; real formations are numbered (6th Infantry, 7th Armoured,
9th Airborne + regional commands). Sources: armedconflicts.org, fews.net,
Wikipedia (Sudanese Armed Forces).

**BLR (Belarus) — minor deviations.** Six of seven ground units are in the
wrong city and **the two airborne brigades are swapped** (38th is Brest, 103rd
is Vitebsk); Su-30SM belong at Baranovichi, not Minsk; "927th"/"206th" air
base designations no longer exist. **The Russian military and nuclear presence
is not modelled** — a defining 2026 feature (Iskander-M, Oreshnik, Zapad-2025).
Sources: Wikipedia (Armed Forces of Belarus, Western Operational Command),
militarnyi.com, belta.by.

**GEO (Georgia) — minor deviations.** Two divisions are parked in Batumi
(real: battalion-sized light infantry only); the second artillery brigade is
missing; 3rd Brigade/1st Artillery are at Gori, not Tbilisi. Air (Su-25KM,
TB2) and brigade count are recognisable. Sources: Wikipedia (Georgian Land
Forces, Defence Forces of Georgia).

**ARM (Armenia) — minor deviations.** Deployment is mislabelled: three units
in Gegharkunik-Tavush and three in Yerevan-Gyumri, **nothing in Syunik** (the
most sensitive sector); real force is corps-based (2nd/3rd Army Corps, 2026).
Su-30SM 4 correct; Su-25 8 vs ~15. **The Russian 102nd Military Base at
Gyumri is not modelled**, and the post-2022 rearmament (French APCs, Indian
artillery, US V-BAT drones) is absent. Sources: armenpress.am, Wikipedia
(Armed Forces of Armenia), evnreport.com, militarnyi.com.

**Cross-cutting from this batch:** MD's state *file names* are unreliable
(`220-Kassala.txt` is localised "Khartoum", `221-Khartoum.txt` is "River
Nile") — the digest and this audit use localisation/VP evidence, so trust the
digest state names. The `ruling party = communism` label appears for GEO, ARM,
ETH and BLR — a party-array mapping artefact worth checking separately.

## 5. Politics / economy 2026

Verified against IMF WEO Oct-2025 / World Bank 2025 data and 2026 news
sources. **All 30 bookmark leaders are correct for 2026-01-01** — no wrong
names. The problems are stale election dates, missing 2026 events, and
GDP/debt figures.

### 5.1 High-severity political findings

| Tag | Finding | Severity |
|---|---|---|
| UKR | `elections_allowed = yes` — martial law (extended 14 Jan 2026) bars elections | BUG |
| HOL | Data is a 2023 snapshot: election date 2023.11.22 (real 2025.10.29), coalition/party shares pre-date the PVV/NSC walkout; Schoof correct for Jan 1 | ACCURACY |
| KOR | `last_election` 2024.4.10 — the snap presidential election was 2025.6.3 | BUG |
| KOS | `last_election` 2021.2.14 — snap election 2025.12.28; Kurti was caretaker | BUG |
| MLV | `last_election` 2023.7.11 — parliamentary election was 2025.9.28 (the value looks like the 2021 date) | BUG |
| EGY | `last_election` 2024.12.10 matches nothing — parliamentary election 10–25 Nov 2025 | BUG |
| NRY | `last_election` 2021.9.13 — was 2025.9.8 | BUG |
| ALB | `last_election` 2025.4.25 — was 2025.5.11 | BUG |
| POR | `last_election` 2024.3.10 — was 2025.5.18 | BUG |
| BRM | `elections_allowed = no`, 2000.1.1 — elections were held 28 Dec 2025–25 Jan 2026 | BUG |
| PER | The Dec-2025/Jan-2026 protest wave and crackdown (started 28 Dec 2025, before the start date) is not modelled; the nuclear-crisis chain (`md2026_mideast.20–22`) does exist | ACCURACY |
| VEN | The crisis chain (`md2026_venezuela.*`) exists; the 3 Jan 2026 US strike is 2 days after the start, so modelling it as a pending event would be an improvement, not a bug | NOTE |
| ARM | `set_popularities` (communism 50) vs `party_pop_array` (Conservative 0.50, Communist-State 0.03) — internally inconsistent; MD's taxonomy maps Conservative into the communism family, so it is partly a taxonomy artefact | NOTE |
| GEO | Georgian Dream coded under `Autocracy`/communism family — taxonomy artefact | NOTE |
| SAF | ANC coded `anarchist_communism` — factually wrong (see 4.4) | BUG |

Missing 2026 transitions that would make good event content: Japan snap
election (8 Feb), Kosovo government (11 Feb), Netherlands (Jetten, 23 Feb),
Denmark (24 Mar), Bulgaria (19 Apr, after the Dec-2025 resignation and euro
adoption on 1 Jan), Serbia (Oct), Syria SDF integration (Jan), UK leadership
(Jun).

### 5.2 GDP per capita outliers (mod value → reference)

TUR 13.0 → ~18.6 (−30%), MNT 12.0 → ~7.5 (+53%), UZB 2.5 → ~4.0 (−37%),
KYR 1.7 → ~3.1 (−45%), ALB 8.0 → ~12.7 (−36%), POL 22.0 → ~28.4 (−23%),
TAJ 1.1 → ~1.7 (−33%), plus borderline BOS/FYR/BLR/BUL/SER (−21–24%).
Denmark 67.0 and Saudi 30.0 are inside 20% of the reference — not errors.

### 5.3 Debt

`tools/economy_report.py` never checks debt, and the reference comparison in
the subagent report used IMF *general government gross debt* while MD's own
2000 values are closer to **central-government debt** (e.g. MD Canada 2000 =
804 vs general-government ≈ 590; MD UK 2000 = 840 vs general-government
≈ 600). Under MD's convention our 2026 values are broadly plausible
(CAN 1400, ENG 2800, POL 380, TUR 480 all sit on plausible
central-government trajectories), but the **Taiwan value (30) is clearly
wrong** — Taiwan's government debt is ~$200bn+ and the mod also sets
`treasury = 50` which exceeds it, which is incoherent (BUG). Recommend
documenting the debt definition in `docs/Economy-2026.md` and adding a debt
sanity check to `economy_report.py`.


## 6. Runtime risks (cannot be verified statically)

1. Whether `AFG` annexation of `TAL` at `on_startup` runs before the first
   daily tick (units on foreign soil).
2. Whether duplicate `global.nato_members` entries actually double-count in
   MD's NATO tally loops (C-01) — needs a save/console check.
3. Air wing spawning from combined `set_oob` files (D-02) — check the air
   base screen on day 1.
4. The 2118 pre-completed focuses run on `on_startup`/`on_daily`; check
   `error.log` for focus rewards that reference missing systems.
5. Legacy-war settlement in `md2026_on_actions.txt` (Chechnya, Aceh, Tamil
   Eelam, Afghanistan, Eritrea, South Sudan, African rebels) — verify no
   leftover wars on day 1.

## 7. Prioritised recommendations

**Game-breaking / visible on day 1 (fix first):**

1. **Misplaced deployments** (O-02): USA 2nd ID in Pakistan; German brigade in
   Kaliningrad; five Russian armies in Yunnan; six Ukrainian brigades in
   Crimea; Sudanese units in South Sudan; Syrian units in Lebanon; Afghan
   units on TAL soil. These are single province-ID changes with outsized
   impact.
2. **Phantom platforms** (ships/aircraft that did not exist on 1 Jan 2026):
   USA Anzio/Vella Gulf/Lyndon B. Johnson; UK Lancaster/Northumberland/Albion/
   Bulwark; France Émeraude; Brazil Tamandaré/Niterói/Tamoio; Australia
   Anzac/Pilbara; Finland Pohjanmaa/Häme; Taiwan Hai Kun; Pakistan Hangor;
   Iran Damavand; Venezuela F-21/PC-22/F-5 flight; Moldova's MiG-29 squadron;
   Saudi MQ-9A wing; Romania MQ-9A wing; Spain P-3M; Germany P-3C; India
   Chakra III/Triput; Turkey İzmir/Murat Reis; Kazakhstan MiG-29/MiG-31;
   Netherlands Walrus; Croatia's Omiš-class phantoms; Estonia M313/Wambola.
3. **AFG/TAL design decision** (D-01) — pick one tag and make the 2026 setup
   consistent.
4. **NATO/CSTO array ordering** (C-01, C-02) and the **Indonesian naval base
   province** (O-03).

**Accuracy (second pass):**

5. **Ground basing** — a systematic re-map is needed: the same pattern (units
   in the wrong region even when the unit is real) appears in ~30 countries.
   Cross-check every division against its real 2025 garrison.
6. **Foreign deployments** — add the missing ones (Canada/Spain/Sweden NATO
   brigades, US 3rd Marine Division in Okinawa, North Korean troops in Kursk,
   Israeli Gaza/Lebanon/Syria positions, Russian units in occupied Ukraine).
7. **Procurement timing** — move all 2026 deliveries to a "not yet in
   service" state (the mod is consistently 1–2 years early).
8. **Naval registers** — names/hull numbers/classes need a pass in nearly
   every country (9 of 19 small-NATO files have at least one wrong hull).
9. **Air counts** — most are 20–50% low or high; a full re-count against
   World Air Forces 2026 would fix them.

**Content / data:**

10. **Election dates** (10 countries), **Ukraine elections_allowed**,
    **Taiwan debt**, and the **GDP outliers** (TUR, MNT, UZB, KYR, ALB, POL,
    TAJ).
11. **Party-popularity gaps** (H-04) and the **South Africa ANC ideology**
    coding.
12. **Tooling**: fix the hardcoded paths (T-01); add the OOB basing check
    (O-02), a debt sanity check to `economy_report.py`, and a phantom-platform
    checklist to the validator so this audit is repeatable.
13. **Runtime verification**: the five items in section 6, plus the
    `set_oob`/`air_wings` check (D-02).
