"""HoI4 scope definitions — adapted for Millennium Dawn context."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ScopeType(Enum):
    COUNTRY = "country"
    STATE = "state"
    CHARACTER = "character"
    UNIT_LEADER = "unit_leader"
    DIVISION = "division"
    ANY = "any"            # wildcard / unknown
    GLOBAL = "global"


@dataclass
class Scope:
    name: str
    type: ScopeType
    parent: Optional["Scope"] = None
    aliases: set[str] = field(default_factory=set)


# ---------------------------------------------------------------------------
# Scope changers: keywords that switch the active scope inside their block
# ---------------------------------------------------------------------------
COUNTRY_SCOPE_CHANGERS: set[str] = {
    "every_country", "any_country", "all_country",
    "random_country", "country_event",
    "ROOT", "PREV", "FROM", "THIS",
    "overlord", "faction_leader",
}

STATE_SCOPE_CHANGERS: set[str] = {
    "every_state", "any_state", "all_state",
    "random_state", "capital_scope",
    "owner", "controller",
}

CHARACTER_SCOPE_CHANGERS: set[str] = {
    "every_character", "any_character",
    "random_character", "recruit_character",
}

UNIT_SCOPE_CHANGERS: set[str] = {
    "every_unit_leader", "any_unit_leader", "random_unit_leader",
}

# Mapping: keyword → expected inner scope type
SCOPE_CHANGER_MAP: dict[str, ScopeType] = {}
for _kw in COUNTRY_SCOPE_CHANGERS:
    SCOPE_CHANGER_MAP[_kw] = ScopeType.COUNTRY
for _kw in STATE_SCOPE_CHANGERS:
    SCOPE_CHANGER_MAP[_kw] = ScopeType.STATE
for _kw in CHARACTER_SCOPE_CHANGERS:
    SCOPE_CHANGER_MAP[_kw] = ScopeType.CHARACTER
for _kw in UNIT_SCOPE_CHANGERS:
    SCOPE_CHANGER_MAP[_kw] = ScopeType.UNIT_LEADER

# Millennium-Dawn specific scope changers
MD_SCOPE_CHANGERS: dict[str, ScopeType] = {
    "every_neighbor_country": ScopeType.COUNTRY,
    "any_neighbor_country": ScopeType.COUNTRY,
    "random_neighbor_country": ScopeType.COUNTRY,
    "every_core_state": ScopeType.STATE,
    "any_core_state": ScopeType.STATE,
    "every_owned_state": ScopeType.STATE,
    "any_owned_state": ScopeType.STATE,
    "every_controlled_state": ScopeType.STATE,
    "any_controlled_state": ScopeType.STATE,
    "every_alliance_member": ScopeType.COUNTRY,
    "any_alliance_member": ScopeType.COUNTRY,
}
SCOPE_CHANGER_MAP.update(MD_SCOPE_CHANGERS)
