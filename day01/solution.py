from pathlib import Path
from typing import List

CWD = Path(__file__).parent

def read_input() -> List[int]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        return [int(l) for l in reader.readlines()]

def first(numbers: List[int], element: int) -> bool:
    for i, n in enumerate(numbers):
        for j in range(i+1, len(numbers)):
            m = numbers[j]
            if element + n + m == 2020:
                print(f"{element} + {n} + {m} = {element + n + m}")
                print(f"{element} * {n} * {m} = {element * n * m}")
                return True
    return False

def second(numbers: List[int]) -> None:
    for i, n in enumerate(numbers):
        if first(numbers[i+1:], n):
            pass
            # break

def run() -> None:
    numbers = read_input()
    print("First step:")
    first(numbers, 0)
    print("\nSecond step:")
    second(numbers)
