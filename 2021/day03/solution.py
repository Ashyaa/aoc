#!/usr/bin/env python3

import contextlib

from pathlib import Path

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[str]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [l.strip() for l in reader.readlines()]


@show
def first(inp: List[str]) -> int:
    nb_words, nb_chars = len(inp), len(inp[0])
    gamma, epsilon = 0, 0
    for col in range(nb_chars):
        digit = 1 if [word[col] for word in inp].count("1") > nb_words / 2 else 0
        gamma += digit << nb_chars - col - 1
        epsilon += (not digit) << nb_chars - col - 1
    return gamma * epsilon


@show
def second(inp: List[str]) -> int:
    def rec(inp: List[str], criteria: bool, idx: int = 0) -> str:
        if len(inp) == 1:
            return inp[0]
        nb_words = len(inp)
        nb_ones = [word[idx] for word in inp].count("1")
        if nb_ones == len(inp) / 2:
            wanted = 1 if criteria else 0
        else:
            wanted = 0 if nb_ones > nb_words / 2 else 1
            if criteria:
                wanted = int(not wanted)
        return rec(
            [word for word in inp if int(word[idx]) == wanted], criteria, idx + 1
        )

    return int(rec(inp, True), 2) * int(rec(inp, False), 2)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 198
        assert second(inp) == 230


if __name__ == "__main__":
    inp = read_input()
    test_example()
    first(inp)  # 2498354
    second(inp)  # 3277956
