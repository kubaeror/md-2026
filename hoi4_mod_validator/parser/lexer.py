"""Tokenizer for Paradox Script (HoI4 / Millennium Dawn scripting language)."""
from __future__ import annotations
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator


class TokenType(Enum):
    IDENTIFIER = auto()    # unquoted word, tag, etc.
    STRING = auto()        # "quoted string"
    NUMBER = auto()        # integer or float (including dates like 2026.1.1)
    OPERATOR = auto()      # = < > <= >= !=
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    AT = auto()            # @ (used in modifiers)
    COMMENT = auto()       # # ... to end of line  (usually skipped)
    NEWLINE = auto()       # \n
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"{message} at line {line}, column {column}")
        self.line = line
        self.column = column


# Combined scanner regex — groups are named to identify the token type.
# Order matters: longer multi-char operators before single-char ones.
_SCANNER = re.compile(
    r'(?P<WHITESPACE>[ \t\r]+)'
    r'|(?P<COMMENT>#[^\n]*)'
    r'|(?P<STRING>"(?:[^"\\]|\\.)*")'
    r'|(?P<NUMBER>-?(?:\d+\.\d+(?:\.\d+)*|\d+))'
    r'|(?P<OPERATOR><=|>=|!=|[=<>])'
    r'|(?P<LBRACE>\{)'
    r'|(?P<RBRACE>\})'
    r'|(?P<AT>@)'
    r'|(?P<NEWLINE>\n)'
    r'|(?P<IDENTIFIER>[A-Za-z_\-][A-Za-z0-9_\-\.]*)'
    r'|(?P<UNKNOWN>.)',   # catch-all
)

# Map group name → TokenType
_GROUP_TO_TYPE: dict[str, TokenType] = {
    "COMMENT":    TokenType.COMMENT,
    "STRING":     TokenType.STRING,
    "NUMBER":     TokenType.NUMBER,
    "OPERATOR":   TokenType.OPERATOR,
    "LBRACE":     TokenType.LBRACE,
    "RBRACE":     TokenType.RBRACE,
    "AT":         TokenType.AT,
    "NEWLINE":    TokenType.NEWLINE,
    "IDENTIFIER": TokenType.IDENTIFIER,
    "UNKNOWN":    TokenType.IDENTIFIER,  # treat unknown chars as identifiers
}


class Lexer:
    """Tokenize a Paradox Script source string."""

    def __init__(self, source: str, file_path: str = "<unknown>"):
        self.source = source
        self.file_path = file_path
        self._pos = 0
        self._line = 1
        self._col = 1

    def tokenize(self, skip_comments: bool = True, skip_newlines: bool = True) -> list[Token]:
        tokens: list[Token] = []
        for tok in self._generate():
            if skip_comments and tok.type == TokenType.COMMENT:
                continue
            if skip_newlines and tok.type == TokenType.NEWLINE:
                continue
            tokens.append(tok)
        tokens.append(Token(TokenType.EOF, "", self._line, self._col))
        return tokens

    def _generate(self) -> Iterator[Token]:
        src = self.source
        line = 1
        col = 1

        for m in _SCANNER.finditer(src):
            group = m.lastgroup
            text = m.group()

            if group == "WHITESPACE":
                col += len(text)
                continue

            tok_type = _GROUP_TO_TYPE[group]
            yield Token(tok_type, text, line, col)

            if group == "NEWLINE":
                line += 1
                col = 1
            else:
                col += len(text)

        self._line = line
        self._col = col
