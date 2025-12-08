#!/usr/bin/env python3

import contextlib
from math import dist
from pathlib import Path
from typing import Dict, List, Set, Tuple

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[Tuple[int, int, int]]:
    input_file = CWD.joinpath(filename)
    res = []
    with open(input_file, "r") as reader:
        for line in reader.readlines():
            res.append(tuple(map(int, line.strip().split(","))))
    return res


def distances(points: List[Tuple[int, int, int]]) -> Dict[int, Tuple[int, int]]:
    res = {}
    for i, p1 in enumerate(points):
        for j in range(i + 1, len(points)):
            p2 = points[j]
            d = dist(p1, p2)
            res[d] = (i, j)
    return res


def update_circuits(circuits: List[Set[int]], p1: int, p2: int):
    p1_idx, p2_idx = None, None
    for j, c in enumerate(circuits):
        if p1 in c:
            p1_idx = j
        if p2 in c:
            p2_idx = j
        if p1_idx and p2_idx:
            break
    if p1_idx is None and p2_idx is None:
        circuits.append(set([p1, p2]))
    elif p1_idx is None:
        circuits[p2_idx].add(p1)
    elif p2_idx is None:
        circuits[p1_idx].add(p2)
    elif p1_idx != p2_idx:
        c2 = circuits[p2_idx]
        circuits[p1_idx] |= c2
        del circuits[p2_idx]

    return circuits


@show
def solve(inp: List[Tuple[int, int, int]], ex: bool = False) -> Tuple[int, int]:
    ds = distances(inp)
    nb_points = len(inp)
    circuits = []
    lim = 10 if ex else 1000
    r1 = 0
    for i, d in enumerate(sorted(ds.keys())):
        if i == lim:
            lengths = sorted({len(c) for c in circuits})
            r1 = lengths[-1] * lengths[-2] * lengths[-3]
        p1, p2 = ds[d]
        circuits = update_circuits(circuits, p1, p2)
        if len(circuits[0]) == nb_points:
            break
    lengths = sorted({len(c) for c in circuits})
    return r1, inp[p1][0] * inp[p2][0]


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1, r2 = solve(inp, True)
        assert r1 == 40, r1
        assert r2 == 25272


if __name__ == "__main__":
    test_example()
    inp = read_input()
    solve(inp)  # (79560, 31182420)
