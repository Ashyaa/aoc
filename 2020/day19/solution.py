from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Set, Tuple

import numpy as np

CWD = Path(__file__).parent


def list_sub_rules(rule: str) -> List[List[int]]:
    tmp = [r.strip() for r in rule.split('|')]
    sub_rules = [r.split(" ") for r in tmp]
    return [[int(v) for v in rule] for rule in sub_rules]


def update_sub_rule(sub_rule: List[int], k: int, val: List[str], res=None) -> List:
    if res is None:
        res = [[]]
    for i, n in enumerate(sub_rule):
        if n == k:
            tmp = []
            for v in val:
                r2 = deepcopy(res)
                for r in r2:
                    r.append(v)
                tmp.extend(update_sub_rule(sub_rule[i+1:], k, val, r2))
            res = tmp
            break
        else:
            for r in res:
                r.append(n)
    return res


def update_rule(rule: List[List[int]], k: int, val: List[str]) -> List:
    res = []
    for sub_r in rule:
        tmp = []
        if k in set(sub_r):
            tmp.extend(update_sub_rule(sub_r, k, val))
        else:
            tmp = [sub_r]
        res.extend(tmp)
    return res


def parse_rules(raw: List[str], second: bool=False) -> List[List[str]]:
    nb_rules = len(raw)
    rules = [None]*nb_rules
    ok_rules = set()
    sub_rules = {}
    for l in raw:
        k, v = l.split(":")
        index = int(k)
        if not '|' in v and '"' in v:
            ok_rules.add(index)
            rules[index] = [v.replace('"', '').replace(" ", "")]
        else:
            cur_sub_rules = list_sub_rules(v)
            rules[index] = cur_sub_rules
            sub_rules[index] = set(np.array(cur_sub_rules).flatten())
    searching = nb_rules-3 if second else nb_rules
    while len(ok_rules) != searching:
        for i in range(nb_rules):
            if second and i in [0,8,11]:
                continue
            if i in ok_rules: 
                continue
            ok_sub_rules = sub_rules[i].intersection(ok_rules)
            if len(ok_sub_rules) == 0:
                continue
            for j in ok_sub_rules:
                rules[i] = update_rule(rules[i], j, rules[j])
                sub_rules[i].remove(j)
            if len(sub_rules[i]) == 0:
                rules[i] = ["".join(sub_r) for sub_r in rules[i]]
                del sub_rules[i]
                ok_rules.add(i)
    return rules


def read_input() -> Tuple[List[List[str]], List[str]]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        rules, lines = reader.read().split("\n\n", maxsplit=1)
        return parse_rules(rules.splitlines()), lines.split("\n")


def first(rules: List[List[str]], lines: List[str]) -> int:
    return len([l for l in lines if l in rules[0]])


def alt_0(rules: List[List[str]], line: str) -> bool:
    nb_char = len(line)
    if nb_char < 24 or nb_char%8 != 0:
        return False
    if line[-8:] not in rules[31]:
        return False
    offset = 1
    nb_42, nb_31 = 0,1
    was_42 = False
    while offset*8 < nb_char: #TODO
        subset = line[nb_char-(8*(offset+1)):nb_char-(8*offset)]
        is_42 = subset in rules[42]
        is_31 = subset in rules[31]
        if not (is_31 or is_42):
            return False
        if was_42 and is_31:
            return False
        was_42 = is_42
        nb_42+= is_42
        nb_31+= is_31
        offset+=1
    return nb_42 > nb_31


def second(rules: List[List[str]], lines: List[str]) -> None:
    
    return len([l for l in lines if alt_0(rules, l)])


def run() -> None:
    rules, lines = read_input()
    print("First step:")
    # step1
    print(first(rules, lines)) # 213
    print("\nSecond step:")
    # step2
    print(second(rules, lines)) # 325