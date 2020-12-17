#!/usr/bin/env python3

import copy

from pathlib import Path
from typing import Dict, List


CWD = Path(__file__).parent


class Cell:
    neighbours: List[int] = []
    state: int = 0
    prev_state: int = 0
    next_state: int = -1
    row: int
    col: int


    def __init__(self, row: int, col: int, state: int, neighbours: List[int]):
        self.row = row
        self.col = col
        self.state = state
        self.neighbours = neighbours


    def is_active(self):
        return self.state == 1


    def active_neighbours(self, cur_state: List['Cell']) -> int:
        cn = [cur_state[n] for n in self.neighbours]
        return len([n for n in cn if n.is_active()])


    def advance(self):
        self.prev_state = self.state
        self.state = self.next_state
        self.next_state = -1


    def is_stale(self):
        return self.prev_state == self.state


class Matrix:
    cubes = List[List[List[Cell]]]
    rows: int = 0
    columns: int = 0
    plans: int = 0
    volumes: int = 0


    def __init__(self, rows: int, columns: int, plans: int, volumes: int):
        self.rows = rows
        self.columns = columns
        self.plans = plans
        self.volumes = volumes
        self.cubes = []
        for v in range(volumes):
          self.cubes.append([])
          for _ in range(plans):
              self.cubes[v].append([])


    def add_cell(self, z: int, w: int, row: int, col: int, state: int):
        neighbours = []
        for i in range(-1,2):
            r = row+i
            for j in range(-1,2):
                c = col + j
                if 0 <= r < self.rows and 0 <= c < self.columns:
                    neighbours.append(r*self.columns+c)
        self.cubes[w][z].append(Cell(row, col, state, neighbours))


    def new_volume(self, index: int):
        for z in range(self.plans):
          for x in range(self.rows):
            for y in range(self.columns):
                self.add_cell(z, index, x, y, 0)


    def inflate(self) -> None:
      for j in range(self.plans//2):
        for row in range(self.rows):
          for col in range(self.columns):
            self.add_cell(j, self.volumes//2, row, col, 0)
            self.add_cell(-j-1, self.volumes//2, row, col, 0)
      for v in range(self.volumes//2):
        self.new_volume(v)
        self.new_volume(-v-1)


    def active_plan_neighbours(self, c: Cell, z: int, cur_vol: int):
        res = 0
        if z > 0:
            res += c.active_neighbours(self.cubes[cur_vol][z-1])
        res += c.active_neighbours(self.cubes[cur_vol][z])
        if z < self.plans-1:
            res += c.active_neighbours(self.cubes[cur_vol][z+1])
        return res


    def active_neighbours(self, c: Cell, z: int, w: int) -> int:
        res = 0
        if w > 0:
            res += self.active_plan_neighbours(c, z, w-1)
        res += self.active_plan_neighbours(c, z, w)
        if w < self.volumes-1:
            res += self.active_plan_neighbours(c, z, w+1)
        return res


    def run(self):
        for j, cube in enumerate(self.cubes):
          for i, p in enumerate(cube):
              for c in p:
                  v = self.active_neighbours(c, i, j)
                  if c.is_active() and not (3 <= v <= 4):
                      c.next_state = 0
                      continue
                  if not c.is_active() and v == 3:
                      c.next_state = 1
                      continue
                  c.next_state = c.state
        for cube in self.cubes:
            for p in cube:
                for c in p:
                    c.advance()


    def nb_active(self) -> int:
        return len([c for cube in self.cubes for p in cube for c in p if c.is_active()])


    def __str__(self) -> str:
        res = ""
        for j, cube in enumerate(self.cubes):
            res += "\nvolume %d:\n" % (j+1)
            for i, p in enumerate(cube):
              res += "plan %d:\n" % (i+1)
              for c in p:
                  if c.col == 0:
                      res += "\n"
                  res += str(c.state)
            res += "\n"
        return res


def read_input(hyper: bool) -> Matrix:
    input_file = CWD.joinpath("input.txt")
    with open(input_file, "r") as reader:
        rows = len(list(reader.readlines()))
        reader.seek(0)
        columns = len(list(reader.readlines())[0].rstrip())
        reader.seek(0)
        tot_rows = rows + 2*6
        tot_cols = columns + 2*6
        tot_volumes = 2*6+1 if hyper else 1
        cur = tot_volumes // 2
        m = Matrix(tot_rows, tot_cols, 15, tot_volumes)
        for i in range(6):
            for j in range(tot_cols):
                m.add_cell(7, cur, i, j, 0)
        for row, line in enumerate(list(reader.readlines())):
            for j in range(6):
                m.add_cell(7, cur, 6+row, j, 0)
            for col, char in enumerate(list(line.rstrip())):
                m.add_cell(7, cur, 6+row, 6+col, 1 if char == "#" else 0)
            for j in range(tot_cols-6, tot_cols):
                m.add_cell(7, cur, 6+row, j, 0)
        for i in range(tot_rows-6, tot_rows):
            for j in range(tot_cols):
                m.add_cell(7, cur, i, j, 0)
        m.inflate()
        return m


def first() -> int:
    m = read_input(False)
    for i in range(6):
        m.run()
    return m.nb_active()


def second() -> int:
    m = read_input(True)
    for _ in range(6):
        m.run()
    return m.nb_active()


def run() -> None:
    print("First step:") # 265
    print(first())
    print("\nSecond step:")
    print(second()) # 1936


if __name__ == "__main__":
    run()