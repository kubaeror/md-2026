"""Known HoI4 effects with their required scope and expected value types."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .scopes import ScopeType
from .types import ValueType


@dataclass
class EffectSpec:
    name: str
    scopes: set[ScopeType]          # which scopes this effect is valid in
    value_type: ValueType = ValueType.ANY
    is_block: bool = False          # True if the value is a block { }
    deprecated: bool = False
    md_only: bool = False           # Millennium Dawn specific


# ---------------------------------------------------------------------------
# Country-scope effects
# ---------------------------------------------------------------------------
COUNTRY_EFFECTS: list[EffectSpec] = [
    EffectSpec("add_political_power", {ScopeType.COUNTRY}, ValueType.INTEGER),
    EffectSpec("add_stability", {ScopeType.COUNTRY}, ValueType.FLOAT),
    EffectSpec("add_war_support", {ScopeType.COUNTRY}, ValueType.FLOAT),
    EffectSpec("add_ideas", {ScopeType.COUNTRY}, ValueType.IDEA_ID),
    EffectSpec("remove_ideas", {ScopeType.COUNTRY}, ValueType.IDEA_ID),
    EffectSpec("set_politics", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("set_popularities", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("set_party_name", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("add_timed_idea", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("activate_technology", {ScopeType.COUNTRY}, ValueType.TECHNOLOGY),
    EffectSpec("set_technology", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("add_equipment_to_stockpile", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("add_opinion_modifier", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("reverse_add_opinion_modifier", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("remove_opinion_modifier", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("add_relation_modifier", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("add_relations", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("set_country_flag", {ScopeType.COUNTRY}, ValueType.STRING),
    EffectSpec("clr_country_flag", {ScopeType.COUNTRY}, ValueType.STRING),
    EffectSpec("set_global_flag", {ScopeType.COUNTRY, ScopeType.GLOBAL}, ValueType.STRING),
    EffectSpec("clr_global_flag", {ScopeType.COUNTRY, ScopeType.GLOBAL}, ValueType.STRING),
    EffectSpec("country_event", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("news_event", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("random_country", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("every_country", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True),
    EffectSpec("hidden_effect", {ScopeType.COUNTRY, ScopeType.STATE, ScopeType.ANY},
               ValueType.ANY, is_block=True),
    EffectSpec("if", {ScopeType.ANY}, ValueType.ANY, is_block=True),
    EffectSpec("else_if", {ScopeType.ANY}, ValueType.ANY, is_block=True),
    EffectSpec("else", {ScopeType.ANY}, ValueType.ANY, is_block=True),
    EffectSpec("random_list", {ScopeType.ANY}, ValueType.ANY, is_block=True),
    EffectSpec("log", {ScopeType.ANY}, ValueType.STRING),
    EffectSpec("custom_effect_tooltip", {ScopeType.ANY}, ValueType.LOCALISATION_KEY),
    # Millennium Dawn
    EffectSpec("add_ruling_party_ideology_change", {ScopeType.COUNTRY}, ValueType.FLOAT, md_only=True),
    EffectSpec("add_party_popularity", {ScopeType.COUNTRY}, ValueType.ANY, is_block=True, md_only=True),
    EffectSpec("set_temp_variable", {ScopeType.ANY}, ValueType.ANY, is_block=True, md_only=True),
    EffectSpec("add_to_variable", {ScopeType.ANY}, ValueType.ANY, is_block=True, md_only=True),
    EffectSpec("set_variable", {ScopeType.ANY}, ValueType.ANY, is_block=True, md_only=True),
    EffectSpec("round_variable", {ScopeType.ANY}, ValueType.STRING, md_only=True),
    EffectSpec("clamp_variable", {ScopeType.ANY}, ValueType.ANY, is_block=True, md_only=True),
    EffectSpec("multiply_variable", {ScopeType.ANY}, ValueType.ANY, is_block=True, md_only=True),
]

# ---------------------------------------------------------------------------
# State-scope effects
# ---------------------------------------------------------------------------
STATE_EFFECTS: list[EffectSpec] = [
    EffectSpec("add_manpower", {ScopeType.STATE}, ValueType.INTEGER),
    EffectSpec("add_resource", {ScopeType.STATE}, ValueType.ANY, is_block=True),
    EffectSpec("set_state_flag", {ScopeType.STATE}, ValueType.STRING),
    EffectSpec("clr_state_flag", {ScopeType.STATE}, ValueType.STRING),
    EffectSpec("add_building_construction", {ScopeType.STATE}, ValueType.ANY, is_block=True),
    EffectSpec("set_demilitarized_zone", {ScopeType.STATE}, ValueType.BOOL),
]

ALL_EFFECTS: dict[str, EffectSpec] = {}
for _e in COUNTRY_EFFECTS + STATE_EFFECTS:
    ALL_EFFECTS[_e.name] = _e

# Effects that are always valid regardless of scope (structural)
STRUCTURAL_EFFECTS = {"if", "else_if", "else", "random_list", "hidden_effect", "log",
                      "custom_effect_tooltip", "limit"}
