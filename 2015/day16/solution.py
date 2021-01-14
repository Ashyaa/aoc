#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List
from AoC.util import show


CWD = Path(__file__).parent

WANTED = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}
RANGE_GTR = set(["cats", "trees"])
RANGE_LWR = set(["pomeranians", "goldfish"])
NOT_EQUAL = RANGE_LWR.union(RANGE_GTR)

class Sue:
    def __init__(self, raw):
        props = raw.split(", ")
        self.items = {}
        for p in props:
            key, value = p.split(": ")
            self.items[key] = int(value)


    def is_wanted(self) -> bool:
        for k, v in self.items.items():
            if v == WANTED[k]:
                continue
            return False
        return True


    def is_wanted_2(self) -> bool:
        for k, v in self.items.items():
            if k in RANGE_GTR and v > WANTED[k]:
                continue
            if k in RANGE_LWR and v < WANTED[k]:
                continue
            if k not in NOT_EQUAL and v == WANTED[k]:
                continue
            return False
        return True


def read_input(filename: str="input.txt") -> List[Sue]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = [None] * 500
        for i, l in enumerate(reader.readlines()):
            res[i] = Sue(l.split(": ", maxsplit=1)[1])
        return res


@show
def first(sues: List[Sue]) -> int:
    for i, s in enumerate(sues):
        if s.is_wanted():
            return i+1


@show
def second(sues: List[Sue]) -> int:
    for i, s in enumerate(sues):
        if s.is_wanted_2():
            return i+1


sues = read_input()
first(sues) # 103
second(sues) # 103