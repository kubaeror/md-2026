"""Registry: stores definitions indexed by type and source layer."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SourceLayer(Enum):
    VANILLA = "vanilla"
    MILLENNIUM_DAWN = "millennium_dawn"
    SUBMOD = "submod"


@dataclass
class Definition:
    id: str
    layer: SourceLayer
    file_path: str
    line: int = 0


class Registry:
    """
    Central store of known definitions.
    Maps  (definition_type, id)  →  Definition
    Priority: SUBMOD > MILLENNIUM_DAWN > VANILLA
    """

    # Layer priority for overriding
    _PRIORITY = {
        SourceLayer.VANILLA: 0,
        SourceLayer.MILLENNIUM_DAWN: 1,
        SourceLayer.SUBMOD: 2,
    }

    def __init__(self) -> None:
        # type_name → {id → Definition}
        self._store: dict[str, dict[str, Definition]] = {}
        # track all IDs per type as a flat set (for fast lookup)
        self._id_sets: dict[str, set[str]] = {}

    def register(self, def_type: str, def_id: str, layer: SourceLayer,
                 file_path: str, line: int = 0) -> None:
        """Register a definition.  Higher-priority layers overwrite lower ones."""
        if def_type not in self._store:
            self._store[def_type] = {}
            self._id_sets[def_type] = set()

        existing = self._store[def_type].get(def_id)
        new_prio = self._PRIORITY[layer]

        if existing is None or new_prio >= self._PRIORITY[existing.layer]:
            self._store[def_type][def_id] = Definition(
                id=def_id, layer=layer, file_path=file_path, line=line
            )
            self._id_sets[def_type].add(def_id)

    def exists(self, def_type: str, def_id: str) -> bool:
        return def_id in self._id_sets.get(def_type, set())

    def get(self, def_type: str, def_id: str) -> Optional[Definition]:
        return self._store.get(def_type, {}).get(def_id)

    def all_ids(self, def_type: str) -> set[str]:
        return set(self._id_sets.get(def_type, set()))

    def all_types(self) -> set[str]:
        return set(self._store.keys())

    def summary(self) -> dict[str, int]:
        """Return a dict of type → count of definitions."""
        return {t: len(ids) for t, ids in self._id_sets.items()}

    def merge(self, other: "Registry") -> None:
        """Merge another registry into this one (other's definitions may override)."""
        for def_type, defs in other._store.items():
            for def_id, defn in defs.items():
                self.register(def_type, def_id, defn.layer, defn.file_path, defn.line)
