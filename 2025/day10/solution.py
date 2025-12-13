#!/usr/bin/env python3

import contextlib
from collections import defaultdict
from functools import cache
from itertools import combinations, product
from pathlib import Path
from typing import List, Tuple

from AoC.util import show

CWD = Path(__file__).parent

Pattern = List[bool]
Button = Joltage = Tuple[int]
Buttons = List[Button]
Line = Tuple[Pattern, Buttons, Joltage]


def read_input(filename: str = "input.txt") -> List[Line]:
    input_file = CWD.joinpath(filename)
    res = []
    with open(input_file, "r") as reader:
        for line in reader.readlines():
            a, b = line.index("]"), line.index("{")
            pattern = [c == "#" for c in line[1:a]]
            buttons = [tuple(map(int, btn[1:-1].split(","))) for btn in line[a + 2 : b - 1].split()]
            joltage = tuple(map(int, line.strip()[b + 1 : -1].split(",")))
            res.append((pattern, buttons, joltage))
    return res


@show
def first(inp: List[Line]) -> int:
    res = 0
    for pattern, buttons, _ in inp:

        def solves(n: int) -> bool:
            for c in combinations(buttons, n):
                cur = [False] * len(pattern)
                for btn in c:
                    for idx in btn:
                        cur[idx] = not cur[idx]
                if cur == pattern:
                    return True
            return False

        res += next(i for i in range(1, 10) if solves(i))
    return res


@show
def second(inp: List[Line]) -> int:
    res = 0
    for _, buttons, joltage in inp:
        jolt_per_press, patterns = {}, defaultdict(list)

        for pressed in product((0, 1), repeat=len(buttons)):
            jolt = [0] * len(joltage)
            for i, p in enumerate(pressed):
                for j in buttons[i]:
                    jolt[j] += p
            jolt_per_press[pressed] = jolt
            patterns[tuple(x % 2 for x in jolt)] += [pressed]

        @cache
        def solve(joltage: Joltage) -> int:
            if all(x == 0 for x in joltage):
                return 0
            if any(x < 0 for x in joltage):
                return 1 << 63

            nb_pressed, lights = 1 << 63, tuple(x % 2 for x in joltage)
            for pressed in patterns[lights]:
                jolt_diff = jolt_per_press[pressed]
                new_joltage = tuple((tot - diff) // 2 for diff, tot in zip(jolt_diff, joltage))
                nb_pressed = min(nb_pressed, sum(pressed) + 2 * solve(new_joltage))
            return nb_pressed

        res += solve(joltage)
    return res


def test_example() -> None:
    inp = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        assert first(inp) == 7
        assert second(inp) == 33


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 452
    second(inp)  # 17424
