#!/usr/bin/env python3

import contextlib

from collections import deque

from pathlib import Path
from typing import Dict, Union
from AoC.util import show


CWD = Path(__file__).parent
OPS = {
    "*": "/",
    "/": "*",
    "-": "+",
    "+": "-",
    "(": ")",
    ")": "(",
}

def to_postfix(exp: str) -> str:
    stack = []
    output = []
    i = 0
    while i < len(exp):
        char = exp[i]
        if char not in OPS:
            wd = char
            if i < len(exp) -1:
                c2 = exp[i+1]
                while c2 not in OPS:
                    wd += c2
                    i += 1
                    c2 = exp[i+1]
            output.append(wd)
        elif char=='(':
            stack.append('(')
        elif char==')':
            while stack and stack[-1]!= '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.append(char)
        i += 1
    while stack:
        output.append(stack.pop())
    return " ".join(output)


class BET:
    def __init__(self, elt: str) -> None:
        self.d = elt
        self.left: Union[BET,None] = None
        self.right: Union[BET,None] = None

    def humn(self) -> bool:
        if self.right is None and self.left is None:
            return self.d == "humn"
        return self.left.humn() or self.right.humn()

    def infix(self) -> str:
        if self.right is None and self.left is None:
            return self.d
        return f"({self.left.infix()} {self.d} {self.right.infix()})"


def createTree(exp: str) -> BET:
    s = deque()
    words = exp.split(" ")
    root = BET(words[-1])
    s.appendleft(root)
    for elt in reversed(words[:-1]):
        curr_node = s[0]
        if not curr_node.right:
            node = BET(elt)
            curr_node.right = node
            if elt in OPS:
                s.appendleft(node)
        else:
            node = BET(elt)
            curr_node.left = node
            s.popleft()
            if elt in OPS:
                s.appendleft(node)
    return root


def read_input(filename: str = "input.txt") -> Dict[str,Union[int,str]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        res = {}
        for l in reader.read().splitlines():
            s = l.split(": ")
            res[s[0]] = int(s[1]) if len(s[1]) < 3 else s[1]
        return res


def expr(inp: Dict[str,Union[int,str]], key: str, lcls: Dict[str,str], p2: bool = False) -> str:
    if key == "humn":
        lcls[key] = key
        if not p2:
            lcls[key] = f"{int(inp[key])}"
        return lcls[key]
    if isinstance(inp[key], int):
        lcls[key] = f"{inp[key]}"
        return f"{inp[key]}"
    args = inp[key].split(" ")
    if args[0] in lcls:
        args[0] = lcls[args[0]]
    else:
        args[0] = expr(inp, args[0], lcls, p2)
    if args[2] in lcls:
        args[2] = lcls[args[2]]
    else:
        args[2] = expr(inp, args[2], lcls, p2)
    res = "(" + " ".join(args) + ")"
    lcls[key] = res
    return res


@show
def run_1(inp: Dict[str,Union[int,str]]) -> int:
    exp = expr(inp, "root", {})
    return int(eval(exp, None, None))


@show
def run_2(inp: Dict[str,Union[int,str]]) -> int:
    inp["root"] = inp["root"].replace("+", "==")
    exp = expr(inp, "root", {}, True)
    t = exp[1:-1].split(" == ")
    goal = int(eval(t[1]))
    tree = createTree(to_postfix(t[0].replace(" ", "")))

    while tree.d != "humn":
        op = OPS[tree.d]
        l, r = tree.left, tree.right
        negate = False
        if tree.right.humn():
            if tree.d == "-":
                op = "-"
                negate = True
            if tree.d == "/":
                op = "/"
                negate = True
            tree, subgoal = r, l
        else:
            tree, subgoal = l, r
        n = int(eval(subgoal.infix(), None, None))
        goal = int(eval(f"{goal} {op} {n}", None, None))
        if negate:
            if op == "-":
                goal *= -1
            else:
                goal = 1 / goal
    return goal


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = run_1(inp)
        assert r1 == 152, r1
        r2  = run_2(inp)
        assert r2 == 301, r2


# test_example()
inp = read_input()
assert run_1(inp) == 276156919469632
assert run_2(inp) == 3441198826073
