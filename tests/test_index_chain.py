"""Tests for the three-layer index chain: vanilla → MD → submod."""
import pytest
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"


def test_vanilla_layer_indexed():
    from hoi4_mod_validator.index.builder import IndexBuilder
    from hoi4_mod_validator.index.registry import SourceLayer

    builder = IndexBuilder(
        vanilla_path=str(FIXTURES / "vanilla"),
        md_path=None,
        submod_path=None,
    )
    registry = builder.build()
    assert registry.exists("event", "test_vanilla.1")
    defn = registry.get("event", "test_vanilla.1")
    assert defn.layer == SourceLayer.VANILLA


def test_md_layer_overrides_vanilla():
    """If MD defines something vanilla also defines, MD should win."""
    from hoi4_mod_validator.index.builder import IndexBuilder
    from hoi4_mod_validator.index.registry import Registry, SourceLayer

    registry = Registry()
    # Register vanilla first
    registry.register("event", "shared.1", SourceLayer.VANILLA, "vanilla/events.txt", 1)
    # Register MD second — should override
    registry.register("event", "shared.1", SourceLayer.MILLENNIUM_DAWN, "md/events.txt", 1)

    defn = registry.get("event", "shared.1")
    assert defn.layer == SourceLayer.MILLENNIUM_DAWN


def test_submod_overrides_md():
    """Submod definitions override MD definitions."""
    from hoi4_mod_validator.index.registry import Registry, SourceLayer

    registry = Registry()
    registry.register("idea", "shared_idea", SourceLayer.MILLENNIUM_DAWN, "md/ideas.txt", 1)
    registry.register("idea", "shared_idea", SourceLayer.SUBMOD, "submod/ideas.txt", 1)

    defn = registry.get("idea", "shared_idea")
    assert defn.layer == SourceLayer.SUBMOD


def test_full_chain():
    """Full three-layer chain — submod reference is valid because MD defines it."""
    from hoi4_mod_validator.index.builder import IndexBuilder
    from hoi4_mod_validator.validators.references import ReferenceValidator

    builder = IndexBuilder(
        vanilla_path=str(FIXTURES / "vanilla"),
        md_path=str(FIXTURES / "millennium_dawn"),
        submod_path=str(FIXTURES / "submod"),
    )
    registry = builder.build()

    # md_test_idea is defined in MD layer
    assert registry.exists("idea", "md_test_idea")

    # Submod references md_test_idea in a trigger — this should be valid
    validator = ReferenceValidator(str(FIXTURES / "submod"), registry)
    issues = validator.validate()
    idea_errors = [i for i in issues if "md_test_idea" in i.message and i.code == "REF003"]
    assert len(idea_errors) == 0, \
        f"md_test_idea (from MD layer) falsely flagged as unknown: {idea_errors}"


def test_opinion_modifier_chain():
    """Opinion modifiers from MD are reachable via the registry."""
    from hoi4_mod_validator.index.builder import IndexBuilder

    builder = IndexBuilder(
        vanilla_path=str(FIXTURES / "vanilla"),
        md_path=str(FIXTURES / "millennium_dawn"),
        submod_path=str(FIXTURES / "submod"),
    )
    registry = builder.build()
    assert registry.exists("opinion_modifier", "improve_relation"), \
        "improve_relation (MD layer) should be in registry"


def test_registry_summary():
    from hoi4_mod_validator.index.builder import IndexBuilder

    builder = IndexBuilder(
        vanilla_path=str(FIXTURES / "vanilla"),
        md_path=str(FIXTURES / "millennium_dawn"),
        submod_path=str(FIXTURES / "submod"),
    )
    registry = builder.build()
    summary = registry.summary()
    assert isinstance(summary, dict)
    assert all(isinstance(v, int) for v in summary.values())
    # At least events and ideas should be present
    assert "event" in summary
