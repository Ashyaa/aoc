#!/usr/bin/env python3

import contextlib
import sys

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


class Graph():

    def __init__(self, cities):
        self.graph = cities
        self.cities = cities.keys()


    def minDistance(self, dist, sptSet):
        min = sys.maxsize
        for v in self.cities:
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                city = v
        return city


    def maxDistance(self, dist, sptSet):
        max = -1
        for v in self.cities:
            if dist[v] > max and sptSet[v] == False:
                max = dist[v]
                city = v
        return city


    def dijkstra(self, src: str, max: bool = False) -> int:
        dist = {k: -1 if max else sys.maxsize for k in self.cities}
        dist[src] = 0
        path = []
        sptSet = defaultdict(bool)
        for _ in self.graph:
            u = self.maxDistance(dist, sptSet) if max else self.minDistance(dist, sptSet)
            sptSet[u] = True
            for v in self.cities:
                if u != v and sptSet[v] == False:
                    dist[v] = dist[u] + self.graph[u][v]
            path.append(u)
        return dist[path[-1]]


    def p1(self) -> int:
        return min([self.dijkstra(c) for c in self.cities])


    def p2(self) -> int:
        return max([self.dijkstra(c, max=True) for c in self.cities])


def read_input(filename: str="input.txt") -> Graph:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = defaultdict(dict)
        for l in reader.readlines():
            raw, dist = l.split(" = ", maxsplit=1)
            d = int(dist)
            c1, c2 = raw.split(" to ", maxsplit=1)
            res[c1][c2] = res[c2][c1] = d
        return Graph(res)

@show
def first(g: Graph) -> int:
    return g.p1()


@show
def second(g: Graph) -> int:
    return g.p2()


def test_example() -> None:
    g = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        assert g.dijkstra("London") == 605
        assert g.dijkstra("Dublin") == 659
        assert g.dijkstra("Belfast") == 605
        assert first(g) == 605
        assert second(g) == 982


test_example()
g = read_input()
first(g) # 141
second(g) # 736