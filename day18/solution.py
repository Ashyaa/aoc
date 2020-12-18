#!/usr/bin/env python3

import operator
import shlex

from pathlib import Path
from typing import List, Tuple


CWD = Path(__file__).parent

PARENS = set('()')
OPERATORS = set('+*')
NON_NUMBERS = PARENS.union(OPERATORS)
OPERATORS_DICT = {
    '*': operator.mul,
    '+': operator.add,
}


def read_input() -> List[str]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        return reader.read().replace(" ", "").split("\n")


def compute(s: str) -> int:
    parsed_s = list(shlex.shlex(s))
    expr = [item if item in NON_NUMBERS else int(item) for item in parsed_s]
    res, _ = parse(expr, 0)
    return res


def parse(expr: List, index: int) -> Tuple[int, int]:
    op = None
    res = None
    while index < len(expr):
        item = expr[index]
        if item == ")":
            return res, index
        if item == "(":
            b, index = parse(expr, index+1)
            if res and op:
              res = op(res, b)
            else:
              res = b
        if item in OPERATORS:
            op = OPERATORS_DICT[expr[index]]
        if isinstance(item, int):
            if not res:
                res = item
            else:
                res = op(res, item)
        index+=1
    return res, index


def first(lines: List[str]) -> int:
    return sum([compute(l) for l in lines])


def add_char(c: str, l: str, index: int) -> str:
    return l[:index] + c + l[index:]


def add_parens(l: str, index: int) -> str:
    def find_index(right: bool) -> int:
        i = index + 1 if right else index - 1 
        count = 0
        while 0 <= i < len(l):
            char = l[i]
            if char in OPERATORS:
                pass
            elif char == ')':
                count+=1
            elif char == '(':
                count-=1
            if (char not in NON_NUMBERS or char in PARENS)\
                and count == 0:
                break
            i = i+1 if right else i-1
        if right:
            i+=1
        return i
    opening = find_index(False)
    closing = find_index(True)
    res = add_char(")", l, closing)
    return add_char("(", res, opening)


def apply_priority(l: str) -> str:
    nb_plus = l.count('+')
    res = l
    for count in range(nb_plus):
        found = 0
        for index, char in enumerate(res):
            if char != '+':
                continue
            else:
                found += 1
                if found > count:
                    res = add_parens(res, index)
                    break
    return res


def priority(lines: List[str]) -> List[str]:
    return [apply_priority(l) for l in lines]


def second(lines: List[str]) -> int:
    return sum([compute(l) for l in priority(lines)])


def run() -> None:
    lines = read_input()
    print("First step:") # 6923486965641
    print(first(lines))
    print("\nSecond step:")
    print(second(lines)) # ?