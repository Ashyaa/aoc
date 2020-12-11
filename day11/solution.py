from pathlib import Path
from typing import Dict, List


CWD = Path(__file__).parent

class Cell:
    neighbours: List[int] = []
    state: str = "."
    prev_state: str = ""
    next_state: str = ""
    row: int
    col: int


    def __init__(self, row: int, col: int, state: str, neighbours: List[int]):
        self.row = row
        self.col = col
        self.state = state
        self.neighbours = neighbours


    def set_neighbours(self, neighbours: List[int]) -> None:
        self.neighbours = neighbours


    def is_empty(self):
        return self.state == "L"


    def is_occupied(self):
        return self.state == "#"


    def run(self, cur_state: List['Cell'], tol: int) -> None:
        if self.state == ".":
            self.next_state = "."
            return
    
        cn = [cur_state[n] for n in self.neighbours]
        if self.is_empty() and len([n for n in cn if n.is_occupied()]) == 0:
            self.next_state = "#"
            return

        if self.is_occupied() and len([n for n in cn if n.is_occupied()]) >= tol:
            self.next_state = "L"
            return
        self.next_state = self.state


    def advance(self):
        self.prev_state = self.state
        self.state = self.next_state
        self.next_state = ""


    def is_stale(self):
        return self.prev_state == self.state


class Matrix:
    cells: List[Cell] = []
    rows: int = 0
    colums: int = 0


    def __init__(self, rows: int, columns: str):
        self.rows = rows
        self.columns = columns


    def add_cell(self, row: int, col: int, state: str):
        neighbours = []
        for i in range(-1,2):
            r = row+i
            for j in range(-1,2):
                if i == j == 0:
                    continue
                c = col + j
                if 0 <= r < self.rows and 0 <= c < self.columns:
                    neighbours.append(r*self.columns+c)
        self.cells.append(Cell(row, col, state, neighbours))


    def run(self, tol: int):
        for c in self.cells:
            c.run(self.cells, tol)
        for c in self.cells:
            c.advance()


    def update_neighbours(self) -> None:
        for i, c in enumerate(self.cells):
            c.set_neighbours([n for n in self.neighbours(i)])


    def neighbours(self, index: int) -> List[int]:
        for i in range(-1,2):
            for j in range(-1,2):
                if i == j == 0:
                    continue
                r = self.axis(index, i, j)
                if r is not None:
                    yield r


    def axis(self, index, v, h: int) -> int:
        op = lambda x: (v*self.columns) + x + h
        i, r, c = op(index), (index // self.columns) + v, (index % self.columns) + h
        while 0 <= r < self.rows and 0 <= c < self.columns:
            if self.cells[i].state != ".":
                return i
            i, r, c = op(i), r+v, c+h


    def is_stale(self):
        return all([c.is_stale() for c in self.cells])


    def nb_occupied(self) -> int:
        return len([c for c in self.cells if c.is_occupied()])


    def __str__(self) -> str:
        res = ""
        for c in self.cells:
            if c.col == 0:
                res += "\n"
            res += c.state
        return res


def read_input() -> Matrix:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        rows = len(list(reader.readlines()))
        reader.seek(0)
        columns = len(list(reader.readlines())[0].rstrip())
        reader.seek(0)
        m = Matrix(rows, columns)
        for row, line in enumerate(list(reader.readlines())):
            for col, char in enumerate(list(line.rstrip())):
                m.add_cell(row, col, char)
        return m


def first(matrix: Matrix) -> int:
    while not matrix.is_stale():
        matrix.run(4)
    return matrix.nb_occupied()


def second(matrix: Matrix) -> int:
    matrix.update_neighbours()
    while not matrix.is_stale():
        matrix.run(5)
    return matrix.nb_occupied()


def run() -> None:
    matrix = read_input()
    print("First step:")
    # # 2093
    print(first(matrix))
    print("\nSecond step:")
    # 1862
    print(second(matrix))