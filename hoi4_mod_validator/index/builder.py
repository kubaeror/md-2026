"""
Index builder: scans the three-layer chain (vanilla → MD → submod)
and populates the Registry with known definitions.
"""
from __future__ import annotations
import logging
import os
from pathlib import Path
from typing import Optional

from .registry import Registry, SourceLayer
from ..parser.parser import parse_file, walk_assignments
from ..parser.ast_nodes import Assignment, Document, Literal, ListLiteral, Block

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Mapping: directory/file pattern → (definition_type, key_field)
# key_field is the field inside the block that holds the ID.
# None means the top-level key IS the ID.
# ---------------------------------------------------------------------------
_EXTRACTORS: list[tuple[str, str, Optional[str]]] = [
    # (glob-like path fragment, definition_type, id_field_or_None)
    ("common/national_focus",      "focus",              "id"),
    ("common/ideas",               "idea",               None),   # key is id
    ("common/technologies",        "technology",         None),
    ("common/scripted_triggers",   "scripted_trigger",   None),
    ("common/scripted_effects",    "scripted_effect",    None),
    ("common/opinion_modifiers",   "opinion_modifier",   None),
    ("common/decisions",           "decision",           "id"),
    ("common/characters",          "character",          None),
    ("common/ai_strategy_plans",   "ai_strategy_plan",   "id"),
    ("common/on_actions",          "on_action",          None),
    ("events",                     "event",              "id"),
    ("common/bookmarks",           "bookmark",           "name"),
    ("common/countries",           "country",            None),   # tag files
]

# For events: top-level keys like "country_event", "news_event", etc.
_EVENT_KEYS = {"country_event", "news_event", "state_event", "unit_leader_event"}

# namespace tracking
_NAMESPACE_KEYS = {"add_namespace", "namespace"}


def _find_txt_files(base_dir: Path) -> list[Path]:
    """Recursively find all .txt files under base_dir."""
    results = []
    if not base_dir.exists():
        return results
    for root, _dirs, files in os.walk(base_dir):
        for fname in files:
            if fname.endswith(".txt"):
                results.append(Path(root) / fname)
    return results


def _find_yml_files(base_dir: Path) -> list[Path]:
    results = []
    if not base_dir.exists():
        return results
    for root, _dirs, files in os.walk(base_dir):
        for fname in files:
            if fname.endswith(".yml") or fname.endswith(".yaml"):
                results.append(Path(root) / fname)
    return results


def _extract_value_str(node) -> Optional[str]:
    """Get a string value from a Literal node."""
    if isinstance(node, Literal):
        return str(node.value)
    return None


def _index_file(
    doc: Document,
    def_type: str,
    id_field: Optional[str],
    layer: SourceLayer,
    registry: Registry,
    file_path: str,
) -> None:
    """
    Extract definitions from a parsed document.
    Handles two patterns:
      1. id_field=None: each top-level key IS the definition ID
         e.g.  my_idea = { ... }
      2. id_field="id": inside each top-level block, look for  id = <value>
         e.g.  focus = { id = my_focus ... }
    """
    for stmt in doc.children:
        if not isinstance(stmt, Assignment):
            continue

        # Pattern 2: id_field is specified
        if id_field is not None:
            if isinstance(stmt.value, Block):
                for inner in stmt.value.statements:
                    if isinstance(inner, Assignment) and inner.key == id_field:
                        val = _extract_value_str(inner.value)
                        if val:
                            line = (inner.loc.line if inner.loc else 0)
                            registry.register(def_type, val, layer, file_path, line)
        else:
            # Pattern 1: key is the ID
            key = stmt.key
            if key in ("ideas",):
                # ideas = { country = { idea_name = { ... } } }
                # Two levels of wrapping: top key → category → idea id
                if isinstance(stmt.value, Block):
                    for cat in stmt.value.statements:
                        if isinstance(cat, Assignment) and isinstance(cat.value, Block):
                            for inner in cat.value.statements:
                                if isinstance(inner, Assignment):
                                    line = (inner.loc.line if inner.loc else 0)
                                    registry.register(def_type, inner.key, layer, file_path, line)
            elif key in ("technologies", "opinion_modifiers", "characters",
                          "on_actions", "scripted_triggers", "scripted_effects",
                          "decisions", "ai_strategy_plans"):
                # These have a single wrapper block — recurse one level
                if isinstance(stmt.value, Block):
                    for inner in stmt.value.statements:
                        if isinstance(inner, Assignment):
                            inner_key = inner.key
                            if isinstance(inner.value, Block):
                                line = (inner.loc.line if inner.loc else 0)
                                registry.register(def_type, inner_key, layer, file_path, line)
            else:
                # Direct top-level definition
                line = stmt.loc.line if stmt.loc else 0
                registry.register(def_type, key, layer, file_path, line)


def _index_events(doc: Document, layer: SourceLayer, registry: Registry, file_path: str) -> None:
    """Extract event IDs and namespaces from event files."""
    for stmt in doc.children:
        if not isinstance(stmt, Assignment):
            continue
        if stmt.key in _EVENT_KEYS:
            if isinstance(stmt.value, Block):
                for inner in stmt.value.statements:
                    if isinstance(inner, Assignment) and inner.key == "id":
                        val = _extract_value_str(inner.value)
                        if val:
                            line = inner.loc.line if inner.loc else 0
                            registry.register("event", val, layer, file_path, line)
        elif stmt.key in _NAMESPACE_KEYS:
            val = _extract_value_str(stmt.value)
            if val:
                line = stmt.loc.line if stmt.loc else 0
                registry.register("namespace", val, layer, file_path, line)


