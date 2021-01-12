#!/usr/bin/env python3

import contextlib
import json

from pathlib import Path
from typing import Dict
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> Dict:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return json.load(reader)


def json_sum(data, ignore_red=False) -> int:
    if isinstance(data, str):
        return 0
    elif isinstance(data, list):
        return sum([v if isinstance(v, int) else json_sum(v, ignore_red) for v in data])
    else: # dict
        if ignore_red and "red" in data.values():
            return 0
        return sum([v if isinstance(v, int) else json_sum(v, ignore_red) for v in data.values()])


@show
def first(data: Dict) -> int:
    return json_sum(data)


@show
def second(data: Dict) -> int:
    return json_sum(data, True)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert first(json.loads('[1,2,3]')) == first(json.loads('{"a":2,"b":4}')) == 6
        assert first(json.loads('[[[3]]]')) == first(json.loads('{"a":{"b":4},"c":-1}')) == 3
        assert first(json.loads('{"a":[-1,1]}')) == first(json.loads('[-1,{"a":1}]')) == 0
        assert first(json.loads('[]')) == first(json.loads('{}')) == 0
        assert second(json.loads('[1,2,3]')) == 6
        assert second(json.loads('[1,{"c":"red","b":2},3]')) == 4
        assert second(json.loads('{"d":"red","e":[1,2,3,4],"f":5}')) == 0
        assert second(json.loads('[1,"red",5]')) == 6


test_example()
data = read_input()
first(data) # 119433
second(data) # 68466
