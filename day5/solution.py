from functools import reduce
from pathlib import Path
from typing import List, Tuple

CWD = Path(__file__).parent

ROWS = [r for r in range(128)]
COLUMNS = [c for c in range(8)]

def read_input() -> List[str]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        return [l.strip() for l in reader.readlines()]


def get_int_rec(rows: List[int], raw:str) -> int:
    if len(rows) == 1:
        return rows[0]
    # Lower half
    if raw[0] == "F" or raw[0] == "L":
        return get_int_rec(rows[:int(len(rows)/2)] , raw[1:])
    # Upper half
    if raw[0] == "B" or raw[0] == "R":
        return get_int_rec(rows[int(len(rows)/2):] , raw[1:])


def get_row_column(raw: str) -> Tuple[int, int]:
    return get_int_rec(ROWS, raw[:7]), get_int_rec(COLUMNS, raw[7:])


def seat_id(row, col: int) -> int:
    return row * 8 + col


def first(passes: List[str]) -> int:
    coords = [get_row_column(b_pass) for b_pass in passes]
    return reduce(max, [seat_id(row, col) for row, col in coords])


def second(passes: List[str]) -> int:
    coords = [get_row_column(b_pass) for b_pass in passes]
    IDs = [seat_id(row, col) for row, col in coords]
    IDs.sort()
    for i, ID in enumerate(IDs):
        if ID + 2 == IDs[i+1]:
            return ID+1
    return -1

def run() -> None:
    passes = read_input()
    print("First step:")
    max_ID = first(passes)
    print("The highest seat ID on a boarding pass is %d!" % max_ID)
    print("\nSecond step:")
    seat_ID = second(passes)
    print("My seat ID is %d!" % seat_ID)
