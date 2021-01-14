#!/usr/bin/env python3
import contextlib

from pathlib import Path
from functools import reduce
from typing import List
from AoC.util import show

import numpy as np

CWD = Path(__file__).parent

PROPERTIES = ["capacity", "durability", "flavor", "texture"]


class Ingredient:
    def __init__(self, raw: str):
        self.name, props = raw.split(": ", maxsplit=1)
        self.props = {}
        for i in props.split(", "):
            n, v = i.split(" ", maxsplit=1)
            self.props[n] = v


def read_input(filename: str="input.txt") -> List[Ingredient]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = []
        for l in reader.readlines():
            res.append(Ingredient(l))
        return res


def get_score(ings: List[Ingredient]):
    matrix = np.zeros((len(ings), len(PROPERTIES)))
    for k, ing in enumerate(ings):
        for l, prop in enumerate(PROPERTIES):
            matrix[k,l] = ing.props[prop]
    def score(*arg):
        m = np.copy(matrix)
        for i in range(len(ings)):
            m[i] *= arg[i]
        totals = m.sum(axis=0)
        totals[totals<0] = 0
        return reduce(lambda x, y:x*y, totals)
    return score


def get_calories(ings: List[Ingredient]):
    vector = np.zeros(len(ings))
    for k, ing in enumerate(ings):
        vector[k] = ing.props["calories"]
    def score(*arg):
        return np.dot(vector, arg)
    return score


def candidates(n: int, total: int=100):
    if n == 1:
        yield [total]
        return
    for i in range(0, total+1):
        left = total - i
        for y in candidates(n-1, left):
            yield [i] + y


@show
def first(ings: List[Ingredient]) -> int:
    score = get_score(ings)
    cs = candidates(len(ings))
    return max([score(*c) for c in cs])


@show
def second(ings: List[Ingredient]) -> int:
    score = get_score(ings)
    cs = candidates(len(ings))
    calories = get_calories(ings)
    cs = [c for c in cs if calories(*c) == 500]
    return max([score(*c) for c in cs])


def test_example() -> None:
    ings = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        score = get_score(ings)
        assert score(44, 56) == 62842880
        cals = get_calories(ings)
        assert cals(40, 60) == 500
        assert first(ings) == 62842880
        assert second(ings) == 57600000


# test_example()
ings = read_input()
first(ings) # 21367368
second(ings) # 1766400