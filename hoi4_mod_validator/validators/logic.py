"""
Logic validator — Layer 3.
Performs static analysis: scope checking, effect/trigger context validation,
circular dependencies in focuses, etc.
"""
from __future__ import annotations
from pathlib import Path
from typing import Optional

from ..parser.ast_nodes import Assignment, Block, Document, Literal, Statement
from ..parser.parser import parse_file, walk_assignments
from ..schema.scopes import SCOPE_CHANGER_MAP, ScopeType
from ..schema.effects import ALL_EFFECTS, STRUCTURAL_EFFECTS
from ..schema.triggers import ALL_TRIGGERS, STRUCTURAL_TRIGGERS
from ..reporting.models import Issue, Severity

_LOG001 = "LOG001"  # Effect used outside valid scope
_LOG002 = "LOG002"  # Trigger used outside valid scope
_LOG003 = "LOG003"  # Missing required field in block
_LOG004 = "LOG004"  # Focus has no x/y coordinates
_LOG005 = "LOG005"  # Event has no option
_LOG006 = "LOG006"  # Event option has no name
_LOG007 = "LOG007"  # Mean-time-to-happen with fire_only_once (contradiction)
_LOG008 = "LOG008"  # Negative cost/days value
_LOG009 = "LOG009"  # Missing event title or desc
_LOG010 = "LOG010"  # Focus cost missing

# Required fields per block type
_REQUIRED_FIELDS: dict[str, list[str]] = {
    "focus":         ["id", "icon", "cost", "x", "y"],
    "country_event": ["id", "title", "option"],
    "news_event":    ["id", "title", "option"],
    "state_event":   ["id", "title", "option"],
    "decision":      ["icon", "cost", "days"],
    "character":     ["name"],
}

_EVENT_KEYS = {"country_event", "news_event", "state_event", "unit_leader_event"}
_NUMERIC_FIELDS = {"cost", "days", "manpower", "months"}


def _get_block_keys(block: Block) -> set[str]:
    return {stmt.key for stmt in block.statements if isinstance(stmt, Assignment)}


def _get_block_value(block: Block, key: str) -> Optional[str]:
    for stmt in block.statements:
        if isinstance(stmt, Assignment) and stmt.key == key:
            if isinstance(stmt.value, Literal):
                return str(stmt.value.value)
    return None


