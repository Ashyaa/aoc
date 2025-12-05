#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import List, NamedTuple, Tuple

from AoC.util import show


class rge(NamedTuple):
    min: int
    max: int

    def within(self, n: int) -> int:
        return self.min <= n <= self.max

    def intersects(self, other) -> bool:
        return (self.min <= other.max) and (other.min <= self.max)


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> Tuple[List[rge], List[int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        rges_str, avail_str = reader.read().split("\n\n")
    rges = [rge(*map(int, s.split("-", 1))) for s in rges_str.strip().split("\n")]
    avail = [int(s) for s in avail_str.strip().split("\n")]
    return rges, avail


@show
def first(rges: List[rge], avail: List[int]) -> int:
    return sum(any(rge.within(id) for rge in rges) for id in avail)


@show
def second(rges: List[rge], _: List[int]) -> int:
    new_rges = rges.copy()
    for r in rges:
        cur = r
        tmp = []
        for other in new_rges:
            if cur.intersects(other):
                cur = rge(min(cur.min, other.min), max(cur.max, other.max))
            else:
                tmp.append(other)
        tmp.append(cur)
        new_rges = tmp
    return sum(r.max - r.min + 1 for r in new_rges)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(*inp) == 3
        assert second(*inp) == 14


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(*inp)  # 782
    second(*inp)  # 353863745078671
