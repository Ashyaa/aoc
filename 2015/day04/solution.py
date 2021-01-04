#!/usr/bin/env python3

import contextlib

from hashlib import md5
from pathlib import Path
# from typing import ...
from AoC.util import show


CWD = Path(__file__).parent


@show
def first(s: str) -> int:
    i = 0
    while True:
        q = s + "%06d" % i
        hash_ = md5(q.encode("UTF-8")).hexdigest()
        if hash_.startswith("00000"):
            return i
        i += 1


@show
def second(s: str) -> None:
    i = 0
    while True:
        q = s + "%06d" % i
        if hash_ = md5(q.encode("UTF-8")).hexdigest().startswith("000000"):
            return i
        i += 1

def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert first("abcdef") == 609043
        assert first("pqrstuv") == 1048970


pzl_input = "ckczppom"
test_example()
first(pzl_input) # 117946
second(pzl_input) # 3938038