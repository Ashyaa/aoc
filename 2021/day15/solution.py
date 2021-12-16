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


def neighbours(shape: Tuple[int, int], coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = coord
    res = []
    for delta_x, delta_y in [(-1,0), (1,0), (0,-1), (0,1)]:
        new_x, new_y = x + delta_x, y + delta_y
        if 0 <= new_x < shape[0] and 0 <= new_y < shape[1]:
            res.append((new_x, new_y))
    return res


def a_star(arr: np.ndarray, stop: Tuple[int, int], p2: bool = False) -> int:
    total_risk = np.zeros(arr.shape, dtype=int) # total risk for each node
    q = [[(0,0)]] + [[] for _ in range(10*(arr.shape[0]+arr.shape[1]))] # queue of nodes by distance
    cur_risk = 0 # inital risk is none

    while total_risk[stop] == 0:
        for node in q[cur_risk]: # for each node at the current risk
            if cur_risk > total_risk[node]: # skip nodes whose risk is under the current risk
                continue
            for nbr in neighbours(arr.shape, node): # for each neighbour
                delta_risk = arr[nbr]
                if total_risk[nbr] == 0: # if neighbour was never visited
                    total_risk[nbr] = cur_risk + delta_risk # save neighbour total risk
                    q[cur_risk + delta_risk].append(nbr) # add neighbour to the queue for its total risk
        cur_risk += 1
    return total_risk[stop]


@show
def first(inp: np.ndarray) -> int:
    return a_star(inp, (inp.shape[0]-1, inp.shape[1]-1))


def build_map(inp: np.ndarray) -> np.ndarray:
    size_x, size_y = inp.shape[0], inp.shape[1]
    res = np.zeros((size_x*5, size_y*5), dtype=int)
    for x in range(res.shape[0]):
        for y in range(res.shape[1]):
            base_val = inp[x%size_x, y%size_y]
            shift = (x // size_x) + (y // size_y)
            res[x,y] = ((base_val - 1 + shift) % 9) + 1
    return res


@show
def second(inp: np.ndarray) -> int:
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
