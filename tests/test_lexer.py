"""Tests for the Paradox Script lexer."""
import pytest
from hoi4_mod_validator.parser.lexer import Lexer, TokenType


def lex(source: str, **kwargs):
    return Lexer(source, "<test>").tokenize(**kwargs)


def test_simple_assignment():
    tokens = lex("tag = GER")
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert types == [TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.IDENTIFIER]


def test_number():
    tokens = lex("cost = 10")
    values = [t.value for t in tokens if t.type != TokenType.EOF]
    assert values == ["cost", "=", "10"]


def test_float():
    tokens = lex("stability = 0.05")
    num_tok = [t for t in tokens if t.type == TokenType.NUMBER]
    assert num_tok[0].value == "0.05"


def test_date():
    tokens = lex("date > 2026.6.1")
    num_tok = [t for t in tokens if t.type == TokenType.NUMBER]
    assert num_tok[0].value == "2026.6.1"


def test_quoted_string():
    tokens = lex('name = "Hello World"')
    str_tok = [t for t in tokens if t.type == TokenType.STRING]
    assert str_tok[0].value == '"Hello World"'


def test_comment_skipped():
    tokens = lex("# this is a comment\ntag = GER", skip_comments=True, skip_newlines=True)
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert types == [TokenType.IDENTIFIER, TokenType.OPERATOR, TokenType.IDENTIFIER]


def test_block():
    tokens = lex("block = { key = val }")
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert TokenType.LBRACE in types
    assert TokenType.RBRACE in types


def test_operators():
    for op in ["=", "<", ">", "<=", ">=", "!="]:
        tokens = lex(f"x {op} 1")
        op_tok = [t for t in tokens if t.type == TokenType.OPERATOR]
        assert op_tok[0].value == op


def test_yes_no():
    tokens = lex("is_major = yes")
    id_tokens = [t for t in tokens if t.type == TokenType.IDENTIFIER]
    assert any(t.value == "yes" for t in id_tokens)


def test_line_numbers():
    tokens = lex("a = 1\nb = 2", skip_newlines=False)
    b_tok = next(t for t in tokens if t.value == "b")
    assert b_tok.line == 2


def test_negative_number():
    tokens = lex("x = -5")
    num_tok = [t for t in tokens if t.type == TokenType.NUMBER]
    assert num_tok[0].value == "-5"


def test_multiline_block():
    src = """
focus = {
    id = my_focus
    cost = 10
    x = 0
    y = 0
}
"""
    tokens = lex(src)
    ids = [t.value for t in tokens if t.type == TokenType.IDENTIFIER]
    assert "focus" in ids
    assert "my_focus" in ids
