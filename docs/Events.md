# Events

The mod includes approximately 75 events organized into 11 event chains, covering major geopolitical scenarios from 2026 onward. All event files are in the `events/` directory with the `md2026_` prefix.

---

## Event Chains Overview

| File | Namespace | Events | Theme |
|------|-----------|--------|-------|
| `md2026_elections.txt` | `md2026_elections` | ~8 | Cyclical democratic elections |
| `md2026_nato_russia.txt` | `md2026_nato_russia` | ~8 | NATO-Russia tensions and incidents |
| `md2026_russia_ukraine.txt` | `md2026_russia_ukraine` | ~8 | Peace negotiations, war escalation |
| `md2026_taiwan.txt` | `md2026_taiwan` | ~10 | Cross-strait crisis scenarios |
| `md2026_middle_east.txt` | `md2026_middle_east` | ~8 | Iran nuclear, Syria, Gulf tensions |
| `md2026_brics.txt` | `md2026_brics` | ~6 | BRICS expansion, de-dollarization |
| `md2026_migration.txt` | `md2026_migration` | ~6 | Migration waves, border policy |
| `md2026_climate.txt` | `md2026_climate` | ~6 | Climate events, natural disasters |
| `md2026_tech_revolution.txt` | `md2026_tech_revolution` | ~6 | AI breakthroughs, cyber attacks |
| `md2026_space.txt` | `md2026_space` | ~5 | Space race, ASAT incidents |
| `md2026_demographics.txt` | `md2026_demographics` | ~5 | Aging crisis, urbanization, brain drain |

---

## Elections System

**File**: `md2026_elections.txt`

### Generic Elections (`md2026_elections.1`)

A cyclical election event that fires for democratic countries every ~2 years:

**Trigger conditions:**
- Date after June 2026
- Country has `democratic` government
- Not currently at war
- Flag `md2026_election_held` is not set
- Country is one of: USA, FRA, GER, ENG, JAP, KOR, BRA, CAN, AST, ITA, SPR, POL, ISR

**Options:**
| Option | Effect |
|--------|--------|
| Center-right wins | +50 PP, +5% stability |
| Center-left wins | +50 PP, +5% stability |
| Populist surge | -25 PP, -10% stability, +5% war support |
| Incumbent retains power | +25 PP, +3% stability |

**Cycling mechanism**: Each option sets a **timed flag** (`md2026_election_held`, 730 days) that auto-expires after ~2 years, allowing the event to fire again.

### Country-Specific Elections

| Event | Country | Trigger |
|-------|---------|---------|
| `md2026_elections.10` | USA | 2028 Midterm Elections |
| `md2026_elections.20` | France | 2027 Presidential Election |

---

## NATO-Russia Events

**File**: `md2026_nato_russia.txt`

Events covering the escalating tensions between NATO and Russia:

| Event | Description |
|-------|-------------|
| Baltic incident | Naval/air encounter in Baltic Sea |
| Arctic confrontation | Resource/military competition in Arctic |
| Cyber warfare | Major cyber attack on NATO infrastructure |
| Article 5 test | Incident that could trigger collective defense |
| Nuclear posturing | Nuclear threats and deterrence signaling |
| Arms race escalation | New weapons deployments |
| Hybrid warfare | Disinformation, sabotage operations |
| De-escalation summit | Diplomatic attempt to reduce tensions |

---

## Russia-Ukraine Events

**File**: `md2026_russia_ukraine.txt`

Events covering the ongoing war and potential peace scenarios:

| Event | Description |
|-------|-------------|
| Ceasefire proposal | Negotiated ceasefire attempt |
| Western aid package | New military aid delivery |
| Offensive operations | Major military operations by either side |
| Nuclear escalation risk | Escalation to nuclear threshold |
| Frozen conflict | War settles into stalemate |
| Peace conference | International peace talks |
| Reconstruction begins | Post-war rebuilding (if peace achieved) |

---

## Taiwan Crisis Events

**File**: `md2026_taiwan.txt`

Events covering the Taiwan Strait tensions:

