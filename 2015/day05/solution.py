#!/usr/bin/env python3

import contextlib
import re

from pathlib import Path
from typing import List
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> List[str]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return reader.readlines()


VOWELS = set("aeiou")
UNWANTED = ["ab", "cd", "pq", "xy"]
DUP_REGEX = re.compile(r"(([a-z])\2+)")


def is_nice_p1(s: str) -> bool:
    if sum([c in VOWELS for c in s]) < 3:
        return False
    if DUP_REGEX.search(s) is None:
        return False
    for uw in UNWANTED:
        if uw in s:
            return False
    return True


@show
def first(strs: List[str]) -> int:
    return sum([is_nice_p1(s) for s in strs])


DUP_PAIR_REGEX = re.compile(r"([a-z]{2}).*\1")
LETTER_REGEX = re.compile(r"([a-z]).\1")


def is_nice_p2(s: str) -> bool:
    if DUP_PAIR_REGEX.search(s) is None:
        return False
    if LETTER_REGEX.search(s) is None:
        return False
    return True

@show
def second(strs: List[str]) -> int:
    return sum([is_nice_p2(s) for s in strs])


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert is_nice_p1("ugknbfddgicrmopn")
        assert is_nice_p1("aaa")
        assert not is_nice_p1("jchzalrnumimnmhp")
        assert not is_nice_p1("haegwjzuvuyypxyu")
        assert not is_nice_p1("dvszwmarrgswjxmb")
        assert is_nice_p2("qjhvhtzxzqqjkmpb")
        assert is_nice_p2("xxyxx")
        assert not is_nice_p2("uurcxstgmygtbstg")
        assert not is_nice_p2("ieodomkazucvgmuy")


test_example()
strs = read_input()
first(strs) # 258
second(strs) # 53