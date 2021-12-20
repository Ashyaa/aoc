#!/usr/bin/env python3

"""
This implementation relies on the fact that if two scanner boxes match, the distance between
their common beacons will always be the same. So we proceed to find, for each axis, the proper
rotation. Working on each axis separately works: if one does not match, it's enough to say the
two boxes can't match. If they do, all 3 axes will match separately.
When rotating, each axis can end up being negated, so there are only 6 permutations to consider.
"""

import contextlib
from collections import Counter
from itertools import product
from pathlib import Path
from typing import *

from AoC.util import show

CWD = Path(__file__).parent

Position = Tuple[int,int,int]
Scanner = List[Position]


def read_input(filename: str = "input.txt") -> List[Scanner]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = []
        for l in reader.readlines():
            if l.startswith("--"):
                res.append([])
            elif l.strip() == "":
                continue
            else:
                res[-1].append(tuple([int(n) for n in l.strip().split(",")]))
        return res


AXIS_PERMUTATIONS = list(product(range(0,3), [1, -1]))


def match(a: Scanner, b: Scanner) -> Tuple[Union[None, Scanner], Position]:
    res, b_pos = [], [-1]*3
    b_ax, found_ax = [], set()
    distance, count, b_idx = 0, 0, 0
    # for each axis of a
    for a_idx in range(3):
        a_ax = [beacon[a_idx] for beacon in a] # axis n°a_idx in a
        # for each axis of b, possibly negated
        for b_idx, factor in AXIS_PERMUTATIONS:
            if b_idx in found_ax:
                # an axis can only be matched once, skip it if it was already matched
                continue
            b_ax = [beacon[b_idx] * factor for beacon in b] # axis n°b_idx in b, negated if needed
            # compute distance between each partial beacons of a and b
            distances =  [bcb-bca for bca, bcb in product(a_ax, b_ax)]
            distance, count = Counter(distances).most_common(1)[0]
            if count >= 12:
                # if a single distance was found 12 times or more, it's the offset on
                # the current axis between the two scanners, meaning that we have a match
                break
        if count < 12:
            # the axis does not match, meaning the two scanner boxes can't match
            return None, (-1,-1,-1)
        # save the previously found axis for later iterations
        found_ax.add(b_idx)
        # shift the axis of b to absolute coordinates using the distance between scanners
        res.append([bc - distance for bc in b_ax])
        # save the scanner coordinate
        b_pos[a_idx] = distance
    # zip the 3 axis together to return the absolute version of b, along with the absolute position of b
    return list(zip(res[0], res[1], res[2])), tuple(b_pos) # type: ignore


@show
def first(inp: List[Scanner]) -> Tuple[int, int]:
    # part 1
    fifo, not_found, =  inp[:1], inp[1:]
    res = set(fifo[0])
    positions: List[Position] = [(0,0,0)] # first center
    while fifo:
        ref = fifo.pop()
        tmp = []
        for b in not_found:
            rotated_b, pos = match(ref, b)
            if rotated_b:
                fifo.append(rotated_b)
                positions.append(pos)
                res |= set(rotated_b)
            else:
                tmp.append(b)
        not_found = tmp

    # part 2
    distances = []
    for i, scanner_1 in enumerate(positions[:-1]):
        for scanner_2 in positions[i+1:]:
            distances.append(sum(abs(x2 - x1) for x1, x2 in zip(scanner_1, scanner_2)))
    return len(res), max(distances)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == (79, 3621)


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 400, 12168
