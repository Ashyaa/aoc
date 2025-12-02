#!/usr/bin/env python3

import contextlib
from math import ceil, log
from pathlib import Path
from typing import List, Tuple

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[Tuple[int, int]]:
    input_file = CWD.joinpath(filename)
    res = []
    with open(input_file, "r") as reader:
        for line in reader.readlines():
            for item in line.rstrip().split(","):
                rge = item.split("-")
                res.append((int(rge[0]), int(rge[1])))
    return res


def nb_digits(n: int) -> int:
    return 1 if n == 1 else ceil(log(n) / log(10))


@show
def first(inp: List[Tuple[int, int]]) -> int:
    res = 0
    for mi, ma in inp:
        tmp = [str(n) for n in range(mi, ma + 1) if (nb_digits(n) % 2 == 0)]
        for t in tmp:
            s1, s2 = t[: len(t) // 2], t[len(t) // 2 :]
            if s1 == s2:
                res += int(t)
    return res


@show
def second(inp: List[Tuple[int, int]]) -> int:
    res = 0
    max_digits = max(max(nb_digits(mi), nb_digits(ma)) for mi, ma in inp)
    IDs = set()
    for i in range(1, 100000):
        max_reps = max_digits // nb_digits(i)
        for nb_reps in range(2, max_reps + 1):
            n = int(str(i) * nb_reps)
            if n not in IDs and any(mi <= n <= ma for (mi, ma) in inp):
                IDs.add(n)
                res += n
    return res


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1 = first(inp)
        assert r1 == 1227775554, r1
        r2 = second(inp)
        assert r2 == 4174379265, r2


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 37314786486
    second(inp)  # 47477053982
