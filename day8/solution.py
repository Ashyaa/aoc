import copy
from pathlib import Path
from typing import List, Tuple


CWD = Path(__file__).parent


OPERATORS = {
  "nop": lambda n: lambda index, count: (index+1, count),
  "acc": lambda n: lambda index, count: (index+1, count+n),
  "jmp": lambda n: lambda index, count: (index+n, count),
}


def read_input() -> List[Tuple[str, int]]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        tmp = [l.split(" ") for l in reader.read().rstrip().split("\n")]
        return [(f, int(arg)) for f, arg in tmp]


def first(code: List[Tuple[str, int]], index: int, counter: int) -> Tuple[int, bool]:
    visited = set()
    while 0 <= index < len(code) and index not in visited:
        visited.add(index)
        op, arg = code[index]
        index, counter = OPERATORS[op](arg)(index, counter)
    return counter, index >= len(code)


def second(code: List[Tuple[str, int]]) -> int:
    visited, index, counter = set(), 0, 0
    while index not in visited or index >= len(code):
        visited.add(index)
        op, arg = code[index]
        res, unlooped = 0, False
        if op != "acc":
            alt_code = copy.copy(code)
            alt_code[index] = ("jmp" if op == "nop" else "nop", code[index][1])
            res, unlooped = first(alt_code, index, counter)
        if unlooped:
            return res
        index, counter = OPERATORS[op](arg)(index, counter)


def run() -> None:
    rules = read_input()
    print("First step:")
    print(first(rules, 0, 0))
    print("\nSecond step:")
    print(second(rules))