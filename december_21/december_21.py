from pprint import pprint
import time
from functools import lru_cache
from typing import Tuple


def main():
    with open("./december_21/test.txt") as f:
        lines = f.readlines()

    map_ = []
    for line in lines:
        map_.append(list(line.strip()))

        if 'S' in line:
            start = (line.index('S'), len(map_) - 1)


    MOVES = {
        'N': (0, -1),
        'S': (0, 1),
        'E': (1, 0),
        'W': (-1, 0),
    }

    current_branches = set()
    current_branches.add(start)

    init_time = time.time()
    for step in range(64):
        # process all branches and create a new set containing all new branches
        new_branches = set()
        for branch in current_branches:
            for move in MOVES.values():
                new_x = branch[0] + move[0]
                new_y = branch[1] + move[1]
                if new_x < 0 or new_x >= len(map_[0]) or new_y < 0 or new_y >= len(map_):
                    continue
                if map_[new_y][new_x] == '#':
                    continue
                new_branches.add((new_x, new_y))

        current_branches = new_branches

    print(f'Time: {time.time() - init_time}s')
    print(f'Part 1_: {len(new_branches)}')

    # Part 2
    # i think i can solve with only 
    # 1 map, and a counter for each position, same computing, but with a counter on each position
    
    current_branches = set()
    current_branches.add((*start, 0, 0))


    @lru_cache(maxsize=None)
    def step_map(branch: Tuple[int, int]):
        new_branches = []
        for move in MOVES.values():
            new_x = branch[0] + move[0]
            new_y = branch[1] + move[1]
            new_map_id = 0, 0

            # loop around the map
            if new_x < 0:
                new_x = len(map_[0]) - 1
                new_orig_x = -1
            elif new_x >= len(map_[0]):
                new_x = 0
                new_orig_x = 1
            else:
                new_orig_x = 0
            
            new_map_id = new_orig_x, new_map_id[1]

            if new_y < 0:
                new_y = len(map_) - 1
                new_orig_y = 1
            elif new_y >= len(map_):
                new_y = 0
                new_orig_y = -1
            else:
                new_orig_y = 0
            
            new_map_id = new_map_id[0], new_orig_y

            # avoid walls
            if map_[new_y][new_x] == '#':
                continue

            new_branches.append((new_x, new_y, *new_map_id))

        return new_branches

    init_time = time.time()
    for _ in range(500):
        new_branches = set()
        for branch in current_branches:
            point = branch[0:2]
            new_branches_list = step_map(point)
            for new_branch in new_branches_list:
                x, y, new_x, new_y = new_branch
                new_x += branch[2]
                new_y += branch[3]
                new_branches.add((x, y, new_x, new_y))

        current_branches = new_branches  

    print(f'Time: {time.time() - init_time}s')
    print(f'Part 2_: {len(new_branches)}')

if __name__ == "__main__":
    main()