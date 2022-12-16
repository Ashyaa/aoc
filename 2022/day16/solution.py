#!/usr/bin/env python3
# improved solution credit: https://github.com/juanplopes/advent-of-code-2022/blob/main/day16.py

import contextlib

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import floyd_warshall

from pathlib import Path
from typing import Dict, List, Tuple
from AoC.util import show


CWD = Path(__file__).parent
START = "AA"


def read_input(filename: str = "input.txt") -> Tuple[List[List[int]], Dict[int, int], Dict[int, int], int]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        lines = [l for l in reader.read().splitlines()]
    names = [l[6:8] for l in lines]
    graph, rates = [[0 for _ in lines] for _ in lines], {}
    for i, l  in enumerate(lines):
        r = int(l.split(";")[0].split("=")[-1])
        if r != 0: rates[i] = r
        for j in [names.index(s[-2:]) for s in l.split(";")[1].split(", ")]:
            graph[i][j] = 1
    return floyd_warshall(csr_matrix(graph), directed=False), rates, {i: 1 << i for i in rates},  names.index(START)


def visit(mtx: List[List[int]], rates: Dict[int, int], mask: Dict[int, int], cur: int, budget: int, state: int, value: int, answer: Dict[int, int]):
    answer[state] = max(answer.get(state, 0), value)
    for u, r in rates.items():
        newbudget = budget - int(mtx[cur][u]) - 1
        if mask[u] & state or newbudget < 0:
            continue
        visit(mtx, rates, mask, u, newbudget, state | mask[u], value + newbudget * r, answer)
    return answer


@show
def first(mtx: List[List[int]], rate: Dict[int, int], mask: Dict[int, int], cur: int) -> int:
    return max(visit(mtx, rate, mask, cur, 30, 0, 0, {}).values())


@show
def second(mtx: List[List[int]], rate: Dict[int, int], mask: Dict[int, int], cur: int) -> int:
    dic = visit(mtx, rate, mask, cur, 26, 0, 0, {})
    return max(v1+v2 for k1, v1 in dic.items() for k2, v2 in dic.items() if not k1 & k2)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(*inp)
        assert r1 == 1651, r1
        r2  = second(*inp)
        assert r2 == 1707, r2


test_example()
s = read_input()
first(*s)  # 1737
second(*s)  # 2216
