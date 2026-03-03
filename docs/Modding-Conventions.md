# Modding Conventions

Guidelines and patterns used throughout this submod. Follow these conventions when adding new content.

---

## File Naming

| Content Type | Naming Pattern | Example |
|-------------|---------------|---------|
| New scripted effects | `md2026_*.txt` | `md2026_startup_effects.txt` |
| New events | `md2026_*.txt` | `md2026_elections.txt` |
| New ideas | `md2026_*.txt` | `md2026_national_spirits.txt` |
| New decisions | `md2026_*.txt` | `md2026_decisions.txt` |
| New focus trees | `md2026_TAG_focus.txt` | `md2026_usa_focus.txt` |
| Copied MD files | Keep original name | `USA_NF.txt` |
| OOB files | `TAG_2026.txt` | `USA_2026.txt` |
| Localisation | `md2026_l_english.yml` | — |

---

## ID Naming

All custom IDs use the `md2026_` prefix (or `MD2026_` for focus trees) to avoid collisions with base MD:

```
# Ideas
md2026_western_sanctions

# Events
md2026_elections.1

# Decisions
md2026_impose_sanctions

# Focus trees
MD2026_USA_trump_agenda

# Flags
md2026_election_held

# Opinion modifiers
md2026_improved_relations
```

---

## Country History Pattern

When adding a 2026 date block to a country history file:

```
capital = STATE_ID

2000.1.1 = {
    # ... original MD content — DO NOT MODIFY ...
}

2026.1.1 = {
    # Only include what CHANGES from 2000
    
    set_politics = {
        ruling_party = ideology
        last_election = "YYYY.MM.DD"
        election_frequency = 48
        elections_allowed = yes  # or no
    }
    
    set_popularities = {
        democratic = X
        communism = X
        fascism = X
        neutrality = X
        nationalist = X
    }
    
    create_country_leader = {
        name = "Leader Name"
        desc = ""
        picture = "Portrait_TAG_Leader_Name"
        expire = "2099.1.1"
        ideology = sub_ideology
        traits = { trait1 trait2 }
    }
    
    oob = "TAG_2026"
    
    # Technology assignment (via scripted effect)
    md2026_tierX_2026_techs = yes
    
    # National spirits
    add_ideas = {
        md2026_spirit_name
        conscription_law
        economic_cycle_law
    }
    
    # Country flags
    set_country_flag = flag_name
}
```

---

## Event Pattern

```
country_event = {
    id = md2026_namespace.number
    title = md2026_namespace.number.t
    desc = md2026_namespace.number.d
    picture = GFX_report_event_picture_name
    
    fire_only_once = yes  # for one-time events
    
    trigger = {
        date > 2026.6.1
        # conditions
    }
    
    mean_time_to_happen = {
        months = X
    }
    
    option = {
        name = md2026_namespace.number.o1
        log = "[GetDateText]: [This.GetName]: md2026_namespace.number.o1 executed"
        
        # effects
        
        ai_chance = {
            base = X
        }
    }
}
```

### Event Best Practices

- Always include `log` lines for debugging
- Use `ai_chance` with weighted `base` values
- Use `fire_only_once = yes` for historical one-time events
- Use timed flags for cyclical events: `set_country_flag = { flag = name days = X value = 1 }`
- Wrap news events in `hidden_effect = { news_event = { id = ... hours = 6 } }`
- Use `is_triggered_only = yes` for news events and events triggered by other events

---

## Focus Tree Pattern (Shared Focus)

### New Branch Definition

```
shared_focus = {
    id = MD2026_TAG_focus_name
    icon = GFX_goal_icon_name
    cost = 10
    
    allow_branch = {
        original_tag = TAG
        date > 2025.12.31
    }
    
    # For root focuses (no prerequisite)
    x = X
    y = Y
    
    # For child focuses
    prerequisite = { focus = MD2026_TAG_parent_focus }
    
    completion_reward = {
        log = "[GetDateText]: [This.GetName]: Focus MD2026_TAG_focus_name completed"
        # effects
    }
}
```

### Attaching to Existing Tree

In the copied MD focus tree file, add inside the `focus_tree = { }` header:

```
focus_tree = {
    id = TAG_focus
    
    shared_focus = MD2026_TAG_root
    
    # ... existing focuses ...
}
```

---

## Localisation Pattern

File must be UTF-8 with BOM. Format:

```
l_english:
 md2026_key:0 "Text value"
 md2026_key_desc:0 "Description text with $VARIABLE$ substitution"
```

Key naming conventions:
- Event title: `md2026_namespace.number.t`
- Event description: `md2026_namespace.number.d`
- Event option: `md2026_namespace.number.oX`
- Focus name: `MD2026_TAG_focus_name`
- Focus description: `MD2026_TAG_focus_name_desc`
- Spirit name: `md2026_spirit_name`
- Spirit description: `md2026_spirit_name_desc`

---

## Opinion Modifier Pattern

```
md2026_modifier_name = {
    value = X        # positive = friendly, negative = hostile
    decay = Y        # decay per year (positive number)
}
```

Use context-specific modifiers rather than generic ones:
- `md2026_improved_relations` — for diplomatic focus effects
- `md2026_border_conflict` — for border tension events
- `md2026_diplomatic_disapproval` — for election/political shift reactions
- `md2026_tech_rivalry` — for tech/space competition
- `md2026_migration_tensions` — for migration-related friction
- `embargo` — **only** for actual trade embargoes/sanctions

---

## Debugging

### Error Log
Check `Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log` after game launch.

### Console Commands
- `tdebug` — Show state IDs, province IDs on map
- `tag TAG` — Switch to playing as a country
- `observe` — Observer mode (no country selected)
- `event md2026_namespace.number` — Fire an event manually
- `focus.autocomplete` — Instantly complete focuses
- `set_country_flag flag_name` — Set a flag manually

### Log Lines
All events and focuses include `log` commands that write to the game log, making it easy to trace execution flow.
