"""
Reference validator — Layer 2.
Checks that referenced IDs (focuses, events, ideas, etc.) exist in the
three-layer registry (vanilla → MD → submod).
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Union

from ..parser.ast_nodes import (
    Assignment, Block, Document, Literal, ListLiteral, Statement,
)
from ..parser.parser import parse_file, walk_assignments
from ..index.registry import Registry
from ..reporting.models import Issue, Severity

_REF001 = "REF001"  # Unknown focus ID
_REF002 = "REF002"  # Unknown event ID
_REF003 = "REF003"  # Unknown idea/spirit ID
_REF004 = "REF004"  # Unknown technology
_REF005 = "REF005"  # Unknown opinion modifier
_REF006 = "REF006"  # Unknown scripted trigger
_REF007 = "REF007"  # Unknown scripted effect
_REF008 = "REF008"  # Unknown GFX sprite
_REF009 = "REF009"  # Unknown country tag (only for known-bad ones)
_REF010 = "REF010"  # Unknown character ID
_REF011 = "REF011"  # Unknown decision ID

# Country tags that are always valid (major powers)
_KNOWN_TAGS: set[str] = {
    "USA", "GER", "FRA", "ENG", "SOV", "JAP", "CHI", "ITA", "RAJ", "BRA",
    "TUR", "POL", "SPA", "MEX", "ARG", "AUS", "SAF", "CAN", "HOL", "BEL",
    "NOR", "SWE", "DEN", "FIN", "HUN", "ROM", "YUG", "GRE", "IRQ", "IRN",
    "AFG", "CHN", "MAN", "PRC", "CAN", "AUS", "NZL", "SAU", "EGY", "ETH",
    "PAK", "PHI", "PER", "COL", "VEN", "CHL", "BOL", "ECU", "URU", "PAR",
    "POR", "SWI", "IRE", "ISR", "KOR", "PRK", "VIN", "TAI", "IND", "IDC",
    "NGR", "KEN", "ZIM", "MOZ", "ANG", "LIB", "ALG", "TUN", "MAR", "GHA",
    "UAR", "SYR", "JOR", "ISR", "KWT", "UAE", "BAH", "QAT", "OMA", "YEM",
    # MD-specific tags
    "RUS", "UKR", "POL", "CZE", "SVK", "HRV", "SRB", "BIH", "MNE", "ALB",
    "MKD", "SLV", "EST", "LAT", "LTU", "BLR", "GEO", "ARM", "AZE", "KAZ",
    "UZB", "TKM", "KGZ", "TJK", "MNG", "VIE", "LAO", "CAM", "MYA", "THA",
    "MAS", "SGP", "BRU", "INS", "PHI",
}

# Field-name → (registry_type, issue_code, severity)
_FIELD_CHECKS: list[tuple[str, str, str, Severity]] = [
    ("focus",          "focus",             _REF001, Severity.ERROR),
    ("id",             "event",             _REF002, Severity.WARNING),   # only in country_event blocks
    ("add_ideas",      "idea",              _REF003, Severity.ERROR),
    ("remove_ideas",   "idea",              _REF003, Severity.ERROR),
    ("swap_ideas",     "idea",              _REF003, Severity.WARNING),
    ("add_idea",       "idea",              _REF003, Severity.ERROR),
    ("activate_technology", "technology",   _REF004, Severity.WARNING),
    ("add_opinion_modifier",  None,         _REF005, Severity.WARNING),   # handled specially
    ("remove_opinion_modifier", None,       _REF005, Severity.WARNING),
    ("has_completed_focus",   "focus",      _REF001, Severity.ERROR),
    ("picture",        "gfx_sprite",        _REF008, Severity.WARNING),
    ("icon",           "gfx_sprite",        _REF008, Severity.WARNING),
]

# Context blocks that change what "id" means
_EVENT_CONTAINER_KEYS = {"country_event", "news_event", "state_event", "unit_leader_event"}


class ReferenceValidator:
    def __init__(self, submod_path: str, registry: Registry):
        self.submod_path = Path(submod_path)
        self.registry = registry

    def validate(self) -> list[Issue]:
        issues: list[Issue] = []
        for txt_file in self.submod_path.rglob("*.txt"):
            doc, _ = parse_file(str(txt_file))
            issues.extend(self._validate_document(doc, str(txt_file)))
        return issues

    def _validate_document(self, doc: Document, file_path: str) -> list[Issue]:
        issues: list[Issue] = []
        for child in doc.children:
            issues.extend(self._check_node(child, file_path, context_stack=[]))
        return issues

    def _check_node(self, node, file_path: str, context_stack: list[str]) -> list[Issue]:
        issues: list[Issue] = []
        if isinstance(node, Assignment):
            issues.extend(self._check_assignment(node, file_path, context_stack))
        elif isinstance(node, Statement):
            if isinstance(node.value, Block):
                issues.extend(self._check_block(node.value, file_path, context_stack))
        return issues

    def _check_assignment(self, assign: Assignment, file_path: str, context_stack: list[str]) -> list[Issue]:
        issues: list[Issue] = []
        line = assign.loc.line if assign.loc else 0
        key = assign.key

        # Focus references
        if key in ("prerequisite", "mutually_exclusive") and isinstance(assign.value, Block):
            issues.extend(self._check_block_focus_refs(assign.value, file_path))

        # Script trigger reference
        if key == "has_scripted_trigger" and isinstance(assign.value, Literal):
            ref = str(assign.value.value)
            if not self.registry.exists("scripted_trigger", ref):
                issues.append(self._make_issue(_REF006, Severity.ERROR, file_path, line,
                                                f"Unknown scripted trigger: '{ref}'"))

        # Script effect reference
        if key == "use_scripted_effect" and isinstance(assign.value, Literal):
            ref = str(assign.value.value)
            if not self.registry.exists("scripted_effect", ref):
                issues.append(self._make_issue(_REF007, Severity.ERROR, file_path, line,
                                                f"Unknown scripted effect: '{ref}'"))

        # Idea references
        if key in ("add_ideas", "remove_ideas", "add_idea") and isinstance(assign.value, Literal):
            ref = str(assign.value.value)
            if not self.registry.exists("idea", ref):
                issues.append(self._make_issue(_REF003, Severity.ERROR, file_path, line,
                                                f"Unknown idea/national spirit: '{ref}'"))

        # has_completed_focus
        if key == "has_completed_focus" and isinstance(assign.value, Literal):
            ref = str(assign.value.value)
            if not self.registry.exists("focus", ref):
                issues.append(self._make_issue(_REF001, Severity.ERROR, file_path, line,
                                                f"Unknown focus ID in has_completed_focus: '{ref}'"))

        # Event references (inside country_event = { id = ... })
        new_context = context_stack + [key]
        if key in _EVENT_CONTAINER_KEYS and isinstance(assign.value, Block):
            issues.extend(self._check_event_ref_block(assign.value, file_path, line))

        # Opinion modifier references
        if key in ("add_opinion_modifier", "remove_opinion_modifier", "reverse_add_opinion_modifier"):
            if isinstance(assign.value, Block):
                for stmt in assign.value.statements:
                    if isinstance(stmt, Assignment) and stmt.key == "modifier":
                        ref = str(stmt.value.value) if isinstance(stmt.value, Literal) else ""
                        if ref and not self.registry.exists("opinion_modifier", ref):
                            stmt_line = stmt.loc.line if stmt.loc else line
                            issues.append(self._make_issue(_REF005, Severity.WARNING, file_path, stmt_line,
                                                            f"Unknown opinion modifier: '{ref}'"))

        # GFX references
        if key in ("picture", "icon") and isinstance(assign.value, Literal):
            ref = str(assign.value.value)
            if ref.startswith("GFX_") and not self.registry.exists("gfx_sprite", ref):
                issues.append(self._make_issue(_REF008, Severity.WARNING, file_path, line,
                                                f"Unknown GFX sprite: '{ref}'"))

        # Recurse
        if isinstance(assign.value, Block):
            issues.extend(self._check_block(assign.value, file_path, new_context))

        return issues

    def _check_event_ref_block(self, block: Block, file_path: str, parent_line: int) -> list[Issue]:
        """Check that event ID referenced in country_event/news_event block exists."""
        issues: list[Issue] = []
        for stmt in block.statements:
            if isinstance(stmt, Assignment) and stmt.key == "id" and isinstance(stmt.value, Literal):
                ref = str(stmt.value.value)
                if not self.registry.exists("event", ref):
                    line = stmt.loc.line if stmt.loc else parent_line
                    issues.append(self._make_issue(_REF002, Severity.ERROR, file_path, line,
                                                    f"Referenced event does not exist: '{ref}'"))
        return issues

    def _check_block_focus_refs(self, block: Block, file_path: str) -> list[Issue]:
        """Check focus references inside prerequisite/mutually_exclusive blocks."""
        issues: list[Issue] = []
        for stmt in block.statements:
            if isinstance(stmt, Assignment) and stmt.key == "focus" and isinstance(stmt.value, Literal):
                ref = str(stmt.value.value)
                if not self.registry.exists("focus", ref):
                    line = stmt.loc.line if stmt.loc else 0
                    issues.append(self._make_issue(_REF001, Severity.ERROR, file_path, line,
                                                    f"Unknown focus ID in prerequisite: '{ref}'"))
        return issues

    def _check_block(self, block: Block, file_path: str, context_stack: list[str]) -> list[Issue]:
        issues: list[Issue] = []
        for stmt in block.statements:
            issues.extend(self._check_node(stmt, file_path, context_stack))
        return issues

    @staticmethod
    def _make_issue(code: str, severity: Severity, file_path: str, line: int, message: str) -> Issue:
        return Issue(severity=severity, file=file_path, line=line, code=code, message=message)
