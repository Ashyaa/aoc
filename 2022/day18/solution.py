#!/usr/bin/env python3

import contextlib

from collections import deque

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[Tuple[int,int,int]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return [tuple(int(c) for c in l.split(",") ) for l in reader.readlines()]


@show
def first(l: List[Tuple[int,int,int]]) -> int:
    res = 0
    d = lambda c1, c2: sum(abs(c1[i] - c2[i]) for i in range(3))
    for i, c1 in enumerate(l):
        for j in range(i+1, len(l)):
            c2 = l[j]
            if d(c1, c2) == 1: res +=2
    return (len(l) * 6) - res


NEIGHBORS = [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1),(0,0,1)]


def flood_fill(mtx, size_x, size_y, size_z) -> int:
    queue = deque([(0,0,0)])
    count = 0
    while queue:
        x,y,z = queue.pop()
        if mtx[x][y][z] != 0:
            continue
        mtx[x][y][z] = 2
        for dx, dy, dz in NEIGHBORS:
            nx, ny, nz = x+dx, y+dy, z+dz
            if 0 <= nx <= size_x-1 and 0 <= ny <= size_y-1 and 0 <= nz <= size_z-1:
                if mtx[nx][ny][nz] == 1:
                    count += 1
                else:
                    queue.append((nx,ny,nz))
    return count


@show
def second(arr: List[Tuple[int,int,int]]) -> int:
    min_x, max_x = min(c[0] for c in arr)-1, max(c[0] for c in arr)+2
    min_y, max_y = min(c[1] for c in arr)-1, max(c[1] for c in arr)+2
    min_z, max_z = min(c[2] for c in arr)-1, max(c[2] for c in arr)+2
    mtx = [[[int((x,y,z) in arr) for z in range(min_z, max_z)] for y in range(min_y, max_y)] for x in range(min_x, max_x)]
    return flood_fill(mtx, max_x-min_x, max_y-min_y, max_z-min_z)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp)
        assert r1 == 64, r1
        r2  = second(inp)
        assert r2 == 58, r2


test_example()
s = read_input()
first(s)  # 3496
second(s)  # 2064
