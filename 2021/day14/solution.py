#!/usr/bin/env python3

import contextlib

from pathlib import Path
import numpy as np

from typing import *
from AoC.util import show


CWD = Path(__file__).parent

CACHE = {}


def read_input(filename: str = "input.txt") -> Tuple[str, List[Dict[str, str]]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res, rules = reader.readline().strip(), {}
        reader.readline()
        for l in reader.readlines():
            a, b = l.strip().split(" -> ")
            rules[a] = b
        return res, rules


def update_count(a: Dict[str, int], b: Dict[str, int]):
    for k, v in b.items():
        if k in a:
            a[k] += v
        else:
            a[k] = v


def run_step(inp: str, rules: List[Dict[str, str]], step: int) -> Dict[str, int]:
    if step <= 0 or inp not in rules:
        return {}
    if (inp, step) not in CACHE:
        char = rules[inp]
        res = {char: 1}
        update_count(res, run_step(inp[0]+char, rules, step-1))
        update_count(res, run_step(char+inp[1], rules, step-1))
        CACHE[(inp, step)] = res
    return CACHE[(inp, step)]


def run(inp: str, rules: List[Dict[str, str]], steps: int) -> int:
    unique, counts = np.unique(list(inp), return_counts=True)
    res = dict(zip(unique, counts))
    for i in range(len(inp)-1):
        update_count(res, run_step(inp[i:i+2], rules, steps))
    return max(res.values()) - min(res.values())


@show
def first(inp: str, rules: List[Dict[str, str]]) -> int:
    return run(inp, rules, 10)


@show
def second(inp: str, rules: List[Dict[str, str]]) -> int:
    return run(inp, rules, 40)


def test_example() -> None:
    global CACHE
    with contextlib.redirect_stdout(None):
        inp, rules = read_input("example.txt")
        assert first(inp, rules) == 1588
        assert second(inp, rules) == 2188189693529
        CACHE = {}


if __name__ == "__main__":
    test_example()
    inp, rules = read_input()
    first(inp, rules)  # 2360
    second(inp, rules)  # 2967977072188
