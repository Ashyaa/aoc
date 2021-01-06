#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import Dict
from AoC.util import show


CWD = Path(__file__).parent


GATES = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "LSHIFT": lambda x, y: x << y,
    "RSHIFT": lambda x, y: x >> y,
    "NOT": lambda x, y: ~x & 0xFFFF,
    "ID": lambda x, y: x,
}

class Gate:
    def __init__(self, raw: str):
        fragments = raw.split(" ")
        self.arg = 0
        if len(fragments) == 1:
            self.op = "ID"
            self.source = raw
        if len(fragments) == 2:
            self.op = "NOT"
            self.source = fragments[1]
        if len(fragments) == 3:
            self.op = fragments[1]
            self.source = fragments[0]
            self.arg = fragments[2]
        try:
            self.source = int(self.source)
        except ValueError:
            pass
        try:
            self.arg = int(self.arg)
        except ValueError:
            pass


def read_input(filename: str="input.txt") -> Dict[str, Gate]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        circuit = {}
        for l in reader.readlines():
            gate, output = l.strip().split(" -> ", maxsplit=1)
            circuit[output] = Gate(gate)
        return circuit


def compute(circuit: Dict[str, Gate], memory: Dict[str, int], wire: str) -> int:
    g = circuit[wire]
    src = g.source
    if not isinstance(src, int):
        if g.source in memory:
            src = memory[g.source]
        else:
            src = compute(circuit, memory, src)
            memory[g.source] = src
    arg = g.arg
    if not isinstance(arg, int):
        if g.arg in memory:
            arg = memory[g.source]
        else:
            arg = compute(circuit, memory, arg)
            memory[g.source] = src
    res = GATES[g.op](src, arg)
    return res


@show
def first(circuit: Dict[str, Gate]) -> int:
    memory = {}
    return compute(circuit, memory, "a")


@show
def second(circuit: Dict[str, Gate], sig: int) -> int:
    memory = {}
    circuit["b"].source = sig
    return compute(circuit, memory, "a")


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        ex = read_input("example.txt")
        assert compute(ex, {}, "d") == 72
        assert compute(ex, {}, "e") == 507
        assert compute(ex, {}, "f") == 492
        assert compute(ex, {}, "g") == 114
        assert compute(ex, {}, "h") == 65412
        assert compute(ex, {}, "i") == 65079
        assert compute(ex, {}, "x") == 123
        assert compute(ex, {}, "y") == 456


test_example()
circuit = read_input()
sig = first(circuit) # 956
second(circuit, sig) # 40149