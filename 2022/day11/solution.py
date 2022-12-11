#!/usr/bin/env python3

import contextlib

from math import floor
from pathlib import Path
from typing import Callable, Dict, List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


def get_operation(str) -> Callable:
    arg = str.split()[-1]
    if "*" in str:
        if arg == "old":
            return lambda x: x * x
        return lambda x: x * int(arg)
    return lambda x: x + int(arg)


class Monkey():
    init_items: List[int] = []
    items: List[Dict[int,int]] = []
    op: Callable
    mod: int
    tru: int
    fals: int
    count: int = 0


    def __init__(self, str):
        lines = str.split("\n")
        self.init_items = [int(n) for n in lines[1][18:].split(', ')]
        self.items = []
        self.op = get_operation(lines[2])
        self.mod = int(lines[3].split()[-1])
        self.tru = int(lines[4].split()[-1])
        self.fals = int(lines[5].split()[-1])


    def send(self, p2: bool) -> Tuple[int, int, Dict[int, int]]:
        self.count += 1
        f = lambda x: self.op(x) if p2 else int(self.op(x) / 3)
        raw = -1
        if p2:
            it = {k: f(v) % k for k, v in self.items[0].items()}
        else:
            raw = f(self.init_items[0])
            it = {k: raw % k for k, v in self.items[0].items()}
        self.items = self.items[1:]
        self.init_items = self.init_items[1:]
        if it[self.mod] == 0:
            return self.tru, raw, it
        return self.fals, raw, it

    def apply_mods(self, mods: List[int]):
        for n in self.init_items:
            self.items.append({mod: n % mod for mod in mods})


def read_input(filename: str = "input.txt") -> List[Monkey]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        res = [Monkey(s) for s in reader.read().split("\n\n")]
        mods = [m.mod for m in res]
        for i, _ in enumerate(res):
            res[i].apply_mods(mods)
        return res


def turn(l: List[Monkey], p2: bool) -> List[Monkey]:
    for i, m in enumerate(l):
        for _ in enumerate(m.items):
            dst, raw, it = l[i].send(p2)
            l[dst].init_items.append(raw)
            l[dst].items.append(it)
    return l


@show
def run(l: List[Monkey], turns: int, p2: bool = False) -> int:
    for i in range(turns):
        l = turn(l, p2)
    res = [m.count for m in l]
    res.sort()
    return res[-2] * res[-1]


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        r1  = run(read_input("example.txt"), 20)
        assert r1 == 10605, r1
        r2  = run(read_input("example.txt"), 10000, True)
        assert r2 == 2713310158, r2


test_example()
run(read_input(), 20)  # 95472
run(read_input(), 10000, True)  # 17926061332
