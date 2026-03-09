"""AST node definitions for Paradox Script."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional, Union


@dataclass
class SourceLocation:
    file: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.column}"


# Note: we do NOT inherit loc from a base class to avoid the "non-default
# argument follows default argument" error in Python's dataclass inheritance.
# Instead, loc is an optional field on each node class with a default of None.


@dataclass
class Literal:
    """A scalar value: string, number, bool, identifier."""
    value: Union[str, int, float, bool]
    raw: str = ""
    loc: Optional[SourceLocation] = field(default=None, repr=False)

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class Block:
    """A { ... } block containing a list of statements."""
    statements: list[Union["Assignment", "Statement"]] = field(default_factory=list)
    loc: Optional[SourceLocation] = field(default=None, repr=False)


@dataclass
class ListLiteral:
    """A block used as a list of bare values: { SOV CHI USA }"""
    items: list[Literal] = field(default_factory=list)
    loc: Optional[SourceLocation] = field(default=None, repr=False)


@dataclass
class Assignment:
    """key op value  — e.g.  tag = GER  or  date > 2026.1.1"""
    key: str
    operator: str   # =, >, <, >=, <=, !=
    value: Union[Literal, Block, ListLiteral]
    loc: Optional[SourceLocation] = field(default=None, repr=False)


@dataclass
class Statement:
    """A standalone value without an operator (rare but valid in some lists)."""
    value: Union[Literal, Block]
    loc: Optional[SourceLocation] = field(default=None, repr=False)


@dataclass
class Document:
    """Root node — a sequence of top-level assignments/statements."""
    children: list[Union[Assignment, Statement]] = field(default_factory=list)
    file_path: str = ""
    loc: Optional[SourceLocation] = field(default=None, repr=False)


# Type alias used in ASTNode references
ASTNode = Union[Literal, Block, ListLiteral, Assignment, Statement, Document]
