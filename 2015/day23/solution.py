#!/usr/bin/env python3

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


INSTRUCTIONS = {
    "hlf": lambda r, o, s_p: (r//2, s_p+1),
    "tpl": lambda r, o, s_p: (r*3, s_p+1),
    "inc": lambda r, o, s_p: (r+1, s_p+1),
    "jmp": lambda r, o, s_p: (r, s_p+o),
    "jie": lambda r, o, s_p: (r, s_p+o if r % 2 == 0 else s_p+1),
    "jio": lambda r, o, s_p: (r, s_p+o if r == 1 else s_p+1),
}


def get_op(name: str, args: List[str]) -> Tuple[str, bool, int]:
    if name == "jmp":
        return name, False, int(args[0])
    if name in ["jie", "jio"]:
        return name, args[0]=="a", int(args[1])
    return name, args[0]=="a", 0


def read_input(filename: str="input.txt") -> List[Tuple[str, bool, int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = []
        for l in reader.readlines():
            op, tmp = l.strip().split(" ", maxsplit=1)
            res.append(get_op(op, tmp.split(", ")))
        return res


@show
def run(stack: List[Tuple[str, bool, int]], p2: bool=False) -> int:
    a = b = s_p = 0
    if p2: a = 1
    while 0 <= s_p < len(stack):
        op, reg_a, offset = stack[s_p]
        if reg_a:
            a, s_p = INSTRUCTIONS[op](a, offset, s_p)
        else:
            b, s_p = INSTRUCTIONS[op](b, offset, s_p)
    return b


stack = read_input()
run(stack) # 255
run(stack, True) # p2