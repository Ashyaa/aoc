#!/usr/bin/env python3

import contextlib

from pathlib import Path
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> str:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return reader.read().strip()


@show
def search(inp: str, head_size: int) -> int:
    for i in range(len(inp)):
        if len(set(inp[i:i+head_size])) == head_size:
            return i+head_size
    return -1


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        ex_1  = search("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4)
        assert ex_1 == 7, ex_1
        ex_2  = search("bvwbjplbgvbhsrlpgdmjqwftvncz", 4)
        assert ex_2 == 5, ex_2
        ex_3  = search("nppdvjthqldpwncqszvftbrmjlhg", 4)
        assert ex_3 == 6, ex_3
        ex_4  = search("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4)
        assert ex_4 == 10, ex_4
        ex_5  = search("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4)
        assert ex_5 == 11, ex_5
        ex_6  = search("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14)
        assert ex_6 == 19, ex_6
        ex_7  = search("bvwbjplbgvbhsrlpgdmjqwftvncz", 14)
        assert ex_7 == 23, ex_7
        ex_8  = search("nppdvjthqldpwncqszvftbrmjlhg", 14)
        assert ex_8 == 23, ex_8
        ex_9  = search("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14)
        assert ex_9 == 29, ex_9
        ex_0  = search("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14)
        assert ex_0 == 26, ex_0


test_example()
s = read_input()
search(s, 4)  # 1625
search(s, 14)  # 2250
