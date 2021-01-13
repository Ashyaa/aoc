#!/usr/bin/env python3

import contextlib

from collections import defaultdict
from pathlib import Path
from typing import Dict, Tuple
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> Dict[str, Tuple[int, int, int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = {}
        for l in reader.readlines():
            words = l.split(" ")
            name = words[0]
            speed = int(words[3])
            speed_dur = int(words[6])
            cycle_dur = speed_dur + int(words[-2])
            res[name] = speed, speed_dur, cycle_dur
        return res


def race(r: Tuple[int, int, int], time: int) -> int:
    res = 0
    f = lambda t: r[0] if t % r[2] < r[1] else 0
    for t in range(time):
        res += f(t)
    return res


@show
def first(rs: Dict[str, Tuple[int, int, int]]) -> int:
    return max([race(r, 2503) for r in rs.values()])


def race_2(rs: Dict[str, Tuple[int, int, int]], ds: Dict[str, int], t: int) -> Dict[str, int]:
    for name, r in rs.items():
        f = lambda t: r[0] if t % r[2] < r[1] else 0
        ds[name] += f(t)
    return ds

@show
def second(rs: Dict[str, Tuple[int, int, int]], time=2503) -> int:
    res = defaultdict(int)
    ds = defaultdict(int)
    for t in range(time):
        ds = race_2(rs, ds, t)
        leader = max(list(ds.values()))
        for n in rs.keys():
            res[n] += 1 if ds[n] == leader else 0
    return max(list(res.values()))


def test_example() -> None:
    reindeers = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        assert race(reindeers["Dancer"], 1000) == 1056
        assert race(reindeers["Comet"], 1000) == 1120
        assert second(reindeers, 1000) == 689


test_example()
reindeers = read_input()
first(reindeers) # 2660
second(reindeers) # 1256