def _index_localisation(base_dir: Path, layer: SourceLayer, registry: Registry) -> None:
    """Extract localisation keys from YAML files (HoI4 format)."""
    for yml_file in _find_yml_files(base_dir / "localisation"):
        try:
            with open(yml_file, encoding="utf-8-sig") as fh:
                for line_num, line in enumerate(fh, 1):
                    line = line.strip()
                    if not line or line.startswith("#") or line.startswith("l_"):
                        continue
                    # Format:  key:N "value"  or  key: "value"
                    colon_pos = line.find(":")
                    if colon_pos > 0:
                        key = line[:colon_pos].strip()
                        if key:
                            registry.register("localisation_key", key, layer,
                                              str(yml_file), line_num)
        except Exception as exc:
            log.warning("Cannot read localisation file %s: %s", yml_file, exc)


def _index_gfx(base_dir: Path, layer: SourceLayer, registry: Registry) -> None:
    """Extract GFX sprite names from interface/*.gfx files."""
    gfx_dir = base_dir / "interface"
    if not gfx_dir.exists():
        return
    for gfx_file in gfx_dir.rglob("*.gfx"):
        doc, _ = parse_file(str(gfx_file))
        for assign in walk_assignments(doc):
            if assign.key == "name" and isinstance(assign.value, Literal):
                val = str(assign.value.value)
                line = assign.loc.line if assign.loc else 0
                registry.register("gfx_sprite", val, layer, str(gfx_file), line)


def _index_focuses(doc: Document, layer: SourceLayer, registry: Registry, file_path: str) -> None:
    """Extract focus IDs from focus tree files."""
    for stmt in doc.children:
        if not isinstance(stmt, Assignment):
            continue
        if stmt.key == "focus_tree":
            if isinstance(stmt.value, Block):
                for inner in stmt.value.statements:
                    if isinstance(inner, Assignment) and inner.key == "focus":
                        if isinstance(inner.value, Block):
                            for f_inner in inner.value.statements:
                                if isinstance(f_inner, Assignment) and f_inner.key == "id":
                                    val = _extract_value_str(f_inner.value)
                                    if val:
                                        line = f_inner.loc.line if f_inner.loc else 0
                                        registry.register("focus", val, layer, file_path, line)
        elif stmt.key == "shared_focus":
            if isinstance(stmt.value, Block):
                for inner in stmt.value.statements:
                    if isinstance(inner, Assignment) and inner.key == "id":
                        val = _extract_value_str(inner.value)
                        if val:
                            line = inner.loc.line if inner.loc else 0
                            registry.register("focus", val, layer, file_path, line)


def _index_characters(doc: Document, layer: SourceLayer, registry: Registry, file_path: str) -> None:
    """Extract character IDs."""
    for stmt in doc.children:
        if not isinstance(stmt, Assignment):
            continue
        if stmt.key == "characters":
            if isinstance(stmt.value, Block):
                for inner in stmt.value.statements:
                    if isinstance(inner, Assignment):
                        line = inner.loc.line if inner.loc else 0
                        registry.register("character", inner.key, layer, file_path, line)


class IndexBuilder:
    """Builds a Registry by scanning the vanilla→MD→submod chain."""

    def __init__(
        self,
        vanilla_path: Optional[str] = None,
        md_path: Optional[str] = None,
        submod_path: Optional[str] = None,
        cache_dir: Optional[str] = None,
    ):
        self.vanilla_path = Path(vanilla_path) if vanilla_path else None
        self.md_path = Path(md_path) if md_path else None
        self.submod_path = Path(submod_path) if submod_path else None
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.registry = Registry()

    def build(self) -> Registry:
        """Build the full registry from all available layers."""
        if self.vanilla_path:
            log.info("Indexing vanilla HoI4: %s", self.vanilla_path)
            self._index_layer(self.vanilla_path, SourceLayer.VANILLA)

        if self.md_path:
            log.info("Indexing Millennium Dawn: %s", self.md_path)
            self._index_layer(self.md_path, SourceLayer.MILLENNIUM_DAWN)

        if self.submod_path:
            log.info("Indexing submod: %s", self.submod_path)
            self._index_layer(self.submod_path, SourceLayer.SUBMOD)

        log.info("Registry summary: %s", self.registry.summary())
        return self.registry

    def _index_layer(self, base_dir: Path, layer: SourceLayer) -> None:
        """Index a single layer directory."""
        self._index_txt_files(base_dir, layer)
        _index_localisation(base_dir, layer, self.registry)
        _index_gfx(base_dir, layer, self.registry)

    def _index_txt_files(self, base_dir: Path, layer: SourceLayer) -> None:
        for txt_file in _find_txt_files(base_dir):
            rel = txt_file.relative_to(base_dir)
            rel_str = str(rel).replace("\\", "/")
            file_str = str(txt_file)

            doc, errors = parse_file(file_str)
            if errors:
                for err in errors:
                    log.debug("Parse warning: %s", err)

            # Route to appropriate indexer based on path
            if "national_focus" in rel_str:
                _index_focuses(doc, layer, self.registry, file_str)
            elif "events" in rel_str:
                _index_events(doc, layer, self.registry, file_str)
            elif "characters" in rel_str:
                _index_characters(doc, layer, self.registry, file_str)
            else:
                for path_frag, def_type, id_field in _EXTRACTORS:
                    if path_frag in rel_str:
                        _index_file(doc, def_type, id_field, layer, self.registry, file_str)
                        break
