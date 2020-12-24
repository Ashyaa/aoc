from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Tuple

CWD = Path(__file__).parent

EW_AXIS = ["w", "e"]
NE_SW_AXIS = ["ne", "sw"]
NW_SE_AXIS = ["nw", "se"]


def get_move(coord: str) -> Tuple[int,int]:
    if coord == "e":
        return 1, 0
    if coord == "w":
        return -1, 0
    y = 0.5
    if coord.startswith("s"):
        y = -0.5
    x = 0.5
    if coord.endswith("w"):
        x = -0.5
    return x, y


def parse_line(l: str) -> Tuple[int, int]:
    res = [0, 0]
    while l != "":
        nb_char = 1
        if l.startswith("n") or l.startswith("s"):
            nb_char = 2
        x, y = get_move(l[:nb_char])
        res[0] += x
        res[1] += y
        l = l[nb_char:]
    return tuple(res)


def read_input(filename: str="input.txt") -> List[Tuple[int, int, int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [parse_line(l.strip()) for l in reader.readlines()]


def first(tiles: List[Tuple[int, int, int]]) -> int:
    pavement = defaultdict(bool)
    for t in tiles:
        pavement[t] = not pavement[t]
    return sum([p for p in pavement.values()])


class Matrix:
    state: Dict[Tuple[int,int],bool]
    next_state: Dict[Tuple[int,int],bool]
    neighbours = [(1,0), (-1,0), (0.5,0.5), (0.5,-0.5), (-0.5,0.5), (-0.5,-0.5)]

    def __init__(self, init_state: Dict[Tuple[int,int],bool]):
        self.state = init_state


    def populate(self):
        tiles = list(self.state.keys())
        for x, y in tiles:
            nts = [(x+dx, y+dy) for dx, dy in self.neighbours]
            for nt in nts:
                if nt not in self.state:
                    self.state[nt] = False


    def run(self) -> None:
        self.populate()
        tiles = list(self.state.keys())
        self.next_state = defaultdict(bool)
        for x, y in tiles:
            cur_tile = self.state[(x,y)]
            nts = [(x+dx, y+dy) for dx, dy in self.neighbours]
            nb_black = sum([self.state[nt] for nt in nts])
            if cur_tile and (nb_black == 0 or nb_black > 2):
                self.next_state[(x,y)] = False
                continue
            if not cur_tile and nb_black == 2:
                self.next_state[(x,y)] = True
                continue
            self.next_state[(x,y)] = cur_tile
        self.state = self.next_state


def second(tiles: List[Tuple[int, int, int]], turns: int=100) -> None:
    pavement = defaultdict(bool)
    for t in tiles:
        pavement[t] = not pavement[t]
    m = Matrix(pavement)
    for _ in range(turns):
        m.run()
    return sum([p for p in m.state.values()])


def test_example() -> None:
    ins = read_input("example.txt")
    assert parse_line("esew") == (0.5,-0.5)
    assert parse_line("nwwswee") == (0,0)
    assert first(ins) == 10
    assert second(ins, 10) == 37
    assert second(ins, 50) == 566
    assert second(ins) == 2208


def run() -> None:
    test_example()
    ins = read_input()
    print("First step:")
    print(first(ins)) # step1
    print("\nSecond step:")
    print(second(ins)) # step2
