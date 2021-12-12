#!/usr/bin/env python3

from collections import defaultdict
import contextlib

from pathlib import Path

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> Dict[str, List[str]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = {}
        for l in reader.readlines():
            n1, n2 = l.split("-")[0], l.strip().split("-")[1]
            if n1 in res:
                res[n1].append(n2)
            else:
                res[n1] = [n2]
            if n2 in res:
                res[n2].append(n1)
            else:
                res[n2] = [n1]
        return res


def path(graph: Dict[str, List[str]], cur_node: str, visited: Dict[str, int]) -> List[List[str]]:
    res = []
    if cur_node == "end":
        return [[cur_node]]
    if cur_node.islower():
        visited[cur_node] += 1
    for node in graph[cur_node]:
        if visited[node] < 2:
            pths =  path(graph, node, visited.copy())
            for p in pths:
                res.append([cur_node] + p)
    if not res:
        res = [[cur_node]]
    return res


@show
def first(inp: Dict[str, List[str]]) -> int:
    visited = {node: int(node.islower()) for node in inp}
    return len([p for p in path(inp, "start", visited) if p[-1] == "end"])


@show
def second(inp: Dict[str, List[str]]) -> int:
    visited = {node: int(node.islower()) for node in inp}
    res = []
    for k in [k for k in visited if k.islower()]:
        if k == "start" or k == "end": continue
        vis2 = visited.copy()
        vis2[k] = 0
        tmp = [p for p in path(inp, "start", vis2) if p[-1] == "end"]
        for p in tmp:
            pth = "".join(p)
            if pth not in res:
                res.append(pth)
    return len(res)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 10
        assert second(inp) == 36
    with contextlib.redirect_stdout(None):
        inp = read_input("example_2.txt")
        assert first(inp) == 19
        assert second(inp) == 103
    with contextlib.redirect_stdout(None):
        inp = read_input("example_3.txt")
        assert first(inp) == 226
        assert second(inp) == 3509


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 4720
    second(inp)  # p2
