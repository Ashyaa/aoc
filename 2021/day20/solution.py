#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import *

import numpy as np
from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> Tuple[str, np.ndarray]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        s = reader.readline().strip().replace('.', '0').replace('#', '1')
        reader.readline()
        res = []
        for l in reader.readlines():
            ll = l.strip().replace('.', '0').replace('#', '1')
            res.append(np.array([c for c in ll], dtype=str))
        res = np.array(res)
        return s, res


def step(s: str, arr: np.ndarray, i: int) -> np.ndarray:
    inverted = s[0] == '1' and s[-1] == '0'
    cons = i%2 if inverted else 0
    arr = np.pad(arr, ((2, 2), (2, 2)), 'constant', constant_values=cons)
    if inverted and not(i%2):
        res = np.ones(arr.shape, dtype=int).astype(str)
    else:
        res = np.zeros(arr.shape, dtype=int).astype(str)
    for i in range(1, arr.shape[0]-1):
        for j in range(1, arr.shape[1]-1):
            idx = int("".join(arr[i-1:i+2, j-1:j+2].flatten()), 2)
            res[i,j] = s[idx]
    return res


@show
def first(s: str, inp: np.ndarray, steps: int) -> None:
    arr = inp.copy()
    for i in range(steps):
        arr = step(s, arr, i)
    return arr.astype(int).sum()


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        s, inp = read_input("example.txt")
        assert first(s, inp, 2) == 35
        assert first(s, inp, 50) == 3351


if __name__ == "__main__":
    test_example()
    s, inp = read_input()
    first(s, inp, 2)  # 5065
    first(s, inp, 50)  # 14790
