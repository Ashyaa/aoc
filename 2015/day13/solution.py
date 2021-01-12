#!/usr/bin/env python3
import contextlib

from collections import defaultdict
from pathlib import Path
from typing import Dict, List
from AoC.util import show


CWD = Path(__file__).parent


class Graph():
    def __init__(self, g):
        self.graph = g
        self.people = list(self.graph.keys())
        self.nb = len(self.people)


    def permutations(self, partial: List[str]=[]) -> List[List[str]]:
        res = []
        for p in self.people:
          if p in partial:
            continue
          tmp = partial+[p]
          if len(partial) == self.nb-1:
            res.append(tmp)
          else:
            res.extend(self.permutations(tmp))
        return res


    def happiness(self, order: List[str]) -> int:
        res = 0
        for i in range(self.nb):
            p1, p2 = order[i-1], order[i]
            res += self.graph[p1][p2]
        return res


def read_input(filename: str="input.txt") -> Dict[str, Dict[str, int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = defaultdict(lambda: defaultdict(int))
        for l in reader.readlines():
          sign = -1 if "lose" in l else 1
          words = l.strip()[:-1].split(" ")
          n1, n2, val = words[0], words[-1], int(words[3])
          res[n1][n2] += sign*val
          res[n2][n1] += sign*val
        return Graph(res)


@show
def first(g: Graph) -> int:
    return max([g.happiness(p) for p in g.permutations()])


@show
def second(g: Graph) -> int:
    g.nb += 1
    g.people.append("I")
    return max([g.happiness(p) for p in g.permutations()])


def test_example() -> None:
    g = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        assert first(g) == 330


test_example()
g = read_input()
first(g) # 664
second(g) # 640