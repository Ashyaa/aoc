from pathlib import Path

CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> None:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        for l in reader.readlines():
            # TODO: parse input
            pass


def first() -> None:
    pass


def second() -> None:
    pass


def test_example() -> None:
    ins = read_input("example.txt")
    assert first(ins) == None
    assert second(ins) == None


def run() -> None:
    ins = read_input()
    print("First step:")
    print(first(ins)) # step1
    print("\nSecond step:")
    print(second(ins)) # step2