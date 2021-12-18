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


    def will_explode(self) -> bool:
        lvl = 0
        for c in str(self):
            if c == '[':
                lvl +=1
            elif c == ']':
                lvl -=1
            if lvl > 4:
                return True
        return False


    def explode(self):
        lvl = 0
        s = str(self)
        begin, end = -1, -1
        for i, c in enumerate(s):
            if c == '[':
                lvl +=1
                if lvl == 5:
                    begin = i
            elif c == ']':
                if lvl == 5:
                    end = i
                    break
                lvl -=1
        left_str, right_str = s[:begin], s[end+1:]
        l_val, r_val = [int(n) for n in s[begin+1:end].split(',')]
        new_str = add_to_str(left_str, l_val, True) + "0" + add_to_str(right_str, r_val, False)
        new_self = from_str(new_str)
        self.l = new_self.l
        self.r = new_self.r


    def will_split(self) -> bool:
        return any(int(n) >= 10 for n in str(self).replace("[", ",").replace("]", ",").split(",") if n != '')

        lsplit, rsplit = False, False
        if isinstance(self.l, int):
            if self.l >= 10:
                lsplit = True
        else:
            lsplit = self.l.will_split()
        if isinstance(self.r, int):
            if self.r >= 10:
                rsplit = True
        else:
            rsplit = self.r.will_split()
        return lsplit or rsplit


    def split(self):
        if isinstance(self.l, int):
            if self.l >= 10:
                self.l = Snailfish(self.l // 2, self.l - (self.l // 2))
                return
        elif self.l.will_split():
            self.l.split()
            return
        if isinstance(self.r, int):
            if self.r >= 10:
                self.r = Snailfish(self.r // 2, self.r - (self.r // 2))
                return
        elif self.r.will_split():
            self.r.split()


    def reduce(self):
        reduced = False
        while not reduced:
            if self.will_explode():
                self.explode()
                continue
            if self.will_split():
                self.split()
                continue
            reduced = True


    def magnitude(self) -> int:
        l = self.l if isinstance(self.l, int) else self.l.magnitude()
        r = self.r if isinstance(self.r, int) else self.r.magnitude()
        return 3*l + 2*r


    def __str__(self) -> str:
        return f"[{str(self.l)},{str(self.r)}]"


def add_to_str(s: str, v: int, left: bool) -> str:
    values = [int(n) for n in s.replace("[", ",").replace("]", ",").split(",") if n != '']
    if not values:
        return s
    wanted = values[-1] if left else values[0]
    new_value = wanted + v
    if left:
        return (s[::-1].replace(str(wanted)[::-1], str(new_value)[::-1], 1))[::-1]
    return s.replace(str(wanted), str(new_value), 1)


def is_valid(s: str) -> bool:
    return s.count('[') == s.count(']')


def cast(s: str) -> Union[int, Snailfish]:
    try:
        return int(s)
    except ValueError:
        return from_str(s)


def from_str(s: str) -> Snailfish:
    l, r = "", ""
    s = s[1:-1]
    for i, c in enumerate(s):
        if c != ",":
            continue
        l, r = s[:i], s[i+1:]
        if is_valid(l) and is_valid(r):
            break
    return Snailfish(cast(l), cast(r))


def read_input(filename: str = "input.txt") -> List[Snailfish]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [from_str(l.strip()) for l in reader.readlines()]


@show
def first(inp: List[Snailfish]) -> int:
    return reduce(lambda x,y: x+y, inp).magnitude()


@show
def second(inp) -> int:
    res = []
    for i in range(len(inp)-1):
        for j in range(i, len(inp)):
            res.append((inp[i]+inp[j]).magnitude())
            res.append((inp[j]+inp[i]).magnitude())
    return max(res)


def test_example() -> None:
    assert add_to_str(",1],2],3],4]", 8, False) == ",9],2],3],4]"
    assert add_to_str("[7,[6,[5,[14,", 3, True) == "[7,[6,[5,[17,"
    n = from_str("[[[[[9,8],1],2],3],4]")
    n.explode()
    assert str(n) == "[[[[0,9],2],3],4]"
    n = from_str("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    n.explode()
    assert str(n) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
    assert str(from_str("[[[[4,3],4],4],[7,[[8,4],9]]]") + from_str("[1,1]")) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
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
