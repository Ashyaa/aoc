#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent
ROTATE = lambda dir, right: (dir + 1) % 4 if right else (dir - 1) % 4
IN_BOUNDS = lambda x,y,map: 0 <= x < len(map) and 0 <= y < len(map[0])
MOVES: List[Tuple[int,int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]
UNMATCHED = (-1,-1)


def read_input(filename: str = "input.txt") -> Tuple[List[str], str]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        tmp = reader.read().split("\n\n")
        map = tmp[0].split("\n")
        max_len = max(len(s) for s in map)
        for i in range(len(map)):
            if len(map[i]) < max_len:
                map[i] += " " * (max_len - len(map[i]))
        return map, tmp[1]


def layout(map: List[str]) -> Tuple[List[Tuple[int,int]],List[Tuple[int,int]], List[List[Tuple[int,int]]]]:
    row, col = [], []
    nb_cols = max(len(s) for s in map)
    for s in map:
        mi, ma = 0, 0
        for j, c in enumerate(s):
            if c != " ":
                mi = j
                break
        for j, c in enumerate(s[::-1]):
            if c != " ":
                ma = len(s)-j-1
                break
        row.append((mi, ma))
    for i in range(nb_cols):
        s = [map[row][i] for row in range(len(map))]
        mi, ma = 0, 0
        for j, c in enumerate(s):
            if c != " ":
                mi = j
                break
        for j, c in enumerate(s[::-1]):
            if c != " ":
                ma = len(s)-j-1
                break
        col.append((mi, ma))
    return row, col, sides(map, row)


def new_dir(side: List[Tuple[int,int]]) -> int:
    x1, y1 = side[0]
    x2, y2 = side[-1]
    if x1 == x2:
        return 1 if y1 < y2 else 3
    return 2 if x1 < x2 else 0


def mapping(sides: List[List[Tuple[int,int]]]) -> List[Tuple[int,int]]:
    res = [UNMATCHED for _ in sides]
    for i, side in enumerate(sides):
        j = (i + 1) % 14
        if res[i] != UNMATCHED or res[j] != UNMATCHED:
            continue
        next_side = sides[j]
        if dist(*side[-1], *next_side[0]) == 2:
            res[i] = (j, new_dir(next_side))
            res[j] = (i, new_dir(side))
            h, k = (i-1) % 14, (j+1) % 14
            prev_side, next_next_side = sides[h], sides[k]
            d1, d2 = dist(*prev_side[-1], *side[0]), dist(*next_side[-1], *next_next_side[0])
            if (d1, d2) == (0,1) or (d2, d1) == (0,1):
                res[h] = (k, new_dir(next_next_side))
                res[k] = (h, new_dir(prev_side))
    for i in range(14):
        if res[i] != UNMATCHED:
                continue
        j = (i + 1) % 14
        op = lambda n: (n+1) % 14
        if res[j] == UNMATCHED:
            j = (i - 1) % 14
            op = lambda n: (n-1) % 14
        while j != i and res[j] != UNMATCHED:
            j = op(j)
        res[i] = (j, new_dir(sides[j]))
        res[j] = (i, new_dir(sides[i]))
    return res


def sides(map: List[str], row: List[Tuple[int,int]]) -> List[List[Tuple[int,int]]]:
    sides = []
    side_len = min(abs(a - b)+1 for a,b in row)
    x, y = 0, row[0][0]
    dir = 0
    while map[x][y] != ".":
        y = y + 1
    while len(sides) < 14:
        new_dir = ROTATE(dir, False)
        lx, ly = MOVES[new_dir]
        if IN_BOUNDS(x+lx, y+ly, map) and map[x+lx][y+ly] != " ":
            x, y = x+lx, y+ly
            dir = new_dir
            continue
        dx, dy = MOVES[dir]
        nx = x + dx*(side_len-1)
        ny = y + dy*(side_len-1)
        if not (IN_BOUNDS(nx, ny, map) ) or map[nx][ny] == " ":
            dir = (dir + 1) % 4
            continue
        sides.append(((x,y), (nx,ny)))
        x, y = nx, ny
        if IN_BOUNDS(x+dx, y+dy, map) and map[x+dx][y+dy] != " ":
            x, y = x +dx, y + dy
    res = []
    for (p1_x, p1_y), (p2_x, p2_y) in sides:
        if p1_x == p2_x:
            begin, end, step = (p1_y, p2_y+1, 1) if p1_y < p2_y else (p1_y, p2_y-1, -1)
            res.append([(p1_x, y) for y in range(begin, end, step)])
        else:
            begin, end, step = (p1_x, p2_x+1, 1) if p1_x < p2_x else (p1_x, p2_x-1, -1)
            res.append([(x, p1_y) for x in range(begin, end, step)])
    return res


def move_p1(x: int, y: int, dx: int, dy: int, mi: int, ma: int, map: List[str]) -> Tuple[int,int]:
    nx, ny = x+dx, y+dy
    if dx == 0:
        ny = mi if ny > ma else ny
        ny = ma if ny < mi else ny
    elif dy == 0:
        nx = mi if nx > ma else nx
        nx = ma if nx < mi else nx
    if map[nx][ny] == "#":
        return x, y
    return nx, ny


def dist(a: int, b: int, c: int, d: int) -> int:
    return abs(a-c) + abs(b-d)


def warp(x: int, y: int, dir: int, sides: List[List[Tuple[int,int]]], warps: List[Tuple[int,int]]):
    cur_side_idx = next(i for i, side in enumerate(sides) if (x,y) in side and (dir % 2) == (side[0][0] == side[-1][0]))
    pos_idx = sides[cur_side_idx].index((x,y))
    new_side, new_dir = warps[cur_side_idx]
    nx, ny =  sides[new_side][-pos_idx-1]
    return nx, ny, new_dir


def move_p2(x: int, y: int, dir: int, map: List[str], sides: List[List[Tuple[int,int]]], warps: List[Tuple[int,int]]) -> Tuple[int,int,int]:
    dx, dy = MOVES[dir]
    nx, ny = x+dx, y+dy
    if IN_BOUNDS(nx, ny, map):
        if map[nx][ny] == ".":
            return nx, ny, dir
        elif map[nx][ny] == "#":
            return x, y, dir
    nx, ny, ndir = warp(x, y, dir, sides, warps)
    if map[nx][ny] == "#":
        return x, y, dir
    return nx, ny, ndir


@show
def run(map: List[str], path: str, p2: bool = False) -> int:
    rows, cols, sides = layout(map)
    warps = mapping(sides)
    dir, i = 0, 0
    x, y = 0, rows[0][0]
    while map[x][y] != ".":
        y = y + 1
    while i < len(path):
        if path[i].isalpha():
            c = path[i]
            i += 1
            dir = ROTATE(dir, c == "R")
            continue
        raw = ""
        while i < len(path) and path[i].isdigit():
            raw += path[i]
            i += 1
        mv = MOVES[dir]
        mi, ma = rows[x] if mv[0] == 0 else cols[y]
        for _ in range(int(raw)):
            if p2:
                nx, ny, ndir = move_p2(x, y, dir, map, sides, warps)
            else:
                nx, ny = move_p1(x, y, *mv, mi, ma, map)
                ndir = dir
            if (x,y,dir) == (nx,ny,ndir):
                break
            x, y, dir = nx, ny, ndir
    return 1000 * (x+1) + 4 * (y+1) + dir


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = run(*inp)
        assert r1 == 6032, r1
        r2  = run(*inp, True)
        assert r2 == 5031, r2


test_example()
s = read_input()
run(*s)  # 106094
run(*s, True)  # 162038
