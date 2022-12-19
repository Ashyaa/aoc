#!/usr/bin/env python3

import contextlib

from copy import deepcopy
from functools import reduce

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent
TRIANGULAR = [(t - 1) * t // 2 for t in range(32 + 1)]
ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3


def read_input(filename: str = "input.txt") -> List[List[int]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        res = []
        for l in reader.read().splitlines():
            w = l.split(" ")
            res.append([int(w[i]) for i in [6, 12, 18, 21, 27, 30]])
        return res


def run(a,b,c,d, e,f,g,h):
    return a+e, b+f, c+g, d+h


def run_bp(bp: List[int], turn: int, to_build: int, stock: Tuple[int,int,int,int], robots: Tuple[int,int,int,int], res: int) -> int:
    max_or, max_cl, max_ob = max(bp[0], bp[1], bp[2], bp[4]), bp[3], bp[5]
    # stop path if the robot tp build is useless, i.e.:
    #     - it won't improve efficiency
    #     - it cannot be built
    #     - the robot building path is suboptimal
    if (to_build == ORE and robots[ORE] >= max_or or
        to_build == CLAY and robots[CLAY] >= max_cl or
        to_build == OBSIDIAN and (robots[OBSIDIAN] >= max_ob or robots[CLAY] == 0 ) or
        to_build == GEODE and robots[OBSIDIAN] == 0 or
        stock[GEODE] + robots[GEODE] * turn + TRIANGULAR[turn] <= res):
        return 0
    while turn > 0:
        if to_build == ORE and stock[ORE] >= bp[0]:
            new_s = run(*(stock[ORE]-bp[0], stock[CLAY], stock[OBSIDIAN], stock[GEODE]), *robots)
            new_robots = robots[ORE]+1, robots[CLAY], robots[OBSIDIAN], robots[GEODE]
            for robot in range(4):
                res = max(res, run_bp(bp, turn - 1, robot, new_s, new_robots, res))
            return res
        elif to_build == CLAY and stock[ORE] >= bp[1]:
            new_s = run(*(stock[ORE]-bp[1], stock[CLAY], stock[OBSIDIAN], stock[GEODE]), *robots)
            new_robots = robots[ORE], robots[CLAY]+1, robots[OBSIDIAN], robots[GEODE]
            for robot in range(4):
                res = max(res, run_bp(bp, turn - 1, robot, new_s, new_robots, res))
            return res
        elif to_build == OBSIDIAN and stock[ORE] >= bp[2] and stock[CLAY] >= bp[3]:
            new_s = run(*(stock[ORE]-bp[2], stock[CLAY]-bp[3], stock[OBSIDIAN], stock[GEODE]), *robots)
            new_robots = robots[ORE], robots[CLAY], robots[OBSIDIAN]+1, robots[GEODE]
            for robot in range(4):
                res = max(res, run_bp(bp, turn - 1, robot, new_s, new_robots, res))
            return res
        elif to_build == GEODE and stock[ORE] >= bp[4] and stock[OBSIDIAN] >= bp[5]:
            new_s = run(*(stock[ORE]-bp[4], stock[CLAY], stock[OBSIDIAN]-bp[5], stock[GEODE]), *robots)
            new_robots = robots[ORE], robots[CLAY], robots[OBSIDIAN], robots[GEODE]+1
            for robot in range(4):
                res = max(res, run_bp(bp, turn - 1, robot, new_s, new_robots, res))
            return res
        turn = turn - 1
        stock = run(*stock, *robots)
    return stock[GEODE]


def bp_score(bp: List[int], turns: int = 24) -> int:
    return max(run_bp(bp, turns, robot, (0,0,0,0), (1,0,0,0), 0) for robot in range(4))


@show
def first(l: List[List[int]]) -> int:
    return sum((i+1) * bp_score(bp) for i, bp in enumerate(l))


@show
def second(l: List[List[int]]) -> int:
    return reduce(lambda x, y: x*y, [bp_score(l[i], 32) for i in range(3) if i < len(l)])


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp)
        assert r1 == 33, r1
        r2  = second(inp)
        assert r2 == 56*62, r2


# test_example()
s = read_input()
first(s)  # 1466
second(s)  # 8250
