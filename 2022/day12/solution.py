#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List, Tuple

import numpy as np
from AoC.util import show


CWD = Path(__file__).parent


def elev(c: str) -> int:
    if c == b"S":
        return 0
    if c == b"E":
        return 27
    return ord(c) - ord("a") + 1


def read_input(filename: str = "input.txt", cols: int = 8) -> List[str]:
  input_file = CWD.joinpath(filename)
  return np.genfromtxt(input_file, delimiter=1, dtype=int, converters={i: elev for i in range(cols)})


def neighbours(shape: Tuple[int, int], coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = coord
    res = []
    for delta_x, delta_y in [(-1,0), (1,0), (0,-1), (0,1)]:
      new_x, new_y = x + delta_x, y + delta_y
      if 0 <= new_x < shape[0] and 0 <= new_y < shape[1]:
            res.append((new_x, new_y))
    return res


def a_star(arr: np.ndarray, start: Tuple[int, int], end: Tuple[int, int], cur_min: int = 1000) -> int:
    total_risk = np.zeros(arr.shape, dtype=int)
    max_risk = 10*(arr.shape[0]+arr.shape[1])
    q = [[start]] + [[] for _ in range(max_risk)]
    cur_risk = 0

    while total_risk[end] == 0:
        if cur_risk >= min(cur_min, max_risk):
            return cur_min
        for node in q[cur_risk]:
            if cur_risk > total_risk[node]:
              continue
            for nbr in neighbours(arr.shape, node):
              if arr[nbr] > arr[node] +1:
                q[-1].append(nbr)
                continue
              delta_risk = 1
              if total_risk[nbr] == 0:
                total_risk[nbr] = cur_risk + delta_risk
                q[cur_risk + delta_risk].append(nbr)
        cur_risk += 1
    return total_risk[end]


def get_coord(arr: np.ndarray, n: int) -> List[Tuple[int,int]]:
    tmp = np.where(arr == n)
    return [c for c in zip(tmp[0], tmp[1])]


@show
def first(inp: np.ndarray) -> int:
    return a_star(inp, get_coord(inp, 0)[0], get_coord(inp, 27)[0])


@show
def second(inp: np.ndarray) -> int:
    end = get_coord(inp, 27)[0]
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
s = read_input(cols=70)
first(s)  # 352
second(s)  # 345
