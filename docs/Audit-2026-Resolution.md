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
| `tools/fix_oob_locations.py`, `tools/fix_politics_2026.py`, `tools/fix_party_arrays.py` | the migration scripts that applied the O-02 and politics fixes |
| `tools/check_oob_layout.py` | diagnostic for the D-02 combined-OOB layout |

## 5. OOB reality audit (section 4)

<!-- filled in after the country work -->
