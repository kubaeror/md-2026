"""Data types used in Paradox Script validation."""
from __future__ import annotations
from enum import Enum


class ValueType(Enum):
    """The expected type of a value in a Paradox Script assignment."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOL = "bool"
    DATE = "date"
    TAG = "tag"              # 3-letter country tag
    PROVINCE_ID = "province_id"
    STATE_ID = "state_id"
    IDEOLOGY = "ideology"
    TECHNOLOGY = "technology"
    FOCUS_ID = "focus_id"
    EVENT_ID = "event_id"
    IDEA_ID = "idea_id"
    CHARACTER_ID = "character_id"
    DECISION_ID = "decision_id"
    OPINION_MODIFIER = "opinion_modifier"
    SCRIPTED_TRIGGER = "scripted_trigger"
    SCRIPTED_EFFECT = "scripted_effect"
    GFX_SPRITE = "gfx_sprite"
    LOCALISATION_KEY = "localisation_key"
    ANY = "any"


# Fields that reference localisation keys
LOCALISATION_FIELDS = {
    "title", "desc", "name", "text", "tooltip",
    "custom_effect_tooltip", "custom_trigger_tooltip",
    "flavor",
}

# Fields that reference GFX sprites
GFX_FIELDS = {
    "picture", "icon", "gfx",
}

# Date regex pattern
DATE_PATTERN = r"^\d{4}\.\d{1,2}\.\d{1,2}$"

# Country tag pattern
TAG_PATTERN = r"^[A-Z]{3}$"
