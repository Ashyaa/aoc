#!/usr/bin/env python3

import contextlib

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import floyd_warshall

from itertools import combinations

from pathlib import Path
from typing import List
from AoC.util import show


CWD = Path(__file__).parent
START= "AA"

class Valve():
    name: str
    rate: int
    __dests: List[str] = []
    dests: List[int] = []
    open: bool = False

    def __init__(self, raw: str) -> None:
        self.open = False
        self.name = raw[6:8]
        tmp = raw.split(";")
        self.rate = int(tmp[0].split("=")[-1])
        self.__dests = [s[-2:] for s in tmp[1].split(", ")]
        self.dests = []

    def set_dests(self, d: List[str]) -> None:
        self.dests = [d.index(v) for v in self.__dests]


def read_input(filename: str = "input.txt") -> List[Valve]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        res = [Valve(l) for l in reader.read().split("\n")]
        keys = [v.name for v in res]
        for v in res:
            v.set_dests(keys)
        return res


def build_graph(vs: List[Valve]):
    matrix = [[1 if i in vs[j].dests else 0 for i in range(len(vs))] for j in range(len(vs))]
    return csr_matrix(matrix)


def sub_cost(vs, mtx, cur, flow, step, visited, res, p2: bool = False) -> int: 
    arr = [(j, mtx[cur][j], vs[j].rate) for j in range(len(vs)) if j not in visited and vs[j].rate != 0]
    time = 26 if p2 else 30
    if not arr:
        return int(res + flow * (time-step))
    tmp = []
    for (idx, dist, rate) in arr:
        if step + dist + 1 > time:
            tmp.append(int(res + flow * (time-step)))
            continue
        visited_2 = visited.copy()
        visited_2.add(idx)
        tmp.append(sub_cost(vs, mtx, idx, flow + rate, step + dist+1, visited_2, res + flow * (dist+1), p2))
    return max(tmp)


def sub_cost_2(vs, mtx, cur, flow, step, visited, res) -> List: 
    arr = [(j, mtx[cur][j], vs[j].rate) for j in range(len(vs)) if j not in visited and vs[j].rate != 0]
    if not arr:
        return [(0, int(res + flow * (30-step)))]
    tmp = []
    for (idx, dist, rate) in arr:
        if step + dist + 1 > 30:
            tmp.append((idx, int(res + flow * (30-step))))
            continue
        visited_2 = visited.copy()
        visited_2.add(idx)
        c = sub_cost_2(vs, mtx, idx, flow + rate, step + dist+1, visited_2, res + flow * (dist+1))
        tmp.append((idx, max(it[1] for it in c)))
    return sorted(tmp, key=lambda it: it[1])


@show
def first(vs: List[Valve]) -> int:
    dist_matrix = floyd_warshall(build_graph(vs), directed=False)
    cur = next(i for i, v in enumerate(vs) if v.name == START)
    return sub_cost(vs, dist_matrix, cur, 0, 0, set([cur]), 0)


@show
def second(vs: List[Valve]) -> int:
    mtx = floyd_warshall(build_graph(vs), directed=False)
    v2 = [i for i, v in enumerate(vs) if v.rate != 0]
    cur = next(i for i, v in enumerate(vs) if v.name == START)
    ma = 0
    l1 = int(len(v2) / 2)
    for perm1 in combinations(v2, l1):
        p1 = set(perm1)
        p2 = set(v2) - p1
        p1.add(cur)
        p2.add(cur)
        tmp = sub_cost(vs, mtx, cur, 0, 0, p1, 0, True) + sub_cost(vs, mtx, cur, 0, 0, p2, 0, True)
        if tmp > ma:
            ma = tmp
            print(p1, p2, ma)
    return ma


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp)
        assert r1 == 1651, r1
        r2  = second(inp)
        assert r2 == 1707, r2


# test_example()
s = read_input()
first(s)  # 1737
second(s)  # 2216
