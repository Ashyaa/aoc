#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent
ROTATE = lambda dir, right: (dir + 1) % 4 if right else (dir - 1) % 4
MOVES: List[Tuple[int,int]] = [
    (0, 1), # RIGHT
    (1, 0), # DOWN
    (0, -1), # LEFT
    (-1, 0), # UP
]
IN_BOUNDS = lambda x,y,map: 0 <= x < len(map) and 0 <= y < len(map[0])
WARP = [ #TODO: generate structure with mapping function
    (9, 1),
    (8, 0),
    (5, 2),
    (4, 1),
    (3, -1),
    (2, 2),
    (7, 1),
    (6, -1),
    (1, 0),
    (0, -1),
    (13, 2),
    (12, 1),
    (11, -1),
    (10, 2),
]


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


def mapping(sides: List) -> List:
    res = [(-1,-1,-1) for _ in sides] # matching side, reversed, rotation
    for i, side in enumerate(sides):
        if res[i] != (-1,-1,-1):
            continue
        p2 = side[-1]
        j = (i+1) % 14
        c1, c2 = (0,0,0), (1,0,0)
        flip = False
        while j != i:
            other_side = sides[j]
            nc1 = c2
            # FIX: handle cube flip properly to match sides
            if dist(*other_side[0], *p2) == 2:
                nc2 = c1
                flip = not flip
            elif other_side[0] == p2: # same face
                nc2 = (c2[1], int(not c2[0]), c2[2]) if flip else (int(not c2[1]), c2[0], c2[2])
            else:
                nc2 = int(not c2[2]), c2[1], c2[0]
                nc2 = (c2[2], c2[1], int(not c2[0])) if flip else (int(not c2[2]), c2[1], c2[0])
            if nc1 == (0,0,0) and nc2 == (1,0,0):
                res[i] = (j, 0, 0)
                res[j] = (i, 0, 0)
                break
            elif nc1 == (1,0,0) and nc2 == (0,0,0):
                res[i] = (j, 1, 0)
                res[j] = (i, 1, 0)
                break
            p2 = other_side[-1]
            c1, c2 = nc1, nc2
            j = (j + 1) % 14
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
    # mapping(res)
    return res


def move(x: int, y: int, dx: int, dy: int, mi: int, ma: int, map: List[str]) -> Tuple[int,int]:
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


def dist(a,b, c, d) -> int:
    return abs(a-c) + abs(b-d)


def warp(x: int, y: int, dir: int, sides: List[List[Tuple[int,int]]], cheat: bool):
    cur_side_idx = next(i for i, side in enumerate(sides) if (x,y) in side and (dir % 2) == (side[0][0] == side[-1][0])) 
    pos_idx = sides[cur_side_idx].index((x,y))
    if cheat:
        new_side, rot = WARP[cur_side_idx]
        new_dir = (dir + rot) % 4
        nx, ny =  sides[new_side][-pos_idx-1]
        return nx, ny, new_dir
    step, i = 0, 1
    new_dir = dir 
    while i != 0:
        next_side_idx = (cur_side_idx + 1) % 14
        p1 = sides[cur_side_idx][-1]
        p2 = sides[next_side_idx][0]
        if p1 == p2:
            i += 1
        else:
            i -= 1
            new_dir = (new_dir + 1) % 4
        cur_side_idx = next_side_idx
        step += 1
    nx, ny = sides[cur_side_idx][-pos_idx-1]
    return nx, ny, new_dir


def move_2(x: int, y: int, dir: int, map: List[str], sides: List[List[Tuple[int,int]]], cheat: bool) -> Tuple[int,int,int]:
    dx, dy = MOVES[dir]
    nx, ny = x+dx, y+dy
    if IN_BOUNDS(nx, ny, map):
        if map[nx][ny] == ".":
            return nx, ny, dir
        elif map[nx][ny] == "#":
            return x, y, dir
    nx, ny, ndir = warp(x, y, dir, sides, cheat)
    if map[nx][ny] == "#":
        return x, y, dir
    return nx, ny, ndir


@show
def first(map: List[str], path: str) -> int:
    rows, cols, _ = layout(map)
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
        n = int(raw)
        mv = MOVES[dir]
        mi, ma = rows[x] if mv[0] == 0 else cols[y]
        for _ in range(n):
            nx, ny = move(x, y, *mv, mi, ma, map)
            if (x,y) == (nx,ny):
                break
            x, y = nx,ny
    return 1000 * (x+1) + 4 * (y+1) + dir


@show
def second(map: List[str], path: str, cheat: bool = False) -> int:
    rows, _, sides = layout(map)
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
        for _ in range(int(raw)):
            nx, ny, ndir = move_2(x, y, dir, map, sides, cheat)
            if (x,y,dir) == (nx,ny,ndir):
                break
            x, y, dir = nx, ny, ndir
    return 1000 * (x+1) + 4 * (y+1) + dir


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(*inp)
        assert r1 == 6032, r1
        r2  = second(*inp)
        assert r2 == 5031, r2


test_example()
s = read_input()
first(*s)  # 106094
second(*s, cheat=True)  # 162038
