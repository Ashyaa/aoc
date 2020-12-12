from pathlib import Path
from typing import List, Tuple

CWD = Path(__file__).parent

CARDINALS = ['N', 'E', 'S', 'W']
TURNS = set(['L', 'R'])


class Boat:
    direction: int = 1
    ns: int = 0
    ew: int = 0
    has_wp = False
    wp_ns: int = 1
    wp_ew: int = 10


    def __init__(self, has_wp: bool = False):
        self.has_wp = has_wp


    def rotate(self, side: str, angle: int) -> None:
        sign = 1 if side == 'R' else -1
        shift = angle // 90
        if self.has_wp:
            for _ in range(shift):
                self.wp_ns, self.wp_ew = -1 * sign * self.wp_ew, sign * self.wp_ns
        else:
            self.direction = (self.direction + sign * shift) % 4


    def move(self, act: str, v: int) -> None:
        if act in TURNS:
            self.rotate(act, v)
            return
        if act == "F":
            if self.has_wp:
                self.to_wp(v)
                return
            act = CARDINALS[self.direction]
        index = CARDINALS.index(act)
        sign = 1 if index < 2 else -1
        self.translate(index % 2 == 0, self.has_wp, sign*v)


    def translate(self, ns: bool, wp: bool, v: int) -> None:
        if wp:
            if ns:
                self.wp_ns += v
            else:
                self.wp_ew += v
        else:
            if ns:
                self.ns += v
            else:
                self.ew += v


    def to_wp(self, count: int) -> None:
        for _ in range(count):
            self.ns += self.wp_ns
            self.ew += self.wp_ew


def read_input() -> List[Tuple[str,int]]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        for l in reader.readlines():
            yield l[0], int(l[1:])


def first(actions: List[Tuple[str,int]]) -> int:
    b = Boat()
    for a, v in actions:
        b.move(a, v)
    return abs(b.ns) + abs(b.ew)


def second(actions: List[Tuple[str,int]]) -> None:
    b = Boat(has_wp = True)
    for a, v in actions:
        b.move(a, v)
    return abs(b.ns) + abs(b.ew)


def run() -> None:
    actions = list(read_input())
    print("First step:")
    # 1152
    print(first(actions))
    print("\nSecond step:")
    # 58637
    print(second(actions))
