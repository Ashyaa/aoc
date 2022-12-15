#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import Iterable, List, Dict, Tuple
from AoC.util import show


CWD = Path(__file__).parent


def parse_coord(s: str) -> Tuple[int, int]:
    tmp = s.split(", ")
    return int(tmp[0][2:]), int(tmp[1][2:])


def read_input(filename: str = "input.txt") -> Dict[Tuple[int, int],Tuple[int, int]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        res = {}
        for l in reader.readlines():
            tmp = l.strip().split(":")
            res[parse_coord(tmp[0][10:])] = parse_coord(tmp[1][22:])
        return res


def distance(c1: Tuple[int,int], c2: Tuple[int,int]) -> int:
    return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1])


def merge(arr: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    arr.sort(key=lambda c: c[0])
    res = [arr[0]]
    arr = arr[1:]
    while arr:
        elt = arr[0]
        arr = arr[1:]
        if res[-1][1] >= elt[0] - 1:
            res[-1] = min(res[-1][0], elt[0]), max(res[-1][1], elt[1])
        else:
            res.append(elt)
    return res


def no_beacons(d:  Dict[Tuple[int, int],Tuple[int, int]], row: int) -> List[Tuple[int, int]]:
  res = []
  for s, b in d.items():
      dist = distance(s,b)
      dist_y = distance(s, (s[0], row))
      if dist_y > dist or b == (s[0], row):
          continue
      dist_x = dist - dist_y 
      mi, ma = s[0]-dist_x, s[0]+dist_x
      if b[1] == row:
          if b[0] == mi:
              mi = mi+1
          elif b[0] == ma:
              ma = ma-1
      res.append((mi,ma))
  return merge(res)


@show
def first(d:  Dict[Tuple[int, int],Tuple[int, int]], row: int = 2000000) -> int:
    return sum(abs(c[0]-c[1])+1 for c in no_beacons(d, row))


def perimeter(s: Tuple[int, int], b: Tuple[int, int], limit: int) -> Iterable[Tuple[int,int]]:
    d = distance(s, b) + 1
    ok = lambda p: 0 <= p[0] <= limit and 0 <= p[1] <= limit
    for n in range(d+1):
        for dx, dy in [(n,d-n), (-n,n-d), (d-n, n), (n-d, n)]:
            p = s[0]+dx, s[1]+dy
            if ok(p):
              yield p


def candidates(d: Dict[Tuple[int, int],Tuple[int, int]], limit: int) -> Iterable[Tuple[int,int]]:
    for s, b in d.items():
        for c in perimeter(s, b, limit):
          yield c


@show
def second(d: Dict[Tuple[int, int],Tuple[int, int]], limit: int = 4000000) -> int:
    for c in candidates(d, limit):
        ok = True
        for s, b in d.items():
            if distance(s,c) <= distance(s,b):
                ok = False
                break
        if ok:
            return c[0]*4000000+c[1]
    return 0


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp, 10)
        assert r1 == 26, r1
        r2  = second(inp, 20)
        assert r2 == 56000011, r2


test_example()
s = read_input()
first(s)  # 5040643
second(s)  # 11016575214126
