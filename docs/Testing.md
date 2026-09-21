# Testing

The submod cannot be validated by static analysis alone - please run through this checklist
after enabling **Millennium Dawn 2.0.0** and **Millennium Dawn 2026 Rework** in the launcher.

Before testing:

1. Delete any old `Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log`.
2. Start the game with the `-debug` launch option.
3. After the test, look at `logs/error.log` and search for `md2026`.

## Checklist

### Launcher
- [ ] "Millennium Dawn 2026 Rework" appears without an "outdated" warning.
- [ ] Both mods can be enabled in the same playset.

### Bookmark screen
- [ ] Both bookmarks are visible: `MILLENNIUM_DAWN` (2000) and `MD_2026` (2026).
- [ ] The 2026 bookmark lists the featured countries (USA, SOV, CHI, UKR, ISR, TUR, POL, JAP, ...).
- [ ] No error popup when switching between bookmarks.

### 2000 start (regression check)
- [ ] The game starts, the focus trees are MD's own (no duplicates in the tree view).
- [ ] No 2026 focus branches are visible (`allow_branch` date gate).
- [ ] USA/Russia/Poland histories look unchanged compared to MD alone.

### 2026 start
- [ ] Countries have 2026 leaders, parties and national spirits (spot-check USA, POL, UKR, CHI, RUS).
- [ ] Crimea/Donbas/Kherson/Zaporizhzhia belong to Russia, the rest of Ukraine to UKR.
- [ ] NATO members (incl. FIN, SWE, POL, BAL states) have the `NATO_member` idea.
- [ ] The 2026 focus branch is visible at the edge of the tree (USA, POL, UKR, CHI, JAP, GER, ...).
- [ ] Pre-completed focuses do not show as available again; Russia's Putin branch is open.
- [ ] Technology: a tier-1 country (USA) has modern equipment unlocked; a tier-5 country has less.
- [ ] Army: units exist with 2026 names; no "invalid division template" errors.
- [ ] Army: stockpiles are not empty (check Army -> Equipment; infantry weapons should show).
- [ ] Air wings: 4th/4.5-generation aircraft exist (F-16, Eurofighter, Su-30) instead of empty wings.
- [ ] Decisions: the `md2026_` decision categories are visible and open without errors.
- [ ] Events: `event md2026_system.1` fires and displays text (not raw keys).
- [ ] Ukraine's `Bryhada TRO` rewards create divisions (complete a TDF focus or check the pre-completed ones).
- [ ] Save and reload the 2026 game.

### 2026 start without No Step Back (in the launcher, disable the DLC)
- [ ] The game starts with the same units (the non-NSB OOB variant loads).
- [ ] No "unknown equipment" or "invalid equipment version" errors for our files.

### Localisation
- [ ] Switch the game language to Polish: bookmark descriptions, focus names and events are in Polish.
- [ ] No raw loc keys are displayed anywhere.

### Log
- [ ] `error.log` contains no `md2026` errors other than the MD-side entries documented in
      `docs/Known-Issues.md`.

Report issues at https://github.com/kubaeror/md-2026/issues with the `error.log` section and
the steps to reproduce.
