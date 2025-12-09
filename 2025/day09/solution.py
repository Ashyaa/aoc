#!/usr/bin/env python3

import bisect
import contextlib
from itertools import combinations
from pathlib import Path
from typing import List, Tuple

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[Tuple[int, ...]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [tuple(map(int, line.strip().split(","))) for line in reader.readlines()]


@show
def first(inp: List[Tuple[int, ...]]) -> int:
    return max(abs(x1 - x2 + 1) * abs(y1 - y2 + 1) for (x1, y1), (x2, y2) in combinations(inp, 2))


def is_rectangle_inscribed(
    rectangle: Tuple[int, int, int, int],
    h_edges: List[Tuple[int, int, int]],
    v_edges: List[Tuple[int, int, int]],
    h_edge_ys: List[int],
    v_edge_xs: List[int],
) -> bool:
    x1, y1, x2, y2 = rectangle

    for i in range(bisect.bisect_right(h_edge_ys, y1), bisect.bisect_left(h_edge_ys, y2)):
        hx1, hx2, _ = h_edges[i]
        if hx1 < x2 <= hx2 or hx1 <= x1 < hx2:
            return False

    for i in range(bisect.bisect_right(v_edge_xs, x1), bisect.bisect_left(v_edge_xs, x2)):
        vy1, vy2, _ = v_edges[i]
        if vy1 < y2 <= vy2 or vy1 <= y1 < vy2:
            return False

    return True


@show
def solve(inp: List[Tuple[int, ...]]) -> Tuple[int, int]:
    rect_areas = []
    for (x1, y1), (x2, y2) in combinations(inp, 2):
        rect_areas.append(((x1, y1), (x2, y2), abs(x1 - x2 + 1) * abs(y1 - y2 + 1)))
    rect_areas.sort(key=lambda item: item[2], reverse=True)

    p1 = rect_areas[0][2]

    h_edges, v_edges = [], []
    for i, (x1, y1) in enumerate(inp):
        x2, y2 = inp[(i + 1) % len(inp)]
        if x1 == x2:
            v_edges.append((min(y1, y2), max(y1, y2), x1))
        else:
            h_edges.append((min(x1, x2), max(x1, x2), y1))

    h_edges.sort(key=lambda item: item[2])
    h_edge_ys = [h[2] for h in h_edges]

    v_edges.sort(key=lambda item: item[2])
    v_edge_xs = [v[2] for v in v_edges]

    for (x1, y1), (x2, y2), area in rect_areas:
        rectangle = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

        if is_rectangle_inscribed(rectangle, h_edges, v_edges, h_edge_ys, v_edge_xs):
            p2 = area
            break

    return p1, p2


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert solve(inp) == (50, 24)


if __name__ == "__main__":
    test_example()
    inp = read_input()
    solve(inp)  # 4777967538, 1439894345
