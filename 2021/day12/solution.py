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
        def add_edge(x,y):
            if x in res:
                res[x].append(y)
            else:
                res[x] = [y]
        for l in reader.readlines():
            n1, n2 = l.strip().split("-", maxsplit=1)
            add_edge(n1, n2)
            add_edge(n2, n1)
        return res


def path(graph: Dict[str, List[str]], cur_node: str, visited: Set[str], part2: bool = False) -> int:
    if cur_node == "end":
        return 1
    res = 0
    for node in graph[cur_node]:
        if node.islower():
            if node not in visited:
                res += path(graph, node, visited | {node}, part2)
            elif part2 and node not in {"start", "end"}:
                res += path(graph, node, visited | {node}, False)
        else:
            res += path(graph, node, visited, part2)
    return res


@show
def first(inp: Dict[str, List[str]]) -> int:
    return path(inp, "start", {"start"})


@show
def second(inp: Dict[str, List[str]]) -> int:
    return path(inp, "start", {"start"}, True)


def test_example() -> None:
    inp = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        assert first(inp) == 10
        assert second(inp) == 36
        inp = read_input("example_2.txt")
        assert first(inp) == 19
        assert second(inp) == 103
        inp = read_input("example_3.txt")
        assert first(inp) == 226
        assert second(inp) == 3509


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 4720
    second(inp)  # 147848
