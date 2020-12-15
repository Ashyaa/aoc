from pathlib import Path
from typing import List


CWD = Path(__file__).parent


def read_input() -> List[int]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        return [int(n) for n in reader.readline().split(",")]


def pipe(n: int, numbers: List[int]) -> List[int]:
    res = numbers + [n]
    if len(res) > 2:
        res = res[1:]
    return res


def play(ins: List[int], max_turn: int) -> int:
    game = {n: index for index, n in enumerate(ins)}
    turn = len(ins) - 1
    last_said = ins[-1]
    while turn < max_turn-1:
        if last_said in game:
            v = turn - game[last_said]
        else:
            v = 0
        game[last_said] = turn
        last_said = v
        turn += 1
    return last_said


def first(ins: List[int]) -> int:
    return play(ins, 2020)


def second(ins: List[int]) -> int:
    return play(ins, 30000000)


def run() -> None:
    ins = read_input()
    print("First step:", first(ins)) # 257
    print("\nSecond step:", second(ins)) # 8546398
