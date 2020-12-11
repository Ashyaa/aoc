from pathlib import Path
from typing import List

CWD = Path(__file__).parent

class Map:
    rows: List[List[bool]] = []
    pos_x: int = 0
    pos_y: int = 0

    def __init__(self):
        pass

    def add_row(self, row: str):
        self.rows.append([c == "#" for c in row.replace('\n','')])

    def go_right(self, steps: int) -> None:
        self.pos_x = (self.pos_x + steps) % (len(self.rows[self.pos_y]))

    def go_down(self, steps: int) -> bool:
        """ Moves down by a given  number of steps and returns True if bottom reached"""
        self.pos_y += steps
        if self.pos_y >= len(self.rows) - 1:
            self.pos_y = len(self.rows) - 1
            return True
        return False

    def is_pos_tree(self) -> bool:
        return self.rows[self.pos_y][self.pos_x]

    def reset(self):
        self.pos_x = 0
        self.pos_y = 0

    def walk(self, right, down: int) -> int:
        self.reset()
        count = 0
        finished = False
        while not finished:
            self.go_right(right)
            finished = self.go_down(down)
            if self.is_pos_tree():
                count += 1
        return count


def read_input() -> Map:
    input_file = CWD.joinpath("input.txt")
    res = Map()
    with open(input_file, "r") as reader:
        for l in reader.readlines():
            res.add_row(l)
    return res


def first(map: Map) -> None:
    print("Encountered %d trees!" % map.walk(3, 1))

def second(map: Map) -> None:
    slope_1 = map.walk(1, 1)
    print("Slope n°1: %d trees" % slope_1)
    slope_2 = map.walk(3, 1)
    print("Slope n°2: %d trees" % slope_2)
    slope_3 = map.walk(5, 1)
    print("Slope n°3: %d trees" % slope_3)
    slope_4 = map.walk(7, 1)
    print("Slope n°4: %d trees" % slope_4)
    slope_5 = map.walk(1, 2)
    print("Slope n°5: %d trees" % slope_5)
    product = slope_1 * slope_2 * slope_3 * slope_4 * slope_5
    print(f"Result = {slope_1} * {slope_2} * {slope_3} * {slope_4} * {slope_5}"
          f" = {product}")

def run() -> None:
    tree_map = read_input()
    print("First step:")
    first(tree_map)
    print("\nSecond step:")
    second(tree_map)
