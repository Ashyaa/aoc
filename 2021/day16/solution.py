#!/usr/bin/env python3

import contextlib

from functools import reduce
from pathlib import Path

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> str:
    with open(CWD.joinpath(filename), "r") as reader: return reader.readline().strip()


to_bin_str = lambda s: "".join(format(int(c, 16), '04b') for c in s)


class Packet:
    ver: int
    typ: int
    subpackets: List = []
    remainder: str = ""
    _value: int = -1


    def __init__(self, inp: str) -> None:
        self.ver, self.typ = int(inp[0:3], 2), int(inp[3:6], 2)
        if self.typ == 4:
            self.remainder, self._value = type4(inp[6:])
        else:
            if inp[6] == '1':
                self.remainder, self.subpackets = subpackets1(inp[18:], int(inp[7:18], 2))
            else:
                self.remainder, self.subpackets = subpackets0(inp[22:], int(inp[7:22], 2))


    def version(self):
        return self.ver + sum(sp.version() for sp in self.subpackets)


    def value(self):
        OPERATORS = {
          0: lambda: sum(sp.value() for sp in self.subpackets), # sum
          1: lambda: reduce(lambda x,y: x*y, [sp.value() for sp in self.subpackets]), # product
          2: lambda: min(sp.value() for sp in self.subpackets), # min
          3: lambda: max(sp.value() for sp in self.subpackets), # max
          4: lambda: self._value, # value
          5: lambda: self.subpackets[0].value() > self.subpackets[1].value(), # gt
          6: lambda: self.subpackets[0].value() < self.subpackets[1].value(), # lt
          7: lambda: self.subpackets[0].value() == self.subpackets[1].value(), # eq
        }
        return OPERATORS[self.typ]()


def type4(inp: str) -> Tuple[str, int]:
    s, end = "", False
    while not end:
        end = inp[0] == '0'
        s += inp[1:5]
        inp = inp[5:]
    return inp, int(s, 2)


def subpackets0(inp: str, bitlen: int) -> Tuple[str, List[Packet]]:
    res, s = [], inp[:bitlen]
    while s:
      res.append(Packet(s))
      s = res[-1].remainder
    return inp[bitlen:], res


def subpackets1(inp: str, nb: int) -> Tuple[str, List[Packet]]:
    res, s = [], inp
    for _ in range(nb):
        res.append(Packet(s))
        s = res[-1].remainder
    return s, res


@show
def first(inp: str) -> int:
    return Packet(to_bin_str(inp)).version()


@show
def second(inp: str) -> int:
    return Packet(to_bin_str(inp)).value()


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert first("D2FE28") == 6
        assert first("38006F45291200") == 9
        assert first("EE00D40C823060") == 14
        assert first("8A004A801A8002F478") == 16
        assert first("620080001611562C8802118E34") == 12
        assert first("C0015000016115A2E0802F182340") == 23
        assert first("A0016C880162017C3686B18A3D4780") == 31
        assert second("C200B40A82") == 3
        assert second("04005AC33890") == 54
        assert second("880086C3E88112") == 7
        assert second("CE00C43D881120") == 9
        assert second("D8005AC2A8F0") == 1
        assert second("F600BC2D8F") == 0
        assert second("9C005AC2F8F0") == 0
        assert second("9C0141080250320F1802104A08") == 1


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 847
    second(inp)  # 333794664059
