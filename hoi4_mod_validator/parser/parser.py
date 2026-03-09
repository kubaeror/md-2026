"""Parser: builds an AST from a list of tokens (Paradox Script)."""
from __future__ import annotations
from typing import Optional, Union
from .lexer import Lexer, Token, TokenType
from .ast_nodes import (
    ASTNode, Assignment, Block, Document, Literal, ListLiteral,
    SourceLocation, Statement,
)


class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(f"{message} at {token.line}:{token.column} (got {token.type.name} {token.value!r})")
        self.token = token


class Parser:
    """Recursive-descent parser for Paradox Script."""

    def __init__(self, tokens: list[Token], file_path: str = "<unknown>"):
        self._tokens = tokens
        self._pos = 0
        self._file = file_path

    # ------------------------------------------------------------------ helpers
    def _peek(self) -> Token:
        return self._tokens[self._pos]

    def _advance(self) -> Token:
        tok = self._tokens[self._pos]
        if self._pos < len(self._tokens) - 1:
            self._pos += 1
        return tok

    def _at_eof(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _loc(self, tok: Token) -> SourceLocation:
        return SourceLocation(self._file, tok.line, tok.column)

    def _expect(self, *types: TokenType) -> Token:
        tok = self._peek()
        if tok.type not in types:
            raise ParseError(f"Expected {[t.name for t in types]}", tok)
        return self._advance()

    # ------------------------------------------------------------------ public
    def parse(self) -> Document:
        doc = Document(loc=self._loc(self._peek()), file_path=self._file)
        while not self._at_eof():
            child = self._parse_statement()
            if child is not None:
                doc.children.append(child)
        return doc

    # ------------------------------------------------------------------ grammar
    def _parse_statement(self) -> Optional[Union[Assignment, Statement]]:
        """Parse a single top-level or block-level statement."""
        tok = self._peek()

        # Empty block end or EOF
        if tok.type in (TokenType.RBRACE, TokenType.EOF):
            return None

        # Could be a standalone value (rare) or key [op value]
        if tok.type in (TokenType.IDENTIFIER, TokenType.STRING, TokenType.NUMBER, TokenType.AT):
            first = self._advance()
            next_tok = self._peek()

            # If followed by an operator → Assignment
            if next_tok.type == TokenType.OPERATOR:
                op_tok = self._advance()
                value = self._parse_value()
                return Assignment(
                    key=self._token_to_str(first),
                    operator=op_tok.value,
                    value=value,
                    loc=self._loc(first),
                )
            else:
                # Standalone value (e.g., bare identifier inside a list block)
                lit = self._make_literal(first)
                return Statement(value=lit, loc=self._loc(first))

        # Opening brace without key — shouldn't normally happen at top level
        if tok.type == TokenType.LBRACE:
            block = self._parse_block()
            return Statement(value=block, loc=self._loc(tok))

        # Skip unexpected tokens
        self._advance()
        return None

    def _parse_value(self) -> Union[Literal, Block, ListLiteral]:
        tok = self._peek()

        if tok.type == TokenType.LBRACE:
            return self._parse_block_or_list()

        if tok.type in (TokenType.IDENTIFIER, TokenType.STRING, TokenType.NUMBER, TokenType.AT):
            return self._make_literal(self._advance())

        # Fallback: treat whatever is there as a literal
        return self._make_literal(self._advance())

    def _parse_block_or_list(self) -> Union[Block, ListLiteral]:
        """
        Decide between a Block (contains assignments) and a ListLiteral
        (contains only bare values).  We peek ahead: if the second token
        is an operator we have assignments, otherwise a list.
        """
        lbrace = self._expect(TokenType.LBRACE)
        loc = self._loc(lbrace)

        # Empty block
        if self._peek().type == TokenType.RBRACE:
            self._advance()
            return Block(statements=[], loc=loc)

        # Peek to decide: list vs block
        # A "list" block: all children are bare values (no operators follow)
        # We look at the first two tokens
        is_list = self._looks_like_list()

        if is_list:
            items: list[Literal] = []
            while self._peek().type not in (TokenType.RBRACE, TokenType.EOF):
                tok = self._peek()
                if tok.type in (TokenType.IDENTIFIER, TokenType.STRING,
                                TokenType.NUMBER, TokenType.AT):
                    items.append(self._make_literal(self._advance()))
                else:
                    break
            self._expect(TokenType.RBRACE)
            return ListLiteral(items=items, loc=loc)
        else:
            return self._parse_block_body(loc)

    def _looks_like_list(self) -> bool:
        """
        Fast heuristic: peek at the first two tokens inside the block.
        If the second token (after first value) is an operator → block.
        If first token is a { → block.
        Otherwise → list.
        """
        pos = self._pos
        # first token
        if pos >= len(self._tokens):
            return True
        t0 = self._tokens[pos]
        if t0.type in (TokenType.RBRACE, TokenType.EOF):
            return True  # empty
        if t0.type == TokenType.LBRACE:
            return False  # nested block immediately → not a flat list
        # second token
        pos += 1
        if pos >= len(self._tokens):
            return True
        t1 = self._tokens[pos]
        if t1.type == TokenType.OPERATOR:
            return False  # key = value pattern → block
        return True

    def _parse_block_body(self, loc: SourceLocation) -> Block:
        stmts: list[Union[Assignment, Statement]] = []
        while self._peek().type not in (TokenType.RBRACE, TokenType.EOF):
            stmt = self._parse_statement()
            if stmt is not None:
                stmts.append(stmt)
        self._expect(TokenType.RBRACE)
        return Block(statements=stmts, loc=loc)

    def _parse_block(self) -> Block:
        lbrace = self._expect(TokenType.LBRACE)
        return self._parse_block_body(self._loc(lbrace))

    # ------------------------------------------------------------------ utils
    @staticmethod
    def _token_to_str(tok: Token) -> str:
        if tok.type == TokenType.STRING:
            # strip surrounding quotes
            return tok.value[1:-1] if len(tok.value) >= 2 else tok.value
        return tok.value

    def _make_literal(self, tok: Token) -> Literal:
        raw = tok.value
        if tok.type == TokenType.STRING:
            return Literal(value=raw[1:-1] if len(raw) >= 2 else raw, raw=raw, loc=self._loc(tok))
        if tok.type == TokenType.NUMBER:
            try:
                val: Union[int, float] = int(raw)
            except ValueError:
                try:
                    val = float(raw)
                except ValueError:
                    val = raw  # date strings like 2026.1.1
            return Literal(value=val, raw=raw, loc=self._loc(tok))
        if raw in ("yes", "no"):
            return Literal(value=(raw == "yes"), raw=raw, loc=self._loc(tok))
        return Literal(value=raw, raw=raw, loc=self._loc(tok))


def parse_file(file_path: str) -> tuple[Document, list[str]]:
    """
    Parse a Paradox Script file.
    Returns (document, errors).  Errors are non-fatal parse warnings.
    """
    errors: list[str] = []
    try:
        with open(file_path, encoding="utf-8-sig") as fh:
            source = fh.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, encoding="latin-1") as fh:
                source = fh.read()
        except Exception as exc:
            errors.append(f"Cannot read {file_path}: {exc}")
            return Document(file_path=file_path), errors

    lexer = Lexer(source, file_path)
    tokens = lexer.tokenize()
    parser = Parser(tokens, file_path)
    try:
        doc = parser.parse()
    except Exception as exc:
        errors.append(f"Parse error in {file_path}: {exc}")
        doc = Document(file_path=file_path)
    return doc, errors


def walk_assignments(node: Union[Document, Block, Assignment, Statement, ListLiteral],
                     key_filter: Optional[str] = None):
    """
    Generator yielding all Assignment nodes in the AST subtree.
    If key_filter is given, only yields assignments whose key matches.
    """
    if isinstance(node, Document):
        for child in node.children:
            yield from walk_assignments(child, key_filter)
    elif isinstance(node, Block):
        for stmt in node.statements:
            yield from walk_assignments(stmt, key_filter)
    elif isinstance(node, Assignment):
        if key_filter is None or node.key == key_filter:
            yield node
        if isinstance(node.value, (Block, ListLiteral)):
            yield from walk_assignments(node.value, key_filter)
    elif isinstance(node, Statement):
        if isinstance(node.value, (Block, ListLiteral)):
            yield from walk_assignments(node.value, key_filter)
    elif isinstance(node, ListLiteral):
        pass  # no nested assignments inside a list
