from pathlib import Path
from typing import Dict, List, Tuple


CWD = Path(__file__).parent
MY_BAG = "shiny gold bag"


def parse_elements(elements: str) -> List[Tuple[int, str]]:
    res = []
    for elt in elements.split(", "):
        count, bag = elt.split(" ", maxsplit=1)
        if count == "no":
            break
        res.append((int(count), bag))
    return res


def parse_line(line: str) -> Tuple[str, List[Tuple[int, str]]]:
    key, elements = line.split(" contain ", maxsplit=1)
    return key, parse_elements(elements)


def read_input() -> Dict[str,List[Tuple[int, str]]]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        couples = [parse_line(l.rstrip().replace(".", "").replace("bags", "bag")) for l in reader.readlines()]
        return {key: value for key, value in couples}


def contains_bag(bag: str, wanted: str, rules: Dict[str, List[Tuple[int, str]]]) -> bool:
    for _, b in rules[bag]:
        if b == wanted:
            return True
        if contains_bag(b, wanted, rules):
            return True
    return False


def is_holding(bag: str, rules: Dict[str, List[Tuple[int, str]]]) -> int:
    if len(rules[bag]) == 0:
        return 0
    return sum([qty + qty * is_holding(b, rules) for qty, b in rules[bag]])


def first(rules: Dict[str, List[Tuple[int, str]]]) -> int:
    return len([b for b  in rules.keys() if contains_bag(b, MY_BAG, rules)])


def second(rules: Dict[str, List[Tuple[int, str]]]) -> int:
    return is_holding(MY_BAG, rules)


def run() -> None:
    rules = read_input()
    print("First step:")
    print(first(rules))
    print("\nSecond step:")
    print(second(rules))