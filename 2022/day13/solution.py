#!/usr/bin/env python3

import contextlib

from functools import cmp_to_key
from pathlib import Path
from typing import List
from AoC.util import show


CWD = Path(__file__).parent

ITEMS = ["A","B","C"]
PLAYS = ["X","Y","Z"]


func = {
  (type(0), type(0)): lambda a, b, i: eq_int(a[i],b[i]),
  (type([]), type([])): lambda a, b, i: compare(a[i],b[i]),
  (type([]), type(0)): lambda a, b, i: compare(a[i],[b[i]]),
  (type(0), type([])): lambda a, b, i: compare([a[i]],b[i]),
}


def read_input(filename: str = "input.txt") -> List:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return [[eval(li) for li in l.split("\n")] for l in reader.read().split("\n\n")]


def eq_int(a: int, b: int) -> int:
    if a < b:
      return -1
    if a > b:
      return 1
    return 0


def compare(a: List, b: List) -> int:
    for i in range(len(b)):
        if i >= len(a):
            return -1 # a ran out of items
        typ = type(a[i]), type(b[i])
        res = func[typ](a, b, i)
        if res == 0:
            continue
        return res
    if len(a) > len(b):
        return 1
    return 0


@show
def first(l: List) -> int:
    return sum(i+1 for i, v in enumerate(l) if compare(v[0], v[1]) == -1)


@show
def second(l: List) -> int:
    res = [[[2]], [[6]]]
    for li in l:
        res.extend(li)
    res.sort(key=cmp_to_key(compare))
    return (res.index([[2]])+1) * (res.index([[6]])+1)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp)
        assert r1 == 13, r1
        r2  = second(inp)
        assert r2 == 140, r2


test_example()
s = read_input()
first(s)  # 6568
second(s)  # 19493
