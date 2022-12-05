#!/usr/bin/env python3

import contextlib

from copy import deepcopy
from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


def get_crates_stacks(inp: str) -> List[List[int]]:
    lines = inp.split("\n")
    nb_stacks = next(n for n in range(20) if len(lines[0]) == 3*n+(n-1))
    res = [ [] for _ in range(nb_stacks)]
    for l in lines[:-1]:
      for i in range(nb_stacks):
          if l[4*i + 1] != " ":
              res[i].insert(0, l[4*i + 1])
    return res


def get_instructions(inp: str) -> List[Tuple[int, int, int]]:
    res = []
    for l in inp.split("\n"):
      ints = [int(c) for c in l.replace("move ", "").replace("from ", "").replace("to ", "").split()]
      res.append((ints[0], ints[1]-1, ints[2]-1))
    return res


def read_input(filename: str = "input.txt") -> Tuple[List[List[int]], List[Tuple[int, int, int]]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        tmp = reader.read().split("\n\n")
        return get_crates_stacks(tmp[0]), get_instructions(tmp[1])


@show
def first(layout: List[List[int]], insts: List[Tuple[int, int, int]]) -> str:
    for nb, src, dest in insts:
        for _ in range(nb):
            layout[dest].append(layout[src].pop())
    return "".join(s[-1] for s in layout)


@show
def second(layout: List[List[int]], insts: List[Tuple[int, int, int]]) -> str:
    for nb, src, dest in insts:
        tmp = []
        for _ in range(nb):
            tmp.append(layout[src].pop())
        tmp.reverse()
        layout[dest].extend(tmp)
    return "".join(s[-1] for s in layout)


def test_example() -> None:
    inp = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        r1  = first(*deepcopy(inp))
        assert r1 == "CMZ", r1
        r2  = second(*inp)
        assert r2 == "MCD", r2


test_example()
s = read_input()
first(*deepcopy(s))  # FZCMJCRHZ
second(*s)  # JSDHQMZGF
