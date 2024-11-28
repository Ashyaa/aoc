from pathlib import Path
from shutil import copyfile

YEAR = 2024
CWD = Path(__file__).parent
SOLUTION_GO = "solution_test.go"
EXAMPLE_TXT = "example.txt"
SRC_TEMPLATE = CWD.joinpath(SOLUTION_GO)
EXAMPLE = CWD.joinpath(EXAMPLE_TXT)
YEAR_DIR = CWD.parent.joinpath(f"{YEAR}")


def main():
    for i in range(1, 26):
        day = f"{i:02}"
        directory = YEAR_DIR.joinpath(f"day{day}")
        directory.mkdir(parents=True, exist_ok=True)
        src_file = directory.joinpath(SOLUTION_GO)
        copyfile(SRC_TEMPLATE, src_file)
        copyfile(EXAMPLE, directory.joinpath(EXAMPLE_TXT))
        with src_file.open("r") as f:
            content = f.read().replace("XX", day)
        with src_file.open("w") as f:
            f.write(content)


if __name__ == "__main__":
    main()
