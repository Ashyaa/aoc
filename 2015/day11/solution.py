#!/usr/bin/env python3
import contextlib
import re

from pathlib import Path
from AoC.util import show


CWD = Path(__file__).parent


ALPHABET = "abcdefghijklmnopqrstuvwxyz"
POSITIONS = {char: i for i, char in enumerate(ALPHABET)}
FORBIDDEN_CHARACTERS = set("ilo")
PAIR = re.compile(r"([a-z])\1")


def cond_1(p: str) -> bool:
    for i, c in enumerate(p[:-2]):
      if POSITIONS[c] == POSITIONS[p[i+1]]-1 == POSITIONS[p[i+2]]-2:
        return True
    return False


def cond_2(p: str) -> bool:
    return len(FORBIDDEN_CHARACTERS.intersection(set(p))) == 0


def cond_3(p: str) -> bool:
    return len(PAIR.findall(p)) >= 2


def is_valid(p: str) -> bool:
    return cond_1(p) and cond_2(p) and cond_3(p)


def increment(p: str, pos: int=0) -> str:
    index = (-1-pos)%len(p)
    cur = POSITIONS[p[index]]
    p = p[:index] + ALPHABET[(cur+1) % 26] + p[index+1:]
    if cur >= 25:
      p = increment(p, pos+1)
    return p


@show
def next_pass(p: str) -> str:
    while True:
        p = increment(p)
        if is_valid(p):
          break
    return p


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert not is_valid("hijklmmn")
        assert not is_valid("abbceffg")
        assert not is_valid("abbcegjk")
        assert is_valid("abcdffaa")
        assert is_valid("ghjaabcc")
        assert increment("abcdefgh") == "abcdefgi"
        assert increment("abcdezzz") == "abcdfaaa"
        assert next_pass("abcdefgh") == "abcdffaa"
        assert next_pass("ghijklmn") == "ghjaabcc"


test_example()
p2 = next_pass("hepxcrrq") # hepxxyzz
next_pass(p2) # heqaabcc