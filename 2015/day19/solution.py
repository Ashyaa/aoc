#!/usr/bin/env python3

import contextlib
import sys

from collections import defaultdict
from pathlib import Path
from typing import Dict, KeysView, List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> Tuple[Dict[str, List[str]], str]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = defaultdict(list)
        transfos, molecule = reader.read().split("\n\n")
        for t in transfos.split("\n"):
            src, dst = t.split(" => ", maxsplit=1)
            res[src].append(dst)
        return res, molecule


def process(mol: str, elts: List[str]) -> List[str]:
    tmp = mol
    for e in elts:
        tmp = tmp.replace(e, f"_{e}_")
    tmp = tmp.replace("__", "_")
    if tmp.startswith("_"): tmp = tmp[1:]
    if tmp.endswith("_"): tmp = tmp[:-1]
    return tmp.split("_")


@show
def first(transfos: Dict[str, List[str]], mol: str) -> int:
    comps = process(mol, list(transfos.keys()))
    res = set()
    for i, c in enumerate(comps):
        if c not in transfos: continue
        for new in transfos[c]:
            new_mol = "".join(comps[:i] + [new] + comps[i+1:])
            res.add(new_mol)
    return len(res)


@show
def second(ts: Dict[str, List[str]], mol: str, double: bool=True) -> int:
    """ Solution based of: https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/cy4etju
    Only one solution is possible: any more moves would make a different result, as all
    transformations make the string longer.
    The gist is not to try finding the exact chain of transformations, but figuring out
    a grammar that will make computing the steps trivial.
    Let λ, α, β, ω, ϕ be elements not Ar, Y or Rn. They may be equal between them.
    Transormations are always in the form:
        λ -> αβ (+1 element)
        λ -> α Ar β Rn (+3 elements)
        λ -> α Ar β Y ω Rn (+5 elements)
        λ -> α Ar β Y ω Y ϕ Rn (+5 elements)
    The increase in elements by transformation can then be summarized by the formula:
        1 + count(Ar) + count(Rn) + 2 * count(Y)
    The solution can then be found by reversing this formula to apply it to
    the number of elements in the wanted molecule.
    Double shall be set to false if the transformations from e does not chang ethe number of elements
    ie: e -> α (+0 elements)"""
    comps = process(mol, list(ts.keys())+["Rn", "Y", "Ar"])
    return len(comps) - mol.count("Ar")- mol.count("Rn") - 2 * mol.count("Y") - (1 if double else 0)


def test_example() -> None:
    ex, mol = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        assert mol == "HOH"
        assert first(ex, mol) == 4
        assert first(ex, "HOHOHO") == 7
        assert second(ex, mol, False) == 3
        assert second(ex, "HOHOHO", False) == 6


test_example()
transformations, molecule = read_input()
first(transformations, molecule) # 518
second(transformations, molecule) # 200