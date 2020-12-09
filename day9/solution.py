import copy
from pathlib import Path
from typing import List

CWD = Path(__file__).parent


def read_input() -> List[int]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        return [int(l) for l in reader.read().rstrip().split("\n")]


def pipe(n: int, numbers: List[int]) -> List[int]:
    return numbers[1:] + [n]


def is_valid(n: int, numbers: List[int]) -> bool:
    for i in numbers:
        if n != 2*i and n - i in numbers:
            return True
    return False

def first(numbers: List[int]) -> int:
    preamble = numbers[:25]
    for n in numbers[25:]:
        if not is_valid(n, preamble):
            return n
        preamble = pipe(n, preamble)

def second(numbers: List[int], target: int) -> int:
    sublist, acc = [], 0
    for n in numbers:
        if n >= target:
            sublist, acc = [], 0
            continue
        acc += n
        sublist.append(n)
        if acc == target:
            return min(sublist) + max(sublist)
        while acc > target:
            acc -= sublist[0]
            sublist = sublist[1:]


def run() -> None:
    numbers = read_input()
    print("First step:")
    # 14360655
    res =first(numbers)
    print(res)
    print("\nSecond step:")
    # 1962331
    print(second(numbers, res))