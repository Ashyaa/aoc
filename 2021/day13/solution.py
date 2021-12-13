#!/usr/bin/env python3

import contextlib

from pathlib import Path
import numpy as np

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> Tuple[np.ndarray, List[Tuple[str, int]]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        dots, instructions, dots_ok = [], [], False
        for l in reader.readlines():
            if l.strip() == "":
                dots_ok = True
                continue
            if dots_ok:
                axis, coord = l.strip().rsplit(" ", 1)[1].split("=", maxsplit=1)
                instructions.append((axis, int(coord)))
            else:
                x, y = l.strip().split(",")
                dots.append((int(y), int(x)))
        arr = np.zeros((max(dots, key=lambda x: x[0])[0]+1, max(dots, key=lambda x: x[1])[1]+1), dtype=bool)
        for d in dots:
            arr[d] = True
        return arr, instructions


def apply_fold(arr: np.ndarray, fold: Tuple[str, int]) -> np.ndarray:
    axis = fold[1]
    if fold[0] == "y":
        arr1 = arr[:axis,:]
        arr2 = np.flipud(arr[axis+1:,:])
    else:
        arr1 = arr[:,:axis]
        arr2 = np.fliplr(arr[:,axis+1:])
    return arr1 | arr2


@show
def first(input: np.ndarray, instructions: List[Tuple[str, int]]) -> int:
    return np.count_nonzero(apply_fold(input, instructions[0]))


def dump(arr: np.ndarray, file: Path) -> None:
    with open(file, 'w') as fi:
        for x in range(arr.shape[0]):
            for y in range(arr.shape[1]):
                fi.write('█' if arr[x,y] else ' ')
            fi.write('\n')


@show
def second(input: np.ndarray, instuctions: List[Tuple[str, int]]) -> None:
    arr = input.copy()
    for fold in instuctions:
        arr = apply_fold(arr, fold)
    dump(arr, CWD.joinpath("output.txt"))


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        i1, i2 = read_input("example.txt")
        assert first(i1, i2) == 17
        assert second(i1, i2) == None


if __name__ == "__main__":
    test_example()
    i1, i2 = read_input()
    first(i1, i2)  # 724
    second(i1, i2)  # CPJBERUL (see output.txt)
