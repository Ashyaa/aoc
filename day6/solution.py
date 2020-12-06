from pathlib import Path
from typing import List

CWD = Path(__file__).parent


def read_input() -> List[str]:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        return reader.read().split("\n\n")


def group_count(survey: str) -> int:
    return len({c: True for c in survey})


def first(surveys: List[str]) -> int:
    return sum([group_count("".join(survey.split())) for survey in surveys])


def intersection_length(survey: List[str]) -> int:
    sets = [set(entry) for entry in survey]
    return len(sets[0].intersection(*sets[1:]))


def second(surveys: List[str]) -> int:
    return sum([intersection_length(survey.split("\n")) for survey in surveys])


def run() -> None:
    surveys = read_input()
    print("First step:")
    count_sum = first(surveys)
    print("Count sum: %d" % count_sum)
    print("\nSecond step:")
    count_sum_2 = second(surveys)
    print("Count sum: %d" % count_sum_2)
