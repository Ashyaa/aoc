from math import prod
from pathlib import Path
from typing import Dict, List, Set, Tuple


CWD = Path(__file__).parent


class Rule:
    ranges: List[Tuple[int,int]]
    name: str

    def __init__(self, line: str):
        self.name, tmp = line.replace(" ","").split(":")
        self.ranges = []
        for s in tmp.split("or"):
            v1, v2 = s.split("-")
            self.ranges.append((int(v1), int(v2)))


    def __repr__(self) -> str:
        return self.name + " " + str(self.ranges)

    def can_fit(self, n: int) -> bool:
        return any([m1<=n<=m2 for m1, m2 in self.ranges])


class Rules:
    rs: List[Rule] = []
    positions: Dict[str, int] = {}


    def add_rule(self, rule):
        self.rs.append(rule)


    def __repr__(self) -> str:
        return " ".join([str(r) for r in self.rs])


    def can_fit(self, n: int) -> bool:
        return any([r.can_fit(n) for r in self.rs])


    def parse_positions(self, ts: List["Ticket"]) -> None:
        set_positions = set()
        cs = []
        for r in self.rs:
            c1 = None
            for t in ts:
                c2 = t.valid_pos(r)
                if c1 is None:
                    c1 = c2
                else:
                    c1 = c1.intersection(c2)
            if len(c1) == 1:
                n = c1.pop()
                set_positions.add(n)
                self.positions[r.name] = n
            cs.append(c1)
        while len(set_positions) != len(self.rs):
            updated = [c - set_positions for c in cs]
            for i, u in enumerate(updated):
                if len(u) == 1:
                    n = u.pop()
                    set_positions.add(n)
                    self.positions[self.rs[i].name] = n


class Ticket:
    fields: List[int] = []


    def __init__(self, line: str):
        self.fields = [int(n) for n in line.split(",")]


    def __repr__(self) -> str:
        return str(self.fields)


    def is_valid(self, rs: Rules) -> bool:
        return all([rs.can_fit(n) for n in self.fields])


    def valid_pos(self, r: Rule) -> Set[int]:
        return set([index for index, n in enumerate(self.fields) if r.can_fit(n)])


    def answer(self, rs: Rules) -> int:
        return prod([self.fields[v] for k, v in rs.positions.items() if k.startswith("departure")])


def read_input() -> Tuple[Rules, Ticket, List[Ticket]]:
    input_file = CWD.joinpath("input.txt")
    rules = Rules()
    with open(input_file, "r") as reader:
        data = reader.read().replace("\n\n", "\n")
        part_1, tmp = data.split("your ticket:\n")
        for l in part_1.splitlines():
            if l == "":
                break
            rules.add_rule(Rule(l))
        my_ticket, others = tmp.split("nearby tickets:\n")

        return rules, Ticket(my_ticket), [Ticket(t) for t in others.split("\n")]


def first(rules: Rules, others: List[Ticket]) -> int:
    invalids = [t for t in others if not t.is_valid(rules)]
    return sum([n for t in invalids for n in t.fields if not rules.can_fit(n)])


def second(rules: Rules, mine: Ticket, others: List[Ticket]) -> None:
    valid_others = [t for t in others if t.is_valid(rules)]
    rules.parse_positions(valid_others)
    return mine.answer(rules)


def run() -> None:
    rules, ticket, others = read_input()
    print("First step:")
    print(first(rules, others)) # 24021
    print("\nSecond step:")
    print(second(rules, ticket, others)) # 1289178686687