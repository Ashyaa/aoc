
#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import *

from itertools import product

import numpy as np
from AoC.util import show

CWD = Path(__file__).parent

Ranges = Tuple[int, int, int, int, int, int]
Cuboid = Tuple[int, Ranges]


def read_input(filename: str = "input.txt") -> List[Cuboid]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = []
        for l in reader.readlines():
            value = l[:2] == "on"
            ranges = tuple([int(v) for coord in l.strip().split(' ', 1)[1].split(",") for v in coord[2:].split("..")])
            res.append((value, ranges))
        return res


@show
def first(inp: List[Cuboid]) -> int:
    arr = np.zeros((101,101,101), dtype=int)
    for val, (x1, x2, y1, y2, z1, z2) in inp:
        if not (-50 <= x1 <= 50): break
        arr[x1+50:x2+51, y1+50:y2+51, z1+50:z2+51] = val
    return sum(arr.flatten())


volume = lambda a, b, c, d, e, f: (b+1-a) * (d+1-c) * (f+1-e)


def extrude(ax1:int, ax2: int, bx1: int, bx2: int) -> Tuple[List[Tuple[int,int]], Tuple[int,int]]:
    """extrude b from a"""
    res = []
    if (bx1 <= ax1 and bx2 >= ax2):
        return [(ax1, ax2)], (ax1, ax2)
    if ax1 < bx1:
        res.append((ax1, bx1-1))
        if bx2 < ax2:
            res.append((bx2+1, ax2))
            res.append((bx1, bx2))
        else:
            res.append((bx1, ax2))
    else:
        res.append((bx2+1, ax2))
        res.append((ax1, bx2))
    return res, res[-1]


def sub_volumes(o: Ranges, e: Ranges) -> List[Ranges]:
    ox1, ox2, oy1, oy2, oz1, oz2 = o
    ex1, ex2, ey1, ey2, ez1, ez2 = e
    are_disjoint = lambda a, b, c, d: (a > d or c > b)
    if are_disjoint(ox1, ox2, ex1, ex2) or are_disjoint(oy1, oy2, ey1, ey2) or are_disjoint(oz1, oz2, ez1, ez2):
        return [o]
    sub_rx, ix = extrude(ox1, ox2, ex1, ex2)
    sub_ry, iy = extrude(oy1, oy2, ey1, ey2)
    sub_rz, iz = extrude(oz1, oz2, ez1, ez2)
    res = [rx+ry+rz for rx, ry, rz in product(sub_rx, sub_ry, sub_rz) if rx != ix or ry != iy or rz != iz]
    return res


@show
def second(inp: List[Cuboid]) -> int:
    res = [inp[0][1]]
    for val, cur_rges in inp[1:]:
        tmp = []
        for rges_1 in res:
            tmp.extend(sub_volumes(rges_1, cur_rges))
        res = tmp
        if val:
            res.append(cur_rges)
    return sum(volume(*rges) for rges in res)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert volume(1,3,1,3,1,3) == 27
        assert volume(-5,5,0,10,10,20) == 1331
        a = (-1,10,1,28,3,5)
        b = (3,5,3,5,3,5)
        exp = [(-1, 2, 1, 2, 3, 5), (-1, 2, 3, 5, 3, 5), (-1, 2, 6, 28, 3, 5), (6, 10, 1, 2, 3, 5), (6, 10, 3, 5, 3, 5), (6, 10, 6, 28, 3, 5), (3, 5, 1, 2, 3, 5), (3, 5, 6, 28, 3, 5)]
        assert set(sub_volumes(a,b)) == set(exp)
        inp = read_input("example.txt")
        assert first(inp) == 590784
        inp = read_input("example_2.txt")
        assert second(inp) == 2758514936282235


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 527915
    second(inp)  # 1218645427221987
