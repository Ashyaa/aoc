#!/usr/bin/env python3

import contextlib

from pathlib import Path

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


class Scanner:
    x: int
    y: int
    z: int
    beacons: List[Tuple[int, int, int]]
    distances: Dict[Tuple[int, int], Tuple[int, int, int]]

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.z = 0
        self.beacons = []
        self.distances = {}

    def compute_distances(self):
        for i in range(len(self.beacons) - 1):
            x1, y1, z1 = self.beacons[i]
            for j in range(i + 1, len(self.beacons)):
                x2, y2, z2 = self.beacons[j]
                dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
                self.distances[(i, j)] = (dx, dy, dz)
                self.distances[(j, i)] = (-dx, -dy, -dz)

    def rotate(self, x: int, y: int, z: int) -> None:
        for i in range(len(self.beacons)):
            self.beacons[i] = rot_xyz(self.beacons[i], x, y, z)
        for k in self.distances.keys():
            self.distances[k] = rot_xyz(self.distances[k], x, y, z)

    def set_pos(self, x: int, y: int, z: int, i: int):
        dx, dy, dz = self.beacons[i]
        self.x = x - dx
        self.y = y - dy
        self.z = z - dz
        # print(x, y, z)
        # print(dx, dy, dz)
        print("scanner found:", self.x, self.y, self.z)
        print()
        # input()

    def abs_beacon(self, i: int) -> Tuple[int, int, int]:
        dx, dy, dz = self.beacons[i]
        return self.x + dx, self.y + dy, self.z + dz

    def abs_beacons(self) -> List[Tuple[int, int, int]]:
        return [self.abs_beacon(i) for i in range(len(self.beacons))]


rot_x = lambda x, y, z: (x, -z, y)
rot_y = lambda x, y, z: (-z, y, x)
rot_z = lambda x, y, z: (-y, x, z)


def rot_xyz(node: Tuple[int, int, int], x: int, y: int, z: int) -> Tuple[int, int, int]:
    res = node
    for _ in range(x):
        res = rot_x(*res)
    for _ in range(y):
        res = rot_y(*res)
    for _ in range(z):
        res = rot_z(*res)
    return res


def read_input(filename: str = "input.txt") -> List[Scanner]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = []
        for l in reader.readlines():
            if l.startswith("--"):
                res.append(Scanner())
            elif l.strip() == "":
                res[-1].compute_distances()
            else:
                res[-1].beacons.append(tuple([int(n) for n in l.strip().split(",")]))
        return res


ROTATIONS = [
    (0, 0, 0),
    (1, 0, 0),
    (2, 0, 0),
    (3, 0, 0),
    (0, 0, 1),
    (0, 1, 1),
    (0, 2, 1),
    (0, 3, 1),
    (0, 0, 2),
    (1, 0, 2),
    (2, 0, 2),
    (3, 0, 2),
    (0, 0, 3),
    (0, 1, 3),
    (0, 2, 3),
    (0, 3, 3),
    (0, 1, 0),
    (0, 1, 1),
    (0, 1, 2),
    (0, 1, 0),
    (0, 3, 0),
    (0, 3, 1),
    (0, 3, 2),
    (0, 3, 0),
]


def match(a: Scanner, b: Scanner) -> Tuple[bool, Tuple[int, int], Tuple[int, int, int]]:
    """[summary]

    Args:
        a (Scanner): scanner in absolute pos
        b (Scanner): scanner in relative pos

    Returns:
        Tuple[bool, Tuple[int, int], Tuple[int, int, int]]: match found, (common beacon index in a and b), (rotation applied to b)
    """
    scan1 = (a.x, a.y, a.z) == (68, -1246, -43)
    scan4 = b.beacons[0] == (727, 592, 562)
    pr = scan1 and scan4
    if pr:
        print("scanner 1 found and trying to match with scanner 4")
        print(len(a.beacons), len(b.beacons))
        # input()
    for rx, ry, rz in ROTATIONS:
        matching = set()
        # if pr:
        #     print("rotation:", rx, ry, rz)
        #     print()
        for (i, j), (dxa, dya, dza) in a.distances.items():
            # if pr:
            #     print(f"distance in a ({i},{j}):", dxa, dya, dza)
            for (m, n), coord in b.distances.items():
                cx, cy, cz = rot_xyz(coord, rx, ry, rz)
                if pr:
                    print(f"distance in b ({m},{n}):", cx, cy, cz)
                if dxa == cx and dya == cy and dza == cz:
                    # input()
                    matching.add(i)
                    matching.add(j)
                if len(matching) >= 12:
                    if pr:
                        input("match found")
                    return True, (i, m), (rx, ry, rz)
    # exit(-1)
    return False, (-1, -1), (-1, -1, -1)


@show
def first(inp: List[Scanner]) -> int:
    found = inp[:1]
    not_found = inp[1:]
    res = set(found[0].beacons)
    i = 0
    while len(found) != len(inp):
        print("found scanners:")
        for s in found:
            print(s.x, s.y, s.z, s.beacons[0])
        print("not found scanners:")
        for s in not_found:
            print(s.x, s.y, s.z, s.beacons[0])
        print()
        ref = found[i]

        match_found = False
        tmp = []
        for b in not_found:
            match_found, idx, rot = match(ref, b)
            if match_found:
                b.rotate(*rot)
                b.set_pos(*(ref.abs_beacon(idx[0])), idx[1])
                found.append(b)
                res |= set(b.abs_beacons())
            else:
                tmp.append(b)
        not_found = tmp
        i += 1
    return len(res)


@show
def second(inp) -> None:
    pass


def test_example() -> None:
    inp = read_input("example.txt")
    assert first(inp) == 79
    with contextlib.redirect_stdout(None):
        assert second(inp) == None


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # p1
    second(inp)  # p2
