"""
Asset validator — Layer 5.
Checks that referenced asset files (DDS textures, GFX sprites, sound files)
exist in the mod or game directory.
"""
from __future__ import annotations
from pathlib import Path
from typing import Optional

from ..parser.ast_nodes import Assignment, Block, Document, Literal
from ..parser.parser import parse_file
from ..index.registry import Registry
from ..reporting.models import Issue, Severity

_AST001 = "AST001"  # Referenced GFX sprite not defined
_AST002 = "AST002"  # DDS/texture file not found
_AST003 = "AST003"  # GFX file references non-existent texture
_AST004 = "AST004"  # Sound file not found

_GFX_FIELDS = {"picture", "icon", "gfx", "small_icon", "charismatic_icon"}
_TEXTURE_FIELDS = {"texturefile", "texture_file", "name"}  # inside spriteType blocks


class AssetValidator:
    def __init__(self, submod_path: str, registry: Registry,
                 md_path: Optional[str] = None, vanilla_path: Optional[str] = None):
        self.submod_path = Path(submod_path)
        self.md_path = Path(md_path) if md_path else None
        self.vanilla_path = Path(vanilla_path) if vanilla_path else None
        self.registry = registry

    def _file_exists(self, relative_path: str) -> bool:
        """Check if a file exists in any layer."""
        for base in [self.submod_path, self.md_path, self.vanilla_path]:
            if base and (base / relative_path).exists():
                return True
        return False

    def validate(self) -> list[Issue]:
        issues: list[Issue] = []

        # Check GFX references in script files
        for txt_file in self.submod_path.rglob("*.txt"):
            doc, _ = parse_file(str(txt_file))
            issues.extend(self._check_gfx_refs_in_script(doc, str(txt_file)))

        # Check GFX files themselves (texture paths)
        for gfx_file in self.submod_path.rglob("*.gfx"):
            doc, _ = parse_file(str(gfx_file))
            issues.extend(self._check_gfx_file(doc, str(gfx_file)))

        return issues

    def _check_gfx_refs_in_script(self, doc: Document, file_path: str) -> list[Issue]:
        issues: list[Issue] = []
        for assign in _walk_all_assignments(doc):
            if assign.key in _GFX_FIELDS and isinstance(assign.value, Literal):
                ref = str(assign.value.value)
                if ref.startswith("GFX_"):
                    if not self.registry.exists("gfx_sprite", ref):
                        line = assign.loc.line if assign.loc else 0
                        issues.append(Issue(
                            severity=Severity.WARNING,
                            file=file_path, line=line,
                            code=_AST001,
                            message=f"GFX sprite '{ref}' not defined in any interface/*.gfx file",
                        ))
        return issues

    def _check_gfx_file(self, doc: Document, file_path: str) -> list[Issue]:
        """Check that texture files referenced in .gfx definitions exist."""
        issues: list[Issue] = []
        for assign in _walk_all_assignments(doc):
            if assign.key == "texturefile" and isinstance(assign.value, Literal):
                tex_path = str(assign.value.value).replace("\\", "/").lstrip("/")
                if not self._file_exists(tex_path):
                    line = assign.loc.line if assign.loc else 0
                    issues.append(Issue(
                        severity=Severity.WARNING,
                        file=file_path, line=line,
                        code=_AST003,
                        message=f"Texture file not found: '{tex_path}'",
                    ))
        return issues


def _walk_all_assignments(doc: Document):
    """Yield all Assignment nodes recursively."""
    from ..parser.parser import walk_assignments
    yield from walk_assignments(doc)
