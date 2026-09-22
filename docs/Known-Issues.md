# Known Issues

## Fixed in 1.2.0 (September 2026)

The 2026 data and OOB pass:

- **Orders of battle** - every 2026 OOB now has a non-No-Step-Back variant
  (`history/units/<TAG>_2026_nonnsb.txt`, see `tools/make_nonnsb_oob.py`); the
  bookmark no longer falls back to Millennium Dawn's 2000 army. Indonesia and
  Venezuela received their own 2026 OOB (`IND_2026_*`, `VEN_2026_*`).
- **Stockpiles work** - MD's `set_oob` runs `instant_effect` with
  `add_equipment_to_stockpile`, and an equipment version only exists after the
  technology that unlocks it is granted. All 65 history patches now grant the
  2026 technology tiers *before* `set_oob`, and stockpiles are produced by the
  country itself (a foreign producer's history has not run yet at that point).
- **Equipment names** - the 2026 OOBs used vanilla names that Millennium Dawn's
  `replace_path` removes (`CAS_equipment_2`, `heavy_fighter_equipment_2`,
  `artillery_equipment`) and MD 1.x names; they are mapped to MD 2.0 equipment
  (`tools/fix_oob_equipment.py`). Air wings were silently empty before.
- **Norway's tag** - `history/units/NRY_2026_nsb.txt` used `NOR`, which no
  longer exists (21 "Unexpected token: owner" errors).
- **Ukraine's territorial defence** - MD's `05_ukraine.txt` creates units with
  `division_template = "Bryhada TRO"` without defining it; our UKR 2026 OOB now
  provides the template, so the reward works.
- **MD's hidden `Light_*` sub-units** - MD declares `group = support` without
  listing `support` in the type, logging nine errors at startup. The generator
  writes a fixed copy (`common/units/MD_regimental_support.txt`).
- **Vanilla SIA operation** - MD replaces `common/scripted_effects`, so vanilla's
  `SIA_plant_indochina_port_charges` was reported as an invalid effect;
  `common/scripted_effects/md2026_vanilla_compat.txt` defines it (and its
  detonation counterpart) as no-ops, since Siam has no Indochina tree under MD.
- **China's air wings** - two wings used state 585 (Western Sichuan), which has
  no air base; they moved to 586 (Sichuan).
- **Ideology case** - MD writes `Democratic`, `Nat_populism` and
  `has_government = Democratic` in several focus rewards; the game is case
  sensitive, so those effects did nothing. The generator normalises the case in
  the files we override.
- **Focus overrides** - four 2026-relevant focuses that the safety filter used to
  skip are adapted (`patches/focus_overrides.json`): `RAJ_bharatiya_janata_party`
  (BJP rules in 2026), `SOV_putin` (Putin branch opens; the 2000-era election
  event and the 2000-era party switch are removed), `GEO_gergiandream2013` and
  `EGY_al_sisi_rise` (el-Sisi is already the 2026 president, so the reward no
  longer creates a duplicate leader).
- **Localisation** - English is complete (the bookmark referenced
  `NRY_MD2026_DESC` while the file defined `NOR_MD2026_DESC`), a Polish
  translation is included, and `tools/validate.py` now fails on missing or
  duplicate keys.
- **Indonesia and Venezuela** are selectable in the 2026 bookmark.

## Open issues

### Coverage of Millennium Dawn's own-tree countries

The 2026 bookmark is complete for its 30 countries (patch, focus branch and both
OOB variants - enforced by `tools/validate.py`). 79 other countries that have
their own focus tree in Millennium Dawn do not have a 2026 history patch yet:
their 2026 start uses MD's 2000-era politics and parties at the 2026 date. The
full list and the reasoning (breakaway tags, generic-tree countries, priority
lists) are in `docs/Coverage.md`.

### Focuses that are deliberately not pre-completed

47 path/political focuses are skipped by the pre-completion safety filter,
because their rewards would rewrite the 2026 government, release countries,
start civil wars or fire 2000-era events. They are grouped below; the intention
is to keep the real 2026 starting position, not MD's 2000 branching.

- **Post-Assad Syria exclusions** (manual entries in
  `patches/unsafe_focuses.json`): `SYR_iranian_sponsorship`,
  `SYR_support_hezbollah`, `SYR_expand_tartus_base`,
  `SYR_reaffirm_claims_on_hatay`, `SYR_affirm_presence_in_lebanon`,
  `SYR_concentrate_on_lebanon`, `SYR_invest_in_lebanon`,
  `SYR_relocate_lebanese_industry`, `SYR_harbor_extremists`,
  `SYR_reduced_political_liberty` (the 2026 government is not the Ba'athist
  autocracy and no longer has forces in Lebanon or a Russian base at Tartus).

- **Party path starters** (would change the 2026 ruling party):
  `RAJ_indian_national_congress`, `RAJ_communist_party_of_india`,
  `RAJ_communist_party_of_india_marxist`, `RAJ_bahujan_samaj_party`,
  `RAJ_samajwadi_party`, `SOV_reign_of_yeltsin`, `SOV_zyuganov`,
  `SOV_zhirinovsky`, `UKR_cpu_start`, `UKR_party_regions_start`,
  `UKR_poroshenko_start`, `UKR_spu_start`, `UKR_ukraine_always_right`,
  `UKR_vitrenko_party`, `UKR_ukraine_elections`, `ARM_echoes_of_1999`,
  `ARM_triump_revolution_barhat`, `BLR_soviet_system` (an alt-history fascist
  path with a fictional leader), `EST_estonias_future`, `HOL_gay`, `HOL_paars`,
  `HOL_royal_wedding`, `HOL_threats_against_politicians`,
  `HOL_un_mission_ehtiopia`, `SYR_bashar_al_assad`, `TUR_only_getting_started`
  (an alt-history "Anatolian Syndicate" tag), `USA_focus_secretary_to_president`.
- **Civil war / war starters**: `POL_betray_the_communists`,
  `POL_socialdemocracy` (also fires `poland_news.34`, whose options are invalid
  in 2026 - 148 log lines), `EGY_dontallow_copt_pol`, `PER_descend_on_iraq`,
  `FRA_haitian_coup`, `USA_focus_congressional_chaos`.
- **Country releases and alt-history**: `ETH_eritrea_federation`,
  `ETH_eritrea_start`, `SYR_withdraw_from_lebanon`,
  `SYR_assassinate_lebanese_prime_minister`.

Adding more of them needs a hand-written 2026 reward in
`patches/focus_overrides.json` (see `docs/Architecture.md`).

### MD-side entries that remain in `error.log`

- `common/scripted_guis/02_conditional_peace_deals_scripted_gui.txt`:
  `Unexpected token: context_type`. MD's own comment says the value is
  intentional and that changing it breaks the diplomatic-action entry point.
- `common/national_focus/05_netherlands.txt`: `complete_special_project:
  project sp_space_program in already completed. do nothing.` - triggered by
  the pre-completed `HOL_space_efforts`. MD completes the project during its own
  startup pass; the message is informational and the other rewards still apply.
- `Unknown equipment type: ship_hull_*` at startup: MD's own
  `common/ai_equipment/*` files still reference vanilla ship hulls that MD
  replaced. Only MD's AI design templates are affected; no 2026 content uses
  those names.
- `create_unit with unknown division template` for ~52 of MD's own focus
  rewards (e.g. `Aidar Battalion`, `Albionis Special Forces Brigade`): MD never
  defines those templates. Only MD's 2000-era rewards are affected.

### OOB equipment tiers

Lower-tier equipment names still use MD 1.x digits in places (an F-16 wing may
field a 1985 airframe). 5th-generation air wings were upgraded with
`tools/fix_oob_tiers.py`; a full generation mapping is future work
(`docs/Order-of-Battle.md`).

### Bookmark picture

The 2026 bookmark uses `GFX_select_date_2000`, which is not defined by MD or
vanilla; MD's own `blitzkrieg` bookmark uses the same sprite, so the game falls
back to the default background. A 2026 date picture is future work.

### Economy data

`docs/Economy-2026.md` compares the shipped GDP/debt values with indicative 2025
reference data and runs a debt sanity check (`tools/economy_report.py`): `debt`
is central-government gross debt, must be positive and must not be smaller than
`treasury`. Two GDP entries (North Korea, Syria) differ from the reference but
are kept because both reference values are uncertain.

## Pending runtime verification

The 2026 audit (`docs/Audit-2026.md`, section 6) lists behaviour that cannot be
verified statically. The matching checks are in `docs/Testing.md`:

1. The AFG setup: TAL's states are transferred to AFG at `2026.1.1`
   (`patches/history_states/409,410,412,414,415,1152,1207,1208.txt`) and the
   `TAL` -> `AFG` annexation still runs at `on_startup` as a fallback - confirm
   TAL does not exist on day 1 and no unit is destroyed on foreign soil.
2. Duplicate `global.nato_members` entries: the USA patch now only adds MNT,
   FYR, FIN and SWE (MD's `setup_global_arrays` adds the rest), and the CSTO
   removal of ARM moved to `md2026_on_actions.txt` because MD re-adds it at
   `on_startup` - spot-check the arrays in a save/console.
3. `air_wings` inside a file loaded by `set_oob`: the layout is unusual (MD and
   vanilla use separate `set_air_oob` files), but vanilla's `PAK_1936` uses the
   same combined layout and the 1.2.0 history (empty wings before the equipment
   fix) shows the loader parses the block. **Verify the air base screen on day 1**;
   if the wings are missing they must move to `set_air_oob` files.
4. The pre-completed focuses run on `on_startup`/`on_daily`; check `error.log`
   for focus rewards that reference missing systems.
5. Legacy-war settlement in `md2026_on_actions.txt` (Chechnya, Aceh, Tamil
   Eelam, Afghanistan, Eritrea, South Sudan, African rebels) - verify no
   leftover wars on day 1.

## Troubleshooting

### The mod does not appear in the launcher

Run `pwsh -File tools/install_mod.ps1` - it creates the junction and the
`md-2026.mod` descriptor. Then restart the launcher.

### The 2026 bookmark does not appear

Make sure both Millennium Dawn and this submod are enabled in the same playset,
with MD loading first (the `dependencies` field handles that). Check
`logs/error.log` for `md2026` entries.

### Regenerating after a Millennium Dawn update

```bash
python tools/rebase.py generate
python tools/validate.py
python tools/audit_2026.py --write
```

Fix any errors reported by the validator (usually a rename in
`patches/mappings/*.csv` or in `patches/history_countries/*`).
