"""Integration tests for validators using fixture files."""
import os
import pytest
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"
SUBMOD_FIXTURE = FIXTURES / "submod"
MD_FIXTURE = FIXTURES / "millennium_dawn"
VANILLA_FIXTURE = FIXTURES / "vanilla"


def build_registry():
    from hoi4_mod_validator.index.builder import IndexBuilder
    builder = IndexBuilder(
        vanilla_path=str(VANILLA_FIXTURE),
        md_path=str(MD_FIXTURE),
        submod_path=str(SUBMOD_FIXTURE),
    )
    return builder.build()


def test_registry_contains_md_ideas():
    registry = build_registry()
    assert registry.exists("idea", "md_test_idea"), \
        "MD idea 'md_test_idea' should be in registry"


def test_registry_contains_md_events():
    registry = build_registry()
    assert registry.exists("event", "md_test.1")


def test_registry_contains_submod_events():
    registry = build_registry()
    assert registry.exists("event", "submod_test.1")
    assert registry.exists("event", "submod_test.2")


def test_registry_contains_submod_focuses():
    registry = build_registry()
    assert registry.exists("focus", "submod_focus_one")
    assert registry.exists("focus", "submod_focus_two")


def test_registry_contains_opinion_modifiers():
    registry = build_registry()
    assert registry.exists("opinion_modifier", "improve_relation")


def test_registry_layer_priority():
    """Submod definitions should override MD definitions."""
    from hoi4_mod_validator.index.registry import SourceLayer
    registry = build_registry()
    defn = registry.get("event", "submod_test.1")
    assert defn is not None
    assert defn.layer == SourceLayer.SUBMOD


def test_syntax_validator_no_errors():
    from hoi4_mod_validator.validators.syntax import SyntaxValidator
    validator = SyntaxValidator(str(SUBMOD_FIXTURE))
    issues = validator.validate()
    errors = [i for i in issues if i.severity.value == "error"]
    assert len(errors) == 0, f"Unexpected syntax errors: {errors}"


def test_reference_validator_valid_events():
    registry = build_registry()
    from hoi4_mod_validator.validators.references import ReferenceValidator
    validator = ReferenceValidator(str(SUBMOD_FIXTURE), registry)
    issues = validator.validate()
    # submod_test.2 is referenced and should exist → no REF002 error for it
    ref_errors = [i for i in issues if i.code == "REF002"]
    # There should be no reference errors for valid internal event refs
    assert all("submod_test.2" not in i.message for i in ref_errors), \
        f"Valid event reference flagged as error: {ref_errors}"


def test_logic_validator_focus_tree():
    from hoi4_mod_validator.validators.logic import LogicValidator
    validator = LogicValidator(str(SUBMOD_FIXTURE))
    issues = validator.validate()
    # Our test focus has all required fields — should be no LOG003 errors for it
    log_errors = [i for i in issues if i.code == "LOG003"
                  and "submod_focus_one" in str(i)]
    assert len(log_errors) == 0


def test_localization_validator():
    registry = build_registry()
    from hoi4_mod_validator.validators.localization import LocalizationValidator
    validator = LocalizationValidator(str(SUBMOD_FIXTURE), registry)
    issues = validator.validate()
    # All keys in our fixture events should be localized
    loc_errors = [i for i in issues if i.code == "LOC001"
                  and "submod_test" in i.message]
    assert len(loc_errors) == 0, f"Unexpected missing localization: {loc_errors}"


def test_reporting_json():
    from hoi4_mod_validator.reporting.models import ValidationReport, Issue, Severity
    from hoi4_mod_validator.reporting.formatter_json import format_json
    import json

    report = ValidationReport(submod_path="/test", files_scanned=5)
    report.issues = [
        Issue(severity=Severity.ERROR, file="test.txt", line=10,
              code="REF001", message="Missing focus"),
        Issue(severity=Severity.WARNING, file="test.txt", line=20,
              code="LOC001", message="Missing localization key"),
    ]

    json_str = format_json(report)
    data = json.loads(json_str)

    assert data["summary"]["error_count"] == 1
    assert data["summary"]["warning_count"] == 1
    assert data["summary"]["passed"] is False
    assert len(data["issues"]) == 2


def test_reporting_markdown():
    from hoi4_mod_validator.reporting.models import ValidationReport, Issue, Severity
    from hoi4_mod_validator.reporting.formatter_markdown import format_markdown

    report = ValidationReport(submod_path="/test", files_scanned=3)
    report.issues = [
        Issue(severity=Severity.ERROR, file="a.txt", line=1,
              code="SYN001", message="Parse error"),
    ]

    md = format_markdown(report)
    assert "FAILED" in md
    assert "SYN001" in md
    assert "Parse error" in md


def test_reporting_html():
    from hoi4_mod_validator.reporting.models import ValidationReport
    from hoi4_mod_validator.reporting.formatter_html import format_html

    report = ValidationReport(submod_path="/test", files_scanned=2)
    html = format_html(report)
    assert "<!DOCTYPE html>" in html
    assert "HoI4 Mod Validator" in html
