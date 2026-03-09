"""Tests for the Paradox Script parser."""
import pytest
from hoi4_mod_validator.parser.lexer import Lexer
from hoi4_mod_validator.parser.parser import Parser, parse_file
from hoi4_mod_validator.parser.ast_nodes import (
    Assignment, Block, Document, Literal, ListLiteral, Statement,
)


def parse(source: str) -> Document:
    tokens = Lexer(source, "<test>").tokenize()
    return Parser(tokens, "<test>").parse()


def test_simple_assignment():
    doc = parse("tag = GER")
    assert len(doc.children) == 1
    child = doc.children[0]
    assert isinstance(child, Assignment)
    assert child.key == "tag"
    assert child.operator == "="
    assert isinstance(child.value, Literal)
    assert child.value.value == "GER"


def test_block_assignment():
    doc = parse("focus = { id = my_focus cost = 10 }")
    assert len(doc.children) == 1
    assign = doc.children[0]
    assert isinstance(assign, Assignment)
    assert isinstance(assign.value, Block)


def test_nested_blocks():
    src = """
focus_tree = {
    focus = {
        id = f1
        cost = 10
    }
}
"""
    doc = parse(src)
    tree = doc.children[0]
    assert tree.key == "focus_tree"
    assert isinstance(tree.value, Block)


def test_list_literal():
    doc = parse("tags = { USA GER FRA }")
    assign = doc.children[0]
    assert isinstance(assign.value, ListLiteral)
    vals = [item.value for item in assign.value.items]
    assert "USA" in vals
    assert "GER" in vals


def test_operators():
    doc = parse("date > 2026.1.1")
    assign = doc.children[0]
    assert assign.operator == ">"


def test_quoted_string_stripped():
    doc = parse('name = "My Event"')
    assign = doc.children[0]
    assert assign.value.value == "My Event"


def test_bool_literals():
    doc = parse("fire_only_once = yes")
    assign = doc.children[0]
    assert assign.value.value is True

    doc2 = parse("hidden = no")
    assign2 = doc2.children[0]
    assert assign2.value.value is False


def test_multiple_assignments():
    src = "a = 1\nb = 2\nc = 3"
    doc = parse(src)
    assert len(doc.children) == 3
    assert doc.children[0].key == "a"
    assert doc.children[2].key == "c"


def test_walk_assignments():
    from hoi4_mod_validator.parser.parser import walk_assignments
    src = """
country_event = {
    id = test.1
    option = {
        add_political_power = 100
    }
}
"""
    doc = parse(src)
    all_assigns = list(walk_assignments(doc))
    keys = [a.key for a in all_assigns]
    assert "id" in keys
    assert "add_political_power" in keys


def test_empty_block():
    doc = parse("ideas = {}")
    assign = doc.children[0]
    assert isinstance(assign.value, Block)
    assert len(assign.value.statements) == 0


def test_location_tracking():
    doc = parse("tag = GER")
    assign = doc.children[0]
    assert assign.loc is not None
    assert assign.loc.line == 1
