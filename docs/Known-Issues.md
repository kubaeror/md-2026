# Known Issues

## Fixed in the 2.0.0 rebase (September 2026)

The previous version of this submod was built against Millennium Dawn 1.12.3 / HoI4 1.17 and
was broken on MD 2.0.0 / HoI4 1.19. The rebase fixed, among others:

- the mod was not registered in the launcher at all (no `.mod` file, no thumbnail),
- `replace_path="common/bookmarks"` replaced MD 2.0's bookmarks with a stale copy
  (19 invalid ideas and 18 invalid focuses in the 2000 bookmark),
- 22 stale focus tree copies duplicated ~8,000 focus ids instead of overriding MD's renamed
  tree files, so the 2026 branches never appeared,
- 12 stale character files removed 237 MD 2.0 characters (UKR alone lost 148),
- 66 country history copies referenced 1,853 technologies and 394 ideas that no longer exist
  in MD 2.0,
- state files lost MD 2.0 resources, buildings and state variables,
- Norway's content used the old `NOR` tag (MD 2.0 uses `NRY`),
- 30 duplicate localisation keys, broken accent encoding,
- war exhaustion counter was never initialised, NATO membership used the pre-2.0 system,
- 134 pre-completed focuses referenced focus ids that no longer exist,
- missing GFX sprites (event pictures, focus icons, idea pictures).

`tools/validate.py` now reports **0 errors** against MD 2.0.0.

## Open issues

### 2026 real-world data pass (September 2026)

A full audit against real January 2026 data corrected nine leaders (Japan, South Korea,
Czechia, Belgium, Iceland, Lithuania, Serbia, Bulgaria, Romania), India's and Turkey's
ideology, North Korea's leader ideology, Moldova's ruling party, the Japanese emperor
idea, the BRICS membership list (Indonesia was missing), three GDP values and the
US-Venezuela crisis (new `events/md2026_venezuela.txt`).

`MD`'s 2000-era wars are now settled at game start (`md2026_legacy_wars_settled` in
`common/on_actions/md2026_on_actions.txt`): Chechnya, Aceh, Tamil Eelam, the Taliban
state, the Eritrea/South Sudan wars and the defunct rebel movements (AFR, LUR, MLC,
RCD, NPM, UNI) are resolved to their real 2026 state. The Somali civil war is left
running because it is still ongoing in reality.

### Known limitations

- **Ukraine `create_unit` focuses**: MD's own rewards in `05_ukraine.txt` use a division
  string the 1.19 parser rejects (`create_unit -- division string was not parsed
  correctly`). The units are not created; the focuses are still pre-completed for their
  other effects. This is an MD-side bug.
- **OOB equipment tiers**: the equipment names in `history/units/*` are valid MD 2.0
  names and 5th-generation air wings (F-35, F-22, Su-57, J-20) were upgraded to
  year-appropriate airframes with `tools/fix_oob_tiers.py`. Lower tiers were left as they
  were (the tier digits still follow MD 1.x), so an F-16 wing may field a 1995 airframe.
- **Bulgaria**: at 2026-01-01 the country was run by Rosen Zhelyazkov's caretaker
  government (the regular cabinet resigned in December 2025).
- **Bookmark picture** still uses MD's 2000 selection picture (`GFX_select_date_2000`).
- **IND (Indonesia) and VEN (Venezuela)** now have 2026 history patches but no 2026
  order of battle; they use MD's 2000 OOB with 2026 tech levels.

### Army orders of battle require No Step Back

`history/units/<TAG>_2026_nsb.txt` exists only in the NSB variant. Without No Step Back the
2026 bookmark uses MD's 2000 OOB for that country (the tech levels are still 2026). Generating
non-NSB variants is on the to-do list.

### MD-side issues (not caused by this submod)

`tools/validate.py` reports one warning that lives inside Millennium Dawn's own content:

- `has_government = ARM` in MD's `05_france.txt` (`ai_will_do` block) - invalid trigger.

Millennium Dawn 2.0 additionally contains a few hundred of its own stale references
(e.g. `Cat_missile`, `early_APC`, `UKR_dmytro_kiva`); where they appear in files this submod
overrides, the generator repairs them automatically.

### Cosmetics

- Leaders without a Millennium Dawn portrait use one of MD's generic politician portraits
  (`gfx/leaders/generic_politicians/`); the generator marks those lines with a `MD2026:` comment.
  Using a non-existent portrait file would crash the game at bookmark start.
- Some event pictures fall back to a generic sprite when MD has no exact match.
- The 2026 bookmark uses MD's `GFX_select_date_2000` date picture.

## Troubleshooting

### The mod does not appear in the launcher

Run `pwsh -File tools/install_mod.ps1` - it creates the junction and the `md-2026.mod`
descriptor. Then restart the launcher.

### The 2026 bookmark does not appear

Make sure both Millennium Dawn and this submod are enabled in the same playset, with MD loading
first (the `dependencies` field handles that). Check `logs/error.log` for `md2026` entries.

### Regenerating after a Millennium Dawn update

```bash
python tools/rebase.py generate
python tools/validate.py
```

Fix any errors reported by the validator (usually a rename in `patches/mappings/*.csv` or in
`patches/history_countries/*`).
