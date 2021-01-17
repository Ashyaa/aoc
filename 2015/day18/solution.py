#!/usr/bin/env python3

import contextlib
import numpy as np

from pathlib import Path
from typing import Dict, Tuple
from AoC.util import show


CWD = Path(__file__).parent


class Matrix:
    state: np.ndarray
    next_state: np.ndarray

    def __init__(self, init_state: np.ndarray, p2: bool=False):
        self.state = init_state
        self.rows, self.cols = self.state.shape
        if p2: self.state[::self.rows-1, ::self.cols-1] = True
        self.p2 = p2


    def run(self) -> None:
        self.next_state = np.copy(self.state)
        for x, y in np.ndindex(self.state.shape):
            cur = self.state[x,y]
            neighbours = sum(self.state[max(x-1,0):min(x+2,self.rows), max(y-1,0):min(y+2,self.cols)].flatten())
            if cur and neighbours not in [3,4]:
                self.next_state[x,y] = False
            if not cur and neighbours == 3:
                self.next_state[x,y] = True
        self.state = self.next_state
        if self.p2: self.state[::self.rows-1, ::self.cols-1] = True


    def nb_on(self) -> int:
        return sum(self.state.flatten())


    def __repr__(self) -> str:
        return str(self.state)


def read_input(filename: str="input.txt") -> np.ndarray:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        lines = list(reader.readlines())
        res = np.zeros((len(lines), len(lines[0].strip())), dtype=bool)
        for i, l in enumerate(lines):
            for j, c in enumerate(l.strip()):
                res[i,j] = c == '#'
        return res


@show
def first(init: np.ndarray, n=100) -> int:
    m = Matrix(init)
    for _ in range(n):
        m.run()
    return m.nb_on()


@show
def second(init: np.ndarray, n=100) -> int:
    m = Matrix(init, True)
    for _ in range(n):
        m.run()
    return m.nb_on()


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        ex = read_input("example.txt")
        assert first(ex, 4) == 4
        assert second(ex, 5) == 17


test_example()
m = read_input()
first(m) # 1061
second(m) # 1006
