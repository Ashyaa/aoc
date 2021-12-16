#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import *

import numpy as np
from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> np.ndarray:
    input_file = CWD.joinpath(filename)
    return np.genfromtxt(input_file, delimiter=1, dtype=int)


def neighbours(shape: Tuple[int, int], coord: Tuple[int, int]) -> Generator[Tuple[int, int], None, None]:
    x, y = coord
    for delta_x, delta_y in [(-1,0), (1,0), (0,-1), (0,1)]:
        new_x, new_y = x + delta_x, y + delta_y
        if 0 <= new_x < shape[0] and 0 <= new_y < shape[1]:
            yield (new_x, new_y)


def a_star(arr: np.ndarray, stop: Tuple[int, int], p2: bool = False) -> int:
    shape = (arr.shape[0]*5, arr.shape[1]*5) if p2 else arr.shape
    total_risk = np.zeros(shape, dtype=int) # total risk for each node
    q = [[(0,0)]] + [[] for _ in range(10000)] # queue of nodes by distance
    cur_risk = 0 # inital risk is none

    while total_risk[stop] == 0:
        for node in q[cur_risk]: # for each node at the current risk
            if cur_risk > total_risk[node]: # skip nodes whose risk is under the current risk
                continue
            for nbr in neighbours(shape, node): # for each neighbour
                if p2:
                    qx, rx = nbr[0] // arr.shape[0], nbr[0] % arr.shape[0]
                    qy, ry = nbr[1] // arr.shape[1], nbr[1] % arr.shape[1]
                    delta_risk = ((arr[rx, ry] + qx + qy - 1) % 9) + 1
                else:
                    delta_risk = arr[nbr]
                if total_risk[nbr] == 0: # if neighbour was never visited
                    total_risk[nbr] = cur_risk + delta_risk # save neighbour total risk
                    q[cur_risk + delta_risk].append(nbr) # add neighbour to the for its total risk
        cur_risk += 1
    return total_risk[stop]



@show
def first(inp: np.ndarray) -> int:
    return a_star(inp, (inp.shape[0]-1, inp.shape[1]-1))


def tile_value(value: int, shift: int) -> int:
    res = value
    for _ in range(shift):
        res = res + 1 if res < 9 else 1
    return res


def build_map(inp: np.ndarray) -> np.ndarray:
    size_x, size_y = inp.shape[0], inp.shape[1]
    res = np.zeros((size_x*5, size_y*5), dtype=int)
    for (x,y), value in np.ndenumerate(inp):
        for r1 in range(5):
            for r2 in range(5):
                res[(r1*size_x)+x, (r2*size_y)+y] = tile_value(value, r1+r2)
    return res


@show
def second(inp: np.ndarray) -> int:
    return a_star(inp, ((inp.shape[0] * 5) - 1, (inp.shape[1] * 5) - 1), True)


@show
def third(inp: np.ndarray) -> int:
    arr = build_map(inp)
    return a_star(arr, (arr.shape[0]-1, arr.shape[1]-1))


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 40
        assert second(inp) == 315


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 527
    second(inp)  # 2887
    third(inp)  # 2887