| Event | Description |
|-------|-------------|
| Military exercises | PLA exercises near Taiwan |
| Trade restrictions | Economic pressure on Taiwan |
| US arms sales | American weapons package to Taiwan |
| Naval blockade threat | Potential Chinese blockade scenario |
| AUKUS response | Allied naval deployment |
| Diplomatic recognition | Countries changing Taiwan recognition |
| Invasion scenario | Full-scale military crisis |

All Taiwan events appropriately use the `embargo` opinion modifier (representing actual trade sanctions/restrictions).

---

## Middle East Events

**File**: `md2026_middle_east.txt`

| Event | Description |
|-------|-------------|
| Iran nuclear threshold | Nuclear program milestones |
| Syria reconstruction | Post-Assad rebuilding |
| Gulf normalization | Abraham Accords expansion |
| Oil market shock | Energy price disruptions |
| Proxy conflict | Regional proxy warfare |
| Humanitarian crisis | Refugee/aid situations |

---

## BRICS Events

**File**: `md2026_brics.txt`

| Event | Description |
|-------|-------------|
| New member joins | BRICS expansion |
| Alternative currency | De-dollarization efforts |
| Development bank | New Development Bank projects |
| Internal tensions | Contradictions within BRICS |
| Trade war | Economic competition with West |
| Summit declaration | Policy coordination |

---

## Migration Events

**File**: `md2026_migration.txt`

Events use the `md2026_migration_tensions` opinion modifier for migration-related friction.

| Event | Description |
|-------|-------------|
| Mediterranean crisis | Migration wave across Mediterranean |
| Border wall decision | Border security investment |
| Integration challenge | Social integration issues |
| Brain drain | Skilled worker emigration |
| Climate migration | Climate-driven displacement |

---

## Climate Events

**File**: `md2026_climate.txt`

| Event | Description |
|-------|-------------|
| Extreme heat wave | Record temperatures, infrastructure damage |
| Flooding disaster | Major flood events |
| Wildfire crisis | Unprecedented wildfire seasons |
| Green transition | Renewable energy milestones |
| Climate summit | International agreements |

---

## Technology Revolution Events

**File**: `md2026_tech_revolution.txt`

Events use the `md2026_tech_rivalry` opinion modifier for tech competition.

| Event | Description |
|-------|-------------|
| AI breakthrough | Major artificial intelligence advance |
| Quantum computing | Quantum supremacy milestone |
| Cyber attack | State-sponsored cyber warfare |
| Chip war | Semiconductor supply chain conflict |
| Biotech advance | Medical/genetic breakthrough |

---

## Space Events

**File**: `md2026_space.txt`

Events use the `md2026_tech_rivalry` opinion modifier for space competition.

| Event | Description |
|-------|-------------|
| Moon landing | Crewed lunar mission |
| ASAT incident | Anti-satellite weapon test |
| Space station | New orbital station |
| Satellite constellation | Mega-constellation deployment |
| Mars mission | Mars exploration milestone |

---

## Demographics Events

**File**: `md2026_demographics.txt`

| Event | Description | Affected Countries |
|-------|-------------|-------------------|
| Aging population crisis | Labor shortage, pension strain | JAP, GER, ITA, KOR |
| Youth bulge instability | High youth unemployment | EGY, SAU, PER, ETH, PAK, SUD |
| Brain drain | Skilled worker emigration | UKR, POL, ROM, BRA, RAJ, SAF |
| Urbanization pressure | Megacity infrastructure strain | RAJ, CHI, BRA, EGY, ETH |

Includes a news event (`md2026_demographics_news.1`) that broadcasts the aging crisis event globally.

---

## Event Conventions

- All events use `log = "[GetDateText]: [This.GetName]: event_id option executed"` for debugging
- Events use `ai_chance` blocks with weighted `base` values for AI behavior
- `fire_only_once = yes` is used for one-time historical events
- `mean_time_to_happen` with `months` is used for periodic/conditional events
- News events use `major = yes` and `is_triggered_only = yes`
- All event text is in `localisation/english/md2026_l_english.yml`
