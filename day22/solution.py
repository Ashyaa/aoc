from copy import copy
from pathlib import Path
from typing import List,Tuple

CWD = Path(__file__).parent


def deck(raw: str) -> List[int]:
    return [int(s) for s in raw.split("\n")[1:]]


def read_input(filename: str="input.txt") -> Tuple[List[int],List[int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        p1, p2 = reader.read().split("\n\n", maxsplit=1)
        return deck(p1), deck(p2)


def play_combat(p1: List[int], p2: List[int]) -> Tuple[List[int],List[int]]:
    while len(p1) > 0 and len(p2) > 0:
        p1_card, p2_card = p1.pop(0), p2.pop(0)
        if p1_card > p2_card:
            p1.extend([p1_card, p2_card])
        else:
            p2.extend([p2_card, p1_card])
    return p1, p2


def score(deck: List[int]) -> int:
    nb = len(deck)
    return sum([c * (nb-i) for i, c in enumerate(deck)])


def first(p1: List[int], p2: List[int]) -> int:
    p1, p2 = play_combat(p1, p2)
    if p1:
        return score(p1)
    return score(p2)


def play_rec_combat(p1: List[int], p2: List[int]) -> Tuple[List[int],List[int], bool]:
    history_p1 = set()
    history_p2 = set()
    while len(p1) > 0 and len(p2) > 0:
        turn_p1 = ' '.join([str(n) for n in p1])
        turn_p2 = ' '.join([str(n) for n in p2])
        if turn_p1 in history_p1 and turn_p2 in history_p2:
            return p1, p2, True
        history_p1.add(turn_p1)
        history_p2.add(turn_p2)
        p1_card, p2_card = p1.pop(0), p2.pop(0)
        p1_winner = False
        if len(p1) >= p1_card and len(p2) >= p2_card:
            _,_, p1_winner = play_rec_combat(p1[:p1_card], p2[:p2_card])
        else:
            p1_winner = p1_card > p2_card
        if p1_winner:
            p1.extend([p1_card, p2_card])
        else:
            p2.extend([p2_card, p1_card])
    return p1, p2, len(p2) == 0


def second(p1: List[int], p2: List[int]) -> int:
    p1, p2, p1_winner = play_rec_combat(p1, p2)
    if p1_winner:
        return score(p1)
    return score(p2)


def test_example() -> None:
    p1, p2 = read_input("example.txt")
    assert first(copy(p1), copy(p2)) == 306
    assert second(p1, p2) == 291


def run() -> None:
    test_example()
    p1, p2 = read_input()
    print("First step:")
    print(first(copy(p1), copy(p2)))  # 35005
    print("\nSecond step:")
    print(second(p1, p2)) # 32751