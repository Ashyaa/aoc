#!/usr/bin/env python3

import contextlib
from functools import reduce
from pathlib import Path
from typing import *

from AoC.util import show

CWD = Path(__file__).parent


class Snailfish:
    l: Union[int, "Snailfish"]
    r: Union[int, "Snailfish"]


    def __init__(self, l: Union[int, "Snailfish"], r: Union[int, "Snailfish"]) -> None:
        self.l = l
        self.r = r


    def __add__(self, other):
        res = Snailfish(self, other)
        res.reduce()
        return res


    def explode(self) -> bool:
        lvl,s = 0, str(self)
        stack, st_l, st_exp = [], [], []
        begin, end = -1, -1
        for i, c in enumerate(s):
            if c == '[':
                lvl += 1
                stack.append(False)
                if lvl == 5 and begin < 0:
                    st_exp = stack[:-1]
                    begin = i
            elif c == ']':
                stack = stack[:-1]
                if lvl == 5 and end < 0:
                    end = i
                lvl -= 1
            elif c == ',':
                stack[-1] = True
            else:
                if end > 0:
                    break
                if begin < 0:
                    st_l = stack.copy()
        if begin < 0:
            return False
        l_val, r_val = [int(n) for n in s[begin+1:end].split(',')]
        self.set_val(st_l, l_val, True)
        self.set_val(st_exp, 0, False)
        self.set_val(stack, r_val, True)
        return True


    def set_val(self, stack: List[bool], val, add: bool):
        if not stack:
            return
        sn = self
        for s in stack[:-1]:
            sn = sn.r if s else sn.l
        if stack[-1]:
            if add:
                sn.r += val
            else:
                sn.r = val
        else:
            if add:
                sn.l += val
            else:
                sn.l = val


    def split(self) -> bool:
        res = False
        if isinstance(self.l, int):
            if self.l >= 10:
                self.l = Snailfish(self.l // 2, self.l - (self.l // 2))
                return True
        else:
            res = self.l.split()
        if not res:
            if isinstance(self.r, int):
                if self.r >= 10:
                    self.r = Snailfish(self.r // 2, self.r - (self.r // 2))
                    return True
            else:
                return self.r.split()
        return res


    def reduce(self):
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break


    def magnitude(self) -> int:
        l = self.l if isinstance(self.l, int) else self.l.magnitude()
        r = self.r if isinstance(self.r, int) else self.r.magnitude()
        return 3*l + 2*r


    def __str__(self) -> str:
        return f"[{str(self.l)},{str(self.r)}]"


def cast(s: str) -> Union[int, Snailfish]:
    if ',' in s:
        return from_str(s)
    return int(s)


def from_str(s: str) -> Snailfish:
    s = s[1:-1]
    i, lvl = 0, 0
    for i, c in enumerate(s):
        if c == '[':
            lvl += 1
        elif c == ']':
            lvl -= 1
        if c == "," and lvl == 0:
            break
    return Snailfish(cast(s[:i]), cast(s[i+1:]))


def read_input(filename: str = "input.txt") -> List[str]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [l.strip() for l in reader.readlines()]


@show
def first(inp: List[str]) -> int:
    return reduce(lambda x,y: x+y, [from_str(l) for l in inp]).magnitude()


@show
def second(inp: List[str]) -> int:
    res = []
    for i in range(len(inp)-1):
        for j in range(i+1, len(inp)):
            res.append((from_str(inp[i])+from_str(inp[j])).magnitude())
            res.append((from_str(inp[j])+from_str(inp[i])).magnitude())
    return max(res)


def test_example() -> None:
    n = from_str("[[[[[9,8],1],2],3],4]")
    n.explode()
    assert str(n) == "[[[[0,9],2],3],4]"
    n = from_str("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    n.explode()
    assert str(n) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
    assert str(from_str("[[[[4,3],4],4],[7,[[8,4],9]]]") + from_str("[1,1]")) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    assert from_str("[9,1]").magnitude() == 29
    assert from_str("[1,9]").magnitude() == 21
    assert from_str("[[9,1],[1,9]]").magnitude() == 129
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 4140
        assert second(inp) == 3993


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 3654
    second(inp)  # 4578
