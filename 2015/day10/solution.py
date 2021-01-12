#!/usr/bin/env python3
import contextlib

from pathlib import Path
from AoC.util import show


CWD = Path(__file__).parent


def look_and_say(s: str) -> str:
    index, res = 0, ""
    while index < len(s):
        char, count = s[index], 1
        index +=1
        while index < len(s) and s[index] == char:
          index += 1
          count += 1
        res += f"{count}{char}"
    return res


@show
def solution(s: str, count: int) -> int:
    for _ in range(count):
        s = look_and_say(s)
    return len(s)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert look_and_say("1") == "11"
        assert look_and_say("11") == "21"
        assert look_and_say("21") == "1211"
        assert look_and_say("1211") == "111221"
        assert look_and_say("111221") == "312211"


test_example()
solution("3113322113", 40) # 329356
solution("3113322113", 50) # 4666278