"""
Syntax validator — Layer 1.
Checks basic Paradox Script structural correctness.
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Union

from ..parser.ast_nodes import (
    Assignment, Block, Document, Literal, ListLiteral, Statement,
)
from ..parser.parser import parse_file
from ..reporting.models import Issue, Severity

# Issue codes
_SYN001 = "SYN001"  # Parse error (file could not be parsed)
_SYN002 = "SYN002"  # Empty top-level file
_SYN003 = "SYN003"  # Suspicious key (likely typo or invalid)
_SYN004 = "SYN004"  # Date format mismatch
_SYN005 = "SYN005"  # Unexpected operator for context
_SYN006 = "SYN006"  # Empty block where value expected
_SYN007 = "SYN007"  # File encoding issue (BOM OK, other bad)
_SYN008 = "SYN008"  # Duplicate key in same block

_DATE_RE = re.compile(r"^\d{4}\.\d{1,2}\.\d{1,2}$")
_VALID_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_\-\.]*$")

# Known "date" fields — value should match date format
_DATE_FIELDS = {"date", "start_date", "end_date", "fire_date"}

# Fields that must be "yes" or "no"
_BOOL_FIELDS = {"fire_only_once", "is_triggered_only", "major", "hidden",
                 "show_effect_tooltip", "fire_only_once", "always"}


class SyntaxValidator:
    def __init__(self, submod_path: str):
        self.submod_path = Path(submod_path)

    def validate(self) -> list[Issue]:
        issues: list[Issue] = []
        for txt_file in self.submod_path.rglob("*.txt"):
            doc, parse_errors = parse_file(str(txt_file))
            for err in parse_errors:
                issues.append(Issue(
                    severity=Severity.ERROR,
                    file=str(txt_file),
                    line=1,
                    code=_SYN001,
                    message=err,
                ))
            if not parse_errors:
                issues.extend(self._validate_document(doc, str(txt_file)))
        return issues

    def _validate_document(self, doc: Document, file_path: str) -> list[Issue]:
        issues: list[Issue] = []
        if not doc.children:
            # Some files are legitimately empty (on_actions etc.)
            # Only warn if the file has a known content-bearing path
            fp_lower = file_path.lower()
            if any(p in fp_lower for p in ("events", "national_focus", "decisions")):
                issues.append(Issue(
                    severity=Severity.WARNING,
                    file=file_path,
                    line=1,
                    code=_SYN002,
                    message="File appears empty or has no parseable content",
                ))
        for child in doc.children:
            issues.extend(self._check_node(child, file_path, depth=0))
        return issues

    def _check_node(self, node, file_path: str, depth: int) -> list[Issue]:
        issues: list[Issue] = []
        if isinstance(node, Assignment):
            issues.extend(self._check_assignment(node, file_path, depth))
        elif isinstance(node, Statement):
            pass  # standalone values are generally OK
        return issues

    def _check_assignment(self, assign: Assignment, file_path: str, depth: int) -> list[Issue]:
        issues: list[Issue] = []
        line = assign.loc.line if assign.loc else 0

        # Check key validity
        key = assign.key
        if key and not _VALID_KEY_RE.match(key):
            issues.append(Issue(
                severity=Severity.WARNING,
                file=file_path,
                line=line,
                code=_SYN003,
                message=f"Suspicious key name: {key!r}",
            ))

        # Check date fields
        if key in _DATE_FIELDS and isinstance(assign.value, Literal):
            val = str(assign.value.value)
            if not _DATE_RE.match(val):
                issues.append(Issue(
                    severity=Severity.WARNING,
                    file=file_path,
                    line=line,
                    code=_SYN004,
                    message=f"Field '{key}' looks like a date field but '{val}' is not a valid date (expected YYYY.MM.DD)",
                ))

        # Check bool fields
        if key in _BOOL_FIELDS and isinstance(assign.value, Literal):
            val = str(assign.value.value)
            if val not in ("yes", "no", "True", "False", "1", "0"):
                issues.append(Issue(
                    severity=Severity.WARNING,
                    file=file_path,
                    line=line,
                    code=_SYN005,
                    message=f"Field '{key}' should be 'yes' or 'no', got: {val!r}",
                ))

        # Recurse into blocks
        if isinstance(assign.value, Block):
            issues.extend(self._check_block(assign.value, file_path, depth + 1))

        return issues

    def _check_block(self, block: Block, file_path: str, depth: int) -> list[Issue]:
        issues: list[Issue] = []
        seen_keys: dict[str, int] = {}

        for stmt in block.statements:
            if isinstance(stmt, Assignment):
                # Track duplicates for non-list-like keys
                key = stmt.key
                if key not in ("option", "prerequisite", "mutually_exclusive",
                                "ai_will_do", "modifier", "add_namespace",
                                "every_country", "any_country", "if", "else_if",
                                "hidden_effect", "trigger"):
                    if key in seen_keys:
                        line = stmt.loc.line if stmt.loc else 0
                        issues.append(Issue(
                            severity=Severity.HINT,
                            file=file_path,
                            line=line,
                            code=_SYN008,
                            message=f"Key '{key}' appears multiple times in this block (first at line {seen_keys[key]}). This may override the earlier value.",
                        ))
                    else:
                        seen_keys[key] = stmt.loc.line if stmt.loc else 0

                issues.extend(self._check_node(stmt, file_path, depth))

        return issues
