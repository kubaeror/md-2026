# Borders & Territorial Changes

The 2026 bookmark reflects several significant territorial changes that occurred between 2000 and 2026. These are implemented via `history/states/` files with `2026.1.1` date blocks inside the `history = { }` section.

---

## Territorial Changes

### 1. Crimea — Russian Annexation (2014)

| State | 2000 Owner | 2026 Owner | Cores |
|-------|------------|------------|-------|
| Crimea | UKR | SOV | SOV + UKR |

Russia annexed Crimea following a disputed referendum in March 2014. Ukraine and most of the international community do not recognize the annexation — both countries retain cores.

### 2. Donbas — Russian Occupation (2022)

| State | 2000 Owner | 2026 Owner | Cores |
|-------|------------|------------|-------|
| Donetsk Oblast | UKR | SOV | SOV + UKR |
| Luhansk Oblast | UKR | SOV | SOV + UKR |

Russia declared annexation of the Donetsk and Luhansk oblasts in September 2022. In-game, Russia controls these states but Ukraine retains cores (representing its claim and ongoing resistance).

### 3. Zaporizhzhia & Kherson — Partial Occupation (2022)

| State | 2000 Owner | 2026 Owner | Cores | Notes |
|-------|------------|------------|-------|-------|
| Zaporizhzhia Oblast | UKR | Split | SOV + UKR | Northern part under Russian control |
| Kherson Oblast | UKR | Split | SOV + UKR | Western Kherson liberated by Ukraine (Nov 2022) |

The front lines as of January 2026 are approximated using HoI4's state boundaries. Some states are assigned to Russia to reflect the occupied territory, while others remain Ukrainian.

### 4. Syria — Post-Assad (December 2024)

| State | 2000 Owner | 2026 Owner | Notes |
|-------|------------|------------|-------|
| Syrian states | SYR | SYR | HTS (Ahmad al-Sharaa) controls most of Syria |

The Assad regime fell in December 2024 when Hayat Tahrir al-Sham (HTS) forces captured Damascus. The new de facto government under Ahmad al-Sharaa controls most of the country. Kurdish-held northeast regions are represented through existing MD mechanics.

### 5. Golan Heights

| State | 2000 Owner | 2026 Owner | Cores |
|-------|------------|------------|-------|
| Golan | Disputed | ISR (de facto) | ISR + SYR |

Israel has maintained de facto control of the Golan Heights since 1967, with formal annexation in 1981. The US recognized Israeli sovereignty in 2019.

### 6. Kosovo

| State | 2000 Owner | 2026 Owner | Cores |
|-------|------------|------------|-------|
| Kosovo | SER | KOS | KOS + SER |

Kosovo declared independence in 2008, recognized by ~100 UN members. Serbia does not recognize independence — both retain cores.

### 7. South Sudan (2011)

South Sudan's independence (2011) is handled by Millennium Dawn's base mod. Our submod ensures the correct 2026 state is reflected (ongoing civil conflict represented through national spirits and events).

---

## Active Front Lines (January 2026)

### Russo-Ukrainian War

The war, ongoing since February 2022, has the following approximate front as of January 2026:

**Russian-controlled territory:**
- All of Crimea
- Most of Luhansk Oblast
- Parts of Donetsk Oblast (including Mariupol, Severodonetsk, Lysychansk)
- Northern Kherson Oblast (east of Dnipro river)
- Parts of Zaporizhzhia Oblast

**Ukrainian-controlled territory:**
- Western Kherson Oblast (liberated November 2022)
- Most of Zaporizhzhia Oblast (including Zaporizhzhia city)
- Parts of Donetsk Oblast (Pokrovsk area under pressure)
- All other Ukrainian territory

**Active combat zones:**
- Donetsk Oblast (Pokrovsk direction, Kurakhove area)
- Kursk Oblast, Russia (Ukrainian incursion since August 2024)

The war is set up via `declare_war_on` in the startup scripted effects, with appropriate unit deployments on both sides.

---

## Demographics & Population

As of the v1.1.0 update, the submod includes a **Global Population Rework**. 

The base Millennium Dawn mod uses year 2000 population data for its states. To reflect the 26 years of global growth leading up to our start date, we have applied a uniform **+30% increase** to the `manpower` variable in all **1213 states** globally (adjusting from ~6.1 billion to ~8.0 billion global population).

*   **Exceptions:** Conflict zones with significant displacement or localized data (e.g., specific Ukrainian oblasts) have been manually adjusted to reflect more accurate 2026 estimates rather than a flat multiplier.

---

## State History Implementation

State changes are implemented in `history/states/ID-Name.txt` files. Date blocks go **inside** the `history = { }` block:

```
state = {
    id = 123
    name = "STATE_NAME"
    # ...
    history = {
        owner = UKR
        # ... 2000 setup ...

        2026.1.1 = {
            owner = SOV
            add_core_of = SOV
        }
    }
}
```

**Important**: The `2026.1.1` date block must be placed inside `history = { }`, not after it. Placing it outside causes the game to ignore the changes silently.

### Modified State Files

| File | States Covered |
|------|---------------|
| `226-Crimea.txt` | Crimea |
| `227-Donetsk.txt` | Donetsk Oblast |
| `228-Luhansk.txt` | Luhansk Oblast |
| `229-Zaporizhzhia.txt` | Zaporizhzhia Oblast |
| `230-Kherson.txt` | Kherson Oblast |
| `677-Syria.txt` | Syrian territories |
| `454-Golan.txt` | Golan Heights |
| `105-Kosovo.txt` | Kosovo |
