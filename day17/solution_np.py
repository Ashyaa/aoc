#!/usr/bin/env python3

import copy
from pathlib import Path
from typing import Dict, List

import numpy as np

CWD = Path(__file__).parent


class Matrix:
    arr = []
    rows: int = 0
    columns: int = 0
    plans: int = 0
    volumes: int = 0


    def __init__(self, rows: int, columns: int, plans: int, volumes: int):
        self.rows = rows
        self.columns = columns
        self.plans = plans
        self.volumes = volumes
        self.cubes = np.zeros((volumes, plans, rows, columns), dtype=bool)


    def set_cell(self, w: int, z: int, row: int, col: int):
        self.cubes[w,z,row,col] = True


    def run(self):
        next_state = np.zeros((self.volumes, self.plans, self.rows, self.columns), dtype=bool)
        it = np.nditer(self.cubes, flags=['multi_index'])
        for cell in it:
            w, z, x, y = it.multi_index
            neighbours_coords = [
                (a,b,c,d)
                for a in range(w-1, w+2) 
                for b in range(z-1, z+2)
                for c in range(x-1, x+2)
                for d in range(y-1, y+2)
                if 0 <= a < self.volumes and
                0 <= b < self.plans and
                0 <= c < self.rows and
                0 <= d < self.columns
            ]
            v = 0
            for n in neighbours_coords:
                try:
                    if self.cubes[n]:
                        v+=1
                except IndexError:
                    pass
            if cell and not 3<=v<=4:
                next_state[w,z,x,y] = False
                continue
            if not cell and v==3:
                next_state[w,z,x,y] = True
                continue
            next_state[w,z,x,y] = cell
        self.cubes = next_state


    def nb_active(self) -> int:
        return list(self.cubes.flatten()).count(True)


    def __str__(self) -> str:
        res = ""
        for w in range(self.volumes):
            res += "\nvolume %d:\n" % (w+1)
            for z in range(self.plans):
                res += "\nplan %d:\n" % (z+1)
                for x in range(self.rows):
                    res += "\n"
                    for y in range(self.columns):
                        res += "#" if self.cubes[w,z,x,y] else "."
        return res


def read_input(hyper: bool) -> Matrix:
    input_file = CWD.joinpath("input.txt")
    tot_volumes = 2*6+1 if hyper else 1
    cur = tot_volumes // 2
    plans = 15
    with open(input_file, "r") as reader:
        rows = len(list(reader.readlines()))
        reader.seek(0)
        columns = len(list(reader.readlines())[0].rstrip())
        reader.seek(0)
        tot_rows = rows + 2*6
        tot_cols = columns + 2*6
        m = Matrix(tot_rows, tot_cols, plans, tot_volumes)
        for row, line in enumerate(list(reader.readlines())):
            for col, char in enumerate(list(line.rstrip())):
                if char == "#":
                    m.set_cell(cur, plans//2, 6+row, 6+col)
        return m


def first() -> int:
    m = read_input(False)
    for _ in range(6):
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
