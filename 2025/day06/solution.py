#!/usr/bin/env python3

import contextlib
from functools import reduce
from pathlib import Path
from typing import List, Tuple

from AoC.util import show

CWD = Path(__file__).parent

OP = {
    "*": lambda x, y: x * y,
    "+": lambda x, y: x + y,
}


def read_input(filename: str = "input.txt") -> Tuple[List[str], List[str]]:
    input_file = CWD.joinpath(filename)
    res = []
    with open(input_file, "r") as reader:
        for line in reader.readlines():
            res.append(line)
    return res[:-1], res[-1].strip().split()


@show
def first(numbers: List[str], operators: List[str]) -> int:
    res = 0
    nbs = [list(map(int, line.strip().split())) for line in numbers]
    for i, op in enumerate(operators):
        res += reduce(OP[op], (number[i] for number in nbs))
    return res


def str_to_numbers(read_nbs: List[str]) -> List[int]:
    res = []
    max_len = max(len(n) for n in read_nbs)
    padded = [n + " " * (max_len - len(n)) for n in read_nbs]
    for idx in range(len(padded[0])):
        s = ""
        for nb in padded:
            s += nb[idx] if nb[idx] != " " else ""
        if s:
            res.append(int(s))
    return res


def p2_numbers(numbers: List[str], cur_idx: List[int]) -> Tuple[List[int], List[int]]:
    res, new_idx = [], []
    max_start_idx = max(cur_idx)
    for i, line in enumerate(numbers):
        start_idx = cur_idx[i]
        found = False
        s = ""
        for idx in range(start_idx, len(line)):
            char = line[idx]
            s += char if idx >= max_start_idx else ""
            if char == " " and found:
                new_idx.append(idx)
                res.append(s)
                break
            if char != " ":
                found = True
    return str_to_numbers(res), new_idx


@show
def second(numbers: List[str], operators: List[str]) -> int:
    res = 0
    cur_idx = [0] * len(numbers)
    max_len = max(len(n) for n in numbers)
    ltr_numbers = [
        (" " + n.replace("\n", "") + " " * (max_len - len(n)))[::-1] for n in numbers
    ]
    for op in reversed(operators):
        nbs, cur_idx = p2_numbers(ltr_numbers, cur_idx)
        res += reduce(OP[op], nbs)
    return res


def test_example() -> None:
    inp = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        assert first(*inp) == 4277556
        assert second(*inp) == 3263827


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(*inp)  # 5595593539811
    second(*inp)  # 10153315705125
