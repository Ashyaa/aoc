#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List, Dict
from AoC.util import show


CWD = Path(__file__).parent


class Node:
    name: str
    __children: Dict[str, "Node"]
    __size: int


    def __init__(self, name, size):
        self.name = name
        self.__children = {}
        self.__size = size


    @property
    def is_dir(self) -> bool:
        return len(self.__children) > 0


    @property
    def children(self) -> List["Node"]:
        return self.__children.values()


    def size(self):
        if self.__size < 0:
            self.__size = sum(c.size() for c in self.children)
        return self.__size


    def add_child(self, name: List[str], size: str) -> None:
        if len(name) > 1:
            self.__children[name[0]].add_child(name[1:], size)
        else:
            self.__children[name[0]] = Node(name[0], -1 if size == "dir" else int(size))


    def print(self, level: int = 0) -> None:
        print(f"{'  '* level}{self.name} ({self.size()})")
        for c in self.children:
            c.print(level+1)


    def walk(self):
        yield self
        for c in self.children:
            for n in c.walk():
                yield n


def parse(lines: List[str]) -> Node:
    res = Node("/", -1)
    cwd = []
    idx = 0

    while idx < len(lines):
        words = lines[idx].split()
        if words[1] == "cd":
            cwd = cwd[:-1] if words[2] == ".." else cwd + [words[2]]
            idx += 1
        else:
            idx += 1
            while idx < len(lines) and not lines[idx].startswith("$"):
                words = lines[idx].split()
                res.add_child(cwd + [words[1]], words[0])
                idx += 1
    return res


def read_input(filename: str = "input.txt") -> Node:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return parse(reader.read().split("\n")[1:])


@show
def first(tree: Node) -> int:
    return sum(n.size() for n in tree.walk() if n.is_dir and n.size() <= 100000)


@show
def second(tree: Node) -> int:
    free_space = 70000000 - tree.size()
    return min(n.size() for n in tree.walk() if n.is_dir and n.size() + free_space >= 30000000)


def test_example() -> None:
    inp = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        r1  = first(inp)
        assert r1 == 95437, r1
        r2  = second(inp)
        assert r2 == 24933642, r2


test_example()
s = read_input()
first(s)  # 2061777
second(s)  # 4473403
