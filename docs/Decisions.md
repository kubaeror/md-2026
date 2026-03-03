# Decisions

The mod adds 20 strategic decisions across 5 categories, providing players with meaningful choices to shape their country's direction from 2026 onward.

---

## Decision Categories

Defined in `common/decisions/categories/md2026_decision_categories.txt`:

| Category | Icon | Description |
|----------|------|-------------|
| `md2026_sanctions_decisions` | Political | Sanctions and trade restrictions |
| `md2026_nato_decisions` | Military | NATO alliance management |
| `md2026_military_decisions` | Military | Military modernization programs |
| `md2026_geopolitical_decisions` | Political | Geopolitical maneuvering |
| `md2026_economic_decisions` | Economic | Economic reforms and programs |

---

## Sanctions Decisions

| Decision | Available To | Cost | Effect |
|----------|-------------|------|--------|
| Impose sanctions | Major powers | PP + stability | Target gets factory/trade penalties |
| Lift sanctions | Any with sanctions active | PP | Removes sanction modifiers, improves relations |
| Sanctions evasion | Sanctioned countries | PP | Partially offsets sanction penalties |
| Secondary sanctions | USA | PP + stability | Penalizes third-party trade with sanctioned states |

---

## NATO Decisions

| Decision | Available To | Cost | Effect |
|----------|-------------|------|--------|
| Increase defense spending | NATO members | Consumer goods | Military factory bonuses |
| Request NATO deployment | NATO members (border states) | PP | Garrison bonuses |
| Article 5 consultation | NATO leader | PP + war support | Faction mobilization |
| NATO expansion bid | Non-NATO democracies | PP + stability | Path to membership |

---

## Military Modernization Decisions

| Decision | Available To | Cost | Effect |
|----------|-------------|------|--------|
| Arms procurement program | Any | Civilian factories | Equipment bonuses, tech boost |
| Domestic defense industry | Regional powers | Factories + PP | Long-term military production bonus |
| Cyber warfare program | Major powers | PP + research | Cyber defense/attack capability |
| Nuclear modernization | Nuclear states | Massive cost | Nuclear capability upgrades |

---

## Geopolitical Decisions

| Decision | Available To | Cost | Effect |
|----------|-------------|------|--------|
| Regional influence campaign | Major/regional powers | PP | Opinion improvement in region |
| Diplomatic normalization | Any hostile pairs | PP + stability | Relations improvement |
| Proxy support | Major powers | Equipment + PP | Support faction in third country |
| International summit | Major powers | PP | Global event chain trigger |

---

## Economic Decisions

| Decision | Available To | Cost | Effect |
|----------|-------------|------|--------|
| Economic reform package | Any | PP + stability | GDP/factory bonuses |
| Trade diversification | Sanctioned/dependent countries | PP | New trade routes |
| Infrastructure investment | Developing countries | Civilian factories | State building slots |
| Green transition | Developed countries | Factories + PP | Long-term economic bonus |

---

## Decision Reward Ideas

Completing decisions grants temporary or permanent national spirits defined in `common/ideas/md2026_decision_ideas.txt`:

| Idea | Granted By | Duration | Key Effect |
|------|-----------|----------|------------|
| `md2026_sanctions_imposed` | Impose sanctions | Permanent until lifted | Target penalties |
| `md2026_defense_spending_boost` | Increase defense spending | 365 days | +10% military factory output |
| `md2026_arms_procurement` | Arms procurement | 365 days | +10% equipment production |
| `md2026_cyber_capability` | Cyber warfare program | Permanent | Encryption/intel bonuses |
| `md2026_economic_reform` | Economic reform | 730 days | +5% factory output |
| `md2026_green_economy` | Green transition | Permanent | +10% resource efficiency |
| ... | ... | ... | ... |

*(11 reward ideas total)*

---

## Implementation Details

- All decision IDs use the `md2026_` prefix
- Decisions use `visible` and `available` blocks for proper gating
- Cost is paid via `cost = X` (political power) and `modifier` blocks
- Many decisions use `days_remove = X` for timed completion
- AI weights are configured via `ai_will_do` blocks
- Localisation is in `md2026_l_english.yml`
