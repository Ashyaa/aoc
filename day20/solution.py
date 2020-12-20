from collections import defaultdict
from functools import reduce
from itertools import product
from math import sqrt
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pprint as pp
import numpy as np

CWD = Path(__file__).parent


def variations(tile: np.ndarray) -> List[np.ndarray]:
    return [np.rot90(tile, k=n) for n in range(4)] + [
        np.rot90(np.fliplr(tile), k=n) for n in range(4)
    ]


class Tile:
    def __init__(self, ID, img):
        self.ID = ID
        self.img = img
        self.b = np.array([[1 if c == "#" else 0 for c in s] for s in img], int)
        self.rotations = variations(self.b)
        assert len(self.rotations) == 8


def read_input() -> Dict[int, List[str]]:
    input_file = CWD.joinpath("example.txt")
    input_file = CWD.joinpath("input.txt")
    res = {}
    with open(input_file, "r") as reader:
        for image in reader.read().split("\n\n"):
            tmp = image.split("\n")
            ID = int(tmp[0][5:-1])
            res[ID] = np.array([list(s) for s in tmp[1:]]).reshape((10,10))
    return res


def is_matching_edge(e: str, og_ID: int, edges: Dict[int, List[str]]) -> List[bool]:
    c1, c2 = 0, 0
    for ID, img_edges in edges.items():
        if ID == og_ID:
            continue
        if e in img_edges:
            c1+=1
        if e[::-1] in img_edges:
            c2+=1
    return [c1==1, c2==1]


def get_edges(ins: Dict[int, List[str]]) -> Dict[int, List[str]]:
    res = defaultdict(list)
    for ID, image in ins.items():
        for k in range(4):
            res[ID].append("".join(np.rot90(image, k)[0]))
    return res


def first(ins: Dict[int, List[str]]) -> int:
    edges = get_edges(ins)
    common_edges = {}
    for ID, img_edges in edges.items():
        common_edges[ID] = [is_matching_edge(e, ID, edges) for e in img_edges]
    locations = {ID: sum([sum(row) for row in np.rot90(common_edges[ID], 1)]) for ID in common_edges}
    return reduce(lambda x, y: x*y, [ID for ID, count in locations.items() if count == 2])


def get_next_empty(grid: Dict[Tuple[int,int],Tuple[int,int]], size: int) -> Tuple[int,int]:
    for r in range(size):
        for c in range(size):
            if grid[r, c] is None:
                return r, c


def get_rotated_tile(pos: Tuple[int,int], tiles_dict: Dict[int,Tile]) -> np.ndarray:
    return tiles_dict[pos[0]].rotations[pos[1]]


def horizontal_fit(left: Tuple[int,int], right: Tuple[int,int], tiles_dict: Dict[int,Tile]) -> bool:
    left_rc = get_rotated_tile(left, tiles_dict)[:, -1]
    right_lc = get_rotated_tile(right, tiles_dict)[:, 0]
    if all(left_rc == right_lc):
        return True
    return False


def vertical_fit(top: Tuple[int,int], bottom: Tuple[int,int], tiles_dict: Dict[int,Tile]) -> bool:
    top_br = get_rotated_tile(top, tiles_dict)[-1, :]
    bottom_tr = get_rotated_tile(bottom, tiles_dict)[0, :]
    if all(top_br == bottom_tr):
        return True
    return False


def get_candidates(grid: Dict[Tuple[int,int],Tuple[int,int]], tiles_left: List[int], location: Tuple[int, int], tiles_dict: Dict[int,Tile]) -> List[Tuple[int,int]]:
    all_positions_left = product(tiles_left, range(8))
    candidates = []
    r, c = location
    if r > 0:
        top_tile = grid[(r - 1, c)]
    else:
        top_tile = None
    if c > 0:
        left_tile = grid[(r, c - 1)]
    else:
        left_tile = None
    for pos in all_positions_left:
        if top_tile is not None:
            if not vertical_fit(top_tile, pos, tiles_dict):
                continue
        if left_tile is not None:
            if not horizontal_fit(left_tile, pos, tiles_dict):
                continue
        candidates.append(pos)
    return candidates


def solve(grid: Dict[Tuple[int,int],Tuple[int,int]], tiles_left: List[int], size: int, tiles_dict: Dict[int,Tile]) -> bool:
    if not tiles_left:
        return True
    location = get_next_empty(grid, size)
    potential_positions = get_candidates(grid, tiles_left, location, tiles_dict)
    while potential_positions:
        t = potential_positions.pop()
        grid[location] = t
        new_tiles_left = [ti for ti in tiles_left if t[0] != ti]
        result = solve(grid, new_tiles_left, size, tiles_dict)
        if result:
            return True
        else:
            grid[location] = None  # remove the tile that did not fit from the grid
    return False


def build_img(grid: Dict[Tuple[int,int],Tuple[int,int]], side_length: int, tiles_dict: Dict[int,Tile]) -> np.ndarray:
    blocks = []
    for r in range(side_length):
        r_blocks = []
        for c in range(side_length):
            pos = grid[(r, c)]
            t = get_rotated_tile(pos, tiles_dict)
            t_strip = t[1:-1, 1:-1]
            r_blocks.append(t_strip)
        blocks.append(np.concatenate(r_blocks, axis=1))
    return np.concatenate(blocks, axis=0)


def count_sea(img: np.ndarray, wanted: np.ndarray):
    monster_height, monster_width = wanted.shape
    height, width = img.shape
    monster_space = np.sum(wanted)
    monsters_found = 0
    for r in range(height - monster_height):
        for c in range(width - monster_width):
            search_space = img[r: r + monster_height, c: c + monster_width]
            assert search_space.shape == wanted.shape
            if np.sum(np.multiply(search_space, wanted)) == monster_space:
                monsters_found += 1
    return np.sum(img) - monsters_found * monster_space


def second(ins: Dict[int, List[str]]) -> None:
    tiles = list()
    for ID, img in ins.items():
        body = [''.join(row) for row in img]
        tiles.append(Tile(ID, body))
    side_length = int(round(sqrt(len(tiles))))
    tiles_dict = {t.ID: t for t in tiles}
    grid = {(r, c): None for r in range(side_length) for c in range(side_length)}
    non_placed_tiles = [t.ID for t in tiles]
    solve(grid, non_placed_tiles, side_length, tiles_dict)
    img = build_img(grid, side_length, tiles_dict)
    wanted = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        ])
    not_monsters = []
    for variation in variations(img):
        not_monsters.append(count_sea(variation, wanted))
    return min(not_monsters)


def run() -> None:
    ins = read_input()
    print("First step:")
    print(first(ins)) # 47213728755493
    print("\nSecond step:")
    print(second(ins))  # step2