"""Known HoI4 triggers with their required scope."""
from __future__ import annotations
from dataclasses import dataclass
from .scopes import ScopeType
from .types import ValueType


@dataclass
class TriggerSpec:
    name: str
    scopes: set[ScopeType]
    value_type: ValueType = ValueType.ANY
    is_block: bool = False
    md_only: bool = False


COUNTRY_TRIGGERS: list[TriggerSpec] = [
    TriggerSpec("tag", {ScopeType.COUNTRY}, ValueType.TAG),
    TriggerSpec("original_tag", {ScopeType.COUNTRY}, ValueType.TAG),
    TriggerSpec("has_government", {ScopeType.COUNTRY}, ValueType.IDEOLOGY),
    TriggerSpec("has_idea", {ScopeType.COUNTRY}, ValueType.IDEA_ID),
    TriggerSpec("has_country_flag", {ScopeType.COUNTRY}, ValueType.STRING),
    TriggerSpec("has_global_flag", {ScopeType.COUNTRY, ScopeType.GLOBAL}, ValueType.STRING),
    TriggerSpec("has_war", {ScopeType.COUNTRY}, ValueType.BOOL),
    TriggerSpec("is_major", {ScopeType.COUNTRY}, ValueType.BOOL),
    TriggerSpec("is_faction_leader", {ScopeType.COUNTRY}, ValueType.BOOL),
    TriggerSpec("is_in_faction", {ScopeType.COUNTRY}, ValueType.BOOL),
    TriggerSpec("is_puppet", {ScopeType.COUNTRY}, ValueType.BOOL),
    TriggerSpec("exists", {ScopeType.COUNTRY}, ValueType.BOOL),
    TriggerSpec("date", {ScopeType.ANY}, ValueType.DATE),
    TriggerSpec("stability", {ScopeType.COUNTRY}, ValueType.FLOAT),
    TriggerSpec("war_support", {ScopeType.COUNTRY}, ValueType.FLOAT),
    TriggerSpec("political_power_balance", {ScopeType.COUNTRY}, ValueType.FLOAT),
    TriggerSpec("political_power_daily", {ScopeType.COUNTRY}, ValueType.FLOAT),
    TriggerSpec("num_of_factories", {ScopeType.COUNTRY}, ValueType.INTEGER),
    TriggerSpec("num_of_military_factories", {ScopeType.COUNTRY}, ValueType.INTEGER),
    TriggerSpec("num_of_civilian_factories", {ScopeType.COUNTRY}, ValueType.INTEGER),
    TriggerSpec("has_tech", {ScopeType.COUNTRY}, ValueType.TECHNOLOGY),
    TriggerSpec("has_opinion", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    TriggerSpec("NOT", {ScopeType.ANY}, ValueType.ANY, is_block=True),
    TriggerSpec("AND", {ScopeType.ANY}, ValueType.ANY, is_block=True),
    TriggerSpec("OR", {ScopeType.ANY}, ValueType.ANY, is_block=True),
    TriggerSpec("NAND", {ScopeType.ANY}, ValueType.ANY, is_block=True),
    TriggerSpec("NOR", {ScopeType.ANY}, ValueType.ANY, is_block=True),
    TriggerSpec("if", {ScopeType.ANY}, ValueType.ANY, is_block=True),
    TriggerSpec("custom_trigger_tooltip", {ScopeType.ANY}, ValueType.ANY, is_block=True),
    TriggerSpec("focus_progress", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    TriggerSpec("has_completed_focus", {ScopeType.COUNTRY}, ValueType.FOCUS_ID),
    # Millennium Dawn specific
    TriggerSpec("check_variable", {ScopeType.ANY}, ValueType.ANY, is_block=True, md_only=True),
    TriggerSpec("has_country_leader", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    TriggerSpec("is_democratic_ideology", {ScopeType.COUNTRY}, ValueType.BOOL, md_only=True),
    TriggerSpec("is_authoritarian_ideology", {ScopeType.COUNTRY}, ValueType.BOOL, md_only=True),
]

STATE_TRIGGERS: list[TriggerSpec] = [
    TriggerSpec("is_owned_by", {ScopeType.STATE}, ValueType.TAG),
    TriggerSpec("is_controlled_by", {ScopeType.STATE}, ValueType.TAG),
    TriggerSpec("is_core_of", {ScopeType.STATE}, ValueType.TAG),
    TriggerSpec("has_state_flag", {ScopeType.STATE}, ValueType.STRING),
    TriggerSpec("state_population", {ScopeType.STATE}, ValueType.INTEGER),
]

ALL_TRIGGERS: dict[str, TriggerSpec] = {}
for _t in COUNTRY_TRIGGERS + STATE_TRIGGERS:
    ALL_TRIGGERS[_t.name] = _t

# Structural triggers (always valid)
STRUCTURAL_TRIGGERS = {"NOT", "AND", "OR", "NAND", "NOR", "if", "limit",
                        "custom_trigger_tooltip"}
