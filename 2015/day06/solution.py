#!/usr/bin/env python3

import contextlib
import numpy as np

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


OPERATIONS_P1 = {
    "turn on": lambda x: True,
    "turn off": lambda x: False,
    "toggle": lambda x: not x,
}
OPERATIONS_P2 = {
    "turn on": lambda x: x+1,
    "turn off": lambda x: x-1 if x > 0 else 0,
    "toggle": lambda x: x+2,
}


def get_coords(raw: str) -> Tuple[int, int]:
    c1, c2 = raw.split(",")
    return int(c1), int(c2)


class Operation:
    def __init__(self, raw: str):
        if raw.startswith("toggle"):
            self.op = "toggle"
            s = raw.replace("toggle ", "")
        else:
            arg, s = raw[5:].split(" ", maxsplit=1)
            self.op = "turn " + arg
        c1, c2 = s.split(" through ")
        x1, y1 = get_coords(c1)
        x2, y2 = get_coords(c2)
        self.region = np.ix_(range(x1, x2+1), range(y1, y2+1))


def read_input(filename: str="input.txt") -> List[Operation]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = []
        for l in reader.readlines():
            res.append(Operation(l))
        return res


@show
def first(ops: List[Operation]) -> int:
    arr = np.zeros((1000, 1000), dtype=bool)
    for op in ops:
        f = np.vectorize(OPERATIONS_P1[op.op])
        arr[op.region] = f(arr[op.region])
    return sum(arr.flatten())


@show
def second(ops) -> int:
    arr = np.zeros((1000, 1000))
    for op in ops:
        f = np.vectorize(OPERATIONS_P2[op.op])
        arr[op.region] = f(arr[op.region])
    return sum(arr.flatten())


ops = read_input()
first(ops) # 543903
second(ops) # 14687245.0