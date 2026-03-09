# HoI4 Mod Validator

Static analysis and validation tool for Hearts of Iron IV submods targeting **Millennium Dawn**.

## Architecture

```
vanilla HoI4  ──┐
                ├──▶  Registry (3-layer index)  ──▶  Validators  ──▶  Reports
Millennium Dawn─┤                                    (5 layers)
                │
Your submod   ──┘
```

### Validation layers

| Layer | Validator | Codes | What it checks |
|-------|-----------|-------|----------------|
| 1 | Syntax | `SYN001-SYN008` | Parse errors, date formats, bool fields, duplicate keys |
| 2 | References | `REF001-REF011` | Focuses, events, ideas, GFX sprites, opinion modifiers |
| 3 | Logic | `LOG001-LOG010` | Scope usage, required fields, event structure |
| 4 | Localization | `LOC001-LOC004` | Missing keys, encoding, duplicate keys |
| 5 | Assets | `AST001-AST004` | GFX sprite definitions, texture files |

## Usage (GitHub Actions)

The validator is invoked automatically via `.github/workflows/validate-mod.yml`.

Configure it via `validator.yml` in the repo root:

```yaml
paths:
  submod: "."
  millennium_dawn: "millennium_dawn"   # set via env MD_PATH in CI

suppress:
  - code: REF008
    path: "*/events/*.txt"
    reason: "GFX sprites from vanilla not bundled"
```

## Local development

```bash
pip install -r requirements.txt
python -m pytest tests/ -v

# Run validator locally
python -m hoi4_mod_validator.main --config validator.yml --format json --output report.json
```

## Issue codes

### Syntax (SYN)
- `SYN001` — Parse error (file cannot be parsed)
- `SYN002` — Empty file
- `SYN003` — Suspicious key name
- `SYN004` — Invalid date format
- `SYN005` — Invalid boolean value
- `SYN006` — Empty block
- `SYN007` — Encoding issue
- `SYN008` — Duplicate key in block

### References (REF)
- `REF001` — Unknown focus ID
- `REF002` — Unknown event ID
- `REF003` — Unknown idea/national spirit
- `REF004` — Unknown technology
- `REF005` — Unknown opinion modifier
- `REF006` — Unknown scripted trigger
- `REF007` — Unknown scripted effect
- `REF008` — Unknown GFX sprite
- `REF009` — Unknown country tag
- `REF010` — Unknown character ID
- `REF011` — Unknown decision ID

### Logic (LOG)
- `LOG001` — Effect in wrong scope
- `LOG002` — Trigger in wrong scope
- `LOG003` — Missing required field
- `LOG004` — Focus missing coordinates
- `LOG005` — Event has no options
- `LOG006` — Event option missing name
- `LOG007` — Contradictory MTTH + is_triggered_only
- `LOG008` — Negative cost/days
- `LOG009` — Event missing title/desc
- `LOG010` — Focus cost missing

### Localization (LOC)
- `LOC001` — Missing localization key
- `LOC002` — File encoding issue
- `LOC003` — Duplicate key
- `LOC004` — Missing `l_english:` header

### Assets (AST)
- `AST001` — GFX sprite not defined
- `AST002` — Texture file not found
- `AST003` — GFX file references non-existent texture
- `AST004` — Sound file not found
