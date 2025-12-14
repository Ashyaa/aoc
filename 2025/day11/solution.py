#!/usr/bin/env python3

from collections import defaultdict
from functools import cache
from pathlib import Path
from typing import Dict, Set, Tuple

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> Dict[str, Set[str]]:
    input_file = CWD.joinpath(filename)
    res = defaultdict(set)
    with open(input_file, "r") as reader:
        for line in reader.read().split("\n"):
            node, others = line.split(": ")
            res[node] = set(others.split())
    return res


def solve(inp: Dict[str, Set[str]], skips: int = 0) -> Tuple[int, int]:
    @cache
    def nb_paths(cur: str, target: str = "out") -> int:
        return cur == target or sum(nb_paths(next, target) for next in inp[cur])

    p1, p2 = 0, 0

    if skips != 1:
        p1 = nb_paths("you")

    if skips != 2:
        nb_dac_fft = nb_paths("dac", "fft")
        nb_fft_dac = nb_paths("fft", "dac")

        if nb_dac_fft:
            p2 = nb_paths("svr", "dac") * nb_dac_fft * nb_paths("fft", "out")
        else:
            p2 = nb_paths("svr", "fft") * nb_fft_dac * nb_paths("dac", "out")

    return p1, p2


def test_example() -> None:
    assert (r := solve(read_input("example.txt"), 2)) == (5, 0), r
    assert (r := solve(read_input("example2.txt"), 1)) == (0, 2), r


if __name__ == "__main__":
    test_example()
    show(solve)(read_input())  # 649, 458948453421420
