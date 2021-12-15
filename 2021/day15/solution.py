#!/usr/bin/env python3

import contextlib

from pathlib import Path
import numpy as np

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> np.ndarray:
    input_file = CWD.joinpath(filename)
    return np.genfromtxt(input_file, delimiter=1, dtype=int)


def neighbours(arr: np.ndarray, coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = coord
    for delta_x, delta_y in [(-1,0), (1,0), (0,-1), (0,1)]:
        new_x, new_y = x + delta_x, y + delta_y
        if 0 <= new_x < arr.shape[0] and 0 <= new_y < arr.shape[1]:
            yield (new_x, new_y)


def a_star(arr: np.ndarray, start: Tuple[int, int], stop: Tuple[int, int]) -> List[Tuple[int, int]]:
    open_lst = set([start])
    closed_lst = set([])
    risk_from_start = {start: 0}

    # next_node contains an adjac mapping of all nodes
    next_node = {start: start}

    while len(open_lst) > 0:
        n = None
        for coord in open_lst:
            if n is None or risk_from_start[coord] + arr[coord] <= risk_from_start[n] + arr[n]:
                n = coord

        if n == stop:
            reconst_path = []

            while next_node[n] != n: # start condition
                reconst_path.append(n)
                n = next_node[n]
            reconst_path.reverse()
            return reconst_path

        for m in neighbours(arr, n):
            risk = arr[m]
            if m not in open_lst and m not in closed_lst:
                open_lst.add(m)
                next_node[m] = n
                risk_from_start[m] = risk_from_start[n] + risk
            else:
                if risk_from_start[m] > risk_from_start[n] + risk:
                    risk_from_start[m] = risk_from_start[n] + risk
                    next_node[m] = n
                    if m in closed_lst:
                        closed_lst.remove(m)
                        open_lst.add(m)

        open_lst.remove(n)
        closed_lst.add(n)


@show
def first(inp: np.ndarray) -> int:
    pth = a_star(inp, (0,0), (inp.shape[0]-1, inp.shape[1]-1))
    return sum(inp[n] for n in pth)


def tile_value(value: int, shift: int) -> np.ndarray:
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
    arr = build_map(inp)
    pth = a_star(arr, (0,0), (arr.shape[0]-1, arr.shape[1]-1))
    return sum(arr[n] for n in pth)


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
