#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[str]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return reader.read().split('\n')


def draw(cyc: int, val: int) -> str:
    res = " "
    if val-1 <= cyc % 40 <= val+1:
        res = "#"
    if cyc % 40 == 39:
        res += "\n"
    return res


@show
def run(lines: List[str]) -> Tuple[int, str]:
    cyc, x = 0, 1
    res = 0
    crt = ""
    for l in lines:
        if (cyc + 1) % 40 == 20:
            res += x * (cyc+1)
        if l.startswith('noop'):
            crt += draw(cyc, x)
            cyc += 1
            continue
        val = int(l.split()[1])
        if (cyc + 2) % 40 == 20:
            res += x * (cyc+2)
        crt += draw(cyc, x)
        cyc += 1
        crt += draw(cyc, x)
        cyc += 1
        x += val
    return res, crt



def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        with open(CWD.joinpath("expected.txt"), "r", encoding="utf-8") as reader:
            crt = reader.read()
        r1  = run(inp)
        assert r1 == (13140, crt), r1


test_example()
s = read_input()
res = run(s)  # 15020
print(res[1])
