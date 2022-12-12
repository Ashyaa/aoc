#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import Iterable, List, Tuple

import numpy as np
from AoC.util import show


CWD = Path(__file__).parent


def elev(c: str) -> int:
    if c == "S":
        return 0
    if c == "E":
        return 27
    return ord(c) - ord("a") + 1


def read_input(filename: str = "input.txt") -> List[List[int]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return [[elev(c) for c in s] for s in reader.read().split("\n")]


def neighbours(shape: Tuple[int, int], coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = coord
    res = []
    for delta_x, delta_y in [(-1,0), (1,0), (0,-1), (0,1)]:
        new_x, new_y = x + delta_x, y + delta_y
        if 0 <= new_x < shape[0] and 0 <= new_y < shape[1]:
            res.append((new_x, new_y))
    return res


def a_star(arr: List[List[int]], start: Tuple[int,int], end: Tuple[int,int], cur_min: int = 1000) -> int:
    shape = len(arr), len(arr[0])
    total_risk = [[0 for _ in range(shape[1])] for _ in range(shape[0])]
    max_risk = 10*(shape[0]+shape[1])
    q = [[start]] + [[] for _ in range(max_risk)]
    cur_risk = 0

    while total_risk[end[0]][end[1]] == 0:
        if cur_risk >= min(cur_min, max_risk):
            return cur_min
        for (n_x, n_y) in q[cur_risk]:
            if cur_risk > total_risk[n_x][n_y]:
                continue
            for (nb_x, nb_y) in neighbours(shape, (n_x, n_y)):
                if arr[nb_x][nb_y] > arr[n_x][n_y] +1:
                    q[-1].append((nb_x, nb_y))
                    continue
                delta_risk = 1
                if total_risk[nb_x][nb_y] == 0:
                    total_risk[nb_x][nb_y] = cur_risk + delta_risk
                    q[cur_risk + delta_risk].append((nb_x, nb_y))
        cur_risk += 1
    return total_risk[end[0]][end[1]]


def get_coord(arr: List[List[int]], wanted: int) -> Iterable[Tuple[int,int]]:
    for i, l in enumerate(arr):
        for j, n in enumerate(l):
            if n == wanted:
                yield (i, j)


@show
def first(inp: np.ndarray) -> int:
    return a_star(inp, next(get_coord(inp, 0)), next(get_coord(inp, 27)))


@show
def second(inp: np.ndarray) -> int:
    end = next(get_coord(inp, 27))
    res = 1000
    for s in get_coord(inp, 1):
        res = min(a_star(inp, s, end, res), res)
    return res


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp)
        assert r1 == 31, r1
        r2  = second(inp)
        assert r2 == 29, r2


test_example()
s = read_input()
first(s)  # 352
second(s)  # 345
