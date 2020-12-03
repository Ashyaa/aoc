from pathlib import Path

CWD = Path(__file__).parent


def read_input() -> None:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        for l in reader.readlines():
            # TODO: parse input
            pass


def first() -> None:
    pass


def second() -> None:
    pass


def run() -> None:
    tmp = read_input()
    print("First step:")
    first()
    print("\nSecond step:")
    second()
