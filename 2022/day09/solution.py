#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent
DIRECTIONS = {
    "U": (0,1),
    "D": (0,-1),
    "R": (1, 0),
    "L": (-1, 0),
}

def read_input(filename: str = "input.txt") -> List[Tuple[str, int]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        res = []
        for l in reader.readlines():
            tmp = l.strip().split()
            res.append((tmp[0], int(tmp[1])))
        return res


@show
def run(inp: List[Tuple[str, int]], size: int) -> int:
    rope = [(0,0) for _ in range(size)]
    positions = set([rope[-1]])
    for dir, nb in inp:
        dx, dy = DIRECTIONS[dir]
        for _ in range(nb):
            rope[0] = rope[0][0]+dx, rope[0][1]+dy
            for i in range(1, size):
                xh, yh = rope[i-1]
                x, y = rope[i]
                dist_x, dist_y = abs(x - xh), abs(y - yh)
                if dist_x + dist_y >= 2:
                    if dist_x < dist_y:
                        rope[i] = xh, yh + (-1 if y < yh else 1)
                    elif dist_x > dist_y:
                        rope[i] = xh + (-1 if x < xh else 1), yh
                    else:
                        rope[i] = xh + (-1 if x < xh else 1), yh + (-1 if y < yh else 1)
            positions.add(rope[-1])
    return len(positions)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r2  = run(inp, 2)
        assert r2 == 13, r2
        r2  = run(inp, 10)
        assert r2 == 1, r2
        inp = read_input("example_2.txt")
        r2  = run(inp, 10)
        assert r2 == 36, r2


test_example()
s = read_input()
run(s, 2)  # 6367
run(s, 10)  # 2536