class LogicValidator:
    def __init__(self, submod_path: str):
        self.submod_path = Path(submod_path)

    def validate(self) -> list[Issue]:
        issues: list[Issue] = []
        for txt_file in self.submod_path.rglob("*.txt"):
            doc, _ = parse_file(str(txt_file))
            issues.extend(self._validate_document(doc, str(txt_file)))
        return issues

    def _validate_document(self, doc: Document, file_path: str) -> list[Issue]:
        issues: list[Issue] = []
        for child in doc.children:
            if isinstance(child, Assignment):
                issues.extend(self._check_top_level(child, file_path))
        return issues

    def _check_top_level(self, assign: Assignment, file_path: str) -> list[Issue]:
        issues: list[Issue] = []

        if assign.key == "focus_tree":
            if isinstance(assign.value, Block):
                issues.extend(self._check_focus_tree(assign.value, file_path))

        elif assign.key in ("shared_focus", "focus"):
            if isinstance(assign.value, Block):
                issues.extend(self._check_focus_block(assign.value, file_path,
                                                        assign.loc.line if assign.loc else 0))

        elif assign.key in _EVENT_KEYS:
            if isinstance(assign.value, Block):
                issues.extend(self._check_event_block(assign.value, file_path, assign.key,
                                                       assign.loc.line if assign.loc else 0))

        return issues

    def _check_focus_tree(self, block: Block, file_path: str) -> list[Issue]:
        issues: list[Issue] = []
        for stmt in block.statements:
            if isinstance(stmt, Assignment) and stmt.key == "focus":
                if isinstance(stmt.value, Block):
                    line = stmt.loc.line if stmt.loc else 0
                    issues.extend(self._check_focus_block(stmt.value, file_path, line))
        return issues

    def _check_focus_block(self, block: Block, file_path: str, line: int) -> list[Issue]:
        issues: list[Issue] = []
        keys = _get_block_keys(block)

        # Required fields
        for req in _REQUIRED_FIELDS.get("focus", []):
            if req not in keys:
                issues.append(Issue(
                    severity=Severity.WARNING,
                    file=file_path, line=line, code=_LOG003,
                    message=f"Focus block missing required field: '{req}'",
                ))

        # Negative cost
        cost_str = _get_block_value(block, "cost")
        if cost_str is not None:
            try:
                if float(cost_str) < 0:
                    issues.append(Issue(
                        severity=Severity.WARNING,
                        file=file_path, line=line, code=_LOG008,
                        message=f"Focus has negative cost: {cost_str}",
                    ))
            except ValueError:
                pass

        # Check completion_reward and ai_will_do scopes
        for stmt in block.statements:
            if isinstance(stmt, Assignment) and stmt.key in ("completion_reward", "bypass"):
                if isinstance(stmt.value, Block):
                    stmt_line = stmt.loc.line if stmt.loc else line
                    issues.extend(self._check_effect_block(
                        stmt.value, file_path, ScopeType.COUNTRY, stmt_line
                    ))
            if isinstance(stmt, Assignment) and stmt.key in ("trigger", "available"):
                if isinstance(stmt.value, Block):
                    stmt_line = stmt.loc.line if stmt.loc else line
                    issues.extend(self._check_trigger_block(
                        stmt.value, file_path, ScopeType.COUNTRY, stmt_line
                    ))

        return issues

    def _check_event_block(self, block: Block, file_path: str, event_key: str, line: int) -> list[Issue]:
        issues: list[Issue] = []
        keys = _get_block_keys(block)

        # Check title and desc exist
        if "title" not in keys:
            issues.append(Issue(
                severity=Severity.WARNING, file=file_path, line=line,
                code=_LOG009, message=f"{event_key} missing 'title' field",
            ))
        if "desc" not in keys:
            issues.append(Issue(
                severity=Severity.WARNING, file=file_path, line=line,
                code=_LOG009, message=f"{event_key} missing 'desc' field",
            ))

        # Check options exist
        option_count = sum(1 for stmt in block.statements
                           if isinstance(stmt, Assignment) and stmt.key == "option")
        if option_count == 0:
            issues.append(Issue(
                severity=Severity.WARNING, file=file_path, line=line,
                code=_LOG005, message=f"{event_key} has no options",
            ))

        # Check MTTH vs fire_only_once contradiction
        has_mtth = "mean_time_to_happen" in keys
        has_trigger_only = _get_block_value(block, "is_triggered_only") == "yes"
        fire_once = _get_block_value(block, "fire_only_once") == "yes"
        if has_mtth and fire_once and has_trigger_only:
            issues.append(Issue(
                severity=Severity.HINT, file=file_path, line=line,
                code=_LOG007,
                message="Event has both mean_time_to_happen and is_triggered_only=yes — MTTH is ignored for triggered-only events",
            ))

        # Check option names
        for stmt in block.statements:
            if isinstance(stmt, Assignment) and stmt.key == "option":
                if isinstance(stmt.value, Block):
                    opt_line = stmt.loc.line if stmt.loc else line
                    opt_keys = _get_block_keys(stmt.value)
                    if "name" not in opt_keys:
                        issues.append(Issue(
                            severity=Severity.WARNING, file=file_path, line=opt_line,
                            code=_LOG006, message="Event option missing 'name' field",
                        ))
                    # Check effects in option
                    issues.extend(self._check_effect_block(
                        stmt.value, file_path, ScopeType.COUNTRY, opt_line
                    ))

        return issues

    def _check_effect_block(self, block: Block, file_path: str,
                             scope: ScopeType, parent_line: int) -> list[Issue]:
        """Validate effects within a block for scope correctness."""
        issues: list[Issue] = []
        for stmt in block.statements:
            if not isinstance(stmt, Assignment):
                continue
            key = stmt.key
            line = stmt.loc.line if stmt.loc else parent_line

            # Scope changers — recurse with new scope
            if key in SCOPE_CHANGER_MAP:
                new_scope = SCOPE_CHANGER_MAP[key]
                if isinstance(stmt.value, Block):
                    issues.extend(self._check_effect_block(stmt.value, file_path, new_scope, line))
                continue

            if key in STRUCTURAL_EFFECTS:
                if isinstance(stmt.value, Block):
                    issues.extend(self._check_effect_block(stmt.value, file_path, scope, line))
                continue

            if key in ALL_EFFECTS:
                spec = ALL_EFFECTS[key]
                valid_scopes = spec.scopes | {ScopeType.ANY}
                if scope not in valid_scopes and ScopeType.ANY not in spec.scopes:
                    issues.append(Issue(
                        severity=Severity.WARNING, file=file_path, line=line,
                        code=_LOG001,
                        message=f"Effect '{key}' used in {scope.value} scope, valid in: {[s.value for s in spec.scopes]}",
                    ))

        return issues

    def _check_trigger_block(self, block: Block, file_path: str,
                              scope: ScopeType, parent_line: int) -> list[Issue]:
        """Validate triggers within a block for scope correctness."""
        issues: list[Issue] = []
        for stmt in block.statements:
            if not isinstance(stmt, Assignment):
                continue
            key = stmt.key
            line = stmt.loc.line if stmt.loc else parent_line

            if key in SCOPE_CHANGER_MAP:
                new_scope = SCOPE_CHANGER_MAP[key]
                if isinstance(stmt.value, Block):
                    issues.extend(self._check_trigger_block(stmt.value, file_path, new_scope, line))
                continue

            if key in STRUCTURAL_TRIGGERS:
                if isinstance(stmt.value, Block):
                    issues.extend(self._check_trigger_block(stmt.value, file_path, scope, line))
                continue

            if key in ALL_TRIGGERS:
                spec = ALL_TRIGGERS[key]
                valid_scopes = spec.scopes | {ScopeType.ANY}
                if scope not in valid_scopes and ScopeType.ANY not in spec.scopes:
                    issues.append(Issue(
                        severity=Severity.WARNING, file=file_path, line=line,
                        code=_LOG002,
                        message=f"Trigger '{key}' used in {scope.value} scope, valid in: {[s.value for s in spec.scopes]}",
                    ))

        return issues
