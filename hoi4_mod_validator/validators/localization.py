"""
Localization validator — Layer 4.
Checks that all localization keys referenced in script files exist
in the localization YAML files of the submod (or MD/vanilla).
"""
from __future__ import annotations
import re
from pathlib import Path

from ..parser.ast_nodes import Assignment, Block, Document, Literal
from ..parser.parser import parse_file
from ..index.registry import Registry
from ..reporting.models import Issue, Severity

_LOC001 = "LOC001"  # Missing localization key
_LOC002 = "LOC002"  # Localization file encoding issue
_LOC003 = "LOC003"  # Duplicate localization key in submod
_LOC004 = "LOC004"  # YML file missing l_english header

# Fields whose values are localization keys
_LOC_FIELDS = {
    "title", "desc", "name", "text", "tooltip",
    "custom_effect_tooltip", "custom_trigger_tooltip", "flavor",
}

# Known auto-generated / engine keys (don't validate these)
_LOC_PREFIXES_SKIP = {"EVTOPTION", "EVTDESC", "EVTNAME"}


def _is_loc_key(val: str) -> bool:
    """Heuristic: a value is a localization key if it looks like an identifier."""
    return bool(re.match(r'^[A-Za-z][A-Za-z0-9_\.\-]*$', val))


def _scan_yml_file(yml_path: Path) -> tuple[dict[str, int], list[str]]:
    """
    Parse a HoI4 YAML localisation file.
    Returns (key→line_number dict, list of errors).
    """
    keys: dict[str, int] = {}
    errors: list[str] = []
    has_header = False

    try:
        with open(yml_path, encoding="utf-8-sig") as fh:
            lines = fh.readlines()
    except UnicodeDecodeError:
        try:
            with open(yml_path, encoding="latin-1") as fh:
                lines = fh.readlines()
            errors.append(f"Non-UTF-8 encoding in {yml_path}")
        except Exception as exc:
            errors.append(f"Cannot read {yml_path}: {exc}")
            return keys, errors

    for line_num, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("l_"):
            has_header = True
            continue
        colon_pos = line.find(":")
        if colon_pos > 0:
            key = line[:colon_pos].strip()
            if key:
                if key in keys:
                    errors.append(f"Duplicate key '{key}' at line {line_num} (first seen at {keys[key]})")
                else:
                    keys[key] = line_num

    if not has_header:
        errors.append(f"Missing 'l_english:' header in {yml_path}")

    return keys, errors


class LocalizationValidator:
    def __init__(self, submod_path: str, registry: Registry):
        self.submod_path = Path(submod_path)
        self.registry = registry
        # Collect all localisation keys defined in the submod
        self._submod_keys: dict[str, int] = {}
        self._yml_errors: list[str] = []
        self._scanned = False

    def _ensure_scanned(self) -> None:
        if self._scanned:
            return
        loc_dir = self.submod_path / "localisation"
        if loc_dir.exists():
            for yml_file in loc_dir.rglob("*.yml"):
                keys, errors = _scan_yml_file(yml_file)
                self._submod_keys.update(keys)
                self._yml_errors.extend(errors)
        self._scanned = True

    def validate(self) -> list[Issue]:
        self._ensure_scanned()
        issues: list[Issue] = []

        # Report YML errors
        for err in self._yml_errors:
            issues.append(Issue(
                severity=Severity.WARNING,
                file=str(self.submod_path / "localisation"),
                line=0, code=_LOC002, message=err,
            ))

        # Check that referenced keys exist
        for txt_file in self.submod_path.rglob("*.txt"):
            doc, _ = parse_file(str(txt_file))
            issues.extend(self._check_doc(doc, str(txt_file)))

        return issues

    def _check_doc(self, doc: Document, file_path: str) -> list[Issue]:
        issues: list[Issue] = []
        for child in doc.children:
            if isinstance(child, Assignment):
                issues.extend(self._check_assignment(child, file_path))
        return issues

    def _check_assignment(self, assign: Assignment, file_path: str) -> list[Issue]:
        issues: list[Issue] = []
        line = assign.loc.line if assign.loc else 0

        if assign.key in _LOC_FIELDS and isinstance(assign.value, Literal):
            val = str(assign.value.value)
            if _is_loc_key(val):
                # Check in submod first, then registry (which covers MD+vanilla)
                if (val not in self._submod_keys and
                        not self.registry.exists("localisation_key", val)):
                    issues.append(Issue(
                        severity=Severity.WARNING,
                        file=file_path, line=line, code=_LOC001,
                        message=f"Localisation key not found: '{val}' (field: {assign.key})",
                    ))

        if isinstance(assign.value, Block):
            for stmt in assign.value.statements:
                if isinstance(stmt, Assignment):
                    issues.extend(self._check_assignment(stmt, file_path))

        return issues
